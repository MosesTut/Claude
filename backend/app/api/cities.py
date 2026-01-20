from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.preference import Preference
from app.schemas.itinerary import CityRecommendationsResponse, CityRecommendation
from app.utils.auth import get_current_user
from app.utils.anthropic_client import recommend_cities

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.get("/recommendations", response_model=CityRecommendationsResponse)
async def get_city_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get AI-powered city recommendations based on user preferences

    This endpoint uses the City Selection Agent (Claude 3.5 Sonnet) to recommend
    3 cities that match the user's saved preferences.

    CRITICAL: This is an AI-generated recommendation. The response includes reasoning
    to explain why each city was selected.
    """

    # Get user's preferences
    preference = db.query(Preference).filter(
        Preference.user_id == current_user.id
    ).first()

    if not preference:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please set your travel preferences first"
        )

    # Validate required fields
    if not preference.interests or not preference.trip_length_days:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Preferences must include interests and trip length"
        )

    # Call AI City Selection Agent
    try:
        cities_data = await recommend_cities(
            interests=preference.interests or [],
            food_preferences=preference.food_preferences or [],
            budget_level=preference.budget_level or "mid-range",
            pace=preference.pace or "moderate",
            trip_length_days=preference.trip_length_days
        )

        # Convert to response model
        city_recommendations = [
            CityRecommendation(**city) for city in cities_data
        ]

        return CityRecommendationsResponse(cities=city_recommendations)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate city recommendations: {str(e)}"
        )
