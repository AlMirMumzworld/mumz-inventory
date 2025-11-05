"""
Business model for storing fulfillment types.
"""
from __future__ import annotations
from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel


class BusinessModel(BaseModel):
    """Business model entity for storing fulfillment types."""

    __tablename__ = 'business_models'

    code: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))

    # Relationships
    business_model_priorities: Mapped[List["BusinessModelPriority"]] = relationship(
        "BusinessModelPriority",
        back_populates="business_model")
    vendor_priorities: Mapped[List["VendorPriority"]] = relationship(
        "VendorPriority",
        back_populates="business_model")
    inventory: Mapped[List["Inventory"]] = relationship("Inventory",
                                                        back_populates="business_model")

    def __repr__(self) -> str:
        return f"<BusinessModel(id={self.id}, code='{self.code}', name='{self.name}')>"
