from config import Settings
from fastapi import APIRouter, Depends
from moneynote.routers.deps import get_current_active_user, get_settings
from moneynote.schemas.system import BaseUrlResponse, VersionResponse

router = APIRouter()


@router.get("/version", response_model=VersionResponse)
async def version(
    settings: Settings = Depends(get_settings),
    current_user: dict = Depends(get_current_active_user),
):
    return VersionResponse(version=settings.APP_VERSION)


@router.get("/test3", response_model=BaseUrlResponse)
async def test3(
    settings: Settings = Depends(get_settings),
    current_user: dict = Depends(get_current_active_user),
):
    return BaseUrlResponse(base_url=settings.BASE_URL)
