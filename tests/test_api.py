import pytest
import time


class TestLabirintAPI:
    """Тесты API для сайта Лабиринт."""

    @pytest.mark.api
    def test_main_page_status_code(self, api_client):
        """Тест статус-кода главной страницы."""
        response = api_client()
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    @pytest.mark.api
    def test_search_api(self, api_client):
        """Тест API поиска."""
        params = {"search": "Python"}
        response = api_client("/search/", "GET", params=params)

        assert response.status_code == 200, f"Search API returned {response.status_code}"
        assert "text/html" in response.headers["Content-Type"], "Wrong Content-Type"

    @pytest.mark.api
    def test_headers(self, api_client):
        """Тест заголовков ответа."""
        response = api_client()

        assert "Content-Type" in response.headers, "Content-Type header is missing"
        assert "text/html" in response.headers["Content-Type"], "Wrong Content-Type"
        assert "Server" in response.headers, "Server header is missing"

    @pytest.mark.api
    def test_response_time(self, api_client):
        """Тест времени ответа."""
        start_time = time.time()
        response = api_client()
        end_time = time.time()

        response_time = end_time - start_time
        assert response_time < 5, f"Response time too long: {response_time} seconds"
        assert response.status_code == 200, "Request failed during response time test"

    @pytest.mark.api
    def test_page_content(self, api_client):
        """Тест содержимого страницы."""
        response = api_client()

        assert "Лабиринт" in response.text, "Page content doesn't contain expected text"
        assert response.encoding.lower() == "utf-8", f"Wrong encoding: {response.encoding}"
