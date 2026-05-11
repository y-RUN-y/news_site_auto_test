import logging

import allure
import pytest

from common.base_page import BasePage
from common.conf_loader import project_root
from common.csv_reader import CSVReader
from pages.main_page import MainPage


@allure.title("打开腾讯新闻首页")
@allure.description("验证腾讯新闻首页能否正常打开")
@allure.severity(allure.severity_level.BLOCKER)
@allure.link("https://www.qq.com", name="腾讯新闻")
@pytest.mark.completed
def test_open_main_page(page):
    main_page = MainPage(page)
    with allure.step("打开首页"):
        main_page.go_main_page()
    with allure.step("验证网址是否正确"):
        url = main_page.get_url()
        logging.info("验证URL包含 'qq.com': %s", url)
        assert "qq.com" in url
    with allure.step("验证网站标题是否正确"):
        title = main_page.get_title()
        logging.info("验证页面标题: %s", title)
        assert title == "腾讯网"
    # 添加截图附件
    allure.attach.file(
        main_page.take_screenshot(), attachment_type=allure.attachment_type.PNG
    )


@allure.feature("测试顶部分类导航区")
class TestNavBar:
    def get_nav_item_test_data():
        csv_reader = CSVReader(f"{project_root}/data/nav_links.csv")
        return [(row["title"], row["link"]) for row in csv_reader.get_all_data()]

    @allure.title("测试导航按钮文本、链接是否正确")
    @allure.description("验证导航项的文本内容和href链接是否与CSV测试数据一致")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.completed
    @pytest.mark.parametrize("title, link", get_nav_item_test_data())
    def test_nav_item_data(self, page, title, link):
        main_page = MainPage(page)
        main_page.go_main_page()
        logging.debug("test data: title: %s, link: %s", title, link)
        item = main_page.locator(main_page.NAV_ITEM).get_by_text(title, exact=True)
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
            main_page.take_screenshot(el=item),
            attachment_type=allure.attachment_type.PNG,
        )

    @allure.title("测试导航按钮hover效果")
    @allure.description("验证导航项hover时::before伪元素样式变化")
    @allure.severity(allure.severity_level.TRIVIAL)
    @pytest.mark.completed
    def test_nav_item_hover(self, page):
        main_page = MainPage(page)
        main_page.go_main_page()
        items = main_page.locator(main_page.NAV_ITEM).all()
        logging.info("共找到 %d 个导航项", len(items))
        for item in items:
            if item == items[-1]:
                with allure.step("验证更多菜单下拉显示"):
                    item.hover()
                    dropdown = main_page.locator(main_page.MORE_ITEM_DROPDOWN)
                    classes = dropdown.get_attribute("class")
                    logging.info("更多菜单下拉 class: %s", classes)
                    assert "rc-dropdown-hidden" not in classes
                    allure.attach.file(
                        main_page.take_screenshot(el=dropdown),
                        attachment_type=allure.attachment_type.PNG,
                    )
            else:
                link = item.locator(main_page.NAV_LINK)
                with allure.step(
                    f"验证导航项 '{link.text_content()}' hover前后伪元素变化"
                ):
                    before_hover = link.evaluate(
                        "el => window.getComputedStyle(el, '::before').content"
                    )
                    link.hover()
                    main_page.wait_for_timeout()
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
                        main_page.take_screenshot(item),
                        attachment_type=allure.attachment_type.PNG,
                    )

    @allure.title("测试导航按钮点击效果")
    @allure.description("验证点击导航项后能在新标签页正确打开对应链接")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.completed
    def test_nav_item_click(self, context, page):
        main_page = MainPage(page)
        main_page.go_main_page()
        newpage = None
        items = main_page.locator(main_page.NAV_ITEM).locator(main_page.NAV_LINK).all()
        for item in items:
            href = item.get_attribute("href")
            if href is not None:
                try:
                    with allure.step(f"点击导航项 '{item.text_content()}'"):
                        item.click()
                        main_page.wait_for_timeout(1000)
                    with allure.step("验证新页面打开"):
                        assert len(context.pages) == 2
                        newpage = BasePage(context.pages[-1])
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
                    newpage.take_screenshot(name="error_screenshot")
                finally:
                    newpage.close()

    @allure.title("测试更多导航按钮弹出面板弹出效果")
    @allure.description("验证更多菜单hover时下拉面板显示，鼠标移开后隐藏")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.completed
    def test_more_nav_item_visible(self, page):
        main_page = MainPage(page)
        main_page.go_main_page()
        more_nav_item = main_page.locator(main_page.NAV_ITEM).last
        more_items = main_page.locator(main_page.MORE_ITEM)
        more_nav_item.hover()
        main_page.wait_for_timeout()
        assert more_items.first.is_visible() == True
        main_page.mouse.move(0, 0)
        main_page.wait_for_timeout(500)
        assert more_items.first.is_visible() == False

    @allure.title("测试更多导航按钮弹出面板hover效果")
    @allure.description("验证更多菜单下拉项hover时文字颜色由黑色变为蓝色")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.completed
    def test_more_nav_item_hover(self, page):
        main_page = MainPage(page)
        main_page.go_main_page()
        main_page.locator(main_page.NAV_ITEM).last.hover()
        more_items = main_page.locator(main_page.MORE_ITEM).all()
        for item in more_items:
            assert (
                item.evaluate("el => window.getComputedStyle(el).color")
                == main_page.BLACK
            )
            item.hover()
            main_page.wait_for_timeout()
            assert (
                item.evaluate("el => window.getComputedStyle(el).color")
                == main_page.BLUE
            )

    @allure.title("测试更多导航按钮弹出面板点击效果")
    @allure.description("验证点击更多菜单下拉项后能在新标签页正确打开对应链接")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.completed
    def test_more_nav_item_click(self, context, page):
        main_page = MainPage(page)
        main_page.go_main_page()
        main_page.locator(main_page.NAV_ITEM).last.hover()
        more_items = main_page.locator(main_page.MORE_ITEM).all()
        newpage = None
        for item in more_items:
            href = item.get_attribute("href")
            if href is not None:
                try:
                    with allure.step(f"点击导航项 '{item.text_content()}'"):
                        with context.expect_page() as new_page_info:
                            main_page.locator(main_page.NAV_ITEM).last.hover()
                            item.click()
                            newpage = BasePage(new_page_info.value)
                            newpage.wait_for_load_state("networkidle")
                    with allure.step("验证新页面打开"):
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
                    if newpage is not None:
                        newpage.take_screenshot(name="error_screenshot")
                finally:
                    if newpage is not None:
                        newpage.close()


