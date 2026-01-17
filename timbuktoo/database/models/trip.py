"""Trip and Feedback models"""

from sqlalchemy import Column, String, DateTime, Integer, DECIMAL, ARRAY, Text, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid

from .base import Base


class Trip(Base):
    __tablename__ = "trips"

    trip_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True))
    city_id = Column(UUID(as_uuid=True), ForeignKey("cities.city_id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    preferences = Column(JSONB)
    itinerary = Column(JSONB)
    estimated_cost_usd = Column(DECIMAL(10, 2))
    weather_data = Column(JSONB)
    events_data = Column(JSONB)
    variant_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "trip_id": str(self.trip_id),
            "user_id": str(self.user_id) if self.user_id else None,
            "city_id": str(self.city_id),
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
            "preferences": self.preferences,
            "itinerary": self.itinerary,
            "estimated_cost_usd": float(self.estimated_cost_usd) if self.estimated_cost_usd else None,
            "weather_data": self.weather_data,
            "events_data": self.events_data,
            "variant_id": self.variant_id
        }


class Feedback(Base):
    __tablename__ = "feedback"

    feedback_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id = Column(UUID(as_uuid=True), ForeignKey("trips.trip_id", ondelete="CASCADE"), nullable=False)
    overall_rating = Column(Integer)
    daily_ratings = Column(JSONB)
    comments = Column(Text)
    pacing_rating = Column(Integer)
    authenticity_rating = Column(Integer)
    value_rating = Column(Integer)
    liked_entities = Column(ARRAY(UUID(as_uuid=True)))
    disliked_entities = Column(ARRAY(UUID(as_uuid=True)))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "feedback_id": str(self.feedback_id),
            "trip_id": str(self.trip_id),
            "overall_rating": self.overall_rating,
            "daily_ratings": self.daily_ratings,
            "comments": self.comments,
            "pacing_rating": self.pacing_rating,
            "authenticity_rating": self.authenticity_rating,
            "value_rating": self.value_rating,
            "liked_entities": [str(e) for e in self.liked_entities] if self.liked_entities else [],
            "disliked_entities": [str(e) for e in self.disliked_entities] if self.disliked_entities else []
        }


class CostTracking(Base):
    __tablename__ = "cost_tracking"

    cost_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id = Column(UUID(as_uuid=True), ForeignKey("trips.trip_id", ondelete="CASCADE"))
    agent_type = Column(String, nullable=False)
    model_used = Column(String, nullable=False)
    input_tokens = Column(Integer, nullable=False)
    output_tokens = Column(Integer, nullable=False)
    cost_usd = Column(DECIMAL(10, 6), nullable=False)
    cached = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "cost_id": str(self.cost_id),
            "trip_id": str(self.trip_id) if self.trip_id else None,
            "agent_type": self.agent_type,
            "model_used": self.model_used,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cost_usd": float(self.cost_usd),
            "cached": self.cached,
            "timestamp": self.timestamp.isoformat()
        }
