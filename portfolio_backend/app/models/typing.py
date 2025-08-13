from typing import TypeVar
from sqlalchemy.orm import Mapped, mapped_column

__all__ = ["Mapped", "mapped_column", "PK"]

PK = TypeVar("PK")
