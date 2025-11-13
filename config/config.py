import os
from dotenv import load_dotenv

load_dotenv()  # Это строка загружает переменные из .env файла


class Config:
    """Конфигурация проекта"""

    # URL тестового окружения
    BASE_URL = os.getenv("BASE_URL", "https://www.labirint.ru")  # Значение по умолчанию

    # Настройки браузера
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT", "15"))
    WINDOW_SIZE = os.getenv("WINDOW_SIZE", "1920,1080")

    # Настройки API
    API_TIMEOUT = 30