import pytest
from playwright.sync_api import Browser, sync_playwright

from utils.conf_loader import config

pwcfg = config["playwright"]


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        if pwcfg["platform"] == "webkit":
            browser = p.webkit.launch(**pwcfg["launch_options"])
        elif pwcfg["platform"] == "firefox":
            browser = p.firefox.launch(**pwcfg["launch_options"])
        else:
            browser = p.chromium.launch(**pwcfg["launch_options"])
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser: Browser):
    page = browser.new_page()
    yield page
    page.close()