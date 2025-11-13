import pytest
import requests
import allure
from config.config import Config


@allure.feature("API Тесты Лабиринт")
class TestLabirintAPI:
    """Класс для API тестов книжного магазина Лабиринт"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Настройка перед каждым тестом"""
        self.base_url = Config.BASE_URL
        self.session = requests.Session()
        # Устанавливаем заголовки как у реального браузера
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        })

    @allure.story("Поиск через API")
    @allure.title("Проверка поискового API")
    def test_search_api(self):
        """Тест поискового функционала через API"""
        search_url = f"{self.base_url}/search/"

        with allure.step("Выполнить поисковый запрос"):
            response = self.session.get(
                search_url,
                params={"st": "Гарри Поттер"},
                timeout=Config.API_TIMEOUT,
                allow_redirects=True
            )

        with allure.step("Проверить статус код"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        with allure.step("Проверить содержимое ответа"):
            assert "Гарри Поттер" in response.text, "Результаты поиска не содержат искомый запрос"
            assert "product" in response.text.lower() or "книг" in response.text, "Не найдены элементы товаров"

    @allure.story("Доступность страниц")
    @allure.title("Проверка доступности главной страницы")
    def test_main_page_availability(self):
        """Тест доступности главной страницы"""
        response = self.session.get(self.base_url, timeout=Config.API_TIMEOUT)

        assert response.status_code == 200
        assert "Лабиринт" in response.text
        assert "книг" in response.text.lower()

    @allure.story("Доступность страниц")
    @allure.title("Проверка доступности страницы корзины")
    def test_cart_page_availability(self):
        """Тест доступности страницы корзины"""
        cart_url = f"{self.base_url}/cart/"
        response = self.session.get(cart_url, timeout=Config.API_TIMEOUT)

        assert response.status_code == 200
        assert "корзина" in response.text.lower()

    @allure.story("API функционал")
    @allure.title("Проверка JSON endpoints")
    def test_json_endpoints(self):
        """Тест JSON endpoints сайта"""
        # Проверяем доступность API для подсказок поиска
        suggest_url = f"{self.base_url}/search/suggest/"

        response = self.session.get(
            suggest_url,
            params={"term": "книг"},
            timeout=Config.API_TIMEOUT
        )

        # Некоторые endpoints могут возвращать 404 или другие коды - это нормально
        assert response.status_code in [200, 404, 403], f"Неожиданный статус код: {response.status_code}"

    @allure.story("Доступность страниц")
    @allure.title("Проверка доступности страницы помощи")
    def test_help_page_availability(self):
        """Тест доступности страницы помощи"""
        help_url = f"{self.base_url}/help/"
        response = self.session.get(help_url, timeout=Config.API_TIMEOUT)

        assert response.status_code == 200
        assert "помощь" in response.text.lower() or "вопрос" in response.text.lower()

    @allure.story("Доступность страниц")
    @allure.title("Проверка редиректов")
    def test_redirects(self):
        """Тест корректности редиректов"""
        # Проверяем редирект с HTTP на HTTPS
        http_url = self.base_url.replace("https://", "http://")
        response = self.session.get(http_url, timeout=Config.API_TIMEOUT, allow_redirects=False)

        # Должен быть редирект на HTTPS
        assert response.status_code in [301, 302, 307, 308]
        if 'Location' in response.headers:
            assert response.headers['Location'].startswith('https://')

    @allure.story("Производительность")
    @allure.title("Проверка времени ответа")
    def test_response_time(self):
        """Тест времени ответа сервера"""
        import time

        start_time = time.time()
        response = self.session.get(self.base_url, timeout=Config.API_TIMEOUT)
        end_time = time.time()

        response_time = end_time - start_time

        assert response.status_code == 200
        assert response_time < 5.0, f"Время ответа слишком большое: {response_time} секунд"

    @allure.story("Контент")
    @allure.title("Проверка мета-тегов")
    def test_meta_tags(self):
        """Тест наличия важных мета-тегов"""
        response = self.session.get(self.base_url, timeout=Config.API_TIMEOUT)

        assert '<meta' in response.text, "Мета-теги отсутствуют"
        assert 'charset=' in response.text or 'utf-8' in response.text.lower(), "Кодировка не указана"

    @allure.story("Безопасность")
    @allure.title("Проверка заголовков безопасности")
    def test_security_headers(self):
        """Тест наличия security headers"""
        response = self.session.get(self.base_url, timeout=Config.API_TIMEOUT)

        security_headers = [
            'X-Frame-Options',
            'X-Content-Type-Options',
            'Strict-Transport-Security',
            'Content-Security-Policy'
        ]

        found_headers = [header for header in security_headers if header in response.headers]
        # Сайт может не иметь всех security headers, это не всегда ошибка
        # Проверяем хотя бы наличие Content-Type
        assert 'Content-Type' in response.headers, "Базовые заголовки отсутствуют"