# Cost Dashboards - Timbuktoo Travel Concierge

FinOps-ready monitoring and anomaly detection for AI agent costs.

---

## Dashboard Overview

Three production dashboards for comprehensive cost visibility:

1. **Dashboard A: Cost per Trip** - Token usage and cost breakdown by agent
2. **Dashboard B: Cost vs Quality** - ROI analysis and satisfaction correlation
3. **Dashboard C: Budget Guardrails** - Real-time budget enforcement and degradation

---

## Dashboard A: Cost per Trip

**Purpose**: Track per-trip costs across all agents and tools
**Refresh Rate**: Real-time (30-second intervals)
**Data Source**: `cost_tracking` table + Prometheus metrics

### Panel 1: Average Cost per Trip (Last 7 Days)

**Metric**: `avg(trip_cost_usd)`
**Visualization**: Single Stat with trend line

```sql
SELECT
  DATE_TRUNC('day', created_at) as date,
  AVG(total_cost_usd) as avg_cost,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_cost_usd) as median_cost,
  PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY total_cost_usd) as p95_cost
FROM trips
WHERE created_at >= NOW() - INTERVAL '7 days'
GROUP BY date
ORDER BY date;
```

**Thresholds**:
- Green: < $0.50
- Yellow: $0.50 - $0.70
- Red: > $0.70

**Current Target**: $0.35 average, $0.80 max

---

### Panel 2: Cost Breakdown by Agent

**Metric**: `sum(cost_usd) GROUP BY agent_type`
**Visualization**: Stacked Bar Chart

```sql
SELECT
  agent_type,
  SUM(input_tokens) as total_input_tokens,
  SUM(output_tokens) as total_output_tokens,
  SUM(cost_usd) as total_cost,
  COUNT(*) as execution_count,
  AVG(cost_usd) as avg_cost_per_execution
FROM cost_tracking
WHERE created_at >= NOW() - INTERVAL '7 days'
GROUP BY agent_type
ORDER BY total_cost DESC;
```

**Expected Distribution**:
- Travel Concierge: ~71% ($0.25)
- Local Expert: ~23% ($0.08)
- City Selection: ~6% ($0.02)
- Intent Parser: <1% ($0.0001)

**Anomaly Alert**: If any agent exceeds expected % by >20%

---

### Panel 3: Token Usage per Agent (7-Day Rolling Average)

**Metric**: `avg(input_tokens + output_tokens) BY agent_type`
**Visualization**: Line Chart (multi-series)

```prometheus
# Prometheus Query
avg_over_time(timbuktoo_agent_tokens_total{agent_type=~"city_selection|local_expert|concierge"}[7d])
```

**Baselines**:
- City Selection: 2,700 tokens (1,500 input + 1,200 output)
- Local Expert: 11,000 tokens (6,000 input + 5,000 output)
- Travel Concierge: 25,000 tokens (10,000 input + 15,000 output)

**Alert**: Token spike >25% above baseline for >1 hour

---

### Panel 4: Cost per Trip by Variant

**Metric**: `avg(total_cost_usd) GROUP BY variant`
**Visualization**: Bar Chart with comparison

```sql
SELECT
  variant,
  COUNT(*) as trip_count,
  AVG(total_cost_usd) as avg_cost,
  STDDEV(total_cost_usd) as cost_stddev,
  MIN(total_cost_usd) as min_cost,
  MAX(total_cost_usd) as max_cost
FROM trips
WHERE created_at >= NOW() - INTERVAL '7 days'
GROUP BY variant;
```

**Expected Similarity**: Control and Slow Hidden Gems should have <5% cost difference

**Alert**: If variant cost delta >10%

---

### Panel 5: Daily Cost Trend

**Metric**: `sum(total_cost_usd) GROUP BY date`
**Visualization**: Area Chart

