from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import  Mapped, mapped_column,relationship
from .base import Base
from datetime import datetime
from sqlalchemy import DateTime

class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    content: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    book: Mapped["Book"] = relationship(back_populates="notes")
