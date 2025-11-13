from selenium.webdriver.common.by import By
from .base_page import BasePage


class AuthPage(BasePage):
    """Страница авторизации"""

    # Обновленные локаторы
    LOGIN_BUTTON = (By.XPATH,
                    "//a[@class='b-header-b-personal-e-link top-link-main top-link-main_cabinet']")
    AUTH_FORM = (By.XPATH,
                 "//form[@class='auth-template__form auth-form js-auth-form']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password'], #password, [name='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], .login-btn")
    AUTH_MODAL = (By.CSS_SELECTOR, ".auth-modal, .login-modal")

    def is_auth_form_visible(self):
        """Проверить видимость формы авторизации"""
        # Проверяем либо форму, либо модальное окно
        return self.is_visible(self.AUTH_FORM) or self.is_visible(self.AUTH_MODAL)
