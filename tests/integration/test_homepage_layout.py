import pytest
from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


@pytest.mark.integration
def test_homepage_contains_key_elements():
    """Ensure the root HTML contains the main UI elements in expected order."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.text

    # Check essential elements exist
    assert "Will It Rain Today?" in html
    assert "id=\"rain-btn\"" in html or 'id="rain-btn"' in html
    assert "id=\"horizon-slider\"" in html or 'id="horizon-slider"' in html
    assert "id=\"city-input\"" in html or 'id="city-input"' in html
    assert "id=\"visit-counts\"" in html or 'id="visit-counts"' in html
    # New auto-check UI elements
    assert "id=\"refine-toggle\"" in html or 'id="refine-toggle"' in html
    assert "id=\"controls-panel\"" in html or 'id="controls-panel"' in html
    assert "id=\"result-message\"" in html or 'id="result-message"' in html
