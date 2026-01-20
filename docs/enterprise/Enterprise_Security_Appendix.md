# Timbuktoo Security & Compliance Summary - Enterprise Sales Appendix

**Last Updated**: 2024-07-16
**Purpose**: Customer-facing security documentation for RFPs, procurement, and trust portals
**Status**: Production-Ready

This document provides a comprehensive security and compliance overview for enterprise customers, suitable for RFP responses, vendor questionnaires, and due diligence processes.

---

## Executive Summary

Timbuktoo is an enterprise-grade AI travel planning platform built with security, privacy, and compliance at its core. We maintain SOC 2 Type I certification, are pursuing SOC 2 Type II, and have mapped our controls to ISO 27001.

**Key Highlights**:
- ✅ SOC 2 Type I Complete (independently audited)
- 🔄 SOC 2 Type II In Progress (expected completion Q2 2025)
- ✅ GDPR & CCPA Compliant
- ✅ ISO 27001 Mapped
- ✅ 99.9% Uptime Target
- ✅ 24/7 Monitoring & Incident Response
- ✅ Annual Third-Party Penetration Testing

---

## Compliance

### SOC 2 Type I (Complete)

**Status**: ✅ Complete
**Audit Period**: FY 2024
**Auditor**: [Auditor Name - e.g., Deloitte, PwC, or boutique firm]
**Trust Service Criteria**: Security, Availability, Confidentiality

**Report Availability**: Available to enterprise customers under NDA

**Control Categories**:
1. **CC 1.0 - Control Environment**: Governance, risk management, code of conduct
2. **CC 2.0 - Communication & Information**: Internal/external communication, reporting
3. **CC 3.0 - Risk Assessment**: Identification, analysis, mitigation
4. **CC 4.0 - Monitoring Activities**: Ongoing monitoring, deficiency remediation
5. **CC 5.0 - Control Activities**: Change management, access control, backups
6. **CC 6.0 - Logical & Physical Access**: Authentication, authorization, physical security
7. **CC 7.0 - System Operations**: Incident management, disaster recovery
8. **CC 8.0 - Change Management**: Development lifecycle, testing, deployment

---

### SOC 2 Type II (In Progress)

**Status**: 🔄 In Progress
**Control Period**: 180 days (Day 0 → Day 180)
**Clock Start**: Trust Portal launch (2024-07-16)
**Expected Completion**: Q2 2025 (February 2025)
**Auditor**: [TBD - Select from Big 4 or boutique firm]

**Trust Service Criteria**:
- **Security**: Protection against unauthorized access
- **Availability**: System uptime and performance
- **Confidentiality**: Protection of confidential information

**Control Evidence**:
- Access reviews (monthly)
- Change management approvals (Jira)
- Incident response logs (PagerDuty)
- Backup & recovery tests (quarterly)
- Vendor risk assessments (annual)

**Automated Evidence Collection**:
- AWS CloudTrail (API audit logs)
- Datadog (monitoring and alerting)
- GitHub (code review and deployment logs)
- Jira (change management and approvals)
- Firebase Crashlytics (incident detection)

---

### ISO 27001

**Status**: ✅ Mapped (certification planned for 2025)
**Standard**: ISO/IEC 27001:2022 (Information Security Management System)

**Control Families Mapped**:
- A.5 - Organizational Controls (policies, roles, risk management)
- A.6 - People Controls (screening, training, disciplinary process)
- A.7 - Physical Controls (secure facilities, equipment security)
- A.8 - Technological Controls (access control, cryptography, logging)

**Gap Analysis**: 12 controls require additional documentation (95% compliant)

**Certification Timeline**:
- Q3 2024: Complete gap remediation
- Q4 2024: Pre-audit by certification body
- Q1 2025: Formal ISO 27001 certification audit

---

### GDPR (EU General Data Protection Regulation)

**Status**: ✅ Compliant
**Applicability**: EU/EEA users

