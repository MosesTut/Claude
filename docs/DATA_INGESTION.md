# Data Ingestion Checklist & Vector Schema

Complete operational blueprint for ingesting open-source travel data into Timbuktoo.

---

## 1. Data Ingestion Checklist (Operational & Repeatable)

### A. Source Qualification Checklist

Before ingesting any dataset, verify:

#### Legal & Licensing
- [ ] **License verified** and compatible
  - ✅ CC0 (Public Domain)
  - ✅ CC-BY (Attribution required)
  - ✅ ODbL (OpenStreetMap)
  - ✅ Government Public Domain
  - ❌ All Rights Reserved
  - ❌ Non-commercial only

#### Update Cadence
- [ ] **Update frequency known**
  - Static (once only)
  - Daily (weather, events)
  - Weekly (OSM, reviews)
  - Monthly (cost indices)
  - Quarterly (museums, attractions)
  - Annual (festivals, seasons)

#### Geographic Scope
- [ ] **Scope tagged**
  - Global (GeoNames, World Bank)
  - Country-specific (GTFS feeds)
  - City-specific (municipal data)
  - Neighborhood-level (OSM POIs)

#### Data Type Classification
- [ ] **Type classified**
  - **Structured**: Tables, CSV, JSON (→ PostgreSQL)
  - **Semi-structured**: API responses (→ normalize first)
  - **Unstructured**: Text, guides (→ chunk + embed)

#### Trust Tier Assignment
- [ ] **Trust tier assigned**
  - **Tier 5**: Government/institutional (NOAA, CDC, UNESCO)
  - **Tier 4**: Community-curated verified (OSM verified, Wikidata sourced)
  - **Tier 3**: Community-curated unverified (Wikipedia, OSM unverified)
  - **Tier 2**: Crowd-sourced (Numbeo, reviews)
  - **Tier 1**: Experimental (scraped, beta APIs)

---

### B. Ingestion Pipeline Checklist

#### 1. Raw Intake
- [ ] Store raw files in **immutable storage**
  - Location: `s3://timbuktoo-raw-data/{source}/{date}/`
  - Format: Original format preserved
- [ ] Preserve **original schema & timestamps**
  - Include: `ingested_at`, `source_version`
- [ ] Log **source metadata**
  - URL, license, version, download date
  - Store in `data_sources` table

```python
# Example metadata logging
source_metadata = {
    "source_id": "osm-lisbon-bars",
    "source_name": "OpenStreetMap",
    "source_url": "overpass-api.de",
    "license": "ODbL",
    "version": "2024-01-17",
    "ingested_at": "2024-01-17T10:30:00Z",
    "raw_file_path": "s3://timbuktoo-raw-data/osm/2024-01-17/lisbon-bars.json"
}
```

#### 2. Normalization
- [ ] **Standardize place names**
  - Use GeoNames ID as canonical
  - Cross-reference with OSM node IDs
  - Store aliases in `place_aliases` table

