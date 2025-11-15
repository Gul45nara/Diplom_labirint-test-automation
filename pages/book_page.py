"""Класс для страницы книги."""
from .base_page import BasePage
from selenium.webdriver.common.by import By


class BookPage(BasePage):
    """Класс для страницы книги."""

    # Локаторы для страницы книги
    BOOK_TITLE = (By.CSS_SELECTOR, "h1, .product-title, .book-title")
    BOOK_AUTHOR = (By.CSS_SELECTOR, ".product-author, .authors, .author")
    BOOK_PRICE = (By.CSS_SELECTOR, ".buying-price, .price, .product-price")
    ADD_TO_CART_BUTTON = (
        By.CSS_SELECTOR,
        ".btn-buy, .buy-link, [data-tooltip='В корзину']"
    )
    ADD_TO_COMPARE_BUTTON = (
        By.CSS_SELECTOR,
        ".compare, .compare-btn, [data-tooltip='Сравнить']"
    )
    ADD_TO_FAVORITES_BUTTON = (
        By.CSS_SELECTOR,
        ".fave, .favorite-btn, [data-tooltip='Отложить']"
    )

    def get_book_title(self):
        """Получить название книги."""
        return self.get_text(self.BOOK_TITLE)

    def get_book_author(self):
        """Получить автора книги."""
        return self.get_text(self.BOOK_AUTHOR)

    def get_book_price(self):
        """Получить цену книги."""
        return self.get_text(self.BOOK_PRICE)

    def add_to_cart(self):
        """Добавить книгу в корзину."""
        return self.safe_click(self.ADD_TO_CART_BUTTON)

    def add_to_compare(self):
        """Добавить книгу к сравнению."""
        return self.safe_click(self.ADD_TO_COMPARE_BUTTON)

    def add_to_favorites(self):
        """Добавить книгу в отложенные."""
        return self.safe_click(self.ADD_TO_FAVORITES_BUTTON)
