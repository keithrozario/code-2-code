import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.moneynote.models import Base, User, Group, Book, Category
from app.moneynote.schemas.group import GroupCreate
from app.moneynote.schemas.book import BookCreate
from app.moneynote.crud import crud_group, crud_book, crud_category

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_crud_category.db"
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

def test_copy_categories(session: Session, from_book: Book, to_book: Book):
    # Create categories in the from_book
    parent_cat = Category(name="Parent", book_id=from_book.id, type=1)
    session.add(parent_cat)
    session.commit()
    session.refresh(parent_cat)

    child_cat = Category(name="Child", book_id=from_book.id, type=1, parent_id=parent_cat.id)
    session.add(child_cat)
    session.commit()

    # Call the copy function
    crud_category.copy_categories(db=session, from_book_id=from_book.id, to_book_id=to_book.id)

    # Verify the copied categories
    copied_categories = session.query(Category).filter(Category.book_id == to_book.id).all()
    assert len(copied_categories) == 2

    copied_parent = next((c for c in copied_categories if c.name == "Parent"), None)
    assert copied_parent is not None
    assert copied_parent.parent_id is None

    copied_child = next((c for c in copied_categories if c.name == "Child"), None)
    assert copied_child is not None
    assert copied_child.parent_id == copied_parent.id
