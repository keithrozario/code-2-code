from pydantic import BaseModel, ConfigDict
from typing import Optional


class BookBase(BaseModel):
    name: str


class BookCreate(BookBase):
    group_id: int


class Book(BookBase):
    id: int
    group_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class BookCreateFromTemplate(BookCreate):
    template_id: str


class BookCopy(BaseModel):
    from_book_id: int
    new_book_name: str
    group_id: int


class BookDetails(Book):
    notes: Optional[str] = None
    enable: Optional[bool] = None
    default_expense_account_id: Optional[int] = None
    default_income_account_id: Optional[int] = None
    default_transfer_from_account_id: Optional[int] = None
    default_transfer_to_account_id: Optional[int] = None
    default_expense_category_id: Optional[int] = None
    default_income_category_id: Optional[int] = None
    default_currency_code: Optional[str] = None
    export_at: Optional[int] = None
    sort: Optional[int] = None
