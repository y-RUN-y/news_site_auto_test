from pages.base_page import BasePage


class MainPage(BasePage):
    # 搜索
    INPUT_BOX = "input"
    SEARCH_BTN = '//span[text()="搜索"]'
    SEARCH_SUG_LIST = ".qqcom-search-sug .sug-list .sug-item"

    def get_search_suggestions(self):
        items = self.locator(self.SEARCH_SUG_LIST).all()
        return [item.inner_text() for item in items]

    # 顶部导航栏
    NAV_ITEM = ".nav-item"  # 顶部分类按钮
    NAV_LINK = ".nav-link"
    MORE_ITEM_DROPDOWN = ".rc-dropdown"
    MORE_ITEM = ".more-item"

    # 文本定位（使用 get_by_text 显式定位）
    POP_UP_CLOSE_BTN = "知道了"

    def go_main_page(self):
        self.open_url("https://www.qq.com")

    def close_popup(self):
        """关闭弹窗"""
        self.get_by_text(self.POP_UP_CLOSE_BTN).click()
        return self
