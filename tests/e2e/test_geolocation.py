"""
End-to-end tests for the main "Will it rain today?" button with geolocation.

Note: These tests mock browser geolocation API since we can't grant real
permissions in automated tests.
"""
import re
import pytest
from playwright.sync_api import Page, expect, Route


@pytest.mark.e2e
def test_geolocation_button_with_granted_permission(app_page: Page) -> None:
    """Test the main button when geolocation permission is granted."""

    # Grant geolocation permission and set coordinates
    context = app_page.context
    context.grant_permissions(["geolocation"])
    context.set_geolocation({"latitude": 51.5074, "longitude": -0.1278})

    # Mock the rain endpoint
    def handle_rain(route: Route) -> None:
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"condition": "no_rain", "message": "Sunny skies!"}'
        )

    app_page.route("**/rain?*", handle_rain)

    # Click the main button
    rain_button = app_page.locator("#rain-btn")
    rain_button.click()

    # Should show "Getting your location..." first, then result
    result_div = app_page.locator("#result")
    expect(result_div).to_contain_text("Sunny skies!", timeout=5000)

    # Verify background changed
    body = app_page.locator("body")
    expect(body).to_have_class(re.compile(r"bg-blue-200"))


@pytest.mark.e2e
def test_geolocation_button_api_error(app_page: Page) -> None:
    """Test handling when the rain API returns an error."""

    # Grant geolocation
    context = app_page.context
    context.grant_permissions(["geolocation"])
    context.set_geolocation({"latitude": 40.7128, "longitude": -74.0060})

    # Mock rain endpoint with error
    def handle_rain_error(route: Route) -> None:
        route.fulfill(status=500, body="Internal server error")

    app_page.route("**/rain?*", handle_rain_error)

    # Click the button
    rain_button = app_page.locator("#rain-btn")
    rain_button.click()

    # Should show error message
    result_div = app_page.locator("#result")
    expect(result_div).to_contain_text("Could not fetch weather data", timeout=5000)


@pytest.mark.e2e
def test_geolocation_button_with_denied_permission(app_page: Page) -> None:
    """Test the fallback behavior when geolocation permission is denied."""

    # Deny geolocation permission
    context = app_page.context
    context.grant_permissions([])  # No permissions granted

    # Click the button
    rain_button = app_page.locator("#rain-btn")
    rain_button.click()

    # Should show fallback message
    result_div = app_page.locator("#result")
    expect(result_div).to_contain_text("Location access denied", timeout=5000)

    # City input should be focused
    city_input = app_page.locator("#city-input")
    expect(city_input).to_be_focused()


@pytest.mark.e2e
def test_geolocation_coordinates_precision(app_page: Page) -> None:
    """Test that coordinates are sent with appropriate precision."""

    requests_received: list[str] = []

    # Grant geolocation with specific coordinates
    context = app_page.context
    context.grant_permissions(["geolocation"])
    context.set_geolocation({"latitude": 51.507351, "longitude": -0.127758})

    def handle_rain(route: Route) -> None:
        requests_received.append(route.request.url)
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"condition": "no_rain", "message": "Clear!"}'
        )

    app_page.route("**/rain?*", handle_rain)

    # Click the button
    rain_button = app_page.locator("#rain-btn")
    rain_button.click()

    # Wait for result
    result_div = app_page.locator("#result")
    expect(result_div).to_contain_text("Clear!", timeout=5000)

    # Verify coordinates were sent with 4 decimal precision
    assert len(requests_received) > 0
    url = requests_received[0]
    assert "lat=51.5074" in url  # Rounded to 4 decimals
    assert "lon=-0.1278" in url  # Rounded to 4 decimals
