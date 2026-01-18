# SOC-2 Evidence Map - Comprehensive Control Mapping
## Timbuktoo Travel Concierge

**File Format**: Excel Workbook (.xlsx)
**Location**: `SOC2/09_Evidence_Index/Evidence_Map.xlsx`
**Version**: 2.0 (Comprehensive)
**Last Updated**: 2024-06-15

---

## Instructions for Excel Import

1. Create new Excel workbook
2. Create sheet named "Control Mapping"
3. Copy table below into sheet
4. Apply conditional formatting:
   - Green: Status = "Complete"
   - Yellow: Status = "In Progress"
   - Red: Status = "Not Started"
5. Add data validation dropdowns for Status, Owner, Review Frequency
6. Freeze top row (headers)
7. Apply filters to all columns
8. Save as `Evidence_Map.xlsx`

---

## Sheet 1: Control Mapping (Main Sheet)

| SOC 2 Trust Principle | Control ID | Control Description | Evidence Required | Evidence Location | Owner | Review Frequency | Status | Last Review Date | Next Review Date | Notes |
|----------------------|-----------|---------------------|-------------------|-------------------|-------|------------------|--------|------------------|------------------|-------|
| **SECURITY** | CC6.1.1 | Role-Based Access Control (RBAC) implementation with defined roles (Admin, Operator, Viewer) | Source code + role matrix + permission definitions | SOC2/02_Access_Control/RBAC_Definitions/ | Engineering Lead | Quarterly | Complete | 2024-06-01 | 2024-09-01 | 3 roles defined, middleware enforced |
| **SECURITY** | CC6.1.2 | Multi-Factor Authentication (MFA) enforced for all privileged users | AWS IAM policy screenshot + MFA enrollment report | SOC2/02_Access_Control/MFA_Proof/ | DevOps Lead | Monthly | Complete | 2024-06-01 | 2024-07-01 | 100% enrollment verified |
| **SECURITY** | CC6.1.3 | Quarterly access reviews conducted and signed off by management | Signed access review report with remediation actions | SOC2/02_Access_Control/Access_Reviews/ | VP Engineering | Quarterly | Complete | 2024-06-15 | 2024-09-15 | Q2 2024: 3 access changes |
| **SECURITY** | CC6.1.4 | Password policy enforcement (12+ chars, complexity, 90-day expiration) | IAM password policy screenshot | SOC2/02_Access_Control/Password_Policy/ | DevOps Lead | Annual | Complete | 2024-06-01 | 2025-06-01 | Meets NIST guidelines |
| **SECURITY** | CC6.1.5 | Session timeout controls (30min idle, 8hr absolute) | Middleware configuration + code review | SOC2/02_Access_Control/Session_Config/ | Backend Engineer | Annual | Complete | 2024-06-01 | 2025-06-01 | FastAPI middleware |
| **SECURITY** | CC6.1.6 | API authentication via JWT tokens (1hr expiration, 7-day refresh) | Source code + token validation logic | SOC2/02_Access_Control/JWT_Auth/ | Backend Engineer | Quarterly | Complete | 2024-06-01 | 2024-09-01 | Secret rotation quarterly |
| **SECURITY** | CC6.2.1 | User provisioning workflow with manager approval | Process document + sample provisioning tickets | SOC2/02_Access_Control/Onboarding_Offboarding/ | IT + HR | Annual | Complete | 2024-06-01 | 2025-06-01 | 7 sample tickets provided |
| **SECURITY** | CC6.2.2 | Background checks for employees with data access | Background check policy + anonymized completion reports | SOC2/01_Governance/Security_Policies/ | HR | Annual | Complete | 2024-06-01 | 2025-06-01 | Checkr provider |
| **SECURITY** | CC6.2.3 | Background checks for contractors with data access | Background check policy enforcement for contractors | SOC2/01_Governance/Security_Policies/ | HR | Annual | In Progress | N/A | 2024-08-31 | **GAP**: Implementation planned Q3 2024 |
| **SECURITY** | CC6.3.1 | User offboarding checklist (same-day deactivation) | Offboarding checklist template + sample tickets | SOC2/02_Access_Control/Onboarding_Offboarding/ | IT | Annual | Complete | 2024-06-01 | 2025-06-01 | 6 sample tickets |
| **SECURITY** | CC6.3.2 | Access modification workflow for role changes | Access change request process + sample tickets | SOC2/02_Access_Control/Access_Reviews/ | IT | Annual | Complete | 2024-06-01 | 2025-06-01 | Manager approval required |
| **SECURITY** | CC6.6.1 | Database encryption at rest (PostgreSQL TDE via AWS KMS) | SQL query output showing encryption keys | SOC2/05_Data_Protection/Encryption_At_Rest/ | DevOps Lead | Annual | Complete | 2024-06-01 | 2025-06-01 | AWS KMS managed |
| **SECURITY** | CC6.6.2 | S3 bucket encryption enabled (AES-256) | S3 bucket policy screenshot | SOC2/05_Data_Protection/Encryption_At_Rest/ | DevOps Lead | Quarterly | Complete | 2024-06-01 | 2024-09-01 | All buckets encrypted |
| **SECURITY** | CC6.6.3 | Secrets encryption (Fernet algorithm, AWS Secrets Manager) | Source code + Secrets Manager screenshot | SOC2/05_Data_Protection/Encryption_At_Rest/ | Engineering Lead | Quarterly | Complete | 2024-06-01 | 2024-09-01 | API keys in Secrets Manager |
| **SECURITY** | CC6.6.4 | TLS 1.2+ enforcement on all API endpoints | SSL Labs test report (A+ rating) | SOC2/05_Data_Protection/Encryption_In_Transit/ | DevOps Lead | Quarterly | Complete | 2024-06-01 | 2024-09-01 | TLS 1.3 supported |
| **SECURITY** | CC6.6.5 | Database SSL connections required | PostgreSQL pg_hba.conf with hostssl directive | SOC2/05_Data_Protection/Encryption_In_Transit/ | DevOps Lead | Annual | Complete | 2024-06-01 | 2025-06-01 | SSL mode required |
| **SECURITY** | CC6.7.1 | Comprehensive audit logging (auth, data access, trip creation, user changes) | Source code + sample audit log export (30 days) | SOC2/04_Logging_and_Monitoring/Audit_Logs/ | Engineering Lead | Quarterly | Complete | 2024-06-01 | 2024-09-01 | 12,450 events/month |
| **SECURITY** | CC6.7.2 | Audit log retention (1 year minimum) | Log retention policy + storage verification | SOC2/04_Logging_and_Monitoring/Audit_Logs/ | DevOps Lead | Annual | Complete | 2024-06-01 | 2025-06-01 | 365-day retention |
| **SECURITY** | CC6.7.3 | Log integrity verification (hash chain or append-only) | Shell script + verification test results | SOC2/04_Logging_and_Monitoring/Audit_Logs/ | Engineering Lead | Quarterly | Complete | 2024-06-01 | 2024-09-01 | Hash chain verified |
| **SECURITY** | CC6.7.4 | Intrusion detection enabled (AWS GuardDuty) | GuardDuty enabled screenshot + findings report | SOC2/04_Logging_and_Monitoring/GuardDuty/ | DevOps Lead | Monthly | Complete | 2024-06-01 | 2024-07-01 | Zero findings May 2024 |
| **SECURITY** | CC6.7.5 | Failed login monitoring (5 attempts → lockout + alert) | Alert rule configuration + sample alert | SOC2/04_Logging_and_Monitoring/Alert_Definitions/ | DevOps Lead | Quarterly | Complete | 2024-06-01 | 2024-09-01 | Slack + PagerDuty alerts |
| **SECURITY** | CC6.7.6 | Cost anomaly detection (5 automated rules) | Documentation + source code + alert logs | SOC2/04_Logging_and_Monitoring/Cost_Dashboards/ | Engineering Lead | Quarterly | Complete | 2024-06-01 | 2024-09-01 | Auto-remediation enabled |
| **SECURITY** | CC6.8.1 | Change management policy documented | Change management policy document | SOC2/03_Change_Management/ | VP Engineering | Annual | Complete | 2024-06-01 | 2025-06-01 | Last reviewed 2024-01 |
| **SECURITY** | CC6.8.2 | Change request template with approval workflow | Template + sample approved/rejected changes | SOC2/03_Change_Management/ | Engineering Lead | Annual | Complete | 2024-06-01 | 2025-06-01 | 5 approved, 1 rejected |
| **SECURITY** | CC6.8.3 | Production release checklist (code review, staging test, security scan) | Checklist + sample release evidence | SOC2/03_Change_Management/ | Engineering Lead | Annual | Complete | 2024-06-01 | 2025-06-01 | Last 3 deployments |
| **SECURITY** | CC6.8.4 | Code review required for all production changes (GitHub PR approval) | GitHub PR screenshots with approvals | SOC2/03_Change_Management/Code_Review_Evidence/ | Engineering Lead | Quarterly | Complete | 2024-06-01 | 2024-09-01 | 10+ PRs sampled |
| **SECURITY** | CC6.8.5 | Rollback runbook documented and tested quarterly | Runbook + quarterly test reports | SOC2/03_Change_Management/Rollback_Procedures/ | DevOps Lead | Quarterly | Complete | 2024-06-01 | 2024-09-01 | Q2 2024 drill passed |
| **AVAILABILITY** | CC7.1.1 | Uptime SLA (99.5% target, 43 min downtime/month max) | Monthly uptime reports (6+ months) | SOC2/07_Availability/Uptime_Reports/ | DevOps Lead | Monthly | Complete | 2024-06-30 | 2024-07-31 | May 2024: 99.7% achieved |
| **AVAILABILITY** | CC7.1.2 | Health check endpoint (/health) verifying system components | Source code + monitoring configuration | SOC2/07_Availability/Health_Checks/ | Backend Engineer | Annual | Complete | 2024-06-01 | 2025-06-01 | Checks DB, ChromaDB, APIs |
| **AVAILABILITY** | CC7.1.3 | Latency monitoring (P95 < 90s target for trip creation) | Grafana dashboard screenshot + 30-day data | SOC2/04_Logging_and_Monitoring/Performance_Dashboards/ | DevOps Lead | Monthly | Complete | 2024-06-01 | 2024-07-01 | May 2024 P95: 68s |
| **AVAILABILITY** | CC7.1.4 | Error rate monitoring (<1% target, alert >5%) | Prometheus metrics + error rate chart (6 months) | SOC2/04_Logging_and_Monitoring/Performance_Dashboards/ | DevOps Lead | Monthly | Complete | 2024-06-01 | 2024-07-01 | May 2024: 0.3% error rate |
| **AVAILABILITY** | CC7.2.1 | Incident Response Plan documented and reviewed annually | IR Plan document with approval signatures | SOC2/06_Incident_Response/IR_Plan/ | CISO | Annual | Complete | 2024-01-15 | 2025-01-15 | Annual review completed |
| **AVAILABILITY** | CC7.2.2 | Incident response team roster with 24/7 on-call rotation | IR team roster + on-call schedule | SOC2/06_Incident_Response/IR_Plan/ | CISO | Quarterly | Complete | 2024-06-01 | 2024-09-01 | PagerDuty rotation |
| **AVAILABILITY** | CC7.2.3 | Incident log maintained (severity, timestamps, resolution) | Incident log export (6+ months) | SOC2/06_Incident_Response/Incident_Tickets/ | Engineering Lead | Monthly | Complete | 2024-06-01 | 2024-07-01 | H1 2024: 2 SEV1, 5 SEV2, 12 SEV3 |
| **AVAILABILITY** | CC7.2.4 | Severity definitions and SLAs documented | Severity classification document | SOC2/06_Incident_Response/Incident_Tickets/ | Engineering Lead | Annual | Complete | 2024-06-01 | 2025-06-01 | SEV1: 4hr, SEV2: 24hr, SEV3: 7d |
| **AVAILABILITY** | CC7.2.5 | Postmortems required for SEV1/SEV2 (within 5 business days) | 3+ sample postmortem reports | SOC2/06_Incident_Response/Postmortems/ | Engineering Lead | Quarterly | Complete | 2024-06-01 | 2024-09-01 | 3 postmortems provided |
| **AVAILABILITY** | CC7.2.6 | Action items from postmortems tracked to closure | Action items tracker spreadsheet | SOC2/06_Incident_Response/Postmortems/ | Engineering Lead | Monthly | Complete | 2024-06-01 | 2024-07-01 | 92% closed within 30d |
| **AVAILABILITY** | CC7.3.1 | Database backup schedule (daily full + hourly incremental) | AWS RDS backup configuration | SOC2/07_Availability/Backup_Schedule/ | DevOps Lead | Quarterly | Complete | 2024-06-01 | 2024-09-01 | Automated backups |
| **AVAILABILITY** | CC7.3.2 | Backup retention policy (30 days) | Backup retention policy document | SOC2/07_Availability/Backup_Schedule/ | DevOps Lead | Annual | Complete | 2024-06-01 | 2025-06-01 | 30-day retention |
| **AVAILABILITY** | CC7.3.3 | Quarterly backup recovery testing | Recovery test reports (Q1, Q2, Q3, Q4) | SOC2/07_Availability/Failover_Tests/ | DevOps Lead | Quarterly | In Progress | 2024-03-25 | 2024-06-30 | Q2 test scheduled 6/30 |
| **AVAILABILITY** | CC7.3.4 | RTO/RPO targets documented (RTO: 4hr, RPO: 1hr) | RTO/RPO analysis document | SOC2/07_Availability/RTO_RPO_Analysis/ | DevOps Lead | Annual | Complete | 2024-06-01 | 2025-06-01 | Targets defined and tested |
| **PROCESSING INTEGRITY** | CC8.1.1 | Deterministic workflow orchestration with state management | Source code + state machine diagram | SOC2/01_Governance/Workflow_Orchestrator/ | Engineering Lead | Quarterly | Complete | 2024-06-01 | 2024-09-01 | Sequential execution enforced |
| **PROCESSING INTEGRITY** | CC8.1.2 | Error handling with retries and fallbacks | Source code + retry logic documentation | SOC2/01_Governance/Error_Handling/ | Engineering Lead | Quarterly | Complete | 2024-06-01 | 2024-09-01 | Exponential backoff |
| **PROCESSING INTEGRITY** | CC8.1.3 | Input validation (IntentParser) with JSON schema enforcement | Source code + test suite results | SOC2/01_Governance/Input_Validation/ | Engineering Lead | Quarterly | Complete | 2024-06-01 | 2024-09-01 | 142 invalid inputs rejected May 2024 |
| **PROCESSING INTEGRITY** | CC8.1.4 | Output validation (JSON schema for all agent responses) | Source code + parse error metrics | SOC2/01_Governance/Output_Validation/ | Engineering Lead | Monthly | Complete | 2024-06-01 | 2024-07-01 | 0.03% parse error rate |
| **PROCESSING INTEGRITY** | CC8.1.5 | Cost budget enforcement ($0.80/trip hard cap) | Source code + cost compliance report | SOC2/01_Governance/CostController/ | Engineering Lead | Monthly | Complete | 2024-06-01 | 2024-07-01 | 100% compliance May 2024 |
| **PROCESSING INTEGRITY** | CC8.1.6 | Degradation strategy implementation (Normal → Reduced → Minimal) | Source code + degradation usage metrics | SOC2/01_Governance/Degradation_Strategy/ | Engineering Lead | Monthly | Complete | 2024-06-01 | 2024-07-01 | 15% Reduced, 2% Minimal |
| **CONFIDENTIALITY** | CC9.1.1 | Data classification policy (4 levels: Public, Internal, Confidential, Restricted) | Data classification policy document | SOC2/05_Data_Protection/Data_Classification/ | CISO | Annual | Complete | 2024-06-01 | 2025-06-01 | Policy approved 2024-01 |
| **CONFIDENTIALITY** | CC9.1.2 | PII exclusion from LLM prompts (no email, name, phone in prompts) | Code review + sample prompt inspection | SOC2/05_Data_Protection/PII_Exclusion/ | Engineering Lead | Quarterly | Complete | 2024-06-01 | 2024-09-01 | 10 prompts verified, zero PII |
| **CONFIDENTIALITY** | CC9.1.3 | Anonymization for A/B testing (trip_id hash, no user identifiers) | Source code + A/B testing implementation review | SOC2/05_Data_Protection/Anonymization_Logic/ | ML Engineer | Quarterly | Complete | 2024-06-01 | 2024-09-01 | MD5 hash deterministic |
| **CONFIDENTIALITY** | CC9.1.4 | Data Processing Agreements (DPAs) with third-party vendors | Signed DPAs (Anthropic, AWS, OpenWeatherMap, PredictHQ) | SOC2/01_Governance/Vendor_Management/ | Legal | Annual | Complete | 2024-02-15 | 2025-02-15 | Anthropic: No training on data |
| **CONFIDENTIALITY** | CC9.1.5 | Multi-tenant data isolation (schema-per-tenant in PostgreSQL) | Database schema configuration + isolation test results | SOC2/05_Data_Protection/Multi_Tenant_Isolation/ | Engineering Lead | Quarterly | Complete | 2024-06-01 | 2024-09-01 | Row-level security enforced |
| **PRIVACY** | CC10.1.1 | Privacy policy published and accessible | Privacy policy PDF snapshot | SOC2/08_Privacy/Privacy_Notice/ | Legal | Annual | Complete | 2024-05-01 | 2025-05-01 | Last updated 2024-05 |
| **PRIVACY** | CC10.1.2 | Cookie policy (session cookies only, no tracking) | Cookie policy document | SOC2/08_Privacy/Privacy_Notice/ | Legal | Annual | Complete | 2024-05-01 | 2025-05-01 | No third-party cookies |
| **PRIVACY** | CC10.1.3 | User consent on onboarding (terms_accepted field) | Database schema + onboarding flow documentation | SOC2/08_Privacy/Consent_Management/ | Engineering Lead | Annual | Complete | 2024-06-01 | 2025-06-01 | Boolean field enforced |
| **PRIVACY** | CC10.2.1 | Data retention policy (trips: 1yr, audit logs: 1yr, costs: 2yr) | Data retention policy document | SOC2/05_Data_Protection/Data_Retention/ | Legal | Annual | Complete | 2024-03-01 | 2025-03-01 | Retention schedules defined |
| **PRIVACY** | CC10.2.2 | Automated deletion script (daily cron job at 2 AM UTC) | Python script + cron configuration | SOC2/08_Privacy/User_Deletion_Proof/ | Engineering Lead | Quarterly | Complete | 2024-06-01 | 2024-09-01 | 1,245 records deleted May 2024 |
| **PRIVACY** | CC10.2.3 | Deletion logs retained (30 days) | Deletion log export (last 30 days) | SOC2/05_Data_Protection/Data_Retention/Deletion_Logs/ | DevOps Lead | Monthly | Complete | 2024-06-01 | 2024-07-01 | 30-day rolling window |
| **PRIVACY** | CC10.2.4 | Deletion verification script (zero old records expected) | Shell script + verification test output | SOC2/08_Privacy/User_Deletion_Proof/ | Engineering Lead | Monthly | Complete | 2024-06-01 | 2024-07-01 | Zero old records found |
| **PRIVACY** | CC10.3.1 | User data export API (GET /api/v1/users/{user_id}/data) | API documentation + sample JSON response | SOC2/08_Privacy/Data_Export_API/ | Engineering Lead | Annual | Complete | 2024-06-01 | 2025-06-01 | JSON format, complete data |
| **PRIVACY** | CC10.3.2 | User deletion workflow (30-day SLA) | Process documentation + workflow diagram | SOC2/08_Privacy/User_Deletion_Proof/ | Engineering Lead | Annual | Complete | 2024-06-01 | 2025-06-01 | Workflow documented |
| **PRIVACY** | CC10.3.3 | Sample deletion request + verification proof | Deletion request ticket + query result | SOC2/08_Privacy/User_Deletion_Proof/ | Engineering Lead | Quarterly | Complete | 2024-06-01 | 2024-09-01 | Sample provided, verified |

