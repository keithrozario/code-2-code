from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional

from app.moneynote.models import Book, User
from app.moneynote.schemas import Book, BookCreate, BookCreateFromTemplate, BookCopy
from app.moneynote.crud import crud_book, crud_category, crud_tag, crud_payee, crud_balance_flow
from app.moneynote.services.data_cache_service import data_cache_service

def create_book(db: Session, book: BookCreate, user_id: int) -> Book:
    db_book = crud_book.get_by_name(db, name=book.name)
    if db_book and db_book.group_id == book.group_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with this name already exists in this group.",
        )
    return crud_book.create(db=db, book=book, user_id=user_id)

def create_book_from_template(db: Session, book_template: BookCreateFromTemplate, user_id: int) -> Book:
    template = data_cache_service.get_book_template_by_id(book_template.template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found.",
        )

    # Create the book
    book_in = BookCreate(name=book_template.name, group_id=book_template.group_id)
    new_book = create_book(db=db, book=book_in, user_id=user_id)

    # For the purpose of this task, we assume template entities are stored in a book with a specific ID.
    # In a real application, this might be handled differently.
    # We will use a placeholder from_book_id for now.
    from_book_id = -1 # Placeholder for template book ID

    # Copy entities from template book to new book
    crud_category.copy_categories(db=db, from_book_id=from_book_id, to_book_id=new_book.id)
    crud_tag.copy_tags(db=db, from_book_id=from_book_id, to_book_id=new_book.id)
    crud_payee.copy_payees(db=db, from_book_id=from_book_id, to_book_id=new_book.id)

    return new_book

def copy_book(db: Session, book_copy: BookCopy, user_id: int) -> Book:
    from_book = crud_book.get(db, id=book_copy.from_book_id)
    if not from_book or from_book.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book to copy from not found or not owned by user.",
        )

    # Create the new book
    book_in = BookCreate(name=book_copy.new_book_name, group_id=book_copy.group_id)
    new_book = create_book(db=db, book=book_in, user_id=user_id)

    # Copy entities from old book to new book
    crud_category.copy_categories(db=db, from_book_id=from_book.id, to_book_id=new_book.id)
    crud_tag.copy_tags(db=db, from_book_id=from_book.id, to_book_id=new_book.id)
    crud_payee.copy_payees(db=db, from_book_id=from_book.id, to_book_id=new_book.id)

    return new_book

def query_books(
    db: Session,
    group_id: int,
    enable: Optional[bool],
    name: Optional[str],
    sort: Optional[str],
    skip: int,
    limit: int,
) -> list[Book]:
    filters = {}
    if enable is not None:
        filters["enable"] = enable
    if name is not None:
        filters["name"] = name

    return crud_book.get_multi_by_group_filtered(
        db=db, group_id=group_id, filters=filters, sort=sort, offset=skip, limit=limit
    )

def get_book_details(db: Session, book_id: int, active_group_id: int) -> Book:
    book = crud_book.get(db, id=book_id)
    if not book or book.group_id != active_group_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

def toggle_book(db: Session, book_id: int, user_id: int) -> Book:
    book = crud_book.get(db, id=book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    if book.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to toggle this book")
    return crud_book.toggle_enable_status(db, book)

def delete_book(db: Session, book_id: int, user_id: int):
    book = crud_book.get(db, id=book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    if book.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this book")

    transaction_count = crud_balance_flow.count_by_book_id(db, book_id=book_id)
    if transaction_count > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book cannot be deleted as it still contains transactions.")

    crud_category.remove_by_book_id(db, book_id=book_id)
    crud_tag.remove_by_book_id(db, book_id=book_id)
    crud_payee.remove_by_book_id(db, book_id=book_id)
    crud_book.remove(db, id=book_id)
