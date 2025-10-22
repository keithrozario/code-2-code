from typing import List

from fastapi import APIRouter, Depends, Request
from moneynote.routers.deps import get_current_active_user
from moneynote.schemas import BookTemplate

router = APIRouter()


@router.get(
    "/book-templates/all",
    response_model=List[BookTemplate],
    dependencies=[Depends(get_current_active_user)],
)
async def get_all_book_templates(request: Request):
    return request.app.state.book_templates
