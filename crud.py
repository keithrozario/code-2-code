from sqlalchemy.orm import Session

import models
import schemas
import security

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create a default group for the user
    db_group = models.Group(name=f"{db_user.username}'s Group", owner=db_user)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)

    return db_user