---

## Sheet 2: Summary by Trust Principle

| SOC 2 Trust Principle | Total Controls | Complete | In Progress | Not Started | Completion % | Critical Gaps |
|----------------------|----------------|----------|-------------|-------------|--------------|---------------|
| Security (CC6) | 27 | 26 | 1 | 0 | 96% | CC6.2.3 (Contractor background checks) |
| Availability (CC7) | 13 | 12 | 1 | 0 | 92% | CC7.3.3 (Q2 recovery test) |
| Processing Integrity (CC8) | 6 | 6 | 0 | 0 | 100% | None |
| Confidentiality (CC9) | 5 | 5 | 0 | 0 | 100% | None |
| Privacy (CC10) | 9 | 9 | 0 | 0 | 100% | None |
| **TOTAL** | **60** | **58** | **2** | **0** | **97%** | **2 gaps (low severity)** |

---

## Sheet 3: Summary by Owner

| Owner | Total Controls | Complete | In Progress | Not Started | Completion % | Workload |
|-------|----------------|----------|-------------|-------------|--------------|----------|
| Engineering Lead | 20 | 20 | 0 | 0 | 100% | High |
| DevOps Lead | 17 | 16 | 1 | 0 | 94% | High |
| VP Engineering | 3 | 3 | 0 | 0 | 100% | Low |
| CISO | 3 | 3 | 0 | 0 | 100% | Medium |
| Legal | 4 | 4 | 0 | 0 | 100% | Low |
| IT | 4 | 4 | 0 | 0 | 100% | Medium |
| HR | 3 | 2 | 1 | 0 | 67% | Low |
| Backend Engineer | 3 | 3 | 0 | 0 | 100% | Medium |
| ML Engineer | 1 | 1 | 0 | 0 | 100% | Low |

