import logging
from datetime import datetime

from playwright.sync_api import Page, TimeoutError

from utils.conf_loader import project_root


class BasePage:
    def __init__(self, page: Page, timeout: int = 3000):
        self.page = page
        self.default_timeout = timeout

    def open_url(self, url: str, retry_times: int = 3):
        """打开 URL，内置重试机制"""
        retried_times = 0
        while retried_times <= retry_times:
            try:
                self.page.goto(url, timeout=self.default_timeout)
                logging.info("跳转到：%s", url)
                return
            except TimeoutError:
                retried_times += 1
                if retried_times <= retry_times:
                    logging.info("正在重试……已重试%d次", retried_times)
                else:
                    logging.error("跳转到 %s 失败，超过重试次数", url)
                    raise

    def get_url(self) -> str:
        """获取当前页面 URL"""
        return self.page.url

    def get_title(self) -> str:
        """获取当前页面标题"""
        return self.page.title()

    def locate(self, selector: str):
        return self.page.locator(selector)

    def get_by_text(self, text: str, exact: bool = False):
        return self.page.get_by_text(text, exact=exact)

    def take_screenshot(self, name: str = "screenshot"):
        """截图并保存到 ./screenshots/"""
        screenshots_dir = project_root / "screenshots"
        screenshots_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = str(screenshots_dir / f"{name}_{timestamp}.png")
        logging.info("已截图：%s", path)
        self.page.screenshot(path=path, full_page=False)
        return path
