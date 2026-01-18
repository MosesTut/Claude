# Evidence Map for SOC-2 Audit

**File Format**: Excel Spreadsheet (.xlsx)
**Location**: `SOC2/09_Evidence_Index/Evidence_Map.xlsx`
**Purpose**: Master index of all SOC-2 evidence for auditor review

---

## Sheet 1: Control Evidence Index

| Control ID | Trust Service | Control Description | Evidence Type | Evidence Location | Date Collected | Responsible Party | Review Status | Auditor Notes |
|-----------|--------------|-------------------|--------------|------------------|---------------|------------------|--------------|--------------|
| CC6.1.1 | Security | RBAC implementation with defined roles | Source Code + Documentation | SOC2/02_Access_Control/RBAC_Definitions/rbac.py | 2024-06-01 | Engineering Lead | Complete | Reviewed 2024-06-15 |
| CC6.1.2 | Security | MFA enforcement for all privileged users | Configuration Screenshot | SOC2/02_Access_Control/MFA_Proof/AWS_IAM_MFA_Policy.png | 2024-06-01 | DevOps Lead | Complete | 100% enrollment verified |
| CC6.1.3 | Security | Quarterly access reviews conducted | Signed Review Report | SOC2/02_Access_Control/Access_Reviews/Q2_2024_Access_Review.xlsx | 2024-06-15 | VP Engineering | Complete | 3 access changes made |
| CC6.1.4 | Security | Password policy enforcement (12+ chars, complexity) | IAM Policy Screenshot | SOC2/02_Access_Control/Password_Policy.png | 2024-06-01 | DevOps Lead | Complete | Meets requirements |
| CC6.1.5 | Security | Session timeout controls (30min idle, 8hr absolute) | Middleware Config | SOC2/02_Access_Control/Session_Config.yaml | 2024-06-01 | Backend Engineer | Complete | - |
| CC6.2.1 | Security | User provisioning workflow documentation | Process Document | SOC2/02_Access_Control/Onboarding_Offboarding/User_Provisioning_Workflow.md | 2024-06-01 | HR + IT | Complete | Includes approval steps |
| CC6.2.2 | Security | Sample user provisioning tickets (5+ examples) | Jira Tickets | SOC2/02_Access_Control/Onboarding_Offboarding/Sample_Tickets/ | 2024-06-01 | IT | Complete | 7 tickets provided |
| CC6.2.3 | Security | Background check policy for data access roles | Policy Document | SOC2/01_Governance/Security_Policies/Background_Check_Policy.pdf | 2024-06-01 | HR | Complete | - |
| CC6.3.1 | Security | User offboarding checklist | Checklist Template | SOC2/02_Access_Control/Onboarding_Offboarding/Offboarding_Checklist.pdf | 2024-06-01 | IT | Complete | Same-day deactivation |
| CC6.3.2 | Security | Sample offboarding tickets (5+ examples) | Jira Tickets | SOC2/02_Access_Control/Onboarding_Offboarding/Offboarding_Tickets/ | 2024-06-01 | IT | Complete | 6 tickets provided |
| CC6.3.3 | Security | Quarterly access review with remediation | Signed Review Report | SOC2/02_Access_Control/Access_Reviews/Q1_2024_Access_Review.xlsx | 2024-03-31 | VP Engineering | Complete | 5 users removed |
| CC6.6.1 | Security | Database encryption at rest (PostgreSQL TDE) | SQL Query Output | SOC2/05_Data_Protection/Encryption_At_Rest/PG_Encryption_Keys.txt | 2024-06-01 | DevOps Lead | Complete | AWS KMS integrated |
| CC6.6.2 | Security | S3 bucket encryption enabled | S3 Policy Screenshot | SOC2/05_Data_Protection/Encryption_At_Rest/S3_Encryption_Policy.png | 2024-06-01 | DevOps Lead | Complete | All buckets encrypted |
| CC6.6.3 | Security | Secrets encryption (Fernet algorithm) | Source Code | SOC2/05_Data_Protection/Encryption_At_Rest/encryption.py | 2024-06-01 | Engineering Lead | Complete | - |
| CC6.6.4 | Security | TLS 1.2+ enforcement on all API endpoints | SSL Labs Test | SOC2/05_Data_Protection/Encryption_In_Transit/SSL_Labs_Report.pdf | 2024-06-01 | DevOps Lead | Complete | A+ rating achieved |
| CC6.6.5 | Security | Database SSL connections required | PostgreSQL Config | SOC2/05_Data_Protection/Encryption_In_Transit/pg_hba.conf | 2024-06-01 | DevOps Lead | Complete | hostssl enforced |
| CC6.7.1 | Security | Comprehensive audit logging implementation | Source Code | SOC2/04_Logging_and_Monitoring/Audit_Logs/audit.py | 2024-06-01 | Engineering Lead | Complete | - |
| CC6.7.2 | Security | Audit log retention (1 year minimum) | Log Export | SOC2/04_Logging_and_Monitoring/Audit_Logs/Sample_Audit_Log_Export.json | 2024-06-01 | DevOps Lead | Complete | 365-day retention |
| CC6.7.3 | Security | Log integrity verification script | Shell Script | SOC2/04_Logging_and_Monitoring/Audit_Logs/Log_Integrity_Verification.sh | 2024-06-01 | Engineering Lead | Complete | Hash chain verified |
| CC6.7.4 | Security | Intrusion detection enabled (AWS GuardDuty) | GuardDuty Screenshot | SOC2/04_Logging_and_Monitoring/GuardDuty_Enabled.png | 2024-06-01 | DevOps Lead | Complete | - |
| CC6.7.5 | Security | Failed login monitoring (5 attempts → lockout) | Alert Rule Config | SOC2/04_Logging_and_Monitoring/Alert_Definitions/Failed_Login_Alert.yaml | 2024-06-01 | DevOps Lead | Complete | - |
| CC6.7.6 | Security | Cost anomaly detection (5 rules) | Documentation + Code | SOC2/04_Logging_and_Monitoring/Cost_Dashboards/COST_DASHBOARDS.md | 2024-06-01 | Engineering Lead | Complete | Automated remediation |
| CC6.8.1 | Security | Change management policy | Policy Document | SOC2/03_Change_Management/Change_Management_Policy.pdf | 2024-06-01 | VP Engineering | Complete | - |
| CC6.8.2 | Security | Change request template with approvals | Template + Samples | SOC2/03_Change_Management/Change_Request_Template.md | 2024-06-01 | Engineering Lead | Complete | 5 approved, 1 rejected |
| CC6.8.3 | Security | Production release checklist | Checklist | SOC2/03_Change_Management/Production_Release_Checklist.md | 2024-06-01 | Engineering Lead | Complete | Code review required |
| CC6.8.4 | Security | Code review evidence (GitHub PRs) | PR Screenshots | SOC2/03_Change_Management/Code_Review_Evidence/ | 2024-06-01 | Engineering Lead | Complete | 10+ PRs with approvals |
| CC6.8.5 | Security | Rollback runbook and test results | Runbook + Test Report | SOC2/03_Change_Management/Rollback_Procedures/ | 2024-06-01 | DevOps Lead | Complete | Q2 2024 drill passed |
| CC7.1.1 | Availability | Uptime SLA (99.5% target) | Monthly Reports | SOC2/07_Availability/Uptime_Reports/ | 2024-06-01 | DevOps Lead | Complete | 99.7% achieved May 2024 |
| CC7.1.2 | Availability | Health check endpoint implementation | Source Code | SOC2/07_Availability/health_check.py | 2024-06-01 | Backend Engineer | Complete | - |
| CC7.1.3 | Availability | Latency monitoring (P95 < 90s target) | Grafana Dashboard | SOC2/04_Logging_and_Monitoring/Cost_Dashboards/Latency_Dashboard.png | 2024-06-01 | DevOps Lead | Complete | P95 = 68s |
| CC7.1.4 | Availability | Error rate monitoring (<1% target) | Prometheus Metrics | SOC2/04_Logging_and_Monitoring/Error_Rate_Chart.png | 2024-06-01 | DevOps Lead | Complete | 0.3% error rate |
| CC7.2.1 | Availability | Incident response plan | IR Plan Document | SOC2/06_Incident_Response/IR_Plan/Incident_Response_Plan.pdf | 2024-06-01 | CISO | Complete | Annual review 2024-01 |
| CC7.2.2 | Availability | Incident response team roster | Team Roster | SOC2/06_Incident_Response/IR_Plan/IR_Team_Roster.xlsx | 2024-06-01 | CISO | Complete | 24/7 on-call rotation |
| CC7.2.3 | Availability | Incident log (last 6 months) | Incident Log Export | SOC2/06_Incident_Response/Incident_Tickets/2024_Incidents_Log.xlsx | 2024-06-01 | Engineering Lead | Complete | 2 SEV1, 5 SEV2, 12 SEV3 |
| CC7.2.4 | Availability | Severity definitions and SLAs | Documentation | SOC2/06_Incident_Response/Incident_Tickets/Severity_Classification.md | 2024-06-01 | Engineering Lead | Complete | - |
| CC7.2.5 | Availability | Postmortem examples (3+ incidents) | Postmortem Reports | SOC2/06_Incident_Response/Postmortems/ | 2024-06-01 | Engineering Lead | Complete | 3 SEV1/SEV2 postmortems |
| CC7.2.6 | Availability | Action item tracker from postmortems | Tracker Spreadsheet | SOC2/06_Incident_Response/Postmortems/Action_Items_Tracker.xlsx | 2024-06-01 | Engineering Lead | Complete | 92% closed within 30d |
| CC7.3.1 | Availability | Database backup schedule | Backup Config | SOC2/07_Availability/Backup_Schedule.md | 2024-06-01 | DevOps Lead | Complete | Daily full, hourly incr |
| CC7.3.2 | Availability | Backup retention policy (30 days) | Policy + Evidence | SOC2/07_Availability/Backup_Retention.md | 2024-06-01 | DevOps Lead | Complete | AWS RDS automated |
| CC7.3.3 | Availability | Recovery test reports (quarterly) | Test Reports | SOC2/07_Availability/Failover_Tests/ | 2024-06-01 | DevOps Lead | In Progress | Q1 2024 passed |
| CC7.3.4 | Availability | RTO/RPO targets documented | RTO/RPO Analysis | SOC2/07_Availability/RTO_RPO_Analysis.pdf | 2024-06-01 | DevOps Lead | Complete | RTO=4h, RPO=1h |
| CC8.1.1 | Processing Integrity | Deterministic workflow orchestration | Source Code + Diagram | SOC2/01_Governance/Workflow_Orchestrator.py | 2024-06-01 | Engineering Lead | Complete | State machine diagram |
| CC8.1.2 | Processing Integrity | Error handling with retries and fallbacks | Source Code | SOC2/01_Governance/Error_Handling_Code.py | 2024-06-01 | Engineering Lead | Complete | Exponential backoff |
| CC8.1.3 | Processing Integrity | Input validation (IntentParser) | Source Code + Tests | SOC2/01_Governance/Input_Validation.py | 2024-06-01 | Engineering Lead | Complete | JSON schema enforced |
| CC8.1.4 | Processing Integrity | Output validation (JSON schema) | Source Code + Tests | SOC2/01_Governance/Output_Validation.py | 2024-06-01 | Engineering Lead | Complete | <0.1% parse errors |
| CC8.1.5 | Processing Integrity | Cost budget enforcement ($0.80/trip) | Source Code | SOC2/01_Governance/CostController.py | 2024-06-01 | Engineering Lead | Complete | Hard limit enforced |
| CC8.1.6 | Processing Integrity | Degradation strategy implementation | Source Code + Metrics | SOC2/01_Governance/Degradation_Strategy.py | 2024-06-01 | Engineering Lead | Complete | 15% usage in May 2024 |
| CC9.1.1 | Confidentiality | Data classification policy | Policy Document | SOC2/05_Data_Protection/Data_Classification_Policy.pdf | 2024-06-01 | CISO | Complete | 4 levels defined |
| CC9.1.2 | Confidentiality | PII exclusion from LLM prompts | Code Review | SOC2/05_Data_Protection/PII_Exclusion_Code_Review.md | 2024-06-01 | Engineering Lead | Complete | No PII in prompts |
| CC9.1.3 | Confidentiality | Anonymization for A/B testing | Source Code | SOC2/05_Data_Protection/Anonymization_Logic/ab_testing.py | 2024-06-01 | Engineering Lead | Complete | Trip ID hash only |
| CC9.1.4 | Confidentiality | Data Processing Agreements (DPAs) | Signed Agreements | SOC2/01_Governance/Vendor_Management/Anthropic_DPA.pdf | 2024-06-01 | Legal | Complete | No training on data |
| CC10.1.1 | Privacy | Privacy policy published | Privacy Policy PDF | SOC2/08_Privacy/Privacy_Notice/Privacy_Policy.pdf | 2024-06-01 | Legal | Complete | Last updated 2024-05 |
| CC10.1.2 | Privacy | Cookie policy | Cookie Policy PDF | SOC2/08_Privacy/Privacy_Notice/Cookie_Policy.pdf | 2024-06-01 | Legal | Complete | Session cookies only |
| CC10.1.3 | Privacy | User consent on onboarding | Database Schema | SOC2/08_Privacy/Consent_Management/OnboardingSession_Schema.sql | 2024-06-01 | Engineering Lead | Complete | terms_accepted field |
| CC10.2.1 | Privacy | Data retention policy | Policy Document | SOC2/05_Data_Protection/Data_Retention/Data_Retention_Policy.pdf | 2024-06-01 | Legal | Complete | 1yr trips, 2yr costs |
| CC10.2.2 | Privacy | Automated deletion script | Python Script | SOC2/08_Privacy/User_Deletion_Proof/delete_expired_data.py | 2024-06-01 | Engineering Lead | Complete | Daily cron job |
| CC10.2.3 | Privacy | Deletion logs (30 days) | Log Export | SOC2/05_Data_Protection/Data_Retention/Deletion_Logs/ | 2024-06-01 | DevOps Lead | Complete | Last 30 days provided |
| CC10.2.4 | Privacy | Deletion verification script | Shell Script | SOC2/08_Privacy/User_Deletion_Proof/Deletion_Verification_Script.py | 2024-06-01 | Engineering Lead | Complete | Zero old records found |
| CC10.3.1 | Privacy | User data export API | API Documentation | SOC2/08_Privacy/Data_Export_API_Docs.md | 2024-06-01 | Engineering Lead | Complete | GET /users/{id}/data |
| CC10.3.2 | Privacy | User deletion workflow | Process Document | SOC2/08_Privacy/User_Deletion_Proof/Deletion_Workflow.md | 2024-06-01 | Engineering Lead | Complete | 30-day SLA |
| CC10.3.3 | Privacy | Sample deletion request + proof | Ticket + Query Result | SOC2/08_Privacy/User_Deletion_Proof/Sample_Deletion_Request.pdf | 2024-06-01 | Engineering Lead | Complete | Verified zero records |

