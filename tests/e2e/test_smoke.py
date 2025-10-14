"""
End-to-end smoke test: verify the application loads and basic elements are present.
"""
import re
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_homepage_loads(app_page: Page) -> None:
    """Verify the homepage loads with all essential elements."""
    # Check the page title
    expect(app_page).to_have_title("Will It Rain Today?")

    # Check main heading
    heading = app_page.locator("h1")
    expect(heading).to_have_text("Will It Rain Today?")

    # Check city input form elements
    city_input = app_page.locator("#city-input")
    expect(city_input).to_be_visible()
    expect(city_input).to_have_attribute("placeholder", "Enter city name...")

    search_button = app_page.locator("#city-search-btn")
    expect(search_button).to_be_visible()
    expect(search_button).to_have_text("Check")

    # Check horizon slider
    horizon_slider = app_page.locator("#horizon-slider")
    expect(horizon_slider).to_be_visible()
    expect(horizon_slider).to_have_attribute("min", "0")
    expect(horizon_slider).to_have_attribute("max", "3")

    # Check horizon label
    horizon_label = app_page.locator("#horizon-label")
    expect(horizon_label).to_be_visible()
    expect(horizon_label).to_have_text("Today")

    # Check result container exists (even if empty)
    result_div = app_page.locator("#result")
    expect(result_div).to_be_attached()


@pytest.mark.e2e
def test_initial_background_color(app_page: Page) -> None:
    """Verify the page starts with the default indigo background."""
    body = app_page.locator("body")
    expect(body).to_have_class(re.compile(r"bg-indigo-100"))
