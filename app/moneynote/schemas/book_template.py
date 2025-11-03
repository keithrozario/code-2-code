from typing import List
from pydantic import BaseModel

class AccountTemplate(BaseModel):
    name: str
    type: str
    description: str

class BookTemplate(BaseModel):
    id: str
    name: str
    description: str
    accounts: List[AccountTemplate]
