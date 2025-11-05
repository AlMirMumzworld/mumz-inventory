"""
Country model for storing country information.
"""
from __future__ import annotations
from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel


class Country(BaseModel):
    """Country entity model for storing country information."""
    __tablename__ = 'countries'

    code: Mapped[str] = mapped_column(String(3), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))

    # Relationships
    business_model_priorities: Mapped[List["BusinessModelPriority"]] = relationship(
        "BusinessModelPriority",
        back_populates="country")
    vendor_priorities: Mapped[List["VendorPriority"]] = relationship("VendorPriority",
                                                                     back_populates="country")
    inventory: Mapped[List["Inventory"]] = relationship("Inventory",
                                                        back_populates="country")

    def __repr__(self) -> str:
        return f"<Country(id={self.id}, code='{self.code}', name='{self.name}')>"
