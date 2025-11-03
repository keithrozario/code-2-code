from sqlalchemy.orm import Session
from sqlalchemy import select

from app.moneynote.models.group import Group

def get(db: Session, id: int) -> Group | None:
    return db.execute(select(Group).filter(Group.id == id)).scalar_one_or_none()
