from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.moneynote.models.base import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    notes = Column(String)
    enable = Column(Boolean, default=True)
    type = Column(Integer)
    sort = Column(Integer)
    parent_id = Column(Integer, ForeignKey("categories.id"))

    book = relationship("Book", back_populates="categories")
    parent = relationship("Category", remote_side=[id])
