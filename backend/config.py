"""
Конфигурационный файл для PyLearn приложения.
"""
import os
from pathlib import Path

class Settings:
    """
    Настройки приложения PyLearn.
    """
    
    # Основные настройки
    APP_NAME: str = "PyLearn"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # Настройки сервера
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Пути
    BASE_DIR = Path(__file__).parent
    FRONTEND_DIR = BASE_DIR.parent / "frontend"
    
    # Настройки безопасности для выполнения кода
    CODE_EXECUTION_TIMEOUT: int = 5  # секунд
    MAX_CODE_LENGTH: int = 1000  # символов

# Создаем экземпляр настроек
settings = Settings()