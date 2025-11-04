from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app.main import app
from app.database import get_db
from app.moneynote.models import Base, User, Group, Book
from app.moneynote.routers.deps import get_current_user

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./app/tests/test_users.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="session")
def session_fixture():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(name="client")
def client_fixture(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

# Test cases
def test_get_init_state_unauthenticated(client):
    response = client.get("/api/v1/users/initState")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_get_init_state_user_with_defaults(client, session):
    # Override dependency to return the correct user for this test
    def override_get_current_user():
        return "testuser"
    app.dependency_overrides[get_current_user] = override_get_current_user

    # Create a user, group, and book
    user = User(username="testuser", email="test@example.com", default_group_id=1, default_book_id=1)
    session.add(user)
    session.commit()
    session.refresh(user)

    group = Group(id=1, name="Default Group")
    session.add(group)
    session.commit()
    session.refresh(group)

    book = Book(id=1, name="Default Book")
    session.add(book)
    session.commit()
    session.refresh(book)

    response = client.get("/api/v1/users/initState", headers={"Authorization": "Bearer test"})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["user"]["username"] == "testuser"
    assert response_data["group"]["name"] == "Default Group"
    assert response_data["book"]["name"] == "Default Book"

    # Clean up the override
    app.dependency_overrides.clear()

def test_get_init_state_user_with_partial_defaults(client, session):
    # Override dependency to return the correct user for this test
    def override_get_current_user():
        return "testuser2"
    app.dependency_overrides[get_current_user] = override_get_current_user

    # Create a user with default group but no default book
    user = User(username="testuser2", email="test2@example.com", default_group_id=1, default_book_id=None)
    session.add(user)
    session.commit()
    session.refresh(user)

    group = Group(id=1, name="Default Group")
    session.add(group)
    session.commit()
    session.refresh(group)

    response = client.get("/api/v1/users/initState", headers={"Authorization": "Bearer test"})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["user"]["username"] == "testuser2"
    assert response_data["group"]["name"] == "Default Group"
    assert response_data["book"] is None

    # Clean up the override
    app.dependency_overrides.clear()

def test_get_init_state_user_with_no_defaults(client, session):
    # Override dependency to return the correct user for this test
    def override_get_current_user():
        return "testuser3"
    app.dependency_overrides[get_current_user] = override_get_current_user

    # Create a user with no default group or book
    user = User(username="testuser3", email="test3@example.com", default_group_id=None, default_book_id=None)
    session.add(user)
    session.commit()
    session.refresh(user)

    response = client.get("/api/v1/users/initState", headers={"Authorization": "Bearer test"})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["user"]["username"] == "testuser3"
    assert response_data["group"] is None
    assert response_data["book"] is None

    # Clean up the override
    app.dependency_overrides.clear()
