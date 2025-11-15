"""Базовый класс для всех страниц с улучшенной стабильностью."""
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Базовый класс для всех страниц."""

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(browser, 15)

    def open(self, url=""):
        """Открыть указанный URL или базовый URL."""
        full_url = f"{self.browser.base_url}{url}"
        print(f"Opening URL: {full_url}")
        self.browser.get(full_url)
        time.sleep(2)

    def find_element(self, locator, timeout=15):
        """Найти элемент с явным ожиданием и логированием."""
        print(f"Looking for element: {locator}")
        wait = WebDriverWait(self.browser, timeout)
        try:
            element = wait.until(EC.presence_of_element_located(locator))
            print(f"Element found: {locator}")
            return element
        except TimeoutException:
            print(f"Element NOT found within {timeout}s: {locator}")
            raise

    def find_elements(self, locator, timeout=15):
        """Найти несколько элементов с явным ожиданием."""
        print(f"Looking for multiple elements: {locator}")
        wait = WebDriverWait(self.browser, timeout)
        try:
            elements = wait.until(EC.presence_of_all_elements_located(locator))
            print(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            print(f"No elements found within {timeout}s: {locator}")
            return []

    def click_element(self, locator, timeout=15):
        """Кликнуть на элемент с явным ожиданием кликабельности."""
        print(f"Clicking element: {locator}")
        wait = WebDriverWait(self.browser, timeout)
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()
        print(f"Element clicked: {locator}")

    def input_text(self, locator, text, timeout=15):
        """Ввести текст в поле с явным ожиданием."""
        print(f"Inputting text '{text}' to: {locator}")
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
        print(f"Text input completed: {locator}")

    def get_text(self, locator, timeout=15):
        """Получить текст из элемента с явным ожиданием."""
        element = self.find_element(locator, timeout)
        text = element.text
        print(f"Got text '{text}' from: {locator}")
        return text

    def wait_for_url_contains(self, text, timeout=15):
        """Ожидать, что URL содержит указанный текст."""
        print(f"Waiting for URL to contain: {text}")
        wait = WebDriverWait(self.browser, timeout)
        return wait.until(EC.url_contains(text))

    def is_element_present(self, locator, timeout=5):
        """Проверить, присутствует ли элемент на странице."""
        try:
            self.find_element(locator, timeout)
            return True
        except TimeoutException:
            return False

    def get_current_url(self):
        """Получить текущий URL."""
        url = self.browser.current_url
        print(f"Current URL: {url}")
        return url

    def safe_click(self, locator, timeout=10):
        """Безопасный клик с обработкой исключений."""
        try:
            self.click_element(locator, timeout)
            return True
        except Exception as e:
            print(f"Safe click failed: {e}")
            return False
