from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
import uuid


class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # City Information
    city_name = Column(String, nullable=False)
    country = Column(String, nullable=False)

    # AI-Generated Content
    city_reasoning = Column(Text, nullable=True)  # Why this city was recommended
    itinerary_data = Column(JSON, nullable=False)  # Full day-by-day itinerary

    # Trip Details
    trip_length_days = Column(Integer, nullable=False)

    # AI Model Information
    ai_model = Column(String, default="claude-3-5-sonnet-20241022", nullable=False)
    prompt_version = Column(String, default="v1.0", nullable=False)

    # User Feedback
    helpful_rating = Column(String, nullable=True)  # "helpful", "not_helpful", null

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)
