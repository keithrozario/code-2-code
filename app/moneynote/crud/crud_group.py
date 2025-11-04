from sqlalchemy.orm import Session
from sqlalchemy import select

from app.moneynote.models.group import Group
from app.moneynote.schemas.group import GroupCreate

def get(db: Session, id: int) -> Group | None:
    return db.execute(select(Group).filter(Group.id == id)).scalar_one_or_none()

def get_by_name(db: Session, name: str) -> Group | None:
    return db.execute(select(Group).filter(Group.name == name)).scalar_one_or_none()

def create(db: Session, group: GroupCreate, user_id: int) -> Group:
    db_group = Group(**group.dict(), user_id=user_id)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group
