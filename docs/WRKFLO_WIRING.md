# Wrk.Flo UI Wiring Specification - Timbuktoo MVP

Complete visual workflow builder configuration for Timbuktoo Travel Concierge.

---

## Canvas Overview

**Workflow Name**: `timbuktoo_travel_concierge`
**Trigger Type**: REST API
**Execution Mode**: Sequential with parallel branches
**Total Nodes**: 8
**Estimated Runtime**: 45-120 seconds per trip

---

## Node Layout (Left to Right)

```
┌─────────────────────────────────────────────────────────────────────┐
│                       TIMBUKTOO WORKFLOW CANVAS                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [START]                                                            │
│     │                                                               │
│     ▼                                                               │
│  ┌──────────────┐                                                  │
│  │ Intent       │                                                  │
│  │ Parser       │                                                  │
│  │ (AI Router)  │                                                  │
│  └──────┬───────┘                                                  │
│         │                                                          │
│         ▼                                                          │
│  ┌──────────────┐                                                  │
│  │ City         │                                                  │
│  │ Selection    │                                                  │
│  │ (AI Decision)│                                                  │
│  └──────┬───────┘                                                  │
│         │                                                          │
│         ▼                                                          │
│  ┌──────────────────────────────────────┐                         │
│  │ Local Expert (AI Knowledge)          │                         │
│  │ + Vector Search (35 chunks)          │                         │
│  └──────┬───────────────────────────────┘                         │
│         │                                                          │
│         ├────────────┬─────────────┐                               │
│         ▼            ▼             ▼                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                        │
│  │ Weather  │  │ Events   │  │ (Future  │                        │
│  │ Tool     │  │ Tool     │  │  Tools)  │                        │
│  └────┬─────┘  └────┬─────┘  └──────────┘                        │
│       │             │                                              │
│       └─────┬───────┘                                              │
│             ▼                                                      │
│  ┌──────────────────────────┐                                     │
│  │ Travel Concierge         │                                     │
│  │ (AI Multistep)           │                                     │
│  │ Variant: {control/slow}  │                                     │
│  └──────┬───────────────────┘                                     │
│         │                                                          │
│         ▼                                                          │
│  ┌──────────────┐                                                  │
│  │ Post-        │                                                  │
│  │ Processor    │                                                  │
│  └──────┬───────┘                                                  │
│         │                                                          │
│         ├──────────────┐                                           │
│         ▼              ▼                                           │
│    [RETURN]      ┌──────────────┐                                 │
│                  │ Feedback     │                                 │
│                  │ Listener     │                                 │
│                  │ (Async)      │                                 │
│                  └──────────────┘                                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Node 1: Intent Parser (AI Router)

**Type**: AI Router
**Purpose**: Validate user preferences and route to appropriate workflow branch
**Model**: Claude 3.5 Haiku
**Max Tokens**: 2048
**Temperature**: 0.2

### Input Schema
```json
{
  "preferences": {
    "vibes": ["string"],
    "interests": ["string"],
    "budget_level": "string"
  },
  "travel_dates": {
    "start": "YYYY-MM-DD",
    "end": "YYYY-MM-DD"
  },
  "candidate_cities": ["string"],
  "user_id": "uuid"
}
```

### Prompt Template
```
You are an intent parser for a travel concierge system.

TASK: Validate and normalize user preferences.

INPUT:
{input_json}

VALIDATION RULES:
- Travel dates must be at least 14 days in the future
- Trip duration must be exactly 7 days
- Budget level must be: low, mid, or high
- At least 2 interests required
- Candidate cities must be from pilot list: Lisbon, Barcelona, Tokyo, Mexico City, NYC, Bangkok

OUTPUT JSON:
{
  "valid": true/false,
  "normalized_preferences": {...},
  "validation_errors": [],
  "routing_decision": "create_trip" or "error"
}

