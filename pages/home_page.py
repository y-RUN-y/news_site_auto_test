from pages.base_page import BasePage


class HomePage(BasePage):
    INPUT_BOX = "input"
    SEARCH_BTN = '//span[text()="搜索"]'

    def gohome(self):
        self.open_url("https://www.qq.com")