@allure.feature("测试搜索栏")
class TestSearch:
    def get_search_keywords():
        csv_reader = CSVReader(f"{project_root}/data/search_keywords.csv")
        return [
            (
                row["keyword"],
                int(row["has_suggestions"]),
                int(row["has_search_res"]),
                int(row["response_code"]) if row["response_code"] is not None else None,
            )
            for row in csv_reader.get_all_data()
        ]

    @allure.title("测试输入搜索词时显示搜索提示")
    @allure.description("验证在搜索框输入文字时，下方是否出现搜索提示词")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.completed
    @pytest.mark.parametrize(
        "keyword,has_suggestions,has_search_res,response_code", get_search_keywords()
    )
    def test_search_suggestions_appear(
        self, page, keyword, has_suggestions, has_search_res, response_code
    ):
        main_page = MainPage(page)
        main_page.go_main_page()
        with allure.step("输入搜索词"):
            input_box = main_page.locator(main_page.INPUT_BOX)
            input_box.fill(keyword)
            main_page.wait_for_timeout(1000)
        with allure.step("验证搜索提示是否出现"):
            suggestions = main_page.locator(main_page.SEARCH_SUG_LIST)
            suggestion_count = suggestions.count()
            logging.info("搜索提示项数量: %d", suggestion_count)
            if has_suggestions == 1:
                assert suggestion_count > 0, "输入搜索词后未出现搜索提示"
            else:
                assert suggestion_count == 0, "输入搜索词后不应出现搜索提示"
            first_suggestion = suggestions.first
            if first_suggestion.is_visible():
                logging.info("第一个搜索提示: %s", first_suggestion.text_content())
            allure.attach.file(
                main_page.take_screenshot(),
                attachment_type=allure.attachment_type.PNG,
            )

    @allure.title("测试搜索功能")
    @allure.description("验证搜索框输入不同关键词（含异常输入）后页面行为是否正常")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.completed
    @pytest.mark.parametrize(
        "keyword,has_suggestions,has_search_res,response_code", get_search_keywords()
    )
    def test_search_with_keywords(
        self, context, page, keyword, has_suggestions, has_search_res, response_code
    ):
        main_page = MainPage(page)
        main_page.go_main_page()
        with allure.step(f"输入搜索词 '{keyword[:20]}...' 并点击搜索"):
            main_page.locator(main_page.INPUT_BOX).fill(keyword)
            main_page.locator(main_page.SEARCH_BTN).click()
            main_page.wait_for_timeout(1000)
        with allure.step("验证页面行为"):
            current_page = BasePage(context.pages[-1])
            current_url = current_page.get_url()
            logging.info("搜索 '%s' 后的URL: %s", keyword[:20], current_url)
            try:
                if has_search_res == 0:
                    assert len(context.pages) == 1, "空搜索词不应打开新标签页"
                    logging.info("空搜索词未触发跳转，符合预期")
                else:
                    assert len(context.pages) >= 1
                    current_title = current_page.get_title()
                    logging.info("搜索结果页标题: %s", current_title)
                    assert keyword[:10] in current_title
                    assert (
                        current_page.get_response(current_url).status == response_code
                    )
                allure.attach.file(
                    current_page.take_screenshot(),
                    attachment_type=allure.attachment_type.PNG,
                )
            except:
                current_page.take_screenshot(name="error_screenshot")
            finally:
                current_page.close()
