from typing import List

from fastapi import APIRouter, Depends

from ..schemas.currency import Currency
from ..services.data_loader import CURRENCIES
from .deps import get_current_user

router = APIRouter(
    prefix="/currencies",
    tags=["currencies"],
)

@router.get("/all", response_model=List[Currency])
async def get_all_currencies(current_user: dict = Depends(get_current_user)):
    return CURRENCIES