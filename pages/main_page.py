from .base_page import BasePage
from selenium.webdriver.common.by import By
import time  # ← ДОБАВИТЬ ЭТУ СТРОКУ


class MainPage(BasePage):
    """Класс для главной страницы Лабиринт с альтернативными локаторами."""

    # Основные локаторы
    SEARCH_INPUT = (By.ID, "search-field")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], .b-header-b-search-e-btn")

    # Альтернативные локаторы для корзины
    CART_BUTTON = (By.CSS_SELECTOR,
                   "[data-basket-toggle], .b-header-b-personal-e-link[href*='cart'], .b-header-b-personal-e-icon-m-cart")
    CART_COUNT = (By.CSS_SELECTOR, ".b-header-b-personal-e-icon-count-m-cart, [data-basket-count]")

    # Другие элементы
    LOGO = (By.CSS_SELECTOR, ".b-header-b-logo, .b-header-logo")
    MAIN_MENU = (By.CSS_SELECTOR, ".b-header-b-menu-e-list, .header-menu")
    USER_ICON = (By.CSS_SELECTOR, ".b-header-b-personal-e-icon-m-profile, .js-b-autofade")

    def search_book(self, book_title):
        """Поиск книги по названию с улучшенной стабильностью."""
        print(f"Searching for book: {book_title}")
        self.input_text(self.SEARCH_INPUT, book_title)
        self.click_element(self.SEARCH_BUTTON)
        # Ждем загрузки результатов поиска
        self.wait_for_url_contains("search")
        time.sleep(2)  # Дополнительное время для загрузки

    def go_to_cart(self):
        """Перейти в корзину с улучшенной стабильностью."""
        print("Navigating to cart")
        self.click_element(self.CART_BUTTON)
        # Ждем перехода на страницу корзины
        self.wait_for_url_contains("cart")

    def get_cart_count(self):
        """Получить количество товаров в корзине с обработкой ошибок."""
        try:
            count_element = self.find_element(self.CART_COUNT, timeout=3)
            count_text = count_element.text.strip()
            print(f"Cart count text: '{count_text}'")

            # Парсим число из текста
            import re
            numbers = re.findall(r'\d+', count_text)
            count = int(numbers[0]) if numbers else 0
            print(f"Parsed cart count: {count}")
            return count

        except Exception as e:
            print(f"Could not get cart count: {e}")
            return 0

    def is_main_page_loaded(self):
        """Проверить, загружена ли главная страница."""
        checks = [
            self.is_element_present(self.LOGO),
            self.is_element_present(self.SEARCH_INPUT),
            self.is_element_present(self.MAIN_MENU)
        ]

        result = all(checks)
        print(f"Main page loaded check: {result} (logo: {checks[0]}, search: {checks[1]}, menu: {checks[2]})")
        return result
