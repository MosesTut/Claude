# Post-Launch Growth Experiments - Timbuktoo Mobile (90-Day Plan)

**Last Updated**: 2024-07-16
**Purpose**: App-Store-safe, measurable, low-risk growth experiments for first 90 days post-launch
**Status**: Production-Ready

This document provides 5 execution-ready growth experiments designed to optimize key conversion metrics while maintaining App Store compliance.

---

## Experiment Framework

### Success Criteria
- **Statistical Significance**: 95% confidence level (p < 0.05)
- **Minimum Sample Size**: 1,000 users per variant
- **Runtime**: 7-14 days per experiment
- **Guardrail Metrics**: Crash-free rate ≥ 99%, Day 7 retention ≥ baseline

### Prioritization
Experiments are prioritized by:
1. **Impact**: Expected improvement to North Star metric (Itinerary Generation Rate)
2. **Ease**: Engineering effort required (Story Points)
3. **Confidence**: Based on industry benchmarks and user research

---

## Experiment 1: First-Trip Completion Rate

**Priority**: P0 (Highest Impact)
**Timeline**: Week 1-2 post-launch
**Owner**: Product + Engineering

### Hypothesis
Reducing onboarding steps increases first itinerary generation rate by eliminating friction in the preference-setting flow.

**Theory**: New users are uncertain about their preferences and may abandon during a lengthy onboarding. Offering a "quick start" option with default preferences may increase completion.

### Variants

**Variant A (Control): Full Preference Flow**
- Onboarding: Welcome → AI Disclosure → Data Use → Preferences
- Preferences screen: 8 interests, food, budget, dates (all required)
- CTA: "Build My First Trip"
- Estimated time: 2-3 minutes

**Variant B (Test): Skip Preferences → Default Itinerary**
- Onboarding: Welcome → AI Disclosure → Data Use → Skip to City Recommendations
- No preference screen shown initially
- Default preferences applied:
  - Interests: Culture, Food (most popular based on research)
  - Budget: Medium
  - Dates: None (flexible)
- CTA: "Show Me Destinations"
- Estimated time: 1 minute
- **Note**: Users can edit preferences later via Settings

### Primary Metric
**First Itinerary Generation Rate**
- Definition: % of users who generate at least one itinerary within first session
- Baseline: 40% (industry benchmark for travel apps)
- Success Threshold: +15% lift (40% → 46%)

### Secondary Metrics
- Time to first itinerary (Control vs. Test)
- Preference completion rate (% who fill preferences after seeing first itinerary)
- Day 7 retention (guardrail - must not decrease)

### Guardrail Metrics
- Crash-free rate ≥ 99% (both variants)
- Day 7 retention ≥ baseline (Test should not harm retention)
- Itinerary quality rating (Helpful vs. Not Helpful) - Test should not decrease quality

### Implementation
```typescript
// Feature flag: skip_preferences_onboarding
if (featureFlags.skipPreferencesOnboarding) {
  // Variant B: Skip preferences
  const defaultPreferences = {
    interests: ['culture', 'food'],
    food: 'adventurous',
    budget: 'medium',
    dates: null
  };
  await savePreferences(userId, defaultPreferences);
  navigation.navigate('CityRecommendation');
} else {
  // Variant A: Full preference flow
  navigation.navigate('Preferences');
}
```

### Analysis Plan
**Week 1-2**: Run experiment (50/50 split, 1,000+ users per variant)
**Week 3**: Analyze results
- If Test wins (+15% or more): Ship Variant B to 100%
- If Test loses or neutral: Keep Variant A (full preference flow)

### Rollout Decision Tree
```
If Variant B wins:
  → Ship to 100% of users
  → Add "Edit Preferences" CTA after first itinerary
  → Monitor Day 7 retention for 2 weeks

If Variant B loses:
  → Keep Variant A (full preference flow)
  → Test shorter preference flow (reduce from 8 to 4 interests)
```

---

## Experiment 2: Paywall Timing

**Priority**: P0 (Revenue Impact)
**Timeline**: Week 3-4 post-launch
**Owner**: Product + Growth

### Hypothesis
Delaying the paywall until after the second itinerary (instead of first) increases trial start rate by allowing users to experience value before being asked to pay.

**Theory**: Users who generate 2+ itineraries are more engaged and more likely to convert. Showing the paywall too early may cause churn.

### Variants

**Variant A (Control): Paywall After First Itinerary**
- User generates 1st itinerary (free tier)
- User taps "Create Another Trip"
- Paywall shown: "You've used 1 of 3 free itineraries this month. Upgrade to Pro?"
- CTA: "Upgrade to Pro" / "Maybe Later"

