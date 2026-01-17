"""Travel Concierge Agent - Creates detailed 7-day itineraries"""

from typing import Dict, Any, List, Optional
import json
from datetime import datetime, timedelta

from ..base_agent import BaseAgent
from ...utils.logger import get_logger

logger = get_logger(__name__)


class TravelConciergeAgent(BaseAgent):
    """Creates comprehensive 7-day travel itineraries"""

    SYSTEM_PROMPT = """You are Timbuktoo's Travel Concierge Agent.

Your role is to create detailed, day-by-day itineraries that combine:
- Local expert knowledge
- Real-time weather and events
- Practical logistics (transit, timing, reservations)
- Budget tracking
- Pacing and flow

Rules:
1. NO HALLUCINATIONS - Use only provided data
2. Create REALISTIC schedules (no rushing, include travel time)
3. Balance structured plans with flexibility
4. Prioritize authentic local experiences
5. Include specific meal recommendations
6. Account for weather and seasonal factors
7. Provide budget breakdowns
8. Include packing recommendations
9. Output STRICT JSON only

Pacing philosophy (A/B test variant aware):
- CONTROL: Balanced pacing, 2-3 activities per day
- SLOW_HIDDEN_GEMS: Slower pace, more hidden gems, 1-2 activities per day

Output format:
{
  "trip_summary": {
    "city": "string",
    "dates": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"},
    "total_days": 7,
    "variant": "control|slow_hidden_gems",
    "theme": "Overall trip theme"
  },
  "daily_itineraries": [
    {
      "day": 1,
      "date": "YYYY-MM-DD",
      "theme": "Day theme",
      "weather": {"temp": "20C", "conditions": "sunny"},
      "schedule": [
        {
          "time": "09:00",
          "duration_minutes": 120,
          "activity": "Activity name",
          "type": "meal|culture|nature|transit",
          "location": "Place name",
          "details": "What to do/expect",
          "cost_usd": 25,
          "reservations_needed": false,
          "insider_tip": "Local tip"
        }
      ],
      "meals": {
        "breakfast": {"place": "name", "cost_usd": 15},
        "lunch": {"place": "name", "cost_usd": 20},
        "dinner": {"place": "name", "cost_usd": 40}
      },
      "daily_budget_usd": 150,
      "evening_suggestion": "Optional evening activity"
    }
  ],
  "logistics": {
    "getting_around": "How to navigate the city",
    "key_reservations": ["What to book in advance"],
    "transit_passes": "Recommended passes",
    "estimated_total_cost_usd": 1050
  },
  "packing_list": {
    "essentials": ["Item 1", "Item 2"],
    "weather_appropriate": ["Item 1", "Item 2"],
    "nice_to_have": ["Item 1", "Item 2"]
  },
  "insider_tips": ["Tip 1", "Tip 2", "Tip 3"]
}"""

    def __init__(self, variant: str = "control"):
        """
        variant: 'control' or 'slow_hidden_gems' for A/B testing
        """
        super().__init__(
            agent_type="travel_concierge",
            model="claude-sonnet-4-5-20250929",
            max_tokens=38000,
            temperature=0.7
        )
        self.variant = variant

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Input:
        {
            "city": {...},
            "city_guide": {...},
            "preferences": {...},
            "weather_data": {...},
            "events_data": {...},
            "travel_dates": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
        }
        """

        logger.info("Travel Concierge Agent processing request", extra={"variant": self.variant})

        # Extract input
        city = input_data.get("city", {})
        city_guide = input_data.get("city_guide", {})
        preferences = input_data.get("preferences", {})
        weather_data = input_data.get("weather_data", {})
        events_data = input_data.get("events_data", {})
        travel_dates = input_data.get("travel_dates", {})

        # Build prompt with variant-specific instructions
        user_message = self._build_user_message(
            city, city_guide, preferences, weather_data, events_data, travel_dates
        )

        # Call LLM
        messages = [{"role": "user", "content": user_message}]
        llm_response = self.call_llm(messages)

        # Parse response
        try:
            result = self.parse_json_response(llm_response["response"])

            # Validate
            required_fields = ["trip_summary", "daily_itineraries", "logistics", "packing_list"]
            if not self.validate_output(result, required_fields):
                raise ValueError("Invalid output format")

            # Add variant info
            result["trip_summary"]["variant"] = self.variant

            logger.info(
                f"Generated 7-day itinerary for {city.get('name')}",
                extra={
                    "days": len(result.get("daily_itineraries", [])),
                    "variant": self.variant,
                    "estimated_cost": result.get("logistics", {}).get("estimated_total_cost_usd")
                }
            )

            return {
                "success": True,
                "itinerary": result,
                "cost_tracking": {
                    "input_tokens": self.input_tokens,
                    "output_tokens": self.output_tokens,
                    "cost_usd": self.total_cost
                }
            }

        except Exception as e:
            logger.error(f"Itinerary generation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def _build_user_message(
        self,
        city: Dict[str, Any],
        city_guide: Dict[str, Any],
        preferences: Dict[str, Any],
        weather_data: Dict[str, Any],
        events_data: Dict[str, Any],
        travel_dates: Dict[str, Any]
    ) -> str:
        """Build user message for LLM"""

        # Variant-specific instructions
        pacing_instruction = ""
        if self.variant == "slow_hidden_gems":
            pacing_instruction = """
PACING VARIANT: SLOW & HIDDEN GEMS
- Maximum 1-2 major activities per day
- Prioritize hidden gems over popular spots
- Include more downtime and flexibility
- Focus on depth over breadth
- Allow time for spontaneous discoveries
"""
        else:
            pacing_instruction = """
PACING VARIANT: BALANCED
- 2-3 activities per day
- Mix of popular and hidden gems
- Balanced pace with some flexibility
"""

        return f"""Create a detailed 7-day itinerary for this trip:

CITY:
{json.dumps(city, indent=2)}

TRAVEL DATES:
{json.dumps(travel_dates, indent=2)}

USER PREFERENCES:
{json.dumps(preferences, indent=2)}

LOCAL EXPERT GUIDE:
{json.dumps(city_guide, indent=2)}

WEATHER FORECAST:
{json.dumps(weather_data, indent=2)}

LOCAL EVENTS:
{json.dumps(events_data, indent=2)}

{pacing_instruction}

Create a comprehensive 7-day itinerary that:
1. Follows the specified pacing variant
2. Uses the local expert recommendations
3. Accounts for weather conditions
4. Incorporates relevant local events
5. Includes specific meal recommendations
6. Provides realistic timing and logistics
7. Tracks daily budgets
8. Offers insider tips and flexibility

Return ONLY valid JSON following the specified format."""
