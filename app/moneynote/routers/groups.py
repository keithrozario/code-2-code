from typing import List
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.moneynote.routers.deps import get_current_user
from app.moneynote.schemas.group import Group, GroupCreate, GroupUpdate
from app.moneynote.services import group_service
from app.moneynote.models import User
from app.moneynote.crud import crud_user, crud_group

router = APIRouter()

@router.post(
    "/",
    response_model=Group,
    tags=["Groups"],
    summary="Create Group",
    description="Create a new group for the current user, including a default book."
)
async def create_group_endpoint(
    group: GroupCreate,
    db: Session = Depends(get_db),
    current_user_username: str = Depends(get_current_user)
):
    user = crud_user.get_by_username(db, username=current_user_username)
    return group_service.create_group(db=db, group=group, user_id=user.id)

@router.get(
    "/",
    response_model=List[Group],
    tags=["Groups"],
    summary="Read Groups",
    description="Retrieve a paginated list of groups owned by the current user."
)
async def read_groups_endpoint(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user_username: str = Depends(get_current_user)
):
    user = crud_user.get_by_username(db, username=current_user_username)
    return crud_group.get_multi_by_owner(db, user_id=user.id, skip=skip, limit=limit)

@router.put(
    "/{group_id}",
    response_model=Group,
    tags=["Groups"],
    summary="Update Group",
    description="Update the details of a specific group owned by the current user."
)
async def update_group_endpoint(
    group_id: int,
    group_in: GroupUpdate,
    db: Session = Depends(get_db),
    current_user_username: str = Depends(get_current_user)
):
    user = crud_user.get_by_username(db, username=current_user_username)
    return group_service.update_group(db=db, group_id=group_id, group_in=group_in, user_id=user.id)

@router.delete(
    "/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Groups"],
    summary="Delete Group",
    description="Delete a group owned by the current user. Fails if the group contains books."
)
async def delete_group_endpoint(
    group_id: int,
    db: Session = Depends(get_db),
    current_user_username: str = Depends(get_current_user)
):
    user = crud_user.get_by_username(db, username=current_user_username)
    group_service.delete_group(db=db, group_id=group_id, user_id=user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