**Variant B (Test): Paywall After Second Itinerary**
- User generates 1st itinerary (free tier)
- User taps "Create Another Trip" → No paywall, allow 2nd itinerary
- User generates 2nd itinerary (free tier)
- User taps "Create Another Trip" (3rd attempt)
- Paywall shown: "You've used 2 of 3 free itineraries this month. Upgrade to Pro?"
- CTA: "Upgrade to Pro" / "Continue with Free (1 left)"

### Primary Metric
**Trial Start Rate**
- Definition: % of users who start a free trial (tap "Start Free Trial" on paywall)
- Baseline: 10% (industry benchmark for freemium apps)
- Success Threshold: +20% lift (10% → 12%)

### Secondary Metrics
- Total revenue per user (ARPU) - must not decrease
- Day 7 retention (guardrail)
- Paywall view rate (% of users who see paywall)

### Guardrail Metrics
- Revenue per visitor ≥ baseline (total revenue ÷ total users)
  - Variant B may have lower trial start rate but higher conversion rate
  - Must optimize for total revenue, not just trial starts
- Day 30 retention ≥ baseline

### Implementation
```typescript
// Feature flag: delayed_paywall
const freeItinerariesUsed = await getItineraryUsage(userId);
const paywallThreshold = featureFlags.delayedPaywall ? 2 : 1;

if (freeItinerariesUsed >= paywallThreshold) {
  navigation.navigate('Paywall', { source: 'limit_reached' });
} else {
  // Allow itinerary generation
  navigation.navigate('CityRecommendation');
}
```

### Analysis Plan
**Week 3-4**: Run experiment (50/50 split, 2,000+ users per variant)
**Week 5**: Analyze results
- Compare trial start rate AND revenue per user
- If Variant B wins on both: Ship to 100%
- If Variant B wins on revenue but loses on trial starts: Ship to 100% (optimize for revenue)
- If Variant B loses on revenue: Keep Variant A

### Rollout Decision Tree
```
If Variant B wins (higher revenue):
  → Ship to 100% of users
  → Monitor revenue and retention for 30 days
  → Consider testing "Paywall After Third Itinerary" (next experiment)

If Variant B loses:
  → Keep Variant A (paywall after first itinerary)
  → Test alternative: "Paywall on Day 3" (time-based, not usage-based)
```

---

## Experiment 3: Screenshot-Driven Conversion

**Priority**: P1 (Acquisition Optimization)
**Timeline**: Week 5-6 post-launch
**Owner**: Product + Design + Growth

### Hypothesis
Leading with AI transparency in App Store screenshots (Screenshot 1 shows AI disclosure) increases install rate by building trust with users concerned about AI accuracy.

**Theory**: Users are increasingly skeptical of AI-generated content. Proactively showing AI disclosure may attract users who value transparency and deter users who distrust AI (which is acceptable, as they would churn anyway).

### Variants

**Variant A (Control): Feature-Led Screenshots**
- Screenshot 1: City Recommendations ("Smart Destination Picks")
- Screenshot 2: Itinerary View ("Day-by-Day Clarity")
- Screenshot 3: Preferences ("Trips, Your Way")
- Screenshot 4: AI Disclosure ("AI You Can Trust")
- Screenshot 5: Feedback ("Easy Feedback on AI Content")

**Variant B (Test): AI Transparency-Led Screenshots**
- Screenshot 1: AI Disclosure ("AI You Can Trust") ← Moved to front
- Screenshot 2: City Recommendations ("Smart Destination Picks")
- Screenshot 3: Itinerary View ("Day-by-Day Clarity")
- Screenshot 4: Preferences ("Trips, Your Way")
- Screenshot 5: Feedback ("Easy Feedback on AI Content")

### Primary Metric
**App Store Page Conversion Rate**
- Definition: Installs ÷ App Store Page Views (Apple/Google provides this metric)
- Baseline: 30% (industry average for travel apps)
- Success Threshold: +5% lift (30% → 31.5%)

### Secondary Metrics
- First itinerary generation rate (do AI-transparency users engage more?)
- Day 7 retention (do transparency-attracted users retain better?)
- Trial start rate (do they convert at higher rates?)

### Guardrail Metrics
- Total installs must not decrease (lower conversion may be offset by higher volume)
- Day 7 retention ≥ baseline

### Implementation
**Apple App Store**:
1. Create two App Store Connect listings (A/B test via Custom Product Pages)
2. Variant A: Default listing (feature-led screenshots)
3. Variant B: Custom Product Page (AI transparency-led screenshots)
4. Split traffic 50/50 via paid ads (Apple Search Ads)

**Google Play Store**:
1. Use Google Play Store Listing Experiments feature
2. Create Variant B with AI transparency-led screenshots
3. Google automatically splits traffic 50/50

