# Engineering Tickets - Timbuktoo MVP

Complete engineering delivery plan with Epics, Stories, Tasks, and Acceptance Criteria.

---

## EPIC 1: Core Knowledge Infrastructure

**Priority**: P0
**Owner**: Data Engineering
**Timeline**: Weeks 1-2

---

### TICKET 1.1 — Create Vector Schema & Collection

**Type**: Backend / ML
**Priority**: P0
**Points**: 5
**Owner**: ML Engineer

#### Description
Implement the `city_knowledge_vectors` collection with metadata filtering and city-level indexing using ChromaDB.

#### Tasks
- [ ] Define vector payload schema with all required metadata fields
- [ ] Enable metadata filtering (city, entity_type, seasonality, vibes, price_tier)
- [ ] Add batch embedding ingestion pipeline
- [ ] Implement vector search with multi-field filters
- [ ] Add city-level indexing for fast retrieval
- [ ] Test with sample data (100+ entities)

#### Acceptance Criteria
- ✅ Vectors retrievable by city + tag combination
- ✅ Metadata filters work without full collection scan
- ✅ Embeddings persist across server restarts
- ✅ Search latency < 100ms for 1000-entity collection
- ✅ Batch ingestion handles 100+ entities/minute

#### Technical Specs
```python
# Vector schema
{
    "vector_id": "uuid",
    "entity_id": "uuid",
    "city_id": "uuid",
    "entity_type": str,  # restaurant, bar, museum, nature
    "title": str,
    "content": str,  # 300-600 tokens
    "tags": List[str],
    "vibe": List[str],
    "price_tier": str,
    "seasonality": List[str],
    "time_of_day": List[str],
    "duration_minutes": int,
    "geo_lat": float,
    "geo_lon": float,
    "trust_tier": int,  # 1-5
    "source": str,
    "last_verified": str
}
```

#### Dependencies
- ChromaDB >= 0.4.22
- sentence-transformers >= 2.3.1

---

### TICKET 1.2 — Relational Database Schema

**Type**: Backend
**Priority**: P0
**Points**: 3
**Owner**: Backend Engineer

#### Description
Create relational tables for cities, entities, trips, and feedback with proper indexing and foreign key constraints.

#### Tasks
- [ ] Create `cities` table with geographic metadata
- [ ] Create `entities` table with foreign keys to cities
- [ ] Create `vectors` metadata table (links to ChromaDB)
- [ ] Create `trips` table for user itineraries
- [ ] Create `feedback` table with ratings
- [ ] Add foreign key constraints
- [ ] Add indexes for common queries
- [ ] Write migration scripts

#### Acceptance Criteria
- ✅ Referential integrity enforced across all tables
- ✅ Can join vectors → entities → cities without errors
- ✅ Indexes created on: city_id, entity_type, price_tier, trust_tier
- ✅ Migration script runs successfully on fresh database
- ✅ All tables have created_at and updated_at timestamps

#### Schema Files
- `timbuktoo/database/migrations/001_initial_schema.sql`
- `timbuktoo/database/models/*.py`

#### Dependencies
- PostgreSQL 14+
- SQLAlchemy >= 2.0.25

---

## EPIC 2: City Ingestion Pipeline

**Priority**: P0
**Owner**: Data Engineering
**Timeline**: Weeks 2-3

---

### TICKET 2.1 — City Ingestion Job

**Type**: Data Engineering
**Priority**: P0
**Points**: 8
**Owner**: Data Engineer

#### Description
Automated end-to-end pipeline to ingest a new city including POIs, narratives, embeddings, and validation.

#### Tasks
- [ ] Create ingestion orchestrator script
- [ ] Implement OpenStreetMap data fetcher
- [ ] Implement Wikidata entity fetcher
- [ ] Build normalization pipeline (names, coordinates, prices)
- [ ] Generate embeddings using sentence-transformers
- [ ] Implement validation and QA checks
- [ ] Add error handling and retry logic
- [ ] Create ingestion monitoring dashboard

#### Acceptance Criteria
- ✅ City ingestion completes in < 30 minutes
- ✅ At least 120 entities ingested per city
- ✅ Entity types distributed: 30% food, 20% bars, 20% nature, 15% museums, 15% other
- ✅ All entities have valid coordinates
- ✅ Trust tier assigned based on source
- ✅ QA checklist passes (no duplicates, no hallucinations)
- ✅ Ingestion logs created with source attribution

#### Script Location
- `scripts/ingest_city.py --city "Lisbon" --country "Portugal"`

#### Dependencies
- overpy (OpenStreetMap API)
- SPARQLWrapper (Wikidata)
- sentence-transformers