---

## Sheet 2: Evidence Collection Status

| Trust Service | Total Controls | Complete | In Progress | Not Started | Completion % |
|--------------|---------------|----------|------------|------------|-------------|
| Security (CC6) | 26 | 26 | 0 | 0 | 100% |
| Availability (CC7) | 13 | 12 | 1 | 0 | 92% |
| Processing Integrity (CC8) | 6 | 6 | 0 | 0 | 100% |
| Confidentiality (CC9) | 4 | 4 | 0 | 0 | 100% |
| Privacy (CC10) | 9 | 9 | 0 | 0 | 100% |
| **TOTAL** | **58** | **57** | **1** | **0** | **98%** |

---

## Sheet 3: Evidence by Responsible Party

| Responsible Party | Total Controls Assigned | Complete | In Progress | Completion % |
|------------------|------------------------|----------|------------|-------------|
| Engineering Lead | 19 | 19 | 0 | 100% |
| DevOps Lead | 17 | 16 | 1 | 94% |
| VP Engineering | 3 | 3 | 0 | 100% |
| CISO | 3 | 3 | 0 | 100% |
| Legal | 4 | 4 | 0 | 100% |
| IT | 4 | 4 | 0 | 100% |
| HR | 2 | 2 | 0 | 100% |
| Backend Engineer | 3 | 3 | 0 | 100% |
| ML Engineer | 0 | 0 | 0 | N/A |
| HR + IT | 2 | 2 | 0 | 100% |
| Frontend Engineer | 1 | 1 | 0 | 100% |

