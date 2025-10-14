"""Weather service utilities built on top of Open-Meteo."""
from __future__ import annotations

from typing import Any, Dict, Iterable, Tuple

import requests

from src.services.messages import pick_message


class WeatherServiceError(RuntimeError):
    """Raised when the weather service cannot provide a forecast."""


_HORIZON_MAP: Dict[str, int] = {
    "today": 24,
    "1h": 1,
    "3h": 3,
    "6h": 6,
}

_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def _resolve_horizon(horizon: str) -> Tuple[str, int]:
    """Return the canonical horizon name and hours window."""
    if horizon in _HORIZON_MAP:
        return horizon, _HORIZON_MAP[horizon]
    return "today", _HORIZON_MAP["today"]


def _build_params(lat: float, lon: float) -> Dict[str, float | int | str]:
    return {
        "latitude": lat,
        "longitude": lon,
        "hourly": "precipitation_probability,precipitation",
        "forecast_days": 1,
        "timezone": "auto",
    }


def _safe_sequence(raw: Any) -> Iterable[float]:
    if isinstance(raw, list):
        return [float(item) for item in raw if isinstance(item, (int, float))]
    return []


def _determine_condition(
    precip_prob: Iterable[float],
    precip_mm: Iterable[float],
) -> Tuple[bool, str]:
    max_prob = max(precip_prob, default=0.0)
    total_mm = sum(precip_mm)

    if max_prob > 60 or total_mm > 0.5:
        return True, "rain"
    if 30 < max_prob <= 60:
        return False, "maybe"
    return False, "no_rain"


def get_rain_forecast(lat: float, lon: float, horizon: str) -> Dict[str, Any]:
    """Fetch and evaluate weather data for the given coordinates."""
    horizon_name, hours = _resolve_horizon(horizon)
    params = _build_params(lat, lon)

    try:
        response = requests.get(_WEATHER_URL, params=params, timeout=5)
    except Exception as exc:  # noqa: BLE001
        raise WeatherServiceError("Weather API error") from exc

    status_code = getattr(response, "status_code", 200)
    if status_code >= 400:
        raise WeatherServiceError("Weather API returned an error (status >= 400)")

    try:
        payload = response.json()
    except Exception as exc:  # noqa: BLE001
        raise WeatherServiceError("Failed to decode weather response") from exc

    hourly = payload.get("hourly", {}) if isinstance(payload, dict) else {}
    precip_prob = list(
        _safe_sequence(hourly.get("precipitation_probability", []))
    )[:hours]
    precip_mm = list(
        _safe_sequence(hourly.get("precipitation", []))
    )[:hours]

    will_rain, condition = _determine_condition(precip_prob, precip_mm)
    message = pick_message(condition)

    return {
        "will_rain": will_rain,
        "condition": condition,
        "message": message,
        "lat": lat,
        "lon": lon,
        "horizon": horizon_name,
        "hours": hours,
    }