---

### TICKET 2.2 — Pilot City Load (6 Cities)

**Type**: Data
**Priority**: P0
**Points**: 5
**Owner**: Data Engineer

#### Description
Ingest 6 pilot cities: Mexico City, Barcelona, Tokyo, Lisbon, NYC, and one surprise city.

#### Tasks
- [ ] Ingest Lisbon (full entity set)
- [ ] Ingest Barcelona
- [ ] Ingest Mexico City
- [ ] Ingest Tokyo
- [ ] Ingest New York City
- [ ] Ingest Bangkok OR Marrakech (team vote)
- [ ] Run QA validation on all cities
- [ ] Generate city comparison report

#### Acceptance Criteria
- ✅ Each city meets minimum entity thresholds:
  - Lisbon: 150+ entities
  - Others: 120+ entities each
- ✅ QA checklist passes for all cities
- ✅ Vector search returns relevant results for test queries
- ✅ No duplicate entities within same city
- ✅ Coverage report shows balanced entity type distribution

#### Test Queries (for QA)
```python
test_queries = [
    "authentic tequila bars in Mexico City",
    "hidden gem seafood restaurants in Lisbon",
    "best ramen spots in Tokyo",
    "craft beer bars in Barcelona",
    "jazz clubs in New York City",
    "coffee roasters in [city]"
]
```

---

## EPIC 3: Agent Orchestration

**Priority**: P0
**Owner**: Backend / ML
**Timeline**: Weeks 3-4

---

### TICKET 3.1 — Agent Router (Workflow Orchestrator)

**Type**: Backend
**Priority**: P0
**Points**: 8
**Owner**: Backend Engineer + ML Engineer

#### Description
Implement deterministic agent router with enforced execution order, error handling, and state management.

#### Tasks
- [ ] Implement WorkflowState class (immutable state container)
- [ ] Create TravelOrchestrator with node execution logic
- [ ] Add intent validation (Node 1)
- [ ] Wire City Selection Agent (Node 2)
- [ ] Wire Weather & Events Tools (Nodes 3-4, parallel)
- [ ] Wire Local Expert Agent (Node 5)
- [ ] Wire Travel Concierge Agent (Node 6)
- [ ] Add post-processing and trip saving (Nodes 7-8)
- [ ] Implement error handling with graceful degradation
- [ ] Add retry logic for transient failures

#### Acceptance Criteria
- ✅ Agents execute in strict sequential order
- ✅ Each agent receives validated input from previous agent
- ✅ Failed agents don't crash entire workflow
- ✅ Workflow state is immutable and auditable
- ✅ Can resume workflow from any completed node
- ✅ All agent outputs logged for debugging
- ✅ Cost tracking works across all agents

#### Code Location
- `timbuktoo/workflows/orchestrator.py`

#### Dependencies
- All agent implementations
- CostController
- Monitoring/metrics

---

### TICKET 3.2 — Shared Agent Memory & Context

**Type**: Backend
**Priority**: P0
**Points**: 3
**Owner**: Backend Engineer

#### Description
Persist trip context across agents with immutable history and context passing.

#### Tasks
- [ ] Design trip context schema
- [ ] Implement context serialization/deserialization
- [ ] Add context validation between agents
- [ ] Create context snapshot mechanism
- [ ] Implement context retrieval API

#### Acceptance Criteria
- ✅ Context accessible by all agents in workflow
- ✅ Context is immutable (append-only)
- ✅ Can retrieve full execution history for debugging
- ✅ Context includes: preferences, selected city, city guide, weather, events
- ✅ Context serialized to JSON for storage

---

## EPIC 4: Real-Time Tools

**Priority**: P1
**Owner**: Backend
**Timeline**: Week 4

---

### TICKET 4.1 — Weather Tool Integration

**Type**: Backend
**Priority**: P1
**Points**: 3
**Owner**: Backend Engineer

#### Description
Integrate OpenWeatherMap API with caching and fallback to mock data.

#### Tasks
- [ ] Implement WeatherTool class
- [ ] Add OpenWeatherMap API client
- [ ] Implement 7-day forecast fetching
- [ ] Add response caching (60min TTL)
- [ ] Implement mock weather fallback
- [ ] Add retry logic with exponential backoff
- [ ] Add usage tracking for API quota

#### Acceptance Criteria
- ✅ 7-day forecast returned with temp, conditions, precipitation
- ✅ Weather used in itinerary logic (outdoor activities on sunny days)
- ✅ Cache hit rate > 80% for repeated queries
- ✅ Mock fallback works when API unavailable
- ✅ API errors logged but don't break workflow

