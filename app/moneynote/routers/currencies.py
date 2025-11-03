from typing import List
from fastapi import APIRouter, Depends

from app.moneynote.schemas.currency import Currency
from app.moneynote.services.data_cache_service import DataCacheService, get_data_cache_service
from app.moneynote.routers.deps import get_current_user
from app.moneynote.models.user import User

router = APIRouter()

@router.get("/all", response_model=List[Currency], tags=["currencies"])
def get_all_currencies(service: DataCacheService = Depends(get_data_cache_service), current_user: User = Depends(get_current_user)):
    return service.get_currencies()
