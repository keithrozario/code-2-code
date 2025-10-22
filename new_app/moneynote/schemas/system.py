from pydantic import BaseModel


class VersionResponse(BaseModel):
    version: str

class BaseUrlResponse(BaseModel):
    base_url: str
