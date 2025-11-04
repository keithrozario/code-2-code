from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    name: str


class BookCreate(BookBase):
    group_id: int


class Book(BookBase):
    id: int
    group_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
