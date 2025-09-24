from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import models
import dependencies
from database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    return crud.create_book(db=db, book=book, group_id=current_user.group.id)


@router.get("/", response_model=List[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    books = crud.get_books_by_group(db, group_id=current_user.group.id, skip=skip, limit=limit)
    return books


@router.get("/{book_id}", response_model=schemas.Book)
def read_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_book.group_id != current_user.group.id:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.put("/{book_id}", response_model=schemas.Book)
def update_book(
    book_id: int,
    book: schemas.BookUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_book.group_id != current_user.group.id:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.update_book(db=db, db_book=db_book, book_in=book)


@router.delete("/{book_id}", response_model=schemas.Book)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_book.group_id != current_user.group.id:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.delete_book(db=db, db_book=db_book)
