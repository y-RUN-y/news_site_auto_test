import allure

from pages.home_page import HomePage


class TestHomePage:
    @allure.title("打开腾讯新闻首页")
    @allure.description("验证腾讯新闻首页能否正常打开")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://www.qq.com", name="腾讯新闻")
    def test_open_home_page(self, page):
        home = HomePage(page)
        home.gohome()

        assert "qq.com" in home.get_url()
        assert home.get_title() != ""
