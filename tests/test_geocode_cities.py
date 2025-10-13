import pytest
from fastapi.testclient import TestClient
from app.main import app
import requests

client = TestClient(app)

def mock_geocode(monkeypatch, city, lat, lon, name=None):
    def mock_get(url, params, timeout):
        class MockResponse:
            def json(self):
                if city.lower() in ["london", "londres"]:
                    return {"results": [{"latitude": 51.5074, "longitude": -0.1278, "name": name or "London"}]}
                elif city.lower() == "springfield":
                    return {"results": [{"latitude": 39.7817, "longitude": -89.6501, "name": "Springfield"}]}
                elif city.lower() == "münchen":
                    return {"results": [{"latitude": 48.1374, "longitude": 11.5755, "name": "München"}]}
                elif city.lower() == "北京":
                    return {"results": [{"latitude": 39.9042, "longitude": 116.4074, "name": "北京"}]}
                elif city.lower() == "nowhereville":
                    return {"results": []}
                else:
                    return {"results": [{"latitude": lat, "longitude": lon, "name": name or city}]}
            @property
            def status_code(self):
                return 200
        return MockResponse()
    monkeypatch.setattr(requests, "get", mock_get)

def test_geocode_multiple_cities(monkeypatch):
    # London
    mock_geocode(monkeypatch, "London", 51.5074, -0.1278)
    resp = client.get("/geocode", params={"city": "London"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["lat"] == 51.5074 and data["lon"] == -0.1278

    # Springfield (ambiguous)
    mock_geocode(monkeypatch, "Springfield", 39.7817, -89.6501)
    resp = client.get("/geocode", params={"city": "Springfield"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["lat"] == 39.7817 and data["lon"] == -89.6501

    # München (international)
    mock_geocode(monkeypatch, "München", 48.1374, 11.5755)
    resp = client.get("/geocode", params={"city": "München"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["lat"] == 48.1374 and data["lon"] == 11.5755

    # 北京 (Beijing, unicode)
    mock_geocode(monkeypatch, "北京", 39.9042, 116.4074)
    resp = client.get("/geocode", params={"city": "北京"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["lat"] == 39.9042 and data["lon"] == 116.4074

    # Not found
    mock_geocode(monkeypatch, "Nowhereville", 0, 0)
    resp = client.get("/geocode", params={"city": "Nowhereville"})
    assert resp.status_code == 404
    data = resp.json()
    assert data["detail"] == "City not found"
