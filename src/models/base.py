"""
Base model with common attributes.
"""

from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class BaseModel(Base):
    """Base abstract model with common attributes."""

    # abstract class
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
