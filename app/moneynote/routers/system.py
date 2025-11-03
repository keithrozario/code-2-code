from fastapi import APIRouter, Depends
from app.config import Settings

router = APIRouter()

def get_settings() -> Settings:
    return Settings()

@router.get("/version")
async def get_version(settings: Settings = Depends(get_settings)):
    return {"version": settings.APP_VERSION}

@router.get("/test3")
async def get_test3(settings: Settings = Depends(get_settings)):
    return {"base_url": settings.BASE_URL}
