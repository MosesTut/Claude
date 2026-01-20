# Enterprise Pricing & MSA Template - Timbuktoo

**Last Updated**: 2024-07-16
**Purpose**: Pricing calculator and Master Service Agreement (MSA) template for enterprise sales
**Status**: Production-Ready

---

## Pricing Tiers

| Tier | Use Case | Pricing Model | Features |
|------|----------|---------------|----------|
| **Pro** | Individuals | $9.99/month or $79.99/year | Unlimited itineraries, mobile app, email support |
| **Team** | Small businesses (5-50 employees) | Per-seat pricing | Team management, shared itineraries, admin controls |
| **Enterprise** | Large organizations (50+ employees) | Custom pricing | SSO, SAML, API access, SLA, dedicated support |
| **White Label** | OEM partners (travel tech companies) | Platform fee + usage-based | Custom branding, API access, reseller terms |

---

## Enterprise Pricing Calculator

### Inputs
1. **Seats**: Number of users (minimum 50 for Enterprise tier)
2. **Monthly Itinerary Volume**: Estimated number of itineraries generated per month
3. **Cities Enabled**: Number of destination cities (all cities included by default, premium cities cost extra)
4. **SLA Tier**: Standard (99.9%), Enhanced (99.95%), Premium (99.99%)
5. **Add-Ons**: SSO, SAML, API access, dedicated support, custom data retention

### Pricing Formula

**Base Platform Fee**: $1,000/month (minimum commitment)

**Per-Seat Fee**: $25/seat/month
- Example: 100 seats = $2,500/month

**Per-Itinerary Fee**: $50 per 1,000 itineraries
- Example: 10,000 itineraries/month = $500/month
- Note: First 5,000 itineraries included in base fee

**SLA Premium**:
- Standard (99.9%): Included
- Enhanced (99.95%): +10% of total
- Premium (99.99%): +20% of total

**Add-Ons**:
- SSO/SAML: $500/month
- API Access: $1,000/month (includes 100,000 API calls, $0.01 per additional call)
- Dedicated Support: $2,000/month (named CSM, <4 hour response SLA)
- Custom Data Retention: $500/month (extend from 2 years to 5 years)

### Example Calculation

**Customer**: Acme Corp (500 employees, 20,000 itineraries/month, Enhanced SLA, SSO + API Access)

```
Base Platform Fee:           $1,000/month
Per-Seat (500 seats):       $12,500/month ($25 × 500)
Per-Itinerary (20,000):      $1,500/month ($50 × 30,000/1,000, first 5,000 included)
SLA Premium (Enhanced):      +10% of subtotal = $1,500/month
SSO/SAML:                      $500/month
API Access:                  $1,000/month

Subtotal (Monthly):         $18,000/month
Annual Discount (-15%):      -$2,700/month
──────────────────────────────────────
TOTAL (Monthly):            $15,300/month
TOTAL (Annual):            $183,600/year (billed annually)
```

**Annual Discount**: 10-20% discount for annual prepayment (12-month commitment)

---

## Team Pricing (SMB)

**Pricing**:
- 5-10 seats: $25/seat/month
- 11-25 seats: $22/seat/month
- 26-50 seats: $20/seat/month

**Features**:
- Team dashboard (view all team itineraries)
- Shared itinerary library
- Basic admin controls (add/remove users)
- Email support (<24 hour response)

**Example**:
- **Customer**: TravelCo (15 employees)
- **Pricing**: 15 seats × $22/seat = $330/month or $3,564/year (10% annual discount)

---

## White Label Pricing (OEM Partners)

**Pricing**:
- **Platform Fee**: $2,000/month (minimum)
- **Per-API-Call**: $0.01 per API call (after first 100,000)
- **Per-Itinerary**: $0.50 per itinerary generated (reseller revenue share)

**Features**:
- Custom branding (logo, colors, domain)
- API access (RESTful API, webhooks)
- Reseller terms (50/50 revenue share on subscriptions)
- Priority support (named technical account manager)

**Example**:
- **Customer**: GlobalTravel Inc. (OEM partner, 500,000 API calls/month, 10,000 itineraries/month)
- **Pricing**:
  - Platform Fee: $2,000/month
  - API Calls: $0.01 × 400,000 (500,000 - 100,000 included) = $4,000/month
  - Itineraries: $0.50 × 10,000 = $5,000/month
  - **Total**: $11,000/month or $118,800/year (10% annual discount)

---

## Master Service Agreement (MSA) Template

### MSA Sections

**1. Services**
- Scope of services (AI-powered travel itinerary generation)
- Service level commitments (SLA)
- Support terms

**2. Data Ownership**
- Customer retains ownership of all customer data
- Timbuktoo owns AI-generated content (non-exclusive license to customer)
- Customer grants Timbuktoo right to use data for service provision only

**3. Security Obligations**
- Timbuktoo maintains SOC 2 Type II certification
- Encryption at rest (AES-256) and in transit (TLS 1.2+)
- Annual penetration testing
- Incident notification within 24 hours

**4. AI Usage Disclaimer**
```
Timbuktoo provides AI-generated travel recommendations for informational purposes only.
Timbuktoo does NOT guarantee accuracy, availability, pricing, or safety of any recommendation.
Customer is solely responsible for verifying all AI-generated content before relying on it for
travel decisions or providing it to end users.
```

