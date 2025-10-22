from typing import List

from fastapi import APIRouter, Depends, Request

from ..schemas.currency import Currency
from .deps import get_current_user

router = APIRouter(
    prefix="/currencies",
    tags=["currencies"],
)

@router.get("/all", response_model=List[Currency])
async def get_all_currencies(request: Request, current_user: dict = Depends(get_current_user)):
    return request.app.state.currencies