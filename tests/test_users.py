import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import timedelta

from main import app
from database import Base, get_db
import models
import security

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the test database
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_user_success(db_session):
    response = client.post(
        "/users/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "hashed_password" not in data

def test_create_user_duplicate_email(db_session):
    # Create a user first
    client.post(
        "/users/register",
        json={"username": "testuser1", "email": "test1@example.com", "password": "password"},
    )
    # Attempt to create another user with the same email
    response = client.post(
        "/users/register",
        json={"username": "testuser2", "email": "test1@example.com", "password": "password"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

def test_create_user_duplicate_username(db_session):
    # Create a user first
    client.post(
        "/users/register",
        json={"username": "testuser3", "email": "test3@example.com", "password": "password"},
    )
    # Attempt to create another user with the same username
    response = client.post(
        "/users/register",
        json={"username": "testuser3", "email": "test4@example.com", "password": "password"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}

def test_password_hashing(db_session):
    response = client.post(
        "/users/register",
        json={"username": "testuser5", "email": "test5@example.com", "password": "a_very_secret_password"},
    )
    assert response.status_code == 200
    user_id = response.json()["id"]
    
    user_in_db = db_session.query(models.User).filter(models.User.id == user_id).first()
    assert user_in_db
    assert user_in_db.hashed_password != "a_very_secret_password"

def test_login_success(db_session):
    # Create user
    client.post(
        "/users/register",
        json={"username": "logintest", "email": "login@test.com", "password": "password"},
    )
    # Attempt to login
    response = client.post(
        "/users/login",
        data={"username": "logintest", "password": "password"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_password(db_session):
    # Create user
    client.post(
        "/users/register",
        json={"username": "logintest2", "email": "login2@test.com", "password": "password"},
    )
    # Attempt to login with wrong password
    response = client.post(
        "/users/login",
        data={"username": "logintest2", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

def test_login_invalid_username(db_session):
    response = client.post(
        "/users/login",
        data={"username": "nonexistentuser", "password": "password"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

def test_get_me_success(db_session):
    # Create and login user to get a token
    client.post("/users/register", json={"username": "me_user", "email": "me@example.com", "password": "password"})
    login_response = client.post("/users/login", data={"username": "me_user", "password": "password"})
    token = login_response.json()["access_token"]

    # Access protected route
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "me_user"
    assert data["email"] == "me@example.com"

def test_get_me_no_token():
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_get_me_invalid_token():
    response = client.get("/users/me", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}

def test_get_me_expired_token():
    # Create an expired token
    expired_token = security.create_access_token(
        data={"sub": "testuser"}, expires_delta=timedelta(minutes=-1)
    )
    response = client.get("/users/me", headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}
