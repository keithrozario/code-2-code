from sqlalchemy.orm import Session
from sqlalchemy import select

from app.moneynote.models import User

def get_by_username(db: Session, username: str) -> User | None:
    return db.execute(select(User).filter(User.username == username)).scalar_one_or_none()
