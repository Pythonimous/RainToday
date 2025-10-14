import pytest
import requests
from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


@pytest.mark.integration
def test_geocode_endpoint_success(monkeypatch):
    """Test /geocode returns correct lat/lon for a valid city name using Open-Meteo geocoding."""

    def mock_get(url, params, timeout):
        class MockResponse:
            def json(self):
                return {
                    "results": [
                        {"latitude": 51.5074, "longitude": -0.1278, "name": "London"}
                    ]
                }

            @property
            def status_code(self):
                return 200

        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    response = client.get("/geocode", params={"city": "London"})
    assert response.status_code == 200
    data = response.json()
    assert data["lat"] == 51.5074
    assert data["lon"] == -0.1278
    assert data["name"] == "London"


@pytest.mark.integration
def test_geocode_endpoint_not_found(monkeypatch):
    """Test /geocode returns 404 if city is not found."""

    def mock_get(url, params, timeout):
        class MockResponse:
            def json(self):
                return {"results": []}

            @property
            def status_code(self):
                return 200

        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    response = client.get("/geocode", params={"city": "Nowhereville"})
    assert response.status_code == 404
