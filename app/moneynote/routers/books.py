from typing import List, Optional
from fastapi import APIRouter, Depends, Response, status, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.moneynote.routers.deps import get_current_user, get_current_active_group_id
from app.moneynote.schemas.book import Book, BookCreate, BookCreateFromTemplate, BookCopy, BookDetails, BookUpdateForm
from app.moneynote.services import book_service
from app.moneynote.models import User
from app.moneynote.crud import crud_user

router = APIRouter()

@router.post(
    "/",
    response_model=Book,
    tags=["Books"],
    summary="Create Book",
    description="Create a new, empty book within a specified group."
)
async def create_book_endpoint(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user_username: str = Depends(get_current_user)
):
    user = crud_user.get_by_username(db, username=current_user_username)
    return book_service.create_book(db=db, book=book, user_id=user.id)

@router.post(
    "/template",
    response_model=Book,
    tags=["Books"],
    summary="Create Book from Template",
    description="Create a new book from a system-defined template."
)
async def create_book_from_template_endpoint(
    book_template: BookCreateFromTemplate,
    db: Session = Depends(get_db),
    current_user_username: str = Depends(get_current_user)
):
    user = crud_user.get_by_username(db, username=current_user_username)
    return book_service.create_book_from_template(db=db, book_template=book_template, user_id=user.id)

@router.post(
    "/copy",
    response_model=Book,
    tags=["Books"],
    summary="Copy Book",
    description="Create a new book by copying the structure of an existing book."
)
async def copy_book_endpoint(
    book_copy: BookCopy,
    db: Session = Depends(get_db),
    current_user_username: str = Depends(get_current_user)
):
    user = crud_user.get_by_username(db, username=current_user_username)
    return book_service.copy_book(db=db, book_copy=book_copy, user_id=user.id)

@router.get(
    "/",
    response_model=List[BookDetails],
    tags=["Books"],
    summary="Read Books",
    description="Retrieve a paginated list of books within the user's active group, with optional filtering."
)
async def read_books_endpoint(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    enable: Optional[bool] = None,
    name: Optional[str] = None,
    sort: Optional[str] = None,
    active_group_id: int = Depends(get_current_active_group_id)
):
    return book_service.query_books(
        db=db, group_id=active_group_id, enable=enable, name=name, sort=sort, skip=skip, limit=limit
    )

@router.get(
    "/{book_id}",
    response_model=BookDetails,
    tags=["Books"],
    summary="Read Book Details",
    description="Retrieve the complete details for a single, specific book."
)
async def read_book_details_endpoint(
    book_id: int,
    db: Session = Depends(get_db),
    active_group_id: int = Depends(get_current_active_group_id)
):
    return book_service.get_book_details(db=db, book_id=book_id, active_group_id=active_group_id)

@router.patch(
    "/{book_id}/toggle",
    response_model=Book,
    tags=["Books"],
    summary="Toggle Book Enable Status",
    description="Toggle the 'enable' status of a specific book."
)
async def toggle_book_endpoint(
    book_id: int,
    db: Session = Depends(get_db),
    current_user_username: str = Depends(get_current_user)
):
    user = crud_user.get_by_username(db, username=current_user_username)
    return book_service.toggle_book(db=db, book_id=book_id, user_id=user.id)

@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Books"],
    summary="Delete Book",
    description="Delete a book owned by the current user. Fails if the book contains transactions."
)
async def delete_book_endpoint(
    book_id: int,
    db: Session = Depends(get_db),
    current_user_username: str = Depends(get_current_user)
):
    user = crud_user.get_by_username(db, username=current_user_username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    book_service.delete_book(db=db, book_id=book_id, user_id=user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put(
    "/{book_id}",
    response_model=BookDetails,
    tags=["Books"],
    summary="Update Book",
    description="Update the details of an existing book owned by the current user."
)
async def update_book_endpoint(
    book_id: int,
    book_in: BookUpdateForm,
    db: Session = Depends(get_db),
    current_user_username: str = Depends(get_current_user)
):
    user = crud_user.get_by_username(db, username=current_user_username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return book_service.update_book(db=db, book_id=book_id, book_in=book_in, user_id=user.id)

@router.get(
    "/{book_id}/export",
    tags=["Books"],
    summary="Export Book Data to Excel",
    description="Export all transaction data for a specific book to an Excel file.",
    response_class=StreamingResponse,
    responses={200: {"content": {"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {}}}},
)
async def export_book_endpoint(
    book_id: int,
    timeZoneOffset: int = Query(0, description="Time zone offset in minutes from UTC"),
    db: Session = Depends(get_db),
    current_user_username: str = Depends(get_current_user)
):
    user = crud_user.get_by_username(db, username=current_user_username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # This will also handle authorization check for the book
    book_service.get_book_details(db=db, book_id=book_id, active_group_id=user.default_group_id) # Assuming default_group_id is the active group

    excel_file = book_service.export_book_data(db=db, book_id=book_id, timeZoneOffset=timeZoneOffset)

    filename = f"book_{book_id}_export.xlsx"
    headers = {
        "Content-Disposition": f"attachment; filename=\"{filename}\"",
        "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }
    return StreamingResponse(excel_file, headers=headers)
