import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import get_db
from app.moneynote.models import Base, User, Group, Book
from app.moneynote.schemas.group import GroupCreate
from app.moneynote.routers.deps import get_current_user

# Setup test database
from sqlalchemy import create_engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./app/tests/test_groups_router.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
from sqlalchemy.orm import sessionmaker
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

@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    user = User(username="testuser", email="test@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def test_create_group(client: TestClient, test_user: User, mock_auth):
    user_id = test_user.id  # Get the ID before the API call
    response = client.post("/api/v1/groups/", json={"name": "Test Group"}, headers={"Authorization": "Bearer test"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Group"
    assert data["user_id"] == user_id

    # Verify the group and default book were created in the database
    db = next(app.dependency_overrides[get_db]())
    group = db.query(Group).filter(Group.name == "Test Group").first()
    assert group is not None
    book = db.query(Book).filter(Book.group_id == group.id).first()
    assert book is not None
    assert book.name == "Default Book"
