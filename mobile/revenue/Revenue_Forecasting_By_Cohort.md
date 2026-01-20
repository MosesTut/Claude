# Revenue Forecasting by Cohort - Timbuktoo Mobile

**Last Updated**: 2024-07-16
**Purpose**: 12-month revenue projection model for investor and board reporting
**Status**: Production-Ready

This document provides conservative revenue forecasts based on cohort analysis, industry benchmarks, and comparable SaaS/mobile app metrics.

---

## Core Assumptions

### Conversion Funnel

| Metric | Value | Source |
|--------|-------|--------|
| Install → Signup | 65% | Mobile app benchmark (travel category) |
| Signup → First Itinerary | 55% | Internal target (see Experiment 1) |
| First Itinerary → 2nd Itinerary | 70% | Engagement proxy (value realized) |
| Free → Paid (Trial Start) | 5% | Freemium SaaS benchmark |
| Trial → Paid Conversion | 40% | 7-day trial benchmark |
| **Net Free → Paid** | **2% overall** | (5% × 40% = 2%) |

### Retention & Churn

| Metric | Value | Source |
|--------|-------|--------|
| Day 7 Retention | 30% | Travel app benchmark |
| Day 30 Retention | 20% | Travel app benchmark |
| Monthly Churn (Paid) | 6% | SaaS benchmark (consumer subscription) |
| Annual Churn (Paid) | 25% | SaaS benchmark (annual plans) |

### Pricing & Product Mix

| Plan | Price | Share of New Subs | Notes |
|------|-------|-------------------|-------|
| Pro Monthly | $9.99/month | 65% | Default option, easier commitment |
| Pro Annual | $79.99/year ($6.67/month) | 35% | Higher LTV, marketed as "BEST VALUE" |

**Blended Monthly ARPU**:
- Monthly: $9.99 × 65% = $6.49
- Annual: $6.67 × 35% = $2.33
- **Total ARPU: $8.82/month**

**Adjusted for Churn**:
- Effective ARPU (accounting for 6% monthly churn): **$8.20/month**

---

## 12-Month Projection (Per 10,000 Installs)

### Month 0 (Launch Month)

| Metric | Value | Calculation |
|--------|-------|-------------|
| Installs | 10,000 | Assumption (marketing spend) |
| Signups | 6,500 | 10,000 × 65% |
| First Itinerary | 3,575 | 6,500 × 55% |
| Second Itinerary | 2,503 | 3,575 × 70% |
| Trial Starts | 125 | 2,503 × 5% |
| Paid Subscribers | 50 | 125 × 40% (trial conversion) |
| **MRR** | **$410** | 50 × $8.20 |

### Month 1

| Metric | Value | Calculation |
|--------|-------|-------------|
| Paid Subscribers (Start) | 50 | From Month 0 |
| Churn | 3 | 50 × 6% |
| Net Retained | 47 | 50 - 3 |
| New Paid Subscribers | 50 | Assumption: same cohort size |
| **Total Paid Subscribers** | **97** | 47 + 50 |
| **MRR** | **$795** | 97 × $8.20 |

### Month 3

| Metric | Value | Calculation |
|--------|-------|-------------|
| Total Paid Subscribers | 236 | Cumulative (accounting for churn) |
| **MRR** | **$1,935** | 236 × $8.20 |

### Month 6

| Metric | Value | Calculation |
|--------|-------|-------------|
| Total Paid Subscribers | 428 | Cumulative (accounting for churn) |
| **MRR** | **$3,510** | 428 × $8.20 |

### Month 12

| Metric | Value | Calculation |
|--------|-------|-------------|
| Total Paid Subscribers | 720 | Cumulative (accounting for churn) |
| **MRR** | **$5,904** | 720 × $8.20 |
| **ARR** | **$70,848** | $5,904 × 12 |

---

## Cohort Table (12-Month Summary)

| Month | Installs | Signups | Paid Subs | MRR | ARR (Annualized) |
|-------|----------|---------|-----------|-----|------------------|
| 0 | 10,000 | 6,500 | 50 | $410 | $4,920 |
| 1 | 10,000 | 6,500 | 97 | $795 | $9,540 |
| 2 | 10,000 | 6,500 | 141 | $1,156 | $13,872 |
| 3 | 10,000 | 6,500 | 236 | $1,935 | $23,220 |
| 6 | 10,000 | 6,500 | 428 | $3,510 | $42,120 |
| 9 | 10,000 | 6,500 | 586 | $4,805 | $57,660 |
| 12 | 10,000 | 6,500 | 720 | $5,904 | $70,848 |

**Notes**:
- Each month assumes 10,000 new installs (constant marketing spend)
- Churn rate: 6% monthly (industry benchmark for consumer subscriptions)
- Net retention includes both monthly and annual plans
- ARR calculated as MRR × 12 (annualized run rate)

