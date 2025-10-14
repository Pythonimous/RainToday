"""
E2E: Refine panel toggle/collapse and single input
"""
import pytest
from playwright.sync_api import Page, expect
import re


@pytest.mark.e2e
def test_refine_toggle_open_close_escape(app_page: Page):
    """Refine toggle opens/closes panel, Escape closes it."""
    app_page.goto(app_page.url)
    refine_toggle = app_page.locator("#refine-toggle")
    controls_panel = app_page.locator("#controls-panel")
    # Initially collapsed
    expect(controls_panel).to_have_class(re.compile(r"panel-collapsed"))
    # Open
    refine_toggle.click()
    expect(controls_panel).to_have_class(re.compile(r"panel-open"))
    # Close with Escape
    app_page.keyboard.press("Escape")
    expect(controls_panel).to_have_class(re.compile(r"panel-collapsed"))
    # Open again, then close by clicking toggle
    refine_toggle.click()
    expect(controls_panel).to_have_class(re.compile(r"panel-open"))
    refine_toggle.click()
    expect(controls_panel).to_have_class(re.compile(r"panel-collapsed"))


@pytest.mark.e2e
def test_single_city_input_when_panel_open(app_page: Page):
    """Only one city input exists when refine panel is open."""
    app_page.goto(app_page.url)
    refine_toggle = app_page.locator("#refine-toggle")
    refine_toggle.click()
    city_inputs = app_page.locator("#city-input")
    expect(city_inputs).to_have_count(1)
