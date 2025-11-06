from pydantic import BaseModel, ConfigDict
from typing import Optional


class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    notes: Optional[str] = None
    default_currency_code: Optional[str] = None
    default_book_id: Optional[int] = None


class Group(GroupBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