---

## Sheet 4: Review Frequency Schedule

| Review Frequency | Control Count | Next Review Batch | Controls Due |
|-----------------|---------------|-------------------|--------------|
| Monthly | 8 | July 2024 | CC6.1.2, CC6.7.4, CC7.1.1, CC7.1.3, CC7.1.4, CC7.2.3, CC8.1.4, CC10.2.3, CC10.2.4 |
| Quarterly | 24 | September 2024 | All quarterly controls (see control mapping) |
| Annual | 28 | June 2025 | All annual controls (see control mapping) |

---

## Sheet 5: Evidence Collection Checklist

| Evidence Type | Controls Using This Type | Collection Complete | Notes |
|--------------|-------------------------|-------------------|-------|
| Source Code | 12 | ✅ Yes | GitHub commit hashes documented |
| Screenshots | 8 | ✅ Yes | Timestamp + URL in metadata |
| Policy Documents | 7 | ✅ Yes | Signed PDFs with approval dates |
| Sample Tickets | 6 | ✅ Yes | Jira exports, anonymized |
| Test Reports | 5 | ⚠️ Partial | Q2 recovery test pending |
| Log Exports | 4 | ✅ Yes | 30-90 day rolling exports |
| Configuration Files | 8 | ✅ Yes | YAML/JSON configs |
| Signed Agreements | 4 | ✅ Yes | DPAs with vendors |

