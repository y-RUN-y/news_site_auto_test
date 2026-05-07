from pages.base_page import BasePage


class SearchResultPage(BasePage):
    class ImgTextCard:
        ROOT = ".img-text-card:not(.wiki-card)"
        TITLE = "p.title"
        DESCRIPTION = "p.description"
        KEYWORD_SPAN = "span[style*='color']"
        LINK = "a.hover-link"

    def get_img_text_card(self, index: int = 0):
        return self.locator(self.ImgTextCard.ROOT).nth(index)

    def img_text_card_title(self, card) -> str:
        return card.locator(self.ImgTextCard.TITLE).get_attribute("title")

    def img_text_card_is_keyword_blue(self, card) -> bool:
        spans = card.locator(self.ImgTextCard.KEYWORD_SPAN).all()
        for span in spans:
            if not span.get_attribute('style') == 'color: #37f':
                return False
        return True

    def click_img_text_card(self, card):
        card.locator(self.ImgTextCard.LINK).click()
