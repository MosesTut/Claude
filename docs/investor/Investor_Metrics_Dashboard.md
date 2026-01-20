# Investor Metrics Dashboard - Timbuktoo Mobile

**Last Updated**: 2024-07-16
**Purpose**: Core KPIs for investor and board reporting
**Refresh Frequency**: Weekly (Monday morning updates)

---

## Dashboard Layout

```
┌─────────────────────────────────────────────────────────┐
│         TIMBUKTOO MOBILE - INVESTOR DASHBOARD           │
│                    Week of [Date]                       │
└─────────────────────────────────────────────────────────┘

┌──────────────┬──────────────┬──────────────────────────┐
│    GROWTH    │   REVENUE    │  TRUST & COMPLIANCE      │
├──────────────┼──────────────┼──────────────────────────┤
│ Installs     │ MRR          │ Uptime %                 │
│ Activation   │ ARPU         │ Crash-free Rate          │
│ DAU / MAU    │ LTV          │ Incident Count           │
│ Retention D7 │ CAC          │ SOC-2 Progress %         │
│ Retention D30│ Conversion   │                          │
└──────────────┴──────────────┴──────────────────────────┘
```

---

## Core KPIs

### Growth Metrics

**1. Installs**
- **Definition**: Total app downloads (iOS App Store + Google Play)
- **Goal**: 10,000 installs/month (Month 1), 50,000 installs/month (Month 12)
- **Source**: App Store Connect Analytics, Google Play Console
- **Trend**: Week-over-week growth rate

**2. Activation Rate**
- **Definition**: % of users who generate at least one itinerary within first 7 days
- **Formula**: (Users with 1+ itinerary ÷ Total signups) × 100
- **Goal**: 45% (baseline), 55% (after Experiment 1 - Skip Preferences)
- **Source**: Firebase Analytics, Amplitude

**3. DAU / MAU (Daily Active Users / Monthly Active Users)**
- **Definition**: Unique users who open the app daily vs. monthly
- **Benchmark**: 20-30% for travel apps (seasonal)
- **Goal**: 25% (Month 3), 30% (Month 12)
- **Source**: Firebase Analytics

**4. Retention - Day 7**
- **Definition**: % of users who return to app 7 days after signup
- **Goal**: 30% (baseline), 35% (after Experiment 5 - Feedback Trust Signal)
- **Source**: Firebase Analytics, Amplitude

**5. Retention - Day 30**
- **Definition**: % of users who return to app 30 days after signup
- **Goal**: 20% (baseline), 25% (optimistic)
- **Source**: Firebase Analytics, Amplitude

---

### Revenue Metrics

**1. MRR (Monthly Recurring Revenue)**
- **Definition**: Predictable monthly revenue from subscriptions
- **Goal**: $2,000 (Month 3), $6,000 (Month 12), $15,000 (Month 18 with upside levers)
- **Source**: Stripe Dashboard, RevenueCat
- **Formula**: Sum of all active subscriptions (prorated for annual plans)

**2. ARPU (Average Revenue Per User)**
- **Definition**: Average revenue per paying user per month
- **Formula**: MRR ÷ Total Paid Subscribers
- **Goal**: $8.20 (blended monthly + annual)
- **Source**: Stripe Dashboard, RevenueCat

**3. LTV (Lifetime Value)**
- **Definition**: Total revenue expected from an average customer over their lifetime
- **Formula**: ARPU ÷ Monthly Churn Rate
- **Goal**: $220 (blended), $167 (monthly), $320 (annual)
- **Source**: Calculated from ARPU and churn rate

**4. CAC (Customer Acquisition Cost)**
- **Definition**: Cost to acquire one paying customer
- **Formula**: Total Sales & Marketing Spend ÷ New Paid Customers
- **Goal**: $26 (blended: 70% organic, 30% paid)
- **Source**: Ad platforms (Apple Search Ads, Google App Campaigns), calculated

**5. Conversion Rate (Free → Paid)**
- **Definition**: % of free users who convert to paid
- **Formula**: (New Paid Subscribers ÷ Free Users) × 100
- **Goal**: 2% (baseline), 2.4% (after Experiment 2 - Paywall Timing)
- **Source**: RevenueCat, Firebase Analytics

