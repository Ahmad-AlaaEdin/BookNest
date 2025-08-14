from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Relationship, Mapped, mapped_column
from .base import Base
from datetime import datetime


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    content: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
    book: Mapped["Book"] = Relationship(back_populates="notes")
