import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.moneynote.models import Base, User, Group, Book
from app.moneynote.schemas.group import GroupCreate
from app.moneynote.schemas.book import BookCreate
from app.moneynote.crud import crud_book, crud_group

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./app/tests/test_crud_book.db"
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

@pytest.fixture(name="test_group")
def test_group_fixture(session: Session, test_user: User):
    group = crud_group.create(db=session, group=GroupCreate(name="Test Group"), user_id=test_user.id)
    return group

def test_create_book(session: Session, test_user: User, test_group: Group):
    book_in = BookCreate(name="Test Book", group_id=test_group.id)
    created_book = crud_book.create(db=session, book=book_in, user_id=test_user.id)
    assert created_book.name == "Test Book"
    assert created_book.user_id == test_user.id
    assert created_book.group_id == test_group.id
    assert created_book.id is not None

    # Verify it's in the database
    db_book = session.get(Book, created_book.id)
    assert db_book is not None
    assert db_book.name == "Test Book"

def test_get_book(session: Session, test_user: User, test_group: Group):
    book_in = BookCreate(name="Test Book", group_id=test_group.id)
    created_book = crud_book.create(db=session, book=book_in, user_id=test_user.id)
    
    retrieved_book = crud_book.get(db=session, id=created_book.id)
    assert retrieved_book is not None
    assert retrieved_book.id == created_book.id
    assert retrieved_book.name == "Test Book"

def test_get_book_by_name(session: Session, test_user: User, test_group: Group):
    book_in = BookCreate(name="Unique Book Name", group_id=test_group.id)
    crud_book.create(db=session, book=book_in, user_id=test_user.id)
    
    retrieved_book = crud_book.get_by_name(db=session, name="Unique Book Name")
    assert retrieved_book is not None
    assert retrieved_book.name == "Unique Book Name"