**6. Annual Plan Mix**
- **Definition**: % of new subscribers choosing annual plan
- **Goal**: 35% (baseline), 40% (after Experiment 4 - Pro Feature Highlight)
- **Source**: RevenueCat, Stripe

---

### Unit Economics

**1. LTV:CAC Ratio**
- **Definition**: Ratio of customer lifetime value to acquisition cost
- **Formula**: LTV ÷ CAC
- **Goal**: 8.5:1 (baseline), > 3:1 is healthy SaaS benchmark
- **Status**: ✅ Excellent

**2. CAC Payback Period**
- **Definition**: Time to recover customer acquisition cost
- **Formula**: CAC ÷ (ARPU × Gross Margin)
- **Goal**: 3.2 months (baseline), < 12 months is healthy
- **Status**: ✅ Excellent

**3. Gross Margin**
- **Definition**: (Revenue - COGS) ÷ Revenue
- **COGS**: Infrastructure (AWS, Anthropic AI API), payment processing (Stripe 2.9% + $0.30)
- **Goal**: 85% (typical SaaS gross margin is 70-90%)
- **Status**: ✅ Healthy

**4. Churn Rate**
- **Definition**: % of paying customers who cancel per month
- **Goal**: 6% monthly (consumer SaaS benchmark), 25% annual
- **Source**: RevenueCat, Stripe

**5. Net Revenue Retention (NRR)**
- **Definition**: Revenue retention after accounting for churn, contraction, and expansion
- **Formula**: ((Starting MRR + Expansion - Churn - Contraction) ÷ Starting MRR) × 100
- **Goal**: 95% (consumer apps), 110%+ (B2B SaaS with upsells)
- **Source**: Calculated from MRR movements

---

### Trust & Reliability Metrics

**1. Uptime %**
- **Definition**: % of time the service is available and operational
- **Goal**: 99.9% (< 43 minutes downtime per month)
- **Source**: Pingdom, Datadog
- **Status**: Real-time monitoring, published on status.timbuktoo.app

**2. Crash-Free Rate**
- **Definition**: % of user sessions without crashes
- **Goal**: 99.5%+ (Google Play "Good" rating requires 99.5%+)
- **Source**: Firebase Crashlytics
- **Status**: Monitored daily

**3. Incident Count**
- **Definition**: Number of production incidents per week (P0/P1)
- **Goal**: 0 P0 (critical outages), < 2 P1 (degraded performance)
- **Source**: PagerDuty, Jira

**4. SOC-2 Progress %**
- **Definition**: % completion of SOC-2 Type II audit (180-day control period)
- **Goal**: 100% by Month 6 (February 2025)
- **Source**: Auditor + Security Team tracking
- **Status**: In Progress (0% → 100% over 6 months)

**5. AI Quality Metrics**
- **Helpful Rate**: % of itineraries rated "Helpful" by users
- **Goal**: 75%+ (baseline)
- **Source**: Firebase Analytics (feedback submissions)

---

## Dashboard Visualizations

### Growth Chart (Line Graph)
```
Installs per Week
    │
60K │                                   ╱
    │                               ╱
40K │                           ╱
    │                       ╱
20K │                   ╱
    │               ╱
 0K │───────────────────────────────────
    Week 1      Week 20     Week 40     Week 52
```

### Revenue Chart (Bar Graph)
```
MRR ($)
    │
20K │                                   █
    │                               █   █
15K │                           █   █   █
    │                       █   █   █   █
10K │                   █   █   █   █   █
    │               █   █   █   █   █   █
 5K │           █   █   █   █   █   █   █
    │       █   █   █   █   █   █   █   █
 0K │───────────────────────────────────────
    M1  M2  M3  M4  M5  M6  M7  M8  M9  M10 M11 M12
```

### Cohort Retention Table
```
Cohort Retention (% of users returning on Day N)

Cohort     D0    D7    D14   D30   D60   D90
────────────────────────────────────────────
Week 1    100%   32%   25%   20%   15%   12%
Week 2    100%   34%   26%   21%   16%   13%
Week 3    100%   36%   28%   23%   18%   15%
Week 4    100%   38%   30%   25%   20%   17%
```

