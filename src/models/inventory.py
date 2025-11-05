"""
Inventory records with stock levels per SKU, country, vendor, and business model.
"""
from __future__ import annotations
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel


class Inventory(BaseModel):
    """Inventory records with stock levels per SKU, country, vendor, and business model."""
    __tablename__ = 'inventory'

    sku: Mapped[str] = mapped_column(String(255))
    country_id: Mapped[int] = mapped_column(ForeignKey('countries.id'))
    vendor_id: Mapped[int] = mapped_column(ForeignKey('vendors.id'))
    business_model_id: Mapped[int] = mapped_column(ForeignKey('business_models.id'))
    stock: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 default=func.now(),
                                                 server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 default=func.now(),
                                                 server_default=func.now(),
                                                 onupdate=func.now(),
                                                 server_onupdate=func.now())

    # Relationships
    country: Mapped["Country"] = relationship("Country", back_populates="inventory")
    vendor: Mapped["Vendor"] = relationship("Vendor", back_populates="inventory")
    business_model: Mapped["BusinessModel"] = relationship("BusinessModel",
                                                           back_populates="inventory")

    # Unique constraint to ensure one inventory record per SKU-country-vendor-business_model combination
    __table_args__ = (
        UniqueConstraint(
            'sku', 'country_id', 'vendor_id', 'business_model_id',
            name='uq_inventory_sku_country_vendor_bm'
        ),
    )

    def __repr__(self) -> str:
        return (f"<Inventory(id={self.id}, sku='{self.sku}', country_id={self.country_id}, "
                f"vendor_id={self.vendor_id}, business_model_id={self.business_model_id}, "
                f"stock={self.stock})>")
