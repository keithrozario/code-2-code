import pytest
from fastapi import Depends

from app.main import app
from app.moneynote.routers.deps import get_current_user
from app.moneynote.models.user import User


def mock_get_current_user():
    return "testuser"


@pytest.fixture
def mock_auth(monkeypatch):
    app.dependency_overrides[get_current_user] = mock_get_current_user
    yield
    app.dependency_overrides = {}
