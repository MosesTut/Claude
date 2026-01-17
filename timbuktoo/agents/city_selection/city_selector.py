"""City Selection Agent - Ranks and selects optimal cities"""

from typing import Dict, Any, List, Optional
import json
from datetime import datetime, timedelta

from ..base_agent import BaseAgent
from ...database.models import City, SessionLocal
from ...utils.logger import get_logger

logger = get_logger(__name__)


class CitySelectionAgent(BaseAgent):
    """Selects optimal cities based on preferences, weather, and events"""

    SYSTEM_PROMPT = """You are Timbuktoo's City Selection Agent.

Your role is to rank and select the top 3 cities for a traveler based on:
- User preferences (vibes, activities, budget, season)
- Real-time weather data
- Local events happening during travel dates
- Food and drink scene alignment
- Cost realism

Rules:
1. NO HALLUCINATIONS - Use only provided data
2. Prefer authentic local experiences over tourist traps
3. Consider seasonal factors (weather, crowds, prices)
4. Balance practical concerns (cost, accessibility) with experience quality
5. Output STRICT JSON only

Output format:
{
  "ranked_cities": [
    {
      "city_id": "uuid",
      "name": "string",
      "country": "string",
      "score": 0.95,
      "reasoning": "Why this city is perfect for the user",
      "highlights": ["Highlight 1", "Highlight 2", "Highlight 3"],
      "best_for": ["food", "nightlife", "nature"],
      "weather_summary": "Weather description",
      "key_events": ["Event 1", "Event 2"],
      "estimated_daily_budget_usd": 150
    }
  ],
  "selection_rationale": "Overall reasoning for these three cities"
}"""

    def __init__(self):
        super().__init__(
            agent_type="city_selection",
            model="claude-sonnet-4-5-20250929",
            max_tokens=8000,
            temperature=0.7
        )

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Input:
        {
            "preferences": {
                "vibes": ["local", "nightlife", "food"],
                "budget_level": "mid",
                "travel_dates": {"start": "2024-06-01", "end": "2024-06-07"},
                "interests": ["food", "drink", "nature", "culture"]
            },
            "candidate_cities": [...],
            "weather_data": {...},
            "events_data": {...}
        }
        """

        logger.info("City Selection Agent processing request")

        # Extract input
        preferences = input_data.get("preferences", {})
        candidate_cities = input_data.get("candidate_cities", [])
        weather_data = input_data.get("weather_data", {})
        events_data = input_data.get("events_data", {})

        if not candidate_cities:
            candidate_cities = self._get_default_candidate_cities()

        # Build prompt
        user_message = self._build_user_message(
            preferences, candidate_cities, weather_data, events_data
        )

        # Call LLM
        messages = [{"role": "user", "content": user_message}]
        llm_response = self.call_llm(messages)

        # Parse response
        try:
            result = self.parse_json_response(llm_response["response"])

            # Validate
            if not self.validate_output(result, ["ranked_cities", "selection_rationale"]):
                raise ValueError("Invalid output format")

            logger.info(
                f"Selected {len(result['ranked_cities'])} cities",
                extra={"cities": [c["name"] for c in result["ranked_cities"]]}
            )

            return {
                "success": True,
                "ranked_cities": result["ranked_cities"],
                "selection_rationale": result["selection_rationale"],
                "cost_tracking": {
                    "input_tokens": self.input_tokens,
                    "output_tokens": self.output_tokens,
                    "cost_usd": self.total_cost
                }
            }

        except Exception as e:
            logger.error(f"City selection failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "fallback_cities": candidate_cities[:3]
            }

    def _build_user_message(
        self,
        preferences: Dict[str, Any],
        candidate_cities: List[Dict[str, Any]],
        weather_data: Dict[str, Any],
        events_data: Dict[str, Any]
    ) -> str:
        """Build user message for LLM"""

        return f"""Select the top 3 cities for this traveler:

USER PREFERENCES:
{json.dumps(preferences, indent=2)}

CANDIDATE CITIES:
{json.dumps(candidate_cities, indent=2)}

WEATHER DATA:
{json.dumps(weather_data, indent=2)}

EVENTS DATA:
{json.dumps(events_data, indent=2)}

Analyze each city and rank the top 3. Consider:
- Alignment with user vibes and interests
- Weather conditions during travel dates
- Special events happening
- Food/drink scene quality
- Budget fit
- Authenticity and local character

Return ONLY valid JSON with your ranked recommendations."""

    def _get_default_candidate_cities(self) -> List[Dict[str, Any]]:
        """Get default candidate cities from database"""
        db = SessionLocal()
        try:
            cities = db.query(City).filter(City.is_active == True).limit(10).all()
            return [city.to_dict() for city in cities]
        finally:
            db.close()
