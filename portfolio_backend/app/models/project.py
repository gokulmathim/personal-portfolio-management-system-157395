from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from sqlalchemy import Boolean, Text, JSON
from .typing import Mapped, mapped_column
from .base import TimestampMixin
from ..extensions import db

@dataclass
class Project(db.Model, TimestampMixin):
    """Portfolio project entity."""
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    url: Mapped[Optional[str]] = mapped_column(nullable=True)
    # Store tags as JSON array (list of strings). Compatible with SQLite and PostgreSQL.
    tags: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, default=list)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"<Project {self.title}>"
