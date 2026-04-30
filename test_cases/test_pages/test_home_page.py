import logging

import allure
import pytest

from pages.base_page import BasePage
from pages.home_page import HomePage
from utils.conf_loader import project_root
from utils.csv_reader import CSVReader


@allure.title("打开腾讯新闻首页")
@allure.description("验证腾讯新闻首页能否正常打开")
@allure.severity(allure.severity_level.BLOCKER)
@allure.link("https://www.qq.com", name="腾讯新闻")
@pytest.mark.completed
@pytest.mark.dependency(name="homepage")
def test_open_homepage(page):
    home = HomePage(page)
    with allure.step("打开首页"):
        home.gohome()
    with allure.step("验证网址是否正确"):
        url = home.get_url()
        logging.info("验证URL包含 'qq.com': %s", url)
        assert "qq.com" in url
    with allure.step("验证网站标题是否正确"):
        title = home.get_title()
        logging.info("验证页面标题: %s", title)
        assert title == "腾讯网"
    # 添加截图附件
    allure.attach.file(
        home.take_screenshot(), attachment_type=allure.attachment_type.PNG
    )


@allure.feature("测试顶部分类导航区")
@pytest.mark.dependency(depends=["homepage"])
class TestNavBar:
    def get_nav_item_test_data():
        csv_reader = CSVReader(f"{project_root}/data/nav_links.csv")
        return [(row["title"], row["link"]) for row in csv_reader.get_all_data()]

    @allure.title("测试导航按钮文本、链接是否正确")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.completed
    @pytest.mark.parametrize("title, link", get_nav_item_test_data())
    @pytest.mark.dependency(name="nav_data")
    def test_nav_item_data(self, page, title, link):
        home = HomePage(page)
        home.gohome()
        logging.debug("test data: title: %s, link: %s", title, link)
        item = home.locator(home.NAV_ITEM).get_by_text(title, exact=True)
        with allure.step("验证导航项数量"):
            count = item.count()
            logging.info("导航项 '%s' 数量: %d", title, count)
            assert count == 1
        with allure.step("验证导航项链接"):
            href = item.get_attribute("href")
            logging.info("导航项 '%s' 链接: %s, 期望: %s", title, href, link)
            if href is not None:
                assert href == link
            else:
                text = item.text_content()
                logging.info("导航项无链接, 验证文本为 '更多': %s", text)
                assert text == "更多"
        allure.attach.file(
            home.take_screenshot(el=item), attachment_type=allure.attachment_type.PNG
        )

    @allure.title("测试导航按钮hover效果")
    @allure.severity(allure.severity_level.TRIVIAL)
    @pytest.mark.completed
    @pytest.mark.dependency(name="nav_item_hover")
    def test_nav_item_hover(self, page):
        home = HomePage(page)
        home.gohome()
        items = home.locator(home.NAV_ITEM).all()
        logging.info("共找到 %d 个导航项", len(items))
        for item in items:
            if item == items[-1]:
                with allure.step("验证更多菜单下拉显示"):
                    item.hover()
                    dropdown = home.locator(home.MORE_ITEM_DROPDOWN)
                    classes = dropdown.get_attribute("class")
                    logging.info("更多菜单下拉 class: %s", classes)
                    assert "rc-dropdown-hidden" not in classes
                    allure.attach.file(
                        home.take_screenshot(el=dropdown),
                        attachment_type=allure.attachment_type.PNG,
                    )
            else:
                link = item.locator(home.NAV_LINK)
                with allure.step(
                    f"验证导航项 '{link.text_content()}' hover前后伪元素变化"
                ):
                    before_hover = link.evaluate(
                        "el => window.getComputedStyle(el, '::before').content"
                    )
                    link.hover()
                    home.wait_for_timeout()
                    after_hover = link.evaluate(
                        "el => window.getComputedStyle(el, '::before').content"
                    )
                    logging.info(
                        "导航项 '%s' hover前: %s, hover后: %s",
                        link.text_content(),
                        before_hover,
                        after_hover,
                    )
                    assert before_hover != after_hover
                    allure.attach.file(
                        home.take_screenshot(item),
                        attachment_type=allure.attachment_type.PNG,
                    )

    @allure.title("测试导航按钮点击效果")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.completed
    @pytest.mark.dependency(["nav_data"])
    def test_nav_item_click(self, context, page):
        home = HomePage(page)
        home.gohome()
        items = home.locator(home.NAV_ITEM).locator(home.NAV_LINK).all()
        for item in items:
            href = item.get_attribute("href")
            if href is not None:
                try:
                    with allure.step(f"点击导航项 '{item.text_content()}'"):
                        item.click()
                    with allure.step("验证新页面打开"):
                        assert len(context.pages) == 2
                        newpage = BasePage(
                            [p for p in context.pages if p != home.page][0]
                        )
                        logging.debug(
                            "page: title: %s, link: %s",
                            newpage.get_title(),
                            newpage.get_url(),
                        )
                        assert newpage.get_url() == href
                        # 特殊规则
                        if item.text_content() == "王者世界":
                            assert "王者荣耀世界" in newpage.get_title()
                        else:
                            assert item.text_content() in newpage.get_title()
                        allure.attach.file(
                            newpage.take_screenshot(),
                            attachment_type=allure.attachment_type.PNG,
                        )
                except Exception as e:
                    logging.warning("error: %s", e)
                finally:
                    newpage.close()

    @allure.title("测试更多导航按钮弹出面板弹出效果")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.completed
    @pytest.mark.dependency(["nav_item_hover"], name="visible")
    def test_more_nav_item_visible(self, page):
        home = HomePage(page)
        home.gohome()
        more_nav_item = home.locator(home.NAV_ITEM).last
        more_items = home.locator(home.MORE_ITEM)
        more_nav_item.hover()
        home.wait_for_timeout()
        assert more_items.first.is_visible() == True
        home.mouse.move(0, 0)
        home.wait_for_timeout()
        assert more_items.first.is_visible() == False

    @allure.title("测试更多导航按钮弹出面板hover效果")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.completed
    @pytest.mark.dependency(["visible"])
    def test_more_nav_item_hover(self, page):
        home = HomePage(page)
        home.gohome()
        home.locator(home.NAV_ITEM).last.hover()
        more_items = home.locator(home.MORE_ITEM).all()
        for item in more_items:
            assert (
                item.evaluate("el => window.getComputedStyle(el).color") == home.BLACK
            )
            item.hover()
            home.wait_for_timeout()
            assert item.evaluate("el => window.getComputedStyle(el).color") == home.BLUE

    @allure.title("测试更多导航按钮弹出面板点击效果")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.completed
    @pytest.mark.dependency(["visible"])
    def test_more_nav_item_click(self, context, page):
        home = HomePage(page)
        home.gohome()
        home.locator(home.NAV_ITEM).last.hover()
        more_items = home.locator(home.MORE_ITEM).all()
        for item in more_items:
            href = item.get_attribute("href")
            if href is not None:
                try:
                    with allure.step(f"点击导航项 '{item.text_content()}'"):
                        home.locator(home.NAV_ITEM).last.hover()
                        item.click()
                    with allure.step("验证新页面打开"):
                        assert len(context.pages) == 2
                        newpage = BasePage(
                            [p for p in context.pages if p != home.page][0]
                        )
                        logging.debug(
                            "page: title: %s, link: %s",
                            newpage.get_title(),
                            newpage.get_url(),
                        )
                        assert newpage.get_url() == href
                        assert item.text_content() in newpage.get_title()
                        allure.attach.file(
                            newpage.take_screenshot(),
                            attachment_type=allure.attachment_type.PNG,
                        )
                except Exception as e:
                    logging.warning("error: %s", e)
                finally:
                    newpage.close()
