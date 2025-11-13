from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure


class CartPage(BasePage):
    """Страница корзины"""

    # Обновленные локаторы
    CART_TITLE = (By.CSS_SELECTOR, "h1, .cart-title, .basket-title")
    CART_ITEMS = (By.CSS_SELECTOR, ".cart-item, .basket-item, .cart-product")
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, ".cart-empty, .basket-empty, .empty-cart")
    CART_CONTENT = (By.CSS_SELECTOR, ".cart-content, .basket-content")

    def get_cart_items_count(self):
        """Получить количество товаров в корзине"""
        return len(self.find_elements(self.CART_ITEMS))

    def is_cart_empty(self):
        """Проверить, пуста ли корзина"""
        return self.is_visible(self.EMPTY_CART_MESSAGE) or self.get_cart_items_count() == 0

    def find_elements(self, locator, timeout=None):
        """Найти все элементы"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        try:
            return wait.until(EC.presence_of_all_elements_located(locator))
        except Exception:
            return []
