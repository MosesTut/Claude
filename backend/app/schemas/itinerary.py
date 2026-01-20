from pydantic import BaseModel, UUID4
from typing import Optional, Dict, Any, List
from datetime import datetime


class CityRecommendation(BaseModel):
    city_name: str
    country: str
    reasoning: str
    match_score: Optional[float] = None


class ItineraryRequest(BaseModel):
    city_name: str
    country: str
    trip_length_days: int


class ItineraryResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    city_name: str
    country: str
    city_reasoning: Optional[str]
    itinerary_data: Dict[str, Any]
    trip_length_days: int
    ai_model: str
    prompt_version: str
    helpful_rating: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class CityRecommendationsResponse(BaseModel):
    cities: List[CityRecommendation]
