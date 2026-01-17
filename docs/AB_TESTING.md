# A/B Testing Framework for Timbuktoo

Complete experimentation framework for itinerary pacing and content optimization.

---

## Overview

Timbuktoo uses rigorous A/B testing to optimize travel itineraries for user satisfaction. The framework enables us to test different pacing strategies, content mixes, and recommendation algorithms.

## Experiment Dimensions

### Primary Variants

#### Variant A: Control (Balanced Pacing)
**Characteristics:**
- 2-3 major activities per day
- 60% local spots, 40% popular landmarks
- Moderate walking distance (2-4km/day)
- Structured morning/afternoon, flexible evening
- Mix of indoor and outdoor activities

**Target Audience:**
- First-time city visitors
- Users seeking comprehensive overview
- Travelers with limited time
- Moderate energy levels

**Expected Outcomes:**
- Higher activity completion rate
- Balanced satisfaction across days
- Lower "too slow" complaints

---

#### Variant B: Slow Hidden Gems (Deep Immersion)
**Characteristics:**
- 1-2 major activities per day
- 90% hidden gems, 10% optional landmarks
- Shorter distances but deeper experiences
- Lots of unstructured "discovery" time
- Emphasis on lingering vs. seeing everything

**Target Audience:**
- Repeat city visitors
- Users seeking authentic local experience
- Digital nomads / longer stays
- High cultural curiosity

**Expected Outcomes:**
- Higher authenticity ratings
- Lower "too busy" complaints
- Potential for higher overall satisfaction
- More user edits (personalization)

---

## Randomization Strategy

### Unit of Randomization
- **Trip ID** (not user ID)
- Each trip independently randomized
- Allows same user to experience both variants

### Assignment Method
```python
import hashlib

def assign_variant(trip_id: str) -> str:
    """
    Deterministic variant assignment based on trip_id
    Ensures 50/50 split
    """
    hash_val = int(hashlib.md5(trip_id.encode()).hexdigest(), 16)
    return "slow_hidden_gems" if hash_val % 2 == 0 else "control"
```

### Stratification
Stratify by:
- City (ensure balance across destinations)
- User budget tier (starter/pro/enterprise)
- Trip duration (7 days standard)

---

## Metrics Framework

### Primary Metrics

#### Overall Itinerary Rating
- **Measurement**: 1-5 star rating
- **Collection Point**: Post-trip feedback form
- **Success Criteria**: Slow Hidden Gems shows +10% improvement

#### Completion Rate
- **Measurement**: % of activities actually done
- **Collection Point**: Daily check-ins or post-trip survey
- **Success Criteria**: No significant degradation (<5% drop)

---

### Secondary Metrics

#### Day-Level Satisfaction Variance
- **Measurement**: Standard deviation of daily ratings
- **Why**: Lower variance = more consistent experience
- **Collection Point**: Daily feedback

#### User Edit Rate
- **Measurement**: % of users who edit/regenerate itinerary
- **Why**: High edits may indicate poor initial fit
- **Collection Point**: Workflow logs

#### "Too Busy" / "Too Slow" Flags
- **Measurement**: Count of pacing complaints
- **Success Criteria**: Slow variant shows -20% "too busy" complaints
- **Collection Point**: Free-text comment analysis

#### Entity-Level Engagement
- **Measurement**: Which recommendations were followed
- **Why**: Understand which types of places resonate
- **Collection Point**: Post-trip "places visited" checkboxes

---

### Guardrail Metrics

Monitor for unintended negative effects:

| Metric | Threshold | Action if Breached |
|--------|-----------|-------------------|
| Completion Rate | <70% | Pause variant |
| Avg Rating | <3.5 stars | Review variant logic |
| Cost Overrun | >$1.00/trip | Investigate efficiency |
| Error Rate | >5% | Technical investigation |

---

## Data Collection

### Feedback Survey Structure

