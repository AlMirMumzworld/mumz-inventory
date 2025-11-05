"""
Business model priority configuration per country.
"""
from __future__ import annotations

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel


class BusinessModelPriority(BaseModel):
    """Business model priority configuration per country."""

    __tablename__ = 'business_model_priorities'

    country_id: Mapped[int] = mapped_column(ForeignKey('countries.id'))
    business_model_id: Mapped[int] = mapped_column(ForeignKey('business_models.id'))
    priority: Mapped[int]

    # Relationships
    country: Mapped["Country"] = relationship("Country", back_populates="business_model_priorities")
    business_model: Mapped["BusinessModel"] = relationship(
        "BusinessModel",
        back_populates="business_model_priorities")

    # Unique constraint to ensure one priority per country-business_model combination
    __table_args__ = (
        UniqueConstraint('country_id',
                         'business_model_id',
                         name='uq_business_model_priority_country_bm'),
    )

    def __repr__(self) -> str:
        return (f"<BusinessModelPriority(id={self.id}, country_id={self.country_id}, "
                f"business_model_id={self.business_model_id}, priority={self.priority})>")