```sql
SELECT
  DATE_TRUNC('day', created_at) as date,
  COUNT(*) as trip_count,
  SUM(total_cost_usd) as daily_cost,
  AVG(total_cost_usd) as avg_trip_cost
FROM trips
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY date
ORDER BY date;
```

**Budget Projection**: `daily_cost * 30` → Monthly forecast

**Alert**: If daily_cost > $100 (assumes ~200 trips/day at $0.50 avg)

---

### Panel 6: Top 10 Most Expensive Trips

**Metric**: Top trips by `total_cost_usd`
**Visualization**: Table

```sql
SELECT
  trip_id,
  city,
  variant,
  total_cost_usd,
  created_at,
  feedback_overall_rating
FROM trips
WHERE created_at >= NOW() - INTERVAL '7 days'
ORDER BY total_cost_usd DESC
LIMIT 10;
```

**Columns**:
- Trip ID (clickable to drill-down)
- City
- Variant
- Cost (USD)
- Timestamp
- User Rating (if available)

**Action**: Investigate trips >$0.70 for degradation failures

---

## Dashboard B: Cost vs Quality

**Purpose**: Analyze ROI and identify low-value high-cost trips
**Refresh Rate**: Hourly
**Data Source**: `trips` JOIN `feedback`

### Panel 1: Cost vs Satisfaction Scatter Plot

**Metric**: `(total_cost_usd, feedback_overall_rating)`
**Visualization**: Scatter Plot with quadrant lines

```sql
SELECT
  t.trip_id,
  t.total_cost_usd,
  f.overall_rating,
  t.variant,
  t.city
FROM trips t
LEFT JOIN feedback f ON t.trip_id = f.trip_id
WHERE t.created_at >= NOW() - INTERVAL '30 days'
  AND f.overall_rating IS NOT NULL;
```

**Quadrants**:
- **Top Left** (Low Cost, High Rating): Optimal
- **Top Right** (High Cost, High Rating): Acceptable
- **Bottom Left** (Low Cost, Low Rating): Quality issue
- **Bottom Right** (High Cost, Low Rating): **RED FLAG** - worst ROI

**Alert**: If >5% of trips fall in Bottom Right quadrant

---

### Panel 2: Average Rating by Cost Tier

**Metric**: `avg(overall_rating) GROUP BY cost_tier`
**Visualization**: Bar Chart

```sql
SELECT
  CASE
    WHEN total_cost_usd < 0.30 THEN 'Low (<$0.30)'
    WHEN total_cost_usd < 0.50 THEN 'Medium ($0.30-$0.50)'
    WHEN total_cost_usd < 0.70 THEN 'High ($0.50-$0.70)'
    ELSE 'Very High (>$0.70)'
  END as cost_tier,
  COUNT(*) as trip_count,
  AVG(f.overall_rating) as avg_rating,
  AVG(f.pacing_rating) as avg_pacing_rating
FROM trips t
LEFT JOIN feedback f ON t.trip_id = f.trip_id
WHERE t.created_at >= NOW() - INTERVAL '30 days'
  AND f.overall_rating IS NOT NULL
GROUP BY cost_tier
ORDER BY cost_tier;
```

**Hypothesis**: Higher cost should correlate with higher quality (or no correlation)

**Alert**: If Low tier outperforms High tier by >0.3 rating points

---

### Panel 3: Regeneration Rate

**Metric**: `regenerations / total_trips`
**Visualization**: Single Stat with history

```sql
SELECT
  COUNT(CASE WHEN regeneration_count >= 1 THEN 1 END)::float / COUNT(*) as regeneration_rate,
  AVG(regeneration_count) as avg_regenerations
FROM trips
WHERE created_at >= NOW() - INTERVAL '7 days';
```

**Target**: <2% regeneration rate

**Alert**: If rate >5%

**Cost Impact**: Each regeneration doubles cost (~$0.70 total for 2 attempts)

---

### Panel 4: Satisfaction by Variant

**Metric**: `avg(overall_rating) GROUP BY variant`
**Visualization**: Bar Chart with error bars (stddev)

