from sqlalchemy.orm import Session
from sqlalchemy import select

from app.moneynote.models.book import Book

def get(db: Session, id: int) -> Book | None:
    return db.execute(select(Book).filter(Book.id == id)).scalar_one_or_none()
