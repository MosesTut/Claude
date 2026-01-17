# Open-Source Data Sources for Timbuktoo

Complete guide to open-source databases, data feeds, and public datasets that can be ingested into Timbuktoo's knowledge base to create a best-in-class Travel Concierge Agent.

---

## 1. Core Foundational Datasets (All Agents)

These form the backbone of geographic, cultural, and structural knowledge.

### 🌍 Geographic & Places

#### OpenStreetMap (OSM)
- **What**: POIs, roads, parks, landmarks, neighborhoods
- **Enables**: Walkability analysis, proximity reasoning, hidden gems discovery
- **How to Use**:
  - Extract via Overpass API or planet dumps
  - Store as vector embeddings for semantic place lookup
  - Query for restaurants, bars, parks by coordinates
- **Integration**:
  ```python
  # Query OSM for bars in Lisbon
  overpass_query = """
  [out:json];
  area[name="Lisboa"]->.a;
  (
    node["amenity"="bar"](area.a);
    way["amenity"="bar"](area.a);
  );
  out body;
  """
  ```
- **Vector Schema**: Chunk POI descriptions → embed → store with geo coords

#### GeoNames
- **What**: Cities, regions, elevations, alternate place names
- **Enables**: Destination disambiguation, routing logic
- **How to Use**:
  - Download country-specific dumps
  - Load into PostgreSQL with PostGIS extension
  - Use for city metadata enrichment
- **Integration**:
  ```sql
  CREATE TABLE geonames (
    geonameid INT PRIMARY KEY,
    name TEXT,
    asciiname TEXT,
    alternatenames TEXT,
    latitude DECIMAL,
    longitude DECIMAL,
    country_code CHAR(2),
    population BIGINT
  );
  ```

---

## 2. City Selection Agent – Data Inputs

Used to rank destinations dynamically.

### 🌤 Weather & Seasonality

#### NOAA Global Surface Summary
- **What**: Historical weather patterns, temperature, precipitation
- **Enables**: Best months to visit, rain/heat avoidance
- **How to Use**:
  - Download via NOAA API or FTP
  - Aggregate monthly averages per city
  - Feed into City Selection Agent scoring
- **Integration**:
  ```python
  # Load NOAA data
  import pandas as pd
  df = pd.read_csv('noaa_summary.csv')
  monthly_avg = df.groupby(['city', 'month'])['temp'].mean()
  ```

#### ECMWF Open Climate Data
- **What**: Long-term climate projections
- **Enables**: Seasonal recommendations
- **Integration**: API calls for climate zones

#### Meteostat
- **What**: Historical weather database (open)
- **Enables**: "This time last year" comparisons
- **How to Use**: Python library `meteostat`
  ```python
  from meteostat import Point, Daily
  from datetime import datetime

  # Lisbon weather last June
  location = Point(38.7223, -9.1393)
  data = Daily(location, datetime(2023, 6, 1), datetime(2023, 6, 30))
  ```

### 🎉 Events & Festivals

#### Eventbrite Open Data
- **What**: Public events API (limited but usable)
- **Enables**: Event-driven travel recommendations
- **Integration**: REST API with OAuth

#### Municipal Open Data Portals
- **Examples**:
  - NYC Open Data: `data.cityofnewyork.us`
  - Barcelona Open Data: `opendata-ajuntament.barcelona.cat`
  - Tokyo Open Data: `portal.data.metro.tokyo.lg.jp`
- **What**: City-run events calendars, permits, festivals
- **How to Use**: Download CSV/JSON, load into `events` table

#### Wikidata Events & Festivals
- **What**: Structured festival data
- **SPARQL Query**:
  ```sparql
  SELECT ?festival ?festivalLabel ?location ?date WHERE {
    ?festival wdt:P31 wd:Q132241 .  # instance of festival
    ?festival wdt:P276 ?location .  # location
    ?festival wdt:P585 ?date .      # point in time
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
  }
  ```

### 💸 Cost & Affordability

#### World Bank Open Data
- **What**: Economic indicators, GDP per capita
- **Enables**: Budget-aware destination ranking
- **API**: `api.worldbank.org/v2/country/{code}/indicator/NY.GDP.PCAP.CD`

#### OECD Cost of Living Indices
- **What**: Comparative price levels
- **Enables**: Daily cost estimates
- **Integration**: Download Excel files, parse into cost database

#### Numbeo Public Datasets
- **What**: Crowd-sourced cost of living data
- **Enables**: Meal prices, beer prices, hotel estimates
- **Note**: Use scraped summaries only (API not free)