```sql
SELECT
  t.variant,
  COUNT(*) as trip_count,
  AVG(f.overall_rating) as avg_overall_rating,
  STDDEV(f.overall_rating) as rating_stddev,
  AVG(f.pacing_rating) as avg_pacing_rating,
  AVG(CASE WHEN f.pacing_feedback LIKE '%too fast%' THEN 1 ELSE 0 END) as pacing_complaint_rate
FROM trips t
LEFT JOIN feedback f ON t.trip_id = f.trip_id
WHERE t.created_at >= NOW() - INTERVAL '30 days'
  AND f.overall_rating IS NOT NULL
GROUP BY t.variant;
```

**A/B Test Success Criteria**:
- Winner: Overall rating +10% AND pacing complaints -20%
- Sample size: ≥100 trips per variant

---

### Panel 5: Completion Rate by Cost Tier

**Metric**: `completed_days / 7`
**Visualization**: Box Plot

```sql
SELECT
  CASE
    WHEN total_cost_usd < 0.40 THEN 'Low'
    WHEN total_cost_usd < 0.60 THEN 'Medium'
    ELSE 'High'
  END as cost_tier,
  AVG(f.completion_estimate) as avg_completion_rate,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY f.completion_estimate) as median_completion
FROM trips t
LEFT JOIN feedback f ON t.trip_id = f.trip_id
WHERE f.completion_estimate IS NOT NULL
GROUP BY cost_tier;
```

**Hypothesis**: Higher cost should NOT significantly improve completion rate

