from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
import uuid


class Preference(Base):
    __tablename__ = "preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Trip Details
    start_date = Column(String, nullable=True)  # ISO 8601 date string
    end_date = Column(String, nullable=True)    # ISO 8601 date string
    trip_length_days = Column(Integer, nullable=True)

    # Interests (stored as array of strings)
    interests = Column(ARRAY(String), nullable=True)

    # Food Preferences
    food_preferences = Column(ARRAY(String), nullable=True)

    # Budget
    budget_level = Column(String, nullable=True)  # "budget", "mid-range", "luxury"

    # Pace
    pace = Column(String, nullable=True)  # "relaxed", "moderate", "packed"

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)
