# Enterprise Customer Security Package

**Document Purpose**: Sales-ready security overview and FAQ for enterprise prospects. This package accelerates procurement by proactively addressing common security questions.

**Audience**: CISOs, Security Teams, Procurement, Legal/Compliance, Privacy Officers

**Usage**: Share during enterprise sales process, attach to RFP responses, publish on trust portal.

**Last Updated**: 2024-07-15

---

## Table of Contents

1. [Security Overview (Executive Summary)](#security-overview-executive-summary)
2. [Security FAQ](#security-faq)
3. [Compliance Summary](#compliance-summary)
4. [Customer Assurance Artifacts](#customer-assurance-artifacts)
5. [Contact Information](#contact-information)

---

## Security Overview (Executive Summary)

### About Timbuktoo

Timbuktoo is an AI-powered travel concierge that creates personalized itineraries using multi-agent orchestration. We process customer travel preferences and personally identifiable information (PII), making security and compliance our top priorities.

**Key Security Commitments**:
- ✅ **SOC-2 Type II Certified** (annual audit, zero findings)
- ✅ **ISO 27001 Certified** (Q1 2025 - 95% complete)
- ✅ **GDPR & CCPA Compliant** (privacy-first design)
- ✅ **99.9% Uptime SLA** (multi-AZ, daily backups)
- ✅ **24/7 Security Monitoring** (15-min incident SLA)

---

### Security Architecture

**Multi-Layered Defense**:

```
[Customer] → [Security Layer 1: Network] → [Security Layer 2: Application] → [Security Layer 3: Data]
```

**Layer 1: Network Security**
- **CloudFront WAF**: DDoS protection, rate limiting (100 req/min)
- **VPC Isolation**: Private subnets, security groups, NACLs
- **TLS 1.2+ Only**: All traffic encrypted in transit

**Layer 2: Application Security**
- **Authentication**: Multi-factor authentication (MFA) required for all users
- **Authorization**: Role-based access control (RBAC) with least privilege
- **Input Validation**: Parameterized queries (no SQL injection), OWASP top 10 coverage
- **API Security**: JWT tokens, rate limiting, API key rotation (90 days)

**Layer 3: Data Security**
- **Encryption at Rest**: AES-256 (AWS KMS, auto-rotate annually)
- **Encryption in Transit**: TLS 1.2+ (Let's Encrypt certs, auto-renew)
- **Multi-Tenancy**: Schema-per-tenant isolation (PostgreSQL RLS)
- **Backups**: Daily automated backups, quarterly restore tests, 30-day retention

---

### AI Safety & Hallucination Prevention

**Challenge**: AI agents may generate inaccurate or "hallucinated" recommendations (e.g., non-existent venues).

**Our Approach**:

1. **Source Attribution**: All venue recommendations cite trusted sources:
   - OpenStreetMap (OSM)
   - Wikidata
   - TripAdvisor
   - Local expert databases

2. **Trust Tier Filtering**: Sources rated 1-5 (5 = highest trust), minimum 70% tier 4-5 required

3. **Vector Database Cross-Check**: Every recommendation is verified against our knowledge base

4. **Approval Gates** (Wrk.Flo):
   - **City Ingestion Gate**: 12 automated checks (schema, attribution, trust tier)
   - **Itinerary Generation Gate**: 10 checks (hallucination detection, budget, safety)

5. **Deterministic Workflows**: Temperature = 0 (no randomness), immutable state machine

**Result**: Zero hallucinated venues in production (100% accuracy since launch)

---

### Compliance Certifications

| Certification | Status | Audit Date | Next Audit |
|---------------|--------|------------|------------|
| **SOC-2 Type II** | ✅ Certified | June 2024 | June 2025 |
| **ISO 27001** | ⏳ In Progress (95%) | Q1 2025 (planned) | Annual (after certification) |
| **GDPR** | ✅ Compliant | N/A (ongoing) | Annual review |
| **CCPA** | ✅ Compliant | N/A (ongoing) | Annual review |

**SOC-2 Type II Highlights**:
- Trust Services Criteria: Security, Availability, Confidentiality, Privacy
- Observation Period: 12 months (July 2023 - June 2024)
- Findings: **Zero exceptions**
- Auditor: [Auditor Firm Name]

**ISO 27001 Status**:
- Gap closure: 95% complete
- Controls implemented: 78/83 applicable controls
- Remaining work: 5 controls (threat intelligence, asset inventory enhancements)
- Certification audit: Q1 2025

---

### Data Protection

**Data Classification**:
- **Public**: Marketing content, public documentation
- **Internal**: Business data, analytics, non-PII
- **Confidential**: Customer PII, API keys, audit logs

**Data Retention**:
| Data Type | Retention Period | Deletion Method |
|-----------|------------------|-----------------|
| Customer PII | 7 years | Automated S3 lifecycle policy |
| Trip Preferences | 2 years after last login | Automated PostgreSQL job |
| Execution Logs | 90 days | Automated Datadog deletion |
| Audit Logs | 365 days | Immutable S3 archive |
| Backups | 30 days | Automated S3 lifecycle |

**Data Subject Rights** (GDPR/CCPA):
- ✅ **Right to Access**: Download all PII via self-service portal (30-day SLA)
- ✅ **Right to Rectification**: Update PII via account settings
- ✅ **Right to Erasure**: Delete all data via Data Subject Access Request (DSAR) form
- ✅ **Right to Portability**: JSON export via API
- ✅ **Right to Object**: Opt-out of marketing emails

---

### Incident Response

**Severity Levels**:
- **SEV1** (Critical): Service outage, data breach
- **SEV2** (High): Service degradation, security vulnerability
- **SEV3** (Medium): Minor issues, no customer impact

**Response SLAs**:
| Severity | Detection | Response | Resolution | Customer Notification |
|----------|-----------|----------|------------|----------------------|
| **SEV1** | 15 minutes | 15 minutes | 4 hours | Immediate (email + status page) |
| **SEV2** | 1 hour | 1 hour | 24 hours | Within 1 hour |
| **SEV3** | 4 hours | 4 hours | 7 days | Daily summary |

**Incident Process**:
1. **Detection**: Automated alerts (Datadog, PagerDuty)
2. **Triage**: On-call engineer assesses severity (SEV1/2/3)
3. **Response**: Incident runbook executed, escalation as needed
4. **Resolution**: Root cause identified, fix deployed
5. **Post-Mortem**: Root Cause Analysis (RCA) for SEV1/SEV2 (100% completion rate)

**Recent Incidents** (last 12 months):
- **SEV1**: 1 (15-min API outage, resolved in 12 min)
- **SEV2**: 2 (avg resolution: 45 min)
- **SEV3**: 1 (non-customer-impacting)

---

### Vendor Security

**Third-Party Risk Management**:
- ✅ Annual vendor risk assessments
- ✅ SOC-2 attestation requirement for critical vendors
- ✅ NDA requirement for all vendors
- ✅ Data Processing Agreements (DPAs) for GDPR compliance

**Critical Vendors** (all SOC-2 certified):
| Vendor | Service | Data Processed | SOC-2 Certified |
|--------|---------|----------------|-----------------|
| **Anthropic** | AI agents (Claude API) | Trip preferences (no PII) | ✅ Yes |
| **AWS** | Infrastructure (RDS, S3, KMS) | All data | ✅ Yes |
| **Datadog** | Monitoring, logs | Execution logs (PII masked) | ✅ Yes |
| **Stripe** | Payment processing | Payment info (not stored by Timbuktoo) | ✅ Yes |

---

### Security Testing

**Vulnerability Management**:
- **Weekly Vulnerability Scans**: Snyk (SAST + dependency scanning)
- **Patching SLA**: 30 days for high/critical vulnerabilities
- **Annual Penetration Testing**: Third-party security firm
  - Last Test: May 2024
  - Critical Findings: 0
  - High Findings: 0
  - Medium Findings: 2 (both remediated)

**Secure Development Lifecycle (SDLC)**:
1. **Design**: Security requirements defined
2. **Development**: Bandit (Python linting), Semgrep (SAST)
3. **Review**: Peer review (2 approvers), GitHub branch protection
4. **Testing**: Automated tests (≥80% coverage), Snyk scans
5. **Deployment**: Wrk.Flo approval gates (3 gates: city ingestion, itinerary, production)
6. **Monitoring**: Datadog APM, PagerDuty alerts

---

## Security FAQ

### General Security

**Q1: How do you protect customer data?**

**A**: We use a multi-layered approach:
- **Encryption**: AES-256 (at rest), TLS 1.2+ (in transit)
- **Access Control**: RBAC + MFA, quarterly access reviews
- **Monitoring**: 24/7 security monitoring, 15-min incident SLA
- **Backups**: Daily automated backups, quarterly restore tests
- **Compliance**: SOC-2 Type II certified, ISO 27001 (Q1 2025)

**Q2: Where is our data stored?**

**A**: All customer data is stored in AWS us-east-1 (Virginia, USA). Backups are replicated to AWS us-west-2 (Oregon, USA) for disaster recovery. We use AWS's SOC-2/ISO 27001 certified infrastructure.

**Q3: Do you support data residency requirements (e.g., EU data in EU)?**

**A**: Currently, all data is stored in AWS us-east-1 (USA). For EU customers with data residency requirements, we can discuss custom deployments in AWS eu-central-1 (Frankfurt) or eu-west-1 (Ireland). This requires an enterprise contract. Please contact sales@timbuktoo.ai.

**Q4: How do you handle multi-tenancy? Can other customers access our data?**

**A**: We use schema-per-tenant isolation:
- Each customer has a dedicated PostgreSQL schema (e.g., `tenant_acme`)
- Row-Level Security (RLS) enforces tenant filtering at the database level
- ChromaDB uses namespaces (`tenant_{id}_vectors`)
- 100 automated tests verify zero cross-tenant data leakage
- Annual penetration tests verify isolation

**Result**: Other customers cannot access your data, even if application code has a bug.

---

### Access Control

**Q5: Who can access our data?**

**A**: Access is restricted to:
- **Your Users**: Via authenticated login (MFA required)
- **Timbuktoo Engineers**: Only Admin role (2 users), audit logged, least privilege
- **Support Team**: Read-only access for troubleshooting (requires ticket, audit logged)

Access is reviewed quarterly. No third parties have access without your explicit consent.

**Q6: Do you require multi-factor authentication (MFA)?**

**A**: Yes. MFA is **mandatory** for all Timbuktoo employees (100% adoption via AWS IAM). For customer users, MFA is:
- **Recommended** for standard accounts
- **Required** for enterprise accounts (configurable)

**Q7: How do you manage privileged access?**

**A**: Privileged access (Admin role) is limited to 2 users:
- CISO
- Platform Owner

All privileged actions are:
- ✅ Logged (CloudTrail + Datadog)
- ✅ Reviewed quarterly (access review tickets)
- ✅ Require MFA (no exceptions)
- ✅ Time-limited (sessions expire after 12 hours)

---

### Encryption & Data Protection

**Q8: What encryption standards do you use?**

**A**:
- **At Rest**: AES-256 (AWS KMS, auto-rotate annually)
- **In Transit**: TLS 1.2+ (Let's Encrypt certs, auto-renew)
- **Backups**: AES-256 (separate KMS key)
- **Secrets**: AES-256 (AWS Secrets Manager, 90-day rotation)
- **Laptops**: Full-disk encryption (FileVault/BitLocker)

**Q9: How are encryption keys managed?**

**A**:
- **Storage**: AWS KMS (FIPS 140-2 Level 2 validated)
- **Rotation**: Automatic annual rotation
- **Access**: Least privilege (only Admin role + RDS service)
- **Audit**: All key usage logged (CloudTrail)

Timbuktoo does **not** have access to plaintext encryption keys (AWS manages key material).

**Q10: Can you provide encryption at rest for backups?**

**A**: Yes. All backups (PostgreSQL snapshots, S3 archives) are encrypted using AES-256 with a dedicated KMS key. Backups are immutable (versioned, cannot be deleted by application code) to prevent ransomware attacks.

---

### Compliance & Audits

**Q11: Are you SOC-2 certified?**

**A**: Yes. Timbuktoo is **SOC-2 Type II certified** (June 2024). Our report covers:
- **Trust Services Criteria**: Security, Availability, Confidentiality, Privacy
- **Observation Period**: 12 months (July 2023 - June 2024)
- **Findings**: Zero exceptions
- **Next Audit**: June 2025

SOC-2 reports are available under NDA. Request via security@timbuktoo.ai.

**Q12: Are you ISO 27001 certified?**

**A**: **In Progress** (95% complete, certification Q1 2025). We are reusing 70% of SOC-2 evidence for ISO 27001, reducing incremental effort. Certification audit scheduled for January 2025.

**Q13: Are you GDPR compliant?**

**A**: Yes. Timbuktoo is GDPR-ready:
- ✅ Privacy policy published (https://timbuktoo.ai/privacy)
- ✅ Data Protection Officer (DPO) designated (dpo@timbuktoo.ai)
- ✅ Data Processing Agreements (DPAs) available
- ✅ Data Subject Rights supported (DSAR workflow, 30-day SLA)
- ✅ Breach notification procedures (72-hour GDPR Article 33)

**Q14: Are you HIPAA compliant?**

**A**: **Not currently**. Timbuktoo does not process Protected Health Information (PHI). If you require HIPAA compliance (e.g., medical tourism use case), please contact us. We can achieve HIPAA compliance in 6-8 weeks (90% overlap with existing SOC-2 controls).

**Q15: Are you FedRAMP authorized?**

**A**: **No**. FedRAMP is not currently applicable (no federal contracts). FedRAMP requires 24-month timeline and $2M+ investment. We can pursue FedRAMP if you have a federal contract opportunity.

---

### Incident Response & Business Continuity

**Q16: What is your incident response process?**

**A**:
1. **Detection**: Automated alerts (Datadog, PagerDuty) - 15-min SLA
2. **Triage**: On-call engineer (SEV1/SEV2/SEV3 classification)
3. **Response**: Incident runbooks executed, escalation path defined
4. **Customer Notification**: SEV1 immediate, SEV2 within 1 hour
5. **Resolution**: Root cause fix, deployment
6. **Post-Mortem**: Root Cause Analysis (RCA) for SEV1/SEV2 (100% completion)

All SEV1/SEV2 incidents are shared with affected customers (RCA reports available upon request).

**Q17: What is your disaster recovery (DR) plan?**

**A**:
- **RTO** (Recovery Time Objective): 4 hours
- **RPO** (Recovery Point Objective): 24 hours (daily backups)
- **DR Strategy**: Multi-AZ RDS (automatic failover), cross-region S3 replication
- **Testing**: Quarterly backup restore tests (100% success rate)

DR plan document available under NDA.

**Q18: What is your uptime SLA?**

**A**: **99.9% monthly uptime** (excludes scheduled maintenance).

**Current Performance**:
- Last 30 days: 99.95%
- Last 90 days: 99.93%
- Last 365 days: 99.91%

SLA credits apply if uptime < 99.9% (per contract terms).

**Q19: How do you handle scheduled maintenance?**

**A**:
- **Maintenance Windows**: Tuesdays/Thursdays 10:00-16:00 UTC (low-traffic periods)
- **Customer Notification**: 7 days advance notice (email + status page)
- **Zero-Downtime Deployments**: Multi-AZ failover (no customer impact)

Last 6 months: 2 maintenance windows, 0 downtime.

---

### AI Safety

**Q20: How do you prevent AI hallucinations?**

**A**: We use a multi-layered approach:
1. **Source Attribution**: All venues cite trusted sources (OSM, Wikidata, TripAdvisor)
2. **Trust Tier Filtering**: Minimum 70% tier 4-5 sources
3. **Vector DB Cross-Check**: Verify all recommendations against knowledge base
4. **Wrk.Flo Gates**: 12 automated checks (city ingestion), 10 checks (itinerary generation)
5. **Deterministic Workflows**: Temperature = 0 (no randomness)

**Result**: Zero hallucinated venues in production (100% accuracy since launch).

**Q21: Can we review AI agent outputs before delivery?**

**A**: Yes. Enterprise customers can enable **human-in-the-loop review**:
- 5% sample rate for high-cost trips (> $0.60 cost)
- Manual review by Concierge Lead
- Approval gate before itinerary delivery

Contact sales@timbuktoo.ai to enable.

**Q22: How do you handle bias in AI recommendations?**

**A**: We monitor for bias using:
- **Diversity metrics**: Ensure recommendations span multiple neighborhoods, price tiers
- **Variant testing**: A/B test "Control" vs "Slow Hidden Gems" (ensures variety)
- **Feedback loops**: Customer ratings (1-5 stars) detect low-quality recommendations

Bias incidents are reviewed in quarterly product reviews.

---

### Data Privacy

**Q23: Do you sell customer data?**

**A**: **No**. Timbuktoo does **not** sell, rent, or share customer data with third parties for marketing purposes. Customer data is used solely for:
- Service delivery (itinerary generation)
- Product improvement (aggregate analytics, no PII)
- Legal compliance (audit logs)

See our privacy policy: https://timbuktoo.ai/privacy

**Q24: How do customers delete their data?**

**A**: Customers can delete their data via:
1. **Self-Service**: Account settings → "Delete Account" (immediate deletion)
2. **Data Subject Access Request (DSAR)**: Email dpo@timbuktoo.ai (30-day SLA)

Deletion process:
- Immediate: PostgreSQL data deleted (`users`, `trips`, `feedback` tables)
- 30 days: S3 backups purged (immutable retention period)
- 30 days: Third-party logs deleted (Datadog, Anthropic)

**Q25: Do you use customer data to train AI models?**

**A**: **No**. Timbuktoo does **not** train AI models on customer data. We use Anthropic's Claude API (pre-trained models). Anthropic does **not** use customer data for model training (per Anthropic's DPA).

Customer data is used only for:
- Itinerary generation (real-time inference)
- Vector database search (semantic similarity)

---

### Vendor & Supply Chain Security

**Q26: How do you assess third-party vendors?**

**A**: All vendors undergo annual risk assessments:
- ✅ SOC-2 attestation requirement (for critical vendors)
- ✅ NDA requirement (all vendors)
- ✅ Data Processing Agreements (DPAs) for GDPR
- ✅ Security questionnaire (access controls, encryption, incident response)
- ✅ Contract review (security clauses, liability, breach notification)

Vendor list available upon request.

**Q27: What happens if a vendor has a security breach?**

**A**:
1. **Notification**: Vendor must notify Timbuktoo within 24 hours (per contract)
2. **Assessment**: Security Lead assesses impact (customer data exposure?)
3. **Customer Notification**: If customer data affected, notify within 72 hours (GDPR Article 33)
4. **Remediation**: Work with vendor on corrective actions
5. **Review**: Quarterly vendor review includes breach history

Vendor breach insurance: $1M coverage (planned Q4 2024).

---

### Security Testing & Audits

**Q28: Do you perform penetration testing?**

**A**: Yes. **Annual penetration testing** by third-party security firm:
- **Last Test**: May 2024
- **Scope**: API, web app, infrastructure
- **Critical Findings**: 0
- **High Findings**: 0
- **Medium Findings**: 2 (both remediated)
- **Low Findings**: 5 (3 remediated, 2 accepted risk)

Pentest summary available under NDA. Request via security@timbuktoo.ai.

**Q29: Can we conduct our own security assessment?**

**A**: Yes. Enterprise customers can conduct security assessments:
- **Questionnaires**: Respond within 5 business days
- **Third-Party Audits**: Coordinate with our Security Lead
- **Penetration Testing**: Requires 30-day advance notice, rules of engagement (no production disruption)

Contact security@timbuktoo.ai to schedule.

**Q30: How do you handle vulnerability disclosures?**

**A**: We welcome responsible disclosures via security@timbuktoo.ai:
- **Response SLA**: 24 hours (acknowledgment)
- **Remediation SLA**: 90 days (critical findings)
- **Safe Harbor**: No legal action against responsible disclosures
- **Bug Bounty**: $100-$2,000 rewards (based on severity)

See responsible disclosure policy: https://trust.timbuktoo.ai/contact

---

## Compliance Summary

### Certifications & Standards

| Framework | Status | Audit Date | Scope | Evidence |
|-----------|--------|------------|-------|----------|
| **SOC-2 Type II** | ✅ Certified | June 2024 | Security, Availability, Confidentiality, Privacy | Download report (NDA-gated) |
| **ISO 27001** | ⏳ 95% Complete | Q1 2025 (planned) | 83 applicable controls (78 implemented) | ISO roadmap available |
| **GDPR** | ✅ Compliant | N/A (ongoing) | Privacy policy, DSAR workflow, DPO, DPAs | Privacy policy (public) |
| **CCPA** | ✅ Compliant | N/A (ongoing) | California-specific deletion, privacy notice | Privacy policy (public) |
| **HIPAA** | ❌ Not Applicable | N/A | No PHI processed | Available if needed (6-8 weeks) |
| **FedRAMP** | ❌ Not Applicable | N/A | No federal contracts | Available if $5M+ contract |

---

### Security Controls

**Implemented Controls** (from ISO 27001 / SOC-2):

| Control Category | Examples | Compliance Standard |
|------------------|----------|---------------------|
| **Access Control** | RBAC, MFA, quarterly access reviews, least privilege | ISO A.9, SOC-2 CC6.1-CC6.3 |
| **Cryptography** | AES-256 (at rest), TLS 1.2+ (in transit), KMS key management | ISO A.10, SOC-2 CC6.7 |
| **Operations Security** | Daily backups, quarterly restore tests, change management | ISO A.12, SOC-2 CC7.2, CC8.1 |
| **Incident Management** | IRP, 15-min SLA, RCA (100% completion), PagerDuty | ISO A.16, SOC-2 CC7.3-CC7.4 |
| **Vulnerability Management** | Weekly Snyk scans, 30-day patching SLA, annual pentests | ISO A.12.6, SOC-2 CC6.6 |
| **Vendor Risk** | Annual vendor assessments, SOC-2 requirement, NDAs, DPAs | ISO A.15, SOC-2 CC9.2 |
| **Logging & Monitoring** | Centralized Datadog logging, 90-day retention, audit trails | ISO A.12.4, SOC-2 CC7.2 |
| **Business Continuity** | Multi-AZ RDS, DR plan (RTO 4h, RPO 24h), quarterly tests | ISO A.17, SOC-2 CC7.2 |

**Total**: 78 implemented controls (from 83 applicable ISO 27001 controls)

---

### Privacy & Data Protection

**GDPR Compliance**:
- ✅ Legal Basis: Legitimate interest (service delivery) + consent (marketing)
- ✅ Privacy Notice: https://timbuktoo.ai/privacy
- ✅ Data Protection Officer (DPO): dpo@timbuktoo.ai
- ✅ Data Processing Agreements (DPAs): Available for all customers
- ✅ Data Subject Rights:
  - Right to Access (30-day SLA)
  - Right to Rectification (self-service)
  - Right to Erasure (30-day SLA)
  - Right to Portability (JSON export)
  - Right to Object (opt-out)
- ✅ Breach Notification: 72-hour GDPR Article 33 compliance
- ✅ Data Minimization: Only collect email, name, trip preferences (no unnecessary PII)
- ✅ Cross-Border Transfers: AWS us-east-1 (US), standard contractual clauses (SCCs) for EU

**CCPA Compliance**:
- ✅ Privacy Notice (California-specific)
- ✅ Do Not Sell My Personal Information (we do not sell data)
- ✅ Data Deletion (30-day SLA)
- ✅ Opt-Out of Sale (N/A - we do not sell data)

---

## Customer Assurance Artifacts

### Available Documents (Under NDA)

The following documents are available to enterprise prospects and customers under Non-Disclosure Agreement (NDA):

1. **SOC-2 Type II Report** (87 pages)
   - Trust Services Criteria: Security, Availability, Confidentiality, Privacy
   - Observation Period: July 2023 - June 2024
   - Findings: Zero exceptions
   - Request: security@timbuktoo.ai

2. **SOC-2 Audit Letter** (2 pages, public)
   - Summary letter confirming SOC-2 certification
   - Safe for RFP attachments (no detailed findings)
   - Download: https://trust.timbuktoo.ai/reports

3. **Security Whitepaper** (20 pages, public)
   - "Timbuktoo Security Architecture: Multi-Tenancy, AI Safety, and Compliance"
   - Technical deep-dive (CISOs, security engineers)
   - Download: https://trust.timbuktoo.ai/reports

4. **ISO 27001 Roadmap** (5 pages)
   - Gap closure status (95% complete)
   - Certification timeline (Q1 2025)
   - Control mapping (SOC-2 → ISO)
   - Request: security@timbuktoo.ai

5. **Penetration Test Summary** (8 pages, sanitized)
   - Annual pentest (May 2024)
   - Findings: 0 critical, 0 high, 2 medium (remediated)
   - Request: security@timbuktoo.ai

6. **Data Processing Agreement (DPA)** (12 pages)
   - GDPR-compliant DPA for EU customers
   - Standard contractual clauses (SCCs)
   - Request: legal@timbuktoo.ai

7. **Business Associate Agreement (BAA)** (10 pages, if HIPAA needed)
   - HIPAA-compliant BAA for healthcare customers
   - Available upon request (HIPAA implementation 6-8 weeks)
   - Request: legal@timbuktoo.ai

8. **Incident Response Plan** (12 pages)
   - SEV1/SEV2/SEV3 procedures
   - Escalation paths, communication templates
   - Request: security@timbuktoo.ai

9. **Disaster Recovery Plan** (10 pages)
   - RTO/RPO metrics (4 hours / 24 hours)
   - Quarterly testing results
   - Request: security@timbuktoo.ai

10. **Vendor Risk Assessment Template** (5 pages)
    - Questionnaire used for all vendors
    - SOC-2 requirement, security controls
    - Request: security@timbuktoo.ai

---

### NDA Process

**To Access NDA-Gated Documents**:

1. **Request NDA**: Email security@timbuktoo.ai with:
   - Company name
   - Your name and title
   - Which documents you need
   - Use case (RFP, security review, procurement)

2. **NDA Signature**: Legal team sends NDA via DocuSign (1-2 business days)

3. **Access Granted**: Upon NDA signature, you receive:
   - Unique login link (valid 90 days)
   - Access to all requested documents
   - Download permissions

4. **Support**: Questions? Email security@timbuktoo.ai (24-hour response SLA)

---

### Security Questionnaire Support

**Enterprise Procurement Support**:

We know enterprise procurement involves detailed security questionnaires. We're here to help:

**Option 1: Self-Service Trust Portal**
- Visit https://trust.timbuktoo.ai
- 70% of common questions answered (RBAC, encryption, backups, incident response)
- Download SOC-2 report, security whitepaper, policies

**Option 2: Direct Questionnaire Completion**
- Send questionnaire to security@timbuktoo.ai
- **Response SLA**: 5 business days (standard questionnaires)
- **Rush SLA**: 2 business days (with escalation, $500 rush fee waived for enterprise contracts > $100K)

**Option 3: Live Security Review Call**
- Schedule 30-min call with CISO or Security Lead
- Walk through architecture, controls, compliance
- Q&A session (technical questions welcome)
- Request: security@timbuktoo.ai

**Common Questionnaires We've Completed**:
- ✅ SIG (Standard Information Gathering) Questionnaire
- ✅ CAIQ (Consensus Assessments Initiative Questionnaire)
- ✅ VSA (Vendor Security Alliance) Questionnaire
- ✅ Custom CISOs questionnaires (Fortune 500)

Average completion time: 3 business days.

---

## Contact Information

### Security & Compliance Contacts

**General Security Inquiries**:
- Email: security@timbuktoo.ai
- Response SLA: 24 hours (business days)

**Compliance & Audits**:
- Email: compliance@timbuktoo.ai
- Response SLA: 24 hours (business days)

**Privacy & Data Protection**:
- Email: dpo@timbuktoo.ai (Data Protection Officer)
- Response SLA: 48 hours (business days)

**Vulnerability Disclosures**:
- Email: security@timbuktoo.ai
- Response SLA: 24 hours (acknowledgment)
- Responsible Disclosure Policy: https://trust.timbuktoo.ai/contact

**Enterprise Sales (Security Questions)**:
- Email: sales@timbuktoo.ai
- Phone: +1-555-TIMBUKTOO
- Response SLA: 12 hours (business days)

**Incident Escalation (Customers Only)**:
- Email: incidents@timbuktoo.ai
- Phone (SEV1 only): +1-555-TIMBUKTOO (toll-free)
- Response SLA: 15 minutes (24/7)

---

### Trust Portal

**Self-Service Security Information**:
- URL: https://trust.timbuktoo.ai
- Pages:
  - Overview (compliance badges, audit status)
  - Security (architecture, AI safety, multi-tenancy)
  - Compliance (SOC-2, ISO 27001, GDPR)
  - Reliability (uptime metrics, incident history)
  - Privacy (DSAR, data retention, GDPR)
  - Reports (SOC-2 download, policies, pentest summaries)
  - Contact (security email, responsible disclosure)

**Access Tiers**:
- **Public**: Overview, security architecture, FAQ (no login required)
- **NDA-Gated**: SOC-2 reports, policies, pentest summaries (NDA required)
- **Customer-Only**: Incident RCAs, dedicated status page (active contract required)

---

## Appendix: Quick Reference

### Security Checklist

Use this checklist to evaluate Timbuktoo's security posture:

- [ ] **SOC-2 Certified?** ✅ Yes (Type II, June 2024, zero findings)
- [ ] **ISO 27001 Certified?** ⏳ Q1 2025 (95% complete)
- [ ] **Encryption at Rest?** ✅ Yes (AES-256, AWS KMS)
- [ ] **Encryption in Transit?** ✅ Yes (TLS 1.2+)
- [ ] **MFA Required?** ✅ Yes (100% enforcement for employees, configurable for customers)
- [ ] **Multi-Tenancy Isolation?** ✅ Yes (schema-per-tenant, RLS, 100 tests)
- [ ] **Backups?** ✅ Yes (daily automated, quarterly restore tests)
- [ ] **Disaster Recovery Plan?** ✅ Yes (RTO 4h, RPO 24h, multi-AZ)
- [ ] **Incident Response Plan?** ✅ Yes (15-min SLA, RCA 100%)
- [ ] **Penetration Testing?** ✅ Yes (annual, May 2024, 0 critical/high findings)
- [ ] **Vulnerability Scanning?** ✅ Yes (weekly Snyk, 30-day patching SLA)
- [ ] **GDPR Compliant?** ✅ Yes (DPA, DSAR, DPO, 72-hour breach notification)
- [ ] **Vendor Risk Management?** ✅ Yes (annual assessments, SOC-2 requirement)
- [ ] **99.9% Uptime SLA?** ✅ Yes (current: 99.95%)
- [ ] **AI Hallucination Prevention?** ✅ Yes (source attribution, vector DB cross-check, 0 hallucinations)

**Verdict**: ✅ **Enterprise-Ready** (15/15 security requirements met)

---

**Document Version**: 1.0
**Owner**: CISO + VP Sales
**Approval Date**: 2024-07-15
**Next Review**: 2025-01-15 (semi-annual)

**Usage Rights**: This document may be shared with enterprise prospects under NDA. For public distribution, use the Trust Portal (https://trust.timbuktoo.ai) instead.
