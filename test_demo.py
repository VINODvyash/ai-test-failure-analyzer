import pytest
# from playwright.sync_api import page


def test_google_search_failure(page):
    # Navigating to Google
    page.goto("https://www.google.com")

    # This element does not exist, so Playwright will time out and fail
    page.locator("#non-existent-button-12345").click(timeout=2000)