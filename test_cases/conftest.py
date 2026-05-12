import allure
import pytest


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
