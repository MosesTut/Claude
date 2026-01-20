from anthropic import Anthropic
from app.config import settings
from typing import List, Dict, Any
import json

# Initialize Anthropic client
client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

# AI Model Configuration
AI_MODEL = "claude-3-5-sonnet-20241022"
PROMPT_VERSION = "v1.0"


async def recommend_cities(
    interests: List[str],
    food_preferences: List[str],
    budget_level: str,
    pace: str,
    trip_length_days: int
) -> List[Dict[str, Any]]:
    """
    City Selection Agent
    Recommends 3 cities based on user preferences using Anthropic Claude API
    """

    prompt = f"""You are a travel expert AI. Based on the user's preferences, recommend exactly 3 cities that would be perfect for their trip.

User Preferences:
- Interests: {', '.join(interests) if interests else 'None specified'}
- Food Preferences: {', '.join(food_preferences) if food_preferences else 'None specified'}
- Budget Level: {budget_level}
- Pace: {pace}
- Trip Length: {trip_length_days} days

For each city, provide:
1. City name
2. Country
3. 2-3 sentence reasoning explaining why this city matches their preferences

Return your response as a JSON array with this exact structure:
[
  {{
    "city_name": "Paris",
    "country": "France",
    "reasoning": "Paris is perfect for...",
    "match_score": 0.95
  }},
  ...
]

Be specific about how each city matches their interests, food preferences, budget, and pace."""

    try:
        message = client.messages.create(
            model=AI_MODEL,
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract text content
        response_text = message.content[0].text

        # Parse JSON response
        cities = json.loads(response_text)

        # Validate we got exactly 3 cities
        if len(cities) != 3:
            cities = cities[:3]  # Take first 3 if more

        return cities

    except Exception as e:
        # Fallback to hardcoded cities if API fails
        print(f"Anthropic API error: {e}")
        return [
            {
                "city_name": "Lisbon",
                "country": "Portugal",
                "reasoning": "Lisbon offers a perfect blend of history, culture, and coastal charm. The city's diverse food scene and relaxed pace match your preferences.",
                "match_score": 0.90
            },
            {
                "city_name": "Tokyo",
                "country": "Japan",
                "reasoning": "Tokyo combines cutting-edge modernity with traditional culture. The incredible food scene and efficient transportation fit your travel style.",
                "match_score": 0.88
            },
            {
                "city_name": "Barcelona",
                "country": "Spain",
                "reasoning": "Barcelona's vibrant culture, stunning architecture, and Mediterranean cuisine align perfectly with your interests and budget.",
                "match_score": 0.85
            }
        ]


async def generate_itinerary(
    city_name: str,
    country: str,
    trip_length_days: int,
    interests: List[str],
    food_preferences: List[str],
    budget_level: str,
    pace: str
) -> Dict[str, Any]:
    """
    Concierge Agent
    Generates a day-by-day itinerary for the selected city using Anthropic Claude API

    Returns a structured itinerary with meals, activities, and logistics for each day
    """

    prompt = f"""You are a local travel expert for {city_name}, {country}. Create a detailed {trip_length_days}-day itinerary.

User Preferences:
- Interests: {', '.join(interests) if interests else 'General sightseeing'}
- Food Preferences: {', '.join(food_preferences) if food_preferences else 'Open to all cuisines'}
- Budget Level: {budget_level}
- Pace: {pace}

For each day, provide:
1. Morning activity (with specific venue name and neighborhood)
2. Lunch recommendation (restaurant name, cuisine type, price range)
3. Afternoon activity (with specific venue name)
4. Dinner recommendation (restaurant name, cuisine type, price range)
5. Optional evening activity
6. Practical tips (transportation, timing, reservations needed)

Return your response as a JSON object with this exact structure:
{{
  "city": "{city_name}",
  "country": "{country}",
  "trip_length_days": {trip_length_days},
  "daily_plans": [
    {{
      "day": 1,
      "morning": {{
        "activity": "Visit the Eiffel Tower",
        "location": "Champ de Mars, 7th arrondissement",
        "duration": "2-3 hours",
        "tips": "Arrive early to avoid crowds. Pre-book tickets online."
      }},
      "lunch": {{
        "restaurant": "Café de Flore",
        "cuisine": "French bistro",
        "price_range": "€€",
        "neighborhood": "Saint-Germain-des-Prés"
      }},
      "afternoon": {{
        "activity": "Louvre Museum",
        "location": "1st arrondissement",
        "duration": "3-4 hours",
        "tips": "Focus on specific wings to avoid overwhelm."
      }},
      "dinner": {{
        "restaurant": "Le Comptoir du Relais",
        "cuisine": "Modern French",
        "price_range": "€€€",
        "neighborhood": "Saint-Germain"
      }},
      "evening": {{
        "activity": "Seine River walk",
        "optional": true
      }}
    }},
    ...
  ],
  "general_tips": [
    "Purchase a Paris Museum Pass for skip-the-line access",
    "Use the Metro for efficient transportation",
    "Make dinner reservations 1-2 days in advance"
  ]
}}

Be specific, practical, and match the user's budget and pace preferences."""

    try:
        message = client.messages.create(
            model=AI_MODEL,
            max_tokens=4000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract text content
        response_text = message.content[0].text

        # Parse JSON response
        itinerary = json.loads(response_text)

        return itinerary

    except Exception as e:
        # Fallback to mock itinerary if API fails
        print(f"Anthropic API error: {e}")
        return {
            "city": city_name,
            "country": country,
            "trip_length_days": trip_length_days,
            "daily_plans": [
                {
                    "day": i + 1,
                    "morning": {
                        "activity": f"Morning activity in {city_name}",
                        "location": "City center",
                        "duration": "2-3 hours",
                        "tips": "Start early to avoid crowds"
                    },
                    "lunch": {
                        "restaurant": "Local restaurant",
                        "cuisine": "Local cuisine",
                        "price_range": budget_level,
                        "neighborhood": "City center"
                    },
                    "afternoon": {
                        "activity": f"Afternoon sightseeing",
                        "location": "Main attractions",
                        "duration": "3-4 hours",
                        "tips": "Take breaks as needed"
                    },
                    "dinner": {
                        "restaurant": "Local dining spot",
                        "cuisine": "Traditional",
                        "price_range": budget_level,
                        "neighborhood": "Downtown"
                    },
                    "evening": {
                        "activity": "Evening stroll",
                        "optional": True
                    }
                }
                for i in range(trip_length_days)
            ],
            "general_tips": [
                f"Explore {city_name} at your own pace",
                "Try local specialties",
                "Use public transportation when possible"
            ]
        }
