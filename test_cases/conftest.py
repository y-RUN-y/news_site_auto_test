import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, sync_playwright

from common.base_page import BasePage
from common.conf_loader import config

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


@pytest.fixture(scope="class")
def context(browser: Browser):
    with browser.new_context() as context:
        yield context


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    with BasePage(context.new_page()) as page:
        yield page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 运行所有其他钩子以获取报告对象
    outcome = yield
    rep = outcome.get_result()
    # 仅当处于测试调用阶段且测试失败时处理
    if rep.when == "call" and rep.failed:
        # 尝试找到测试使用的 Playwright page fixture
        page = None
        try:
            if "page" in item.fixturenames:
                page = item.funcargs.get("page", None)
        except Exception:
            page = None

        if page is not None:
            try:
                allure.attach.file(
                    page.take_screenshot("error_screenshot"),
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass
