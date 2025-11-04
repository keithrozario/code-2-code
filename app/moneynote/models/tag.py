from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.moneynote.models.base import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    notes = Column(String)
    enable = Column(Boolean, default=True)
    canExpense = Column(Boolean, default=True)
    canIncome = Column(Boolean, default=True)
    canTransfer = Column(Boolean, default=True)
    sort = Column(Integer)
    parent_id = Column(Integer, ForeignKey("tags.id"))

    book = relationship("Book", back_populates="tags")
    parent = relationship("Tag", remote_side=[id])