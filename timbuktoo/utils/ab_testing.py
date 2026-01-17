"""A/B Testing utilities for variant assignment and analysis"""

import hashlib
from typing import Dict, Any, Optional
from datetime import datetime

from ..database.models import Trip, Feedback, SessionLocal
from ..utils.logger import get_logger

logger = get_logger(__name__)


def assign_variant(trip_id: str, stratify_by: Optional[str] = None) -> str:
    """
    Deterministic variant assignment based on trip_id
    Ensures 50/50 split between control and slow_hidden_gems

    Args:
        trip_id: Trip UUID string
        stratify_by: Optional stratification key (e.g., city_id)

    Returns:
        Variant name: 'control' or 'slow_hidden_gems'
    """

    # Use trip_id + stratify_by for deterministic hash
    hash_input = trip_id
    if stratify_by:
        hash_input = f"{trip_id}:{stratify_by}"

    # MD5 hash for deterministic assignment
    hash_val = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)

    # Even hash → slow_hidden_gems, Odd → control (50/50 split)
    variant = "slow_hidden_gems" if hash_val % 2 == 0 else "control"

    logger.info(
        f"Variant assigned for trip {trip_id}",
        extra={"variant": variant, "stratify_by": stratify_by}
    )

    return variant


def get_variant_performance(variant_id: str) -> Dict[str, Any]:
    """
    Get aggregate performance metrics for a variant

    Args:
        variant_id: Variant name ('control' or 'slow_hidden_gems')

    Returns:
        Performance metrics dictionary
    """

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

        # Count pacing complaints
        pacing_complaints = {
            "too_fast": 0,
            "too_slow": 0,
            "just_right": 0
        }

        for f in feedbacks:
            if hasattr(f, 'pacing_feedback') and f.pacing_feedback:
                pacing_complaints[f.pacing_feedback] = pacing_complaints.get(f.pacing_feedback, 0) + 1

        # Calculate completion rates (if available)
        completion_estimates = []
        for f in feedbacks:
            if hasattr(f, 'completion_estimate') and f.completion_estimate:
                completion_estimates.append(f.completion_estimate)

        metrics = {
            "overall_rating_avg": round(sum(overall_ratings) / len(overall_ratings), 2) if overall_ratings else 0,
            "overall_rating_stddev": round(_stddev(overall_ratings), 2) if overall_ratings else 0,

            "pacing_rating_avg": round(sum(pacing_ratings) / len(pacing_ratings), 2) if pacing_ratings else 0,
            "authenticity_rating_avg": round(sum(authenticity_ratings) / len(authenticity_ratings), 2) if authenticity_ratings else 0,
            "value_rating_avg": round(sum(value_ratings) / len(value_ratings), 2) if value_ratings else 0,

            "satisfaction_rate": round(len([r for r in overall_ratings if r >= 4]) / len(overall_ratings), 3) if overall_ratings else 0,

            "pacing_complaints": pacing_complaints,
            "pacing_complaint_rate": round(
                (pacing_complaints.get("too_fast", 0) + pacing_complaints.get("too_slow", 0)) / len(feedbacks),
                3
            ) if feedbacks else 0,

            "completion_rate_avg": round(sum(completion_estimates) / len(completion_estimates) / 100, 3) if completion_estimates else 0,

            "recommend_rate": round(
                len([f for f in feedbacks if hasattr(f, 'would_recommend') and f.would_recommend]) / len(feedbacks),
                3
            ) if feedbacks else 0
        }

        return {
            "variant": variant_id,
            "sample_size": len(trips),
            "feedback_count": len(feedbacks),
            "feedback_rate": round(len(feedbacks) / len(trips), 3),
            "metrics": metrics,
            "updated_at": datetime.utcnow().isoformat()
        }

    finally:
        db.close()


