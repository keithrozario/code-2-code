from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.moneynote.models.base import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    notes = Column(String, nullable=True)
    enable = Column(Boolean, default=True)
    default_expense_account_id = Column(Integer, nullable=True)
    default_income_account_id = Column(Integer, nullable=True)
    default_transfer_from_account_id = Column(Integer, nullable=True)
    default_transfer_to_account_id = Column(Integer, nullable=True)
    default_expense_category_id = Column(Integer, nullable=True)
    default_income_category_id = Column(Integer, nullable=True)
    default_currency_code = Column(String, nullable=True)
    export_at = Column(Integer, nullable=True)
    sort = Column(Integer, nullable=True)

    group = relationship("Group", back_populates="books")
    owner = relationship("User", back_populates="books")
    categories = relationship("Category", back_populates="book")
    tags = relationship("Tag", back_populates="book")
    payees = relationship("Payee", back_populates="book")
    balance_flows = relationship("BalanceFlow", back_populates="book")