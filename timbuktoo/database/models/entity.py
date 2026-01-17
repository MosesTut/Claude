"""Entity model"""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, DECIMAL, ARRAY, Text, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from .base import Base


class Entity(Base):
    __tablename__ = "entities"

    entity_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city_id = Column(UUID(as_uuid=True), ForeignKey("cities.city_id", ondelete="CASCADE"), nullable=False)
    entity_type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    price_tier = Column(String)
    vibes = Column(ARRAY(String))
    address = Column(Text)
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    phone = Column(String)
    website = Column(String)
    opening_hours = Column(JSONB)
    average_duration_minutes = Column(Integer)
    best_time_of_day = Column(ARRAY(String))
    seasonality = Column(ARRAY(String))
    trust_tier = Column(Integer, default=1)
    source = Column(String)
    last_verified = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    def to_dict(self):
        return {
            "entity_id": str(self.entity_id),
            "city_id": str(self.city_id),
            "entity_type": self.entity_type,
            "name": self.name,
            "description": self.description,
            "price_tier": self.price_tier,
            "vibes": self.vibes,
            "address": self.address,
            "latitude": float(self.latitude) if self.latitude else None,
            "longitude": float(self.longitude) if self.longitude else None,
            "phone": self.phone,
            "website": self.website,
            "opening_hours": self.opening_hours,
            "average_duration_minutes": self.average_duration_minutes,
            "best_time_of_day": self.best_time_of_day,
            "seasonality": self.seasonality,
            "trust_tier": self.trust_tier,
            "source": self.source,
            "last_verified": str(self.last_verified) if self.last_verified else None,
            "is_active": self.is_active
        }
