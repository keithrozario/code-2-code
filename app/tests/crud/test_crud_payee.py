import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.moneynote.models import Base, User, Group, Book, Payee
from app.moneynote.schemas.group import GroupCreate
from app.moneynote.schemas.book import BookCreate
from app.moneynote.crud import crud_group, crud_book, crud_payee

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./app/tests/test_crud_payee.db"
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

def test_copy_payees(session: Session, from_book: Book, to_book: Book):
    # Create payees in the from_book
    payee1 = Payee(name="Payee 1", book_id=from_book.id)
    payee2 = Payee(name="Payee 2", book_id=from_book.id)
    session.add_all([payee1, payee2])
    session.commit()

    # Call the copy function
    crud_payee.copy_payees(db=session, from_book_id=from_book.id, to_book_id=to_book.id)

    # Verify the copied payees
    copied_payees = session.query(Payee).filter(Payee.book_id == to_book.id).all()
    assert len(copied_payees) == 2
    assert {p.name for p in copied_payees} == {"Payee 1", "Payee 2"}
