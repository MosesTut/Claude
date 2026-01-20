# App Store A/B Test Assets - Timbuktoo Mobile

**Last Updated**: 2024-07-16
**Purpose**: Production-ready A/B test configurations for App Store optimization and in-app conversion
**Status**: Execution-Ready

This document provides complete test specifications for App Store listing optimization (screenshots, headlines) and in-app conversion experiments (paywall, icons).

---

## Test Framework

### Statistical Rigor
- **Confidence Level**: 95% (p < 0.05)
- **Minimum Sample Size**: 1,000 users per variant (App Store), 500 per variant (in-app)
- **Runtime**: 7-14 days (until statistical significance reached)
- **Stop Rules**:
  - Stop early if one variant wins with >99% confidence
  - Stop if no significant difference after 14 days
  - Stop if conversion rate drops >10% (safety guardrail)

### Testing Platform
- **App Store (iOS)**: App Store Connect → Custom Product Pages
- **Google Play (Android)**: Google Play Console → Store Listing Experiments
- **In-App Tests**: Feature flags (Firebase Remote Config, LaunchDarkly, or custom)

---

## Test 1: Screenshot Narrative

**Objective**: Increase App Store page conversion rate (installs ÷ page views)

**Hypothesis**: Trust-led screenshots (emphasizing AI transparency) outperform feature-led screenshots by attracting users who value transparency and deterring users who distrust AI (reducing post-install churn).

**Primary KPI**: Product page conversion rate
**Secondary KPIs**:
- First itinerary generation rate (do transparency-attracted users engage more?)
- Day 7 retention (do they retain better?)

**Stop Rule**: 95% statistical confidence, minimum 10,000 page views per variant

---

### Variant A: Feature-Led (Control)

**Screenshot Order**:
1. City Recommendations ("Smart Destination Picks")
2. Itinerary View ("Day-by-Day Clarity")
3. Preferences ("Trips, Your Way")
4. AI Disclosure ("AI You Can Trust")
5. Feedback ("Easy Feedback on AI Content")

**Messaging Strategy**: Lead with value prop (destination recommendations, clear itineraries) before disclosing AI usage

**Screenshot Files**:
```
ios_screenshot_01_city_selection_feature_led_6.7.png
ios_screenshot_02_itinerary_feature_led_6.7.png
ios_screenshot_03_preferences_feature_led_6.7.png
ios_screenshot_04_ai_disclosure_feature_led_6.7.png
ios_screenshot_05_feedback_feature_led_6.7.png
```

---

### Variant B: Trust-Led (Test)

**Screenshot Order**:
1. AI Disclosure ("AI You Can Trust") ← **Moved to front**
2. City Recommendations ("Smart Destination Picks")
3. Itinerary View ("Day-by-Day Clarity")
4. Preferences ("Trips, Your Way")
5. Feedback ("Easy Feedback on AI Content")

**Messaging Strategy**: Lead with transparency (AI disclosure, trust-building) before showing features

**Screenshot Files**:
```
ios_screenshot_01_ai_disclosure_trust_led_6.7.png
ios_screenshot_02_city_selection_trust_led_6.7.png
ios_screenshot_03_itinerary_trust_led_6.7.png
ios_screenshot_04_preferences_trust_led_6.7.png
ios_screenshot_05_feedback_trust_led_6.7.png
```

---

### Test 1 Implementation

**iOS (App Store Connect)**:
1. Create Custom Product Page: "Trust-Led Screenshots"
2. Upload Variant B screenshots
3. Set traffic allocation: 50% Default (Variant A), 50% Custom (Variant B)
4. Monitor via App Store Connect Analytics → Custom Product Pages

**Android (Google Play Console)**:
1. Create Store Listing Experiment: "Screenshot Narrative Test"
2. Upload Variant B screenshots
3. Google automatically splits traffic 50/50
4. Monitor via Google Play Console → Store Presence → Store Listing Experiments

**Analysis**:
```
Expected Baseline Conversion Rate: 30% (industry average)
Expected Lift (Variant B): +5% (30% → 31.5%)

Sample Size Calculation:
- Minimum: 2,000 page views per variant
- Expected runtime: 7-10 days (at 500 page views/day)

Decision Tree:
- If Variant B wins (+5% or more): Ship trust-led to 100%
- If Variant A wins: Keep feature-led (current default)
- If neutral (no significant difference): Keep feature-led (simpler)
```

---

## Test 2: Paywall Headline

**Objective**: Increase trial start rate (% of users who tap "Start Free Trial" on paywall)

