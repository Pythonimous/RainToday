import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.services import geocode as geocode_service
from src.services import weather as weather_service


client = TestClient(app)


class _DummyResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload


@pytest.mark.integration
def test_geocode_success(monkeypatch):
    def fake_get(url, params, timeout):
        return _DummyResponse({
            "results": [
                {"latitude": 51.5074, "longitude": -0.1278, "name": "London"}
            ]
        })

    monkeypatch.setattr(geocode_service.requests, "get", fake_get)

    response = client.get("/geocode", params={"city": "London"})
    assert response.status_code == 200
    payload = response.json()
    assert payload == {"lat": 51.5074, "lon": -0.1278, "name": "London"}


@pytest.mark.integration
def test_geocode_not_found(monkeypatch):
    def fake_get(url, params, timeout):
        return _DummyResponse({"results": []})

    monkeypatch.setattr(geocode_service.requests, "get", fake_get)

    response = client.get("/geocode", params={"city": "Nowhereville"})
    assert response.status_code == 404


@pytest.mark.integration
def test_geocode_service_error(monkeypatch):
    def fake_get(url, params, timeout):
        raise RuntimeError("boom")

    monkeypatch.setattr(geocode_service.requests, "get", fake_get)

    response = client.get("/geocode", params={"city": "Paris"})
    assert response.status_code == 502


@pytest.mark.integration
def test_rain_endpoint_reports_rain(monkeypatch):
    def fake_get(url, params, timeout):
        return _DummyResponse({
            "hourly": {
                "precipitation_probability": [80, 90, 95],
                "precipitation": [0.7, 1.1, 0.5],
            }
        })

    monkeypatch.setattr(weather_service.requests, "get", fake_get)
    monkeypatch.setattr(weather_service, "pick_message", lambda condition: f"msg:{condition}")

    response = client.get("/rain", params={"lat": 40.7128, "lon": -74.0060, "horizon": "3h"})
    assert response.status_code == 200
    data = response.json()
    assert data["condition"] == "rain"
    assert data["will_rain"] is True
    assert data["message"] == "msg:rain"
    assert data["hours"] == 3


@pytest.mark.integration
def test_rain_endpoint_handles_service_error(monkeypatch):
    def fake_get(url, params, timeout):
        return _DummyResponse({}, status_code=500)

    monkeypatch.setattr(weather_service.requests, "get", fake_get)

    response = client.get("/rain", params={"lat": 0.0, "lon": 0.0, "horizon": "today"})
    assert response.status_code == 502
