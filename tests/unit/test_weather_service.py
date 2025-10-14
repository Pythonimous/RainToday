import pytest

from src.services import weather


class _DummyResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload


@pytest.mark.unit
def test_get_rain_forecast_detects_rain(monkeypatch):
    payload = {
        "hourly": {
            "precipitation_probability": [80, 75, 90],
            "precipitation": [0.6, 1.0, 0.2],
        }
    }

    monkeypatch.setattr(
        weather.requests,
        "get",
        lambda *args, **kwargs: _DummyResponse(payload),
    )
    monkeypatch.setattr(
        weather,
        "pick_message",
        lambda condition: f"message:{condition}",
    )

    result = weather.get_rain_forecast(40.0, -74.0, "3h")

    assert result["will_rain"] is True
    assert result["condition"] == "rain"
    assert result["message"] == "message:rain"
    assert result["hours"] == 3


@pytest.mark.unit
def test_get_rain_forecast_defaults_to_today(monkeypatch):
    payload = {
        "hourly": {
            "precipitation_probability": [5, 15, 25, 10],
            "precipitation": [0.0, 0.0, 0.0, 0.0],
        }
    }

    monkeypatch.setattr(
        weather.requests,
        "get",
        lambda *args, **kwargs: _DummyResponse(payload),
    )
    monkeypatch.setattr(
        weather,
        "pick_message",
        lambda condition: condition,
    )

    result = weather.get_rain_forecast(10.0, 20.0, "invalid")

    assert result["horizon"] == "today"
    assert result["hours"] == 24
    assert result["condition"] == "no_rain"
    assert result["will_rain"] is False


@pytest.mark.unit
def test_get_rain_forecast_raises_on_http_error(monkeypatch):
    monkeypatch.setattr(
        weather.requests,
        "get",
        lambda *args, **kwargs: _DummyResponse({}, status_code=500),
    )

    with pytest.raises(weather.WeatherServiceError):
        weather.get_rain_forecast(0.0, 0.0, "today")


@pytest.mark.unit
def test_get_rain_forecast_raises_on_bad_json(monkeypatch):
    class BadResponse:
        status_code = 200

        def json(self):
            raise ValueError("bad data")

    monkeypatch.setattr(
        weather.requests,
        "get",
        lambda *args, **kwargs: BadResponse(),
    )

    with pytest.raises(weather.WeatherServiceError):
        weather.get_rain_forecast(0.0, 0.0, "today")