Only output valid JSON. No explanations.
```

### Output Routing
- **If valid=true** → Route to Node 2 (City Selection)
- **If valid=false** → Return error to user, skip workflow

### Error Handling
- Timeout: 10 seconds
- On error: Return validation_errors to user
- Retry: None (user must fix input)

### Cost Tracking
- Input tokens: ~300
- Output tokens: ~200
- Estimated cost: $0.0001 per execution

---

## Node 2: City Selection (AI Decision)

**Type**: AI Decision
**Purpose**: Rank cities based on user preferences, weather, events
**Model**: Claude 3.5 Sonnet
**Max Tokens**: 4096
**Temperature**: 0.5

### Input Schema
```json
{
  "normalized_preferences": {...},
  "travel_dates": {...},
  "candidate_cities": [...],
  "weather_data_preview": {...},
  "events_data_preview": {...}
}
```

### Prompt Template
Use `CITY_SELECTION_AGENT_PROMPT` from `timbuktoo/agents/prompts.py`

**Key Sections:**
- SCORING METHODOLOGY (Weather 20%, Events 15%, Food 30%, Nature 15%, Cost 10%, Vibe 10%)
- OUTPUT JSON FORMAT with ranked_cities array (exactly 3 cities)
- Selection rationale

### Output Schema
```json
{
  "ranked_cities": [
    {
      "city": "Lisbon",
      "city_id": "uuid",
      "score": 95,
      "reasoning": "string",
      "highlights": ["string"],
      "weather_summary": "string",
      "estimated_daily_budget_usd": 120
    }
  ],
  "selection_rationale": "string",
  "top_city": {...}
}
```

### Output Routing
- Extract `top_city` from ranked_cities[0]
- Pass to Node 3 (Local Expert)

### Error Handling
- Timeout: 20 seconds
- On error: Fallback to highest-scored city from database
- Retry: 1 attempt with exponential backoff

### Cost Tracking
- Input tokens: ~1500
- Output tokens: ~1200
- Estimated cost: $0.02 per execution

---

## Node 3: Local Expert (AI Knowledge + RAG)

**Type**: AI Knowledge
**Purpose**: Retrieve deep city intelligence via vector search
**Model**: Claude 3.5 Sonnet
**Max Tokens**: 16384
**Temperature**: 0.6

### Input Schema
```json
{
  "selected_city": {
    "city_id": "uuid",
    "name": "string",
    "country": "string"
  },
  "user_preferences": {...}
}
```

### Vector Search Configuration
**Collection**: `city_knowledge_vectors` (or `tenant_{id}_vectors` for multi-tenant)
**Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
**Query Construction**: Concatenate user interests and vibes
**Filters**:
- `city_id` = selected_city.city_id
- `trust_tier` >= 4
- `vibes` IN user_preferences.vibes (if specified)
- `price_tier` matches budget_level

**Results**: 35 chunks
**Cache TTL**: 60 minutes (same city + preferences)

### Prompt Template
Use `LOCAL_EXPERT_AGENT_PROMPT` from `timbuktoo/agents/prompts.py`

**Critical Instructions:**
- All recommendations MUST come from vector search results
- NO fabricated venues
- Include trust tier 4-5 sources only
- Provide specific details: hours, prices, what to order

### Output Schema
```json
{
  "city_guide": {
    "city_overview": {...},
    "neighborhoods": [...],
    "must_visit": {
      "restaurants": [...],
      "bars": [...],
      "nature_spots": [...],
      "cultural_sites": [...]
    },
    "hidden_gems": [...],
    "local_customs": [...],
    "practical_info": {...}
  }
}
```

### Output Routing
- Pass `city_guide` to Nodes 4a, 4b (Weather & Events) and Node 5 (Concierge)

### Error Handling
- Timeout: 30 seconds
- On vector search failure: Use cached city data if available
- On LLM failure: Retry once with reduced token limit (8192)

### Cost Tracking
- Input tokens: ~6000 (including vector context)
- Output tokens: ~5000
- Estimated cost: $0.08 per execution

---

## Node 4a: Weather Tool (Parallel)

**Type**: Tool (HTTP API)
**Purpose**: Fetch 7-day weather forecast
**API**: OpenWeatherMap
**Execution**: Parallel with Node 4b (Events)

### Input Schema
```json
{
  "city": "Lisbon",
  "country": "Portugal",
  "start_date": "2024-06-01",
  "days": 7,
  "city_lat": 38.7223,
  "city_lon": -9.1393
}
```

### API Configuration
**Endpoint**: `https://api.openweathermap.org/data/2.5/forecast`
**Auth**: API key in query params (`appid={key}`)
**Rate Limit**: 60 calls/minute
**Cache TTL**: 60 minutes

### Processing Logic
1. Call API with lat/lon coordinates
2. Aggregate 3-hour intervals into daily forecasts
3. Extract: temp_high, temp_low, conditions, precipitation_mm, wind_speed

