from typing import List
from fastapi import APIRouter, Depends

from app.moneynote.schemas.book_template import BookTemplate
from app.moneynote.services.data_cache_service import DataCacheService, get_data_cache_service
from app.moneynote.routers.deps import get_current_user
from app.moneynote.models.user import User

router = APIRouter()

@router.get("/all", response_model=List[BookTemplate], tags=["Book Templates"])
async def get_all_book_templates(service: DataCacheService = Depends(get_data_cache_service), current_user: User = Depends(get_current_user)):
    return service.get_book_templates()