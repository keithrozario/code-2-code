import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db
import models

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
