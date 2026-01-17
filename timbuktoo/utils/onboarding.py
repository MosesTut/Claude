"""Customer onboarding flow manager"""

from typing import Dict, Any, Optional
import uuid
from datetime import datetime

from ..database.models import OnboardingSession, SessionLocal
from ..agents.city_selection.city_selector import CitySelectionAgent
from ..agents.local_expert.expert import LocalExpertAgent
from ..agents.concierge.concierge import TravelConciergeAgent
from ..tools.weather import get_weather_tool
from ..tools.events import get_events_tool
from ..utils.logger import get_logger
from ..utils.tenant_manager import get_tenant_manager

logger = get_logger(__name__)


class OnboardingManager:
    """Manages customer onboarding flow"""

    STEPS = [
        "signup",
        "preferences",
        "city_selection",
        "itinerary",
        "feedback",
        "completed"
    ]

    def __init__(self):
        self.tenant_manager = get_tenant_manager()

    def start_onboarding(self, email: str, tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Start new onboarding session

        Args:
            email: User email
            tenant_id: Optional tenant ID (for existing tenants)

        Returns:
            {
                "success": bool,
                "session_id": str,
                "current_step": str
            }
        """
        db = SessionLocal()
        try:
            # Create onboarding session
            session = OnboardingSession(
                tenant_id=uuid.UUID(tenant_id) if tenant_id else None,
                email=email,
                current_step="signup"
            )
            db.add(session)
            db.commit()
            db.refresh(session)

            logger.info(
                f"Onboarding started for {email}",
                extra={"session_id": str(session.session_id)}
            )

            return {
                "success": True,
                "session_id": str(session.session_id),
                "current_step": "signup",
                "next_step": "preferences"
            }

        except Exception as e:
            logger.error(f"Failed to start onboarding: {str(e)}")
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            db.close()

    def complete_signup(
        self,
        session_id: str,
        tenant_name: str,
        company_name: str,
        plan_id: str = "starter_monthly"
    ) -> Dict[str, Any]:
        """
        Complete signup step - creates tenant

        Step 1: Tenant signup
        """
        db = SessionLocal()
        try:
            session = db.query(OnboardingSession).filter(
                OnboardingSession.session_id == session_id
            ).first()

            if not session:
                return {"success": False, "error": "Session not found"}

            # Create tenant
            result = self.tenant_manager.create_tenant(
                tenant_name=tenant_name,
                company_name=company_name,
                email=session.email,
                plan_id=plan_id,
                trial_days=14
            )

            if not result["success"]:
                return result

            # Update session
            session.tenant_id = uuid.UUID(result["tenant_id"])
            session.current_step = "preferences"
            db.commit()

            logger.info(
                f"Signup completed for session {session_id}",
                extra={"tenant_id": result["tenant_id"]}
            )

            return {
                "success": True,
                "tenant": result,
                "current_step": "preferences",
                "next_step": "city_selection"
            }

        except Exception as e:
            logger.error(f"Failed to complete signup: {str(e)}")
            db.rollback()
            return {"success": False, "error": str(e)}
        finally:
            db.close()

    def capture_preferences(
        self,
        session_id: str,
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Capture user preferences

        Step 2: Preference capture

        preferences = {
            "vibes": ["local", "food", "nightlife"],
            "interests": ["food", "drink", "nature", "culture"],
            "budget_level": "mid",
            "travel_dates": {"start": "2024-06-01", "end": "2024-06-07"}
        }
        """
        db = SessionLocal()
        try:
            session = db.query(OnboardingSession).filter(
                OnboardingSession.session_id == session_id
            ).first()

            if not session:
                return {"success": False, "error": "Session not found"}

            if session.current_step != "preferences":
                return {"success": False, "error": f"Invalid step. Current: {session.current_step}"}

            # Store preferences
            session.preferences = preferences
            session.current_step = "city_selection"
            db.commit()

            logger.info(
                f"Preferences captured for session {session_id}",
                extra={"preferences": preferences}
            )

            return {
                "success": True,
                "preferences": preferences,
                "current_step": "city_selection",
                "next_step": "itinerary"
            }

        except Exception as e:
            logger.error(f"Failed to capture preferences: {str(e)}")
            db.rollback()
            return {"success": False, "error": str(e)}
        finally:
            db.close()

    def recommend_cities(self, session_id: str) -> Dict[str, Any]:
        """
        Recommend cities based on preferences

        Step 3: City recommendation
        """
        db = SessionLocal()
        try:
            session = db.query(OnboardingSession).filter(
                OnboardingSession.session_id == session_id
            ).first()

            if not session:
                return {"success": False, "error": "Session not found"}

            if not session.preferences:
                return {"success": False, "error": "Preferences not captured"}

            # Get weather and events data
            weather_tool = get_weather_tool()
            events_tool = get_events_tool()

            # Mock candidate cities (would normally query from database)
            candidate_cities = [
                {"name": "Lisbon", "country": "Portugal"},
                {"name": "Barcelona", "country": "Spain"},
                {"name": "Mexico City", "country": "Mexico"},
                {"name": "Tokyo", "country": "Japan"},
                {"name": "New York City", "country": "USA"}
            ]

            # Fetch weather and events for candidates
            travel_dates = session.preferences.get("travel_dates", {})
            weather_data = {}
            events_data = {}

            for city in candidate_cities[:3]:  # Limit to top 3 for performance
                try:
                    weather = weather_tool.get_forecast(
                        city["name"],
                        city["country"],
                        travel_dates.get("start", "2024-06-01"),
                        days=7
                    )
                    weather_data[city["name"]] = weather

                    events = events_tool.get_events(
                        city["name"],
                        city["country"],
                        travel_dates.get("start", "2024-06-01"),
                        travel_dates.get("end", "2024-06-07")
                    )
                    events_data[city["name"]] = events
                except Exception as e:
                    logger.warning(f"Failed to fetch data for {city['name']}: {str(e)}")

            # Use City Selection Agent
            city_agent = CitySelectionAgent()
            result = city_agent.process({
                "preferences": session.preferences,
                "candidate_cities": candidate_cities,
                "weather_data": weather_data,
                "events_data": events_data
            })

            if not result["success"]:
                return result

            # Store top city selection
            ranked_cities = result["ranked_cities"]
            if ranked_cities:
                # Auto-select top city
                top_city = ranked_cities[0]
                session.selected_city_id = uuid.UUID(top_city["city_id"]) if "city_id" in top_city else None

            db.commit()

            logger.info(
                f"Cities recommended for session {session_id}",
                extra={"top_city": ranked_cities[0]["name"] if ranked_cities else None}
            )

            return {
                "success": True,
                "ranked_cities": ranked_cities,
                "selection_rationale": result["selection_rationale"],
                "current_step": "city_selection"
            }

        except Exception as e:
            logger.error(f"Failed to recommend cities: {str(e)}")
            db.rollback()
            return {"success": False, "error": str(e)}
        finally:
            db.close()

    def select_city(self, session_id: str, city_id: str) -> Dict[str, Any]:
        """
        User selects a city

        Step 3b: City selection (user choice)
        """
        db = SessionLocal()
        try:
            session = db.query(OnboardingSession).filter(
                OnboardingSession.session_id == session_id
            ).first()

            if not session:
                return {"success": False, "error": "Session not found"}

            session.selected_city_id = uuid.UUID(city_id)
            session.current_step = "itinerary"
            db.commit()

            return {
                "success": True,
                "selected_city_id": city_id,
                "current_step": "itinerary",
                "next_step": "feedback"
            }

        except Exception as e:
            logger.error(f"Failed to select city: {str(e)}")
            db.rollback()
            return {"success": False, "error": str(e)}
        finally:
            db.close()

    def generate_itinerary(self, session_id: str) -> Dict[str, Any]:
        """
        Generate full itinerary

        Step 4: Itinerary delivery
        """
        db = SessionLocal()
        try:
            session = db.query(OnboardingSession).filter(
                OnboardingSession.session_id == session_id
            ).first()

            if not session:
                return {"success": False, "error": "Session not found"}

            if not session.selected_city_id or not session.preferences:
                return {"success": False, "error": "City or preferences not selected"}

            # Check tenant quota
            if session.tenant_id:
                quota_check = self.tenant_manager.check_quota(
                    str(session.tenant_id),
                    "itineraries"
                )

                if not quota_check["allowed"]:
                    return {
                        "success": False,
                        "error": "Quota exceeded. Please upgrade your plan.",
                        "quota": quota_check
                    }

            # Get city data, local expert guide, then create itinerary
            # (This would integrate with the full agent workflow)

            # Simplified for onboarding
            itinerary = {
                "city": "Lisbon",  # Would be actual city
                "dates": session.preferences.get("travel_dates"),
                "message": "Your personalized 7-day itinerary is being prepared!",
                "status": "generated"
            }

            session.itinerary = itinerary
            session.current_step = "feedback"

            # Increment usage
            if session.tenant_id:
                self.tenant_manager.increment_usage(
                    str(session.tenant_id),
                    "itineraries",
                    1
                )

            db.commit()

            logger.info(f"Itinerary generated for session {session_id}")

            return {
                "success": True,
                "itinerary": itinerary,
                "current_step": "feedback",
                "next_step": "completed"
            }

        except Exception as e:
            logger.error(f"Failed to generate itinerary: {str(e)}")
            db.rollback()
            return {"success": False, "error": str(e)}
        finally:
            db.close()

    def collect_feedback(
        self,
        session_id: str,
        rating: int,
        comments: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Collect onboarding feedback

        Step 5: Feedback loop
        """
        db = SessionLocal()
        try:
            session = db.query(OnboardingSession).filter(
                OnboardingSession.session_id == session_id
            ).first()

            if not session:
                return {"success": False, "error": "Session not found"}

            # Store feedback in session metadata
            if not session.preferences:
                session.preferences = {}

            session.preferences["onboarding_feedback"] = {
                "rating": rating,
                "comments": comments
            }

            session.current_step = "completed"
            session.completed_at = datetime.utcnow()
            db.commit()

            logger.info(
                f"Onboarding completed for session {session_id}",
                extra={"rating": rating}
            )

            return {
                "success": True,
                "message": "Thank you for your feedback!",
                "current_step": "completed"
            }

        except Exception as e:
            logger.error(f"Failed to collect feedback: {str(e)}")
            db.rollback()
            return {"success": False, "error": str(e)}
        finally:
            db.close()

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get onboarding session details"""
        db = SessionLocal()
        try:
            session = db.query(OnboardingSession).filter(
                OnboardingSession.session_id == session_id
            ).first()

            if not session:
                return None

            return session.to_dict()

        finally:
            db.close()


# Singleton instance
_onboarding_manager = None

def get_onboarding_manager() -> OnboardingManager:
    """Get or create onboarding manager instance"""
    global _onboarding_manager
    if _onboarding_manager is None:
        _onboarding_manager = OnboardingManager()
    return _onboarding_manager
