"""
Vendor priority configuration per country and business model.
"""
from __future__ import annotations

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel


class VendorPriority(BaseModel):
    """Vendor priority configuration per country and business model."""
    __tablename__ = 'vendor_priorities'

    country_id: Mapped[int] = mapped_column(ForeignKey('countries.id'))
    business_model_id: Mapped[int] = mapped_column(ForeignKey('business_models.id'))
    vendor_id: Mapped[int] = mapped_column(ForeignKey('vendors.id'))
    priority: Mapped[int] = mapped_column(default=1)

    # Relationships
    country: Mapped["Country"] = relationship("Country", back_populates="vendor_priorities")
    business_model: Mapped["BusinessModel"] = relationship("BusinessModel",
                                                           back_populates="vendor_priorities"
    )
    vendor: Mapped["Vendor"] = relationship("Vendor", back_populates="vendor_priorities")

    # Unique constraint to ensure one priority per country-business_model-vendor combination
    __table_args__ = (
        UniqueConstraint(
            'country_id', 'business_model_id', 'vendor_id',
            name='uq_vendor_priority_country_bm_vendor'
        ),
    )

    def __repr__(self) -> str:
        return (f"<VendorPriority(id={self.id}, country_id={self.country_id}, "
                f"business_model_id={self.business_model_id}, vendor_id={self.vendor_id}, "
                f"priority={self.priority})>")
