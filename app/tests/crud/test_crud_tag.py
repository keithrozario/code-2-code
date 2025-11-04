import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.moneynote.models import Base, User, Group, Book, Tag
from app.moneynote.schemas.group import GroupCreate
from app.moneynote.schemas.book import BookCreate
from app.moneynote.crud import crud_group, crud_book, crud_tag

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./app/tests/test_crud_tag.db"
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

@pytest.fixture(name="from_book")
def from_book_fixture(session: Session, test_user: User):
    group = crud_group.create(db=session, group=GroupCreate(name="Test Group"), user_id=test_user.id)
    book = crud_book.create(db=session, book=BookCreate(name="From Book", group_id=group.id), user_id=test_user.id)
    return book

@pytest.fixture(name="to_book")
def to_book_fixture(session: Session, test_user: User):
    group = crud_group.create(db=session, group=GroupCreate(name="Test Group 2"), user_id=test_user.id)
    book = crud_book.create(db=session, book=BookCreate(name="To Book", group_id=group.id), user_id=test_user.id)
    return book

def test_copy_tags(session: Session, from_book: Book, to_book: Book):
    # Create tags in the from_book
    parent_tag = Tag(name="Parent", book_id=from_book.id)
    session.add(parent_tag)
    session.commit()
    session.refresh(parent_tag)

    child_tag = Tag(name="Child", book_id=from_book.id, parent_id=parent_tag.id)
    session.add(child_tag)
    session.commit()

    # Call the copy function
    crud_tag.copy_tags(db=session, from_book_id=from_book.id, to_book_id=to_book.id)

    # Verify the copied tags
    copied_tags = session.query(Tag).filter(Tag.book_id == to_book.id).all()
    assert len(copied_tags) == 2

    copied_parent = next((t for t in copied_tags if t.name == "Parent"), None)
    assert copied_parent is not None
    assert copied_parent.parent_id is None

    copied_child = next((t for t in copied_tags if t.name == "Child"), None)
    assert copied_child is not None
    assert copied_child.parent_id == copied_parent.id
