from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import models
import dependencies
from database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Account)
def create_account(
    account: schemas.AccountCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    # A user can only create an account in their own group
    return crud.create_account(db=db, account=account, group_id=current_user.group.id)


@router.get("/", response_model=List[schemas.Account])
def read_accounts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    # A user can only see accounts in their own group
    accounts = crud.get_accounts_by_group(db, group_id=current_user.group.id, skip=skip, limit=limit)
    return accounts


@router.get("/{account_id}", response_model=schemas.Account)
def read_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    db_account = crud.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    # A user can only see an account in their own group
    if db_account.group_id != current_user.group.id:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@router.put("/{account_id}", response_model=schemas.Account)
def update_account(
    account_id: int,
    account: schemas.AccountUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    db_account = crud.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    # A user can only update an account in their own group
    if db_account.group_id != current_user.group.id:
        raise HTTPException(status_code=404, detail="Account not found")
    return crud.update_account(db=db, db_account=db_account, account_in=account)


@router.delete("/{account_id}", response_model=schemas.Account)
def delete_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    db_account = crud.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    # A user can only delete an account in their own group
    if db_account.group_id != current_user.group.id:
        raise HTTPException(status_code=404, detail="Account not found")
    return crud.delete_account(db=db, db_account=db_account)
