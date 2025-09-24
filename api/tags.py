from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import models
import dependencies
from database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Tag)
def create_tag(
    book_id: int,
    tag: schemas.TagCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None or db_book.group_id != current_user.group.id:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.create_tag(db=db, tag=tag, book_id=book_id)


@router.get("/", response_model=List[schemas.Tag])
def read_tags(
    book_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None or db_book.group_id != current_user.group.id:
        raise HTTPException(status_code=404, detail="Book not found")
    tags = crud.get_tags_by_book(db, book_id=book_id, skip=skip, limit=limit)
    return tags


@router.delete("/{tag_id}", response_model=schemas.Tag)
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    db_tag = crud.get_tag(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    if db_tag.book.group_id != current_user.group.id:
        raise HTTPException(status_code=404, detail="Tag not found")
    return crud.delete_tag(db=db, db_tag=db_tag)
