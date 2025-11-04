import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.moneynote.models import Base, User, Group
from app.moneynote.schemas.group import GroupCreate
from app.moneynote.crud import crud_group

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./app/tests/test_crud.db"
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

@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    user = User(username="testuser", email="test@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def test_create_group(session: Session, test_user: User):
    group_in = GroupCreate(name="Test Group")
    created_group = crud_group.create(db=session, group=group_in, user_id=test_user.id)
    assert created_group.name == "Test Group"
    assert created_group.user_id == test_user.id
    assert created_group.id is not None

    # Verify it's in the database
    db_group = session.get(Group, created_group.id)
    assert db_group is not None
    assert db_group.name == "Test Group"

def test_get_group(session: Session, test_user: User):
    group_in = GroupCreate(name="Test Group")
    created_group = crud_group.create(db=session, group=group_in, user_id=test_user.id)
    
    retrieved_group = crud_group.get(db=session, id=created_group.id)
    assert retrieved_group is not None
    assert retrieved_group.id == created_group.id
    assert retrieved_group.name == "Test Group"

def test_get_group_by_name(session: Session, test_user: User):
    group_in = GroupCreate(name="Unique Group Name")
    crud_group.create(db=session, group=group_in, user_id=test_user.id)
    
    retrieved_group = crud_group.get_by_name(db=session, name="Unique Group Name")
    assert retrieved_group is not None
    assert retrieved_group.name == "Unique Group Name"