### Output Schema
```json
{
  "daily_forecasts": [
    {
      "date": "2024-06-01",
      "temp_high_c": 26,
      "temp_low_c": 18,
      "conditions": "Sunny",
      "precipitation_mm": 0,
      "precipitation_prob": 0.05,
      "wind_speed_kmh": 15
    }
  ]
}
```

### Fallback Strategy
If API fails:
1. Check cache for recent forecast (< 24 hours old)
2. Use mock weather based on city's typical climate
3. Flag as `forecast_source: "estimated"`

### Error Handling
- Timeout: 5 seconds
- Retry: 2 attempts with 1-second delay
- On total failure: Use mock data, log warning

### Cost Tracking
- API cost: Free tier (60 calls/min)
- No LLM cost

---

## Node 4b: Events Tool (Parallel)

**Type**: Tool (HTTP API)
**Purpose**: Fetch local events during travel dates
**API**: PredictHQ or Municipal Open Data
**Execution**: Parallel with Node 4a (Weather)

### Input Schema
```json
{
  "city": "Lisbon",
  "country": "Portugal",
  "start_date": "2024-06-01",
  "end_date": "2024-06-07",
  "categories": ["festival", "concert", "sports", "cultural"]
}
```

### API Configuration
**Primary**: PredictHQ API
**Fallback**: Municipal open data portals
**Rate Limit**: 100 calls/day (PredictHQ free tier)
**Cache TTL**: 60 minutes

### Processing Logic
1. Call PredictHQ with city + date range
2. Filter by relevance score > 50
3. Categorize events (festival, concert, sports, cultural)
4. Return top 10 most relevant

### Output Schema
```json
{
  "events": [
    {
      "title": "Lisbon Street Food Festival",
      "date": "2024-06-03",
      "category": "festival",
      "relevance": 0.92,
      "location": "string",
      "description": "string"
    }
  ]
}
```

### Fallback Strategy
If API fails:
1. Check cache
2. Query municipal data (scraped weekly)
3. Use mock events (generic festivals for city)

### Error Handling
- Timeout: 5 seconds
- Retry: 2 attempts
- On failure: Return empty events array, continue workflow

### Cost Tracking
- API cost: Free tier
- No LLM cost

---

## Node 5: Travel Concierge (AI Multistep)

**Type**: AI Multistep
**Purpose**: Generate comprehensive 7-day itinerary
**Model**: Claude 3.5 Sonnet
**Max Tokens**: 38000 (degraded to 25000 or 15000 if budget low)
**Temperature**: 0.7

### Input Schema
```json
{
  "city_guide": {...},
  "weather_forecasts": [...],
  "events": [...],
  "user_preferences": {...},
  "travel_dates": {...},
  "variant": "control" | "slow_hidden_gems"
}
```

### Prompt Template
Use `TRAVEL_CONCIERGE_AGENT_PROMPT` from `timbuktoo/agents/prompts.py`

**Variant Injection:**
- `{variant}` → "control" or "slow_hidden_gems"
- `{variant_instructions}` → Injected from `VARIANT_INSTRUCTIONS`

**Control Variant:**
- 2-3 major activities per day
- 60% local spots, 40% must-sees
- Moderate walking (2-4km/day)

**Slow Hidden Gems Variant:**
- 1-2 major activities per day
- 90% local spots, 10% optional landmarks
- More unstructured time, deeper immersion

### Output Schema
```json
{
  "trip_summary": {...},
  "daily_itineraries": [
    {
      "day": 1,
      "date": "2024-06-01",
      "theme": "string",
      "weather": {...},
      "schedule": [
        {
          "time": "09:00",
          "duration_minutes": 120,
          "activity": "string",
          "type": "culture" | "meal" | "nature" | "nightlife",
          "location": "string",
          "details": "string",
          "cost_usd": 15,
          "reservations_needed": false,
          "insider_tip": "string"
        }
      ],
      "meals": {...},
      "daily_budget_usd": 150
    }
  ],
  "logistics": {...},
  "packing_list": {...},
  "insider_tips": [...]
}
```

### Output Routing
- Pass full itinerary to Node 6 (Post-Processor)

### Error Handling
- Timeout: 60 seconds
- On timeout: Return partial itinerary if > 3 days generated
- Retry: 1 attempt with reduced tokens (25000)
- Cost check: Before execution, verify remaining budget > $0.30