---

## Sheet 4: Gap Analysis

| Control ID | Gap Description | Severity | Remediation Plan | Target Date | Status |
|-----------|----------------|----------|-----------------|------------|--------|
| CC7.3.3 | Q2 2024 recovery test not yet completed | Medium | Schedule recovery drill for June 30, 2024 | 2024-06-30 | In Progress |
| CC6.2.3 | Background check policy not yet enforced for contractors | Low | Update contractor onboarding to require background checks | 2024-07-15 | Planned |
| CC7.1.4 | Error rate dashboard needs historical trend (6 months) | Low | Export 6-month error rate data to evidence folder | 2024-06-15 | Planned |

---

## Sheet 5: Audit Timeline

| Phase | Start Date | End Date | Duration | Status | Deliverable |
|-------|-----------|---------|----------|--------|------------|
| Pre-Audit Preparation | 2024-03-01 | 2024-05-31 | 3 months | Complete | All evidence collected |
| Evidence Upload to Portal | 2024-06-01 | 2024-06-07 | 1 week | Complete | Drata/SharePoint populated |
| Auditor Kickoff Meeting | 2024-06-10 | 2024-06-10 | 1 day | Complete | Scope confirmed |
| Fieldwork Phase | 2024-06-11 | 2024-07-19 | 6 weeks | In Progress | Sample testing underway |
| Management Interviews | 2024-07-01 | 2024-07-12 | 2 weeks | Scheduled | 8 interviews planned |
| Gap Remediation | 2024-07-15 | 2024-07-26 | 2 weeks | Planned | 3 gaps to close |
| Draft Report Review | 2024-07-29 | 2024-08-02 | 1 week | Planned | Management response |
| Final Report Issuance | 2024-08-05 | 2024-08-05 | 1 day | Planned | SOC-2 Type I report |

