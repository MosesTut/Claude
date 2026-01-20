from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
import uuid


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    itinerary_id = Column(UUID(as_uuid=True), ForeignKey("itineraries.id", ondelete="CASCADE"), nullable=False, index=True)

    # Feedback Type (matches FeedbackScreen report types)
    feedback_type = Column(String, nullable=False)  # "inaccurate", "inappropriate", "missing_information", "other"

    # Optional User Comments
    comments = Column(Text, nullable=True)

    # Review Status
    reviewed = Column(String, default="pending", nullable=False)  # "pending", "reviewed", "actioned"
    reviewed_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
