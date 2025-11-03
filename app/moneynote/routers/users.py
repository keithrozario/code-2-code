from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.moneynote.routers.deps import get_current_user
from app.moneynote.schemas.user import InitStateResponse
from app.moneynote.services import user_service

router = APIRouter()

@router.get("/initState", response_model=InitStateResponse, tags=["Users"])
async def get_init_state_endpoint(
    current_user_username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return user_service.get_init_state(db, current_user_username)