### Analysis Plan
**Week 5-6**: Run experiment (10,000+ page views per variant)
**Week 7**: Analyze results
- If Variant B wins: Ship AI transparency-led screenshots to 100%
- If Variant A wins: Keep feature-led screenshots

### Rollout Decision Tree
```
If Variant B wins (AI transparency increases conversions):
  → Ship to 100% of users
  → Update all marketing materials to emphasize transparency
  → Consider adding "AI Transparency" badge to app icon (future experiment)

If Variant A wins (feature-led wins):
  → Keep feature-led screenshots
  → Test alternative: "Benefit-focused" screenshots (e.g., "Save 10 Hours of Research")
```

---

## Experiment 4: Pro Feature Highlight

**Priority**: P1 (Revenue Optimization)
**Timeline**: Week 7-8 post-launch
**Owner**: Product + Growth + Copywriting

### Hypothesis
Concrete, time-based benefits ("Plan a 7-day trip in 30 seconds") outperform generic benefits ("Unlimited itineraries") on paywall, increasing trial start rate by making value tangible.

**Theory**: "Unlimited" is abstract and hard to value. Time savings are concrete and immediately understood. Users who see time savings may be more motivated to upgrade.

### Variants

**Variant A (Control): Generic Benefits**
```
Paywall Headline: Unlock Unlimited Travel Planning
Benefits:
✓ Unlimited itineraries
✓ Premium destinations & insights
✓ Faster generation
✓ Early feature access
```

**Variant B (Test): Concrete Time-Based Benefits**
```
Paywall Headline: Plan Your Next Trip in 30 Seconds
Benefits:
✓ Generate a full 7-day itinerary in 30 seconds
✓ Save 10+ hours of research per trip
✓ Get recommendations updated in real-time
✓ Try new AI models before anyone else
```

### Primary Metric
**Subscription Conversion Rate**
- Definition: Subscriptions ÷ Paywall Views (users who see paywall and subscribe)
- Baseline: 15% (industry benchmark for freemium trial conversions)
- Success Threshold: +10% lift (15% → 16.5%)

### Secondary Metrics
- Trial start rate (% who tap "Start Free Trial")
- Annual vs. Monthly selection rate (does Variant B favor annual?)
- Revenue per paywall view (total revenue ÷ paywall views)

### Guardrail Metrics
- Day 30 retention ≥ baseline (concrete benefits should not overpromise)
- Cancellation rate ≤ baseline (users should not feel misled)

### Implementation
```typescript
// Feature flag: concrete_benefits_paywall
const paywallCopy = featureFlags.concreteBenefitsPaywall
  ? {
      headline: 'Plan Your Next Trip in 30 Seconds',
      benefits: [
        'Generate a full 7-day itinerary in 30 seconds',
        'Save 10+ hours of research per trip',
        'Get recommendations updated in real-time',
        'Try new AI models before anyone else'
      ]
    }
  : {
      headline: 'Unlock Unlimited Travel Planning',
      benefits: [
        'Unlimited itineraries',
        'Premium destinations & insights',
        'Faster generation',
        'Early feature access'
      ]
    };

return <PaywallScreen copy={paywallCopy} />;
```

### Analysis Plan
**Week 7-8**: Run experiment (50/50 split, 500+ paywall views per variant)
**Week 9**: Analyze results
- If Variant B wins: Ship concrete benefits to 100%
- If Variant A wins: Keep generic benefits

### Rollout Decision Tree
```
If Variant B wins (concrete benefits increase conversions):
  → Ship to 100% of users
  → Update all paywall copy to emphasize time savings
  → Test additional variants: "Plan trips 10x faster" vs. "Save 10 hours per trip"

If Variant A wins (generic benefits win):
  → Keep generic benefits
  → Test alternative: "Social proof" benefits ("Join 10,000+ travelers planning smarter trips")
```

---

## Experiment 5: Feedback Loop Trust Signal

**Priority**: P2 (Retention & Trust)
**Timeline**: Week 9-10 post-launch
**Owner**: Product + Engineering

### Hypothesis
Making the feedback/report mechanism more visible (icon in itinerary header vs. hidden in menu) increases user trust and Day 7 retention by signaling transparency and control.

**Theory**: Users who see prominent feedback controls feel more in control of AI-generated content and are more likely to trust the app. This may increase retention and reduce churn.

### Variants

**Variant A (Control): Feedback Icon Hidden in Menu**
- Itinerary screen: AI banner at top, "Give Feedback" button at bottom (requires scroll)
- Feedback icon: Hidden in overflow menu (⋮)
- Visibility: Low (only ~20% of users scroll to bottom)