- [ ] **Standardize dates**
  - Format: ISO-8601 (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SSZ`)
  - Store timezone separately

- [ ] **Standardize currency**
  - Convert to USD baseline
  - Store original currency + exchange rate
  - Date exchange rate applied

- [ ] **De-duplicate entities**
  - Match on: name + coordinates (within 50m)
  - Merge metadata from multiple sources
  - Keep highest trust tier source as primary

- [ ] **Resolve aliases**
  - "NYC" → "New York City"
  - "El Born" → "El Born, Barcelona, Spain"
  - Store in normalized form

```python
# Example normalization
{
    "canonical_name": "New York City",
    "aliases": ["NYC", "New York", "The Big Apple"],
    "geonames_id": 5128581,
    "osm_relation_id": 175905
}
```

#### 3. Enrichment
- [ ] **Add geo-coordinates**
  - Latitude, longitude (WGS84)
  - Source: GeoNames or OSM
  - Accuracy: ±10m for POIs

- [ ] **Add tags**
  - `food_type`: ["tapas", "seafood", "fine-dining"]
  - `activity_type`: ["hiking", "museum", "bar-hopping"]
  - `vibe`: ["luxury", "local", "nightlife", "nature", "historic"]
  - `alcohol_focus`: ["beer", "wine", "cocktails", "tequila"]

- [ ] **Attach seasonality markers**
  - `best_seasons`: ["spring", "summer", "fall", "winter"]
  - `avoid_seasons`: ["monsoon", "extreme-heat"]

- [ ] **Attach price tier** (relative, not absolute)
  - `low`: $0-25/person
  - `mid`: $25-75/person
  - `high`: $75-150/person
  - `luxury`: $150+/person

```python
# Example enrichment
{
    "entity_id": "uuid",
    "name": "Cal Pep",
    "tags": ["food", "tapas", "seafood", "local"],
    "vibe": ["authentic", "buzzy"],
    "price_tier": "mid-high",
    "alcohol_focus": ["beer", "wine"],
    "seasonality": ["spring", "summer", "fall", "winter"],
    "geo": {"lat": 41.3851, "lon": 2.1802},
    "trust_tier": 4
}
```

#### 4. Chunking (for embeddings)
- [ ] **Chunk size**: 300-600 tokens
- [ ] **Scope**: City + neighborhood scoped
- [ ] **Granularity**: One concept per chunk
  - ✅ "Cal Pep is a tapas bar known for..."
  - ❌ "Barcelona has many restaurants. Cal Pep is one..."

- [ ] **Metadata injection**
  - Include: city, neighborhood, type, tags in chunk
  - Format: `[CITY: Barcelona] [TYPE: Restaurant] Cal Pep is a legendary...`

```python
# Example chunking
chunk = {
    "chunk_id": "uuid",
    "entity_id": "cal-pep-uuid",
    "content": "[Barcelona, El Born] [Restaurant, Tapas] Cal Pep is a legendary tapas bar known for fresh seafood and buzzy atmosphere. Locals recommend the garlic shrimp and percebes. No reservations, arrive early. Mid-high price range.",
    "tokens": 45,
    "metadata": {
        "city": "Barcelona",
        "neighborhood": "El Born",
        "entity_type": "restaurant",
        "tags": ["tapas", "seafood", "local"]
    }
}
```

#### 5. Embedding & Storage
- [ ] **Generate vector embeddings**
  - Model: `sentence-transformers/all-MiniLM-L6-v2` (default)
  - Or: `text-embedding-ada-002` (OpenAI)
  - Dimension: 384 (MiniLM) or 1536 (Ada)

- [ ] **Store in vector DB**
  - ChromaDB collection per city
  - Or: Tenant-specific namespaces
  - Index by: city, entity_type, tags

- [ ] **Store metadata in parallel relational store**
  - PostgreSQL `entities` table
  - Includes: name, type, price, coordinates, trust_tier

- [ ] **Link vector IDs ↔ canonical entity IDs**
  - `vectors` table: `vector_id, entity_id, embedding`
  - Enables: Update entity metadata without re-embedding

```python
# Example storage
from timbuktoo.database.vector_db import get_vector_db
from timbuktoo.database.models import Entity, SessionLocal

# Store in relational DB
db = SessionLocal()
entity = Entity(
    entity_id=entity_id,
    city_id=city_id,
    name="Cal Pep",
    entity_type="restaurant",
    price_tier="mid-high",
    # ... other fields
)
db.add(entity)
db.commit()

# Store in vector DB
vector_db = get_vector_db()
vector_id = vector_db.add_entity(
    entity_id=str(entity_id),
    city_id=str(city_id),
    entity_type="restaurant",
    title="Cal Pep",
    content=chunk_content,
    tags=["tapas", "seafood"],
    vibe=["authentic", "local"],
    price_tier="mid-high",
    geo_lat=41.3851,
    geo_lon=2.1802,
    trust_tier=4
)
```

#### 6. Validation
- [ ] **Sample QA per city**
  - Test queries: "Best tequila bars in Mexico City"
  - Verify: Top 3 results are relevant
  - Check: No duplicates in top 10

- [ ] **Hallucination check**
  - All facts must trace to source
  - Flag: Unverified claims
  - Require: Citations for tier 1-2 sources

- [ ] **Temporal relevance flagging**
  - Flag: Data >6 months old (for dynamic data)
  - Warning: Data >12 months old
  - Archive: Data >24 months old

```python
# Example validation
def validate_ingestion(city_id, sample_size=10):
    results = {
        "total_entities": 0,
        "by_type": {},
        "by_trust_tier": {},
        "outdated_count": 0,
        "duplicate_count": 0
    }

    # Count entities
    entities = db.query(Entity).filter(Entity.city_id == city_id).all()
    results["total_entities"] = len(entities)

    # Group by type
    for entity in entities:
        results["by_type"][entity.entity_type] = results["by_type"].get(entity.entity_type, 0) + 1
        results["by_trust_tier"][entity.trust_tier] = results["by_trust_tier"].get(entity.trust_tier, 0) + 1

    return results
```

---

### C. Update Strategy

| Data Type | Refresh Frequency | Method |
|-----------|-------------------|--------|
| **Static knowledge** | Quarterly | Batch re-ingestion |
| **Events & weather** | Real-time | Tool-based API calls |
| **Cost indices** | Monthly | API fetch + merge |
| **Restaurants/venues** | Quarterly | Re-scrape + validate with tools |
| **Museums/attractions** | Annually | Manual curation |

```python
# Example update scheduler
from schedule import every, run_pending
import time

def update_weather():
    """Update weather data daily"""
    # Fetch latest forecasts
    pass

def update_events():
    """Update events data daily"""
    # Fetch upcoming events
    pass

def update_costs():
    """Update cost indices monthly"""
    # Fetch latest price data
    pass

# Schedule updates
every().day.at("02:00").do(update_weather)
every().day.at("03:00").do(update_events)
every().month.at("01:00").do(update_costs)

while True:
    run_pending()
    time.sleep(3600)
```

---

## 2. Vector Schema for City Knowledge (RAG-Optimized)

### A. Core Vector Object

```json
{
  "vector_id": "550e8400-e29b-41d4-a716-446655440000",
  "city": "Barcelona",
  "country": "Spain",
  "neighborhood": "El Born",
  "entity_type": "restaurant",
  "title": "Cal Pep",
  "content": "Cal Pep is a legendary tapas bar in El Born, Barcelona, known for exceptional fresh seafood and a buzzy, authentic atmosphere. Locals recommend the garlic shrimp, percebes (goose barnacles), and cava. No reservations accepted - arrive early or expect a wait. Perfect for beer and seafood lovers seeking authentic Catalan experience.",
  "tags": [
    "food",
    "tapas",
    "local",
    "beer",
    "seafood",
    "catalan"
  ],
  "vibe": [
    "authentic",
    "buzzy",
    "high-energy",
    "local-favorite"
  ],
  "price_tier": "mid-high",
  "seasonality": ["spring", "summer", "fall", "winter"],
  "time_of_day": ["lunch", "dinner"],
  "duration_minutes": 90,
  "geo": {
    "lat": 41.3851,
    "lon": 2.1802
  },
  "trust_tier": 4,
  "source": "openstreetmap+wikidata",
  "last_verified": "2024-09-01"
}
```

### B. Specialized Extensions

#### Events
```json
{
  "entity_type": "event",
  "start_date": "2024-09-15",
  "end_date": "2024-09-22",
  "recurrence": "annual",
  "event_category": "festival",
  "tickets_required": true,
  "booking_url": "https://example.com"
}
```

#### Nature / Outdoor
```json
{
  "entity_type": "nature",
  "difficulty": "moderate",
  "elevation_gain_m": 350,
  "distance_km": 8.5,
  "gear_required": ["hiking shoes", "water", "sun protection"],
  "weather_dependency": true,
  "best_months": ["april", "may", "september", "october"]
}
```

#### Dining / Bars
```json
{
  "entity_type": "restaurant",
  "alcohol_focus": ["craft beer", "wine"],
  "cuisine_type": "Catalan",
  "reservation_required": false,
  "dress_code": "casual",
  "dietary_options": ["vegetarian", "gluten-free"],
  "payment_methods": ["cash", "card"]
}
```

#### Museums / Cultural
```json
{
  "entity_type": "museum",
  "collection_focus": ["modern art", "catalan art"],
  "audio_guide_available": true,
  "languages": ["english", "spanish", "catalan"],
  "admission_price_usd": 15,
  "free_hours": "sundays 15:00-20:00"
}
```

### C. Indexing Strategy

#### Primary Index
- **city + entity_type**
  - Fast filtering: "All restaurants in Barcelona"

#### Secondary Index
- **tags + vibe**
  - Semantic search: "Local authentic tapas bars"

#### Tertiary Index
- **seasonality + price_tier**
  - Budget + timing: "Mid-range restaurants open in winter"

### D. Query Examples

```python
# Query 1: Best tequila bars in Mexico City
results = vector_db.search(
    query="authentic tequila mezcal bars local experience",
    city_id=mexico_city_id,
    entity_type="bar",
    vibes=["local", "authentic"],
    n_results=10
)

# Query 2: Luxury dinner near historic center
results = vector_db.search(
    query="fine dining luxury restaurant historic",
    city_id=barcelona_id,
    entity_type="restaurant",
    price_tiers=["high", "luxury"],
    n_results=5
)

# Query 3: Nature hikes for spring
results = vector_db.search(
    query="hiking trails nature outdoor views",
    city_id=lisbon_id,
    entity_type="nature",
    seasonality=["spring"],
    n_results=10
)
```

---

## 3. Implementation Scripts

### A. Ingest OpenStreetMap Data

```bash
#!/bin/bash
# scripts/ingest_osm.sh

CITY=$1
BBOX=$2  # "min_lon,min_lat,max_lon,max_lat"

python << EOF
from timbuktoo.utils.data_ingestion import OSMIngester

ingester = OSMIngester()
ingester.ingest_city(
    city="$CITY",
    bbox="$BBOX",
    entity_types=["bar", "restaurant", "cafe", "museum", "park"]
)
EOF
```

### B. Ingest Wikidata

```bash
#!/bin/bash
# scripts/ingest_wikidata.sh

CITY=$1

python << EOF
from timbuktoo.utils.data_ingestion import WikidataIngester

ingester = WikidataIngester()
ingester.ingest_city(
    city="$CITY",
    entity_types=["museum", "restaurant", "hotel", "landmark"]
)
EOF
```

### C. Ingest Weather History

```bash
#!/bin/bash
# scripts/ingest_weather.sh

CITY=$1
LAT=$2
LON=$3

python << EOF
from timbuktoo.utils.data_ingestion import WeatherIngester

ingester = WeatherIngester()
ingester.ingest_historical_weather(
    city="$CITY",
    latitude=$LAT,
    longitude=$LON,
    years=3  # Last 3 years
)
EOF
```

---

## 4. Data Quality Monitoring

### Metrics to Track

```python
# Data coverage per city
SELECT
    city_id,
    entity_type,
    COUNT(*) as count,
    AVG(trust_tier) as avg_trust,
    MAX(last_verified) as most_recent_verification,
    COUNT(CASE WHEN last_verified < NOW() - INTERVAL '6 months' THEN 1 END) as outdated_count
FROM entities
GROUP BY city_id, entity_type;

# Vector DB stats
stats = vector_db.get_stats()
# {
#   "total_vectors": 5432,
#   "by_city": {"Barcelona": 1234, "Lisbon": 987, ...},
#   "by_type": {"restaurant": 2156, "bar": 843, ...}
# }
```

### Quality Alerts

- ⚠️ City with <100 entities
- ⚠️ Entity type with avg trust_tier <3
- ⚠️ >20% of entities outdated (>6 months)
- ⚠️ Duplicate entities detected

---

## 5. Next Steps

1. **Implement ingestion scripts** for 5 pilot cities
2. **Set up automated update schedule**
3. **Monitor data quality metrics**
4. **Expand to 20+ cities** over Q1
5. **Build data quality dashboard**

---

## Questions?

For data ingestion questions:
- Email: data@timbuktoo.ai
- Slack: #data-engineering
