import logging
import typing
from datetime import datetime
from typing import Literal, Union

from playwright.sync_api import Locator, Page, TimeoutError

from common.conf_loader import project_root


class BasePage:
    BLACK = "rgb(51, 51, 51)"
    BLUE = "rgb(48, 113, 242)"

    def __init__(self, page: Union[Page, "BasePage"], timeout: int = 15000):
        self._page = page.page if isinstance(page, BasePage) else page
        self.default_timeout = timeout

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def close(self):
        self._page.close()

    @property
    def page(self):
        return self._page

    def open_url(self, url: str, retry_times: int = 3):
        """打开 URL，内置重试机制"""
        retried_times = 0
        while retried_times <= retry_times:
            try:
                self._page.goto(
                    url, timeout=self.default_timeout, wait_until="domcontentloaded"
                )
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
        return self._page.url

    def get_title(self) -> str:
        """获取当前页面标题"""
        return self._page.title()

    def wait_for_timeout(self, timeout=50):
        self._page.wait_for_timeout(timeout)

    def wait_for_load_state(
        self,
        state: typing.Optional[
            Literal["domcontentloaded", "load", "networkidle"]
        ] = None,
    ):
        self._page.wait_for_load_state()

    @property
    def mouse(self):
        return self._page.mouse

    def locator(self, selector: str):
        return self._page.locator(selector)

    def get_by_text(self, text: str, exact: bool = False):
        return self._page.get_by_text(text, exact=exact)

    def go_to_iframe_by_name(self, name):
        return self.page.frame(name=name)

    def get_response(self, url: str):
        """获取指定URL的响应对象"""
        with self._page.expect_response(
            lambda response: response.url == url
        ) as response_info:
            self._page.goto(url, timeout=self.default_timeout)
        return response_info.value

    def take_screenshot(self, el: Locator = None, name: str = "screenshot"):
        """截图并保存到 ./screenshots/"""
        self._page.wait_for_load_state("domcontentloaded", timeout=10000)
        screenshots_dir = project_root / "screenshots"
        screenshots_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = str(screenshots_dir / f"{name}_{timestamp}.png")
        if el is not None:
            # 若存在定位器，则对组件所在区域截图
            el.scroll_into_view_if_needed()
            box = el.bounding_box()
            self._page.screenshot(
                path=path,
                clip={
                    "x": box["x"],
                    "y": box["y"],
                    "height": box["height"],
                    "width": box["width"],
                },
            )
        else:
            self._page.screenshot(path=path, full_page=False)
        logging.info("已截图：%s", path)
        return path
