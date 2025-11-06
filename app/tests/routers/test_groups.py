import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import get_db
from app.moneynote.models import Base, User, Group, Book
from app.moneynote.schemas.group import GroupCreate
from app.moneynote.routers.deps import get_current_user

from app.moneynote.crud import crud_user, crud_group

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
    assert response.status_code == 200 # Assuming 200 for now, can be 201
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

def test_read_groups(client: TestClient, test_user: User, mock_auth):
    user_id = test_user.id
    # Create some groups for the user
    crud_group.create(db=next(app.dependency_overrides[get_db]()), group=GroupCreate(name="Group 1"), user_id=user_id)
    crud_group.create(db=next(app.dependency_overrides[get_db]()), group=GroupCreate(name="Group 2"), user_id=user_id)

    response = client.get("/api/v1/groups/", headers={"Authorization": "Bearer test"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Group 1"
    assert data[1]["name"] == "Group 2"

def test_read_groups_pagination(client: TestClient, test_user: User, mock_auth):
    user_id = test_user.id
    # Create 5 groups
    for i in range(1, 6):
        crud_group.create(db=next(app.dependency_overrides[get_db]()), group=GroupCreate(name=f"Group {i}"), user_id=user_id)

    response = client.get("/api/v1/groups/?skip=0&limit=2", headers={"Authorization": "Bearer test"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Group 1"
    assert data[1]["name"] == "Group 2"

    response = client.get("/api/v1/groups/?skip=2&limit=2", headers={"Authorization": "Bearer test"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Group 3"
    assert data[1]["name"] == "Group 4"

def test_read_groups_unauthenticated(client: TestClient):
    response = client.get("/api/v1/groups/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
