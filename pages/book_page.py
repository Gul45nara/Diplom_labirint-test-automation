from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure


class BookPage(BasePage):
    """Страница книги"""

    # Обновленные локаторы
    BOOK_TITLE = (By.CSS_SELECTOR, "h1, .book-title, .product-title")
    BOOK_AUTHOR = (By.CSS_SELECTOR, ".authors, .book-author, .product-author")
    BOOK_PRICE = (By.CSS_SELECTOR, ".buying-price, .price, .product-price")
    BUY_BUTTON = (By.XPATH,
        "//a[@class='btn btn-small btn-primary btn-buy']")
    CART_SUCCESS_ICON = (By.XPATH,
        "//span[@class='btn btn-small btn-primary btn-buy']")
    ISBN = (By.XPATH, "//span[contains(@class, 'isbn')]")
    CART_COUNTER = (By.XPATH,
        "//span[@class='b-header-b-personal-e-icon-count-m-cart basket-in-cart-a']")
    ADD_TO_CART_BUTTON = (By.XPATH, "//a[@class='btn btn-small btn-primary btn-buy']")
    CART_SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class, 'success-message')]")

    @allure.step("Получить информацию о книге")
    def get_book_info(self):
        """Получить основную информацию о книге"""
        info = {
            'title': self.get_text(self.BOOK_TITLE) if self.is_visible(self.BOOK_TITLE) else 'Не указано',
            'author': self.get_text(self.BOOK_AUTHOR) if self.is_visible(self.BOOK_AUTHOR) else 'Не указан',
            'price': self.get_text(self.BOOK_PRICE) if self.is_visible(self.BOOK_PRICE) else 'Не указана'
        }
        return info

    @allure.step("Добавить книгу в корзину")
    def add_to_cart(self):
        """Добавить книгу в корзину"""
        if self.is_visible(self.ADD_TO_CART_BUTTON):
            self.click(self.ADD_TO_CART_BUTTON)
        return self

    @allure.step("Проверить сообщение о добавлении в корзину")
    def is_added_to_cart(self):
        """Проверить, отображается ли сообщение об успешном добавлении"""
        return self.is_visible(self.CART_SUCCESS_MESSAGE, timeout=5)

    @allure.step("Получить ISBN книги")
    def get_isbn(self):
        """Получить ISBN книги"""
        try:
            return self.get_text(self.ISBN)
        except Exception:
            return "Не найден"
