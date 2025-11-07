from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.moneynote.models.base import Base

class BalanceFlow(Base):
    __tablename__ = "balance_flows"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    type = Column(Integer)
    amount = Column(Float)
    convertedAmount = Column(Float)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True) # Assuming accounts table exists
    createTime = Column(Integer)
    title = Column(String)
    notes = Column(String)
    creator_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))
    to_id = Column(Integer, ForeignKey("accounts.id"), nullable=True) # Assuming accounts table exists
    payee_id = Column(Integer, ForeignKey("payees.id"), nullable=True)
    confirm = Column(Integer)
    include = Column(Integer)
    insertAt = Column(Integer)

    book = relationship("Book", back_populates="balance_flows")
    creator = relationship("User", back_populates="balance_flows")
    group = relationship("Group", back_populates="balance_flows")
    payee = relationship("Payee", back_populates="balance_flows")
    account = relationship("Account", foreign_keys=[account_id])
    to_account = relationship("Account", foreign_keys=[to_id])