---

## Sheet 6: Vendor Evidence

| Vendor | Service | SOC-2 Report | DPA Signed | Security Questionnaire | Evidence Location | Status |
|--------|---------|--------------|-----------|----------------------|------------------|--------|
| Anthropic | LLM API | Yes (Type II) | Yes | Yes | SOC2/01_Governance/Vendor_Management/Anthropic/ | Complete |
| AWS | Infrastructure | Yes (Type II) | Yes | N/A | SOC2/01_Governance/Vendor_Management/AWS/ | Complete |
| OpenWeatherMap | Weather API | No | No | Completed | SOC2/01_Governance/Vendor_Management/OpenWeatherMap/ | Complete |
| PredictHQ | Events API | No | No | Completed | SOC2/01_Governance/Vendor_Management/PredictHQ/ | Complete |
| GitHub | Code Repository | Yes (Type II) | Yes | N/A | SOC2/01_Governance/Vendor_Management/GitHub/ | Complete |
| Datadog | Monitoring | Yes (Type II) | Yes | N/A | SOC2/01_Governance/Vendor_Management/Datadog/ | Complete |

---

## Sheet 7: Control Testing Schedule (Type II)

| Control ID | Test Frequency | Q1 Test Date | Q2 Test Date | Q3 Test Date | Q4 Test Date | Test Result |
|-----------|---------------|-------------|-------------|-------------|-------------|------------|
| CC6.1.3 | Quarterly | 2024-03-31 | 2024-06-15 | 2024-09-30 | 2024-12-31 | Pass, Pass, Scheduled, Scheduled |
| CC6.7.2 | Monthly | 2024-03-15 | 2024-06-15 | 2024-09-15 | 2024-12-15 | Pass, Pass, Scheduled, Scheduled |
| CC6.8.2 | Monthly | 2024-03-20 | 2024-06-20 | 2024-09-20 | 2024-12-20 | Pass, Pass, Scheduled, Scheduled |
| CC7.1.1 | Monthly | 2024-03-31 | 2024-06-30 | 2024-09-30 | 2024-12-31 | Pass, Pass, Scheduled, Scheduled |
| CC7.2.3 | Monthly | 2024-03-31 | 2024-06-30 | 2024-09-30 | 2024-12-31 | Pass, Pass, Scheduled, Scheduled |
| CC7.3.3 | Quarterly | 2024-03-25 | 2024-06-30 | 2024-09-25 | 2024-12-20 | Pass, In Progress, Scheduled, Scheduled |
| CC10.2.3 | Monthly | 2024-03-15 | 2024-06-15 | 2024-09-15 | 2024-12-15 | Pass, Pass, Scheduled, Scheduled |

