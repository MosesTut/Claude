#!/usr/bin/env python3
"""
Timbuktoo Travel Concierge - Main Entry Point
"""

import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

from timbuktoo.workflows.orchestrator import TravelOrchestrator
from timbuktoo.utils.logger import get_logger
from timbuktoo.utils.monitoring import get_metrics_collector

# Load environment
load_dotenv()

logger = get_logger(__name__)


def example_trip():
    """Example trip creation"""

    # User preferences
    preferences = {
        "vibes": ["local", "food", "nightlife"],
        "interests": ["food", "drink", "culture", "nature"],
        "budget_level": "mid"
    }

    # Travel dates (7 days from now)
    start_date = datetime.now() + timedelta(days=30)
    end_date = start_date + timedelta(days=6)

    travel_dates = {
        "start": start_date.strftime("%Y-%m-%d"),
        "end": end_date.strftime("%Y-%m-%d")
    }

    # Candidate cities (optional - will use all cities if not provided)
    candidate_cities = [
        {
            "city_id": "placeholder",
            "name": "Lisbon",
            "country": "Portugal"
        },
        {
            "city_id": "placeholder",
            "name": "Barcelona",
            "country": "Spain"
        },
        {
            "city_id": "placeholder",
            "name": "Mexico City",
            "country": "Mexico"
        }
    ]

    # Create trip using A/B test variant
    variant = "control"  # or "slow_hidden_gems"

    logger.info("Creating trip with Timbuktoo Travel Concierge")
    logger.info(f"Preferences: {preferences}")
    logger.info(f"Dates: {travel_dates}")
    logger.info(f"Variant: {variant}")

    # Initialize orchestrator
    orchestrator = TravelOrchestrator(variant=variant)

    # Create trip
    result = orchestrator.create_trip(
        preferences=preferences,
        travel_dates=travel_dates,
        candidate_cities=candidate_cities,
        user_id=None  # Anonymous user
    )

    # Print results
    if result["success"]:
        logger.info("Trip created successfully!")
        print("\n" + "="*80)
        print("TIMBUKTOO TRAVEL CONCIERGE - YOUR PERSONALIZED ITINERARY")
        print("="*80)

        print(f"\nSelected City: {result['selected_city']['name']}, {result['selected_city']['country']}")
        print(f"Trip ID: {result['trip_id']}")
        print(f"\nReasoning: {result['selected_city'].get('reasoning', 'N/A')}")

        print("\n" + "-"*80)
        print("7-DAY ITINERARY")
        print("-"*80)

        itinerary = result["itinerary"]
        for day in itinerary.get("daily_itineraries", []):
            print(f"\nDay {day['day']} - {day['date']} - {day['theme']}")
            print(f"Weather: {day.get('weather', {}).get('conditions', 'N/A')}")
            print(f"Daily Budget: ${day.get('daily_budget_usd', 0)}")

            for activity in day.get("schedule", [])[:3]:  # Show first 3 activities
                print(f"  • {activity['time']} - {activity['activity']}")
                print(f"    {activity.get('details', '')[:100]}...")

        print("\n" + "-"*80)
        print("COST SUMMARY")
        print("-"*80)
        cost_summary = result["cost_summary"]
        print(f"Total API Cost: ${cost_summary['total_cost_usd']:.4f}")
        print(f"Budget Utilized: {cost_summary['budget_utilized_pct']:.1f}%")
        print(f"Processing Time: {result['processing_time_seconds']}s")

        print("\nAgent Breakdown:")
        for agent, cost in cost_summary['agent_breakdown'].items():
            print(f"  {agent}: ${cost:.4f}")

        print("\n" + "="*80)

    else:
        logger.error("Trip creation failed!")
        print(f"Error: {result.get('error', 'Unknown error')}")

    return result


def main():
    """Main function"""

    # Start monitoring
    metrics = get_metrics_collector()
    metrics.start()

    # Run example
    result = example_trip()

    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
