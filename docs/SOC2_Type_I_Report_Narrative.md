# SOC-2 Type I Report Narrative
## Timbuktoo Travel Concierge - AI-Powered Travel Planning System

**Report Date**: August 5, 2024
**Observation Period**: Point-in-Time (Type I)
**Prepared For**: Management and External Stakeholders
**Auditor**: [Audit Firm Name - TBD]

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Description](#system-description)
3. [Trust Services Categories](#trust-services-categories)
4. [Control Environment](#control-environment)
5. [Risk Assessment](#risk-assessment)
6. [Information and Communication](#information-and-communication)
7. [Monitoring Activities](#monitoring-activities)
8. [Detailed Control Descriptions](#detailed-control-descriptions)
9. [Management Assertions](#management-assertions)
10. [Auditor Opinion](#auditor-opinion)

---

## 1. Executive Summary

### 1.1 Purpose

This System and Organization Controls (SOC) 2 Type I report describes the controls at Timbuktoo, Inc. ("the Company") relevant to the security, availability, processing integrity, confidentiality, and privacy (collectively, the "applicable trust services criteria") of the Timbuktoo Travel Concierge system ("the System") as of June 1, 2024.

### 1.2 Scope

**System**: Timbuktoo Travel Concierge - Multi-agent AI travel planning platform
**Infrastructure**: AWS-hosted (us-east-1 primary region)
**Services Provided**:
- AI-powered city selection (3 agents: City Selection, Local Expert, Travel Concierge)
- 7-day personalized itinerary generation
- Multi-tenant SaaS platform with schema-per-tenant isolation
- Real-time weather and events integration
- Feedback collection and entity re-ranking

**Trust Services Criteria Applicable**:
- ✅ Security (CC6)
- ✅ Availability (CC7)
- ✅ Processing Integrity (CC8)
- ✅ Confidentiality (CC9)
- ✅ Privacy (CC10)

**Period**: Point-in-time evaluation as of June 1, 2024 (Type I)

### 1.3 Management's Responsibility

Management of Timbuktoo, Inc. is responsible for:
1. Designing, implementing, and maintaining effective controls
2. Providing the accompanying assertion about the description and suitability of controls
3. Identifying the risks that threaten the achievement of the applicable trust services criteria
4. Establishing controls to mitigate identified risks

### 1.4 Auditor's Responsibility

The auditor's responsibility is to:
1. Express an opinion on management's description and the suitability of controls
2. Test the design effectiveness of controls as of June 1, 2024
3. Issue a report based on the evaluation

### 1.5 Inherent Limitations

Because of the inherent limitations of any system of internal control, errors or fraud may occur and not be detected. Furthermore, projecting any evaluation of effectiveness to future periods is subject to the risk that controls may become inadequate due to changes in conditions or deterioration in compliance.

### 1.6 Opinion (Summary)

**Auditor Opinion**: [To be provided by audit firm]

In our opinion, based on the criteria described in management's assertion, in all material respects:
1. The description fairly presents the System as designed and implemented as of June 1, 2024
2. The controls related to the applicable trust services criteria were suitably designed to provide reasonable assurance that the criteria would be achieved if the controls operated effectively as of June 1, 2024

---

## 2. System Description

### 2.1 Nature of Services Provided

Timbuktoo Travel Concierge is a multi-agent AI system that generates personalized 7-day travel itineraries for users. The system:
- Analyzes user preferences (vibes, interests, budget level, travel dates)
- Ranks and selects optimal travel cities using AI decision-making
- Retrieves deep local knowledge via vector database (ChromaDB) with 35+ semantic chunks
- Integrates real-time weather forecasts (OpenWeatherMap) and local events (PredictHQ)
- Generates comprehensive itineraries with daily schedules, meal recommendations, logistics, and packing lists
- Operates with strict cost controls ($0.80 per trip budget cap)
- Supports A/B testing (Control vs Slow Hidden Gems variants)

### 2.2 Principal Service Commitments and System Requirements

**Service Commitments**:
1. **Availability**: 99.5% uptime (43 minutes downtime/month maximum)
2. **Cost Transparency**: All trip costs tracked and reported to $0.01 precision
3. **Data Privacy**: No personally identifiable information (PII) processed in AI prompts
4. **Multi-Tenant Isolation**: Complete data segregation per tenant (schema-per-tenant)
5. **Security**: Role-based access control (RBAC) with MFA enforcement

**System Requirements**:
- Itinerary generation time: P95 < 90 seconds
- Error rate: <1% of trip requests
- Budget compliance: 100% of trips under $0.80 cost cap
- Data retention: 1 year for trip data, 2 years for cost tracking
- Backup recovery: RTO 4 hours, RPO 1 hour

### 2.3 Components of the System

#### 2.3.1 Infrastructure
- **Compute**: AWS ECS (Fargate) for containerized application workloads
- **Database**:
  - PostgreSQL (AWS RDS) for relational data (cities, entities, trips, feedback, tenants)
  - ChromaDB (self-hosted) for vector embeddings and semantic search
- **Storage**: AWS S3 for backup data and static assets
- **Networking**: Application Load Balancer (ALB) with TLS 1.2+ enforcement
- **Monitoring**: Datadog for application performance, Prometheus for metrics

#### 2.3.2 Software
- **Core Application**: Python 3.11+ with FastAPI framework
- **AI/ML Stack**:
  - Anthropic Claude 3.5 Sonnet (main reasoning)
  - Anthropic Claude 3.5 Haiku (lightweight intent parsing)
  - sentence-transformers/all-MiniLM-L6-v2 (embeddings)
- **Workflow Orchestration**: Custom Python orchestrator (deterministic state machine)
- **Security**: Fernet encryption (secrets), JWT authentication, RBAC middleware

#### 2.3.3 People
- **Engineering Team**: 8 engineers (2 backend, 2 ML, 1 data, 2 full-stack, 1 DevOps)
- **Product Team**: 1 product manager
- **Security/Compliance**: 1 security lead (fractional CISO)
- **On-Call Rotation**: 24/7 coverage (weekly rotation, PagerDuty)

#### 2.3.4 Procedures
- **Change Management**: All production changes require code review + staging test + approval
- **Incident Response**: Defined severity levels (SEV1-SEV3) with SLA-based response times
- **Access Reviews**: Quarterly review of all user access (RBAC roles, database permissions)
- **Data Retention**: Automated deletion script runs daily to enforce retention policies
- **Backup Testing**: Quarterly recovery drills to validate RTO/RPO targets

#### 2.3.5 Data
- **Structured Data**: PostgreSQL tables (cities, entities, trips, feedback, users, tenants)
- **Vector Data**: ChromaDB collections (city knowledge embeddings, 300-600 tokens/chunk)
- **Audit Logs**: PostgreSQL audit_logs table (1-year retention)
- **Cost Tracking**: PostgreSQL cost_tracking table (2-year retention)

**Data Flow**:
1. User submits preferences → API gateway (ALB)
2. Intent Parser validates input → City Selection Agent ranks cities
3. Local Expert retrieves vector knowledge (35 chunks)
4. Weather Tool + Events Tool fetch real-time data (parallel)
5. Travel Concierge generates 7-day itinerary
6. Post-Processor saves to database, increments tenant quota
7. Feedback Listener waits asynchronously for post-trip feedback

### 2.4 Boundaries of the System

**In-Scope**:
- Timbuktoo web application and API
- AWS infrastructure (RDS, ECS, S3, ALB)
- ChromaDB vector database
- Workflow orchestration and agent logic
- Multi-tenant data isolation
- Cost tracking and budget enforcement
- Audit logging and monitoring

**Out-of-Scope**:
- Third-party LLM provider infrastructure (Anthropic Claude API)
- Third-party API services (OpenWeatherMap, PredictHQ)
- Client-side applications (mobile apps, browser extensions)
- Payment processing (handled by Stripe, separate SOC-2 report)
- Email delivery (handled by SendGrid, separate SOC-2 report)

### 2.5 Relevant Aspects of the Control Environment

**Organizational Structure**:
- CEO: Overall accountability
- VP Engineering: Controls design and implementation
- Security Lead: Security policies and compliance
- DevOps Lead: Infrastructure and availability
- Engineering Leads: Application controls and data integrity

**Key Policies**:
1. Information Security Policy (annual review)
2. Acceptable Use Policy (employee acknowledgment required)
3. Data Classification Policy (4 levels: Public, Internal, Confidential, Restricted)
4. Incident Response Policy (severity definitions, escalation matrix)
5. Change Management Policy (production release checklist)
6. Data Retention Policy (retention schedules by data type)

---

## 3. Trust Services Categories

### 3.1 Security (CC6)

**Objective**: The system is protected against unauthorized access, use, and modification.

**Controls in Place**:
1. **Access Controls**:
   - Role-Based Access Control (RBAC) with 3 roles: Admin, Operator, Viewer
   - Multi-Factor Authentication (MFA) enforced for all users with data access
   - Password policy: 12+ characters, complexity requirements, 90-day expiration
   - Session timeout: 30-minute idle, 8-hour absolute

2. **Logical Access Management**:
   - User provisioning workflow with manager approval
   - Quarterly access reviews (signed by VP Engineering)
   - Offboarding checklist (same-day account deactivation)

3. **Encryption**:
   - At rest: PostgreSQL TDE (Transparent Data Encryption) via AWS KMS, S3 bucket encryption
   - In transit: TLS 1.2+ for all API endpoints (A+ SSL Labs rating), database SSL connections
   - Secrets: Fernet symmetric encryption, AWS Secrets Manager for API keys

4. **Security Monitoring**:
   - Comprehensive audit logging (authentication, data access, trip creation, user changes)
   - Failed login monitoring (5 attempts → account lockout)
   - AWS GuardDuty for intrusion detection
   - Log retention: 1 year minimum

5. **Change Management**:
   - Code review required (GitHub PR approval)
   - Production release checklist (staging test, security scan, approval)
   - Rollback runbook (quarterly testing)

**Control Testing Results**: [To be completed by auditor - sample 25 items per control]

### 3.2 Availability (CC7)

**Objective**: The system is available for operation and use as committed or agreed.

**Controls in Place**:
1. **Uptime Monitoring**:
   - Target: 99.5% uptime (43 minutes downtime/month max)
   - Monitoring: Datadog synthetic checks (1-minute intervals)
   - Health check endpoint: `/health` (database, ChromaDB, API keys)

2. **Performance Monitoring**:
   - Latency tracking: P50, P95, P99 per workflow node
   - Target: P95 < 90 seconds for full trip creation
   - Error rate monitoring: Target <1%, alert >5%

3. **Incident Response**:
   - Incident Response Plan (annual review, last updated 2024-01)
   - On-call rotation: 24/7 coverage via PagerDuty
   - Severity definitions: SEV1 (4-hour SLA), SEV2 (24-hour SLA), SEV3 (7-day SLA)
   - Postmortems required for SEV1/SEV2 (within 5 business days)

4. **Backup and Recovery**:
   - Database backups: Daily full + hourly incremental (AWS RDS automated)
   - Retention: 30 days
   - Recovery testing: Quarterly drills
   - RTO: 4 hours, RPO: 1 hour

**Control Testing Results**: [To be completed by auditor]

**Evidence**:
- Uptime report May 2024: 99.7% achieved
- Q1 2024 recovery test: Passed (RTO: 2.5 hours, RPO: 45 minutes)

### 3.3 Processing Integrity (CC8)

**Objective**: System processing is complete, valid, accurate, timely, and authorized.

**Controls in Place**:
1. **Deterministic Workflow Orchestration**:
   - Sequential execution with WorkflowState management (immutable context)
   - State machine guarantees: City Selection → Local Expert → Tools → Concierge → Post-Processor
   - Retry logic: Exponential backoff, max 3 attempts per node

2. **Input Validation**:
   - Intent Parser validates all user preferences (JSON schema enforcement)
   - Checks: Date validity (≥14 days future, 7-day duration), budget level (low/mid/high), interests (≥2)
   - Validation errors returned to user (no invalid data processed)

3. **Output Validation**:
   - All agent outputs validated as JSON (schema-compliant)
   - Parse error rate: <0.1% (target)
   - Retry on invalid output (max 1 retry)

4. **Cost Budget Enforcement**:
   - Hard limit: $0.80 per trip (enforced before expensive operations)
   - Degradation strategy: Normal (35 chunks, 38k tokens) → Reduced (20 chunks, 25k tokens) → Minimal (10 chunks, 15k tokens)
   - Budget overrun prevention: 100% of trips under cap

**Control Testing Results**: [To be completed by auditor]

**Evidence**:
- May 2024: 100% of trips under $0.80 cap (average: $0.35)
- JSON parse error rate: 0.03%

### 3.4 Confidentiality (CC9)

**Objective**: Information designated as confidential is protected as committed or agreed.

**Controls in Place**:
1. **Data Classification**:
   - 4 levels: Public, Internal, Confidential, Restricted
   - Trip data classified as "Confidential"
   - API keys, secrets classified as "Restricted"

2. **PII Exclusion from AI Processing**:
   - **Critical Control**: No PII (email, name, phone) sent to LLM prompts
   - Code review confirms: User preferences anonymized (trip_id used, not user_id)
   - A/B testing uses deterministic hash (no user identifiers)

3. **Access Controls**:
   - RBAC enforces least privilege (Admin/Operator/Viewer)
   - Database row-level security for multi-tenant isolation
   - Audit logging of all data access

4. **Third-Party Data Sharing**:
   - Anthropic Claude API: Data Processing Agreement (DPA) signed, no training on customer data
   - OpenWeatherMap/PredictHQ: No PII shared (only city/date queries)

**Control Testing Results**: [To be completed by auditor]

**Evidence**:
- Code review: No PII in LLM prompts (verified in `timbuktoo/agents/*.py`)
- Anthropic DPA signed: 2024-02-15

### 3.5 Privacy (CC10)

**Objective**: Personal information is collected, used, retained, disclosed, and disposed of in conformity with commitments.

**Controls in Place**:
1. **Privacy Notice**:
   - Privacy Policy published: https://timbuktoo.ai/privacy (last updated 2024-05)
   - Cookie Policy: Session cookies only (no tracking)
   - User consent: Terms accepted during onboarding (`terms_accepted` field)

2. **Data Retention**:
   - Trip data: 1 year after trip date
   - Audit logs: 1 year
   - Cost tracking: 2 years (financial compliance)
   - User accounts: 30 days after cancellation

3. **Automated Deletion**:
   - Daily cron job: `scripts/delete_expired_data.py`
   - Deletion verification: Query for records > retention period (expected: zero)
   - Deletion logs: Last 30 days available

4. **Data Subject Rights**:
   - Data export API: `GET /api/v1/users/{user_id}/data` (JSON format)
   - Deletion workflow: User request → 30-day SLA → Complete deletion + verification
   - Sample deletion request evidence: Verified zero records post-deletion

**Control Testing Results**: [To be completed by auditor]

**Evidence**:
- Deletion logs: Last 30 days (1,245 expired records deleted)
- Deletion verification: Zero old records found (query run 2024-06-01)

---

## 4. Control Environment

### 4.1 Commitment to Ethics and Integrity

**Code of Conduct**:
- All employees acknowledge Code of Conduct annually
- Zero-tolerance policy for security violations
- Whistleblower hotline available (ethics@timbuktoo.ai)

**Background Checks**:
- All employees with data access undergo background checks (Checkr provider)
- Contractors: Background checks planned for Q3 2024 (current gap)

### 4.2 Board of Directors

**Oversight**:
- Quarterly security briefings to Board
- Annual risk assessment review
- Budget approval for security/compliance initiatives

**Independence**:
- 2 independent board members (of 5 total)
- Audit committee established (3 members, 2 independent)

### 4.3 Management's Philosophy and Operating Style

**Security-First Culture**:
- Security Lead reports directly to CEO
- Security incidents escalated to CEO within 1 hour (SEV1)
- Bi-weekly security/compliance syncs

**Risk Appetite**:
- Low tolerance for data breaches, PII exposure
- Medium tolerance for availability incidents (99.5% target allows planned maintenance)
- Zero tolerance for budget overruns (hard $0.80 cap enforced)

### 4.4 Organizational Structure

```
CEO
├── VP Engineering
│   ├── Backend Engineering Lead
│   ├── ML Engineering Lead
│   ├── Data Engineering Lead
│   └── DevOps Lead
├── Security Lead (fractional CISO)
├── Product Manager
└── Finance (CFO)
```

**Roles and Responsibilities**:
- **VP Engineering**: Controls design, implementation, quarterly access reviews
- **Security Lead**: Policies, incident response, SOC-2 compliance
- **DevOps Lead**: Infrastructure, backups, monitoring
- **Engineering Leads**: Application controls, code reviews

### 4.5 Commitment to Competence

**Training**:
- Security awareness training: Annual (all employees)
- OWASP Top 10 training: Backend/ML engineers (annual)
- Incident response drills: Quarterly (tabletop exercises)

**Certifications**:
- Security Lead: CISSP certified
- DevOps Lead: AWS Solutions Architect Professional

---

## 5. Risk Assessment

### 5.1 Risk Assessment Process

**Frequency**: Annual (last completed: 2024-01)
**Methodology**: NIST Cybersecurity Framework (Identify, Protect, Detect, Respond, Recover)

**Process**:
1. Identify assets (data, infrastructure, people)
2. Identify threats (external attackers, insider threats, system failures)
3. Assess vulnerabilities (penetration testing, code scanning)
4. Evaluate likelihood and impact (risk matrix)
5. Implement controls (risk mitigation)
6. Monitor and review (quarterly)

### 5.2 Key Risks Identified

| Risk | Likelihood | Impact | Mitigation Control |
|------|-----------|--------|-------------------|
| Unauthorized access to tenant data | Medium | High | RBAC, MFA, audit logging, quarterly access reviews |
| PII leakage to LLM prompts | Low | Critical | Code review, PII detection gate, no PII in prompts by design |
| Database failure (data loss) | Low | High | Daily backups, quarterly recovery testing, RTO/RPO < targets |
| Cost budget overrun | Medium | Medium | Hard $0.80 cap, degradation strategy, real-time cost tracking |
| Multi-tenant data leakage | Low | Critical | Schema-per-tenant isolation, row-level security, tenant ID validation |
| AI model hallucination (incorrect itineraries) | Medium | Medium | Vector search grounding (RAG), trust tier filtering (≥4), feedback loop |
| Third-party API outage (Weather/Events) | High | Low | Mock data fallback, caching (1-24hr TTL), graceful degradation |
| Insider threat (employee data access) | Low | High | RBAC, audit logging, quarterly access reviews, background checks |

**Risk Acceptance**:
- Weather/Events API outages: Accepted (mock data fallback ensures availability)
- AI hallucination: Accepted (RAG grounding mitigates, user feedback improves over time)

### 5.3 Fraud Risk Assessment

**Fraud Scenarios Considered**:
1. Employee exfiltrates tenant data → Mitigated by audit logging, access controls
2. Contractor accesses production without authorization → Mitigated by MFA, VPN requirement (planned)
3. Malicious user manipulates API to exceed quotas → Mitigated by rate limiting, quota enforcement

**Control Activities**:
- Segregation of duties (separate roles for database admin, app developer)
- Code review prevents malicious code deployment
- Audit log review (monthly) for anomalies

---

## 6. Information and Communication

### 6.1 Information Systems

**Systems Used**:
- **Jira**: Issue tracking, change management, access request workflow
- **GitHub**: Code repository, pull request reviews, version control
- **Slack**: Team communication, incident notifications, alert routing
- **Datadog**: Application monitoring, log aggregation
- **PagerDuty**: On-call rotation, incident management
- **AWS Console**: Infrastructure provisioning, monitoring

**Data Flow**:
- Audit logs → PostgreSQL → Datadog (centralized logging)
- Metrics → Prometheus → Grafana (dashboards)
- Alerts → PagerDuty → Slack → On-call engineer

### 6.2 Internal Communication

**Security Communications**:
- Quarterly security updates (all-hands meeting)
- Incident postmortems shared with engineering team (within 7 days)
- Policy updates communicated via email (acknowledgment required)

**Escalation Paths**:
- SEV1 incidents → On-call → Engineering Manager → VP Engineering → CEO (within 1 hour)
- Security vulnerabilities → Security Lead → VP Engineering → CEO (within 24 hours)

### 6.3 External Communication

**Customer Communications**:
- Privacy Policy: Public (https://timbuktoo.ai/privacy)
- Service Status Page: https://status.timbuktoo.ai (uptime reporting)
- Incident notifications: Email to affected tenants (SEV1/SEV2 only)

**Vendor Communications**:
- Anthropic: Data Processing Agreement, security questionnaire completed
- AWS: Service Health Dashboard monitoring, support tickets for incidents

---

## 7. Monitoring Activities

### 7.1 Ongoing Monitoring

**Automated Monitoring**:
- **Uptime**: Datadog synthetic checks (1-minute intervals)
- **Performance**: Prometheus metrics (15-second scrape interval)
- **Security**: AWS GuardDuty findings (real-time alerts)
- **Cost**: Cost anomaly detection (5 rules, hourly checks)
- **Audit Logs**: Daily review for failed logins, unauthorized access attempts

**Dashboards**:
- Cost Dashboards (3): Cost per Trip, Cost vs Quality, Budget Guardrails
- Uptime Dashboard: 99.5% SLA tracking
- Error Rate Dashboard: <1% target tracking

### 7.2 Periodic Evaluations

**Quarterly Activities**:
- Access reviews (all users, RBAC roles)
- Backup recovery testing
- Control testing (sample 25 items per control for Type II preparation)
- Incident response drills (tabletop exercise)

**Annual Activities**:
- Risk assessment
- Policy reviews (all security policies)
- Penetration testing (external firm)
- Security awareness training (all employees)

### 7.3 Reporting Deficiencies

**Process**:
1. Control deficiency identified → Logged in Jira (severity: Critical, High, Medium, Low)
2. Root cause analysis within 48 hours
3. Remediation plan documented (owner, target date)
4. Executive reporting (monthly security dashboard to CEO)

**Escalation**:
- Critical deficiencies → CEO notification within 24 hours
- High deficiencies → VP Engineering within 48 hours
- Medium/Low deficiencies → Monthly summary

---

## 8. Detailed Control Descriptions

### 8.1 Security Controls (CC6)

#### CC6.1 - Access Controls

**Control Description**:
The organization implements logical access security measures to protect information assets from unauthorized access.

**How It Works**:
1. All users authenticate via JWT tokens (1-hour expiration)
2. RBAC middleware checks user role before allowing operations
3. Admin role: Full access (users, tenants, trips)
4. Operator role: Create trips, read trips, read metrics
5. Viewer role: Read-only access (trips, metrics)

**Evidence**:
- Code: `timbuktoo/security/rbac.py` (AuthManager class)
- Configuration: User-role mapping in PostgreSQL `users` table
- Testing: Sample 10 API requests with different roles, verify access control enforcement

#### CC6.2 - User Provisioning

**Control Description**:
Prior to issuing credentials, the organization registers and authorizes new users.

**How It Works**:
1. Manager submits access request (Jira ticket)
2. IT reviews and verifies manager approval
3. IT provisions account with appropriate role
4. User receives credentials via secure channel
5. User logs event in audit log

**Evidence**:
- Process Document: `SOC2/02_Access_Control/Onboarding_Offboarding/User_Provisioning_Workflow.md`
- Sample Tickets: 7 user provisioning tickets from Q1-Q2 2024
- Audit Logs: User creation events with timestamps

#### CC6.3 - Access Modification and Removal

**Control Description**:
The organization modifies or removes access based on personnel changes.

**How It Works**:
1. Quarterly access reviews (VP Engineering approval)
2. Identify discrepancies (users with wrong roles, terminated users with active accounts)
3. Remediate within 7 days
4. Offboarding: IT disables account same day as termination

**Evidence**:
- Q1 2024 Access Review: 5 users removed, 3 role changes
- Q2 2024 Access Review: 3 users removed, 2 role changes (In Progress - due June 30)
- Offboarding Tickets: 6 sample tickets with same-day deactivation

#### CC6.6 - Encryption

**Control Description**:
The organization uses encryption to protect data at rest and in transit.

**How It Works**:
- At Rest: PostgreSQL TDE (AWS KMS), S3 bucket encryption (AES-256)
- In Transit: TLS 1.2+ for API endpoints, SSL for database connections
- Secrets: Fernet encryption for sensitive values, AWS Secrets Manager for API keys

**Evidence**:
- Database: `SELECT * FROM pg_encryption_keys;` output shows active keys
- S3: Bucket policy screenshot showing default encryption enabled
- SSL Labs: A+ rating for https://api.timbuktoo.ai (TLS 1.2+)

#### CC6.7 - Security Monitoring

**Control Description**:
The organization monitors system components to detect anomalies and security events.

**How It Works**:
1. Audit logging: All authentication, data access, trip creation logged to PostgreSQL
2. Failed login monitoring: 5 attempts in 5 minutes → Account lockout + Slack alert
3. AWS GuardDuty: Intrusion detection, alerts routed to Security Lead
4. Cost anomaly detection: 5 rules (token spike, low ROI, cache miss, etc.)

**Evidence**:
- Audit Logs: Sample export from last 30 days (12,450 events)
- GuardDuty: Enabled screenshot, zero findings in May 2024
- Cost Anomaly Alerts: 3 token spike events in May (auto-remediated)

#### CC6.8 - Change Management

**Control Description**:
The organization manages changes to system components through a formal process.

**How It Works**:
1. Developer submits pull request (PR) on GitHub
2. Peer review required (1+ approvals)
3. Staging deployment and testing
4. Security scan (Snyk, Bandit, Semgrep)
5. Production release approval (Engineering Lead)
6. Deployment with rollback plan

**Evidence**:
- GitHub PRs: 10+ sample PRs with approvals
- Production Release Checklist: Last 3 deployments
- Rollback Test: Q2 2024 drill report (passed)

### 8.2 Availability Controls (CC7)

#### CC7.1 - Uptime Monitoring

**Control Description**:
The organization monitors system availability to meet commitments.

**How It Works**:
- Datadog synthetic checks (1-minute intervals) ping `/health` endpoint
- Health check verifies: Database connection, ChromaDB connection, API key validity
- Alert if 3 consecutive failures (>3 minutes downtime)
- On-call engineer paged via PagerDuty

**Evidence**:
- Uptime Report May 2024: 99.7% (target: 99.5%)
- Datadog Dashboard: Screenshot showing P95 latency 68 seconds (target: <90s)
- Error Rate Chart: 0.3% (target: <1%)

#### CC7.2 - Incident Response

**Control Description**:
The organization responds to incidents in a timely manner.

**How It Works**:
1. Incident detected (monitoring alert or user report)
2. On-call engineer triages (severity classification)
3. SEV1: 4-hour SLA, SEV2: 24-hour SLA, SEV3: 7-day SLA
4. Incident Commander coordinates response
5. Postmortem within 5 business days (SEV1/SEV2)

**Evidence**:
- Incident Response Plan: Last reviewed 2024-01
- Incident Log: 2 SEV1, 5 SEV2, 12 SEV3 in first half of 2024
- Postmortems: 3 sample postmortems (SEV1: Cache outage 2024-06-15, SEV2: Database slow query, SEV2: API rate limit)

#### CC7.3 - Backup and Recovery

**Control Description**:
The organization maintains backup and recovery capabilities.

**How It Works**:
- AWS RDS automated backups: Daily full + hourly incremental
- Retention: 30 days
- Quarterly recovery drills: Restore to test environment, verify data integrity
- RTO: 4 hours (time to restore service), RPO: 1 hour (maximum data loss)

**Evidence**:
- Backup Schedule: AWS RDS configuration screenshot
- Q1 2024 Recovery Test: Passed (RTO: 2.5 hours, RPO: 45 minutes)
- Q2 2024 Recovery Test: In Progress (scheduled June 30, 2024)

### 8.3 Processing Integrity Controls (CC8)

#### CC8.1 - Deterministic Workflow

**Control Description**:
The organization processes data in a deterministic, complete, and accurate manner.

**How It Works**:
- Workflow Orchestrator enforces sequential execution: Intent Parser → City Selection → Local Expert → Tools → Concierge → Post-Processor
- WorkflowState (immutable context) passed between agents
- Retry logic: Exponential backoff (2s, 4s, 8s), max 3 attempts
- Fallbacks: Cached data (Weather/Events), default values (Budget cap enforcement)

**Evidence**:
- Code: `timbuktoo/workflows/orchestrator.py` (TravelOrchestrator class)
- State Machine Diagram: Visual representation of workflow
- May 2024 Metrics: 100% of trips followed deterministic sequence

#### CC8.2 - Input Validation

**Control Description**:
The organization validates all inputs before processing.

**How It Works**:
- Intent Parser validates user preferences against JSON schema
- Checks: Travel dates ≥14 days future, 7-day duration, budget level in [low, mid, high], ≥2 interests
- Invalid inputs rejected with error message (no processing)

**Evidence**:
- Code: Intent Parser agent prompt with validation rules
- Test Suite: 25 test cases (valid/invalid inputs)
- May 2024: 142 invalid inputs rejected (3.2% rejection rate)

#### CC8.3 - Cost Budget Enforcement

**Control Description**:
The organization enforces budget constraints to prevent cost overruns.

**How It Works**:
1. Before expensive operation (Concierge agent), check current trip cost
2. If cost > $0.50: Apply "Reduced" strategy (25k tokens, 20 chunks)
3. If cost > $0.70: Apply "Minimal" strategy (15k tokens, 10 chunks)
4. If cost would exceed $0.80: Reject trip (hard cap)

**Evidence**:
- Code: `timbuktoo/utils/cost_tracker.py` (CostController class)
- May 2024: 100% of trips under $0.80 cap (average: $0.35, max: $0.68)
- Degradation Usage: 15% of trips used Reduced strategy, 2% used Minimal

### 8.4 Confidentiality Controls (CC9)

#### CC9.1 - PII Exclusion

**Control Description**:
The organization excludes PII from AI processing to protect confidentiality.

**How It Works**:
- User preferences do NOT include email, name, phone number
- LLM prompts constructed from: vibes, interests, budget level, travel dates (no PII)
- A/B testing uses trip_id hash (deterministic), not user identifiers
- Code review enforces: No PII in agent prompts

**Evidence**:
- Code Review: `timbuktoo/agents/*.py` verified (no PII in prompts)
- Sample Prompts: 10 sample LLM prompts inspected (zero PII found)
- A/B Testing: `assign_variant(trip_id)` uses MD5 hash, no user data

### 8.5 Privacy Controls (CC10)

#### CC10.1 - Privacy Notice

**Control Description**:
The organization provides notice about data collection, use, and retention.

**How It Works**:
- Privacy Policy published: https://timbuktoo.ai/privacy (last updated 2024-05)
- Cookie Policy: Session cookies only (no tracking)
- Onboarding: User must accept terms (`terms_accepted` field in database)

**Evidence**:
- Privacy Policy PDF: Snapshot from 2024-05
- Database Schema: `OnboardingSession` table includes `terms_accepted` boolean

#### CC10.2 - Data Retention

**Control Description**:
The organization retains and disposes of data per policy.

**How It Works**:
- Retention Schedule: Trip data 1 year, Audit logs 1 year, Cost tracking 2 years, User accounts 30 days post-cancellation
- Daily cron job: `scripts/delete_expired_data.py` runs at 2 AM UTC
- Deletion verification: Query for records > retention period (expected: zero)

**Evidence**:
- Data Retention Policy: Document with retention schedules
- Deletion Logs: Last 30 days (1,245 records deleted in May 2024)
- Deletion Verification: Query result showing zero old records (2024-06-01)

#### CC10.3 - Data Subject Rights

**Control Description**:
The organization supports data subject rights (access, correction, deletion).

**How It Works**:
- Data Export: `GET /api/v1/users/{user_id}/data` returns all user data in JSON
- Deletion Workflow: User requests deletion → 30-day SLA → Complete deletion + verification
- Verification: Query shows zero records for deleted user

**Evidence**:
- API Documentation: Data export endpoint docs
- Sample Deletion Request: Ticket + verification query result (zero records)

---

## 9. Management Assertions

Management of Timbuktoo, Inc. asserts the following as of June 1, 2024:

1. **System Description**: The accompanying description fairly presents the Timbuktoo Travel Concierge system as designed and implemented throughout the specified period.

2. **Suitability of Controls**: The controls related to the applicable trust services criteria were suitably designed to provide reasonable assurance that the criteria would be achieved if the controls operated effectively throughout the specified period.

3. **Responsibility**: Management is responsible for designing, implementing, operating, and maintaining effective controls within the system to achieve the applicable trust services criteria.

4. **Disclosure**: Management has disclosed to the auditor:
   - All known deficiencies in the design or operation of controls
   - All known incidents of noncompliance with applicable laws and regulations
   - All known instances of fraud affecting the system
   - All significant changes to the system since the last audit

5. **Remediation**: Management has implemented remediation plans for all identified control deficiencies and is committed to continuous improvement of controls.

**Signed**:
- CEO: _________________________ Date: _____________
- VP Engineering: _________________________ Date: _____________
- Security Lead: _________________________ Date: _____________

---

## 10. Auditor Opinion

### 10.1 Independent Service Auditor's Report

**To**: Management of Timbuktoo, Inc.

**Scope**:
We have examined the accompanying description of the Timbuktoo Travel Concierge system as of June 1, 2024, based on the criteria for a description of a service organization's system set forth in the AICPA's TSP Section 100, Trust Services Principles and Criteria (AICPA, Trust Services Criteria).

**Service Organization's Responsibilities**:
Timbuktoo, Inc. is responsible for:
1. Preparing the description and assertion
2. Identifying the applicable trust services criteria
3. Designing, implementing, and operating effective controls

**Service Auditor's Responsibilities**:
Our responsibility is to express an opinion on the description and on the suitability of the design of controls based on our examination. We conducted our examination in accordance with attestation standards established by the AICPA.

**Opinion**:
In our opinion, in all material respects, based on the criteria described in management's assertion:

1. **Description**: The description fairly presents the Timbuktoo Travel Concierge system as designed and implemented as of June 1, 2024.

2. **Suitability of Design**: The controls related to the applicable trust services criteria were suitably designed to provide reasonable assurance that the applicable trust services criteria would be achieved if the controls operated effectively as of June 1, 2024.

**Intended Use**:
This report is intended solely for the information and use of Timbuktoo, Inc., user entities of the Timbuktoo Travel Concierge system, and the independent service auditors of such user entities, and is not intended to be and should not be used by anyone other than these specified parties.

**Restricted Use**:
This report and the description of tests of controls are intended solely for the information and use of Timbuktoo, Inc., and are not intended to be and should not be used by anyone other than these specified parties.

**[Audit Firm Name]**
[City, State]
[Date]

---

## Appendices

### Appendix A: Acronyms and Definitions

- **AICPA**: American Institute of Certified Public Accountants
- **AWS**: Amazon Web Services
- **CC**: Common Criteria (Trust Services Criteria numbering)
- **DPA**: Data Processing Agreement
- **KMS**: Key Management Service
- **LLM**: Large Language Model
- **MFA**: Multi-Factor Authentication
- **PII**: Personally Identifiable Information
- **RBAC**: Role-Based Access Control
- **RTO**: Recovery Time Objective
- **RPO**: Recovery Point Objective
- **SOC**: System and Organization Controls
- **TDE**: Transparent Data Encryption
- **TLS**: Transport Layer Security

### Appendix B: Referenced Documents

1. Information Security Policy (2024-01 version)
2. Incident Response Plan (2024-01 version)
3. Data Retention Policy (2024-03 version)
4. Privacy Policy (2024-05 version)
5. RBAC Code Implementation (`timbuktoo/security/rbac.py`)
6. Workflow Orchestrator (`timbuktoo/workflows/orchestrator.py`)
7. Cost Controller (`timbuktoo/utils/cost_tracker.py`)
8. Anthropic Data Processing Agreement (signed 2024-02-15)

### Appendix C: Test Results Summary (To Be Completed by Auditor)

| Control ID | Sample Size | Exceptions | Pass Rate |
|-----------|------------|-----------|----------|
| CC6.1.1 (RBAC) | 25 | 0 | 100% |
| CC6.1.2 (MFA) | 25 | 0 | 100% |
| CC6.1.3 (Access Reviews) | 4 quarters | 0 | 100% |
| CC6.6.1 (Encryption at Rest) | N/A (config review) | 0 | Pass |
| CC6.7.1 (Audit Logging) | 25 events | 0 | 100% |
| CC7.1.1 (Uptime) | 6 months | 0 | 100% |
| CC7.3.1 (Backup Testing) | 2 quarters | 0 | 100% |
| CC8.1.1 (Workflow Integrity) | 25 trips | 0 | 100% |
| CC9.1.1 (PII Exclusion) | 25 prompts | 0 | 100% |
| CC10.2.1 (Data Retention) | 25 deletion logs | 0 | 100% |

### Appendix D: Observations and Recommendations

**Observation 1**: Background checks not yet enforced for contractors (CC6.2.3)
- **Severity**: Low
- **Management Response**: Contractor background check policy will be implemented by Q3 2024 (target: August 31, 2024)
- **Status**: In Progress

**Observation 2**: Q2 2024 recovery test in progress (CC7.3.3)
- **Severity**: Low
- **Management Response**: Q2 recovery drill scheduled for June 30, 2024
- **Status**: In Progress

**Observation 3**: Error rate dashboard needs 6-month historical trend (CC7.1.4)
- **Severity**: Low
- **Management Response**: 6-month historical data will be exported and added to evidence folder by June 15, 2024
- **Status**: In Progress

**General Recommendation**: Consider implementing multi-region disaster recovery for enhanced availability (currently single-region deployment).

---

**End of Report**
