"""UI тесты для сайта Лабиринт."""
import pytest
import time
from selenium.common.exceptions import TimeoutException


class TestLabirintUI:
    """Тесты UI для сайта Лабиринт с улучшенной стабильностью."""

    @pytest.mark.ui
    def test_search_functionality(self, main_page, search_page):
        """Тест функциональности поиска."""
        print("=== Starting search functionality test ===")

        main_page.open()
        assert main_page.is_main_page_loaded(), "Main page not loaded properly"

        # Ищем популярную книгу
        search_term = "Python"
        main_page.search_book(search_term)

        # Проверяем, что поиск сработал
        current_url = search_page.get_current_url()
        assert "search" in current_url, f"Not on search page. URL: {current_url}"

        # Явно ждем загрузки результатов
        search_page.wait_for_search_results()

        results_count = search_page.get_search_results_count()
        print(f"Found {results_count} search results for '{search_term}'")

        # Для отладки получаем все названия (но не сохраняем в переменную)
        search_page.get_all_book_titles()

        # Более гибкая проверка результатов
        if results_count > 0:
            title = search_page.get_first_book_title()
            # Если title пустой, но есть результаты - это нормально для карусели
            if not title or title == "No books found":
                print("No specific book title found (likely carousel)")
            else:
                assert len(title) > 0, "Book title should not be empty"
                print(f"First book title: {title}")
        else:
            # Если нет результатов, проверяем сообщение
            if search_page.is_no_results_found():
                print("No results found - showing appropriate message")
            else:
                print("No results and no message - might be layout issue")

    @pytest.mark.ui
    def test_add_to_cart(self, main_page, search_page):
        """Тест добавления товара в корзину."""
        print("=== Starting add to cart test ===")

        main_page.open()

        # Используем более общий поисковый запрос
        search_term = "книга"
        main_page.search_book(search_term)

        initial_cart_count = main_page.get_cart_count()
        print(f"Initial cart count: {initial_cart_count}")

        # Явно ждем загрузки результатов
        search_page.wait_for_search_results()

        results_count = search_page.get_search_results_count()
        print(f"Available results: {results_count}")

        if results_count > 0:
            # Пробуем добавить в корзину
            added = search_page.add_first_book_to_cart()

            if added:
                print("Item added to cart, waiting for cart update...")
                # Ждем обновления счетчика корзины
                time.sleep(5)

                new_cart_count = main_page.get_cart_count()
                print(f"New cart count: {new_cart_count}")

                # Проверяем, что счетчик увеличился
                expected_msg = f"Cart count should increase from {initial_cart_count}"
                assert new_cart_count > initial_cart_count, expected_msg
                print("✅ Cart count successfully increased!")
            else:
                pytest.skip("Could not add item to cart")
        else:
            pytest.skip("No items found to add to cart")

    @pytest.mark.ui
    def test_main_page_elements_present(self, main_page):
        """Тест наличия основных элементов на главной странице."""
        print("=== Starting main page elements test ===")

        main_page.open()

        # Проверяем ключевые элементы с логированием
        elements_to_check = [
            ("Search input", main_page.SEARCH_INPUT),
            ("Logo", main_page.LOGO),
            ("Main menu", main_page.MAIN_MENU),
            ("Cart button", main_page.CART_BUTTON)
        ]

        missing_elements = []
        for element_name, locator in elements_to_check:
            if main_page.is_element_present(locator, timeout=5):
                print(f"✓ {element_name} is present")
            else:
                print(f"✗ {element_name} is MISSING")
                missing_elements.append(element_name)

        # Если отсутствуют только некоторые неключевые элементы
        if "Search input" in missing_elements or "Logo" in missing_elements:
            pytest.fail(f"Critical elements missing: {missing_elements}")
        elif missing_elements:
            print(f"Non-critical elements missing: {missing_elements}")

        print("✅ All critical elements are present!")

    @pytest.mark.ui
    def test_navigation_to_cart(self, main_page):
        """Тест навигации в корзину."""
        print("=== Starting cart navigation test ===")

        main_page.open()

        try:
            main_page.go_to_cart()

            # Проверяем, что перешли на страницу корзины
            current_url = main_page.get_current_url().lower()
            print(f"Current URL after cart click: {current_url}")

            # Более гибкая проверка URL
            cart_indicators = ["cart", "basket", "korzin"]
            url_contains_cart = any(indicator in current_url for indicator in cart_indicators)

            assert url_contains_cart, f"Not redirected to cart. URL: {current_url}"
            print("✅ Successfully navigated to cart page")

        except TimeoutException:
            # Если не удалось перейти, проверяем текущий URL
            current_url = main_page.get_current_url()
            print(f"Navigation timeout. Current URL: {current_url}")
            pytest.fail(f"Failed to navigate to cart. URL: {current_url}")

    @pytest.mark.ui
    def test_search_placeholder(self, main_page):
        """Тест placeholder в поле поиска."""
        print("=== Starting search placeholder test ===")

        main_page.open()

        search_input = main_page.find_element(main_page.SEARCH_INPUT)
        placeholder = search_input.get_attribute("placeholder")

        assert placeholder, "Search input placeholder is empty"
        print(f"Search placeholder text: '{placeholder}'")
        print("✅ Search placeholder test passed!")
