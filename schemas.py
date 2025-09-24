from pydantic import BaseModel, ConfigDict
from typing import Optional
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
