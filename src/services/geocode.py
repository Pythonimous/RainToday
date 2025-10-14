"""Geocoding service that wraps calls to the Open-Meteo search API."""
from __future__ import annotations

from typing import Any, Dict

import requests


class GeocodeServiceError(RuntimeError):
    """Raised when the geocoding service is unavailable or returns invalid data."""


class CityNotFoundError(GeocodeServiceError):
    """Raised when no results are returned for the provided city name."""


_GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"


def search_city(city: str) -> Dict[str, Any]:
    """Lookup city coordinates via Open-Meteo.

    Args:
        city: The name of the city to search for.

    Raises:
        CityNotFoundError: When no results are returned.
        GeocodeServiceError: For network or parsing failures.
    """
    params: Dict[str, str | int] = {
        "name": city,
        "count": 1,
        "language": "auto",
        "format": "json",
    }

    try:
        response = requests.get(_GEOCODE_URL, params=params, timeout=5)
    except Exception as exc:  # noqa: BLE001
        raise GeocodeServiceError("Geocoding API error") from exc

    status_code = getattr(response, "status_code", 200)
    if status_code == 404:
        raise CityNotFoundError(f"City '{city}' not found")
    if status_code >= 400:
        raise GeocodeServiceError("Geocoding API returned an error (status >= 400)")

    try:
        payload = response.json()
    except Exception as exc:  # noqa: BLE001
        raise GeocodeServiceError("Failed to decode geocoding response") from exc

    results = payload.get("results", []) if isinstance(payload, dict) else []
    if not results:
        raise CityNotFoundError(f"City '{city}' not found")

    result = results[0]
    try:
        latitude = result["latitude"]
        longitude = result["longitude"]
    except KeyError as exc:  # noqa: PERF203
        raise GeocodeServiceError("Geocoding API returned malformed data") from exc

    return {
        "lat": latitude,
        "lon": longitude,
        "name": result.get("name", city),
    }
