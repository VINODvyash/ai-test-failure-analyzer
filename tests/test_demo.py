from playwright.sync_api import Page


def test_open_website(page: Page):
    # page.goto("https://demowebshop.tricentis.com/")
    page.goto("https://www.amazon.in/")

    #assert "Demo Web Shop" in page.title()
    assert "Amazon Shopping" in page.title()