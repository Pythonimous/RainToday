"""
End-to-end tests for background color changes based on weather conditions.
"""
import re
import pytest
from playwright.sync_api import Page, expect, Route


@pytest.mark.e2e
def test_background_rain_condition(app_page: Page) -> None:
    """Test that rain condition changes background to gray."""

    def handle_geocode(route: Route) -> None:
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"lat": 51.5074, "lon": -0.1278, "city": "London"}'
        )

    def handle_rain(route: Route) -> None:
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"condition": "rain", "message": "Yes, it will rain!"}'
        )

    app_page.route("**/geocode?*", handle_geocode)
    app_page.route("**/rain?*", handle_rain)

    # Open the refine panel
    refine_toggle = app_page.locator("#refine-toggle")
    refine_toggle.click()

    # Search for city
    city_input = app_page.locator("#city-input")
    city_input.fill("London")

    search_button = app_page.locator("#city-search-btn")
    search_button.click()

    # Wait for result
    result_message = app_page.locator("#result-message")
    expect(result_message).to_contain_text("Yes, it will rain!", timeout=5000)

    # Verify background is gray for rain
    body = app_page.locator("body")
    expect(body).to_have_class(re.compile(r"bg-gray-200"))


@pytest.mark.e2e
def test_background_no_rain_condition(app_page: Page) -> None:
    """Test that no_rain condition changes background to blue."""

    def handle_geocode(route: Route) -> None:
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"lat": 40.7128, "lon": -74.0060, "city": "New York"}'
        )

    def handle_rain(route: Route) -> None:
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"condition": "no_rain", "message": "No rain today!"}'
        )

    app_page.route("**/geocode?*", handle_geocode)
    app_page.route("**/rain?*", handle_rain)

    # Open the refine panel
    refine_toggle = app_page.locator("#refine-toggle")
    refine_toggle.click()

    # Search for city
    city_input = app_page.locator("#city-input")
    city_input.fill("New York")

    search_button = app_page.locator("#city-search-btn")
    search_button.click()

    # Wait for result
    result_message = app_page.locator("#result-message")
    expect(result_message).to_contain_text("No rain today!", timeout=5000)

    # Verify background is blue for no rain
    body = app_page.locator("body")
    expect(body).to_have_class(re.compile(r"bg-blue-200"))


@pytest.mark.e2e
def test_background_maybe_condition(app_page: Page) -> None:
    """Test that maybe condition changes background to yellow."""

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
            body='{"condition": "maybe", "message": "There might be a chance of rain."}'
        )

    app_page.route("**/geocode?*", handle_geocode)
    app_page.route("**/rain?*", handle_rain)

    # Open the refine panel
    refine_toggle = app_page.locator("#refine-toggle")
    refine_toggle.click()

    # Search for city
    city_input = app_page.locator("#city-input")
    city_input.fill("Paris")

    search_button = app_page.locator("#city-search-btn")
    search_button.click()

    # Wait for result
    result_message = app_page.locator("#result-message")
    expect(result_message).to_contain_text("There might be a chance of rain.", timeout=5000)

    # Verify background is yellow for maybe
    body = app_page.locator("body")
    expect(body).to_have_class(re.compile(r"bg-yellow-100"))


@pytest.mark.e2e
def test_background_transitions_between_conditions(app_page: Page) -> None:
    """Test that background changes correctly when conditions change."""

    def handle_geocode(route: Route) -> None:
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"lat": 51.5074, "lon": -0.1278, "city": "London"}'
        )

    # Start with rain condition
    def handle_rain_first(route: Route) -> None:
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"condition": "rain", "message": "Rainy day!"}'
        )

    app_page.route("**/geocode?*", handle_geocode)
    app_page.route("**/rain?*", handle_rain_first)

    # Open the refine panel
    refine_toggle = app_page.locator("#refine-toggle")
    refine_toggle.click()

    # First search - rain
    city_input = app_page.locator("#city-input")
    city_input.fill("London")

    search_button = app_page.locator("#city-search-btn")
    search_button.click()

    result_message = app_page.locator("#result-message")
    expect(result_message).to_contain_text("Rainy day!", timeout=5000)

    body = app_page.locator("body")
    expect(body).to_have_class(re.compile(r"bg-gray-200"))

    # Now change to no_rain condition
    def handle_no_rain(route: Route) -> None:
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"condition": "no_rain", "message": "All clear now!"}'
        )

    app_page.unroute("**/rain?*")
    app_page.route("**/rain?*", handle_no_rain)

    # Second search - no rain
    city_input.fill("London")
    search_button.click()

    expect(result_message).to_contain_text("All clear now!", timeout=5000)

    # Background should now be blue
    expect(body).to_have_class(re.compile(r"bg-blue-200"))