### Cost Tracking
- Input tokens: ~10000 (city guide + weather + events)
- Output tokens: ~15000 (7-day itinerary)
- Estimated cost: $0.25 per execution

---

## Node 6: Post-Processor (Data Transformation)

**Type**: Data Transform
**Purpose**: Save trip to database, assign variant, prepare response
**Execution**: Synchronous

### Input Schema
```json
{
  "trip_itinerary": {...},
  "user_id": "uuid",
  "variant": "control" | "slow_hidden_gems",
  "total_cost_usd": 0.52,
  "execution_metadata": {...}
}
```

### Processing Steps
1. **Generate Trip ID**: `uuid.uuid4()`
2. **Assign Variant**: Call `assign_variant(trip_id, stratify_by=city_id)`
3. **Save to Database**:
   - Insert into `trips` table
   - Save `daily_itineraries` as JSONB
   - Record `variant_id`, `total_cost_usd`, `created_at`
4. **Save Cost Breakdown**:
   - Insert into `cost_tracking` table per agent
   - Aggregate total cost
5. **Increment Tenant Quota** (if multi-tenant):
   - `increment_usage(tenant_id, "itineraries", 1)`
6. **Log Audit Event**:
   - `log_event("trip_creation", "create", "success", user_id, "trip")`

### Output Schema
```json
{
  "trip_id": "uuid",
  "variant": "slow_hidden_gems",
  "city": "Lisbon",
  "dates": {...},
  "itinerary": {...},
  "cost_usd": 0.52,
  "created_at": "2024-06-01T10:30:00Z",
  "feedback_url": "/api/v1/feedback/{trip_id}"
}
```

### Output Routing
- **Primary**: Return to user (API response)
- **Secondary**: Queue for Node 7 (Feedback Listener - async)

### Error Handling
- Database save failure: Retry 3 times with exponential backoff
- If all retries fail: Return itinerary to user but flag as "not_saved"
- Quota exceeded: Should be caught earlier, but if missed, return 429 error

### Cost Tracking
- No LLM cost
- Database write cost: negligible

---

## Node 7: Feedback Listener (Async Background Process)

**Type**: Async Listener
**Purpose**: Wait for post-trip feedback, update entity rankings
**Execution**: Asynchronous (does not block main workflow)
**Trigger**: User submits feedback via `/api/v1/feedback`

### Input Schema
```json
{
  "trip_id": "uuid",
  "feedback_window_days": 30
}
```

### Processing Logic
1. **Wait State**: Poll for feedback submission (check every 24 hours for 30 days)
2. **On Feedback Received**:
   - Save to `feedback` table
   - Extract ratings: overall, pacing, authenticity, value
   - Extract liked/disliked entities
   - Call `update_entity_rankings(entity_ids, ratings)`
3. **Update Vector Weights**:
   - Boost high-rated entities (avg > 4.5): +0.2 to base score
   - Dampen low-rated entities (avg < 3.0): -0.3 to base score
   - Update trust tier if feedback volume > 10
4. **A/B Test Analytics**:
   - Call `get_variant_performance(variant_id)`
   - Update experiment dashboard metrics

### Timeout
- 30 days from trip creation
- After timeout: Mark trip as `feedback_status: "expired"`

### Error Handling
- Database errors: Retry indefinitely with exponential backoff (max 1 hour)
- No feedback received: Normal state, no error

### Cost Tracking
- No LLM cost
- Database polling: minimal (daily cron job)

---

## Workflow Metadata

### Total Cost Per Trip
- Node 1 (Intent): $0.0001
- Node 2 (City Selection): $0.02
- Node 3 (Local Expert): $0.08
- Node 4a (Weather): $0
- Node 4b (Events): $0
- Node 5 (Concierge): $0.25
- Node 6 (Post-Processor): $0
- Node 7 (Feedback): $0

**Total Average Cost**: $0.35 per trip
**Budget Limit**: $0.80 per trip
**Safety Margin**: 56%

### Execution Time
- Node 1: 2-3 seconds
- Node 2: 5-8 seconds
- Node 3: 10-15 seconds
- Node 4a + 4b (parallel): 3-5 seconds
- Node 5: 25-40 seconds
- Node 6: 1-2 seconds
- Node 7: Async (no blocking)

**Total Runtime**: 46-73 seconds (typical)
**Max Runtime**: 120 seconds (timeout)

### Error Recovery

