# Customer Trust Portal – UI & Feature Specification

**Document Purpose**: Provide a comprehensive, production-ready specification for a customer-facing trust portal that accelerates enterprise sales, reduces security questionnaires, and centralizes compliance artifacts.

**Business Objectives**:
1. **Reduce Security Questionnaires**: Deflect 60-80% of security questions via self-service portal
2. **Accelerate Enterprise Sales**: Shorten sales cycle from 90 days to 45 days
3. **Increase Trust**: Demonstrate transparency and compliance best practices
4. **Support Procurement**: Provide one-stop-shop for legal/security teams

**Target Audience**:
- Enterprise buyers (CISOs, Security Teams, Procurement)
- Legal/Compliance teams
- Privacy officers
- Auditors
- Existing customers (ongoing compliance verification)

---

## Table of Contents

1. [Portal Objectives](#portal-objectives)
2. [Navigation Structure](#navigation-structure)
3. [Page-Level UI Specifications](#page-level-ui-specifications)
4. [Access Control Model](#access-control-model)
5. [Content Management](#content-management)
6. [Implementation Architecture](#implementation-architecture)
7. [Launch Plan](#launch-plan)
8. [Success Metrics](#success-metrics)

---

## Portal Objectives

### Primary Goals

| Goal | Metric | Target | Current (without portal) |
|------|--------|--------|--------------------------|
| **Reduce Security Questionnaires** | % of questions answered via portal | 70% | 0% (all manual) |
| **Accelerate Sales Cycles** | Average days from lead to contract | 45 days | 90 days |
| **Increase Close Rate** | Enterprise deals won | +25% | Baseline |
| **Reduce Sales Engineering Time** | Hours per enterprise deal | 10 hours | 40 hours |
| **Improve Trust Score** | Customer trust rating (survey) | 9/10 | Unknown |

### Secondary Goals

- **SEO**: Rank for "Timbuktoo security" searches
- **Customer Retention**: Provide ongoing compliance updates to existing customers
- **Competitive Differentiation**: Stand out from competitors without transparency
- **Audit Support**: Centralized evidence for customer audits (e.g., SOC-2 in-scope vendors)

---

## Navigation Structure

**Portal URL**: `https://trust.timbuktoo.ai`

**Top-Level Navigation** (Horizontal menu):

```
Trust Portal
├── Overview
├── Security
├── Compliance
├── Reliability
├── Privacy
├── Reports
└── Contact & Escalation
```

**Footer Navigation**:
- Legal (Terms of Service, Privacy Policy)
- Help (FAQ, Support Email)
- Company (About Us, Careers)

---

## Page-Level UI Specifications

### 1. Overview Page

**URL**: `/overview` (landing page)

**Purpose**: High-level summary of Timbuktoo's security posture and compliance status.

---

#### UI Components

##### A. Hero Section

**Layout**: Full-width banner with gradient background (Timbuktoo brand colors)

**Content**:
```
[LOGO] Timbuktoo Trust Portal

Heading: "Enterprise-Grade Security & Compliance"
Subheading: "Transparent. Audited. Always-On."

CTA Button: "Download SOC 2 Report" (NDA-gated)
Secondary CTA: "View Compliance Summary"
```

**Visuals**:
- Animated compliance badges (SOC-2, ISO 27001, GDPR-ready)
- Live uptime status (99.9% - green badge)

---

##### B. Platform Summary

**Layout**: 2-column grid

**Left Column - Architecture Diagram**:
```
[Interactive SVG Diagram]

Components:
- Customer (HTTPS/TLS 1.2+)
  ↓
- FastAPI + CloudFront WAF
  ↓
- Multi-Agent Orchestrator (Anthropic Claude 3.5)
  ↓
- Data Layer:
  - PostgreSQL (schema-per-tenant, encrypted at rest)
  - ChromaDB (vector embeddings, namespaced)
  ↓
- External APIs (encrypted, rate-limited):
  - Anthropic
  - OpenWeather
  - Google Maps

Security Layers:
- Network: VPC, Security Groups
- Access: RBAC, MFA, Quarterly Reviews
- Data: AES-256 (at rest), TLS 1.2+ (in transit)
- Monitoring: Datadog, PagerDuty, CloudTrail
```

**Right Column - Key Security Features**:
```
✅ Multi-Tenancy: Schema-per-tenant isolation
✅ Encryption: AES-256 (at rest), TLS 1.2+ (in transit)
✅ Access Control: RBAC with MFA, least privilege
✅ AI Safety: Deterministic workflows, source attribution
✅ Monitoring: 24/7 alerting, 15-min incident SLA
✅ Backups: Daily automated, quarterly restore tests
✅ Compliance: SOC-2 Type II, ISO 27001 (in progress)
```

---

##### C. Compliance Badges

**Layout**: Horizontal row of badges (clickable, expand to details)

**Badges**:
1. **SOC-2 Type II** (✅ Audited 2024)
   - Expand: "Annual audit by [Auditor Name], covers Security, Availability, Confidentiality, Privacy. Last audit: June 2024. Next audit: June 2025."
   - CTA: "Download Report" (NDA-gated)

2. **ISO 27001** (⏳ In Progress)
   - Expand: "Certification audit scheduled for Q1 2025. Gap closure 95% complete. Leveraging SOC-2 evidence for 70% of controls."
   - CTA: "View ISO Roadmap"

3. **GDPR-Ready** (✅ Compliant)
   - Expand: "Privacy policy, DSAR workflow (30-day SLA), data retention policy, DPO consultation."
   - CTA: "View Privacy Policy"

4. **CCPA-Compliant** (✅ Compliant)
   - Expand: "California-specific data deletion procedures, privacy notice."
   - CTA: "View CCPA Policy"

---

##### D. Current Audit Status

**Layout**: Timeline graphic

**Content**:
```
[Timeline Graphic]

2024 Q2: ✅ SOC-2 Type II Audit Passed (0 findings)
2024 Q3: ⏳ ISO 27001 Gap Closure (95% complete)
2024 Q4: 📅 Internal ISO Audit (scheduled)
2025 Q1: 📅 ISO 27001 Certification Audit
2025 Q2: 📅 SOC-2 Type II Re-audit
```

**Key Metric**: "Next External Audit: June 2025 (SOC-2 Type II)"

---

### 2. Security Page

**URL**: `/security`

**Purpose**: Detailed technical security controls and architecture.

---

#### UI Components

##### A. Access Control Model

**Layout**: Interactive diagram + table

**Diagram**: RBAC Hierarchy
```
[SVG Diagram]

Roles:
- Admin (2 users): Full access (production deploy, user mgmt, secrets)
- Engineer (8 users): Code, staging, read-only production
- Read-Only (7 users): Dashboards, logs (no writes)

Enforcement:
- PostgreSQL: Row-Level Security (RLS) per tenant
- AWS IAM: Role-based policies
- GitHub: CODEOWNERS file, branch protection
```

**Table**: Access Control Details
| Control | Implementation | Evidence |
|---------|----------------|----------|
| **RBAC** | 3 roles (Admin, Engineer, Read-Only) | RBAC matrix (updated quarterly) |
| **MFA** | 100% enforcement via AWS IAM | MFA adoption report |
| **Access Reviews** | Quarterly (Jira-automated) | 4 reviews/year, avg 15 removals |
| **Least Privilege** | Default deny, explicit grants | IAM policy audit logs |
| **Session Timeout** | 12 hours (idle timeout) | AWS IAM config |

---

##### B. AI Safety & Determinism

**Layout**: 2-column grid

**Left Column - Hallucination Prevention**:
```
Challenge: AI agents may recommend non-existent venues.

Mitigation:
1. **Source Attribution**: All venues must cite:
   - OpenStreetMap (OSM)
   - Wikidata
   - TripAdvisor
   - Trusted local guides

2. **Trust Tier Filtering**:
   - Sources rated 1-5 (5 = highest trust)
   - Minimum: ≥70% tier 4-5 sources
   - Block tier 1-2 sources

3. **Vector DB Cross-Check**:
   - Every venue recommendation is cross-checked with ChromaDB
   - If venue not in vector DB → block recommendation
   - Strict mode: 0 tolerance for unverified venues

4. **Wrk.Flo Gates**:
   - City Ingestion Gate: 12 automated checks (schema, attribution, trust tier)
   - Itinerary Generation Gate: 10 checks (hallucination detection, budget, safety)
```

**Right Column - Deterministic Workflows**:
```
Challenge: Non-determinism can lead to unpredictable outputs.

Mitigation:
1. **State Machine**: Immutable workflow sequence:
   Intent Parser → City Selection → Local Expert → Tools → Concierge → Post-Processor

2. **No Randomness**:
   - Temperature = 0 (deterministic Claude responses)
   - A/B testing uses MD5 hash (deterministic variant assignment)

3. **Variant Compliance**:
   - Control Variant: 2-3 activities/day (deterministic constraint)
   - Slow Hidden Gems Variant: 1-2 activities/day
   - Automated validation: Block itineraries violating variant rules

4. **Audit Trail**:
   - Every agent execution logged (Datadog)
   - Prompt, response, cost, variant tracked
```

---

##### C. Data Encryption Details

**Layout**: Table + diagram

**Table**: Encryption Standards
| Data State | Encryption Method | Key Management | Compliance |
|------------|-------------------|----------------|------------|
| **At Rest** | AES-256 | AWS KMS (auto-rotate annually) | SOC-2, ISO 27001 |
| **In Transit** | TLS 1.2+ | Let's Encrypt certs (auto-renew) | PCI DSS, GDPR |
| **Backups** | AES-256 | Separate KMS key (backup-only) | SOC-2 |
| **Secrets** | AES-256 | AWS Secrets Manager (90-day rotation) | SOC-2 |
| **Laptop Disks** | FileVault (Mac), BitLocker (Windows) | Employee-managed | ISO 27001 |

**Diagram**: Encryption Architecture
```
[SVG Diagram]

Customer Data Flow:
1. Customer → CloudFront (TLS 1.2+) → FastAPI
2. FastAPI → PostgreSQL (TLS + AES-256 at rest)
3. PostgreSQL → S3 Backup (encrypted in transit + at rest)
4. Secrets → AWS Secrets Manager (encrypted, auto-rotate)

Key Hierarchy:
- KMS Master Key (auto-rotate annually)
  ↓
- Data Encryption Keys (per-database, per-S3 bucket)
  ↓
- Encrypted Data
```

---

##### D. Tenant Isolation Explanation

**Layout**: Diagram + FAQ

**Diagram**: Multi-Tenancy Architecture
```
[SVG Diagram]

Single PostgreSQL Instance:
├── Schema: tenant_acme
│   ├── users, trips, feedback
│   └── RLS: WHERE tenant_id = 'acme'
├── Schema: tenant_globex
│   ├── users, trips, feedback
│   └── RLS: WHERE tenant_id = 'globex'
└── Schema: tenant_initech
    ├── users, trips, feedback
    └── RLS: WHERE tenant_id = 'initech'

ChromaDB Isolation:
├── Namespace: tenant_acme_vectors
├── Namespace: tenant_globex_vectors
└── Namespace: tenant_initech_vectors

Enforcement:
- PostgreSQL RLS: tenant_id filter on every query
- Application layer: Tenant context from JWT token
- Automated tests: 100 tests verify no cross-tenant data leakage
```

**FAQ**:
- Q: Can Tenant A see Tenant B's data?
  - A: No. PostgreSQL RLS enforces tenant_id filtering at the database level. Even if application code has a bug, the database blocks cross-tenant queries.

- Q: Are tenants on separate infrastructure?
  - A: No (schema-per-tenant, not database-per-tenant). This reduces costs while maintaining security via RLS. Meets SOC-2 multi-tenancy requirements.

- Q: How do you test tenant isolation?
  - A: 100 automated tests attempt cross-tenant access (all blocked). Quarterly penetration tests verify isolation.

---

### 3. Compliance Page

**URL**: `/compliance`

**Purpose**: Certifications, policies, and audit reports.

---

#### UI Components

##### A. SOC-2 Type II Report

**Layout**: Card with download CTA

**Content**:
```
[Card UI]

Title: SOC 2 Type II Report
Status: ✅ Audited (June 2024)
Auditor: [Auditor Firm Name]
Report Period: July 2023 - June 2024
Trust Services Criteria: Security, Availability, Confidentiality, Privacy
Findings: 0 exceptions

Description:
Timbuktoo's SOC 2 Type II report demonstrates operational effectiveness of controls over a 12-month period. The audit covered:
- Access controls (RBAC, MFA, access reviews)
- Change management (Wrk.Flo gates, GitHub PR reviews)
- Incident response (PagerDuty, RCA tickets)
- Data protection (encryption, backups, tenant isolation)
- Monitoring (Datadog, Prometheus, uptime SLAs)

[CTA Button: "Download Report" (NDA-gated)]
[Secondary CTA: "Request Audit Letter" (for RFPs)]
```

---

##### B. ISO 27001 Status

**Layout**: Progress tracker + roadmap

**Progress Tracker**:
```
[Progress Bar UI]

ISO 27001 Certification Progress: 95% Complete

✅ Gap Closure (95%):
  - Risk register: ✅ Complete
  - Asset inventory: ✅ Complete
  - ISMS scope: ✅ Complete
  - Statement of Applicability: ✅ Complete
  - 5 controls to implement: ⏳ In progress

⏳ Internal Audit (Scheduled Q4 2024):
  - External consultant audit
  - Expected findings: 0-2 minor observations

📅 Certification Audit (Q1 2025):
  - Stage 1: Documentation review
  - Stage 2: Control testing
  - Expected outcome: Certificate issued

[CTA: "Download ISO Roadmap PDF"]
```

**Roadmap Table**:
| Phase | Status | Completion Date |
|-------|--------|-----------------|
| Gap Closure | 95% | Oct 2024 (target) |
| Internal Audit | Scheduled | Nov 2024 |
| Stage 1 Audit | Planned | Jan 2025 |
| Stage 2 Audit | Planned | Feb 2025 |
| Certification | Expected | Mar 2025 |

---

##### C. ISO 27001 Mapping Summary

**Layout**: Table (interactive, expandable rows)

**Table**: SOC-2 to ISO 27001 Control Mapping
| SOC-2 Control | ISO 27001 Control | Description | Evidence Reuse |
|---------------|-------------------|-------------|----------------|
| CC6.1 (RBAC) | A.9.2.1 (Access provisioning) | Role-based access control | ✅ 100% reusable |
| CC6.2 (MFA) | A.9.4.2 (Secure authentication) | Multi-factor authentication | ✅ 100% reusable |
| CC7.2 (Backups) | A.12.3.1 (Information backup) | Daily automated backups | ✅ 100% reusable |
| CC8.1 (Change mgmt) | A.12.1.2 (Change management) | Wrk.Flo gates, PR reviews | ✅ 100% reusable |
| [+56 more rows, expandable] | | | |

**Summary**: "70% of ISO 27001 evidence reused from SOC-2 compliance, reducing incremental audit effort by 40%."

---

##### D. Policy Excerpts

**Layout**: Accordion UI (expandable sections)

**Policies**:
1. **Information Security Policy** (expand to view excerpt)
   - Summary: Master policy covering access control, encryption, incident response, risk management
   - Last Updated: 2024-06-01
   - [CTA: "Download Full Policy" (NDA-gated)]

2. **Data Retention & Deletion Policy**
   - Summary: PII retained 7 years, logs 90 days, automated S3 lifecycle rules
   - Last Updated: 2024-06-01
   - [CTA: "Download Policy"]

3. **Incident Response Plan**
   - Summary: SEV1/2/3 triage, 15-min alert SLA, PagerDuty on-call, RCA requirement
   - Last Updated: 2024-06-01
   - [CTA: "Download Plan"]

4. **Vendor Risk Management Policy**
   - Summary: Annual vendor assessments, SOC-2 requirement, NDA, security reviews
   - Last Updated: 2024-06-01
   - [CTA: "Download Policy"]

5. **Privacy Policy** (GDPR/CCPA)
   - Summary: Customer rights, DSAR workflow (30-day SLA), data deletion, DPO contact
   - Last Updated: 2024-06-01
   - [CTA: "View Public Privacy Policy" (no NDA required)]

---

### 4. Reliability Page

**URL**: `/reliability`

**Purpose**: Uptime metrics, incident history, and SLAs.

---

#### UI Components

##### A. Uptime Metrics

**Layout**: Dashboard with live status

**Metrics** (live from Datadog API):
```
[Dashboard UI]

Current Status: ✅ All Systems Operational

Uptime (Last 30 Days): 99.95%
Uptime (Last 90 Days): 99.93%
Uptime (Last 365 Days): 99.91%

SLA Commitment: 99.9% (monthly)
SLA Status: ✅ Met (exceeded by 0.05%)

[Live Status Indicators]
✅ API (FastAPI): Operational (response time: 120ms avg)
✅ Database (PostgreSQL): Operational
✅ Vector DB (ChromaDB): Operational
✅ Monitoring (Datadog): Operational
⚠️ Scheduled Maintenance: None
```

**Chart**: 90-Day Uptime History (line chart, daily granularity)

---

##### B. Incident History (Sanitized)

**Layout**: Timeline + table (last 12 months)

**Table**: Recent Incidents (sanitized, customer-safe)
| Date | Severity | Impact | Root Cause | Resolution Time | Status |
|------|----------|--------|------------|-----------------|--------|
| 2024-06-15 | SEV2 | API latency +200ms (5 min) | AWS RDS failover | 8 minutes | ✅ Resolved |
| 2024-04-22 | SEV3 | Cost overrun ($1.20 for 1 trip) | Agent logic bug | 45 minutes | ✅ Resolved + RCA |
| 2024-02-10 | SEV1 | 15-min API outage | Datadog alert misconfiguration | 12 minutes | ✅ Resolved + RCA |
| 2023-12-05 | SEV2 | ChromaDB degradation (slow queries) | Index corruption | 2 hours | ✅ Resolved |

**Key Metrics**:
- **SEV1 Incidents (12 months)**: 1
- **SEV2 Incidents (12 months)**: 2
- **SEV3 Incidents (12 months)**: 1
- **Average Resolution Time (SEV1)**: 12 minutes (SLA: 4 hours)
- **RCA Completion Rate**: 100%

**Transparency Note**: "All SEV1/SEV2 incidents undergo Root Cause Analysis (RCA) and corrective actions. RCA reports available to customers upon request (NDA-gated)."

---

##### C. Maintenance Notices

**Layout**: Calendar view + table

**Upcoming Maintenance**:
```
[Calendar UI]

No Scheduled Maintenance

Policy: Maintenance windows are Tuesdays/Thursdays 10:00-16:00 UTC (low-traffic periods). Customers notified 7 days in advance via email + status page.
```

**Past Maintenance** (last 6 months):
| Date | Type | Duration | Impact |
|------|------|----------|--------|
| 2024-05-10 | PostgreSQL minor upgrade | 15 minutes | ✅ Zero downtime (Multi-AZ failover) |
| 2024-03-15 | Datadog agent update | 5 minutes | ✅ Zero customer impact |

---

##### D. Service Level Agreements (SLAs)

**Layout**: Table

**SLAs**:
| Metric | SLA | Current Performance | Status |
|--------|-----|---------------------|--------|
| **Monthly Uptime** | 99.9% | 99.95% | ✅ Met |
| **API Response Time (p95)** | < 500ms | 180ms | ✅ Met |
| **Incident Response (SEV1)** | < 15 min | 12 min avg | ✅ Met |
| **Incident Resolution (SEV1)** | < 4 hours | 12 min avg | ✅ Met |
| **Cost Per Trip** | < $0.80 | $0.62 avg | ✅ Met |
| **RCA Completion (SEV1/SEV2)** | 100% | 100% | ✅ Met |

**SLA Credits**: "If monthly uptime < 99.9%, customers receive service credits per contract terms."

---

### 5. Privacy Page

**URL**: `/privacy`

**Purpose**: GDPR/CCPA compliance, data handling practices.

---

#### UI Components

##### A. Data Retention Policy

**Layout**: Table + flowchart

**Table**: Data Retention Periods
| Data Type | Retention Period | Deletion Method | Justification |
|-----------|------------------|-----------------|---------------|
| **Customer PII** (email, name, payment info) | 7 years | Automated S3 lifecycle policy + manual verification | Legal requirement (tax records) |
| **Trip Preferences** | 2 years after last login | Automated deletion (PostgreSQL job) | Business need (personalization) |
| **Agent Execution Logs** | 90 days | Automated deletion (Datadog) | Security monitoring (SOC-2 requirement) |
| **Feedback Ratings** | 5 years | Automated deletion | Product improvement |
| **Audit Logs** (access, changes) | 365 days | Immutable S3 archive | Compliance (SOC-2, ISO 27001) |
| **Backups** | 30 days | Automated deletion (S3 lifecycle) | Disaster recovery |

**Flowchart**: Data Lifecycle
```
[SVG Flowchart]

Data Collection → Active Use → Retention Period → Automated Deletion → Verification
                                       ↓
                               (if requested) → DSAR / Manual Deletion
```

---

##### B. Data Deletion Workflows

**Layout**: Step-by-step guide + form

**Customer-Initiated Deletion** (DSAR):
```
[Interactive Form UI]

Data Subject Access Request (DSAR) Form

Step 1: Verify Identity
  - Email address (must match account)
  - Last 4 digits of payment method (for verification)

Step 2: Select Request Type
  - [ ] Access my data (download all PII)
  - [ ] Delete my data (irreversible)
  - [ ] Correct my data (update PII)

Step 3: Submit Request
  - Processing time: 30 days (GDPR/CCPA requirement)
  - Confirmation email sent immediately
  - Status updates via email

[Submit DSAR Button]
```

**Deletion Process** (behind the scenes):
1. **Request Received** → Compliance Lead notified (Slack + email)
2. **Identity Verification** → Manual review (prevent fraud)
3. **Data Deletion** → Automated script deletes from:
   - PostgreSQL (`users`, `trips`, `feedback` tables)
   - S3 backups (mark for deletion, purge after 30 days)
   - Third-party systems (Anthropic logs, Datadog)
4. **Verification** → Compliance Lead verifies deletion (SQL query confirms 0 results)
5. **Customer Notification** → Email confirmation sent

---

##### C. GDPR Readiness

**Layout**: Checklist + diagram

**GDPR Compliance Checklist**:
```
[Checklist UI]

✅ Legal Basis for Processing: Legitimate interest (service delivery) + consent (marketing)
✅ Privacy Notice: Published at https://timbuktoo.ai/privacy
✅ Data Protection Officer (DPO): dpo@timbuktoo.ai (external consultant)
✅ Data Processing Agreements (DPAs): Signed with all vendors (Anthropic, Datadog, etc.)
✅ Data Subject Rights:
  ✅ Right to Access: DSAR form (30-day SLA)
  ✅ Right to Rectification: Self-service + support email
  ✅ Right to Erasure: DSAR form
  ✅ Right to Portability: JSON export via API
  ✅ Right to Object: Opt-out of marketing emails
✅ Data Breach Notification: 72-hour GDPR Article 33 compliance (incident runbook)
✅ Data Minimization: Only collect email, name, trip preferences (no unnecessary PII)
✅ Encryption: AES-256 (at rest), TLS 1.2+ (in transit)
✅ Cross-Border Transfers: AWS us-east-1 (US), standard contractual clauses (SCCs) for EU transfers
```

**Diagram**: GDPR Data Flow
```
[SVG Diagram]

EU Customer → CloudFront (TLS 1.2+) → AWS us-east-1 (SCCs in place) → PostgreSQL (encrypted)
                                                  ↓
                                   Data Processing Agreement (DPA) with Anthropic (US)
```

---

##### D. Sub-Processor List

**Layout**: Table (updated quarterly)

**Table**: Third-Party Sub-Processors
| Vendor | Service | Data Processed | Location | DPA Signed | SOC-2 Certified |
|--------|---------|----------------|----------|------------|-----------------|
| **Anthropic** | AI agents (Claude API) | Trip preferences, prompts (no PII) | US | ✅ Yes | ✅ Yes |
| **AWS** | Infrastructure (RDS, S3, KMS) | All data | US (us-east-1) | ✅ Yes | ✅ Yes |
| **Datadog** | Monitoring, logs | Execution logs (PII masked) | US | ✅ Yes | ✅ Yes |
| **Stripe** | Payment processing | Payment info (not stored by Timbuktoo) | US | ✅ Yes | ✅ Yes |
| **OpenWeather** | Weather data | City names (no PII) | EU | ✅ Yes | ❌ No (low risk) |
| **Google Maps** | Geocoding | City names, coordinates (no PII) | US | ✅ Yes | ✅ Yes |

**Update Frequency**: Quarterly (or upon vendor changes)
**Customer Notification**: Email notification 30 days before new sub-processor added

---

### 6. Reports Page

**URL**: `/reports`

**Purpose**: Downloadable compliance reports and documentation.

---

#### UI Components

##### A. SOC-2 Reports

**Layout**: List with download CTAs

**Available Reports**:
1. **SOC 2 Type II Report (2024)**
   - Report Period: July 2023 - June 2024
   - Auditor: [Auditor Firm Name]
   - Trust Services Criteria: Security, Availability, Confidentiality, Privacy
   - Findings: 0 exceptions
   - File: `Timbuktoo_SOC2_TypeII_2024.pdf` (87 pages)
   - [CTA: "Download Report" (NDA-gated, requires customer login)]

2. **SOC 2 Type I Report (2023)**
   - Report Date: June 2023
   - Auditor: [Auditor Firm Name]
   - Trust Services Criteria: Security, Availability
   - Findings: 0 exceptions
   - File: `Timbuktoo_SOC2_TypeI_2023.pdf` (45 pages)
   - [CTA: "Download Report" (NDA-gated)]

3. **SOC 2 Audit Letter (for RFPs)**
   - Summary letter confirming SOC-2 certification
   - No detailed findings (safe for RFP attachments)
   - File: `Timbuktoo_SOC2_Audit_Letter_2024.pdf` (2 pages)
   - [CTA: "Download Letter" (public, no NDA)]

---

##### B. Policy PDFs

**Layout**: Grid of downloadable PDFs

**Policies** (all NDA-gated except Privacy Policy):
1. **Information Security Policy** (15 pages)
2. **Access Control Policy** (8 pages)
3. **Data Retention & Deletion Policy** (6 pages)
4. **Incident Response Plan** (12 pages)
5. **Business Continuity Plan** (10 pages)
6. **Vendor Risk Management Policy** (7 pages)
7. **Privacy Policy** (public, 10 pages)
8. **Cryptographic Standards** (5 pages)

---

##### C. Penetration Test Summaries

**Layout**: List with sanitized summaries

**Available Reports**:
1. **Annual Penetration Test (2024)**
   - Test Date: May 2024
   - Tester: [Third-Party Firm Name]
   - Scope: API, web app, infrastructure
   - Critical Findings: 0
   - High Findings: 0
   - Medium Findings: 2 (both remediated)
   - Low Findings: 5 (3 remediated, 2 accepted risk)
   - File: `Timbuktoo_Pentest_Summary_2024.pdf` (sanitized, 8 pages)
   - [CTA: "Download Summary" (NDA-gated)]
   - [CTA: "Request Full Report" (requires security review, email-based)]

---

##### D. Security Whitepaper

**Layout**: Featured download (hero CTA)

**Whitepaper**: "Timbuktoo Security Architecture: Multi-Tenancy, AI Safety, and Compliance"

**Content**:
- Introduction to Timbuktoo platform
- Multi-agent AI architecture
- Tenant isolation (schema-per-tenant, RLS)
- AI safety (hallucination prevention, deterministic workflows)
- Encryption (at rest, in transit, key management)
- Compliance (SOC-2, ISO 27001, GDPR)
- Incident response (SLAs, RCA process)
- Monitoring and alerting (Datadog, PagerDuty)

**File**: `Timbuktoo_Security_Whitepaper_2024.pdf` (20 pages, technical audience)

**Audience**: CISOs, Security Engineers, Compliance Teams

[CTA: "Download Whitepaper" (public, no NDA)]

---

### 7. Contact & Escalation Page

**URL**: `/contact`

**Purpose**: Security contacts and incident escalation procedures.

---

#### UI Components

##### A. Security Contact Email

**Layout**: Contact form + email

**Primary Contact**:
```
[Contact Form UI]

For Security Inquiries:
Email: security@timbuktoo.ai
Response SLA: 24 hours (business days)

Use this contact for:
- Security questionnaires
- Vulnerability disclosures (responsible disclosure)
- Compliance questions (SOC-2, ISO 27001, GDPR)
- Vendor risk assessments

[Contact Form Fields]
- Name (required)
- Company (required)
- Email (required)
- Subject (dropdown: Security Questionnaire, Vulnerability Disclosure, Compliance Question, Other)
- Message (textarea)

[Submit Button]
```

---

##### B. Responsible Disclosure Policy

**Layout**: Policy text + form

**Policy**:
```
Timbuktoo welcomes responsible security researchers to report vulnerabilities.

Responsible Disclosure Guidelines:
1. **Report privately**: Email security@timbuktoo.ai (do not disclose publicly)
2. **Allow time to fix**: We commit to 90-day remediation for critical findings
3. **No malicious activity**: Do not access customer data, disrupt service, or exfiltrate data
4. **Safe harbor**: We will not pursue legal action against responsible disclosures

Scope:
✅ In Scope:
  - https://api.timbuktoo.ai
  - https://app.timbuktoo.ai
  - https://trust.timbuktoo.ai

❌ Out of Scope:
  - Social engineering (phishing employees)
  - Physical security
  - Third-party services (Anthropic, AWS)

Rewards:
- Critical: $500-$2,000 (data breach, RCE)
- High: $250-$500 (authentication bypass, XSS)
- Medium: $100-$250 (CSRF, information disclosure)
- Low: Recognition (public acknowledgment)

[CTA: "Report Vulnerability" (email form)]
```

---

##### C. Incident Escalation SLAs

**Layout**: Table

**Escalation Tiers** (for customer-impacting incidents):
| Severity | Response Time | Resolution Time | Escalation Path |
|----------|---------------|-----------------|-----------------|
| **SEV1** (outage, data breach) | 15 minutes | 4 hours | On-call engineer → Platform Owner → VP Engineering |
| **SEV2** (degradation) | 1 hour | 24 hours | On-call engineer → Platform Owner |
| **SEV3** (minor issue) | 4 hours | 7 days | Support → Engineering |

**Customer Notification**:
- **SEV1**: Immediate (status page + email + Slack if applicable)
- **SEV2**: Within 1 hour
- **SEV3**: Daily summary

**Escalation Contact** (for enterprise customers):
- Email: incidents@timbuktoo.ai
- Slack Connect: #timbuktoo-incidents (for customers with dedicated Slack channels)
- Phone (SEV1 only): +1-555-TIMBUKTOO (toll-free)

---

##### D. Trust Portal Feedback

**Layout**: Feedback form

**Feedback Form**:
```
[Form UI]

Help Us Improve This Trust Portal

What information were you looking for?
[Textarea]

Did you find what you needed?
[ ] Yes
[ ] No (please explain below)

What would make this portal more useful?
[Textarea]

[Submit Feedback Button]
```

---

## Access Control Model

**Three Access Tiers**:

### Tier 1: Public (No Authentication)

**Pages**:
- Overview (landing page)
- Security (general architecture, no sensitive details)
- Compliance (high-level badges, no report downloads)
- Reliability (uptime metrics, sanitized incident history)
- Privacy (public-facing policies)
- Contact (security email, responsible disclosure policy)

**Content**:
- Marketing-safe information
- No customer data
- No detailed reports

---

### Tier 2: NDA-Gated (Requires NDA Signature)

**Pages**:
- Reports (SOC-2 reports, policies, pentest summaries)

**Access Process**:
1. Prospect/customer fills out NDA request form
2. Legal team sends NDA via DocuSign
3. NDA signed → Access granted (unique login link via email)
4. Login persists for 90 days

**Content**:
- SOC-2 Type II reports
- Policy PDFs (detailed)
- Penetration test summaries
- Security whitepapers

**Tracking**:
- Log all downloads (who, what, when)
- Notify sales team (lead tracking)

---

### Tier 3: Customer-Only (Requires Active Contract)

**Pages**:
- Incidents (detailed RCA reports for customer-impacting incidents)
- Dedicated Status Page (real-time alerts for customer's tenant)

**Access Process**:
1. Customer signs contract → Account provisioned
2. SSO or email-based login
3. Customer sees only incidents affecting their tenant

**Content**:
- Detailed RCA reports (root cause, corrective actions)
- Customer-specific uptime metrics
- Maintenance notifications (7-day advance notice)
- Escalation contacts

---

## Content Management

### Content Ownership

| Page | Content Owner | Update Frequency | Approval Required |
|------|---------------|------------------|-------------------|
| **Overview** | Marketing + Security Lead | Quarterly | VP Marketing |
| **Security** | Security Lead | Quarterly (or upon architecture changes) | CISO |
| **Compliance** | Compliance Lead | Monthly (audit status updates) | CISO |
| **Reliability** | Platform Owner | Real-time (Datadog API integration) | None (automated) |
| **Privacy** | Legal + DPO | Annually (or upon policy changes) | General Counsel |
| **Reports** | Compliance Lead | Upon audit completion | CISO |
| **Contact** | Security Lead | Annually | CISO |

---

### Update Triggers

**Automatic Updates** (via API integration):
- Uptime metrics (Datadog API, real-time)
- Incident history (PagerDuty API, daily sync)
- SOC-2 status (manual update, quarterly)

**Manual Updates**:
- Architecture diagrams (upon major changes)
- Policy PDFs (upon annual review or changes)
- Compliance badges (upon certification)

---

### Version Control

**All Content in Git**:
- Repository: `timbuktoo-trust-portal` (private GitHub repo)
- Branching: `main` (production), `staging` (preview), feature branches
- Deployment: GitHub Actions → S3 → CloudFront (CDN)
- Approval: Pull request review required (2 approvers: Content Owner + CISO)

---

## Implementation Architecture

### Tech Stack

**Frontend**:
- **Framework**: Next.js (React) for SEO and server-side rendering
- **Styling**: Tailwind CSS (Timbuktoo brand colors)
- **Charts**: Chart.js or Recharts (uptime graphs, risk heatmaps)
- **Icons**: Heroicons or Lucide (compliance badges)

**Backend** (minimal, mostly static):
- **Hosting**: AWS S3 + CloudFront (CDN)
- **Authentication**: Auth0 or AWS Cognito (for NDA-gated / customer-only content)
- **API Integrations**:
  - Datadog API (uptime metrics, incident history)
  - PagerDuty API (incident status)
  - Internal Timbuktoo API (customer tenant info for Tier 3)

**Analytics**:
- **Google Analytics**: Track page views, downloads, conversions (prospect → NDA → customer)
- **Hotjar**: Heatmaps, session recordings (optimize UX)

**Security**:
- **TLS 1.2+**: CloudFront enforces HTTPS
- **CSP Headers**: Content Security Policy (prevent XSS)
- **Rate Limiting**: CloudFront WAF (prevent DDoS)

---

### Deployment

**Environments**:
- **Staging**: `https://staging-trust.timbuktoo.ai` (internal preview)
- **Production**: `https://trust.timbuktoo.ai` (public)

**CI/CD Pipeline** (GitHub Actions):
1. **Code Push** → Feature branch
2. **PR Review** → 2 approvers (Content Owner + CISO)
3. **Merge to `main`** → Auto-deploy to staging
4. **Manual Approval** → Deploy to production (CISO approval)
5. **Rollback** → One-click revert (S3 versioning)

---

## Launch Plan

### Pre-Launch Checklist (4 weeks)

**Week 1: Content Preparation**
- [ ] Write all page copy (Marketing + Security Lead)
- [ ] Create architecture diagrams (Engineering Lead)
- [ ] Sanitize incident history (Platform Owner)
- [ ] Prepare SOC-2 report PDFs (Compliance Lead)
- [ ] Draft NDA template (Legal)

**Week 2: Development**
- [ ] Build Next.js site (Engineering)
- [ ] Integrate Datadog API (uptime metrics)
- [ ] Implement Auth0 (NDA-gated access)
- [ ] Set up CloudFront + S3 (hosting)
- [ ] Configure Google Analytics

**Week 3: Testing**
- [ ] Internal QA (all pages, all tiers)
- [ ] Security review (CISO approval)
- [ ] Legal review (General Counsel approval)
- [ ] Accessibility audit (WCAG 2.1 AA compliance)
- [ ] Load testing (CloudFront caching)

**Week 4: Soft Launch**
- [ ] Invite 5 friendly customers (beta feedback)
- [ ] Fix bugs, refine UX
- [ ] Prepare launch announcement (blog post, email)
- [ ] Train sales team (how to use portal in sales calls)

---

### Launch Announcement

**Channels**:
- **Blog Post**: "Introducing the Timbuktoo Trust Portal: Transparency at Scale"
- **Email**: Existing customers + prospects (mailing list)
- **LinkedIn**: Company post + personal posts from CEO, CISO
- **Sales Collateral**: Add trust portal link to pitch decks, RFP templates

**Key Messaging**:
- "We're making security and compliance effortless for enterprise buyers."
- "Download our SOC-2 report, view uptime metrics, and see our security architecture—all in one place."
- "Accelerate your procurement process with self-service compliance documentation."

---

## Success Metrics

### Primary KPIs (measured monthly)

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **Security Questionnaire Deflection Rate** | 70% | Sales team survey: "Was the trust portal helpful?" |
| **Average Sales Cycle (Enterprise)** | 45 days | Salesforce: Days from lead to contract |
| **Trust Portal Traffic** | 500 unique visitors/month | Google Analytics |
| **SOC-2 Report Downloads** | 50 downloads/month | Auth0 logs (NDA-gated downloads) |
| **NDA Signature Rate** | 80% | DocuSign: Signed NDAs / Sent NDAs |
| **Customer Satisfaction (Trust Portal)** | 4.5/5 | Feedback form (7-point Likert scale) |

---

### Secondary KPIs

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **Page Views per Visitor** | 3.5 pages | Google Analytics (engagement) |
| **Bounce Rate** | < 30% | Google Analytics (landing page effectiveness) |
| **Time on Site** | > 5 minutes | Google Analytics (content depth) |
| **Mobile Traffic** | > 40% | Google Analytics (responsive design validation) |
| **Uptime (Trust Portal)** | 99.95% | CloudFront metrics |

---

### ROI Analysis

**Cost Savings** (annual):
- **Sales Engineering Time**: 30 hours saved per enterprise deal × 20 deals/year × $150/hour = **$90,000/year**
- **Legal NDA Review Time**: 2 hours saved per NDA × 50 NDAs/year × $200/hour = **$20,000/year**
- **Compliance Team Time**: 10 hours saved per security questionnaire × 40 questionnaires/year × $100/hour = **$40,000/year**

**Total Savings**: **$150,000/year**

**Implementation Cost** (one-time):
- Development (4 weeks × $10K/week) = $40,000
- Design (1 week × $8K/week) = $8,000
- Content creation (2 weeks × $5K/week) = $10,000
- **Total**: **$58,000**

**Ongoing Cost** (annual):
- Hosting (S3 + CloudFront) = $1,200/year
- Auth0 (authentication) = $2,400/year
- Content updates (4 hours/month × $100/hour) = $4,800/year
- **Total**: **$8,400/year**

**ROI**: ($150,000 - $8,400) / $58,000 = **244% first-year ROI**
**Payback Period**: 4.6 months

---

## Appendix: Sample Screens

### Overview Page (Wireframe)

```
[Header: Logo | Overview | Security | Compliance | Reliability | Privacy | Reports | Contact]

[Hero Section]
┌─────────────────────────────────────────────────────────────┐
│ [Timbuktoo Logo]                                            │
│                                                              │
│ Enterprise-Grade Security & Compliance                      │
│ Transparent. Audited. Always-On.                            │
│                                                              │
│ [Download SOC 2 Report] [View Compliance Summary]           │
│                                                              │
│ [✅ SOC-2] [⏳ ISO 27001] [✅ GDPR] [99.95% Uptime]         │
└─────────────────────────────────────────────────────────────┘

[Platform Summary - 2 columns]
┌────────────────────────┬────────────────────────────────────┐
│ [Architecture Diagram] │ Key Security Features:             │
│                        │ ✅ Multi-Tenancy (schema-per-tenant)│
│  Customer              │ ✅ Encryption (AES-256, TLS 1.2+)  │
│    ↓                   │ ✅ RBAC + MFA                      │
│  FastAPI               │ ✅ AI Safety (no hallucinations)   │
│    ↓                   │ ✅ 24/7 Monitoring                 │
│  Multi-Agent           │ ✅ Daily Backups                   │
│    ↓                   │ ✅ SOC-2 Type II Certified         │
│  PostgreSQL + ChromaDB │                                    │
└────────────────────────┴────────────────────────────────────┘

[Compliance Badges - Expandable]
┌──────────┬──────────┬──────────┬──────────┐
│ SOC-2    │ ISO 27001│ GDPR     │ CCPA     │
│ ✅ 2024  │ ⏳ Q1 25 │ ✅ Ready │ ✅ Ready │
│ [Expand] │ [Expand] │ [Expand] │ [Expand] │
└──────────┴──────────┴──────────┴──────────┘

[Current Audit Status - Timeline]
2024 Q2: ✅ SOC-2 Type II Passed
2024 Q3: ⏳ ISO 27001 Gap Closure (95%)
2025 Q1: 📅 ISO Certification Audit

[Footer: Legal | Help | Company]
```

---

**Document Version**: 1.0
**Owner**: VP Marketing + CISO
**Approval Date**: 2024-07-15
**Next Review**: 2025-01-15 (semi-annual)