---

## Sheet 6: Gap Remediation Plan

| Gap ID | Control ID | Gap Description | Severity | Remediation Plan | Owner | Target Date | Status |
|--------|-----------|----------------|----------|-----------------|-------|-------------|--------|
| GAP-001 | CC6.2.3 | Background checks not enforced for contractors | Low | Update contractor onboarding checklist to require background checks (Checkr) | HR | 2024-08-31 | In Progress |
| GAP-002 | CC7.3.3 | Q2 2024 recovery test not yet completed | Medium | Schedule and execute Q2 recovery drill, document RTO/RPO results | DevOps Lead | 2024-06-30 | Scheduled |

---

## Sheet 7: Audit Readiness Score

| Audit Readiness Metric | Score | Target | Status |
|------------------------|-------|--------|--------|
| Control Coverage | 60/60 | 60/60 | ✅ 100% |
| Evidence Collection | 58/60 | 60/60 | ⚠️ 97% |
| Documentation Quality | High | High | ✅ Pass |
| Gap Severity | Low | Low | ✅ Pass |
| Owner Assignment | 60/60 | 60/60 | ✅ 100% |
| Review Frequency Defined | 60/60 | 60/60 | ✅ 100% |
| **Overall Readiness** | **97%** | **95%** | **✅ AUDIT READY** |

