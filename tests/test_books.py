import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db
import crud

# Use a separate test database that can be cleanly dropped
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_books.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db_session(request):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def authenticated_client(client):
    user_data = {
        "username": "testuser_books",
        "email": "books@test.com",
        "password": "password",
    }
    client.post("/users/register", json=user_data)
    login_data = {"username": user_data["username"], "password": user_data["password"]}
    response = client.post("/users/login", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    client.headers = headers
    return client


def test_create_book_success(authenticated_client):
    client = authenticated_client
    book_data = {"name": "Personal Finances", "defaultCurrencyCode": "USD"}
    response = client.post("/books/", json=book_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == book_data["name"]
    assert data["defaultCurrencyCode"] == "USD"
    assert "id" in data

    # Delete created book to ensure all test are idempotent
    book_id = response.json()["id"]
    delete_resp = client.delete(f"/books/{book_id}")
    assert delete_resp.status_code == 200
    get_resp = client.get(f"/books/{book_id}")
    assert get_resp.status_code == 404


def test_get_books_success(authenticated_client):
    client = authenticated_client
    client.post("/books/", json={"name": "Book 1", "defaultCurrencyCode": "USD"})
    client.post("/books/", json={"name": "Book 2", "defaultCurrencyCode": "EUR"})

    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[1]["name"] == "Book 2"


def test_delete_empty_book_success(authenticated_client):
    client = authenticated_client
    create_resp = client.post(
        "/books/", json={"name": "Empty Book", "defaultCurrencyCode": "USD"}
    )
    book_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/books/{book_id}")
    assert delete_resp.status_code == 200

    get_resp = client.get(f"/books/{book_id}")
    assert get_resp.status_code == 404
