import os
from app.config import Settings


def test_settings_default_values():
    settings = Settings()
    assert settings.APP_VERSION == "0.1.0"
    assert settings.BASE_URL == "http://localhost:8000"


def test_settings_from_env(monkeypatch):
    monkeypatch.setenv("APP_VERSION", "0.2.0")
    monkeypatch.setenv("BASE_URL", "http://moneynote.com")
    settings = Settings()
    assert settings.APP_VERSION == "0.2.0"
    assert settings.BASE_URL == "http://moneynote.com"
