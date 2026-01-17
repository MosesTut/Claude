#!/usr/bin/env python3
"""Load pilot city data into the database"""

import json
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from timbuktoo.database.models import City, Entity, SessionLocal
from timbuktoo.database.vector_db import get_vector_db
from timbuktoo.utils.logger import get_logger

logger = get_logger(__name__)


def load_cities(cities_file: str):
    """Load cities from JSON file"""
    logger.info(f"Loading cities from {cities_file}")

    with open(cities_file, 'r') as f:
        cities_data = json.load(f)

    db = SessionLocal()
    loaded_cities = []

    try:
        for city_data in cities_data:
            # Check if city already exists
            existing = db.query(City).filter(
                City.name == city_data['name'],
                City.country == city_data['country']
            ).first()

            if existing:
                logger.info(f"City {city_data['name']} already exists, skipping")
                loaded_cities.append(existing)
                continue

            city = City(**city_data)
            db.add(city)
            loaded_cities.append(city)
            logger.info(f"Added city: {city_data['name']}, {city_data['country']}")

        db.commit()
        logger.info(f"Loaded {len(loaded_cities)} cities")

        return loaded_cities

    except Exception as e:
        logger.error(f"Failed to load cities: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


def load_entities(entities_file: str, city_name: str, city_country: str):
    """Load entities for a city from JSON file"""
    logger.info(f"Loading entities from {entities_file}")

    with open(entities_file, 'r') as f:
        entities_data = json.load(f)

    db = SessionLocal()
    vector_db = get_vector_db()

    try:
        # Find city
        city = db.query(City).filter(
            City.name == city_name,
            City.country == city_country
        ).first()

        if not city:
            logger.error(f"City {city_name}, {city_country} not found")
            return

        loaded_count = 0

        for entity_data in entities_data:
            # Check if entity already exists
            existing = db.query(Entity).filter(
                Entity.city_id == city.city_id,
                Entity.name == entity_data['name']
            ).first()

            if existing:
                logger.info(f"Entity {entity_data['name']} already exists, skipping")
                continue

            # Create entity
            entity = Entity(
                city_id=city.city_id,
                **entity_data
            )
            db.add(entity)
            db.flush()  # Get entity_id

            # Create vector embedding
            content = f"{entity_data['name']}\n{entity_data['description']}"
            title = entity_data['name']

            vector_id = vector_db.add_entity(
                entity_id=str(entity.entity_id),
                city_id=str(city.city_id),
                entity_type=entity_data['entity_type'],
                title=title,
                content=content,
                tags=[entity_data['entity_type']],
                vibe=entity_data.get('vibes', []),
                price_tier=entity_data.get('price_tier'),
                seasonality=entity_data.get('seasonality'),
                time_of_day=entity_data.get('best_time_of_day'),
                duration_minutes=entity_data.get('average_duration_minutes'),
                trust_tier=entity_data.get('trust_tier', 1),
                source=entity_data.get('source', 'pilot_data')
            )

            loaded_count += 1
            logger.info(f"Added entity: {entity_data['name']} (vector_id: {vector_id})")

        db.commit()
        logger.info(f"Loaded {loaded_count} entities for {city_name}")

    except Exception as e:
        logger.error(f"Failed to load entities: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


def main():
    """Main function"""
    logger.info("Starting pilot data load")

    # Get data directory
    data_dir = Path(__file__).parent.parent / "timbuktoo" / "data" / "pilot_cities"

    # Load cities
    cities_file = data_dir / "cities.json"
    cities = load_cities(str(cities_file))

    # Load Lisbon entities
    lisbon_file = data_dir / "lisbon_entities.json"
    if lisbon_file.exists():
        load_entities(str(lisbon_file), "Lisbon", "Portugal")

    logger.info("Pilot data load completed successfully!")

    # Print summary
    vector_db = get_vector_db()
    stats = vector_db.get_stats()
    logger.info(f"Vector DB stats: {stats}")


if __name__ == "__main__":
    main()
