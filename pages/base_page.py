import logging
import os
from datetime import datetime

from playwright.sync_api import Page, TimeoutError


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open_url(self, url, retry_times=3):
        retried_times = 0
        while retried_times <= retry_times:
            try:
                self.page.goto(url, timeout=3000)
            except TimeoutError as e:
                retried_times += 1
                if retried_times <= retry_times:
                    logging.info("正在重试……已重连%d次", retried_times)
                else:
                    logging.error("跳转到 %s 失败，超过重试次数", url)
                    raise
            else:
                logging.info("跳转到：%s", url)
                break

    def get_url(self):
        return self.page.url

    def get_title(self):
        return self.page.title()

    def locate(self, selector):
        try:
            return self.page.locator(selector)
        except Exception as e:
            logging.error("定位元素%s失败，错误为：%s", selector, e)
            return None

    def take_screenshot(self, name="screenshot"):
        os.makedirs("./screenshots", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"./screenshots/{name}_{timestamp}.png"
        logging.info("已截图：%s", path)
        return self.page.screenshot(path=path, full_page=False)