**Variant B (Test): Feedback Icon Visible in Header**
- Itinerary screen: AI banner at top, "Give Feedback" icon in header (⚠️ Report)
- Feedback icon: Always visible, top-right corner
- Visibility: High (100% of users see it)

### Primary Metric
**Day 7 Retention**
- Definition: % of users who open app 7 days after signup
- Baseline: 30% (industry benchmark for travel apps)
- Success Threshold: +5% lift (30% → 31.5%)

### Secondary Metrics
- Feedback submission rate (% of users who submit feedback)
- Trust score (post-itinerary survey: "How much do you trust these recommendations?" 1-5)
- Trial start rate (does increased trust lead to higher conversions?)

### Guardrail Metrics
- Negative feedback rate ≤ baseline (visible icon may increase reports, but should not increase negative sentiment)
- Itinerary generation rate ≥ baseline

### Implementation
```typescript
// Feature flag: visible_feedback_icon
if (featureFlags.visibleFeedbackIcon) {
  // Variant B: Feedback icon in header
  return (
    <View style={styles.header}>
      <Text style={styles.title}>{cityName}</Text>
      <TouchableOpacity onPress={() => navigation.navigate('Feedback')}>
        <Icon name="alert-circle" size={24} color="#FF9800" />
      </TouchableOpacity>
    </View>
  );
} else {
  // Variant A: Feedback button at bottom (requires scroll)
  return (
    <ScrollView>
      {/* Itinerary content */}
      <Button onPress={() => navigation.navigate('Feedback')}>
        Give Feedback
      </Button>
    </ScrollView>
  );
}
```

### Analysis Plan
**Week 9-10**: Run experiment (50/50 split, 1,000+ users per variant)
**Week 11**: Analyze results
- If Variant B wins (higher retention): Ship to 100%
- If Variant B neutral or loses: Keep Variant A

### Rollout Decision Tree
```
If Variant B wins (visible feedback increases retention):
  → Ship to 100% of users
  → Add feedback icon to City Recommendation screen (expand visibility)
  → Monitor feedback submission rate (expect +50-100% increase)

If Variant B loses or neutral:
  → Keep Variant A (hidden feedback)
  → Consider alternative: Post-itinerary survey prompt ("How was this itinerary?")
```

---

## 90-Day Roadmap

| Week | Experiment | Status | Owner | Expected Impact |
|------|------------|--------|-------|-----------------|
| 1-2  | First-Trip Completion Rate | ✅ Ready | Product + Engineering | +15% first itinerary rate |
| 3-4  | Paywall Timing | ✅ Ready | Product + Growth | +20% trial start rate |
| 5-6  | Screenshot-Driven Conversion | ✅ Ready | Product + Design | +5% install rate |
| 7-8  | Pro Feature Highlight | ✅ Ready | Product + Copywriting | +10% subscription conversion |
| 9-10 | Feedback Loop Trust Signal | ✅ Ready | Product + Engineering | +5% Day 7 retention |

---

## Experiment Execution Checklist

**Before Launching Experiment**:

- [ ] Hypothesis documented with clear expected outcome
- [ ] Primary metric defined with success threshold
- [ ] Secondary and guardrail metrics defined
- [ ] Minimum sample size calculated (1,000+ users per variant)
- [ ] Feature flag implemented and tested
- [ ] Analytics tracking events configured (Firebase, Amplitude, Mixpanel)
- [ ] Experiment duration set (7-14 days)
- [ ] Legal/compliance review (ensure App Store compliance)
- [ ] Stakeholder alignment (Product, Engineering, Growth, Legal)

**During Experiment**:

- [ ] Monitor guardrail metrics daily (crash-free rate, retention)
- [ ] Check for sample size imbalance (50/50 split maintained)
- [ ] Monitor for external factors (App Store featured, marketing campaigns)

**After Experiment**:

- [ ] Analyze results with 95% confidence (p < 0.05)
- [ ] Document learnings (what worked, what didn't, why)
- [ ] Make rollout decision (ship winner, keep control, iterate)
- [ ] Communicate results to stakeholders
- [ ] Archive experiment data for future reference

---

## App Store Compliance Notes

**All experiments are designed to be App Store-safe**:

1. ✅ AI disclosure remains mandatory (Experiment 1 does not remove AI disclosure)
2. ✅ Free tier always accessible (Experiment 2 only changes paywall timing, not access)
3. ✅ Screenshots comply with Apple guidelines (Experiment 3 reorders, does not remove)
4. ✅ Paywall copy is truthful (Experiment 4 emphasizes time savings, which is factual)
5. ✅ Feedback mechanism always present (Experiment 5 only changes visibility)

---

**Last Updated**: 2024-07-16
**Next Review**: After first experiment completes (Week 2)
**Owner**: Product + Growth teams
