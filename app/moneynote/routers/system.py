from fastapi import APIRouter, Depends
from app.config import Settings
from app.moneynote.routers.deps import get_current_user
from app.moneynote.models.user import User

router = APIRouter()

def get_settings() -> Settings:
    return Settings()

@router.get("/version")
async def get_version(settings: Settings = Depends(get_settings), current_user: User = Depends(get_current_user)):
    return {"version": settings.APP_VERSION}

@router.get("/test3")
async def get_test3(settings: Settings = Depends(get_settings), current_user: User = Depends(get_current_user)):
    return {"base_url": settings.BASE_URL}
