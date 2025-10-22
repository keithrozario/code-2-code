import importlib
import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_default_settings():
    """
    Test that the default settings are loaded correctly when environment variables are not set.
    """
    with patch.dict(os.environ, {}, clear=True):
        import config

        importlib.reload(config)
        assert config.settings.APP_VERSION == "0.1.0"
        assert config.settings.BASE_URL == "http://localhost:8000"


def test_env_override_settings():
    """
    Test that the settings can be overridden with environment variables.
    """
    test_env = {"APP_VERSION": "test-v9.9.9", "BASE_URL": "http://test.example.com"}
    with patch.dict(os.environ, test_env, clear=True):
        import config

        importlib.reload(config)
        assert config.settings.APP_VERSION == "test-v9.9.9"
        assert config.settings.BASE_URL == "http://test.example.com"
