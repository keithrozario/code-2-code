from pydantic import BaseModel


class Currency(BaseModel):
    """Schema for currency data."""
    code: str
    name: str
    symbol: str
