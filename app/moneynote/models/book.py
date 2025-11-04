from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.moneynote.models.base import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    group = relationship("Group", back_populates="books")
    owner = relationship("User", back_populates="books")
    categories = relationship("Category", back_populates="book")
    tags = relationship("Tag", back_populates="book")
    payees = relationship("Payee", back_populates="book")
