from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.moneynote.models import Group
from app.moneynote.schemas.group import GroupCreate
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
