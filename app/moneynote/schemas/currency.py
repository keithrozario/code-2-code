from pydantic import BaseModel

class Currency(BaseModel):
    code: str
    name: str
    symbol: str