#### Code Location
- `timbuktoo/tools/weather.py`

---

### TICKET 4.2 — Events Tool Integration

**Type**: Backend
**Priority**: P1
**Points**: 3
**Owner**: Backend Engineer

#### Description
Integrate events API (PredictHQ or similar) with fallback to municipal open data.

#### Tasks
- [ ] Implement EventsTool class
- [ ] Add events API client
- [ ] Implement event filtering by city + date range
- [ ] Add response caching (60min TTL)
- [ ] Implement mock events fallback
- [ ] Add municipal data source fallback

#### Acceptance Criteria
- ✅ Events filtered by city + date range
- ✅ Event-based itinerary adjustments (add festivals to relevant days)
- ✅ Returns 5-10 relevant events per city
- ✅ Mock fallback provides realistic sample events
- ✅ Events categorized: festival, concert, sports, cultural

#### Code Location
- `timbuktoo/tools/events.py`

---

## EPIC 5: Feedback & Learning Loop

**Priority**: P1
**Owner**: Full Stack + ML
**Timeline**: Weeks 5-6

---

### TICKET 5.1 — Feedback Capture UI/API

**Type**: Full Stack
**Priority**: P1
**Points**: 5
**Owner**: Full Stack Engineer

#### Description
Build feedback collection API and UI form for post-trip surveys.

#### Tasks
- [ ] Create feedback API endpoints
  - POST /api/v1/feedback
  - GET /api/v1/feedback/{trip_id}
- [ ] Design feedback form UI (mockups)
- [ ] Implement day-level rating capture
- [ ] Implement overall rating capture
- [ ] Add free-text comments field
- [ ] Add pacing feedback selector
- [ ] Add liked/disliked entities checkboxes
- [ ] Store feedback in database

#### Acceptance Criteria
- ✅ Day-level ratings (1-5 stars per day) captured
- ✅ Overall, pacing, authenticity, value ratings collected
- ✅ Comments stored and retrievable
- ✅ Entity-level engagement tracked (liked/disliked)
- ✅ Feedback tied to trip_id and variant_id
- ✅ API returns 201 on successful submission

