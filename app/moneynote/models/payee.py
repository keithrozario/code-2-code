from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.moneynote.models.base import Base

class Payee(Base):
    __tablename__ = "payees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    notes = Column(String)
    enable = Column(Boolean, default=True)
    canExpense = Column(Boolean, default=True)
    canIncome = Column(Boolean, default=True)
    sort = Column(Integer)

    book = relationship("Book", back_populates="payees")
