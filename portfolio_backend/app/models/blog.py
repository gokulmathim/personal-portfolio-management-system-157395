from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from sqlalchemy import Boolean, Text, JSON
from .typing import Mapped, mapped_column
from .base import TimestampMixin
from ..extensions import db

@dataclass
class BlogPost(db.Model, TimestampMixin):
    """Blog post entry."""
    __tablename__ = "blog_posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    slug: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    meta: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    def __repr__(self) -> str:
        return f"<BlogPost {self.slug}>"