**Hypothesis**: Action-oriented headlines ("Plan Any Trip in Minutes") outperform generic headlines ("Unlock Unlimited Travel Planning") by emphasizing speed and ease over unlimited access.

**Primary KPI**: Trial start rate
**Secondary KPIs**:
- Subscription conversion rate (trial → paid)
- Revenue per paywall view

**Stop Rule**: 95% statistical confidence, minimum 500 paywall views per variant

---

### Variant A: Generic Benefits (Control)

**Headline**:
```
Unlock Unlimited Travel Planning
```

**Subheadline**:
```
Create unlimited AI-generated itineraries tailored to you.
```

**Benefits**:
```
✓ Unlimited itineraries
✓ Premium destinations & insights
✓ Faster generation
✓ Early feature access
```

**CTA**: "Start Free Trial"

**Messaging Strategy**: Emphasize unlimited access, premium features (feature-led)

---

### Variant B: Action-Oriented (Test)

**Headline**:
```
Plan Any Trip in Minutes
```

**Subheadline**:
```
Get a complete 7-day itinerary in 30 seconds. Save hours of research.
```

**Benefits**:
```
✓ Generate full itineraries in 30 seconds
✓ Save 10+ hours of research per trip
✓ Get AI recommendations tailored to you
✓ Plan unlimited trips
```

**CTA**: "Try Free for 7 Days"

**Messaging Strategy**: Emphasize speed, time savings, and ease (benefit-led)

---

### Test 2 Implementation

**Feature Flag**:
```typescript
// Firebase Remote Config or LaunchDarkly
const paywallVariant = remoteConfig.getString('paywall_headline_test');

const paywallCopy = paywallVariant === 'action_oriented'
  ? {
      headline: 'Plan Any Trip in Minutes',
      subheadline: 'Get a complete 7-day itinerary in 30 seconds. Save hours of research.',
      benefits: [
        'Generate full itineraries in 30 seconds',
        'Save 10+ hours of research per trip',
        'Get AI recommendations tailored to you',
        'Plan unlimited trips'
      ],
      cta: 'Try Free for 7 Days'
    }
  : {
      headline: 'Unlock Unlimited Travel Planning',
      subheadline: 'Create unlimited AI-generated itineraries tailored to you.',
      benefits: [
        'Unlimited itineraries',
        'Premium destinations & insights',
        'Faster generation',
        'Early feature access'
      ],
      cta: 'Start Free Trial'
    };
```

**Traffic Allocation**: 50/50 split (randomized on user_id hash)

**Analysis**:
```
Expected Baseline Trial Start Rate: 10% (freemium benchmark)
Expected Lift (Variant B): +15% (10% → 11.5%)

Sample Size Calculation:
- Minimum: 500 paywall views per variant
- Expected runtime: 5-7 days (at 150 paywall views/day)

Decision Tree:
- If Variant B wins (+15% or more): Ship action-oriented to 100%
- If Variant A wins: Keep generic benefits
- If neutral: Test alternative headline ("Get Your Perfect Trip Plan")
```

---

## Test 3: App Icon (Optional)

**Objective**: Increase App Store page conversion rate and brand recognition

**Hypothesis**: Icons with clear AI/tech signaling (compass + AI glyph) outperform generic travel icons (location pin) by differentiating the app as an AI-powered tool.

**Primary KPI**: Product page conversion rate
**Secondary KPIs**:
- Install rate (from search vs. browse)
- Brand recall (post-install survey)

**Stop Rule**: 95% statistical confidence, minimum 20,000 impressions per variant

**WARNING**: Icon changes are high-risk (existing users may not recognize the app). Only test if confident in design.

---

### Variant A: Compass + AI Glyph (Test 1)

**Design**:
- Icon: Compass rose (center)
- AI Glyph: Small AI chip/sparkle in top-right corner
- Color: Blue gradient (tech-forward)
- Font: Modern sans-serif (for "T" lettermark if using)

**Messaging**: "AI-powered navigation, smart travel planning"

**Icon File**: `app_icon_compass_ai_1024x1024.png`

---

### Variant B: Location Pin + Itinerary Card (Test 2)

**Design**:
- Icon: Location pin (center)
- Itinerary Card: Small card/list icon overlaid on pin
- Color: Warm gradient (orange to yellow, travel-themed)
- Font: Friendly sans-serif

**Messaging**: "Your personalized travel itinerary, pinpointed"

**Icon File**: `app_icon_pin_itinerary_1024x1024.png`

---

### Variant C: Current Icon (Control)

