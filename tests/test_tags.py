import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db
import crud, schemas

# Setup the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_tags.db"
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
def authenticated_client_with_book(db_session):
    """Provides an authenticated client and a book ID owned by that user."""
    user_data = {"username": "testuser_tags", "email": "tags@test.com", "password": "password"}
    client.post("/users/register", json=user_data)
    login_data = {"username": user_data["username"], "password": user_data["password"]}
    response = client.post("/users/login", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    client.headers = headers

    book_data = {"name": "Test Book for Tags", "defaultCurrencyCode": "USD"}
    book_resp = client.post("/books/", json=book_data)
    book_id = book_resp.json()["id"]
    
    return client, book_id

def test_create_tag_success(authenticated_client_with_book):
    client, book_id = authenticated_client_with_book
    tag_data = {"name": "Urgent"}
    response = client.post(f"/tags/?book_id={book_id}", json=tag_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Urgent"
    assert data["book_id"] == book_id

def test_get_tags_for_book(authenticated_client_with_book):
    client, book_id = authenticated_client_with_book
    client.post(f"/tags/?book_id={book_id}", json={"name": "Work"})
    client.post(f"/tags/?book_id={book_id}", json={"name": "Personal"})

    response = client.get(f"/tags/?book_id={book_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[1]["name"] == "Personal"

def test_delete_tag_success(authenticated_client_with_book):
    client, book_id = authenticated_client_with_book
    tag_resp = client.post(f"/tags/?book_id={book_id}", json={"name": "ToDelete"})
    tag_id = tag_resp.json()["id"]

    # Delete the tag
    response = client.delete(f"/tags/{tag_id}")
    assert response.status_code == 200

    # Verify it's gone
    get_resp = client.get(f"/tags/?book_id={book_id}")
    assert len(get_resp.json()) == 0