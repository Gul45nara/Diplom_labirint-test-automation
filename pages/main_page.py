from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure
import time


class MainPage(BasePage):
    """Главная страница Лабиринт"""

    # Правильные локаторы
    SEARCH_INPUT = (By.ID, "search-field")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button.b-header-b-search-e-btn")
    CART_ICON = (By.CSS_SELECTOR, "a[href*='/cart/'].b-header-b-personal-e-link")
    LOGIN_BUTTON = (By.CSS_SELECTOR, ".js-b-authenticate, .b-header-b-personal-e-link[href*='cabinet']")
    COOKIE_ACCEPT = (By.CSS_SELECTOR, ".cookie-policy__button")

    @allure.step("Принять куки")
    def accept_cookies(self):
        """Принять куки"""
        try:
            self.click(self.COOKIE_ACCEPT)
            time.sleep(1)
        except Exception:
            pass
        return self

    @allure.step("Выполнить поиск по запросу: {query}")
    def search(self, query):
        """Выполнить поиск"""
        self.type_text(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)
        time.sleep(3)
        from .search_page import SearchPage
        return SearchPage(self.driver)

    @allure.step("Перейти в корзину")
    def go_to_cart(self):
        """Перейти в корзину"""
        self.click(self.CART_ICON)
        time.sleep(2)
        from .cart_page import CartPage
        return CartPage(self.driver)

    @allure.step("Перейти к авторизации")
    def go_to_auth(self):
        """Перейти к авторизации"""
        try:
            # Пробуем найти и кликнуть кнопку авторизации
            self.click(self.LOGIN_BUTTON)
        except Exception:
            # Если не нашли кнопку, переходим напрямую по URL
            self.driver.get(f"{self.base_url}/login/")
        time.sleep(2)
        from .auth_page import AuthPage
        return AuthPage(self.driver)
