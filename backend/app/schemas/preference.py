from pydantic import BaseModel, UUID4
from typing import Optional, List
from datetime import datetime


class PreferenceCreate(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    trip_length_days: Optional[int] = None
    interests: Optional[List[str]] = None
    food_preferences: Optional[List[str]] = None
    budget_level: Optional[str] = None  # "budget", "mid-range", "luxury"
    pace: Optional[str] = None  # "relaxed", "moderate", "packed"


class PreferenceResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    start_date: Optional[str]
    end_date: Optional[str]
    trip_length_days: Optional[int]
    interests: Optional[List[str]]
    food_preferences: Optional[List[str]]
    budget_level: Optional[str]
    pace: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
