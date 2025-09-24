from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from enum import Enum


# Pydantic models for Token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Pydantic models for User
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# Pydantic models for Account
class AccountType(str, Enum):
    CHECKING = "CHECKING"
    CREDIT = "CREDIT"
    ASSET = "ASSET"
    DEBT = "DEBT"


class AccountBase(BaseModel):
    name: str
    type: AccountType
    currencyCode: str
    initialBalance: float


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[AccountType] = None
    currencyCode: Optional[str] = None
    initialBalance: Optional[float] = None


class Account(AccountBase):
    id: int
    balance: float

    model_config = ConfigDict(from_attributes=True)

# Pydantic models for Book
class BookBase(BaseModel):
    name: str
    defaultCurrencyCode: str
    notes: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    name: Optional[str] = None
    defaultCurrencyCode: Optional[str] = None
    notes: Optional[str] = None

class Book(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# Pydantic models for Category
class CategoryType(str, Enum):
    EXPENSE = "EXPENSE"
    INCOME = "INCOME"

class CategoryBase(BaseModel):
    name: str
    type: CategoryType

class CategoryCreate(CategoryBase):
    parent_id: Optional[int] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[CategoryType] = None
    parent_id: Optional[int] = None

class Category(CategoryBase):
    id: int
    book_id: int
    parent_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

# Pydantic models for Tag
class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    name: Optional[str] = None

class Tag(TagBase):
    id: int
    book_id: int

    model_config = ConfigDict(from_attributes=True)

# Pydantic models for Payee
class PayeeBase(BaseModel):
    name: str

class PayeeCreate(PayeeBase):
    pass

class PayeeUpdate(BaseModel):
    name: Optional[str] = None

class Payee(PayeeBase):
    id: int
    book_id: int

    model_config = ConfigDict(from_attributes=True)
