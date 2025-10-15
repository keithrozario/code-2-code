from pydantic import BaseModel


class Currency(BaseModel):
    """Schema for currency data."""
    id: str
    name: str
    description: str
    rate: float