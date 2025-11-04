from sqlalchemy.orm import Session
from sqlalchemy import select

from app.moneynote.models.book import Book
from app.moneynote.schemas.book import BookCreate

def get(db: Session, id: int) -> Book | None:
    return db.execute(select(Book).filter(Book.id == id)).scalar_one_or_none()

def get_by_name(db: Session, name: str) -> Book | None:
    return db.execute(select(Book).filter(Book.name == name)).scalar_one_or_none()

def create(db: Session, book: BookCreate, user_id: int) -> Book:
    db_book = Book(**book.dict(), user_id=user_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
