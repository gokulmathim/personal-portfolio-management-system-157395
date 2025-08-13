from __future__ import annotations
from dataclasses import dataclass
from sqlalchemy import Text
from .typing import Mapped, mapped_column
from .base import TimestampMixin
from ..extensions import db

@dataclass
class ContactMessage(db.Model, TimestampMixin):
    """Contact message submitted by users."""
    __tablename__ = "contact_messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)

    def __repr__(self) -> str:
        return f"<ContactMessage {self.email}>"
