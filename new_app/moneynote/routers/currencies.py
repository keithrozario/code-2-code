from typing import List

from fastapi import APIRouter, Depends, Request
from moneynote.routers.deps import get_current_active_user
from moneynote.schemas import Currency

router = APIRouter()


@router.get(
    "/currencies/all",
    response_model=List[Currency],
    dependencies=[Depends(get_current_active_user)],
)
async def get_all_currencies(request: Request):
    return request.app.state.currencies