---

## 3. Local Expert Agent – Deep City Intelligence

Used to surface authentic, non-touristy insights.

### 🍽 Food, Coffee, Bars

#### Open Food Facts
- **What**: Food products database with local specialties
- **Enables**: Identify regional ingredients, dishes
- **API**: `world.openfoodfacts.org/api/v0/product/{barcode}.json`

#### Wikidata → Restaurants, Breweries, Cafes
- **SPARQL Example**:
  ```sparql
  SELECT ?place ?placeLabel ?typeLabel ?coords WHERE {
    ?place wdt:P31/wdt:P279* wd:Q11707 .  # restaurant
    ?place wdt:P131 wd:Q597 .             # located in Lisbon
    ?place wdt:P625 ?coords .             # coordinates
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
  }
  ```

#### Municipal Business License Datasets
- **What**: Official registries of bars, restaurants
- **Enables**: Identify authentic local spots
- **Example**: San Francisco permits, NYC restaurant inspections

### 🏞 Nature & Outdoor Experiences

#### US National Park Service Open Data
- **What**: Parks, trails, visitor centers
- **API**: `developer.nps.gov/api/v1/parks`
- **Enables**: Day hikes, scenic drives

#### Protected Planet (WDPA)
- **What**: Global protected areas database
- **Enables**: Nature reserves, national parks worldwide
- **Download**: `protectedplanet.net/en/thematic-areas/wdpa`

#### AllTrails Open GPX Repositories
- **What**: Trail GPS data (some open)
- **Enables**: Hiking route recommendations

### 🏛 Museums & Historic Sites

#### Europeana
- **What**: EU cultural heritage aggregator
- **API**: `api.europeana.eu`
- **Enables**: Museum collections, historical narratives

#### Smithsonian Open Access
- **What**: 3M+ images and metadata
- **Enables**: Visual cultural context

#### UNESCO World Heritage Dataset
- **What**: All World Heritage Sites
- **Download**: `whc.unesco.org/en/list/`
- **Enables**: Must-see vs optional ranking

---

## 4. Travel Concierge Agent – Itinerary & Logistics

Used for day-by-day planning realism.

### 🏨 Lodging (Open Alternatives)

#### OpenHotelData
- **What**: Hotel listings (limited coverage)
- **Note**: Not comprehensive, supplement with Wikidata

#### Wikidata → Hotels, Boutique Stays
- **SPARQL**: Query for `P31=Q27686` (hotel)

#### Tourism Board Accommodation Registries
- **Examples**: Spain tourism registry, Portugal Turismo

### 🚇 Transportation

#### GTFS Feeds (Public Transit Worldwide)
- **What**: Schedules, routes, stops for buses, metros, trains
- **Examples**:
  - NYC MTA: `transitfeeds.com`
  - Lisbon: `carris.pt/gtfs`
  - Tokyo: `developer-tokyochallenge.odpt.org`
- **Enables**: Transit-aware daily schedules
- **Integration**:
  ```python
  import gtfs_kit as gk
  feed = gk.read_gtfs('lisbon.zip', dist_units='km')
  ```

#### OpenFlights Routes Dataset
- **What**: Airports, airlines, routes
- **Download**: `openflights.org/data.html`
- **Enables**: Flight routing, airport codes

#### OSM Routing Graphs
- **What**: Road network for driving/walking
- **Tools**: OSRM, GraphHopper, Valhalla
- **Enables**: Realistic travel times between POIs

### 🧳 Packing & Climate Logic

#### Weather History + Wikidata Seasonal Norms
- **What**: Combine historical weather with cultural dress codes
- **Enables**: "Pack layers, rain jacket, comfortable shoes"

#### Cultural Norms Datasets
- **Sources**:
  - Wikidata customs (`P2541`)
  - Wikipedia cultural pages
- **Enables**: Tipping customs, dress codes

---

## 5. Legal, Safety & Practical Intelligence

### 🛂 Visas & Entry

#### IATA Timatic (Reference Summaries Only)
- **What**: Visa requirements by nationality
- **Note**: Not fully open, use government sources

#### Government Immigration Open Datasets
- **Examples**:
  - US State Dept travel advisories
  - EU Schengen info
- **Enables**: Entry requirements by passport

### 🚨 Safety & Health

#### CDC Travel Health Notices
- **API**: `wwwnc.cdc.gov/travel`
- **Enables**: Health recommendations, vaccine requirements

#### WHO Open Data
- **What**: Disease outbreaks, health statistics
- **Enables**: Travel health advisories