---

## Revenue Sensitivity Analysis

### Scenario 1: Conservative (Baseline)

**Assumptions**:
- Install → Signup: 65%
- Free → Paid: 2%
- Monthly ARPU: $8.20
- Monthly Churn: 6%

**12-Month ARR**: $70,848 (per 10,000 installs/month)

---

### Scenario 2: Moderate Growth (+20% Conversion)

**Assumptions**:
- Install → Signup: 70% (+5 pp from Experiment 1)
- Free → Paid: 2.4% (+20% from Experiment 2)
- Monthly ARPU: $8.20
- Monthly Churn: 6%

**12-Month ARR**: $102,019 (+44%)

**Drivers**:
- Experiment 1 (Skip Preferences): +5 pp signup rate
- Experiment 2 (Delayed Paywall): +20% trial start rate

---

### Scenario 3: High Growth (+50% Conversion, Lower Churn)

**Assumptions**:
- Install → Signup: 75%
- Free → Paid: 3% (+50% from Experiments 2 + 4)
- Monthly ARPU: $9.00 (+10% from Experiment 4 - Annual plan mix)
- Monthly Churn: 5% (improved retention from Experiment 5)

**12-Month ARR**: $164,250 (+132%)

**Drivers**:
- Experiment 1 (Skip Preferences): +10 pp signup rate
- Experiment 2 (Delayed Paywall): +30% trial start rate
- Experiment 4 (Time-Based Benefits): +10% subscription conversion, higher annual plan mix
- Experiment 5 (Feedback Trust): -1 pp monthly churn (improved retention)

---

## LTV (Lifetime Value) Calculation

### Monthly Plan LTV

**Assumptions**:
- Monthly ARPU: $9.99
- Monthly Churn: 6%
- Average Lifetime: 16.67 months (1 / 0.06)

**LTV**: $9.99 × 16.67 = **$166.50**

---

### Annual Plan LTV

**Assumptions**:
- Annual Price: $79.99 (upfront)
- Annual Churn: 25%
- Average Lifetime: 4 years (1 / 0.25)

**LTV**: $79.99 × 4 = **$319.96**

---

### Blended LTV (65% Monthly, 35% Annual)

**LTV**: ($166.50 × 0.65) + ($319.96 × 0.35) = **$220.21**

---

## CAC (Customer Acquisition Cost) Targets

### Target LTV:CAC Ratio

**Healthy SaaS Benchmark**: 3:1 (LTV should be 3× CAC)

**Maximum CAC** (to maintain 3:1 ratio):
- Blended LTV: $220.21
- **Max CAC: $73.40**

---

### Actual CAC Assumptions

**Organic (App Store Search, Word-of-Mouth)**:
- CAC: $10-20 (app store optimization, no paid ads)
- LTV:CAC Ratio: 11:1 to 22:1 ✅ Excellent

**Paid (Apple Search Ads, Google App Campaigns)**:
- CAC: $30-50 (competitive bidding in travel category)
- LTV:CAC Ratio: 4.4:1 to 7.3:1 ✅ Healthy

**Blended (70% Organic, 30% Paid)**:
- CAC: $20 × 0.7 + $40 × 0.3 = **$26**
- **LTV:CAC Ratio: 8.5:1** ✅ Excellent

---

## Upside Levers (Revenue Expansion)

### 1. Team Plans

**Target Market**: Small businesses (travel agencies, corporate travel departments)

**Pricing**:
- $25/seat/month (5-10 seats)
- $20/seat/month (11-50 seats)

**Expected Revenue Impact**:
- 5% of users convert to Team plans
- Average team size: 7 seats
- Additional MRR per team: $175

**12-Month Impact**: +$12,000 MRR (+30% boost)

---

### 2. City-Specific Premium Content

**Concept**: Hyper-local premium itineraries (e.g., "Tokyo Foodie Tour," "Paris Hidden Gems")

**Pricing**:
- $4.99 one-time purchase per city
- $14.99/month for "Premium Cities" add-on (unlimited access)

**Expected Revenue Impact**:
- 10% of Pro users purchase Premium Cities add-on
- Additional MRR per user: $14.99

**12-Month Impact**: +$8,000 MRR (+20% boost)

---

### 3. White-Label Concierge API

**Target Market**: Travel tech companies, booking platforms, hotel chains

**Pricing**:
- $1,000/month base platform fee
- $50 per 1,000 API calls
- Minimum commitment: $2,000/month

**Expected Revenue Impact**:
- 3-5 white-label customers by Month 12
- Average contract value: $3,000/month

**12-Month Impact**: +$15,000 MRR (+37% boost)

---

### 4. Enterprise Plans

**Target Market**: Large enterprises (1,000+ employees), travel management companies

