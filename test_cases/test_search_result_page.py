# import logging

# import allure
# import pytest

# from pages.base_page import BasePage
# from pages.main_page import MainPage
# from pages.search_result_page import SearchResultPage


# @allure.feature("搜索结果页测试")
# class TestSearchResultPage:
#     SEARCH_KEYWORDS = ["腾讯新闻", "AI技术", "世界杯"]

#     def search_and_navigate(self, context, page, keyword):
#         """执行搜索并导航到搜索结果页"""
#         home = MainPage(page)
#         home.go_main_page()
#         home.locator(home.INPUT_BOX).fill(keyword)
#         home.locator(home.SEARCH_BTN).click()
#         home.wait_for_timeout(5000)
#         return SearchResultPage(context.pages[-1])

#     @allure.title("验证搜索结果页包含图文卡片")
#     @allure.description("验证搜索结果页是否正确加载图文卡片列表")
#     @allure.severity(allure.severity_level.CRITICAL)
#     @pytest.mark.completed
#     @pytest.mark.parametrize('keyword', SEARCH_KEYWORDS)
#     def test_result_page_has_cards(self, context, page, keyword):
#         result_page = self.search_and_navigate(context, page, keyword)
#         try:
#             with allure.step("验证图文卡片数量"):
#                 card_count = result_page.locator(SearchResultPage.ImgTextCard.ROOT).count()
#                 logging.info("搜索 '%s' 找到 %d 个图文卡片", keyword, card_count)
#                 assert card_count > 0, f"搜索 '{keyword}' 未找到任何图文卡片"
#                 allure.attach.file(
#                     result_page.take_screenshot(),
#                     attachment_type=allure.attachment_type.PNG,
#                 )
#         except:
#             result_page.take_screenshot('error_screenshot')
#             raise
#         finally:
#             result_page.close()
            

#     @allure.title("验证图文卡片标题非空")
#     @allure.description("验证每个图文卡片的标题字段是否都有内容")
#     @allure.severity(allure.severity_level.NORMAL)
#     @pytest.mark.completed
#     @pytest.mark.parametrize('keyword', SEARCH_KEYWORDS)
#     def test_card_title_and_description(self, context, page, keyword):
#         result_page = self.search_and_navigate(context, page, keyword)
#         try:
#             cards = result_page.locator(SearchResultPage.ImgTextCard.ROOT).all()
#             for i, card in enumerate(cards[:5]):
#                 with allure.step(f"验证第 {i+1} 个卡片"):
#                     title = result_page.img_text_card_title(card)
                    
#                     logging.info("卡片 %d - 标题: %s", i + 1, title)
#                     assert title, f"卡片 {i+1} 标题为空"
#             allure.attach.file(
#                 result_page.take_screenshot(),
#                 attachment_type=allure.attachment_type.PNG,
#             )
#         except Exception:
#             result_page.take_screenshot(name='error_screenshot')
#             raise
#         finally:
#             result_page.close()

#     @allure.title("验证搜索关键词高亮显示")
#     @allure.description("验证搜索结果中搜索关键词是否以蓝色字体高亮")
#     @allure.severity(allure.severity_level.NORMAL)
#     @pytest.mark.completed
#     @pytest.mark.parametrize('keyword', SEARCH_KEYWORDS)
#     def test_keyword_highlighted(self, context, page, keyword):
#         result_page = self.search_and_navigate(context, page, keyword)
#         try:
#             cards = result_page.locator(SearchResultPage.ImgTextCard.ROOT).all()
#             highlighted_count = 0
#             for i, card in enumerate(cards[:5]):
#                 if result_page.img_text_card_is_keyword_blue(card):
#                     highlighted_count += 1
#                     logging.info("卡片 %d 关键词已高亮", i + 1)
#             logging.info("前5个卡片中 %d 个关键词被高亮", highlighted_count)
#             assert highlighted_count == 5, "搜索结果中关键词未被高亮显示"
#             allure.attach.file(
#                 result_page.take_screenshot(),
#                 attachment_type=allure.attachment_type.PNG,
#             )
#         except Exception:
#             result_page.take_screenshot(name='error_screenshot')
#             raise
#         finally:
#             result_page.close()

#     @allure.title("验证点击图文卡片打开新标签页")
#     @allure.description("验证点击搜索结果中的图文卡片后能在新标签页正确打开链接")
#     @allure.severity(allure.severity_level.CRITICAL)
#     @pytest.mark.completed
#     @pytest.mark.parametrize('keyword', SEARCH_KEYWORDS)
#     def test_click_card_opens_new_tab(self, context, page, keyword):
#         result_page = self.search_and_navigate(context, page, keyword)
#         home = MainPage(page)
#         try:
#             card = result_page.get_img_text_card(0)
#             with allure.step("点击第一个图文卡片"):
#                 result_page.click_img_text_card(card)
#                 home.wait_for_timeout(2000)
#             with allure.step("验证新标签页打开"):
#                 assert len(context.pages) >= 2, "点击卡片后未打开新标签页"
#                 new_page = BasePage(context.pages[-1])
#                 new_url = new_page.get_url()
#                 new_title = new_page.get_title()
#                 logging.info("新页面URL: %s, 标题: %s", new_url, new_title)                
#                 allure.attach.file(
#                     new_page.take_screenshot(),
#                     attachment_type=allure.attachment_type.PNG,
#                 )
#                 new_page.close()
#         except Exception:
#             result_page.take_screenshot(name='error_screenshot')
#             raise
#         finally:
#             result_page.close()
