import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db
import crud, schemas

# Setup the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_payees.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def db_session(request):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def authenticated_client(db_session):
    """Provides a base authenticated client."""
    user_data = {"username": "testuser_payees", "email": "payees@test.com", "password": "password"}
    client.post("/users/register", json=user_data)
    login_data = {"username": user_data["username"], "password": user_data["password"]}
    response = client.post("/users/login", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    client.headers = headers
    return client

@pytest.fixture(scope="function")
def authenticated_client_with_book(authenticated_client):
    """Provides an authenticated client and a book ID owned by that user."""
    client = authenticated_client
    book_data = {"name": "Test Book for Payees", "defaultCurrencyCode": "USD"}
    book_resp = client.post("/books/", json=book_data)
    book_id = book_resp.json()["id"]
    return client, book_id

def test_create_payee_success(authenticated_client_with_book):
    client, book_id = authenticated_client_with_book
    payee_data = {"name": "Supermarket"}
    response = client.post(f"/payees/?book_id={book_id}", json=payee_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Supermarket"
    assert data["book_id"] == book_id

def test_get_payees_for_book(authenticated_client_with_book):
    client, book_id = authenticated_client_with_book
    client.post(f"/payees/?book_id={book_id}", json={"name": "Landlord"})
    client.post(f"/payees/?book_id={book_id}", json={"name": "Gas Station"})

    response = client.get(f"/payees/?book_id={book_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[1]["name"] == "Gas Station"

def test_delete_payee_success(authenticated_client_with_book):
    client, book_id = authenticated_client_with_book
    payee_resp = client.post(f"/payees/?book_id={book_id}", json={"name": "ToDelete"})
    payee_id = payee_resp.json()["id"]

    # Delete the payee
    response = client.delete(f"/payees/{payee_id}")
    assert response.status_code == 200

    # Verify it's gone
    get_resp = client.get(f"/payees/?book_id={book_id}")
    assert len(get_resp.json()) == 0