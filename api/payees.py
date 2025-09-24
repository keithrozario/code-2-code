from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import models
import dependencies
from database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Payee)
def create_payee(
    book_id: int,
    payee: schemas.PayeeCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None or db_book.group_id != current_user.group.id:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.create_payee(db=db, payee=payee, book_id=book_id)


@router.get("/", response_model=List[schemas.Payee])
def read_payees(
    book_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None or db_book.group_id != current_user.group.id:
        raise HTTPException(status_code=404, detail="Book not found")
    payees = crud.get_payees_by_book(db, book_id=book_id, skip=skip, limit=limit)
    return payees


@router.delete("/{payee_id}", response_model=schemas.Payee)
def delete_payee(
    payee_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    db_payee = crud.get_payee(db, payee_id=payee_id)
    if db_payee is None:
        raise HTTPException(status_code=404, detail="Payee not found")
    if db_payee.book.group_id != current_user.group.id:
        raise HTTPException(status_code=404, detail="Payee not found")
    return crud.delete_payee(db=db, db_payee=db_payee)
