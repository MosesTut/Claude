from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime


class FeedbackCreate(BaseModel):
    itinerary_id: UUID4
    feedback_type: str  # "inaccurate", "inappropriate", "missing_information", "other"
    comments: Optional[str] = None


class FeedbackResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    itinerary_id: UUID4
    feedback_type: str
    comments: Optional[str]
    reviewed: str
    created_at: datetime

    class Config:
        from_attributes = True
