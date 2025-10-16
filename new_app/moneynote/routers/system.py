from fastapi import APIRouter, Depends

from config import settings

from .deps import get_current_user

router = APIRouter()

@router.get("/version")
def get_version(current_user: str = Depends(get_current_user)):
    return {"version": settings.APP_VERSION}

@router.get("/test3")
def get_test3(current_user: str = Depends(get_current_user)):
    return {"base_url": settings.BASE_URL}
