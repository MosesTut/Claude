"""Local Expert Agent - Provides deep city knowledge"""

from typing import Dict, Any, List, Optional
import json

from ..base_agent import BaseAgent
from ...database.vector_db import get_vector_db
from ...database.models import City, Entity, SessionLocal
from ...utils.logger import get_logger

logger = get_logger(__name__)


class LocalExpertAgent(BaseAgent):
    """Provides deep, authentic local knowledge about a city"""

    SYSTEM_PROMPT = """You are Timbuktoo's Local Expert Agent.

Your role is to provide deep, authentic knowledge about a city, focusing on:
- Hidden gems and local favorites
- Food and drink scene (restaurants, bars, cafes, markets)
- Cultural experiences and neighborhoods
- Nature and outdoor activities
- Insider tips and local customs

Rules:
1. NO HALLUCINATIONS - Use only the grounded data provided
2. Prioritize authentic LOCAL experiences over tourist attractions
3. Focus on food, drink, nightlife, and nature
4. Include practical details (opening hours, price ranges, how to get there)
5. Organize by neighborhood and vibe
6. Output STRICT JSON only

Output format:
{
  "city_overview": {
    "name": "string",
    "vibe": "Overall city character",
    "best_for": ["food", "nightlife", "nature"],
    "insider_tips": ["Tip 1", "Tip 2", "Tip 3"]
  },
  "neighborhoods": [
    {
      "name": "Neighborhood name",
      "vibe": "Character of this area",
      "best_for": ["lunch", "dinner", "nightlife"],
      "highlights": ["Place 1", "Place 2"]
    }
  ],
  "must_visit": {
    "restaurants": [...],
    "bars": [...],
    "cafes": [...],
    "nature_spots": [...],
    "cultural_sites": [...]
  },
  "hidden_gems": [
    {
      "name": "Place name",
      "type": "restaurant|bar|nature|etc",
      "why": "What makes it special",
      "vibe": ["local", "authentic"],
      "price_tier": "mid"
    }
  ],
  "local_customs": ["Custom 1", "Custom 2"],
  "practical_info": {
    "best_areas_to_stay": ["Area 1", "Area 2"],
    "transport": "How to get around",
    "food_scene_overview": "Summary of food culture"
  }
}"""

    def __init__(self):
        super().__init__(
            agent_type="local_expert",
            model="claude-sonnet-4-5-20250929",
            max_tokens=15000,
            temperature=0.7
        )
        self.vector_db = get_vector_db()

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Input:
        {
            "city_id": "uuid",
            "preferences": {
                "vibes": ["local", "nightlife"],
                "interests": ["food", "drink", "nature"]
            },
            "vector_chunks_limit": 35
        }
        """

        logger.info("Local Expert Agent processing request")

        # Extract input
        city_id = input_data.get("city_id")
        preferences = input_data.get("preferences", {})
        chunks_limit = input_data.get("vector_chunks_limit", 35)

        if not city_id:
            raise ValueError("city_id is required")

        # Get city data
        city_data = self._get_city_data(city_id)

        # Get relevant knowledge from vector DB
        knowledge = self._get_city_knowledge(
            city_id,
            preferences,
            limit=chunks_limit
        )

        # Build prompt
        user_message = self._build_user_message(city_data, knowledge, preferences)

        # Call LLM
        messages = [{"role": "user", "content": user_message}]
        llm_response = self.call_llm(messages)

        # Parse response
        try:
            result = self.parse_json_response(llm_response["response"])

            # Validate
            required_fields = ["city_overview", "must_visit", "hidden_gems"]
            if not self.validate_output(result, required_fields):
                raise ValueError("Invalid output format")

            logger.info(
                f"Generated local guide for {city_data['name']}",
                extra={
                    "neighborhoods": len(result.get("neighborhoods", [])),
                    "hidden_gems": len(result.get("hidden_gems", []))
                }
            )

            return {
                "success": True,
                "city_guide": result,
                "knowledge_chunks_used": len(knowledge),
                "cost_tracking": {
                    "input_tokens": self.input_tokens,
                    "output_tokens": self.output_tokens,
                    "cost_usd": self.total_cost
                }
            }

        except Exception as e:
            logger.error(f"Local expert generation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def _get_city_data(self, city_id: str) -> Dict[str, Any]:
        """Get city metadata from database"""
        db = SessionLocal()
        try:
            city = db.query(City).filter(City.city_id == city_id).first()
            if not city:
                raise ValueError(f"City {city_id} not found")
            return city.to_dict()
        finally:
            db.close()

    def _get_city_knowledge(
        self,
        city_id: str,
        preferences: Dict[str, Any],
        limit: int = 35
    ) -> List[Dict[str, Any]]:
        """Get relevant knowledge from vector database"""

        vibes = preferences.get("vibes", [])
        interests = preferences.get("interests", [])

        # Build search query
        query_parts = []
        if interests:
            query_parts.append(f"Interests: {', '.join(interests)}")
        if vibes:
            query_parts.append(f"Vibes: {', '.join(vibes)}")

        query = " ".join(query_parts) if query_parts else "local experiences food drink"

        # Search vector DB
        results = self.vector_db.search(
            query=query,
            city_id=city_id,
            n_results=limit,
            vibes=vibes if vibes else None
        )

        logger.info(f"Retrieved {len(results)} knowledge chunks from vector DB")

        return results

    def _build_user_message(
        self,
        city_data: Dict[str, Any],
        knowledge: List[Dict[str, Any]],
        preferences: Dict[str, Any]
    ) -> str:
        """Build user message for LLM"""

        # Format knowledge chunks
        knowledge_text = "\n\n".join([
            f"[{k.get('entity_type', 'unknown').upper()}] {k.get('title', 'Unknown')}\n"
            f"Vibes: {', '.join(k.get('vibe', []))}\n"
            f"Price: {k.get('price_tier', 'unknown')}\n"
            f"{k.get('content', '')}"
            for k in knowledge
        ])

        return f"""Create a comprehensive local guide for this city:

CITY: {city_data['name']}, {city_data['country']}
Description: {city_data.get('description', 'No description')}
Best seasons: {', '.join(city_data.get('best_seasons', []))}

USER PREFERENCES:
{json.dumps(preferences, indent=2)}

LOCAL KNOWLEDGE (from verified sources):
{knowledge_text}

Create a detailed guide that helps the traveler experience this city like a local.
Focus on authentic experiences, especially food, drink, nightlife, and nature.
Include hidden gems and insider tips.

Return ONLY valid JSON following the specified format."""