def compare_variants(variant_a: str = "control", variant_b: str = "slow_hidden_gems") -> Dict[str, Any]:
    """
    Compare two variants and determine statistical significance

    Args:
        variant_a: First variant name
        variant_b: Second variant name

    Returns:
        Comparison results with winner determination
    """

    perf_a = get_variant_performance(variant_a)
    perf_b = get_variant_performance(variant_b)

    metrics_a = perf_a.get("metrics", {})
    metrics_b = perf_b.get("metrics", {})

    # Calculate deltas
    delta_overall_rating = metrics_b.get("overall_rating_avg", 0) - metrics_a.get("overall_rating_avg", 0)
    delta_pacing_complaint_rate = metrics_b.get("pacing_complaint_rate", 0) - metrics_a.get("pacing_complaint_rate", 0)
    delta_satisfaction_rate = metrics_b.get("satisfaction_rate", 0) - metrics_a.get("satisfaction_rate", 0)

    # Determine winner
    winner = None
    if delta_overall_rating > 0.4 and delta_pacing_complaint_rate < -0.05:  # +10% rating AND -5% complaints
        winner = variant_b
    elif delta_overall_rating < -0.4:
        winner = variant_a
    else:
        winner = "neutral"

    comparison = {
        "variant_a": variant_a,
        "variant_b": variant_b,
        "sample_sizes": {
            "variant_a": perf_a.get("sample_size", 0),
            "variant_b": perf_b.get("sample_size", 0)
        },
        "metrics_a": metrics_a,
        "metrics_b": metrics_b,
        "deltas": {
            "overall_rating": round(delta_overall_rating, 2),
            "pacing_complaint_rate": round(delta_pacing_complaint_rate, 3),
            "satisfaction_rate": round(delta_satisfaction_rate, 3),
            "completion_rate": round(
                metrics_b.get("completion_rate_avg", 0) - metrics_a.get("completion_rate_avg", 0),
                3
            )
        },
        "winner": winner,
        "confidence": _calculate_confidence(perf_a, perf_b),
        "recommendation": _get_recommendation(winner, perf_a, perf_b)
    }

    return comparison


def _stddev(values: list) -> float:
    """Calculate standard deviation"""
    if not values or len(values) < 2:
        return 0
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
    return variance ** 0.5


def _calculate_confidence(perf_a: Dict[str, Any], perf_b: Dict[str, Any]) -> str:
    """
    Calculate statistical confidence level
    Simplified version - in production, use proper t-test
    """

    sample_a = perf_a.get("feedback_count", 0)
    sample_b = perf_b.get("feedback_count", 0)

    if sample_a < 30 or sample_b < 30:
        return "insufficient_data"
    elif sample_a >= 100 and sample_b >= 100:
        return "high"
    elif sample_a >= 50 and sample_b >= 50:
        return "medium"
    else:
        return "low"


def _get_recommendation(winner: str, perf_a: Dict[str, Any], perf_b: Dict[str, Any]) -> str:
    """Generate recommendation based on winner"""

    confidence = _calculate_confidence(perf_a, perf_b)

    if confidence == "insufficient_data":
        return "Continue collecting data before making decision"

    if winner == "neutral":
        return "No clear winner. Consider offering both as user preferences."

    variant_name = winner if winner != "neutral" else "Neither"

    if confidence == "high":
        return f"High confidence: Launch {variant_name} as default"
    elif confidence == "medium":
        return f"Medium confidence: Run extended test before launching {variant_name}"
    else:
        return f"Low confidence: Continue testing {variant_name}"


# Helper functions for experiments dashboard
def get_experiment_status() -> Dict[str, Any]:
    """Get current status of A/B test"""

    control = get_variant_performance("control")
    experimental = get_variant_performance("slow_hidden_gems")
    comparison = compare_variants("control", "slow_hidden_gems")

    return {
        "experiment_name": "Pacing: Control vs Slow Hidden Gems",
        "status": "running" if comparison["confidence"] != "high" else "ready_to_decide",
        "control": control,
        "experimental": experimental,
        "comparison": comparison,
        "updated_at": datetime.utcnow().isoformat()
    }
