"""Main workflow orchestrator - ties all agents and tools together"""

from typing import Dict, Any, Optional
import uuid
from datetime import datetime, timedelta
import time

from ..agents.city_selection import CitySelectionAgent
from ..agents.local_expert import LocalExpertAgent
from ..agents.concierge import TravelConciergeAgent
from ..tools.weather import get_weather_tool
from ..tools.events import get_events_tool
from ..database.models import Trip, SessionLocal
from ..utils.cost_tracker import CostController
from ..utils.monitoring import get_metrics_collector
from ..security.audit import get_audit_logger
from ..utils.logger import get_logger

logger = get_logger(__name__)


class TravelOrchestrator:
    """Orchestrates the full travel planning workflow"""

    def __init__(self, variant: str = "control"):
        """
        Initialize orchestrator

        Args:
            variant: A/B test variant ('control' or 'slow_hidden_gems')
        """
        self.variant = variant
        self.cost_controller = CostController(max_trip_cost_usd=0.80)
        self.metrics = get_metrics_collector()
        self.audit = get_audit_logger()
        self.weather_tool = get_weather_tool()
        self.events_tool = get_events_tool()

    def create_trip(
        self,
        preferences: Dict[str, Any],
        travel_dates: Dict[str, str],
        candidate_cities: Optional[list] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main workflow: Create a complete trip itinerary

        Args:
            preferences: User preferences (vibes, interests, budget)
            travel_dates: {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
            candidate_cities: Optional list of candidate cities
            user_id: Optional user ID for tracking

        Returns:
            {
                "success": bool,
                "trip_id": str,
                "selected_city": {...},
                "city_guide": {...},
                "itinerary": {...},
                "cost_summary": {...}
            }
        """

        trip_id = str(uuid.uuid4())
        start_time = time.time()

        try:
            logger.info(
                "Starting trip creation workflow",
                extra={"trip_id": trip_id, "variant": self.variant}
            )

            # Step 1: City Selection
            logger.info("Step 1: City Selection")
            city_selection_start = time.time()

            # Get weather data for candidate cities
            weather_data = self._get_weather_for_candidates(
                candidate_cities or [],
                travel_dates
            )

            # Get events data for candidate cities
            events_data = self._get_events_for_candidates(
                candidate_cities or [],
                travel_dates
            )

            # Run city selection agent
            city_agent = CitySelectionAgent()
            city_selection_result = city_agent.process({
                "preferences": preferences,
                "candidate_cities": candidate_cities,
                "weather_data": weather_data,
                "events_data": events_data
            })

            if not city_selection_result.get("success"):
                raise Exception("City selection failed")

            # Track cost
            self.cost_controller.add_cost(
                "city_selection",
                city_selection_result["cost_tracking"]["cost_usd"]
            )

            # Track metrics
            city_selection_time = time.time() - city_selection_start
            self.metrics.record_agent_call(
                "city_selection",
                city_selection_result["cost_tracking"]["cost_usd"],
                city_selection_time
            )

            # Select top city
            selected_city = city_selection_result["ranked_cities"][0]
            logger.info(f"Selected city: {selected_city['name']}")

            # Step 2: Local Expert Knowledge
            logger.info("Step 2: Local Expert Knowledge")
            expert_start = time.time()

            # Check budget
            strategy = self.cost_controller.degrade_gracefully()

            expert_agent = LocalExpertAgent()
            expert_result = expert_agent.process({
                "city_id": selected_city["city_id"],
                "preferences": preferences,
                "vector_chunks_limit": strategy["vector_chunks"]
            })

            if not expert_result.get("success"):
                raise Exception("Local expert failed")

            # Track cost
            self.cost_controller.add_cost(
                "local_expert",
                expert_result["cost_tracking"]["cost_usd"]
            )

            # Track metrics
            expert_time = time.time() - expert_start
            self.metrics.record_agent_call(
                "local_expert",
                expert_result["cost_tracking"]["cost_usd"],
                expert_time
            )

            city_guide = expert_result["city_guide"]

            # Step 3: Get specific weather and events for selected city
            logger.info("Step 3: Fetching weather and events for selected city")

            city_weather = self.weather_tool.get_forecast(
                selected_city["name"],
                selected_city["country"],
                travel_dates["start"],
                days=7
            )

            city_events = self.events_tool.get_events(
                selected_city["name"],
                selected_city["country"],
                travel_dates["start"],
                travel_dates["end"]
            )

            # Step 4: Travel Concierge - Create Itinerary
            logger.info("Step 4: Creating 7-day itinerary")
            concierge_start = time.time()

            concierge_agent = TravelConciergeAgent(variant=self.variant)
            concierge_result = concierge_agent.process({
                "city": selected_city,
                "city_guide": city_guide,
                "preferences": preferences,
                "weather_data": city_weather,
                "events_data": city_events,
                "travel_dates": travel_dates
            })

            if not concierge_result.get("success"):
                raise Exception("Concierge failed")

            # Track cost
            self.cost_controller.add_cost(
                "concierge",
                concierge_result["cost_tracking"]["cost_usd"]
            )

            # Track metrics
            concierge_time = time.time() - concierge_start
            self.metrics.record_agent_call(
                "concierge",
                concierge_result["cost_tracking"]["cost_usd"],
                concierge_time
            )

            itinerary = concierge_result["itinerary"]

            # Step 5: Save trip to database
            logger.info("Step 5: Saving trip to database")
            self._save_trip(
                trip_id,
                user_id,
                selected_city["city_id"],
                travel_dates,
                preferences,
                itinerary,
                city_weather,
                city_events
            )

            # Final metrics
            total_time = time.time() - start_time
            cost_summary = self.cost_controller.get_summary()

            self.metrics.record_trip_request(selected_city["name"], self.variant)
            self.metrics.record_trip_cost(cost_summary["total_cost_usd"], self.variant)

            # Audit log
            self.audit.log_trip_creation(
                user_id=user_id,
                trip_id=trip_id,
                city_id=selected_city["city_id"],
                success=True,
                details={
                    "variant": self.variant,
                    "total_cost_usd": cost_summary["total_cost_usd"]
                }
            )

            logger.info(
                "Trip creation completed successfully",
                extra={
                    "trip_id": trip_id,
                    "total_time": total_time,
                    "cost_summary": cost_summary
                }
            )

            return {
                "success": True,
                "trip_id": trip_id,
                "selected_city": selected_city,
                "all_ranked_cities": city_selection_result["ranked_cities"],
                "city_guide": city_guide,
                "itinerary": itinerary,
                "cost_summary": cost_summary,
                "processing_time_seconds": round(total_time, 2)
            }

        except Exception as e:
            logger.error(f"Trip creation failed: {str(e)}")

            # Audit log failure
            self.audit.log_trip_creation(
                user_id=user_id,
                trip_id=trip_id,
                city_id="unknown",
                success=False,
                details={"error": str(e), "variant": self.variant}
            )

            return {
                "success": False,
                "error": str(e),
                "trip_id": trip_id
            }

    def _get_weather_for_candidates(
        self,
        cities: list,
        travel_dates: Dict[str, str]
    ) -> Dict[str, Any]:
        """Get weather data for candidate cities"""
        weather_data = {}
        for city in cities[:5]:  # Limit to 5 cities to control costs
            try:
                forecast = self.weather_tool.get_forecast(
                    city.get("name", ""),
                    city.get("country", ""),
                    travel_dates["start"],
                    days=7
                )
                weather_data[city["name"]] = forecast
            except Exception as e:
                logger.error(f"Failed to get weather for {city.get('name')}: {str(e)}")
        return weather_data

    def _get_events_for_candidates(
        self,
        cities: list,
        travel_dates: Dict[str, str]
    ) -> Dict[str, Any]:
        """Get events data for candidate cities"""
        events_data = {}
        for city in cities[:5]:  # Limit to 5 cities
            try:
                events = self.events_tool.get_events(
                    city.get("name", ""),
                    city.get("country", ""),
                    travel_dates["start"],
                    travel_dates["end"]
                )
                events_data[city["name"]] = events
            except Exception as e:
                logger.error(f"Failed to get events for {city.get('name')}: {str(e)}")
        return events_data

    def _save_trip(
        self,
        trip_id: str,
        user_id: Optional[str],
        city_id: str,
        travel_dates: Dict[str, str],
        preferences: Dict[str, Any],
        itinerary: Dict[str, Any],
        weather_data: Dict[str, Any],
        events_data: Dict[str, Any]
    ):
        """Save trip to database"""
        db = SessionLocal()
        try:
            trip = Trip(
                trip_id=uuid.UUID(trip_id),
                user_id=uuid.UUID(user_id) if user_id else None,
                city_id=uuid.UUID(city_id),
                start_date=datetime.strptime(travel_dates["start"], "%Y-%m-%d").date(),
                end_date=datetime.strptime(travel_dates["end"], "%Y-%m-%d").date(),
                preferences=preferences,
                itinerary=itinerary,
                estimated_cost_usd=itinerary.get("logistics", {}).get("estimated_total_cost_usd"),
                weather_data=weather_data,
                events_data=events_data,
                variant_id=self.variant
            )
            db.add(trip)
            db.commit()
            logger.info(f"Trip {trip_id} saved to database")
        except Exception as e:
            logger.error(f"Failed to save trip: {str(e)}")
            db.rollback()
        finally:
            db.close()
