from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import UniqueConstraint, Text
from .typing import Mapped, mapped_column
from .base import TimestampMixin
from ..extensions import db

@dataclass
class AboutProfile(db.Model, TimestampMixin):
    """Single record for the About/Profile section."""
    __tablename__ = "about_profile"
    __table_args__ = (UniqueConstraint("id", name="about_singleton_uc"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[Optional[str]] = mapped_column(nullable=True)
    title: Mapped[Optional[str]] = mapped_column(nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(nullable=True)
    location: Mapped[Optional[str]] = mapped_column(nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(nullable=True)
    social_links: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    def __repr__(self) -> str:
        return f"<AboutProfile {self.name or 'about'}>"