#### UI/UX Requirements
- Mobile-friendly feedback form
- Progress indicator (Day 1/7, Day 2/7, etc.)
- Optional fields (don't force completion)

---

### TICKET 5.2 — Feedback Weighting Engine

**Type**: ML
**Priority**: P2
**Points**: 8
**Owner**: ML Engineer

#### Description
Use feedback to adjust entity rankings in vector search (down-rank poor performers, boost high-rated entities).

#### Tasks
- [ ] Design feedback scoring algorithm
- [ ] Implement entity rating aggregation
- [ ] Add boosting logic for high-rated entities
- [ ] Add dampening logic for low-rated entities
- [ ] Implement trust decay over time
- [ ] Create A/B test for feedback-weighted search
- [ ] Monitor impact on satisfaction

#### Acceptance Criteria
- ✅ Entities with avg rating > 4.5 boosted in search results
- ✅ Entities with avg rating < 3.0 down-ranked or hidden
- ✅ Trust tier updated based on feedback volume
- ✅ Feedback loops don't create filter bubbles
- ✅ Algorithm tested on historical feedback data

#### Algorithm Spec
```python
# Boost score
entity_score = base_score + (avg_rating - 3.0) * 0.2
# Decay over time
entity_score *= exp(-days_since_feedback / 180)
```

---

## EPIC 6: Cost Controls & Monitoring

**Priority**: P1
**Owner**: Backend + DevOps
**Timeline**: Week 5

---

### TICKET 6.1 — Cost Tracking Per Agent

**Type**: Backend
**Priority**: P1
**Points**: 3
**Owner**: Backend Engineer

#### Description
Track token usage and costs per agent, per trip, and overall.

#### Tasks
- [ ] Implement CostTracking model
- [ ] Add token counting to base agent
- [ ] Record costs in database per agent call
- [ ] Create cost summary API
- [ ] Add cost alerts (>$0.80/trip)

#### Acceptance Criteria
- ✅ Costs tracked per agent (city_selection, local_expert, concierge)
- ✅ Costs stored in cost_tracking table
- ✅ Can query total cost by trip_id
- ✅ Alert triggered if trip cost > $0.80
- ✅ Cost breakdown available in API response

---

### TICKET 6.2 — Prometheus Metrics

**Type**: DevOps
**Priority**: P1
**Points**: 3
**Owner**: DevOps Engineer

#### Description
Expose Prometheus metrics for monitoring agent performance, costs, and user satisfaction.

#### Tasks
- [ ] Set up Prometheus server
- [ ] Implement metrics collection in agents
- [ ] Expose metrics endpoint
- [ ] Create Grafana dashboards
- [ ] Set up alerting rules

#### Acceptance Criteria
- ✅ Metrics available at /metrics endpoint
- ✅ Agent latency tracked
- ✅ Cost per trip tracked
- ✅ Feedback ratings tracked
- ✅ Dashboards show real-time data

---

## EPIC 7: Multi-Tenancy (Already Complete ✅)

**Priority**: P0
**Owner**: Backend
**Timeline**: Weeks 6-7

See existing implementation and docs/MULTI_TENANCY.md

---

## EPIC 8: Security & Compliance

**Priority**: P1
**Owner**: Security + Backend
**Timeline**: Week 7

---

### TICKET 8.1 — RBAC Implementation

**Type**: Backend / Security
**Priority**: P1
**Points**: 5
**Owner**: Backend Engineer

#### Description
Role-Based Access Control with 3 roles: Admin, Operator, Viewer.

#### Tasks
- [ ] Implement User model with roles
- [ ] Create permission mapping
- [ ] Add JWT authentication
- [ ] Add authorization middleware
- [ ] Create user management API
- [ ] Add audit logging for access control

#### Acceptance Criteria
- ✅ Three roles implemented: admin, operator, viewer
- ✅ Permissions enforced on all API endpoints
- ✅ JWT tokens expire after 1 hour
- ✅ Unauthorized access returns 403
- ✅ All access attempts logged

Already implemented in `timbuktoo/security/rbac.py`

---

### TICKET 8.2 — Audit Logging

**Type**: Backend / Security
**Priority**: P1
**Points**: 3
**Owner**: Backend Engineer

#### Description
Comprehensive audit logging for SOC-2 compliance.

#### Tasks
- [ ] Implement AuditLog model
- [ ] Log all authentication attempts
- [ ] Log all data access
- [ ] Log all trip creations
- [ ] Log all configuration changes
- [ ] Create audit trail query API

#### Acceptance Criteria
- ✅ All user actions logged with timestamp, IP, user_agent
- ✅ Failed login attempts logged
- ✅ Trip creation logged with cost details
- ✅ Logs retained for 1 year
- ✅ Logs queryable by user_id, event_type, date range

Already implemented in `timbuktoo/security/audit.py`

---

## EPIC 9: Deployment & DevOps

**Priority**: P1
**Owner**: DevOps
**Timeline**: Week 8

---

### TICKET 9.1 — Docker Containerization

**Type**: DevOps
**Priority**: P1
**Points**: 3
**Owner**: DevOps Engineer

#### Tasks
- [ ] Create Dockerfile for API server
- [ ] Create docker-compose.yml (API + Postgres + ChromaDB)
- [ ] Add environment variable management
- [ ] Create deployment scripts
- [ ] Document deployment process

#### Acceptance Criteria
- ✅ `docker-compose up` starts full stack
- ✅ Persistent volumes for database and vector data
- ✅ Environment variables configurable
- ✅ Health checks implemented

---

### TICKET 9.2 — CI/CD Pipeline

**Type**: DevOps
**Priority**: P1
**Points**: 5
**Owner**: DevOps Engineer

#### Tasks
- [ ] Set up GitHub Actions workflow
- [ ] Add automated testing
- [ ] Add linting and code quality checks
- [ ] Add automated deployment to staging
- [ ] Add production deployment with manual approval

#### Acceptance Criteria
- ✅ Tests run on every PR
- ✅ Code coverage > 80%
- ✅ Automatic deployment to staging on merge to main
- ✅ Production deployment requires manual approval

---

## Summary

### Total Story Points: ~90
### Estimated Timeline: 8-10 weeks
### Team Size: 4-5 engineers (Backend, ML, Data, DevOps, Full Stack)

### Critical Path
1. Week 1-2: EPIC 1 (Knowledge Infrastructure)
2. Week 2-3: EPIC 2 (Data Ingestion)
3. Week 3-4: EPIC 3 (Agent Orchestration)
4. Week 4: EPIC 4 (Tools)
5. Week 5-6: EPIC 5 (Feedback Loop)
6. Week 6-7: EPIC 7 (Multi-Tenancy) ✅
7. Week 7: EPIC 8 (Security)
8. Week 8: EPIC 9 (Deployment)

### Dependencies
- PostgreSQL 14+ must be provisioned by Week 1
- API keys (OpenWeatherMap, events) needed by Week 4
- Domain and SSL cert needed by Week 8

---

## Questions?

For ticket questions:
- Email: engineering@timbuktoo.ai
- Slack: #engineering
