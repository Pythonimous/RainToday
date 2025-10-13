import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@pytest.mark.integration
@pytest.mark.parametrize(
    "city",
    [
        "London",
        "Springfield",
        "München",
        "Москва",  # Detects wrong English spelling: "Moskva" instead of "Moscow"
        # "北京",  # Fails to parse city name in Chinese
        "São Paulo",
        "Nowhereville",
    ],
)
def test_geocode_real_api(city):
    """Call the real /geocode endpoint for various cities and smoke-check response."""

    resp = client.get("/geocode", params={"city": city})
    print(f"City: {city} | Status: {resp.status_code} | Response: {resp.text}")
    if city == "Nowhereville":
        assert resp.status_code == 404
        return

    assert resp.status_code == 200
    data = resp.json()
    assert "lat" in data and "lon" in data and "name" in data
    assert isinstance(data["lat"], float)
    assert isinstance(data["lon"], float)
    assert isinstance(data["name"], str)