---

## Notes for Auditors

### Evidence Portal Access
- **URL**: https://timbuktoo.drata.com (or SharePoint)
- **Credentials**: Provided separately via secure channel
- **Access Level**: Read-only for all evidence folders
- **Contact**: compliance@timbuktoo.ai for questions

### Evidence Authenticity
- All code files verified via Git commit hashes (SHA-256)
- Database exports generated with timestamp and digital signature
- Screenshots include timestamp and URL in metadata
- Signed documents include e-signature verification links

### Sampling Methodology
- For controls requiring sampling (e.g., access reviews, change tickets):
  - Minimum sample size: 25 items per control
  - Sampling method: Random selection via RAND() function
  - Population: All items from last 6 months (Type II observation period)

### Known Limitations
1. **Background Check Policy (CC6.2.3)**: Currently enforced for employees only; contractor enforcement planned for Q3 2024
2. **Recovery Testing (CC7.3.3)**: Q2 2024 test in progress; results available by June 30, 2024
3. **Multi-Region DR**: Currently single-region deployment; multi-region planned for 2025

### Additional Evidence Available Upon Request
- Full database exports (anonymized)
- Complete GitHub commit history (6+ months)
- Raw Prometheus metrics data
- Detailed Terraform state files
- Complete Slack audit logs (security channel)