#### UNODC Crime Statistics
- **What**: Crime rates by country/city
- **Note**: High-level only, not neighborhood-specific
- **Enables**: Safety scoring

---

## 6. Knowledge Base Structure

### Recommended Architecture

```
timbuktoo_knowledge/
├── geography/
│   ├── osm_places.parquet
│   ├── geonames.sql
│   └── coordinates.index
├── cities/
│   ├── culture/
│   │   ├── museums_wikidata.json
│   │   ├── festivals_events.csv
│   │   └── historical_narratives.md
│   ├── food_drink/
│   │   ├── restaurants_osm.json
│   │   ├── bars_nightlife.json
│   │   ├── coffee_roasters.csv
│   │   └── local_specialties.txt
│   ├── nature/
│   │   ├── parks_trails.gpx
│   │   ├── protected_areas.geojson
│   │   └── beaches_viewpoints.json
│   ├── nightlife/
│   │   ├── bars_clubs.json
│   │   └── event_calendars.ics
│   ├── events/
│   │   ├── festivals.csv
│   │   └── concerts_sports.json
│   └── logistics/
│       ├── gtfs_feeds/
│       ├── hotels.json
│       └── airports_routes.csv
├── seasonal_patterns/
│   ├── noaa_weather.parquet
│   ├── meteostat_history.db
│   └── best_months.json
├── cost_indices/
│   ├── worldbank.csv
│   ├── oecd_prices.xlsx
│   └── numbeo_summary.json
└── safety_health/
    ├── cdc_notices.json
    ├── travel_advisories.xml
    └── crime_stats.csv
```

### Ingestion Strategy

| Data Type | Storage | Processing |
|-----------|---------|------------|
| Structured data (hotels, restaurants) | PostgreSQL with PostGIS | Direct SQL queries |
| Narrative content (history, culture) | Chunked → Vector DB | Semantic embeddings |
| Time-sensitive (weather, events) | API calls (cached) | Real-time tools |
| Static context (festivals, customs) | Knowledge base | Pre-loaded memory |

---

## 7. What This Enables Timbuktoo to Do

With these datasets, Timbuktoo can:

✅ **Hyper-Personalized Recommendations**
- "You like tequila? Here are 3 hidden mezcal bars in Mexico City"
- "Beer lover? Lisbon has 12 craft breweries. Here's the walking route."

✅ **Authentic Local Experiences**
- Recommend neighborhood markets over tourist traps
- Suggest where locals actually eat

✅ **Weather-Aware Planning**
- "It rains afternoons in June. Schedule indoor activities then."
- "Perfect cherry blossom timing in Tokyo, April 5-12."

✅ **Event-Driven Itineraries**
- "Wine festival in Barcelona this week. Add it to Day 3."
- "Avoid this weekend—marathon closes half the city."

✅ **Realistic Logistics**
- "Metro from hotel to museum: 12 minutes, every 5 min"
- "Walk from lunch to park: 800m, 10 min"

✅ **Cultural Context**
- "This cathedral was built in 1147 during the Reconquista..."
- "Locals eat dinner at 10pm, not 6pm"

✅ **Budget Accuracy**
- "Fancy restaurant: $80/person. Local tavern: $25/person"
- "Daily budget: $150 (mid-tier) vs $300 (luxury)"

---

## 8. Integration Examples

### Example 1: Load OSM Bars into Vector DB

```python
from timbuktoo.database.vector_db import get_vector_db
import overpy

# Query OSM
api = overpy.Overpass()
result = api.query("""
  area[name="Lisboa"]->.a;
  node["amenity"="bar"](area.a);
  out body;
""")

# Add to vector DB
vector_db = get_vector_db()

for node in result.nodes:
    content = f"{node.tags.get('name', 'Bar')} - {node.tags.get('description', 'Local bar in Lisbon')}"

    vector_db.add_entity(
        entity_id=str(node.id),
        city_id=lisbon_city_id,
        entity_type="bar",
        title=node.tags.get('name', 'Bar'),
        content=content,
        vibe=["local", "nightlife"],
        price_tier="mid",
        geo_lat=float(node.lat),
        geo_lon=float(node.lon),
        source="OpenStreetMap",
        trust_tier=4
    )
```

### Example 2: Enrich with Weather Data

