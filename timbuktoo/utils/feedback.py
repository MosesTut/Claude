"""Feedback collection and analysis system"""

from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime

from ..database.models import Feedback, Trip, SessionLocal
from ..utils.logger import get_logger

logger = get_logger(__name__)


class FeedbackCollector:
    """Collects and stores user feedback"""

    def __init__(self):
        pass

    def collect_feedback(
        self,
        trip_id: str,
        overall_rating: int,
        daily_ratings: Optional[Dict[str, int]] = None,
        comments: Optional[str] = None,
        pacing_rating: Optional[int] = None,
        authenticity_rating: Optional[int] = None,
        value_rating: Optional[int] = None,
        liked_entities: Optional[List[str]] = None,
        disliked_entities: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Collect feedback for a trip

        Args:
            trip_id: Trip UUID
            overall_rating: 1-5 rating
            daily_ratings: {"day1": 5, "day2": 4, ...}
            comments: Free text feedback
            pacing_rating: 1-5 rating for pacing
            authenticity_rating: 1-5 rating for authenticity
            value_rating: 1-5 rating for value
            liked_entities: List of entity UUIDs user liked
            disliked_entities: List of entity UUIDs user disliked

        Returns:
            {
                "success": bool,
                "feedback_id": str,
                "insights": {...}
            }
        """

        db = SessionLocal()
        try:
            # Validate trip exists
            trip = db.query(Trip).filter(Trip.trip_id == trip_id).first()
            if not trip:
                return {
                    "success": False,
                    "error": f"Trip {trip_id} not found"
                }

            # Create feedback record
            feedback = Feedback(
                trip_id=trip_id,
                overall_rating=overall_rating,
                daily_ratings=daily_ratings,
                comments=comments,
                pacing_rating=pacing_rating,
                authenticity_rating=authenticity_rating,
                value_rating=value_rating,
                liked_entities=[uuid.UUID(e) for e in liked_entities] if liked_entities else [],
                disliked_entities=[uuid.UUID(e) for e in disliked_entities] if disliked_entities else []
            )

            db.add(feedback)
            db.commit()
            db.refresh(feedback)

            logger.info(
                f"Feedback collected for trip {trip_id}",
                extra={
                    "overall_rating": overall_rating,
                    "pacing_rating": pacing_rating,
                    "variant": trip.variant_id
                }
            )

            # Generate insights
            insights = self._generate_insights(feedback, trip)

            return {
                "success": True,
                "feedback_id": str(feedback.feedback_id),
                "insights": insights
            }

        except Exception as e:
            logger.error(f"Failed to collect feedback: {str(e)}")
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            db.close()

    def _generate_insights(self, feedback: Feedback, trip: Trip) -> Dict[str, Any]:
        """Generate insights from feedback"""

        insights = {
            "satisfaction_level": "high" if feedback.overall_rating >= 4 else "medium" if feedback.overall_rating >= 3 else "low",
            "pacing_assessment": None,
            "variant": trip.variant_id,
            "recommendations": []
        }

        # Pacing analysis
        if feedback.pacing_rating:
            if feedback.pacing_rating <= 2:
                insights["pacing_assessment"] = "too_fast"
                insights["recommendations"].append("Consider slower pacing variant")
            elif feedback.pacing_rating >= 4:
                insights["pacing_assessment"] = "good"
            else:
                insights["pacing_assessment"] = "acceptable"

        # Authenticity analysis
        if feedback.authenticity_rating:
            if feedback.authenticity_rating <= 3:
                insights["recommendations"].append("Prioritize more hidden gems")

        # Value analysis
        if feedback.value_rating:
            if feedback.value_rating <= 3:
                insights["recommendations"].append("Review budget recommendations")

        return insights

    def get_trip_feedback(self, trip_id: str) -> Optional[Dict[str, Any]]:
        """Get feedback for a trip"""
        db = SessionLocal()
        try:
            feedback = db.query(Feedback).filter(Feedback.trip_id == trip_id).first()
            if feedback:
                return feedback.to_dict()
            return None
        finally:
            db.close()

    def get_variant_performance(self, variant_id: str) -> Dict[str, Any]:
        """Get aggregate performance for an A/B test variant"""
        db = SessionLocal()
        try:
            # Get all trips with this variant
            trips = db.query(Trip).filter(Trip.variant_id == variant_id).all()

            if not trips:
                return {
                    "variant": variant_id,
                    "sample_size": 0,
                    "metrics": {}
                }

            # Get feedback for these trips
            trip_ids = [str(t.trip_id) for t in trips]
            feedbacks = db.query(Feedback).filter(Feedback.trip_id.in_(trip_ids)).all()

            if not feedbacks:
                return {
                    "variant": variant_id,
                    "sample_size": len(trips),
                    "feedback_count": 0,
                    "metrics": {}
                }

            # Calculate metrics
            overall_ratings = [f.overall_rating for f in feedbacks if f.overall_rating]
            pacing_ratings = [f.pacing_rating for f in feedbacks if f.pacing_rating]
            authenticity_ratings = [f.authenticity_rating for f in feedbacks if f.authenticity_rating]
            value_ratings = [f.value_rating for f in feedbacks if f.value_rating]

            metrics = {
                "overall_rating_avg": sum(overall_ratings) / len(overall_ratings) if overall_ratings else 0,
                "pacing_rating_avg": sum(pacing_ratings) / len(pacing_ratings) if pacing_ratings else 0,
                "authenticity_rating_avg": sum(authenticity_ratings) / len(authenticity_ratings) if authenticity_ratings else 0,
                "value_rating_avg": sum(value_ratings) / len(value_ratings) if value_ratings else 0,
                "satisfaction_rate": len([r for r in overall_ratings if r >= 4]) / len(overall_ratings) if overall_ratings else 0
            }

            return {
                "variant": variant_id,
                "sample_size": len(trips),
                "feedback_count": len(feedbacks),
                "metrics": metrics
            }

        finally:
            db.close()

    def compare_variants(self, variant_a: str, variant_b: str) -> Dict[str, Any]:
        """Compare two A/B test variants"""

        perf_a = self.get_variant_performance(variant_a)
        perf_b = self.get_variant_performance(variant_b)

        comparison = {
            "variant_a": variant_a,
            "variant_b": variant_b,
            "metrics_a": perf_a.get("metrics", {}),
            "metrics_b": perf_b.get("metrics", {}),
            "sample_sizes": {
                "variant_a": perf_a.get("feedback_count", 0),
                "variant_b": perf_b.get("feedback_count", 0)
            }
        }

        # Determine winner
        if perf_a.get("metrics", {}).get("overall_rating_avg", 0) > perf_b.get("metrics", {}).get("overall_rating_avg", 0):
            comparison["winner"] = variant_a
        elif perf_b.get("metrics", {}).get("overall_rating_avg", 0) > perf_a.get("metrics", {}).get("overall_rating_avg", 0):
            comparison["winner"] = variant_b
        else:
            comparison["winner"] = "tie"

        return comparison


# Singleton instance
_feedback_collector = None

def get_feedback_collector() -> FeedbackCollector:
    """Get or create feedback collector instance"""
    global _feedback_collector
    if _feedback_collector is None:
        _feedback_collector = FeedbackCollector()
    return _feedback_collector
