from pydantic import BaseModel, ConfigDict
from typing import Optional

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
