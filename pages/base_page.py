from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from config.config import Config
import allure
import time


class BasePage:
    """Базовый класс для всех страниц"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.TIMEOUT)
        self.base_url = Config.BASE_URL
        self.actions = ActionChains(driver)

    @allure.step("Открыть страницу {url}")
    def open(self, url=""):
        """Открыть указанный URL"""
        full_url = f"{self.base_url}/{url}" if url else self.base_url
        self.driver.get(full_url)
        return self

    @allure.step("Найти элемент {locator}")
    def find_element(self, by, value, timeout=None):
        """Найти элемент с ожиданием"""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))

    @allure.step("Найти видимый элемент {locator}")
    def find_visible_element(self, locator, timeout=None):
        """Найти видимый элемент"""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Кликнуть на элемент {locator}")
    def click(self, locator):
        """Кликнуть на элемент"""
        element = self.find_visible_element(locator)
        element.click()
        return self

    @allure.step("Ввести текст '{text}' в поле {locator}")
    def type_text(self, locator, text):
        """Ввести текст в поле"""
        element = self.find_visible_element(locator)
        element.clear()
        element.send_keys(text)
        return self

    @allure.step("Получить текст элемента {locator}")
    def get_text(self, locator):
        """Получить текст элемента"""
        return self.find_visible_element(locator).text

    @allure.step("Проверить видимость элемента {locator}")
    def is_visible(self, locator, timeout=None):
        """Проверить видимость элемента"""
        try:
            return self.find_visible_element(locator, timeout).is_displayed()
        except TimeoutException:
            return False

    @allure.step("Проверить наличие элемента {locator}")
    def is_element_present(self, locator, timeout=None):
        """Проверить наличие элемента"""
        try:
            self.find_element(locator, timeout)
            return True
        except TimeoutException:
            return False

    @allure.step("Получить текущий URL")
    def get_current_url(self):
        """Получить текущий URL"""
        return self.driver.current_url

    @allure.step("Переключиться на новую вкладку")
    def switch_to_new_tab(self):
        """Переключиться на новую вкладку"""
        handles = self.driver.window_handles
        if len(handles) > 1:
            self.driver.switch_to.window(handles[-1])
        return self

    @allure.step("Закрыть текущую вкладку и вернуться к основной")
    def close_tab_and_return(self):
        """Закрыть текущую вкладку и вернуться к основной"""
        if len(self.driver.window_handles) > 1:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        return self
