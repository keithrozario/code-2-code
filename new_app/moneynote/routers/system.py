from fastapi import APIRouter, Depends

from config import settings
from moneynote.schemas.system import BaseUrlResponse, VersionResponse

from .deps import get_current_user

router = APIRouter()

@router.get("/version", response_model=VersionResponse)
def get_version(current_user: str = Depends(get_current_user)):
    return {"version": settings.APP_VERSION}

@router.get("/test3", response_model=BaseUrlResponse)
def get_test3(current_user: str = Depends(get_current_user)):
    return {"base_url": settings.BASE_URL}