**5. SLA & Uptime**
- **Standard SLA**: 99.9% uptime (< 43 minutes downtime per month)
- **Enhanced SLA**: 99.95% uptime (< 22 minutes downtime per month)
- **Premium SLA**: 99.99% uptime (< 4 minutes downtime per month)

**SLA Credits** (if uptime falls below commitment):
- < Target: 10% monthly credit
- < Target - 0.5%: 25% monthly credit
- < Target - 1%: 50% monthly credit

**Exclusions**: Scheduled maintenance, customer-caused outages, force majeure

**6. Limitation of Liability**
```
IN NO EVENT SHALL TIMBUKTOO'S TOTAL LIABILITY EXCEED THE AMOUNT PAID BY CUSTOMER IN THE
TWELVE (12) MONTHS PRECEDING THE CLAIM.

TIMBUKTOO SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR
PUNITIVE DAMAGES, INCLUDING BUT NOT LIMITED TO LOSS OF PROFITS, DATA LOSS, OR BUSINESS
INTERRUPTION.
```

**7. Audit Rights** (Enterprise Only)
- Customer may audit Timbuktoo's security controls once per year (with 30 days' notice)
- Audit limited to security, privacy, and compliance controls relevant to customer data
- Audit report provided within 30 days of completion

**8. Termination & Data Return**
- **Termination for Convenience**: Either party may terminate with 30 days' notice (after initial term)
- **Termination for Cause**: Immediate termination for material breach (if not cured within 15 days)
- **Data Return**: Timbuktoo provides data export in JSON format within 30 days of termination
- **Data Deletion**: All customer data deleted within 90 days of termination (unless legally required to retain)

**9. Data Processing Agreement (DPA)**
- Required for EU customers (GDPR compliance)
- Specifies data processing terms, sub-processors, data transfers
- Standard Contractual Clauses (SCCs) for EU-US data transfers

**10. Governing Law**
- Governed by laws of [State], USA
- Jurisdiction: Courts of [City], [State]

---

## Contract Terms

**Initial Term**: 12 months (minimum for Enterprise tier)
**Renewal**: Auto-renewal for successive 12-month terms (unless terminated with 30 days' notice)
**Payment Terms**: Net 30 (monthly or annual prepayment)
**Late Payment**: 1.5% per month interest on overdue amounts

---

## Enterprise Sales Process

### Stage 1: Discovery (Week 1)
- Kickoff call (30 minutes)
- Understand customer requirements (seats, volume, SLA, integrations)
- Provide pricing estimate

### Stage 2: Proposal (Week 2)
- Custom pricing proposal (PDF or Google Doc)
- Technical architecture review (if needed)
- Security questionnaire (if requested)

### Stage 3: Legal Review (Week 3-4)
- MSA sent for customer legal review
- Redlines exchanged
- DPA provided (for EU customers)

### Stage 4: Contracting (Week 5)
- MSA signed (DocuSign or wet signature)
- Purchase Order (PO) received
- Invoice sent (Net 30 payment terms)

### Stage 5: Onboarding (Week 6)
- Dedicated Customer Success Manager (CSM) assigned
- Onboarding kickoff call (technical setup, SSO configuration)
- First production deployment (API keys, sandbox access)

**Total Sales Cycle**: 5-6 weeks (typical)

---

## Common Enterprise Requirements

### SSO/SAML Integration
**Supported IDPs**: Okta, Azure AD, OneLogin, Google Workspace
**Setup Time**: 1-2 weeks (requires IT collaboration)
**Cost**: $500/month

### API Access
**REST API**: Full CRUD operations (itinerary generation, user management, analytics)
**Rate Limits**: 10,000 requests/hour (enterprise tier)
**Documentation**: https://api.timbuktoo.app/docs
**Cost**: $1,000/month (includes 100,000 API calls)

### Custom Data Retention
**Default**: 2 years after last login
**Custom**: 5 years, 7 years, or indefinite (for archival)
**Cost**: $500/month

### Dedicated Support
**Named CSM**: Assigned customer success manager
**Response SLA**: < 4 hours (business hours)
**Escalation**: Direct phone line to CTO
**Cost**: $2,000/month

---

## Pricing FAQ

**Q: What's included in the base platform fee?**
A: Base fee includes platform access, up to 50 seats, up to 5,000 itineraries/month, standard SLA (99.9%), and email support.

**Q: Can we mix annual and monthly billing?**
A: Yes, but annual billing provides 10-20% discount.

**Q: Are there setup fees?**
A: No setup fees for Enterprise tier. White Label may incur $5,000 one-time setup fee for custom branding.

**Q: Can we cancel mid-contract?**
A: Yes, with 30 days' notice after initial 12-month term. No refunds for prepaid annual contracts.

**Q: What happens if we exceed our itinerary volume?**
A: Overages billed at $50 per 1,000 additional itineraries (prorated monthly).

**Q: Do you offer volume discounts?**
A: Yes, for 200+ seats or 100,000+ itineraries/month, contact enterprise@timbuktoo.app for custom pricing.

---

**Last Updated**: 2024-07-16
**Contact**: enterprise@timbuktoo.app
**Sales Team**: sales@timbuktoo.app
