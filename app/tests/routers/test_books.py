import pytest
from fastapi.testclient import TestClient

from app.database import get_db
from app.moneynote.models import Base, User, Group, Book, BalanceFlow
from app.moneynote.schemas.book import BookCreate, BookUpdateForm
from app.moneynote.schemas.group import GroupCreate

from app.moneynote.crud import (
    crud_group,
    crud_book,
    crud_category,
    crud_tag,
    crud_payee,
)

# Setup test database
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "sqlite:///./app/tests/test_books_router.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
from sqlalchemy.orm import Session
from app.main import app
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


@pytest.fixture(name="test_group")
def test_group_fixture(session: Session, test_user: User):
    group = crud_group.create(
        db=session, group=GroupCreate(name="Test Group"), user_id=test_user.id
    )
    return group


def test_create_book(client: TestClient, test_user: User, test_group: Group, mock_auth):
    user_id = test_user.id
    group_id = test_group.id
    response = client.post(
        "/api/v1/books/",
        json={"name": "Test Book", "group_id": group_id},
        headers={"Authorization": "Bearer test"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Book"
    assert data["user_id"] == user_id
    assert data["group_id"] == group_id

    # Verify the book was created in the database
    db = next(app.dependency_overrides[get_db]())
    book = db.query(Book).filter(Book.name == "Test Book").first()
    assert book is not None


def test_create_book_from_template(
    client: TestClient, test_user: User, test_group: Group, mock_auth
):
    user_id = test_user.id
    group_id = test_group.id
    response = client.post(
        "/api/v1/books/template",
        json={
            "name": "Template Book",
            "group_id": group_id,
            "template_id": "personal_finance",
        },
        headers={"Authorization": "Bearer test"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Template Book"
    assert data["user_id"] == user_id
    assert data["group_id"] == group_id

    # Verify the book and its copied entities were created
    db = next(app.dependency_overrides[get_db]())
    book = db.query(Book).filter(Book.name == "Template Book").first()
    assert book is not None
    # We can add more assertions here to check for copied categories, etc.


def test_copy_book(
    client: TestClient, session: Session, test_user: User, test_group: Group, mock_auth
):
    user_id = test_user.id
    group_id = test_group.id

    # Create a book to copy from and add a category to it
    from_book = crud_book.create(
        db=session,
        book=BookCreate(name="From Book", group_id=group_id),
        user_id=user_id,
    )
    category_to_copy = crud_category.Category(
        name="Test Category", book_id=from_book.id, type=1
    )
    session.add(category_to_copy)
    session.commit()

    response = client.post(
        "/api/v1/books/copy",
        json={
            "from_book_id": from_book.id,
            "new_book_name": "Copied Book",
            "group_id": group_id,
        },
        headers={"Authorization": "Bearer test"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Copied Book"
    assert data["user_id"] == user_id
    assert data["group_id"] == group_id

    # Verify the book and its copied entities were created
    db = next(app.dependency_overrides[get_db]())
    book = db.query(Book).filter(Book.name == "Copied Book").first()
    assert book is not None
    copied_categories = (
        db.query(crud_category.Category)
        .filter(crud_category.Category.book_id == book.id)
        .all()
    )
    assert len(copied_categories) > 0

def test_update_book_success(client: TestClient, session: Session, test_user: User, test_group: Group, mock_auth):
    user_id = test_user.id
    group_id = test_group.id

    # Create a book to update
    book_to_update = crud_book.create(db=session, book=BookCreate(name="Original Book", group_id=group_id), user_id=user_id)

    update_data = {"name": "Updated Book Name", "notes": "New notes", "enable": False}
    response = client.put(f"/api/v1/books/{book_to_update.id}", json=update_data, headers={"Authorization": "Bearer test"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Book Name"
    assert data["notes"] == "New notes"
    assert data["enable"] is False

    # Verify the book was updated in the database
    db = next(app.dependency_overrides[get_db]())
    updated_book = db.query(Book).filter(Book.id == book_to_update.id).first()
    assert updated_book.name == "Updated Book Name"
    assert updated_book.notes == "New notes"
    assert updated_book.enable is False

def test_update_book_name_conflict(client: TestClient, session: Session, test_user: User, test_group: Group, mock_auth):
    user_id = test_user.id
    group_id = test_group.id

    # Create two books in the same group
    book1 = crud_book.create(db=session, book=BookCreate(name="Book One", group_id=group_id), user_id=user_id)
    book2 = crud_book.create(db=session, book=BookCreate(name="Book Two", group_id=group_id), user_id=user_id)

    # Attempt to update book1's name to book2's name
    update_data = {"name": "Book Two"}
    response = client.put(f"/api/v1/books/{book1.id}", json=update_data, headers={"Authorization": "Bearer test"})
    assert response.status_code == 409
    assert response.json() == {"detail": "Book with this name already exists in this group."}

def test_update_book_not_found(client: TestClient, test_user: User, mock_auth):
    # Ensure a user exists, then try to update a non-existent book
    response = client.put(f"/api/v1/books/999", json={"name": "Non Existent"}, headers={"Authorization": "Bearer test"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

def test_update_book_unauthorized(client: TestClient, session: Session, test_user: User, test_group: Group):
    user_id = test_user.id
    group_id = test_group.id

    # Create a book
    book_to_update = crud_book.create(db=session, book=BookCreate(name="Unauthorized Update Book", group_id=group_id), user_id=user_id)

    response = client.put(f"/api/v1/books/{book_to_update.id}", json={"name": "New Name"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_delete_book_success(client: TestClient, session: Session, test_user: User, test_group: Group, mock_auth):
    user_id = test_user.id
    group_id = test_group.id

    # Create an empty book to delete
    book_to_delete = crud_book.create(db=session, book=BookCreate(name="Book to Delete", group_id=group_id), user_id=user_id)

    response = client.delete(f"/api/v1/books/{book_to_delete.id}", headers={"Authorization": "Bearer test"})
    assert response.status_code == 204

    # Verify the book is deleted from the database
    db = next(app.dependency_overrides[get_db]())
    deleted_book = db.query(Book).filter(Book.id == book_to_delete.id).first()
    assert deleted_book is None

def test_delete_book_with_transactions_fails(client: TestClient, session: Session, test_user: User, test_group: Group, mock_auth):
    user_id = test_user.id
    group_id = test_group.id

    # Create a book and add a transaction to it
    book_with_transactions = crud_book.create(db=session, book=BookCreate(name="Book with Transactions", group_id=group_id), user_id=user_id)
    balance_flow = BalanceFlow(book_id=book_with_transactions.id, type=1, amount=100.0, convertedAmount=100.0, createTime=123, title="test", creator_id=user_id, group_id=group_id)
    session.add(balance_flow)
    session.commit()

    response = client.delete(f"/api/v1/books/{book_with_transactions.id}", headers={"Authorization": "Bearer test"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Book cannot be deleted as it still contains transactions."
}

    # Verify the book still exists in the database
    db = next(app.dependency_overrides[get_db]())
    existing_book = db.query(Book).filter(Book.id == book_with_transactions.id).first()
    assert existing_book is not None

def test_delete_book_not_found(client: TestClient, test_user: User, mock_auth):
    # Ensure a user exists, then try to delete a non-existent book
    response = client.delete(f"/api/v1/books/999", headers={"Authorization": "Bearer test"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

def test_delete_book_unauthorized(client: TestClient, session: Session, test_user: User, test_group: Group):

    user_id = test_user.id

    group_id = test_group.id



    # Create a book

    book_to_delete = crud_book.create(db=session, book=BookCreate(name="Unauthorized Book", group_id=group_id), user_id=user_id)



    response = client.delete(f"/api/v1/books/{book_to_delete.id}")

    assert response.json() == {"detail": "Not authenticated"}

def test_export_book_success(client: TestClient, session: Session, test_user: User, test_group: Group, mock_auth):
    user_id = test_user.id
    group_id = test_group.id

    # Create a book and add a transaction to it
    book_to_export = crud_book.create(db=session, book=BookCreate(name="Export Book", group_id=group_id), user_id=user_id)
    balance_flow = BalanceFlow(book_id=book_to_export.id, type=1, amount=100.0, convertedAmount=100.0, createTime=123, title="test", creator_id=user_id, group_id=group_id)
    session.add(balance_flow)
    session.commit()

    response = client.get(f"/api/v1/books/{book_to_export.id}/export", headers={"Authorization": "Bearer test"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert "attachment; filename=" in response.headers["content-disposition"]

def test_export_book_no_transactions(client: TestClient, session: Session, test_user: User, test_group: Group, mock_auth):
    user_id = test_user.id
    group_id = test_group.id

    # Create an empty book
    empty_book = crud_book.create(db=session, book=BookCreate(name="Empty Book", group_id=group_id), user_id=user_id)

    response = client.get(f"/api/v1/books/{empty_book.id}/export", headers={"Authorization": "Bearer test"})
    assert response.status_code == 404
    assert response.json() == {"detail": "No transactions found for this book."}

def test_export_book_not_found(client: TestClient, test_user: User, mock_auth):
    # Ensure a user exists, then try to export a non-existent book
    response = client.get(f"/api/v1/books/999/export", headers={"Authorization": "Bearer test"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}


def test_toggle_book_status(client: TestClient, session: Session, test_user: User, test_group: Group, mock_auth):

    user_id = test_user.id

    group_id = test_group.id



    # Create a book to toggle

    book_to_toggle = crud_book.create(db=session, book=BookCreate(name="Toggle Book", group_id=group_id), user_id=user_id)

    assert book_to_toggle.enable is True



    # First toggle: True -> False

    response = client.patch(f"/api/v1/books/{book_to_toggle.id}/toggle", headers={"Authorization": "Bearer test"})

    assert response.status_code == 200

    assert response.json()["enable"] is False



    # Verify in database

    db = next(app.dependency_overrides[get_db]())

    toggled_book = db.query(Book).filter(Book.id == book_to_toggle.id).first()

    assert toggled_book.enable is False



    # Second toggle: False -> True

    response = client.patch(f"/api/v1/books/{book_to_toggle.id}/toggle", headers={"Authorization": "Bearer test"})

    assert response.status_code == 200

    assert response.json()["enable"] is True



    # Verify in database

    toggled_book = db.query(Book).filter(Book.id == book_to_toggle.id).first()

    assert toggled_book.enable is True



def test_toggle_book_not_found(client: TestClient, test_user: User, mock_auth):

    response = client.patch(f"/api/v1/books/999/toggle", headers={"Authorization": "Bearer test"})

    assert response.status_code == 404

    assert response.json() == {"detail": "Book not found"}




