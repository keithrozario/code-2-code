import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from main import app
from database import Base, get_db
import crud, schemas

# Use a single test database for the entire test session
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Apply the dependency override for the app
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_database():
    """Fixture to create and drop the test database once per session."""
    if os.path.exists("./test.db"):
        os.remove("./test.db")
    Base.metadata.create_all(bind=engine)
    yield
    if os.path.exists("./test.db"):
        os.remove("./test.db")

@pytest.fixture(scope="function")
def db_session(setup_and_teardown_database):
    """Yield a new database session for a test, rolling back transactions."""
    connection = engine.connect()
    transaction = connection.begin()
    db = TestingSessionLocal(bind=connection)
    try:
        yield db
    finally:
        db.close()
        transaction.rollback()
        connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Yield a TestClient for a test, ensuring the db is clean."""
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def authenticated_client(client, db_session):
    """Yield an authenticated client. Creates a new user for each test."""
    user_data = {"username": "testuser", "email": "test@example.com", "password": "password"}
    # Use CRUD directly to avoid API dependency and state issues
    crud.create_user(db=db_session, user=schemas.UserCreate(**user_data))
    
    login_data = {"username": user_data["username"], "password": user_data["password"]}
    response = client.post("/users/login", data=login_data)
    token = response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    client.headers = headers
    return client