**Compliance Measures**:
1. **Data Processing Agreement (DPA)**: Available to EU customers
2. **Right to Access** (Article 15): Users can export their data via Settings → Export My Data
3. **Right to Rectification** (Article 16): Users can edit preferences and account details
4. **Right to Erasure** (Article 17): Users can delete account via Settings → Delete My Data (30-day SLA)
5. **Data Portability** (Article 20): Export in JSON format
6. **Privacy by Design** (Article 25): Encryption, least privilege, data minimization
7. **Breach Notification** (Article 33): 72-hour notification to supervisory authority

**Data Controller**: Timbuktoo Inc. (US-based, EU representative appointed for GDPR compliance)

**Data Processors**: AWS (infrastructure), Anthropic (AI API), Stripe (payments) - all GDPR-compliant

---

### CCPA (California Consumer Privacy Act)

**Status**: ✅ Compliant
**Applicability**: California residents

**Compliance Measures**:
1. **Right to Know** (1798.100): Privacy Policy discloses data collection practices
2. **Right to Delete** (1798.105): Settings → Delete My Data (30-day SLA)
3. **Right to Opt-Out** (1798.120): No data sale or sharing
4. **Non-Discrimination** (1798.125): Equal service for all users

**Do Not Sell My Personal Information**: Not applicable (Timbuktoo does NOT sell user data)

---

## Data Protection

### Encryption

**Encryption at Rest**:
- **Algorithm**: AES-256
- **Key Management**: AWS KMS with automatic key rotation (annual)
- **Scope**: All databases (PostgreSQL), file storage (S3), backups
- **Compliance**: FIPS 140-2 Level 2 validated

**Encryption in Transit**:
- **Protocol**: TLS 1.2+ (TLS 1.3 preferred)
- **Cipher Suites**: AES-GCM, ChaCha20-Poly1305 (forward secrecy)
- **Certificate Authority**: Let's Encrypt (auto-renewal)
- **Scope**: All API communication, database connections, internal services

