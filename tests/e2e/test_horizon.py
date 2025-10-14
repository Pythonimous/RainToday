"""
End-to-end tests for horizon slider functionality.
"""
import pytest
from playwright.sync_api import Page, expect, Route


@pytest.mark.e2e
def test_horizon_slider_changes_label(app_page: Page) -> None:
    """Test that moving the slider updates the label text."""
    slider = app_page.locator("#horizon-slider")
    label = app_page.locator("#horizon-label")

    # Initial state should be "Today"
    expect(label).to_have_text("Today")

    # Move to position 1 (1h)
    slider.fill("1")
    expect(label).to_have_text("1h")

    # Move to position 2 (3h)
    slider.fill("2")
    expect(label).to_have_text("3h")

    # Move to position 3 (6h)
    slider.fill("3")
    expect(label).to_have_text("6h")

    # Move back to position 0 (Today)
    slider.fill("0")
    expect(label).to_have_text("Today")


@pytest.mark.e2e
def test_horizon_affects_rain_query(app_page: Page) -> None:
    """Test that horizon setting is passed to the rain endpoint."""

    # Track the horizon parameter in requests
    requests_received: list[str] = []

    def handle_geocode(route: Route) -> None:
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"lat": 40.7128, "lon": -74.0060, "city": "New York"}'
        )

    def handle_rain(route: Route) -> None:
        # Capture the horizon parameter from the URL
        url = route.request.url
        requests_received.append(url)
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"condition": "rain", "message": "Yes, bring an umbrella!"}'
        )

    app_page.route("**/geocode?*", handle_geocode)
    app_page.route("**/rain?*", handle_rain)

    # Open the refine panel
    refine_toggle = app_page.locator("#refine-toggle")
    refine_toggle.click()

    # Set slider to "3h"
    slider = app_page.locator("#horizon-slider")
    slider.fill("2")

    # Verify label updated
    label = app_page.locator("#horizon-label")
    expect(label).to_have_text("3h")

    # Search for a city
    city_input = app_page.locator("#city-input")
    city_input.fill("New York")

    search_button = app_page.locator("#city-search-btn")
    search_button.click()

    # Wait for result
    result_message = app_page.locator("#result-message")
    expect(result_message).to_contain_text("Yes, bring an umbrella!", timeout=5000)

    # Verify the rain endpoint was called with horizon=3h
    assert len(requests_received) > 0
    assert "horizon=3h" in requests_received[0]


@pytest.mark.e2e
def test_horizon_1h_parameter(app_page: Page) -> None:
    """Test that selecting 1h horizon passes correct parameter."""

    requests_received: list[str] = []

    def handle_geocode(route: Route) -> None:
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"lat": 51.5074, "lon": -0.1278, "city": "London"}'
        )

    def handle_rain(route: Route) -> None:
        requests_received.append(route.request.url)
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"condition": "no_rain", "message": "Clear skies ahead!"}'
        )

    app_page.route("**/geocode?*", handle_geocode)
    app_page.route("**/rain?*", handle_rain)

    # Open the refine panel
    refine_toggle = app_page.locator("#refine-toggle")
    refine_toggle.click()

    # Set slider to "1h"
    slider = app_page.locator("#horizon-slider")
    slider.fill("1")

    # Search
    city_input = app_page.locator("#city-input")
    city_input.fill("London")

    search_button = app_page.locator("#city-search-btn")
    search_button.click()

    # Wait for result
    result_message = app_page.locator("#result-message")
    expect(result_message).to_contain_text("Clear skies ahead!", timeout=5000)

    # Verify horizon=1h was sent
    assert len(requests_received) > 0
    assert "horizon=1h" in requests_received[0]
