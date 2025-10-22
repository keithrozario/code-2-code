from typing import List

from fastapi import APIRouter, Depends, Request

from ..schemas.book_template import BookTemplate
from .deps import get_current_user

router = APIRouter()

@router.get("/all", response_model=List[BookTemplate], dependencies=[Depends(get_current_user)])
async def get_all_book_templates(request: Request):
    return request.app.state.book_templates