```json
{
  "trip_id": "uuid",
  "variant": "control",
  "feedback_submitted_at": "2024-06-15T10:00:00Z",

  "overall_rating": 5,
  "pacing_rating": 4,
  "authenticity_rating": 5,
  "value_rating": 4,

  "daily_ratings": {
    "day1": 5,
    "day2": 4,
    "day3": 5,
    "day4": 5,
    "day5": 4,
    "day6": 5,
    "day7": 5
  },

  "liked_entities": ["entity_uuid_1", "entity_uuid_2"],
  "disliked_entities": [],

  "pacing_feedback": "just_right",  // options: too_fast, too_slow, just_right

  "comments": "Loved the hidden gem recommendations! Park Bar was incredible. Felt like a local, not a tourist.",

  "would_recommend": true,
  "completion_estimate": 90  // % of activities completed
}
```

---

## Statistical Analysis Plan

### Sample Size Calculation

**Assumptions:**
- Baseline overall rating: 4.0/5
- Minimum detectable effect: 0.4 stars (10%)
- Significance level (α): 0.05
- Power (1-β): 0.80

**Required Sample:**
- **~100 trips per variant** for 80% power
- **~150 trips per variant** for 90% power

### Analysis Method

**Primary Analysis:**
- Two-sample t-test on overall_rating
- Bonferroni correction for multiple comparisons

**Secondary Analysis:**
- Chi-square test for pacing complaints
- Regression analysis controlling for city, budget tier

**Interim Analysis:**
- Check at N=50 per variant for early stopping
- Use O'Brien-Fleming spending function to control Type I error

---

## Rollout Strategy

### Phase 1: Internal Testing (Weeks 1-2)
- **Sample**: 10 internal test trips per variant
- **Goal**: Validate tracking, catch obvious bugs
- **Decision**: Proceed to Phase 2 if no critical issues

### Phase 2: Beta Users (Weeks 3-4)
- **Sample**: 25% of beta user traffic (~50 trips)
- **Goal**: Directional signal on metrics
- **Decision**: Early stopping if degradation > -15%

### Phase 3: Limited Rollout (Weeks 5-6)
- **Sample**: 50% control, 50% slow_hidden_gems
- **Goal**: Achieve full statistical power
- **Decision**: Launch winner at Week 7

### Phase 4: Winner Selection
- **Criteria**:
  - Overall rating improvement >5% AND p < 0.05
  - No guardrail metric breaches
  - Qualitative feedback positive
- **Action**:
  - If Slow Hidden Gems wins: Launch as default
  - If Control wins: Keep current
  - If neutral: Offer as user preference toggle

---

## Monitoring Dashboard

### Key Metrics (Real-Time)

```
┌─────────────────────────────────────────────┐
│  A/B Test: Pacing Experiment                │
│  Running: May 1 - Jun 15, 2024              │
├─────────────────────────────────────────────┤
│                                             │
│  CONTROL           vs.   SLOW HIDDEN GEMS   │
│                                             │
│  N = 127                     N = 131        │
│                                             │
│  Overall Rating:             │
│  4.1 ★                       4.5 ★          │
│                           ↑ +10% (p=0.03)   │
│                                             │
│  Pacing Complaints:          │
│  18%                         7%             │
│                           ↓ -61% (p=0.01)   │
│                                             │
│  Completion Rate:            │
│  78%                         74%            │
│                           ↓ -4% (p=0.22)    │
│                                             │
│  Cost per Trip:              │
│  $0.52                       $0.48          │
│                           ↓ -8%             │
│                                             │
└─────────────────────────────────────────────┘

STATUS: Slow Hidden Gems is WINNING
```

---

## Implementation

### Code Integration

```python
from timbuktoo.workflows.orchestrator import TravelOrchestrator
from timbuktoo.utils.ab_testing import assign_variant

# Create trip with variant assignment
trip_id = str(uuid.uuid4())
variant = assign_variant(trip_id)

orchestrator = TravelOrchestrator(variant=variant)
result = orchestrator.create_trip(
    preferences=preferences,
    travel_dates=travel_dates
)

# Track variant in trip record
# Variant is automatically saved in trip.variant_id
```

