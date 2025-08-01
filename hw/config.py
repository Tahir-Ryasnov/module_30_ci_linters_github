"""Конфигурация приложения и параметры базы данных."""

import os


class Config:
    """Настройки конфигурации для Flask приложения."""

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///hw_29.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
