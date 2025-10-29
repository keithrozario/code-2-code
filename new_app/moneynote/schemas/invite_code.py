from pydantic import BaseModel

class InviteCodeBase(BaseModel):
    code: str
    is_used: bool = False
    user_id: int | None = None

class InviteCodeCreate(InviteCodeBase):
    code: str

class InviteCodeUpdate(InviteCodeBase):
    pass
