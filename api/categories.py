from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import models
import dependencies
from database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Category)
def create_category(
    book_id: int,
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None or db_book.group_id != current_user.group.id:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.create_category(db=db, category=category, book_id=book_id)


@router.get("/", response_model=List[schemas.Category])
def read_categories(
    book_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None or db_book.group_id != current_user.group.id:
        raise HTTPException(status_code=404, detail="Book not found")
    categories = crud.get_categories_by_book(db, book_id=book_id, skip=skip, limit=limit)
    return categories


@router.delete("/{category_id}", response_model=schemas.Category)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    if db_category.book.group_id != current_user.group.id:
        raise HTTPException(status_code=404, detail="Category not found")
    if db_category.children:
        raise HTTPException(status_code=400, detail="Cannot delete category with children")
    return crud.delete_category(db=db, db_category=db_category)