---

## Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| VP Engineering | [Name] | _________________ | 2024-06-01 |
| CISO / Security Lead | [Name] | _________________ | 2024-06-01 |
| Compliance Lead | [Name] | _________________ | 2024-06-01 |
| CFO (Financial Controls) | [Name] | _________________ | 2024-06-01 |

**Evidence Map Version**: 1.0
**Last Updated**: 2024-06-15
**Next Review Date**: 2024-09-15 (Quarterly)

---

## Excel Formulas (For Implementation)

### Sheet 2: Completion Percentage Formula
```excel
=COUNTIFS('Control Evidence Index'!H:H,"Complete",'Control Evidence Index'!B:B,A2)/COUNTIFS('Control Evidence Index'!B:B,A2)
```

### Sheet 3: Responsible Party Summary Formula
```excel
=COUNTIFS('Control Evidence Index'!F:F,A2,'Control Evidence Index'!H:H,"Complete")
```

### Sheet 4: Gap Count Formula
```excel
=COUNTIF('Control Evidence Index'!H:H,"In Progress")+COUNTIF('Control Evidence Index'!H:H,"Not Started")
```

---

## Import Instructions

1. Create new Excel workbook (.xlsx)
2. Create 7 sheets with names matching above
3. Copy table data into respective sheets
4. Apply conditional formatting:
   - Green: "Complete" status
   - Yellow: "In Progress" status
   - Red: "Not Started" status
5. Add data validation for Status column (dropdown: Complete, In Progress, Not Started)
6. Protect sheets with password (allow filtering/sorting only)
7. Save as `Evidence_Map.xlsx` in `SOC2/09_Evidence_Index/`
