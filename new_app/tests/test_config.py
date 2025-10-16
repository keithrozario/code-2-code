import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_default_settings(monkeypatch):
    monkeypatch.delenv("APP_VERSION", raising=False)
    monkeypatch.delenv("BASE_URL", raising=False)

    from config import Settings
    settings = Settings()

    assert settings.APP_VERSION == "1.0.0"
    assert settings.BASE_URL == "http://localhost:8000"

def test_env_override_settings(monkeypatch):
    monkeypatch.setenv("APP_VERSION", "2.0.0-test")
    monkeypatch.setenv("BASE_URL", "https://test.host")

    from config import Settings
    settings = Settings()

    assert settings.APP_VERSION == "2.0.0-test"
    assert settings.BASE_URL == "https://test.host"