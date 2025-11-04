from pydantic import BaseModel, ConfigDict


class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
