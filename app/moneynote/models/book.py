from sqlalchemy import Column, Integer, String
from app.moneynote.models.base import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
