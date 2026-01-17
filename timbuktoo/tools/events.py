"""Events API integration"""

import requests
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from tenacity import retry, stop_after_attempt, wait_exponential

from ..utils.logger import get_logger

logger = get_logger(__name__)


class EventsTool:
    """Fetches local events and happenings"""

    def __init__(self):
        self.api_key = os.getenv("EVENTS_API_KEY")
        self.base_url = "https://api.predicthq.com/v1"  # Example: PredictHQ
        self.cache = {}

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def get_events(
        self,
        city: str,
        country: str,
        start_date: str,
        end_date: str,
        categories: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get local events for a city during date range

        Returns:
        {
            "city": "Lisbon",
            "country": "Portugal",
            "date_range": {"start": "2024-06-01", "end": "2024-06-07"},
            "events": [
                {
                    "title": "Event name",
                    "date": "2024-06-03",
                    "category": "festival|concert|sports|cultural",
                    "description": "Event details",
                    "location": "Venue name",
                    "cost": "free|paid",
                    "relevance": 0.85
                }
            ]
        }
        """

        cache_key = f"{city}_{country}_{start_date}_{end_date}"
        if cache_key in self.cache:
            logger.info(f"Events cache hit for {city}")
            return self.cache[cache_key]

        try:
            if not self.api_key:
                logger.warning("No events API key, returning mock data")
                return self._get_mock_events(city, country, start_date, end_date)

            # Call events API (example with PredictHQ)
            params = {
                "q": city,
                "country": country,
                "start": start_date,
                "end": end_date,
                "limit": 50
            }

            if categories:
                params["category"] = ",".join(categories)

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json"
            }

            response = requests.get(
                f"{self.base_url}/events",
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()

            # Process events
            events = self._process_events_data(data)

            result = {
                "city": city,
                "country": country,
                "date_range": {"start": start_date, "end": end_date},
                "events": events,
                "source": "PredictHQ"
            }

            # Cache result
            self.cache[cache_key] = result

            logger.info(f"Fetched {len(events)} events for {city}")
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"Events API error: {str(e)}")
            return self._get_mock_events(city, country, start_date, end_date)

    def _process_events_data(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process API response into event list"""

        events = []
        for item in data.get("results", []):
            events.append({
                "title": item.get("title", "Unknown Event"),
                "date": item.get("start", "")[:10],  # Extract date part
                "category": item.get("category", "general"),
                "description": item.get("description", ""),
                "location": item.get("location", ""),
                "cost": "paid" if item.get("paid", False) else "free",
                "relevance": item.get("rank", 50) / 100.0
            })

        # Sort by relevance
        events.sort(key=lambda x: x["relevance"], reverse=True)

        return events[:20]  # Top 20 events

    def _get_mock_events(
        self,
        city: str,
        country: str,
        start_date: str,
        end_date: str
    ) -> Dict[str, Any]:
        """Generate mock events data for testing"""

        logger.info(f"Generating mock events for {city}")

        # Sample events database
        event_templates = [
            {
                "title": "Local Food Market",
                "category": "food",
                "description": "Weekly farmers market with local produce and street food",
                "location": "Central Square",
                "cost": "free"
            },
            {
                "title": "Live Music at Downtown Bar",
                "category": "music",
                "description": "Local jazz band performing",
                "location": "Jazz Cafe",
                "cost": "free"
            },
            {
                "title": "Art Gallery Opening",
                "category": "cultural",
                "description": "Contemporary art exhibition opening",
                "location": "City Gallery",
                "cost": "free"
            },
            {
                "title": "Walking Food Tour",
                "category": "food",
                "description": "Guided tour of best local eateries",
                "location": "Historic District",
                "cost": "paid"
            },
            {
                "title": "Outdoor Concert",
                "category": "festival",
                "description": "Free outdoor concert in the park",
                "location": "City Park",
                "cost": "free"
            }
        ]

        # Generate events across date range
        events = []
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        current = start
        idx = 0
        while current <= end and idx < len(event_templates):
            event = event_templates[idx].copy()
            event["date"] = current.strftime("%Y-%m-%d")
            event["relevance"] = 0.7 + (idx % 3) * 0.1
            events.append(event)

            current += timedelta(days=2)
            idx += 1

        return {
            "city": city,
            "country": country,
            "date_range": {"start": start_date, "end": end_date},
            "events": events,
            "source": "mock"
        }


# Singleton instance
_events_tool = None

def get_events_tool() -> EventsTool:
    """Get or create events tool instance"""
    global _events_tool
    if _events_tool is None:
        _events_tool = EventsTool()
    return _events_tool