**Global Error Handler:**
```yaml
on_error:
  - log_error: true
  - notify_ops: if severity >= ERROR
  - fallback_strategy:
      node_1: return validation_errors
      node_2: select highest_scored_city
      node_3: use cached_city_guide
      node_4a: use mock_weather
      node_4b: return empty_events
      node_5: retry with reduced_tokens
      node_6: return itinerary_not_saved
```

**Retry Policy:**
- Max retries per node: 1
- Backoff strategy: Exponential (2s, 4s, 8s)
- Circuit breaker: Open after 5 consecutive failures

---

## Monitoring & Observability

### Metrics to Track
1. **Workflow Success Rate**: % of trips completing Node 6
2. **Node Latency**: P50, P95, P99 per node
3. **Cost per Trip**: Actual vs budget
4. **Variant Distribution**: 50/50 split verification
5. **Feedback Rate**: % of trips receiving feedback within 30 days

### Prometheus Metrics
```
timbuktoo_workflow_executions_total{status="success|failure"}
timbuktoo_node_latency_seconds{node="city_selection|local_expert|concierge"}
timbuktoo_workflow_cost_usd{variant="control|slow_hidden_gems"}
timbuktoo_feedback_submission_rate{variant="control|slow_hidden_gems"}
```

### Alerts
- **High Cost Alert**: If avg cost > $0.70/trip for > 10 trips
- **Latency Alert**: If P95 latency > 90 seconds
- **Error Rate Alert**: If failure rate > 5% over 1 hour
- **Variant Imbalance Alert**: If variant split deviates > 55/45 over 100 trips

---

## Configuration Variables

### Environment Variables
```bash
# LLM Configuration
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL_HAIKU=claude-3-5-haiku-20241022
ANTHROPIC_MODEL_SONNET=claude-3-5-sonnet-20241022

# API Keys
OPENWEATHERMAP_API_KEY=...
PREDICTHQ_API_KEY=...

# Database
POSTGRES_DSN=postgresql://user:pass@localhost:5432/timbuktoo
CHROMADB_HOST=localhost
CHROMADB_PORT=8000

# Cost Controls
MAX_TRIP_COST_USD=0.80
DEGRADATION_THRESHOLD_HIGH=0.30
DEGRADATION_THRESHOLD_LOW=0.10

# A/B Testing
AB_TEST_ENABLED=true
DEFAULT_VARIANT=control

# Caching
WEATHER_CACHE_TTL_MINUTES=60
EVENTS_CACHE_TTL_MINUTES=60
CITY_GUIDE_CACHE_TTL_MINUTES=60
```

### Wrk.Flo Canvas Settings
```json
{
  "canvas_id": "timbuktoo_mvp",
  "version": "1.0.0",
  "execution_mode": "sequential_with_parallel",
  "max_workflow_timeout_seconds": 120,
  "enable_retries": true,
  "enable_caching": true,
  "enable_monitoring": true,
  "log_level": "INFO"
}
```

---

## Deployment Checklist

### Pre-Deployment
- [ ] Configure all environment variables
- [ ] Provision PostgreSQL database
- [ ] Deploy ChromaDB instance
- [ ] Obtain API keys (OpenWeatherMap, PredictHQ)
- [ ] Load pilot city data (6 cities)
- [ ] Run database migrations
- [ ] Verify vector collection exists

### Workflow Import
- [ ] Import workflow YAML into Wrk.Flo
- [ ] Configure node connections
- [ ] Set node-specific settings (model, tokens, temperature)
- [ ] Test each node individually
- [ ] Test end-to-end workflow with sample input
- [ ] Verify cost tracking
- [ ] Verify database writes

### Post-Deployment
- [ ] Monitor first 10 trips for errors
- [ ] Verify A/B test variant assignment (50/50 split)
- [ ] Check Prometheus metrics dashboard
- [ ] Set up alerting rules
- [ ] Document any production issues

---

## Testing Scenarios

### Test Case 1: Happy Path
**Input:**
```json
{
  "preferences": {
    "vibes": ["local", "food", "nightlife"],
    "interests": ["food", "drink", "culture"],
    "budget_level": "mid"
  },
  "travel_dates": {
    "start": "2024-07-01",
    "end": "2024-07-07"
  },
  "candidate_cities": ["Lisbon", "Barcelona", "Tokyo"],
  "user_id": "test-user-1"
}
```

**Expected Output:**
- Workflow completes in < 70 seconds
- Returns 7-day itinerary for top-ranked city
- Cost < $0.50
- Variant assigned (control or slow_hidden_gems)
- Trip saved to database

