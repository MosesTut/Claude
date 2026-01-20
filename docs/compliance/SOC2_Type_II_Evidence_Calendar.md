# SOC 2 Type II Evidence Calendar - Timbuktoo

**Control Period**: Day 0 (2024-07-16) → Day 180 (2025-01-12)
**Expected Completion**: Q2 2025 (February 2025)
**Audit Firm**: [TBD - Select from Big 4 or boutique firm]

---

## 6-Month Control Calendar

| Month | Activity | Evidence Sources | Owner | Status |
|-------|----------|------------------|-------|--------|
| **Month 0** | Auditor Kickoff<br>Control Environment Review | - Governance docs<br>- Risk register<br>- Org chart | Security Team | ⏳ Pending |
| **Month 1** | Access Review + Logging | - Quarterly access review<br>- AWS CloudTrail logs<br>- GitHub audit logs | Engineering + Security | ⏳ Pending |
| **Month 2** | Change Management Evidence | - Jira approvals<br>- GitHub PR reviews<br>- Deployment logs | Engineering | ⏳ Pending |
| **Month 3** | Incident Response Tabletop | - PagerDuty logs<br>- Incident reports<br>- Tabletop exercise results | Security + Engineering | ⏳ Pending |
| **Month 4** | Vendor Risk Review | - Vendor security questionnaires<br>- SOC 2 reports from vendors<br>- Contract reviews | Procurement + Legal | ⏳ Pending |
| **Month 5** | DR Test Execution | - Backup restore logs<br>- DR test report<br>- Service validation | Engineering + Security | ⏳ Pending |
| **Month 6** | Evidence Freeze + Audit | - All evidence finalized<br>- Auditor review<br>- SOC 2 Type II report | Auditor + Security | ⏳ Pending |

---

## Automated Evidence Sources

### Access Reviews (CC 6.0)
- **Frequency**: Quarterly
- **Tool**: Custom script + Google Sheets
- **Evidence**: Access review report (CSV export)
- **Validation**: All production access requires MFA, least privilege enforced

### Change Management (CC 8.0)
- **Frequency**: Continuous
- **Tool**: Jira + GitHub
- **Evidence**:
  - Jira tickets with approval workflow
  - GitHub PR reviews (2 approvals required)
  - Deployment logs (timestamped)
- **Validation**: No production changes without approval

### Monitoring & Alerting (CC 7.0)
- **Frequency**: Real-time
- **Tool**: Datadog + PagerDuty
- **Evidence**:
  - Datadog alerts (P0/P1 incidents)
  - PagerDuty incident logs
  - Response time metrics
- **Validation**: < 15 min response time for P0

### Backups & Recovery (CC 7.0)
- **Frequency**: Daily
- **Tool**: AWS RDS + S3
- **Evidence**:
  - Backup success logs (automated)
  - Quarterly DR test reports (manual)
  - Recovery time metrics
- **Validation**: 30-day retention, cross-region replication

### Incident Management (CC 7.0)
- **Frequency**: As needed
- **Tool**: PagerDuty + Jira
- **Evidence**:
  - Incident tickets (classification, timeline, resolution)
  - Post-mortem reports (root cause analysis)
  - Remediation plans
- **Validation**: P0/P1 post-mortems within 5 business days

---

## Control Testing Procedures

### CC 1.0 - Control Environment
**Test**: Review governance policies (annually)
**Evidence**: Risk management policy, code of conduct, org chart
**Auditor Action**: Interview executives, review policies

### CC 6.0 - Logical & Physical Access
**Test**: Access review (quarterly)
**Evidence**: User list with roles, access review report, MFA logs
**Auditor Action**: Sample 25 users, verify MFA enabled, verify least privilege

### CC 7.0 - System Operations
**Test**: Incident response (tabletop exercise)
**Evidence**: Tabletop exercise results, incident playbook, PagerDuty logs
**Auditor Action**: Observe tabletop, review response times

### CC 8.0 - Change Management
**Test**: Deployment approval (continuous)
**Evidence**: Jira approval logs, GitHub PR reviews, deployment logs
**Auditor Action**: Sample 25 deployments, verify 2 approvals, verify testing

---

## Evidence Collection Checklist

**Before Audit**:
- [ ] Quarterly access reviews completed (4 total over 180 days)
- [ ] All production changes have Jira approvals
- [ ] Incident response tabletop exercise completed
- [ ] Vendor risk assessments completed (AWS, Anthropic, Stripe)
- [ ] DR test executed and documented
- [ ] Backup logs available (180 days of daily backups)
- [ ] Change management logs available (all deployments tracked)

---

**Last Updated**: 2024-07-16
**Owner**: Security Team + Auditor
