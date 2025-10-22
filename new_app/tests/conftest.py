import pytest
from fastapi.testclient import TestClient
from main import app
from moneynote.services.data_loader_service import DataLoaderService
from config import settings

@pytest.fixture(scope="session", autouse=True)
def setup_test_data():
    data_loader = DataLoaderService()
    data_loader.load_all_data(settings)
    app.state.currencies = data_loader.currencies
    app.state.book_templates = data_loader.book_templates

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c