**Alert**: If correlation coefficient >0.3 (means we're overspending)

---

### Panel 6: Low ROI Trips (Table)

**Metric**: Trips with cost >$0.60 AND rating <3.5
**Visualization**: Table with drill-down

```sql
SELECT
  t.trip_id,
  t.city,
  t.variant,
  t.total_cost_usd,
  f.overall_rating,
  f.pacing_rating,
  f.authenticity_rating,
  f.text_feedback
FROM trips t
JOIN feedback f ON t.trip_id = f.trip_id
WHERE t.total_cost_usd > 0.60
  AND f.overall_rating < 3.5
  AND t.created_at >= NOW() - INTERVAL '30 days'
ORDER BY t.total_cost_usd DESC;
```

**Action**: Review these trips for prompt failures or degradation issues

---

## Dashboard C: Budget Guardrails

**Purpose**: Real-time cost enforcement and degradation monitoring
**Refresh Rate**: Real-time (10-second intervals)
**Data Source**: `cost_tracking` + in-memory cost controller state

### Panel 1: Current Month Burn Rate

**Metric**: `sum(total_cost_usd) for current month`
**Visualization**: Single Stat with monthly budget gauge

```sql
SELECT
  SUM(total_cost_usd) as month_to_date_cost,
  COUNT(*) as trips_created,
  AVG(total_cost_usd) as avg_trip_cost,
  (SUM(total_cost_usd) / EXTRACT(DAY FROM NOW())) * 30 as projected_monthly_cost
FROM trips
WHERE created_at >= DATE_TRUNC('month', NOW());
```

**Monthly Budget**: $15,000 (assumes 30,000 trips/month at $0.50 avg)

**Thresholds**:
- Green: <70% of budget
- Yellow: 70-90% of budget
- Red: >90% of budget

---

### Panel 2: Budget Headroom per Trip

**Metric**: `$0.80 - current_cost` during trip execution
**Visualization**: Gauge (real-time)

```python
# Pseudo-code for real-time metric
def get_current_trip_headroom(trip_id):
    current_cost = sum(cost_tracking WHERE trip_id = trip_id)
    headroom = 0.80 - current_cost
    return {
        "headroom_usd": headroom,
        "headroom_pct": (headroom / 0.80) * 100,
        "degradation_tier": get_degradation_tier(headroom)
    }
```

**Degradation Tiers**:
- Normal: ≥$0.50 remaining (green)
- Reduced: $0.30-$0.49 remaining (yellow)
- Minimal: $0.10-$0.29 remaining (orange)
- Critical: <$0.10 remaining (red)

---

### Panel 3: Degradation Strategy Usage

**Metric**: `COUNT(*) GROUP BY degradation_tier`
**Visualization**: Stacked Area Chart

```sql
SELECT
  DATE_TRUNC('hour', created_at) as hour,
  degradation_strategy,
  COUNT(*) as trip_count
FROM trips
WHERE created_at >= NOW() - INTERVAL '24 hours'
GROUP BY hour, degradation_strategy
ORDER BY hour;
```

**Expected Distribution**:
- Normal: 85%
- Reduced: 10%
- Minimal: 5%

**Alert**: If Minimal >10% for >2 hours

---

### Panel 4: Token Cap Adherence

**Metric**: `actual_tokens / token_cap`
**Visualization**: Histogram

```sql
SELECT
  agent_type,
  COUNT(*) as execution_count,
  AVG((input_tokens + output_tokens)::float / CASE
    WHEN agent_type = 'city_selection' THEN 4000
    WHEN agent_type = 'local_expert' THEN 22000
    WHEN agent_type = 'concierge' THEN 38000
  END) as avg_token_utilization
FROM cost_tracking
WHERE created_at >= NOW() - INTERVAL '24 hours'
GROUP BY agent_type;
```

**Target**: 70-85% token cap utilization (sweet spot)

**Alert**: If >95% utilization (near cap, may truncate) OR <50% (over-provisioned)

---

### Panel 5: Cache Hit Rate

**Metric**: `cache_hits / (cache_hits + cache_misses)`
**Visualization**: Line Chart

```prometheus
# Prometheus Query
rate(timbuktoo_cache_hits_total[5m]) /
(rate(timbuktoo_cache_hits_total[5m]) + rate(timbuktoo_cache_misses_total[5m]))
```

**Breakdown by Cache Type**:
- Weather forecasts: Target 80% (1-hour TTL)
- Events data: Target 90% (24-hour TTL)
- City guides: Target 60% (1-hour TTL)

**Cost Impact**: Cache miss → extra API call or LLM invocation

**Alert**: If overall rate <50% for >1 hour

---

### Panel 6: Cost Anomaly Alerts (Live Feed)

**Metric**: Real-time anomaly detection rules
**Visualization**: Table with auto-refresh

```sql
-- Rule 1: Token Spike
SELECT 'TOKEN_SPIKE' as alert_type, trip_id, agent_type,
       current_tokens, rolling_7d_avg, (current_tokens / rolling_7d_avg - 1) * 100 as spike_pct
FROM (
  SELECT ct.trip_id, ct.agent_type,
         ct.input_tokens + ct.output_tokens as current_tokens,
         AVG(ct2.input_tokens + ct2.output_tokens) OVER (
           PARTITION BY ct.agent_type
           ORDER BY ct2.created_at
           ROWS BETWEEN 168 PRECEDING AND 1 PRECEDING
         ) as rolling_7d_avg
  FROM cost_tracking ct
  JOIN cost_tracking ct2 ON ct.agent_type = ct2.agent_type
  WHERE ct.created_at >= NOW() - INTERVAL '1 hour'
) sub
WHERE current_tokens > rolling_7d_avg * 1.25

UNION ALL

-- Rule 2: Low ROI Trip
SELECT 'LOW_ROI_TRIP' as alert_type, t.trip_id, t.variant,
       t.total_cost_usd, f.overall_rating, NULL as spike_pct
FROM trips t
JOIN feedback f ON t.trip_id = f.trip_id
WHERE t.total_cost_usd > 0.60
  AND f.overall_rating < 4.0
  AND t.created_at >= NOW() - INTERVAL '1 hour'

UNION ALL

-- Rule 3: Regeneration Loop
SELECT 'PROMPT_FAILURE' as alert_type, trip_id, NULL,
       regeneration_count, NULL, NULL
FROM trips
WHERE regeneration_count >= 2
  AND created_at >= NOW() - INTERVAL '1 hour'

UNION ALL

-- Rule 4: Cache Miss Surge
SELECT 'CACHE_DEGRADATION' as alert_type, NULL, NULL, NULL, NULL,
       (1 - cache_hit_rate) * 100 as miss_rate_pct
FROM (
  SELECT AVG(CASE WHEN cache_hit THEN 1 ELSE 0 END) as cache_hit_rate
  FROM cache_metrics
  WHERE timestamp >= NOW() - INTERVAL '24 hours'
) sub
WHERE cache_hit_rate < 0.50

UNION ALL

-- Rule 5: Tool Overuse
SELECT 'TOOL_OVERUSE' as alert_type, trip_id, NULL,
       tool_call_count, expected_baseline, (tool_call_count - expected_baseline) as excess_calls
FROM (
  SELECT trip_id,
         COUNT(*) as tool_call_count,
         2 as expected_baseline  -- Weather + Events
  FROM tool_executions
  WHERE created_at >= NOW() - INTERVAL '1 hour'
  GROUP BY trip_id
) sub
WHERE tool_call_count > expected_baseline + 1;
```

**Alert Actions**:
- TOKEN_SPIKE → Log + Alert + Downgrade retrieval depth
- LOW_ROI_TRIP → Route to cheaper variant
- PROMPT_FAILURE → Freeze agent version + Notify engineering
- CACHE_DEGRADATION → Warm cache + Throttle new trips
- TOOL_OVERUSE → Force cached response

---

## Cost Anomaly Detection Rules (Detailed)

### Rule 1: Token Spike

**Condition**: `agent_tokens > rolling_7d_avg(agent_tokens) * 1.25`

**Implementation**:
```python
def check_token_spike(agent_type: str, current_tokens: int) -> bool:
    rolling_avg = get_rolling_avg_tokens(agent_type, days=7)
    spike_threshold = rolling_avg * 1.25

    if current_tokens > spike_threshold:
        log_anomaly("TOKEN_SPIKE", {
            "agent_type": agent_type,
            "current_tokens": current_tokens,
            "baseline_avg": rolling_avg,
            "spike_pct": ((current_tokens / rolling_avg) - 1) * 100
        })

        # Auto-remediation
        if agent_type == "local_expert":
            reduce_vector_chunks(from=35, to=20)
        elif agent_type == "concierge":
            reduce_max_tokens(from=38000, to=25000)

        return True
    return False
```

**Alert Destination**: Slack #cost-alerts, PagerDuty (if spike >50%)

---

### Rule 2: Cost vs Satisfaction

**Condition**: `trip_cost > p75_cost AND satisfaction < 4.0`

**Implementation**:
```python
def check_low_roi_trip(trip_id: str):
    trip = get_trip(trip_id)
    feedback = get_feedback(trip_id)

    p75_cost = get_percentile_cost(75)  # ~$0.55

    if trip.total_cost_usd > p75_cost and feedback.overall_rating < 4.0:
        log_anomaly("LOW_ROI_TRIP", {
            "trip_id": trip_id,
            "cost": trip.total_cost_usd,
            "rating": feedback.overall_rating,
            "variant": trip.variant
        })

        # Auto-remediation: Route future trips for this user to cheaper variant
        if trip.variant == "slow_hidden_gems":
            switch_user_to_variant(trip.user_id, "control")
```

**Alert Destination**: Weekly digest to product team

---

### Rule 3: Regeneration Loop

**Condition**: `regenerations_per_trip >= 2`

**Implementation**:
```python
def check_regeneration_loop(trip_id: str):
    trip = get_trip(trip_id)

    if trip.regeneration_count >= 2:
        log_anomaly("PROMPT_FAILURE", {
            "trip_id": trip_id,
            "regeneration_count": trip.regeneration_count,
            "total_cost": trip.total_cost_usd,
            "agent_version": trip.agent_version
        })

        # Auto-remediation: Freeze problematic agent version
        freeze_agent_version(trip.agent_version)
        send_alert("engineering", severity="HIGH")
```

**Alert Destination**: PagerDuty → Engineering on-call

---

### Rule 4: Cache Miss Surge

**Condition**: `cache_hit_rate < 50% for 24h`

**Implementation**:
```python
def check_cache_degradation():
    cache_hit_rate = calculate_cache_hit_rate(hours=24)

    if cache_hit_rate < 0.50:
        log_anomaly("CACHE_DEGRADATION", {
            "cache_hit_rate": cache_hit_rate,
            "weather_cache_misses": get_cache_misses("weather"),
            "events_cache_misses": get_cache_misses("events"),
            "city_guide_cache_misses": get_cache_misses("city_guide")
        })

        # Auto-remediation: Warm cache + throttle
        warm_cache_for_popular_cities()
        enable_throttling(max_trips_per_minute=5)
```

**Alert Destination**: Slack #infra-alerts

---

### Rule 5: Tool Overuse

**Condition**: `tool_calls > expected_baseline + 1`

**Implementation**:
```python
def check_tool_overuse(trip_id: str):
    tool_calls = count_tool_calls(trip_id)
    expected = 2  # Weather + Events

    if tool_calls > expected + 1:
        log_anomaly("TOOL_OVERUSE", {
            "trip_id": trip_id,
            "tool_call_count": tool_calls,
            "expected_baseline": expected,
            "excess_calls": tool_calls - expected
        })

        # Auto-remediation: Force cached responses for next trip
        enable_aggressive_caching(duration_minutes=60)
```

**Alert Destination**: Log only (low severity)

---

## Prometheus Metrics Export

### Agent Cost Metrics
```prometheus
# Total cost by agent type
timbuktoo_agent_cost_usd_total{agent_type="city_selection|local_expert|concierge"}

# Token usage
timbuktoo_agent_tokens_total{agent_type="...", token_type="input|output"}

# Execution count
timbuktoo_agent_executions_total{agent_type="...", status="success|failure"}
```

### Trip Cost Metrics
```prometheus
# Cost per trip
timbuktoo_trip_cost_usd{variant="control|slow_hidden_gems", city="..."}

# Degradation strategy usage
timbuktoo_degradation_strategy_total{strategy="normal|reduced|minimal"}

# Regeneration rate
timbuktoo_trip_regenerations_total{reason="user_request|quality_failure"}
```

### Cache Metrics
```prometheus
# Cache hit rate
timbuktoo_cache_hits_total{cache_type="weather|events|city_guide"}
timbuktoo_cache_misses_total{cache_type="weather|events|city_guide"}

# Cache size
timbuktoo_cache_entries_count{cache_type="..."}
```

### Budget Metrics
```prometheus
# Monthly burn rate
timbuktoo_monthly_cost_usd{month="2024-06"}

# Budget headroom
timbuktoo_budget_headroom_usd{tier="normal|reduced|minimal"}

# Cost anomalies
timbuktoo_cost_anomalies_total{alert_type="token_spike|low_roi|prompt_failure|cache_degradation|tool_overuse"}
```

---

## Grafana Dashboard JSON Export

```json
{
  "dashboard": {
    "title": "Timbuktoo Cost Monitoring",
    "tags": ["cost", "finops", "ai"],
    "timezone": "utc",
    "panels": [
      {
        "id": 1,
        "title": "Average Cost per Trip",
        "type": "stat",
        "targets": [
          {
            "expr": "avg(timbuktoo_trip_cost_usd)",
            "legendFormat": "Avg Cost"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                {"value": 0, "color": "green"},
                {"value": 0.50, "color": "yellow"},
                {"value": 0.70, "color": "red"}
              ]
            },
            "unit": "currencyUSD"
          }
        }
      },
      {
        "id": 2,
        "title": "Cost Breakdown by Agent",
        "type": "barchart",
        "targets": [
          {
            "expr": "sum(timbuktoo_agent_cost_usd_total) by (agent_type)",
            "legendFormat": "{{agent_type}}"
          }
        ]
      }
    ],
    "refresh": "30s"
  }
}
```

---

## Alert Rules (PagerDuty / Slack Integration)

### Critical Alerts (PagerDuty)
```yaml
- alert: HighCostTrips
  expr: timbuktoo_trip_cost_usd > 0.75
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Trip cost exceeding $0.75"

- alert: PromptFailureLoop
  expr: rate(timbuktoo_trip_regenerations_total[5m]) > 0.05
  for: 10m
  labels:
    severity: critical
  annotations:
    summary: "Regeneration rate >5%"
```

### Warning Alerts (Slack)
```yaml
- alert: TokenSpike
  expr: timbuktoo_agent_tokens_total > (avg_over_time(timbuktoo_agent_tokens_total[7d]) * 1.25)
  for: 15m
  labels:
    severity: warning
  annotations:
    summary: "Token usage 25% above baseline"

- alert: CacheDegradation
  expr: rate(timbuktoo_cache_hits_total[1h]) / (rate(timbuktoo_cache_hits_total[1h]) + rate(timbuktoo_cache_misses_total[1h])) < 0.50
  for: 1h
  labels:
    severity: warning
  annotations:
    summary: "Cache hit rate below 50%"
```

---

## Environment-Specific Configs

### Development
```yaml
cost_controls:
  hard_trip_cap_usd: 1.50
  degradation_thresholds:
    high: 0.50
    low: 0.20
  alert_webhooks:
    enabled: false
```

### Staging
```yaml
cost_controls:
  hard_trip_cap_usd: 1.00
  degradation_thresholds:
    high: 0.40
    low: 0.15
  alert_webhooks:
    slack: "https://hooks.slack.com/services/STAGE"
    enabled: true
```

### Production
```yaml
cost_controls:
  hard_trip_cap_usd: 0.80
  degradation_thresholds:
    high: 0.30
    low: 0.10
  alert_webhooks:
    slack: "https://hooks.slack.com/services/PROD"
    pagerduty: "https://events.pagerduty.com/v2/enqueue"
    enabled: true
```

---

## Monthly Cost Reporting

### Executive Summary (Automated Email)

**Template**:
```
Subject: Timbuktoo Monthly Cost Report - June 2024

Summary:
- Total Trips: 28,450
- Total Cost: $14,225 ($0.50 avg)
- Budget: $15,000 (95% utilized)
- Savings: $775 from degradation strategy

Breakdown by Variant:
- Control: 14,120 trips @ $0.49 avg
- Slow Hidden Gems: 14,330 trips @ $0.51 avg

Top Insights:
- Cache hit rate improved to 78% (+12% MoM)
- Regeneration rate decreased to 1.2% (-0.8% MoM)
- 92% of trips stayed under $0.60

Anomalies Detected:
- 3 token spike events (auto-remediated)
- 12 low-ROI trips flagged for review
- 1 cache degradation incident (June 15, 14:00-16:00 UTC)

Recommendations:
- Increase weather cache TTL from 1h to 6h (save ~$50/month)
- Investigate Local Expert token usage (trending +8% MoM)
```

**Recipients**: Finance, Product, Engineering leads

---

## Conclusion

These three dashboards provide comprehensive cost visibility:

1. **Dashboard A**: Operational view for daily monitoring
2. **Dashboard B**: Product view for ROI optimization
3. **Dashboard C**: Engineering view for real-time guardrails

All dashboards are FinOps-ready with automated anomaly detection, alerting, and remediation.

**Next Steps**:
1. Import Grafana dashboard JSON
2. Configure Prometheus scraping
3. Set up PagerDuty / Slack webhooks
4. Enable cost anomaly rules
5. Schedule monthly reports
