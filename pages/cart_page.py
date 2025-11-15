"""Класс для страницы корзины."""
from .base_page import BasePage
from selenium.webdriver.common.by import By


class CartPage(BasePage):
    """Класс для страницы корзины."""

    # Локаторы для корзины
    CART_ITEMS = (By.CSS_SELECTOR, ".cart-item, .basket-item")
    ITEM_TITLE = (By.CSS_SELECTOR, ".product-title, .item-title")
    ITEM_PRICE = (By.CSS_SELECTOR, ".price-value, .item-price")
    ITEM_QUANTITY = (By.CSS_SELECTOR, ".quantity-input, [name*='quantity']")
    REMOVE_BUTTON = (By.CSS_SELECTOR, ".btn-remove, .remove-item")
    TOTAL_PRICE = (By.CSS_SELECTOR, ".basket-summary, .total-price")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, ".btn-checkout, .checkout-btn")

    def get_cart_items_count(self):
        """Получить количество товаров в корзине."""
        items = self.find_elements(self.CART_ITEMS)
        return len(items)

    def get_item_titles(self):
        """Получить названия всех товаров в корзине."""
        titles = []
        items = self.find_elements(self.ITEM_TITLE)
        for item in items:
            titles.append(item.text)
        return titles

    def remove_first_item(self):
        """Удалить первый товар из корзины."""
        return self.safe_click(self.REMOVE_BUTTON)

    def get_total_price(self):
        """Получить общую стоимость."""
        return self.get_text(self.TOTAL_PRICE)

    def proceed_to_checkout(self):
        """Перейти к оформлению заказа."""
        return self.safe_click(self.CHECKOUT_BUTTON)