### Feedback Collection

```python
from timbuktoo.utils.feedback import get_feedback_collector

collector = get_feedback_collector()

# Collect feedback
feedback = collector.collect_feedback(
    trip_id=trip_id,
    overall_rating=5,
    pacing_rating=4,
    authenticity_rating=5,
    value_rating=4,
    pacing_feedback="just_right",
    comments="Loved the slow pace and hidden gems!",
    would_recommend=True
)

# Analytics automatically includes variant analysis
```

### Variant Performance Query

```sql
-- Compare variants
SELECT
    variant_id,
    COUNT(*) as trips_count,
    AVG(overall_rating) as avg_overall_rating,
    AVG(pacing_rating) as avg_pacing_rating,
    AVG(authenticity_rating) as avg_authenticity_rating,

    -- Pacing complaints
    SUM(CASE WHEN pacing_feedback = 'too_fast' THEN 1 ELSE 0 END) as too_fast_count,
    SUM(CASE WHEN pacing_feedback = 'too_slow' THEN 1 ELSE 0 END) as too_slow_count,

    -- Recommendation rate
    AVG(CASE WHEN would_recommend THEN 1.0 ELSE 0.0 END) as recommend_rate

FROM trips t
JOIN feedback f ON t.trip_id = f.trip_id
WHERE t.created_at >= '2024-05-01'
GROUP BY variant_id;
```

---

## Success Criteria

### Declare Winner If:

1. **Overall Rating**
   - Improvement ≥ 10% (e.g., 4.0 → 4.4)
   - Statistical significance: p < 0.05

2. **Pacing Complaints**
   - Reduction ≥ 20% in "too busy" complaints
   - No increase in "too slow" complaints

3. **Guardrails Met**
   - Completion rate ≥ 70%
   - Average rating ≥ 3.5 stars
   - No cost overruns

4. **Qualitative Validation**
   - Positive sentiment in free-text comments
   - No unexpected negative feedback themes

---

## Post-Experiment Actions

### If Slow Hidden Gems Wins:
1. ✅ Set as default variant for all new trips
2. ✅ Update agent prompts to emphasize hidden gems
3. ✅ Retrain recommendation weights
4. ✅ Archive Control as "Classic" variant (user-selectable)
5. ✅ Publish case study

### If Control Wins:
1. ✅ Keep current implementation
2. ✅ Iterate on Slow variant (reduce gaps)
3. ✅ Test "Moderate Hidden Gems" variant
4. ✅ Offer Slow as opt-in preference

### If Neutral (No Winner):
1. ✅ Offer both as user preferences
2. ✅ Run preference quiz during onboarding
3. ✅ Personalize based on user profile

---

## Future Experiments

### Experiment Queue

1. **Activity Mix Experiment**
   - A: Food-focused (70% food/drink)
   - B: Balanced (40% food, 30% culture, 30% nature)

2. **Neighborhood Depth**
   - A: Single neighborhood deep dive per day
   - B: Multi-neighborhood sampling

3. **Budget Optimization**
   - A: Conservative estimates (pad 20%)
   - B: Realistic estimates (actual costs)

4. **Meal Timing**
   - A: Local timing (9pm dinners)
   - B: Flexible (accommodate American schedules)

---

## Reporting

### Weekly Reports
- Variant performance vs. goals
- Guardrail metric checks
- Sample size progress
- Qualitative feedback highlights

### Final Report (End of Experiment)
- Executive summary
- Detailed statistical analysis
- User quotes and case studies
- Recommendation and next steps

---

## Questions?

For A/B testing questions:
- Email: experiments@timbuktoo.ai
- Slack: #ab-testing

For statistical consultation:
- Contact Data Science team
