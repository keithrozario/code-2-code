from pydantic import BaseModel


class BookBase(BaseModel):
    name: str


class BookCreate(BookBase):
    group_id: int


class Book(BookBase):
    id: int
    group_id: int
    user_id: int

    class Config:
        orm_mode = True
