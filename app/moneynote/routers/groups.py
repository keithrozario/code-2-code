from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.moneynote.routers.deps import get_current_user
from app.moneynote.schemas.group import Group, GroupCreate
from app.moneynote.services import group_service
from app.moneynote.models import User
from app.moneynote.crud import crud_user

router = APIRouter()

@router.post("/", response_model=Group, tags=["Groups"])
async def create_group_endpoint(
    group: GroupCreate,
    db: Session = Depends(get_db),
    current_user_username: str = Depends(get_current_user)
):
    user = crud_user.get_by_username(db, username=current_user_username)
    return group_service.create_group(db=db, group=group, user_id=user.id)