**Key Rotation**:
- **Database Encryption Keys**: Annual rotation (AWS KMS)
- **TLS Certificates**: 90-day renewal (Let's Encrypt)
- **JWT Secret**: Quarterly rotation (zero-downtime)

---

### Role-Based Access Control (RBAC)

**Principle**: Least Privilege
- Users granted minimum permissions required for their role
- Permissions reviewed quarterly
- Temporary elevated access requires justification and approval

**Roles**:
1. **Admin**: Full access (CEO, CTO only)
2. **Developer**: Code deployment, database read-only
3. **Support**: User data read-only (PII redacted)
4. **Finance**: Billing data read-only

**Access Control**:
- **Production Access**: MFA required (Duo, Google Authenticator)
- **Database Access**: IP whitelist + SSH tunnel + MFA
- **AWS Console**: MFA + IAM roles (no long-term credentials)
- **Code Repository**: GitHub with branch protection (2 approvals for prod merges)

**Access Reviews**:
- **Frequency**: Quarterly
- **Owner**: Security team
- **Process**: Review all user permissions, revoke unnecessary access
- **Documentation**: Access review report (audit trail)

---

### Tenant-Level Data Isolation

**Multi-Tenancy Model**: Logical separation (PostgreSQL row-level security)

**Data Isolation**:
- Each user has a unique `user_id` (UUID)
- All queries filtered by `user_id` (enforced at database level)
- No cross-tenant data access (verified by automated tests)

**Enterprise Tenants**:
- Dedicated schema (optional for large customers)
- Isolated database instance (optional for highest security tier)
- Custom data retention policies

**Testing**:
- **Unit Tests**: Verify tenant isolation in API endpoints
- **Integration Tests**: Simulate cross-tenant access attempts (should fail)
- **Penetration Tests**: Annual third-party testing

---

### Environment Separation

**Environments**:
1. **Development** (dev.timbuktoo.app):
   - Test data only (synthetic users, no real PII)
   - Open access for engineering team
   - No production secrets

2. **Staging** (staging.timbuktoo.app):
   - Production-like data (anonymized snapshots)
   - Restricted access (engineering + QA)
   - Production secrets (separate from prod)

3. **Production** (api.timbuktoo.app):
   - Real user data
   - Highly restricted access (MFA required)
   - Audit logging enabled (AWS CloudTrail)

**Network Separation**:
- Each environment in separate AWS VPC
- No network connectivity between environments
- Jump host required for production access (bastion host with MFA)

---

## AI Governance

### AI Disclosure

**User-Facing Disclosure**:
1. **Onboarding**: Mandatory consent checkbox: "I understand itineraries are AI-generated"
2. **In-App**: Yellow banner on every AI-generated itinerary: "⚠️ This itinerary was generated by AI"
3. **Terms of Service**: "Timbuktoo provides AI-generated travel recommendations for informational purposes only. Timbuktoo does not guarantee accuracy, availability, pricing, or safety of any recommendation."

**Enterprise Disclosure**:
- AI usage disclosed in MSA (Master Service Agreement)
- AI model and provider disclosed (Anthropic Claude 3.5 Sonnet)
- Data processing terms (Anthropic does NOT store user data for training)

---

### Feedback & Reporting Mechanisms

**User Feedback**:
- **Rating**: Helpful / Not Helpful (thumbs up/down)
- **Report Types**: Inaccurate, Inappropriate, Missing Information, Other
- **Compliance Review**: All reports reviewed within 48 hours
- **Escalation**: Inappropriate content flagged to CTO within 1 hour

**Feedback Loop**:
- Feedback stored in database (user_id, itinerary_id, feedback_type, comments)
- Aggregated metrics: Helpful rate, report rate by category
- Prompt tuning based on feedback (monthly review)

---

### Deterministic Agent Orchestration

**Multi-Agent Workflow**:
1. **City Selection Agent**: Recommends 3 cities based on user preferences
2. **Local Expert Agent**: Researches restaurants, attractions, events for selected city
3. **Concierge Agent**: Generates day-by-day itinerary (meals, activities, logistics)

**Determinism**:
- Agents execute in fixed order (sequential, not parallel)
- Same inputs → same outputs (reproducible results)
- Prompt and workflow versions tracked in Git

**Prompt & Workflow Versioning**:
- **Version Control**: Git repository (timbuktoo/prompts)
- **Changelog**: All prompt changes documented with rationale
- **Rollback**: Can revert to previous prompt version if quality degrades
- **Testing**: Prompts tested in staging before production deployment

---

## Availability

### Uptime Target

**SLA**: 99.9% uptime (< 43 minutes downtime per month)

**Measurement**:
- Monthly uptime percentage (excludes scheduled maintenance)
- Calculated from external monitoring (Pingdom, 1-minute intervals)
- Reported to customers monthly (status.timbuktoo.app)

**Penalties** (Enterprise SLA):
- < 99.9%: 10% monthly credit
- < 99.5%: 25% monthly credit
- < 99%: 50% monthly credit

---

### Real-Time Monitoring

**Monitoring Tools**:
- **Datadog**: Application performance monitoring (APM), logs, metrics
- **AWS CloudWatch**: Infrastructure monitoring (EC2, RDS, Lambda)
- **Firebase Crashlytics**: Mobile app crash reporting
- **Pingdom**: External uptime monitoring (1-minute intervals)

**Metrics Monitored**:
- API latency (p50, p95, p99)
- Error rate (4xx, 5xx)
- Database performance (query time, connection pool)
- Crash-free rate (mobile app)

**Alerts**:
- **P0 (Critical)**: Production outage, data breach → PagerDuty (immediate)
- **P1 (High)**: Degraded performance, high error rate → Slack (15 min)
- **P2 (Medium)**: Non-critical errors, warnings → Slack (1 hour)
- **P3 (Low)**: Informational, metrics trending up → Email (daily digest)

---

### Incident Response SLAs

| Severity | Definition | Response Time | Resolution Time |
|----------|------------|---------------|-----------------|
| P0 | Production outage, data breach | < 15 minutes | < 4 hours |
| P1 | Degraded performance, high error rate | < 1 hour | < 24 hours |
| P2 | Non-critical errors, localized issues | < 4 hours | < 48 hours |
| P3 | Informational, low-impact | < 24 hours | Best effort |

**Incident Communication**:
- Status page updated every 30 minutes (during P0/P1 incidents)
- Email notification to affected customers (P0/P1 only)
- Post-mortem published within 5 business days (P0/P1 only)

---

### Disaster Recovery

**Backup Strategy**:
- **Frequency**: Daily automated backups (AWS RDS snapshots)
- **Retention**: 30 days (daily), 90 days (weekly)
- **Location**: Cross-region replication (US East → US West)
- **Encryption**: AES-256 (same as production data)

**Recovery Objectives**:
- **RTO (Recovery Time Objective)**: 4 hours (time to restore service)
- **RPO (Recovery Point Objective)**: 24 hours (maximum data loss)

**Disaster Recovery Testing**:
- **Frequency**: Annual (minimum)
- **Scope**: Full database restore, application deployment, service validation
- **Documentation**: DR test report (success criteria, issues, remediation)

---

## Customer Controls

### Data Deletion on Request

**In-App**:
- Settings → Delete My Data
- Confirmation dialog with warning
- 30-day deletion SLA (GDPR/CCPA compliant)

**Email**:
- Contact support@timbuktoo.app
- Request account deletion
- Verification required (email confirmation)
- 30-day deletion SLA

**Deletion Scope**:
- User account
- Travel preferences
- AI-generated itineraries
- Feedback and reports
- Billing history (retained for 7 years per tax law)

---

### Audit Logs (Enterprise Tier)

**Available to Enterprise Customers**:
- User activity logs (login, logout, data access)
- API audit logs (all API calls with timestamp, IP, user_id)
- Admin activity logs (permission changes, data exports)

**Retention**: 90 days (default), 1 year (enterprise tier)

**Access**: Self-service via Enterprise Dashboard or API

**Compliance**: GDPR Article 30 (Records of Processing Activities)

---

### Custom Retention Policies (Enterprise Tier)

**Default Retention**:
- Account data: Until deletion request
- Itineraries: 2 years after last login
- Usage logs: 90 days

**Custom Retention** (Enterprise only):
- Extend itinerary retention to 5 years (for archival)
- Reduce usage log retention to 30 days (for compliance)
- Immediate deletion (no 30-day grace period)

**Configuration**: Contact enterprise@timbuktoo.app to customize retention policies

---

## Vendor Security

### Third-Party Service Providers

| Provider | Service | Compliance | Data Shared |
|----------|---------|------------|-------------|
| AWS | Infrastructure (hosting, database) | SOC 2, ISO 27001, GDPR | User data (encrypted) |
| Anthropic | AI API (Claude 3.5 Sonnet) | SOC 2 Type II, GDPR | Travel preferences, prompts |
| Stripe | Payment processing | PCI-DSS Level 1, SOC 2 | Payment info (tokenized) |
| Datadog | Monitoring & logging | SOC 2, ISO 27001 | Logs (no PII) |
| Firebase | Crash reporting (mobile) | ISO 27001, GDPR | Crash logs (no PII) |

**Vendor Risk Assessment**:
- Annual security questionnaire (all vendors)
- SOC 2 report review (critical vendors)
- Vendor contract includes data protection clauses

---

## Security Contacts

**General Security Inquiries**:
- Email: security@timbuktoo.app
- Response Time: < 24 hours (business days)

**Vulnerability Disclosure**:
- Email: security@timbuktoo.app
- Bug Bounty: [TBD - HackerOne, Bugcrowd]
- Response Time: < 48 hours (acknowledgment), < 7 days (triage)

**Enterprise Support**:
- Email: enterprise@timbuktoo.app
- Phone: [TBD]
- Response Time: < 4 hours (business hours)

---

**Last Updated**: 2024-07-16
**Next Review**: Quarterly (or upon significant changes)
**Owner**: CISO + Legal Team
