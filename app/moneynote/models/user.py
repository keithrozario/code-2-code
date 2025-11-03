from sqlalchemy import Column, Integer, String
from app.moneynote.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    default_group_id = Column(Integer, nullable=True)
    default_book_id = Column(Integer, nullable=True)
