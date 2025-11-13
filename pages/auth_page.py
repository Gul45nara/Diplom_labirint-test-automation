from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure


class AuthPage(BasePage):
    """Страница авторизации"""

    # Обновленные локаторы
    AUTH_FORM = (By.CSS_SELECTOR, "form.auth-form, .login-form, #auth-form")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email'], #email, [name='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password'], #password, [name='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], .login-btn")
    AUTH_MODAL = (By.CSS_SELECTOR, ".auth-modal, .login-modal")

    def is_auth_form_visible(self):
        """Проверить видимость формы авторизации"""
        # Проверяем либо форму, либо модальное окно
        return self.is_visible(self.AUTH_FORM) or self.is_visible(self.AUTH_MODAL)