### Test Case 2: Invalid Input
**Input:**
```json
{
  "preferences": {
    "vibes": ["local"],
    "interests": ["food"],
    "budget_level": "ultra_luxury"
  },
  "travel_dates": {
    "start": "2024-01-01",
    "end": "2024-01-15"
  }
}
```

**Expected Output:**
- Node 1 returns validation errors
- Workflow stops after Intent Parser
- No LLM cost for Nodes 2-5
- Error message: "Budget level must be low, mid, or high"

### Test Case 3: API Failures
**Scenario**: OpenWeatherMap and PredictHQ both down

**Expected Behavior:**
- Nodes 4a, 4b use mock data
- Workflow continues to Node 5 (Concierge)
- Itinerary includes weather estimates flagged as "estimated"
- Completion time < 80 seconds (no API delays)

### Test Case 4: Cost Overrun
**Scenario**: Budget already at $0.75 before Node 5

**Expected Behavior:**
- Node 5 reduces max_tokens to 15000 (minimal strategy)
- Vector chunks reduced to 10
- Itinerary shorter but still valid
- Total cost stays under $0.80

---

## Integration with External Systems

### REST API Endpoint
```
POST /api/v1/trips/create
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "preferences": {...},
  "travel_dates": {...},
  "candidate_cities": [...]
}

Response (200 OK):
{
  "trip_id": "uuid",
  "variant": "slow_hidden_gems",
  "itinerary": {...},
  "cost_usd": 0.52,
  "execution_time_seconds": 58
}
```

### Webhook for Feedback (Node 7)
```
POST /webhooks/feedback-received
Content-Type: application/json

{
  "trip_id": "uuid",
  "feedback": {...}
}

Triggers: Node 7 processing (async)
```

### Grafana Dashboard Integration
- Workflow metrics exposed at `/metrics`
- Prometheus scrapes every 15 seconds
- Grafana dashboards auto-refresh every 30 seconds

---

## Version History

**v1.0.0** (Current)
- Initial production deployment
- 8 nodes (Intent, City Selection, Local Expert, Weather, Events, Concierge, Post-Processor, Feedback)
- A/B testing with 2 variants
- Cost controls with degradation strategy

**Planned for v1.1.0**
- Node 8: Activity Booking Tool (optional reservations)
- Node 9: Translation Tool (non-English cities)
- Multi-language support (Spanish, Portuguese, Japanese)
- Dynamic variant allocation (multi-armed bandit)

---

## Support & Troubleshooting

### Common Issues

**Issue**: "Workflow timeout after 120 seconds"
- **Cause**: Node 5 (Concierge) taking too long
- **Fix**: Check if max_tokens too high, reduce to 25000

**Issue**: "Cost exceeds $0.80 per trip"
- **Cause**: Degradation strategy not triggering
- **Fix**: Verify `CostController` is called before Node 5

**Issue**: "Variant split is 60/40 instead of 50/50"
- **Cause**: Sample size too small or hash collision
- **Fix**: Verify MD5 hash implementation, check trip_id format

**Issue**: "Vector search returns no results"
- **Cause**: City data not loaded or collection missing
- **Fix**: Run `scripts/load_pilot_cities.py`, verify ChromaDB connection

### Debugging Tools
- **Workflow Logs**: `/var/log/timbuktoo/workflow.log`
- **Node Traces**: Enable `LOG_LEVEL=DEBUG` to see full LLM responses
- **Cost Breakdown**: Query `cost_tracking` table by `trip_id`
- **A/B Test Status**: `GET /api/v1/experiments/status`

---

## Conclusion

This Wrk.Flo wiring spec provides a complete, production-ready configuration for the Timbuktoo Travel Concierge workflow. All nodes are optimized for cost, latency, and error resilience.

**Key Takeaways:**
- Sequential execution with parallel tool calls (Nodes 4a, 4b)
- Deterministic A/B testing with variant injection
- Comprehensive error handling and fallback strategies
- Cost controls with automatic degradation
- Async feedback loop for continuous learning

**Next Steps:**
1. Import this spec into Wrk.Flo UI
2. Configure node credentials and API keys
3. Test with sample inputs
4. Deploy to production
5. Monitor metrics and iterate

For questions or issues, contact:
- **Engineering**: engineering@timbuktoo.ai
- **Slack**: #wrkflo-support
