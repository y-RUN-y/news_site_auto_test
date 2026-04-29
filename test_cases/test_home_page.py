import allure
import pytest

from pages.home_page import HomePage


@allure.title("打开腾讯新闻首页")
@allure.description("验证腾讯新闻首页能否正常打开")
@allure.severity(allure.severity_level.BLOCKER)
@allure.link("https://www.qq.com", name="腾讯新闻")
@pytest.mark.completed
def test_open_home_page(page):
    home = HomePage(page)
    with allure.step("打开首页"):
        home.gohome()
    with allure.step("验证网址是否正确"):
        assert "qq.com" in home.get_url()
    with allure.step("验证网站标题是否正确"):
        assert home.get_title() == "腾讯网"
    # 添加截图附件
    allure.attach.file(
        home.take_screenshot(), attachment_type=allure.attachment_type.PNG
    )

@allure.title('测试顶部分类导航栏')
@pytest.mark.inprogress
def test_nav_bar(page):
    home = HomePage(page)
    home.gohome()

    items = home.locate(home.NAV_ITEM)
    print(items.first.text_content())
    # for item in items.all():
    #     item.hover()
    #     print(item.text_content())