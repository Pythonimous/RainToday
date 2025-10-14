import pytest
import requests
from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


@pytest.mark.integration
def test_rain_endpoint_valid_params(monkeypatch):
    """Ensure /rain reports rain when API indicates heavy precipitation."""

    # Simulate Open-Meteo API response for heavy rain
    def mock_get(url, params, timeout):
        class MockResponse:
            def json(self):
                return {
                    "hourly": {
                        "precipitation_probability": [80, 90, 95],
                        "precipitation": [0.6, 1.2, 0.8],
                    }
                }

            @property
            def status_code(self):
                return 200

        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    response = client.get(
        "/rain",
        params={"lat": 40.7128, "lon": -74.0060, "horizon": "3h"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["will_rain"] is True
    assert data["condition"] == "rain"
    assert "message" in data