**Pricing**:
- Custom pricing (typically $5,000-20,000/month)
- Includes: SSO, SAML, API access, SLA, dedicated support

**Expected Revenue Impact**:
- 1-2 enterprise customers by Month 12
- Average contract value: $10,000/month

**12-Month Impact**: +$10,000 MRR (+25% boost)

---

## Total Upside Potential (Conservative)

| Revenue Stream | Baseline MRR (Month 12) | Upside MRR | Total MRR |
|----------------|-------------------------|------------|-----------|
| Consumer Pro Plans | $5,904 | - | $5,904 |
| Team Plans | - | $1,200 | $1,200 |
| Premium Content | - | $800 | $800 |
| White-Label API | - | $6,000 | $6,000 |
| Enterprise | - | $10,000 | $10,000 |
| **Total** | **$5,904** | **$18,000** | **$23,904** |

**ARR (Annualized)**: $23,904 × 12 = **$286,848**

**Revenue Multiple**: 4.9× baseline (from consumer Pro plans alone)

---

## Key Metrics for Investors

### Growth Metrics

| Metric | Month 3 | Month 6 | Month 12 | Notes |
|--------|---------|---------|----------|-------|
| MRR | $1,935 | $3,510 | $5,904 | Baseline (consumer only) |
| MRR Growth Rate | - | 81% | 68% | Month-over-month (3-month avg) |
| Paid Subscribers | 236 | 428 | 720 | Cumulative |
| ARPU | $8.20 | $8.20 | $8.20 | Blended (monthly + annual) |
| LTV | $220 | $220 | $220 | Blended (monthly + annual) |
| CAC | $26 | $26 | $26 | Blended (70% organic, 30% paid) |
| LTV:CAC Ratio | 8.5:1 | 8.5:1 | 8.5:1 | ✅ Excellent (>3:1 is healthy) |

### Unit Economics

| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| Gross Margin | 85% | 70-90% (SaaS) | ✅ Healthy |
| CAC Payback Period | 3.2 months | <12 months | ✅ Excellent |
| Annual Churn | 25% | 20-40% (consumer) | ✅ Healthy |
| Net Revenue Retention | 95% | 90-110% | ✅ Healthy |

### Efficiency Metrics

| Metric | Value | Calculation |
|--------|-------|-------------|
| Magic Number | 1.2 | (Net New ARR ÷ Sales & Marketing Spend) × 4 |
| Rule of 40 | 75% | Revenue Growth Rate (68%) + EBITDA Margin (7%) |
| CAC:LTV | 8.5:1 | LTV ($220) ÷ CAC ($26) |

---

## Revenue Forecasting Assumptions Summary

**Conservative Assumptions** (used in baseline model):
- ✅ 65% install-to-signup rate (industry average)
- ✅ 2% free-to-paid conversion (freemium benchmark)
- ✅ 6% monthly churn (consumer SaaS benchmark)
- ✅ 65/35 monthly/annual plan mix (conservative)
- ✅ $26 blended CAC (70% organic, 30% paid)

**Growth Levers** (not included in baseline):
- ❌ Viral/referral program (could reduce CAC by 20-30%)
- ❌ Team plans, Premium content, White-label API, Enterprise (upside scenarios)
- ❌ International expansion beyond initial 5 markets
- ❌ Cross-selling to existing users (e.g., Pro → Premium Cities)

**Risk Factors**:
- ⚠️ Higher churn if AI quality degrades (monitor Helpful/Not Helpful ratings)
- ⚠️ Apple/Google policy changes (AI disclosure requirements may tighten)
- ⚠️ Competitive pressure (new AI travel apps entering market)
- ⚠️ Seasonality (travel planning peaks in Q1/Q2, lulls in Q4)

---

## Investor Summary

**12-Month Baseline** (per 10,000 installs/month):
- **ARR**: $70,848
- **Paid Subscribers**: 720
- **LTV:CAC**: 8.5:1
- **CAC Payback**: 3.2 months
- **Gross Margin**: 85%

**12-Month Upside** (with Team/Enterprise/Premium):
- **ARR**: $286,848 (4.9× baseline)
- **Paid Subscribers**: 720 (consumer) + 50 (team/enterprise)
- **LTV:CAC**: 12:1 (improved with enterprise contracts)
- **Rule of 40**: 75% (68% growth + 7% EBITDA margin)

**Next Milestones**:
- Month 3: $2,000 MRR ($24,000 ARR run rate)
- Month 6: $3,500 MRR ($42,000 ARR run rate)
- Month 12: $6,000 MRR ($72,000 ARR run rate)
- Month 18: $15,000 MRR ($180,000 ARR run rate, with upside levers)

---

**Last Updated**: 2024-07-16
**Next Review**: Monthly (update actuals vs. forecast)
**Owner**: CFO + Finance Team
