import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import requests


def pytest_addoption(parser):
    """Добавляем кастомные параметры командной строки."""
    parser.addoption(
        "--browser_name",
        action="store",
        default="chrome",
        help="Choose browser: chrome or firefox"
    )
    parser.addoption(
        "--base_url",
        action="store",
        default="https://www.labirint.ru",
        help="Base URL for tests"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )


@pytest.fixture(scope="function")
def browser(request):
    """Фикстура для инициализации браузера."""
    browser_name = request.config.getoption("browser_name")
    base_url = request.config.getoption("base_url")
    headless = request.config.getoption("headless")

    if browser_name == "chrome":
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        browser = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        browser = webdriver.Firefox(options=options)
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")

    browser.base_url = base_url
    browser.implicitly_wait(10)
    browser.maximize_window()

    yield browser

    # Закрываем браузер после теста
    browser.quit()


@pytest.fixture(scope="function")
def api_client():
    """Фикстура для API клиента."""
    base_url = "https://www.labirint.ru"

    def _api_client(endpoint="", method="GET", data=None, params=None):
        """
        Универсальный API клиент.

        Args:
            endpoint: API endpoint
            method: HTTP method (GET, POST)
            data: данные для тела запроса
            params: параметры URL

        Returns:
            Response object
        """
        url = f"{base_url}{endpoint}"
        request_params = params or data

        try:
            if method.upper() == "GET":
                response = requests.get(url, params=request_params, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, data=request_params, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            return response
        except requests.exceptions.RequestException as e:
            pytest.fail(f"API request failed: {e}")

    return _api_client


@pytest.fixture(scope="function")
def main_page(browser):
    """Фикстура для главной страницы."""
    from pages.main_page import MainPage
    return MainPage(browser)


@pytest.fixture(scope="function")
def search_page(browser):
    """Фикстура для страницы поиска."""
    from pages.search_page import SearchPage
    return SearchPage(browser)
