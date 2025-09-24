from sqlalchemy.orm import Session

import models
import schemas
import security

# User CRUD functions
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create a default group for the user
    db_group = models.Group(name=f"{db_user.username}'s Group", owner=db_user)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)

    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username=username)
    if not user:
        return False
    if not security.verify_password(password, user.hashed_password):
        return False
    return user

# Account CRUD functions
def get_account(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id).first()

def get_accounts_by_group(db: Session, group_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Account).filter(models.Account.group_id == group_id).offset(skip).limit(limit).all()

def create_account(db: Session, account: schemas.AccountCreate, group_id: int):
    db_account = models.Account(
        name=account.name,
        type=account.type,
        currencyCode=account.currencyCode,
        initialBalance=account.initialBalance,
        balance=account.initialBalance,  # Set current balance to initial balance
        group_id=group_id
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def update_account(db: Session, db_account: models.Account, account_in: schemas.AccountUpdate):
    update_data = account_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_account, key, value)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def delete_account(db: Session, db_account: models.Account):
    db.delete(db_account)
    db.commit()
    return db_account

# Book CRUD functions
def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books_by_group(db: Session, group_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Book).filter(models.Book.group_id == group_id).offset(skip).limit(limit).all()

def create_book(db: Session, book: schemas.BookCreate, group_id: int):
    db_book = models.Book(**book.model_dump(), group_id=group_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, db_book: models.Book, book_in: schemas.BookUpdate):
    update_data = book_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, db_book: models.Book):
    # TODO: In a future phase, check if book has transactions before deleting.
    db.delete(db_book)
    db.commit()
    return db_book
