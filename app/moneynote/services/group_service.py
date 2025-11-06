from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import select

from app.moneynote.models import Group, Book
from app.moneynote.schemas.group import GroupCreate, GroupUpdate
from app.moneynote.schemas.book import BookCreateFromTemplate
from app.moneynote.crud import crud_group
from app.moneynote.services import book_service

def create_group(db: Session, group: GroupCreate, user_id: int) -> Group:
    db_group = crud_group.get_by_name(db, name=group.name)
    if db_group and db_group.user_id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group with this name already exists for this user.",
        )
    
    # Create the group
    new_group = crud_group.create(db=db, group=group, user_id=user_id)

    # Create a default book from the 'personal_finance' template
    default_book_template = BookCreateFromTemplate(
        name="Default Book",
        group_id=new_group.id,
        template_id="personal_finance"
    )
    book_service.create_book_from_template(db=db, book_template=default_book_template, user_id=user_id)

    return new_group

def update_group(db: Session, group_id: int, group_in: GroupUpdate, user_id: int) -> Group:
    group = crud_group.get(db, id=group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    if group.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this group")

    if group_in.name != group.name:
        existing_group = crud_group.get_by_name(db, name=group_in.name)
        if existing_group and existing_group.user_id == user_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Group with this name already exists for this user.")

    group.name = group_in.name
    group.notes = group_in.notes
    group.default_currency_code = group_in.default_currency_code
    group.default_book_id = group_in.default_book_id

    db.add(group)
    db.commit()
    db.refresh(group)
    return group

def delete_group(db: Session, group_id: int, user_id: int):
    group = crud_group.get(db, id=group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    if group.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this group")

    book_count = db.execute(select(Book).filter(Book.group_id == group_id)).count()
    if book_count > 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Group cannot be deleted as it still contains books.")

    db.delete(group)
    db.commit()
