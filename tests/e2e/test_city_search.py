"""
End-to-end tests for city search functionality.
"""
import re
import pytest
from playwright.sync_api import Page, expect, Route


@pytest.mark.e2e
def test_city_search_flow(app_page: Page) -> None:
    """Test searching for a city and getting weather results."""

    # Mock the geocode endpoint
    def handle_geocode(route: Route) -> None:
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"lat": 51.5074, "lon": -0.1278, "city": "London"}'
        )

    # Mock the rain endpoint
    def handle_rain(route: Route) -> None:
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"condition": "no_rain", "message": "No rain expected today!"}'
        )

    app_page.route("**/geocode?*", handle_geocode)
    app_page.route("**/rain?*", handle_rain)

    # Enter city name
    city_input = app_page.locator("#city-input")
    city_input.fill("London")

    # Click search button
    search_button = app_page.locator("#city-search-btn")
    search_button.click()

    # Wait for result to appear
    result_div = app_page.locator("#result")
    expect(result_div).to_contain_text("No rain expected today!", timeout=5000)

    # Verify background changed
    body = app_page.locator("body")
    expect(body).to_have_class(re.compile(r"bg-blue-200"))


@pytest.mark.e2e
def test_city_search_empty_input(app_page: Page) -> None:
    """Test that submitting empty city name shows an error."""
    # Leave city input empty and click search
    search_button = app_page.locator("#city-search-btn")
    search_button.click()

    # Should show validation message
    result_div = app_page.locator("#result")
    expect(result_div).to_have_text("Please enter a city name.")


@pytest.mark.e2e
def test_city_search_geocode_failure(app_page: Page) -> None:
    """Test handling of geocoding API failure."""

    # Mock geocode endpoint with error
    def handle_geocode_error(route: Route) -> None:
        route.fulfill(status=404, body="Not found")

    app_page.route("**/geocode?*", handle_geocode_error)

    # Enter city and search
    city_input = app_page.locator("#city-input")
    city_input.fill("NonexistentCity123")

    search_button = app_page.locator("#city-search-btn")
    search_button.click()

    # Should show error message
    result_div = app_page.locator("#result")
    expect(result_div).to_contain_text("Could not find city", timeout=5000)


@pytest.mark.e2e
def test_city_search_with_special_characters(app_page: Page) -> None:
    """Test city search with special characters and spaces."""

    # Mock the endpoints
    def handle_geocode(route: Route) -> None:
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"lat": 48.8566, "lon": 2.3522, "city": "Paris"}'
        )

    def handle_rain(route: Route) -> None:
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"condition": "maybe", "message": "Maybe some drizzle?"}'
        )

    app_page.route("**/geocode?*", handle_geocode)
    app_page.route("**/rain?*", handle_rain)

    # Enter city with spaces
    city_input = app_page.locator("#city-input")
    city_input.fill("São Paulo")

    search_button = app_page.locator("#city-search-btn")
    search_button.click()

    # Verify result appears
    result_div = app_page.locator("#result")
    expect(result_div).to_contain_text("Maybe some drizzle?", timeout=5000)

    # Verify background changed to yellow (maybe condition)
    body = app_page.locator("body")
    expect(body).to_have_class(re.compile(r"bg-yellow-100"))
