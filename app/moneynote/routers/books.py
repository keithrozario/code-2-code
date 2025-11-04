from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.moneynote.routers.deps import get_current_user
from app.moneynote.schemas.book import Book, BookCreate, BookCreateFromTemplate, BookCopy
from app.moneynote.services import book_service
from app.moneynote.models import User
from app.moneynote.crud import crud_user

router = APIRouter()

@router.post("/", response_model=Book, tags=["Books"])
async def create_book_endpoint(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user_username: str = Depends(get_current_user)
):
    user = crud_user.get_by_username(db, username=current_user_username)
    return book_service.create_book(db=db, book=book, user_id=user.id)

@router.post("/template", response_model=Book, tags=["Books"])
async def create_book_from_template_endpoint(
    book_template: BookCreateFromTemplate,
    db: Session = Depends(get_db),
    current_user_username: str = Depends(get_current_user)
):
    user = crud_user.get_by_username(db, username=current_user_username)
    return book_service.create_book_from_template(db=db, book_template=book_template, user_id=user.id)

@router.post("/copy", response_model=Book, tags=["Books"])
async def copy_book_endpoint(
    book_copy: BookCopy,
    db: Session = Depends(get_db),
    current_user_username: str = Depends(get_current_user)
):
    user = crud_user.get_by_username(db, username=current_user_username)
    return book_service.copy_book(db=db, book_copy=book_copy, user_id=user.id)
