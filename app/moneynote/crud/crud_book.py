from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Any

from app.moneynote.models import Book
from app.moneynote.schemas.book import BookCreate

def get(db: Session, id: int) -> Book | None:
    return db.execute(select(Book).filter(Book.id == id)).scalar_one_or_none()

def get_by_name(db: Session, name: str) -> Book | None:
    return db.execute(select(Book).filter(Book.name == name)).scalar_one_or_none()

def create(db: Session, book: BookCreate, user_id: int) -> Book:
    db_book = Book(**book.model_dump(), user_id=user_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_multi_by_group_filtered(
    db: Session, group_id: int, filters: dict[str, Any], sort: str | None, offset: int = 0, limit: int = 100
) -> list[Book]:
    query = select(Book).filter(Book.group_id == group_id)

    if "name" in filters:
        query = query.filter(Book.name.ilike(f"%{filters['name']}"))
    if "enable" in filters:
        query = query.filter(Book.enable == filters["enable"])

    # Apply sorting
    if sort:
        # Basic sorting, can be extended for more complex cases
        if hasattr(Book, sort):
            query = query.order_by(getattr(Book, sort))

    query = query.offset(offset).limit(limit)
    return db.execute(query).scalars().all()
