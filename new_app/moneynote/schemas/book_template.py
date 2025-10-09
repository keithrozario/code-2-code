from pydantic import BaseModel
from typing import List

class BookTemplate(BaseModel):
    """Schema for book template data."""
    id: str
    name: str
    description: str
    categories: List[str]
    tags: List[str]
    payees: List[str]
