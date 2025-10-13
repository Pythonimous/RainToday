"""
End-to-end test for visitor counter display and behavior.

Note: Persistence across server restarts is tested at the integration
layer (test_stats_endpoint.py and test_stats_persistence.py) to avoid
fragile server management in E2E tests.
"""
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_visit_counts_display(app_page: Page) -> None:
    """
    Verify that visit counts are displayed correctly on page load.

    The page increments the counter automatically when loaded via
    JavaScript calling the /visit endpoint.
    """
    # Wait for the visit count elements to be visible
    total_visits = app_page.locator("#total-visits")
    today_visits = app_page.locator("#today-visits")

    expect(total_visits).to_be_visible()
    expect(today_visits).to_be_visible()

    # Verify they contain numeric values (not "Loading...")
    expect(total_visits).not_to_have_text("Loading...")
    expect(today_visits).not_to_have_text("Loading...")

    # Verify they are positive integers
    total_text = total_visits.text_content() or "0"
    today_text = today_visits.text_content() or "0"

    assert total_text.isdigit(), "Total visits should be a number"
    assert today_text.isdigit(), "Today visits should be a number"
    assert int(total_text) >= 0, "Total visits should be non-negative"
    assert int(today_text) >= 0, "Today visits should be non-negative"
