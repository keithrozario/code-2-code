import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db
import crud

# Setup the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_accounts.db"
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

client = TestClient(app)


@pytest.fixture(scope="function")
def db_session(request):
    # Before the test, create all tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # After the test, drop all tables
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def authenticated_client(db_session):
    """Provides an authenticated client and the user object."""
    user_data = {
        "username": "testuser_accounts",
        "email": "accounts@test.com",
        "password": "password",
    }
    client.post("/users/register", json=user_data)
    login_data = {"username": user_data["username"], "password": user_data["password"]}
    response = client.post("/users/login", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    client.headers = headers
    user = crud.get_user_by_username(db_session, username=user_data["username"])
    return client, user


def test_create_account_unauthenticated():
    # Clear any existing headers
    client.headers = {}
    account_data = {
        "name": "Unauth Account",
        "type": "CHECKING",
        "currencyCode": "USD",
        "initialBalance": 100.0,
    }
    response = client.post("/accounts/", json=account_data)
    assert response.status_code == 401


def test_create_account_success(authenticated_client):
    client, current_user = authenticated_client
    account_data = {
        "name": "Test Checking Account",
        "type": "CHECKING",
        "currencyCode": "USD",
        "initialBalance": 500.0,
    }
    response = client.post("/accounts/", json=account_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == account_data["name"]
    assert data["balance"] == account_data["initialBalance"]
    assert "id" in data

    # Delete account to ensure all test are idempotent
    account_id = response.json()["id"]
    delete_response = client.delete(f"/accounts/{account_id}")
    assert delete_response.status_code == 200
    get_response = client.get(f"/accounts/{account_id}")
    assert get_response.status_code == 404


def test_get_accounts_success(authenticated_client):
    client, current_user = authenticated_client
    # Create a couple of accounts
    client.post(
        "/accounts/",
        json={
            "name": "Account 1",
            "type": "CHECKING",
            "currencyCode": "USD",
            "initialBalance": 100.0,
        },
    )
    client.post(
        "/accounts/",
        json={
            "name": "Account 2",
            "type": "CREDIT",
            "currencyCode": "EUR",
            "initialBalance": -50.0,
        },
    )

    response = client.get("/accounts/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Account 1"
    assert data[1]["name"] == "Account 2"


def test_get_another_users_account(db_session):
    # Create user 1 and their account
    user1_data = {"username": "user1", "email": "user1@test.com", "password": "pw1"}
    client.post("/users/register", json=user1_data)
    login_resp1 = client.post(
        "/users/login", data={"username": "user1", "password": "pw1"}
    )
    token1 = login_resp1.json()["access_token"]

    # Create user 2 and their account
    user2_data = {"username": "user2", "email": "user2@test.com", "password": "pw2"}
    client.post("/users/register", json=user2_data)
    login_resp2 = client.post(
        "/users/login", data={"username": "user2", "password": "pw2"}
    )
    token2 = login_resp2.json()["access_token"]
    client.headers = {"Authorization": f"Bearer {token2}"}
    account_resp = client.post(
        "/accounts/",
        json={
            "name": "User 2 Account",
            "type": "ASSET",
            "currencyCode": "JPY",
            "initialBalance": 10000,
        },
    )
    account_id_user2 = account_resp.json()["id"]

    # As User 1, try to get User 2's account
    client.headers = {"Authorization": f"Bearer {token1}"}
    response = client.get(f"/accounts/{account_id_user2}")
    assert response.status_code == 404


def test_update_account_success(authenticated_client):
    client, current_user = authenticated_client
    account_data = {
        "name": "Original Name",
        "type": "CHECKING",
        "currencyCode": "USD",
        "initialBalance": 100.0,
    }
    create_response = client.post("/accounts/", json=account_data)
    account_id = create_response.json()["id"]

    update_data = {"name": "Updated Name"}
    response = client.put(f"/accounts/{account_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"

    # Verify the change with a GET request
    get_response = client.get(f"/accounts/{account_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Updated Name"


def test_delete_account_success(authenticated_client):
    client, current_user = authenticated_client
    account_data = {
        "name": "To Be Deleted",
        "type": "DEBT",
        "currencyCode": "CAD",
        "initialBalance": 1000.0,
    }
    create_response = client.post("/accounts/", json=account_data)
    account_id = create_response.json()["id"]

    # Delete the account
    delete_response = client.delete(f"/accounts/{account_id}")
    assert delete_response.status_code == 200

    # Verify it's gone
    get_response = client.get(f"/accounts/{account_id}")
    assert get_response.status_code == 404
