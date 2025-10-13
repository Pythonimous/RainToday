"""
Pytest configuration and fixtures for end-to-end tests.
"""
import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def base_url() -> str:
    """Base URL for the application during E2E tests."""
    return "http://localhost:8000"


@pytest.fixture
def app_page(page: Page, base_url: str) -> Page:
    """Navigate to the application homepage before each test."""
    page.goto(base_url)
    return page


# Configure default timeout for E2E tests
expect.set_options(timeout=10_000)  # 10 seconds
