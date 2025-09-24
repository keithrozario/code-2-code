import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db
import crud, schemas

# Setup the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_categories.db"
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
    user_data = {"username": "testuser_cats", "email": "cats@test.com", "password": "password"}
    client.post("/users/register", json=user_data)
    login_data = {"username": user_data["username"], "password": user_data["password"]}
    response = client.post("/users/login", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    client.headers = headers

    book_data = {"name": "Test Book for Categories", "defaultCurrencyCode": "USD"}
    book_resp = client.post("/books/", json=book_data)
    book_id = book_resp.json()["id"]
    
    return client, book_id

def test_create_category_success(authenticated_client_with_book):
    client, book_id = authenticated_client_with_book
    cat_data = {"name": "Food", "type": "EXPENSE"}
    response = client.post(f"/categories/?book_id={book_id}", json=cat_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Food"
    assert data["book_id"] == book_id

def test_create_category_for_unowned_book(db_session):
    # Create User 1 and their book
    user1_data = {"username": "user1_cat", "email": "user1_cat@test.com", "password": "pw1"}
    client.post("/users/register", json=user1_data)
    login_resp1 = client.post("/users/login", data={"username": "user1_cat", "password": "pw1"})
    token1 = login_resp1.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}
    book_resp = client.post("/books/", json={"name": "User1 Book", "defaultCurrencyCode": "USD"}, headers=headers1)
    book_id_user1 = book_resp.json()["id"]

    # Create User 2
    user2_data = {"username": "user2_cat", "email": "user2_cat@test.com", "password": "pw2"}
    client.post("/users/register", json=user2_data)
    login_resp2 = client.post("/users/login", data={"username": "user2_cat", "password": "pw2"})
    token2 = login_resp2.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    # As User 2, try to create a category for User 1's book
    cat_data = {"name": "Fraudulent Category", "type": "EXPENSE"}
    response = client.post(f"/categories/?book_id={book_id_user1}", json=cat_data, headers=headers2)
    assert response.status_code == 404

def test_get_categories_for_book(authenticated_client_with_book):
    client, book_id = authenticated_client_with_book
    client.post(f"/categories/?book_id={book_id}", json={"name": "Cat Food", "type": "EXPENSE"})
    client.post(f"/categories/?book_id={book_id}", json={"name": "Cat Toys", "type": "EXPENSE"})

    response = client.get(f"/categories/?book_id={book_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Cat Food"

def test_delete_category_fails_if_has_children(authenticated_client_with_book):
    client, book_id = authenticated_client_with_book
    parent_cat_resp = client.post(f"/categories/?book_id={book_id}", json={"name": "Parent", "type": "EXPENSE"})
    parent_id = parent_cat_resp.json()["id"]

    client.post(f"/categories/?book_id={book_id}", json={"name": "Child", "type": "EXPENSE", "parent_id": parent_id})

    # Attempt to delete the parent category
    response = client.delete(f"/categories/{parent_id}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot delete category with children"

def test_delete_empty_category_success(authenticated_client_with_book):
    client, book_id = authenticated_client_with_book
    cat_resp = client.post(f"/categories/?book_id={book_id}", json={"name": "ToDelete", "type": "EXPENSE"})
    category_id = cat_resp.json()["id"]

    # Delete the category
    response = client.delete(f"/categories/{category_id}")
    assert response.status_code == 200

    # Verify it's gone
    get_resp = client.get(f"/categories/?book_id={book_id}")
    assert len(get_resp.json()) == 0