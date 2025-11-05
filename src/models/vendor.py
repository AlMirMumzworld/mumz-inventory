"""
Vendor model for storing vendor information.
"""
from __future__ import annotations
from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel


class Vendor(BaseModel):
    """Vendor entity model for storing vendor information."""
    __tablename__ = 'vendors'

    code: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True, server_default='true')

    # Relationships
    vendor_priorities: Mapped[List["VendorPriority"]] = relationship("VendorPriority",
                                                                     back_populates="vendor")
    inventory: Mapped[List["Inventory"]] = relationship("Inventory",
                                                        back_populates="vendor")

    def __repr__(self) -> str:
        return (f"<Vendor(id={self.id}, code='{self.code}', "
                f"name='{self.name}', is_active={self.is_active})>")
