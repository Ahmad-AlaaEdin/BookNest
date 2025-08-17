from sqlalchemy import ForeignKey, String, Enum
from sqlalchemy.orm import Relationship, Mapped, mapped_column
from .base import Base
from typing import List, Optional


class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str]
    title: Mapped[str]
    author: Mapped[str]
    pages: Mapped[int]
    image: Mapped[str]
    status: Mapped[str] = mapped_column(Enum("to_read", "read", "reading"))
    notes: Mapped[List["Note"]] = Relationship(
        back_populates="book", cascade="all, delete-orphan"
    )
