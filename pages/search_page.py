from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure
import time


class SearchPage(BasePage):
    """Страница результатов поиска"""

    # Обновленные локаторы
    SEARCH_RESULTS = (By.CSS_SELECTOR, "div.product-card")
    BOOK_TITLE = (By.CSS_SELECTOR, "a[data-event-label='book'], .product-title-link")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".buy-link.btn-tocart")

    @allure.step("Получить количество результатов поиска")
    def get_results_count(self):
        """Получить количество найденных товаров"""
        try:
            results = self.find_elements(self.SEARCH_RESULTS, timeout=10)
            return len(results)
        except:
            return 0

    @allure.step("Проверить наличие результатов")
    def has_results(self):
        """Проверить, есть ли результаты поиска"""
        return self.get_results_count() > 0

    @allure.step("Получить сообщение об отсутствии результатов")
    def get_no_results_message(self):
        """Получить сообщение об отсутствии результатов"""
        page_text = self.driver.page_source.lower()
        if "ничего не найдено" in page_text:
            return "ничего не найдено"
        elif "0 товаров" in page_text:
            return "0 товаров"
        return ""

    @allure.step("Открыть книгу по индексу {index}")
    def open_book_by_index(self, index=0):
        """Открыть книгу по индексу в результатах"""
        try:
            # Ждем загрузки результатов
            time.sleep(3)

            # Ищем все карточки товаров
            products = self.find_elements(self.SEARCH_RESULTS)
            if products and index < len(products):
                # В каждой карточке ищем ссылку на книгу
                book_links = products[index].find_elements(By.CSS_SELECTOR, "a")
                for link in book_links:
                    href = link.get_attribute('href')
                    if href and '/books/' in href:
                        # Прокручиваем и кликаем
                        self.driver.execute_script("arguments[0].scrollIntoView();", link)
                        time.sleep(1)
                        link.click()
                        time.sleep(3)
                        from .book_page import BookPage
                        return BookPage(self.driver)

            # Альтернативный способ - ищем по классу
            book_titles = self.find_elements(self.BOOK_TITLE)
            if book_titles and index < len(book_titles):
                self.driver.execute_script("arguments[0].scrollIntoView();", book_titles[index])
                time.sleep(1)
                book_titles[index].click()
                time.sleep(3)
                from .book_page import BookPage
                return BookPage(self.driver)

        except Exception as e:
            print(f"Ошибка при открытии книги: {e}")

        return None

    def find_elements(self, locator, timeout=None):
        """Найти все элементы"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        try:
            return wait.until(EC.presence_of_all_elements_located(locator))
        except:
            return []