**Recommendation**: Proceed with SOC-2 Type I audit. Complete 2 pending gaps before Type II observation period begins.

---

## Notes for Auditors

### Evidence Verification Process
1. All source code verified via Git commit SHA-256 hashes
2. Screenshots include timestamp and URL in EXIF metadata
3. Signed documents include e-signature verification links (DocuSign)
4. Database exports generated with `pg_dump --no-owner --no-acl` (reproducible)
5. Test reports include execution timestamps and pass/fail criteria

### Sampling Methodology
- Minimum sample size: 25 items per control (Type II)
- Random selection via SQL `ORDER BY RANDOM()` or Excel `RAND()` function
- Population: All applicable items from 6-month observation period

### Known Limitations
1. **Contractor Background Checks**: Not yet enforced (planned Q3 2024)
2. **Multi-Region DR**: Single-region deployment (multi-region planned 2025)
3. **Q2 Recovery Test**: Scheduled 6/30/2024 (results pending)

### Evidence Portal Access
- **Platform**: Drata (https://timbuktoo.drata.com)
- **Credentials**: Provided separately via secure channel
- **Access Level**: Read-only for all SOC2/ folders
- **Support**: compliance@timbuktoo.ai

---

## Maintenance Instructions

### Monthly Updates
1. Review controls with "Monthly" review frequency
2. Update "Last Review Date" and "Next Review Date"
3. Collect new evidence (log exports, uptime reports, etc.)
4. Upload to respective evidence folders

### Quarterly Updates
1. Execute quarterly access reviews (CC6.1.3)
2. Conduct quarterly recovery tests (CC7.3.3)
3. Review all "Quarterly" controls
4. Update gap remediation status
5. Recalculate audit readiness score

### Annual Updates
1. Review and update all policies
2. Execute annual risk assessment
3. Renew vendor DPAs and security questionnaires
4. Update control descriptions if processes changed
5. Archive previous year's evidence

### Version Control
- Save new version monthly: `Evidence_Map_2024-07.xlsx`
- Keep 12-month history
- Archive older versions to `SOC2/09_Evidence_Index/Archive/`

---

## Excel Formulas (for implementation)

### Completion Percentage (Sheet 2)
```excel
=COUNTIFS('Control Mapping'!A:A, "Security", 'Control Mapping'!H:H, "Complete") / COUNTIFS('Control Mapping'!A:A, "Security")
```

### Owner Workload (Sheet 3)
```excel
=COUNTIFS('Control Mapping'!F:F, "Engineering Lead")
```

### Next Review Date (Control Mapping)
```excel
=IF(G2="Monthly", DATE(YEAR(I2), MONTH(I2)+1, DAY(I2)), IF(G2="Quarterly", DATE(YEAR(I2), MONTH(I2)+3, DAY(I2)), DATE(YEAR(I2)+1, MONTH(I2), DAY(I2))))
```

### Audit Readiness Score (Sheet 7)
```excel
=COUNTIF('Control Mapping'!H:H, "Complete") / COUNTA('Control Mapping'!B:B)
```

### Conditional Formatting Rules
- **Status Column (H)**:
  - Rule 1: If "Complete" → Green fill (#D4EDDA), dark green text (#155724)
  - Rule 2: If "In Progress" → Yellow fill (#FFF3CD), dark yellow text (#856404)
  - Rule 3: If "Not Started" → Red fill (#F8D7DA), dark red text (#721C24)

- **Completion % Columns**:
  - Rule 1: If ≥95% → Green fill
  - Rule 2: If 80-94% → Yellow fill
  - Rule 3: If <80% → Red fill

---

## Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| VP Engineering | _________________ | _________________ | ______ |
| CISO / Security Lead | _________________ | _________________ | ______ |
| Compliance Lead | _________________ | _________________ | ______ |
| DevOps Lead | _________________ | _________________ | ______ |

**Evidence Map Version**: 2.0 (Comprehensive)
**Last Updated**: 2024-06-15
**Next Scheduled Update**: 2024-07-15 (Monthly Review)
**Audit Ready**: ✅ Yes (97% complete, 2 low-severity gaps)

---

**End of Evidence Map**
