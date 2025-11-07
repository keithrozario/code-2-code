from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.moneynote.models.base import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    type = Column(Integer)
    notes = Column(String)
    enable = Column(Boolean, default=True)
    no = Column(String)
    balance = Column(Float)
    include = Column(Integer)
    canExpense = Column(Boolean)
    canIncome = Column(Boolean)
    canTransferFrom = Column(Boolean)
    canTransferTo = Column(Boolean)
    currencyCode = Column(String)
    initialBalance = Column(Float)
    creditLimit = Column(Float)
    billDay = Column(Integer)
    apr = Column(Float)
    sort = Column(Integer)

    group = relationship("Group", back_populates="accounts")
