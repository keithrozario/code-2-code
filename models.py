from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # Relationship to Group
    group = relationship("Group", back_populates="owner", uselist=False)


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="group")
    accounts = relationship("Account", back_populates="group")
    books = relationship("Book", back_populates="group")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    balance = Column(Numeric(10, 2))
    currencyCode = Column(String)
    notes = Column(String, nullable=True)
    enable = Column(Boolean, default=True)
    include = Column(Boolean, default=True)
    initialBalance = Column(Numeric(10, 2))
    creditLimit = Column(Numeric(10, 2), nullable=True)
    group_id = Column(Integer, ForeignKey("groups.id"))

    group = relationship("Group", back_populates="accounts")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    notes = Column(String, nullable=True)
    defaultCurrencyCode = Column(String)
    group_id = Column(Integer, ForeignKey("groups.id"))

    group = relationship("Group", back_populates="books")
    categories = relationship("Category", back_populates="book")
    tags = relationship("Tag", back_populates="book")
    payees = relationship("Payee", back_populates="book")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    book_id = Column(Integer, ForeignKey("books.id"))
    parent_id = Column(Integer, ForeignKey("categories.id"))

    book = relationship("Book", back_populates="categories")
    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    book_id = Column(Integer, ForeignKey("books.id"))

    book = relationship("Book", back_populates="tags")

class Payee(Base):
    __tablename__ = "payees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    book_id = Column(Integer, ForeignKey("books.id"))

    book = relationship("Book", back_populates="payees")
