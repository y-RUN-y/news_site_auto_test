from pages.base_page import BasePage


class HomePage(BasePage):
    # 搜索
    INPUT_BOX = "input"
    SEARCH_BTN = '//span[text()="搜索"]'

    # 顶部导航栏
    NAV_ITEM = ".nav-link"  # 顶部分类按钮

    MORE_ITEM_DROPDOWN = ".rc-dropdown"

    # 文本定位（使用 get_by_text 显式定位）
    POP_UP_CLOSE_BTN = "知道了"

    def gohome(self):
        self.open_url("https://www.qq.com")

    def get_nav_list(self):
        """获取导航栏元素，返回 Locator 对象"""
        return self.locate(self.NAV_LIST)

    def close_popup(self):
        """关闭弹窗"""
        self.get_by_text(self.POP_UP_CLOSE_BTN).click()
        return self