### LTV:CAC Funnel
```
Funnel (per 10,000 installs)

10,000 Installs
    ↓ 65% signup rate
 6,500 Signups
    ↓ 55% first itinerary rate
 3,575 Activated Users
    ↓ 2% free-to-paid conversion
    71 Paid Subscribers

LTV:   $220
CAC:   $26
Ratio: 8.5:1 ✅
```

---

## Weekly Report Template

**Subject**: Timbuktoo Investor Update - Week of [Date]

**Summary**:
- MRR: $X,XXX (+Y% WoW)
- Paid Subscribers: X (+Y new this week)
- Installs: X,XXX (+Y% WoW)
- Day 7 Retention: XX% (↑ Y pp from last week)
- Uptime: 99.X% (X incidents)

**Highlights**:
- 🚀 Launched Experiment 2 (Paywall Timing) - early results show +15% trial start rate
- ✅ Completed Month 2 of SOC-2 Type II control period (33% complete)
- 📈 App Store featured in "Travel Apps You'll Love" (US, UK, Canada)

**Challenges**:
- ⚠️ Android crash-free rate dropped to 98.5% (below 99.5% target) - investigating
- ⚠️ CAC increased to $32 (from $26) due to competitive bidding on Apple Search Ads

**Next Week Priorities**:
- Ship winning variant from Experiment 2 to 100% of users
- Fix Android crash (identified root cause: OkHttp timeout issue)
- Launch Experiment 3 (Screenshot-Driven Conversion)

---

## Board Deck (Quarterly)

**Slide 1: Executive Summary**
- MRR: $X,XXX (+Y% QoQ)
- ARR: $X,XXX (annualized run rate)
- Paid Subscribers: X (+Y% QoQ)
- LTV:CAC: 8.5:1
- Burn Rate: $X,XXX/month

**Slide 2: Growth Metrics**
- Installs (line chart)
- Activation rate (target vs. actual)
- DAU/MAU (benchmark comparison)
- Retention cohorts (heatmap)

**Slide 3: Revenue Metrics**
- MRR growth (bar chart)
- ARPU trend (line chart)
- Annual plan mix (pie chart)
- Churn rate (target vs. actual)

**Slide 4: Unit Economics**
- LTV:CAC ratio (8.5:1)
- CAC payback period (3.2 months)
- Gross margin (85%)
- Rule of 40 (75% = 68% revenue growth + 7% EBITDA margin)

**Slide 5: Product & Experiments**
- Experiment 1 results: +15% first itinerary rate ✅
- Experiment 2 results: +20% trial start rate ✅
- Experiment 3 in progress (screenshot conversion)
- Roadmap: Team plans, Premium Cities, Enterprise

**Slide 6: Compliance & Trust**
- SOC-2 Type II: 50% complete (Month 3 of 6)
- Uptime: 99.95% (exceeded 99.9% target)
- Crash-free rate: 99.7% (iOS), 99.4% (Android)
- Zero security incidents

**Slide 7: Financials**
- Revenue: $X,XXX (MRR × 12 = ARR)
- Expenses: $X,XXX (burn rate)
- Runway: X months (cash balance ÷ burn rate)
- Next fundraise: Series A in Q2 2025

---

## Data Sources

| Metric | Source | Refresh Frequency |
|--------|--------|-------------------|
| Installs, Store Conversion | App Store Connect, Google Play Console | Daily |
| DAU, MAU, Retention | Firebase Analytics, Amplitude | Real-time |
| MRR, ARPU, Churn | Stripe, RevenueCat | Daily |
| Uptime, Incidents | Pingdom, Datadog, PagerDuty | Real-time |
| Crash-Free Rate | Firebase Crashlytics | Real-time |
| SOC-2 Progress | Manual tracking (Security Team) | Weekly |

---

## Alerts & Notifications

**Slack Channel**: #investor-metrics (auto-posted every Monday 9 AM)

**Email**: Weekly digest sent to investors (every Monday 10 AM)

**Critical Alerts** (immediate notification to CEO + Board):
- MRR drops > 10% WoW
- Uptime drops < 99%
- Crash-free rate < 99%
- P0 incident (production outage)
- Security breach

---

**Last Updated**: 2024-07-16
**Owner**: CFO + Finance Team
**Distribution**: Investors, Board Members, Executive Team