**Design**: (Assume existing icon - replace with actual current design)

**Icon File**: `app_icon_current_1024x1024.png`

---

### Test 3 Implementation

**iOS (App Store Connect)**:
1. Upload Variant A and Variant B icons
2. Create Custom Product Pages for each variant
3. Set traffic allocation: 33% Current (Control), 33% Compass+AI, 33% Pin+Itinerary
4. Monitor via App Store Connect Analytics → Custom Product Pages

**Android (Google Play Console)**:
1. Use Icon Testing feature (if available in your region)
2. Upload Variant A and B
3. Google automatically tests and reports winner

**Analysis**:
```
Expected Baseline Conversion Rate: 30%
Expected Lift (Variant A or B): +3-5% (small but meaningful for branding)

Sample Size Calculation:
- Minimum: 20,000 impressions per variant
- Expected runtime: 14-21 days (at 3,000 impressions/day)

Decision Tree:
- If Variant A or B wins: Ship winning icon to 100% (with announcement to existing users)
- If Current wins: Keep current icon, revisit in 6 months
- If neutral: Keep current icon (avoid change churn)
```

---

## Test Execution Checklist

**Before Launching Test**:

- [ ] Hypothesis documented with clear expected outcome
- [ ] Primary and secondary KPIs defined
- [ ] Minimum sample size calculated
- [ ] Stop rules defined (confidence level, runtime, safety guardrails)
- [ ] Variants created and reviewed by design/legal
- [ ] Feature flags implemented (for in-app tests)
- [ ] Analytics tracking configured (Firebase, Amplitude, Mixpanel)
- [ ] Stakeholder alignment (Product, Design, Growth, Legal)

**During Test**:

- [ ] Monitor sample size daily (ensure 50/50 split maintained)
- [ ] Check for external factors (App Store featuring, marketing campaigns)
- [ ] Review guardrail metrics (crash-free rate, Day 7 retention)
- [ ] Check for statistical significance every 2 days

**After Test**:

- [ ] Analyze results with 95% confidence (p < 0.05)
- [ ] Document learnings (what worked, what didn't, why)
- [ ] Make rollout decision (ship winner, keep control, iterate)
- [ ] Communicate results to stakeholders
- [ ] Archive test data for future reference

---

## Additional Test Ideas (Future)

### Test 4: Free Trial Length

**Variant A**: 3-day free trial (shorter, faster decision)
**Variant B**: 7-day free trial (current, industry standard)
**Variant C**: 14-day free trial (longer, more time to experience value)

**Primary KPI**: Trial → Paid conversion rate
**Hypothesis**: 7-day trial balances value demonstration and urgency

---

### Test 5: Annual vs. Monthly Pricing Display Order

**Variant A**: Annual plan first (higher LTV, "BEST VALUE" badge)
**Variant B**: Monthly plan first (easier commitment, lower barrier)

**Primary KPI**: Annual plan selection rate
**Hypothesis**: Annual-first increases annual plan mix (higher LTV)

---

### Test 6: Social Proof on Paywall

**Variant A**: No social proof (current)
**Variant B**: "Join 10,000+ travelers planning smarter trips with Timbuktoo Pro"

**Primary KPI**: Trial start rate
**Hypothesis**: Social proof increases trust and trial starts by +5-10%

---

### Test 7: Countdown Timer on Paywall (Caution: May Violate Store Policies)

**Variant A**: No urgency (current)
**Variant B**: "Limited time: 7-day free trial expires in 48 hours"

**Primary KPI**: Trial start rate
**WARNING**: Apple/Google may reject apps with misleading urgency tactics. Only test if trial offer is genuinely time-limited.

---

## App Store A/B Testing Best Practices

### Do's
- ✅ Test one variable at a time (screenshot order OR headline, not both)
- ✅ Run tests for at least 7 days to account for weekday/weekend variance
- ✅ Use 50/50 traffic split for maximum statistical power
- ✅ Document learnings even if test is neutral (avoid retesting same hypothesis)
- ✅ Share results with team (transparency builds trust)

### Don'ts
- ❌ Stop tests early (wait for statistical significance)
- ❌ Test too many variants at once (splits traffic too much, reduces power)
- ❌ Change multiple variables in one test (can't isolate causal factor)
- ❌ Ignore guardrail metrics (don't sacrifice retention for conversion)
- ❌ Test during major marketing campaigns (confounding factors)

---

**Last Updated**: 2024-07-16
**Next Review**: After Test 1 and 2 complete (Week 8 post-launch)
**Owner**: Product + Growth teams
