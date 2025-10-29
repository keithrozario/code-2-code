from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .base import Base

class InviteCode(Base):
    __tablename__ = "invite_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    is_used = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
