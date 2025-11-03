from pydantic import BaseModel
from typing import Optional


class UserSessionVo(BaseModel):
    id: int
    username: str
    email: Optional[str] = None


class GroupSessionVo(BaseModel):
    id: int
    name: str


class BookSessionVo(BaseModel):
    id: int
    name: str


class InitStateResponse(BaseModel):
    user: UserSessionVo
    group: Optional[GroupSessionVo] = None
    book: Optional[BookSessionVo] = None