```python
from meteostat import Point, Daily
from datetime import datetime

# Get historical weather for Lisbon in June
location = Point(38.7223, -9.1393)
data = Daily(location, datetime(2023, 6, 1), datetime(2023, 6, 30))
data = data.fetch()

# Store in city metadata
weather_summary = {
    "avg_temp_c": data['tavg'].mean(),
    "avg_precip_mm": data['prcp'].sum(),
    "rainy_days": (data['prcp'] > 0).sum(),
    "recommendation": "Excellent weather, pack light layers"
}
```

### Example 3: Load GTFS Transit Data

```python
import gtfs_kit as gk

# Load Lisbon GTFS feed
feed = gk.read_gtfs('lisbon_gtfs.zip', dist_units='km')

# Get routes
routes = feed.routes[['route_id', 'route_short_name', 'route_type']]

# Get stops near coordinates
stops_nearby = feed.stops[
    (feed.stops['stop_lat'].between(38.70, 38.75)) &
    (feed.stops['stop_lon'].between(-9.20, -9.10))
]

# Store in logistics database
# Use for "How to get from A to B" queries
```

---

## 9. Phased Ingestion Plan

### Phase 1: Core Cities (Weeks 1-2)
- [ ] OpenStreetMap → 5 pilot cities
- [ ] GeoNames → City metadata
- [ ] Wikidata → Museums, restaurants
- [ ] Weather history → NOAA/Meteostat

### Phase 2: Events & Costs (Weeks 3-4)
- [ ] Municipal event calendars
- [ ] World Bank cost indices
- [ ] OECD pricing data
- [ ] Numbeo summaries

### Phase 3: Deep Intelligence (Weeks 5-6)
- [ ] Protected areas → Nature spots
- [ ] GTFS feeds → Transit data
- [ ] Cultural narratives → Wikipedia dumps
- [ ] Safety data → CDC, WHO

### Phase 4: Continuous Updates (Ongoing)
- [ ] Weekly event refreshes
- [ ] Monthly weather updates
- [ ] Quarterly cost adjustments
- [ ] Annual dataset re-ingestion

---

## 10. Data Quality & Trust Tiers

Assign trust tiers to sources:

| Tier | Source Type | Examples |
|------|-------------|----------|
| 5 | Official govt data | NOAA, CDC, UNESCO |
| 4 | Verified open data | OSM (verified), Wikidata (referenced) |
| 3 | Community curated | OSM (unverified), Wikipedia |
| 2 | Crowd-sourced | Numbeo, user reviews |
| 1 | Experimental | Scraped data, beta APIs |

**Usage in RAG**: Filter vector search by `min_trust_tier=3` for high-quality results

---

## 11. Licensing & Attribution

All data sources used must comply with:
- **OSM**: ODbL (Open Database License) - Attribute OpenStreetMap
- **Wikidata**: CC0 - No attribution required
- **NOAA**: Public domain
- **Europeana**: Various - Check per item
- **GTFS**: Usually open, check per transit agency

Include attributions in itinerary footer:
```
Data sources: OpenStreetMap contributors, NOAA, Wikidata, [City] Open Data Portal
```

---

## 12. Optional Enhancements (Still Open)

- [ ] Open audio guides (museum CC licenses)
- [ ] City subreddit archives (topic-modeled, anonymized)
- [ ] Open travel blogs (Creative Commons only)
- [ ] Flickr geotagged photos (CC-licensed)
- [ ] YouTube city guides (Creative Commons)

---

## 13. Next Steps

### To Start Ingesting Data:

1. **Create data ingestion pipeline**:
   ```bash
   python scripts/ingest_osm.py --city Lisbon
   python scripts/ingest_wikidata.py --city Lisbon
   python scripts/ingest_weather.py --city Lisbon
   ```

2. **Set up update schedule**:
   - Daily: Weather, events
   - Weekly: OSM updates
   - Monthly: Cost indices
   - Quarterly: Full refresh

3. **Monitor data quality**:
   - Track coverage per city
   - Flag outdated data (>6 months)
   - Validate coordinates, prices

---

## 14. Tools & Libraries

### Data Fetching
- `overpy` - OSM Overpass API
- `SPARQLWrapper` - Wikidata queries
- `meteostat` - Weather history
- `gtfs-kit` - Transit feeds

### Processing
- `pandas` - Data manipulation
- `geopandas` - Geospatial data
- `sentence-transformers` - Embeddings

### Storage
- PostgreSQL + PostGIS - Structured + geo data
- ChromaDB - Vector embeddings
- Redis - Caching

---

## Questions?

For data source questions or ingestion help:
- Email: data@timbuktoo.ai
- Slack: #data-engineering

For specific city requests:
- Email: cities@timbuktoo.ai
