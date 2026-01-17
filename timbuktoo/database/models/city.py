"""City model"""

from sqlalchemy import Column, String, DateTime, Boolean, DECIMAL, ARRAY, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .base import Base


class City(Base):
    __tablename__ = "cities"

    city_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    timezone = Column(String, nullable=False)
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    description = Column(Text)
    best_seasons = Column(ARRAY(String))
    currency = Column(String)
    language = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    def to_dict(self):
        return {
            "city_id": str(self.city_id),
            "name": self.name,
            "country": self.country,
            "timezone": self.timezone,
            "latitude": float(self.latitude) if self.latitude else None,
            "longitude": float(self.longitude) if self.longitude else None,
            "description": self.description,
            "best_seasons": self.best_seasons,
            "currency": self.currency,
            "language": self.language,
            "is_active": self.is_active
        }
