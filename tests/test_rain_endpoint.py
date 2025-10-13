import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


import json
import requests

def test_rain_endpoint_valid_params(monkeypatch):
    """Test /rain with valid lat, lon, and horizon returns correct rain logic from Open-Meteo API."""

    # Simulate Open-Meteo API response for heavy rain
    def mock_get(url, params, timeout):
        class MockResponse:
            def json(self):
                return {
                    "hourly": {
                        "precipitation_probability": [80, 90, 95],
                        "precipitation": [0.6, 1.2, 0.8]
                    }
                }
            @property
            def status_code(self):
                return 200
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    response = client.get("/rain", params={"lat": 40.7128, "lon": -74.0060, "horizon": "3h"})
    assert response.status_code == 200
    data = response.json()
    assert data["will_rain"] is True
    assert data["condition"] == "rain"
    assert "message" in data

    # Simulate Open-Meteo API response for no rain
    def mock_get_no_rain(url, params, timeout):
        class MockResponse:
            def json(self):
                return {
                    "hourly": {
                        "precipitation_probability": [5, 10, 15],
                        "precipitation": [0.0, 0.0, 0.0]
                    }
                }
            @property
            def status_code(self):
                return 200
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get_no_rain)
    response = client.get("/rain", params={"lat": 40.7128, "lon": -74.0060, "horizon": "3h"})
    assert response.status_code == 200
    data = response.json()
    assert data["will_rain"] is False
    assert data["condition"] == "no_rain"
    assert "message" in data

    # Simulate Open-Meteo API response for maybe
    def mock_get_maybe(url, params, timeout):
        class MockResponse:
            def json(self):
                return {
                    "hourly": {
                        "precipitation_probability": [40, 50, 55],
                        "precipitation": [0.1, 0.2, 0.0]
                    }
                }
            @property
            def status_code(self):
                return 200
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get_maybe)
    response = client.get("/rain", params={"lat": 40.7128, "lon": -74.0060, "horizon": "3h"})
    assert response.status_code == 200
    data = response.json()
    assert data["will_rain"] is False
    assert data["condition"] == "maybe"
    assert "message" in data

def test_rain_endpoint_missing_params():
    """Test /rain returns 422 for missing required parameters."""
    response = client.get("/rain", params={"lat": 40.7128})
    assert response.status_code == 422

def test_rain_endpoint_invalid_params():
    """Test /rain returns 422 for invalid parameter types."""
    response = client.get("/rain", params={"lat": "foo", "lon": "bar", "horizon": "baz"})
    assert response.status_code == 422

def test_rain_endpoint_real_api():
    """Test /rain endpoint with a real Open-Meteo API call, verifying all fields and types."""
    response = client.get("/rain", params={"lat": 40.7128, "lon": -74.0060, "horizon": "3h"})
    assert response.status_code == 200
    data = response.json()
    # Check required fields
    assert "will_rain" in data
    assert "condition" in data
    assert "message" in data
    assert "lat" in data
    assert "lon" in data
    assert "horizon" in data
    # Check types
    assert isinstance(data["will_rain"], bool)
    assert data["condition"] in {"rain", "no_rain", "maybe"}
    assert isinstance(data["message"], str)
    assert isinstance(data["lat"], float)
    assert isinstance(data["lon"], float)
    assert isinstance(data["horizon"], str)
    assert data["horizon"] in {"today", "1h", "3h", "6h"}


def test_rain_endpoint_matches_geoapi():
    """Test /rain endpoint output matches rain logic applied to direct Open-Meteo API response."""
    lat, lon = 40.7128, -74.0060
    for horizon_str, hours in [("1h", 1), ("3h", 3), ("6h", 6), ("today", 24)]:
        # Query Open-Meteo API directly
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "precipitation_probability,precipitation",
            "forecast_days": 1,
            "timezone": "auto"
        }
        resp = requests.get(url, params=params, timeout=5)
        data = resp.json()
        precip_prob = data.get("hourly", {}).get("precipitation_probability", [])[:hours]
        precip_mm = data.get("hourly", {}).get("precipitation", [])[:hours]
        max_prob = max(precip_prob) if precip_prob else 0
        total_mm = sum(precip_mm) if precip_mm else 0
        if max_prob > 60 or total_mm > 0.5:
            expected_condition = "rain"
        elif 30 < max_prob <= 60:
            expected_condition = "maybe"
        else:
            expected_condition = "no_rain"

        # Query our /rain endpoint
        response = client.get("/rain", params={"lat": lat, "lon": lon, "horizon": horizon_str})
        assert response.status_code == 200
        rain_data = response.json()
        assert rain_data["condition"] == expected_condition
        # Optionally, check will_rain field
        if expected_condition == "rain":
            assert rain_data["will_rain"] is True
        else:
            assert rain_data["will_rain"] is False
