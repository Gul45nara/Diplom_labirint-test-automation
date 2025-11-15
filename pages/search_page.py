"""Класс для страницы поиска с улучшенными локаторами."""
import time
from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class SearchPage(BasePage):
    """Класс для страницы поиска."""

    # УЛУЧШЕННЫЕ локаторы на основе реальной структуры сайта
    SEARCH_RESULTS = (
        By.CSS_SELECTOR,
        "div.product, .search-result, .products-grid .product, "
        ".genres-carousel__item"
    )
    PRODUCT_CARD = (By.CSS_SELECTOR, "div.product, .product-card")
    BOOK_TITLE = (
        By.CSS_SELECTOR,
        "a.product-title, .product-title span, .book-title, "
        ".genres-carousel__item .product-title"
    )
    BOOK_AUTHOR = (By.CSS_SELECTOR, ".product-author, .author, [data-product-author]")
    BOOK_PRICE = (
        By.CSS_SELECTOR,
        "span.price-val, .product-price, .price, .buying-price-val-number"
    )
    ADD_TO_CART_BUTTON = (
        By.CSS_SELECTOR,
        "a.btn.buy-link, .buy-link, [data-tooltip='В корзину'], .btn-buy"
    )
    ADD_TO_COMPARE_BUTTON = (
        By.CSS_SELECTOR,
        "a.compare, .compare-btn, [data-tooltip='Добавить к сравнению']"
    )
    ADD_TO_POSTPONED_BUTTON = (
        By.CSS_SELECTOR,
        "a.fave, .favorite-btn, [data-tooltip='Отложить']"
    )
    SEARCH_TITLE = (By.CSS_SELECTOR, "h1.index-top-title, .search-title, h1")
    SORT_SELECTOR = (By.CSS_SELECTOR, "select.sorting-value, .sort-select")
    NO_RESULTS_MESSAGE = (
        By.CSS_SELECTOR,
        ".search-error, .no-results, .search-empty"
    )

    def get_search_results_count(self):
        """Получить количество результатов поиска."""
        try:
            time.sleep(3)
            results = self.find_elements(self.SEARCH_RESULTS, timeout=10)
            return len(results)
        except Exception as e:
            print(f"Error getting search results count: {e}")
            return 0

    def get_first_book_title(self):
        """Получить название первой книги в результатах."""
        try:
            first_book = self.find_element(self.BOOK_TITLE, timeout=10)
            title = first_book.text
            print(f"First book title: {title}")
            return title
        except Exception as e:
            print(f"Error getting first book title: {e}")
            return "No books found"

    def add_first_book_to_cart(self):
        """Добавить первую книгу в корзину."""
        try:
            if self.get_search_results_count() > 0:
                add_buttons = self.find_elements(self.ADD_TO_CART_BUTTON, timeout=10)
                if add_buttons:
                    print(f"Clicking add to cart button (found {len(add_buttons)} buttons)")
                    add_buttons[0].click()
                    time.sleep(2)
                    return True
            return False
        except Exception as e:
            print(f"Error adding to cart: {e}")
            return False

    def add_first_book_to_compare(self):
        """Добавить первую книгу к сравнению."""
        try:
            compare_buttons = self.find_elements(self.ADD_TO_COMPARE_BUTTON, timeout=5)
            if compare_buttons:
                compare_buttons[0].click()
                time.sleep(1)
                return True
        except Exception as e:
            print(f"Error adding to compare: {e}")
        return False

    def add_first_book_to_postponed(self):
        """Добавить первую книгу в отложенные."""
        try:
            postponed_buttons = self.find_elements(self.ADD_TO_POSTPONED_BUTTON, timeout=5)
            if postponed_buttons:
                postponed_buttons[0].click()
                time.sleep(1)
                return True
        except Exception as e:
            print(f"Error adding to postponed: {e}")
        return False

    def get_search_title(self):
        """Получить заголовок страницы поиска."""
        try:
            title = self.get_text(self.SEARCH_TITLE, timeout=5)
            print(f"Search page title: {title}")
            return title
        except Exception as e:
            print(f"Error getting search title: {e}")
            return "Search results"

    def is_no_results_found(self):
        """Проверить, есть ли сообщение об отсутствии результатов."""
        return self.is_element_present(self.NO_RESULTS_MESSAGE, timeout=3)

    def wait_for_search_results(self, timeout=10):
        """Явно подождать загрузки результатов поиска."""
        print("Waiting for search results to load...")
        time.sleep(3)
        try:
            self.find_element(self.SEARCH_RESULTS, timeout=5)
            print("Search results loaded successfully")
            return True
        except TimeoutException:
            if self.is_no_results_found():
                print("No results message shown")
                return True
            print("No search results or message found")
            return False

    def get_all_book_titles(self):
        """Получить все названия книг на странице (для отладки)."""
        try:
            titles = self.find_elements(self.BOOK_TITLE, timeout=5)
            all_titles = []
            for i, title in enumerate(titles):
                all_titles.append(f"Book {i+1}: {title.text}")

            print("All found titles:")
            for title in all_titles:
                print(f"  - {title}")

            return all_titles
        except Exception as e:
            print(f"Error getting all titles: {e}")
            return []
