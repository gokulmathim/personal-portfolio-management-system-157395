from __future__ import annotations
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash
from .typing import Mapped, mapped_column
from .base import TimestampMixin
from ..extensions import db

@dataclass
class AdminUser(db.Model, TimestampMixin):
    """Admin user for dashboard authentication."""
    __tablename__ = "admin_users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    # PUBLIC_INTERFACE
    def set_password(self, password: str) -> None:
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)

    # PUBLIC_INTERFACE
    def check_password(self, password: str) -> bool:
        """Verify a plaintext password against stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<AdminUser {self.username}>"
