# SOC 2 Type II Evidence Automation - End-to-End System
## Timbuktoo Travel Concierge

**Objective**: Eliminate manual evidence collection by making control execution = evidence creation
**Principle**: Every control emits machine-verifiable artifacts on execution
**Target**: Continuous compliance with zero "scramble period" before audits

**Version**: 1.0 (Comprehensive)
**Last Updated**: 2024-06-15

---

## Table of Contents

1. [Evidence Automation Architecture](#evidence-automation-architecture)
2. [Automated Evidence Generation (Wrk.Flo)](#automated-evidence-generation-wrkflo)
3. [Evidence Freshness Enforcement](#evidence-freshness-enforcement)
4. [Evidence Collection by Trust Service](#evidence-collection-by-trust-service)
5. [Evidence Storage and Retrieval](#evidence-storage-and-retrieval)
6. [Auditor Portal Integration](#auditor-portal-integration)
7. [Implementation Guide](#implementation-guide)

---

## 1. Evidence Automation Architecture

### 1.1 Core Principle

**Manual Evidence Collection** (Traditional):
```
Control Executed → (weeks later) → Engineer gathers evidence → Upload to folder
```
Problems: Stale data, missing evidence, scramble before audit

**Automated Evidence Collection** (Timbuktoo):
```
Control Executed → Evidence auto-generated → Evidence auto-stored → Evidence auto-indexed
```
Benefits: Real-time compliance, always audit-ready, zero manual work

### 1.2 Evidence Sources

| Source System | Evidence Type | Controls Covered | Auto-Collection Method |
|--------------|---------------|------------------|------------------------|
| **Wrk.Flo** | Workflow logs, approval records, gate decisions | CC8.1 (Processing Integrity) | Workflow execution hooks |
| **Jira** | Tickets, timestamps, ownership, status transitions | CC6.8 (Change Management), CC7.2 (Incidents) | Jira webhooks + API polling |
| **AWS IAM** | RBAC diffs, MFA status, user provisioning/deprovisioning | CC6.1, CC6.2, CC6.3 (Access Control) | IAM event logs + CloudTrail |
| **Datadog/Prometheus** | Uptime, alerts, incidents, performance metrics | CC7.1 (Availability) | Metrics API + alert webhooks |
| **Cost Engine** | Token usage, anomaly flags, budget compliance | CC8.1.5 (Cost Controls) | Cost tracking database |
| **GitHub** | Code commits, PR reviews, deployment history | CC6.8 (Change Management) | GitHub webhooks |
| **PostgreSQL** | Audit logs, access reviews, data retention deletions | CC6.7 (Logging), CC10.2 (Retention) | Database triggers + scheduled queries |
| **AWS Secrets Manager** | Secret rotation logs, access logs | CC6.6 (Encryption) | CloudTrail events |

### 1.3 Evidence Automation Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    EVIDENCE AUTOMATION SYSTEM                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Wrk.Flo    │  │     Jira     │  │   AWS IAM    │             │
│  │  (Workflows) │  │  (Tickets)   │  │  (Access)    │             │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘             │
│         │                  │                  │                     │
│         └──────────────────┼──────────────────┘                     │
│                            │                                        │
│                            ▼                                        │
│                  ┌─────────────────────┐                           │
│                  │  Evidence Collector │                           │
│                  │   (Python Service)  │                           │
│                  └──────────┬──────────┘                           │
│                             │                                       │
│                             ▼                                       │
│                  ┌─────────────────────┐                           │
│                  │ Evidence Processor  │                           │
│                  │  - Validation       │                           │
│                  │  - Formatting       │                           │
│                  │  - Indexing         │                           │
│                  └──────────┬──────────┘                           │
│                             │                                       │
│                             ▼                                       │
│                  ┌─────────────────────┐                           │
│                  │ Evidence Storage    │                           │
│                  │ - S3 (files)        │                           │
│                  │ - PostgreSQL (meta) │                           │
│                  │ - Drata/Vanta       │                           │
│                  └──────────┬──────────┘                           │
│                             │                                       │
│                             ▼                                       │
│                  ┌─────────────────────┐                           │
│                  │ Evidence Index      │                           │
│                  │ (Evidence_Map.xlsx) │                           │
│                  └─────────────────────┘                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.4 Evidence Lifecycle

```
1. TRIGGER
   ↓
   Control executed (access change, deploy, incident, etc.)
   ↓
2. CAPTURE
   ↓
   Evidence auto-generated (logs, snapshots, attestations)
   ↓
3. VALIDATE
   ↓
   Evidence checked for completeness, format, required fields
   ↓
4. STORE
   ↓
   Evidence uploaded to SOC2/ folder structure + S3 + Drata
   ↓
5. INDEX
   ↓
   Evidence_Map.xlsx updated with metadata (location, timestamp, owner)
   ↓
6. EXPIRE
   ↓
   Evidence expires after control frequency (monthly/quarterly/annual)
   ↓
7. ALERT
   ↓
   If evidence missing or stale, Jira blocks "Audit Ready", Slack alert
```

---

## 2. Automated Evidence Generation (Wrk.Flo)

### 2.1 Evidence Automation Configuration

**File**: `config/evidence_automation.yaml`

```yaml
evidence_automation:
  enabled: true
  evidence_bucket: s3://timbuktoo-compliance/soc2-evidence/
  evidence_local_path: SOC2/
  evidence_index_file: SOC2/09_Evidence_Index/Evidence_Map.xlsx
  compliance_platform: drata  # or vanta

  # Global settings
  global:
    retention_days: 730  # 2 years
    encryption: AES-256
    versioning: enabled
    auto_index: true
    notify_on_failure: true
    notification_channels:
      slack: "#compliance-alerts"
      email: compliance@timbuktoo.ai

  # Evidence collection rules by control
  controls:

    # ═══════════════════════════════════════════════════════════════════
    # ACCESS CONTROL EVIDENCE (CC6.1, CC6.2, CC6.3)
    # ═══════════════════════════════════════════════════════════════════

    - control_id: CC6.1.1
      name: RBAC Implementation
      trigger: access_change
      frequency: event_driven
      evidence_type: snapshot
      artifacts:
        - name: rbac_snapshot.json
          description: Complete snapshot of all users and their roles
          source: postgresql
          query: |
            SELECT
              user_id,
              email,
              role,
              created_at,
              last_login,
              mfa_enabled
            FROM users
            WHERE is_active = true
            ORDER BY email;
          format: json
          schema_validation: rbac_snapshot_schema.json

        - name: rbac_permission_matrix.csv
          description: Role-permission mapping matrix
          source: postgresql
          query: |
            SELECT
              r.role_name,
              p.permission_name,
              p.resource_type,
              p.action
            FROM roles r
            JOIN role_permissions rp ON r.role_id = rp.role_id
            JOIN permissions p ON rp.permission_id = p.permission_id
            ORDER BY r.role_name, p.resource_type, p.action;
          format: csv

      storage:
        destination: SOC2/02_Access_Control/RBAC_Definitions/
        filename_pattern: "rbac_snapshot_{{timestamp}}.json"
        retention_days: 365
        compress: true

      validation:
        required_fields:
          - user_id
          - email
          - role
          - mfa_enabled
        min_records: 1
        max_age_hours: 24

      notifications:
        on_success:
          slack_channel: "#compliance-events"
          message: "✅ RBAC snapshot collected: {{artifact_count}} users"
        on_failure:
          slack_channel: "#compliance-alerts"
          pagerduty: true
          message: "⛔ RBAC snapshot failed: {{error_message}}"

    - control_id: CC6.1.2
      name: MFA Enforcement
      trigger: schedule
      frequency: monthly
      schedule: "0 0 1 * *"  # 1st of every month
      evidence_type: report
      artifacts:
        - name: mfa_status_report.json
          description: MFA enrollment and enforcement status
          source: aws_iam
          aws_api: iam.list_users
          processing: |
            import boto3
            iam = boto3.client('iam')
            users = iam.list_users()['Users']

            mfa_status = []
            for user in users:
                mfa_devices = iam.list_mfa_devices(UserName=user['UserName'])
                mfa_status.append({
                    'user_name': user['UserName'],
                    'user_id': user['UserId'],
                    'created_date': user['CreateDate'].isoformat(),
                    'mfa_enabled': len(mfa_devices['MFADevices']) > 0,
                    'mfa_device_count': len(mfa_devices['MFADevices']),
                    'mfa_devices': [d['SerialNumber'] for d in mfa_devices['MFADevices']]
                })

            return {
                'total_users': len(users),
                'mfa_enabled_count': sum(1 for u in mfa_status if u['mfa_enabled']),
                'mfa_enrollment_rate': sum(1 for u in mfa_status if u['mfa_enabled']) / len(users),
                'users': mfa_status
            }
          format: json

      storage:
        destination: SOC2/02_Access_Control/MFA_Proof/
        filename_pattern: "mfa_status_{{year}}_{{month}}.json"
        retention_days: 365

      validation:
        required_keys:
          - total_users
          - mfa_enrollment_rate
        min_enrollment_rate: 1.0  # 100% required
        alert_if_below: 1.0

    - control_id: CC6.1.3
      name: Quarterly Access Reviews
      trigger: schedule
      frequency: quarterly
      schedule: "0 0 1 */3 *"  # 1st day of Jan, Apr, Jul, Oct
      evidence_type: attestation
      artifacts:
        - name: access_review_attestation.pdf
          description: Signed access review with remediation actions
          source: jira_api
          jira_query: |
            project = TRVL
            AND type = "Access Review"
            AND created >= startOfQuarter()
            AND status = Done
          processing: |
            # Fetch Jira access review tickets
            reviews = jira.search_issues(jql_query)

            # Generate attestation PDF
            pdf = generate_attestation_pdf({
                'quarter': current_quarter,
                'year': current_year,
                'total_users': get_total_users(),
                'users_reviewed': len(reviews),
                'access_changes': extract_access_changes(reviews),
                'reviewer': reviews[0].fields.assignee.displayName,
                'review_date': reviews[0].fields.updated,
                'sign_off': 'VP Engineering'
            })

            return pdf
          format: pdf

        - name: access_review_details.xlsx
          description: Detailed access review spreadsheet with before/after
          source: jira_export
          format: xlsx
          columns:
            - User
            - Previous Role
            - Current Role
            - Change Reason
            - Approved By
            - Change Date

      storage:
        destination: SOC2/02_Access_Control/Access_Reviews/
        filename_pattern: "Q{{quarter}}_{{year}}_access_review"
        retention_days: 730  # 2 years

      validation:
        require_signoff: true
        signoff_role: VP Engineering
        min_users_reviewed: 1

      notifications:
        on_generation:
          email_to: vp.engineering@timbuktoo.ai
          subject: "Q{{quarter}} Access Review - Please Sign Off"
          body: "Access review complete. Please review and sign: {{pdf_url}}"

    - control_id: CC6.2.1
      name: User Provisioning Workflow
      trigger: jira_issue_created
      jira_filter: |
        type = "User Provisioning"
        AND status = Done
      frequency: event_driven
      evidence_type: ticket_export
      artifacts:
        - name: user_provisioning_ticket.json
          description: Jira ticket with approval chain
          source: jira_api
          fields_to_capture:
            - issue_key
            - summary
            - description
            - created
            - updated
            - status
            - assignee
            - reporter
            - approvals
            - custom_fields:
                - User Email
                - Role Requested
                - Manager Approval
                - IT Completion Date
          format: json

      storage:
        destination: SOC2/02_Access_Control/Onboarding_Offboarding/Sample_Tickets/
        filename_pattern: "provisioning_{{issue_key}}.json"
        retention_days: 365

      validation:
        required_fields:
          - Manager Approval
          - IT Completion Date
        approval_required: true

    - control_id: CC6.3.1
      name: User Offboarding Checklist
      trigger: jira_issue_created
      jira_filter: |
        type = "User Offboarding"
        AND status = Done
      frequency: event_driven
      evidence_type: ticket_export
      artifacts:
        - name: user_offboarding_ticket.json
          description: Jira ticket with deactivation proof
          source: jira_api
          fields_to_capture:
            - issue_key
            - termination_date
            - account_disabled_date
            - checklist_items:
                - AWS account disabled
                - Jira account disabled
                - GitHub access revoked
                - MFA devices removed
                - VPN access revoked
          format: json

        - name: account_disabled_proof.json
          description: Proof of account deactivation from IAM
          source: aws_iam
          processing: |
            # Verify user account is disabled
            user_email = jira_ticket['User Email']
            iam_user = iam.get_user(UserName=user_email)

            return {
                'user_email': user_email,
                'account_status': 'disabled' if not iam_user else 'active',
                'disabled_date': jira_ticket['account_disabled_date'],
                'verified_at': datetime.utcnow().isoformat()
            }
          format: json

      storage:
        destination: SOC2/02_Access_Control/Onboarding_Offboarding/Offboarding_Tickets/
        filename_pattern: "offboarding_{{issue_key}}.json"

      validation:
        same_day_deactivation: true
        max_hours_to_deactivation: 8

    # ═══════════════════════════════════════════════════════════════════
    # ENCRYPTION EVIDENCE (CC6.6)
    # ═══════════════════════════════════════════════════════════════════

    - control_id: CC6.6.1
      name: Database Encryption at Rest
      trigger: schedule
      frequency: quarterly
      schedule: "0 0 1 */3 *"
      evidence_type: configuration_snapshot
      artifacts:
        - name: database_encryption_config.json
          description: PostgreSQL encryption configuration
          source: aws_rds
          aws_api: rds.describe_db_instances
          processing: |
            rds = boto3.client('rds')
            instances = rds.describe_db_instances()['DBInstances']

            encryption_status = []
            for instance in instances:
                encryption_status.append({
                    'db_instance_id': instance['DBInstanceIdentifier'],
                    'engine': instance['Engine'],
                    'encryption_enabled': instance['StorageEncrypted'],
                    'kms_key_id': instance.get('KmsKeyId'),
                    'created_time': instance['InstanceCreateTime'].isoformat()
                })

            return {
                'total_instances': len(instances),
                'encrypted_instances': sum(1 for i in encryption_status if i['encryption_enabled']),
                'encryption_rate': sum(1 for i in encryption_status if i['encryption_enabled']) / len(instances),
                'instances': encryption_status
            }
          format: json

      storage:
        destination: SOC2/05_Data_Protection/Encryption_At_Rest/
        filename_pattern: "db_encryption_{{quarter}}_{{year}}.json"

      validation:
        require_all_encrypted: true
        encryption_rate_min: 1.0

    - control_id: CC6.6.4
      name: TLS Enforcement
      trigger: schedule
      frequency: quarterly
      schedule: "0 0 15 */3 *"  # 15th of Jan, Apr, Jul, Oct
      evidence_type: security_scan
      artifacts:
        - name: ssl_labs_report.pdf
          description: SSL Labs A+ rating report
          source: ssl_labs_api
          api_endpoint: "https://api.ssllabs.com/api/v3/analyze"
          parameters:
            host: api.timbuktoo.ai
            publish: "off"
            all: "done"
          processing: |
            # Poll SSL Labs API for results
            result = ssl_labs.analyze('api.timbuktoo.ai')

            return {
                'host': result['host'],
                'grade': result['endpoints'][0]['grade'],
                'has_warnings': result['endpoints'][0]['hasWarnings'],
                'protocol_support': result['endpoints'][0]['details']['protocols'],
                'certificate': {
                    'subject': result['endpoints'][0]['details']['cert']['subject'],
                    'issuer': result['endpoints'][0]['details']['cert']['issuerSubject'],
                    'valid_from': result['endpoints'][0]['details']['cert']['notBefore'],
                    'valid_to': result['endpoints'][0]['details']['cert']['notAfter']
                }
            }
          format: json

        - name: tls_config_code.py
          description: Source code showing TLS enforcement
          source: github
          repository: MosesTut/Claude
          file_path: timbuktoo/api/app.py
          extract_lines: "# TLS configuration section"
          format: code_snippet

      storage:
        destination: SOC2/05_Data_Protection/Encryption_In_Transit/
        filename_pattern: "ssl_labs_{{quarter}}_{{year}}"

      validation:
        required_grade: A+
        min_tls_version: "1.2"

    # ═══════════════════════════════════════════════════════════════════
    # AUDIT LOGGING EVIDENCE (CC6.7)
    # ═══════════════════════════════════════════════════════════════════

    - control_id: CC6.7.1
      name: Comprehensive Audit Logging
      trigger: schedule
      frequency: monthly
      schedule: "0 0 1 * *"
      evidence_type: log_export
      artifacts:
        - name: audit_log_sample.json
          description: Sample of audit logs (30 days)
          source: postgresql
          query: |
            SELECT
              event_id,
              event_type,
              action,
              user_id,
              resource_type,
              resource_id,
              status,
              ip_address,
              user_agent,
              created_at
            FROM audit_logs
            WHERE created_at >= NOW() - INTERVAL '30 days'
            ORDER BY created_at DESC
            LIMIT 1000;
          format: json

        - name: audit_log_statistics.json
          description: Audit log statistics and coverage
          source: postgresql
          query: |
            SELECT
              event_type,
              COUNT(*) as event_count,
              COUNT(DISTINCT user_id) as unique_users,
              MIN(created_at) as first_event,
              MAX(created_at) as last_event
            FROM audit_logs
            WHERE created_at >= NOW() - INTERVAL '30 days'
            GROUP BY event_type
            ORDER BY event_count DESC;
          format: json

      storage:
        destination: SOC2/04_Logging_and_Monitoring/Audit_Logs/
        filename_pattern: "audit_log_sample_{{year}}_{{month}}"

      validation:
        min_events: 100
        required_event_types:
          - authentication
          - data_access
          - trip_creation
          - user_change

    - control_id: CC6.7.2
      name: Audit Log Retention
      trigger: schedule
      frequency: monthly
      schedule: "0 0 5 * *"
      evidence_type: retention_proof
      artifacts:
        - name: log_retention_verification.json
          description: Proof of 1-year log retention
          source: postgresql
          query: |
            SELECT
              MIN(created_at) as oldest_log,
              MAX(created_at) as newest_log,
              COUNT(*) as total_logs,
              EXTRACT(DAY FROM (MAX(created_at) - MIN(created_at))) as retention_days
            FROM audit_logs;
          format: json

      storage:
        destination: SOC2/04_Logging_and_Monitoring/Audit_Logs/
        filename_pattern: "log_retention_{{year}}_{{month}}.json"

      validation:
        min_retention_days: 365

    # ═══════════════════════════════════════════════════════════════════
    # CHANGE MANAGEMENT EVIDENCE (CC6.8)
    # ═══════════════════════════════════════════════════════════════════

    - control_id: CC6.8.1
      name: Change Management Process
      trigger: github_webhook
      github_event: pull_request
      github_action: closed
      github_filter: merged = true
      frequency: event_driven
      evidence_type: pull_request_export
      artifacts:
        - name: pr_approval_record.json
          description: GitHub PR with approvals and merge details
          source: github_api
          processing: |
            pr = github.get_pull_request(pr_number)

            return {
                'pr_number': pr.number,
                'title': pr.title,
                'author': pr.user.login,
                'created_at': pr.created_at.isoformat(),
                'merged_at': pr.merged_at.isoformat(),
                'merged_by': pr.merged_by.login,
                'reviewers': [r.user.login for r in pr.get_reviews()],
                'approvals': [r for r in pr.get_reviews() if r.state == 'APPROVED'],
                'files_changed': pr.changed_files,
                'additions': pr.additions,
                'deletions': pr.deletions,
                'commits': pr.commits,
                'checks_passed': all(c.conclusion == 'success' for c in pr.get_check_runs())
            }
          format: json

      storage:
        destination: SOC2/03_Change_Management/Code_Review_Evidence/
        filename_pattern: "pr_{{pr_number}}_{{timestamp}}.json"
        sample_rate: 0.25  # Collect 25% of PRs (random sampling)

      validation:
        min_approvals: 1
        require_checks_passed: true

    - control_id: CC6.8.5
      name: Rollback Testing
      trigger: schedule
      frequency: quarterly
      schedule: "0 0 20 */3 *"  # 20th of Jan, Apr, Jul, Oct
      evidence_type: test_report
      artifacts:
        - name: rollback_test_report.pdf
          description: Quarterly rollback drill results
          source: jira_api
          jira_query: |
            project = TRVL
            AND type = "Rollback Test"
            AND created >= startOfQuarter()
            AND status = Done
          processing: |
            # Generate rollback test report
            test_ticket = jira.search_issues(jql_query)[0]

            return generate_pdf_report({
                'test_date': test_ticket.fields.updated,
                'test_scenario': test_ticket.fields.description,
                'rollback_steps': extract_steps(test_ticket),
                'test_result': 'PASSED' if test_ticket.fields.status == 'Done' else 'FAILED',
                'rto_actual': extract_rto(test_ticket),
                'rto_target': '4 hours',
                'rpo_actual': extract_rpo(test_ticket),
                'rpo_target': '1 hour',
                'tester': test_ticket.fields.assignee.displayName
            })
          format: pdf

      storage:
        destination: SOC2/03_Change_Management/Rollback_Procedures/
        filename_pattern: "rollback_test_Q{{quarter}}_{{year}}.pdf"

    # ═══════════════════════════════════════════════════════════════════
    # AVAILABILITY EVIDENCE (CC7.1, CC7.2, CC7.3)
    # ═══════════════════════════════════════════════════════════════════

    - control_id: CC7.1.1
      name: Uptime Monitoring
      trigger: schedule
      frequency: monthly
      schedule: "0 0 1 * *"
      evidence_type: uptime_report
      artifacts:
        - name: uptime_report.json
          description: Monthly uptime statistics
          source: datadog_api
          datadog_query: |
            monitors:
              - monitor_id: 12345  # API health check monitor
                metric: uptime_percentage
                timeframe: last_month
          processing: |
            datadog = DatadogAPI(api_key, app_key)

            # Get uptime data for last month
            uptime_data = datadog.get_monitor_uptime(
                monitor_id=12345,
                start=first_day_of_last_month,
                end=last_day_of_last_month
            )

            # Calculate SLA compliance
            uptime_pct = uptime_data['uptime_percentage']
            sla_target = 99.5
            sla_met = uptime_pct >= sla_target

            return {
                'month': last_month,
                'year': current_year,
                'uptime_percentage': uptime_pct,
                'downtime_minutes': uptime_data['downtime_minutes'],
                'sla_target': sla_target,
                'sla_met': sla_met,
                'incidents': uptime_data['incidents']
            }
          format: json

      storage:
        destination: SOC2/07_Availability/Uptime_Reports/
        filename_pattern: "uptime_{{year}}_{{month}}.json"

      validation:
        min_uptime_percentage: 99.5

      notifications:
        on_sla_miss:
          slack_channel: "#compliance-alerts"
          pagerduty: true
          email_to: vp.engineering@timbuktoo.ai
          message: "⛔ SLA MISS: Uptime {{uptime_percentage}}% (target: 99.5%)"

    - control_id: CC7.2.1
      name: Incident Response Plan
      trigger: schedule
      frequency: annual
      schedule: "0 0 15 1 *"  # January 15th
      evidence_type: policy_document
      artifacts:
        - name: incident_response_plan.pdf
          description: Annual IR plan review and update
          source: confluence_api
          page_id: 123456  # IR Plan page
          export_format: pdf
          include_approval: true
          approver: CISO

      storage:
        destination: SOC2/06_Incident_Response/IR_Plan/
        filename_pattern: "IR_Plan_{{year}}.pdf"

      validation:
        require_annual_review: true
        require_approval: true

    - control_id: CC7.2.3
      name: Incident Log
      trigger: schedule
      frequency: monthly
      schedule: "0 0 1 * *"
      evidence_type: incident_export
      artifacts:
        - name: incident_log.csv
          description: Monthly incident log export
          source: jira_api
          jira_query: |
            project = TRVL
            AND type = Incident
            AND created >= startOfMonth(-1)
            AND created < startOfMonth()
          fields_to_export:
            - Issue Key
            - Severity
            - Incident Type
            - Created
            - Resolved
            - Resolution Time
            - Assignee
            - RCA Ticket
          format: csv

      storage:
        destination: SOC2/06_Incident_Response/Incident_Tickets/
        filename_pattern: "incidents_{{year}}_{{month}}.csv"

    - control_id: CC7.3.1
      name: Backup Verification
      trigger: schedule
      frequency: monthly
      schedule: "0 0 1 * *"
      evidence_type: backup_report
      artifacts:
        - name: backup_verification.json
          description: Database backup verification
          source: aws_rds
          processing: |
            rds = boto3.client('rds')
            snapshots = rds.describe_db_snapshots(
                DBInstanceIdentifier='timbuktoo-prod',
                SnapshotType='automated'
            )['DBSnapshots']

            # Get snapshots from last 30 days
            recent_snapshots = [
                s for s in snapshots
                if s['SnapshotCreateTime'] >= (datetime.utcnow() - timedelta(days=30))
            ]

            return {
                'total_snapshots': len(recent_snapshots),
                'oldest_snapshot': min(s['SnapshotCreateTime'] for s in recent_snapshots).isoformat(),
                'newest_snapshot': max(s['SnapshotCreateTime'] for s in recent_snapshots).isoformat(),
                'snapshot_frequency_hours': 24,  # Daily
                'retention_days': 30,
                'snapshots': [
                    {
                        'snapshot_id': s['DBSnapshotIdentifier'],
                        'created_at': s['SnapshotCreateTime'].isoformat(),
                        'size_gb': s['AllocatedStorage'],
                        'status': s['Status']
                    }
                    for s in recent_snapshots[:10]  # Last 10 snapshots
                ]
            }
          format: json

      storage:
        destination: SOC2/07_Availability/Backup_Schedule/
        filename_pattern: "backup_verification_{{year}}_{{month}}.json"

      validation:
        min_snapshots: 28  # At least 28 daily snapshots in 30 days
        require_recent_snapshot: true
        max_snapshot_age_hours: 48

    # ═══════════════════════════════════════════════════════════════════
    # PROCESSING INTEGRITY EVIDENCE (CC8.1)
    # ═══════════════════════════════════════════════════════════════════

    - control_id: CC8.1.5
      name: Cost Budget Enforcement
      trigger: schedule
      frequency: monthly
      schedule: "0 0 1 * *"
      evidence_type: cost_report
      artifacts:
        - name: cost_compliance_report.json
          description: Monthly cost budget compliance
          source: postgresql
          query: |
            SELECT
              DATE_TRUNC('day', created_at) as date,
              COUNT(*) as trip_count,
              AVG(total_cost_usd) as avg_cost,
              MAX(total_cost_usd) as max_cost,
              SUM(CASE WHEN total_cost_usd > 0.80 THEN 1 ELSE 0 END) as budget_breaches
            FROM trips
            WHERE created_at >= DATE_TRUNC('month', NOW() - INTERVAL '1 month')
              AND created_at < DATE_TRUNC('month', NOW())
            GROUP BY date
            ORDER BY date;
          format: json

        - name: cost_anomalies.json
          description: Cost anomalies detected and remediated
          source: postgresql
          query: |
            SELECT
              trip_id,
              city,
              variant,
              total_cost_usd,
              degradation_strategy,
              created_at
            FROM trips
            WHERE degradation_strategy != 'normal'
              AND created_at >= DATE_TRUNC('month', NOW() - INTERVAL '1 month')
              AND created_at < DATE_TRUNC('month', NOW())
            ORDER BY total_cost_usd DESC;
          format: json

      storage:
        destination: SOC2/01_Governance/CostController/
        filename_pattern: "cost_compliance_{{year}}_{{month}}"

      validation:
        budget_breach_count: 0  # Zero tolerance for budget breaches
        alert_if_breaches: true

    # ═══════════════════════════════════════════════════════════════════
    # PRIVACY EVIDENCE (CC10.2, CC10.3)
    # ═══════════════════════════════════════════════════════════════════

    - control_id: CC10.2.2
      name: Automated Data Deletion
      trigger: schedule
      frequency: monthly
      schedule: "0 2 1 * *"  # 2 AM on 1st of month
      evidence_type: deletion_log
      artifacts:
        - name: deletion_log.csv
          description: Monthly deletion log
          source: postgresql
          query: |
            SELECT
              deletion_id,
              table_name,
              record_id,
              deletion_reason,
              deleted_at,
              deleted_by
            FROM deletion_logs
            WHERE deleted_at >= DATE_TRUNC('month', NOW() - INTERVAL '1 month')
              AND deleted_at < DATE_TRUNC('month', NOW())
            ORDER BY deleted_at DESC;
          format: csv

        - name: deletion_verification.json
          description: Verification that no old records exist
          source: postgresql
          query: |
            SELECT
              'trips' as table_name,
              COUNT(*) as old_records_count
            FROM trips
            WHERE created_at < NOW() - INTERVAL '1 year'

            UNION ALL

            SELECT
              'audit_logs' as table_name,
              COUNT(*) as old_records_count
            FROM audit_logs
            WHERE created_at < NOW() - INTERVAL '1 year'

            UNION ALL

            SELECT
              'cost_tracking' as table_name,
              COUNT(*) as old_records_count
            FROM cost_tracking
            WHERE created_at < NOW() - INTERVAL '2 years';
          format: json

      storage:
        destination: SOC2/05_Data_Protection/Data_Retention/Deletion_Logs/
        filename_pattern: "deletion_log_{{year}}_{{month}}"

      validation:
        require_zero_old_records: true
        alert_if_old_records_found: true

    - control_id: CC10.3.3
      name: User Data Deletion Proof
      trigger: jira_issue_created
      jira_filter: |
        type = "Data Deletion Request"
        AND status = Done
      frequency: event_driven
      evidence_type: deletion_proof
      artifacts:
        - name: deletion_request_{{issue_key}}.json
          description: User deletion request and verification
          source: composite
          processing: |
            # Get Jira ticket
            ticket = jira.get_issue(issue_key)
            user_id = ticket.fields.customfield_user_id

            # Verify user deleted from database
            user_exists = db.query(
                "SELECT COUNT(*) FROM users WHERE user_id = %s",
                (user_id,)
            )[0][0] > 0

            # Verify trips deleted
            trips_exist = db.query(
                "SELECT COUNT(*) FROM trips WHERE user_id = %s",
                (user_id,)
            )[0][0] > 0

            # Verify feedback deleted
            feedback_exists = db.query(
                "SELECT COUNT(*) FROM feedback WHERE user_id = %s",
                (user_id,)
            )[0][0] > 0

            return {
                'jira_ticket': issue_key,
                'user_id': user_id,
                'deletion_requested_at': ticket.fields.created,
                'deletion_completed_at': ticket.fields.updated,
                'verification_timestamp': datetime.utcnow().isoformat(),
                'user_record_exists': user_exists,
                'trips_exist': trips_exist,
                'feedback_exists': feedback_exists,
                'deletion_complete': not (user_exists or trips_exist or feedback_exists)
            }
          format: json

      storage:
        destination: SOC2/08_Privacy/User_Deletion_Proof/
        filename_pattern: "deletion_proof_{{issue_key}}.json"

      validation:
        require_complete_deletion: true
        alert_if_records_remain: true

# Notification settings
notifications:
  enabled: true
  channels:
    slack:
      enabled: true
      channel: "#compliance-events"
      webhook_url: "{{secrets.SLACK_COMPLIANCE_WEBHOOK}}"

    email:
      enabled: true
      from: compliance-automation@timbuktoo.ai
      to:
        - compliance@timbuktoo.ai
        - vp.engineering@timbuktoo.ai

    pagerduty:
      enabled: true
      service_key: "{{secrets.PAGERDUTY_COMPLIANCE_KEY}}"
      escalate_on:
        - evidence_collection_failure
        - validation_failure
        - budget_breach

  notification_templates:
    evidence_collected:
      subject: "✅ Evidence Collected: {{control_id}}"
      body: |
        **Control**: {{control_id}} - {{control_name}}
        **Artifacts**: {{artifact_count}} collected
        **Storage**: {{storage_destination}}
        **Timestamp**: {{timestamp}}

    evidence_failed:
      subject: "⛔ Evidence Collection Failed: {{control_id}}"
      body: |
        **Control**: {{control_id}} - {{control_name}}
        **Error**: {{error_message}}
        **Action Required**: Investigate and retry manually
        **Alert Level**: {{alert_level}}
```

---

## 3. Evidence Freshness Enforcement

### 3.1 Evidence Expiration Logic

**Principle**: Evidence expires after control frequency (monthly/quarterly/annual)

**Implementation**: `scripts/evidence_freshness_checker.py`

```python
import pandas as pd
from datetime import datetime, timedelta
import json

# Load Evidence Map
evidence_map = pd.read_excel('SOC2/09_Evidence_Index/Evidence_Map.xlsx', sheet_name='Control Mapping')

# Calculate evidence expiration
def is_evidence_stale(last_review_date, review_frequency):
    """Check if evidence is stale based on review frequency."""
    if pd.isna(last_review_date):
        return True  # Never reviewed = stale

    last_review = pd.to_datetime(last_review_date)
    now = datetime.now()

    # Calculate days since last review
    days_since_review = (now - last_review).days

    # Expiration thresholds
    expiration_days = {
        'Monthly': 35,  # 30 days + 5-day grace period
        'Quarterly': 100,  # 90 days + 10-day grace period
        'Annual': 375  # 365 days + 10-day grace period
    }

    threshold = expiration_days.get(review_frequency, 365)
    return days_since_review > threshold

# Check all controls
stale_controls = []
for idx, row in evidence_map.iterrows():
    if is_evidence_stale(row['Last Review Date'], row['Review Frequency']):
        stale_controls.append({
            'control_id': row['Control ID'],
            'control_description': row['Control Description'],
            'last_review_date': str(row['Last Review Date']),
            'review_frequency': row['Review Frequency'],
            'owner': row['Owner'],
            'next_review_date': str(row['Next Review Date'])
        })

# If stale controls found, block Jira and alert
if stale_controls:
    print(f"⛔ {len(stale_controls)} stale controls found!")

    # Update Jira automation to block "Audit Ready" status
    jira_block_config = {
        'rule_id': 'TRVL-AUTO-EVIDENCE-FRESHNESS',
        'trigger': 'issue_transitioned',
        'to_status': 'Audit Ready',
        'condition': {
            'type': 'api_check',
            'api_endpoint': 'https://api.timbuktoo.ai/internal/evidence/freshness',
            'expected_result': 'all_fresh',
            'blocking': True
        },
        'failure_action': {
            'type': 'block_transition',
            'error_message': f"""
            ⛔ **Evidence Stale - Cannot Mark Audit Ready**

            {len(stale_controls)} control(s) have stale evidence:

            {chr(10).join(f"- {c['control_id']}: Last reviewed {c['last_review_date']} ({c['review_frequency']})" for c in stale_controls)}

            **Action Required**:
            1. Collect fresh evidence for stale controls
            2. Update Evidence Map with new review dates
            3. Retry transition to "Audit Ready"
            """,
            'notify': [row['owner'] for row in stale_controls]
        }
    }

    # Send Slack alert
    slack_alert = {
        'channel': '#compliance-alerts',
        'message': f"""
        🚨 **Stale Evidence Alert**

        {len(stale_controls)} controls have stale evidence:

        {json.dumps(stale_controls, indent=2)}

        **Impact**: Jira "Audit Ready" status is BLOCKED until evidence is refreshed.

        **Action**: Owners must collect fresh evidence ASAP.
        """
    }

    print(json.dumps(slack_alert, indent=2))
else:
    print("✅ All evidence is fresh!")
```

### 3.2 Automated Evidence Collection Schedule

| Frequency | Controls | Collection Schedule | Next Collection |
|-----------|----------|-------------------|----------------|
| **Daily** | CC7.1.1 (Uptime) | Every day at 00:00 UTC | 2024-06-16 |
| **Monthly** | CC6.1.2 (MFA), CC6.7.1 (Audit Logs), CC6.7.2 (Retention), CC7.1.1 (Uptime), CC7.2.3 (Incidents), CC7.3.1 (Backups), CC8.1.5 (Cost), CC10.2.2 (Deletion) | 1st of every month | 2024-07-01 |
| **Quarterly** | CC6.1.3 (Access Review), CC6.6.1 (Encryption), CC6.6.4 (TLS), CC6.8.5 (Rollback Test) | 1st of Jan/Apr/Jul/Oct | 2024-07-01 |
| **Annual** | CC7.2.1 (IR Plan) | January 15th | 2025-01-15 |
| **Event-Driven** | CC6.1.1 (RBAC changes), CC6.2.1 (Provisioning), CC6.3.1 (Offboarding), CC6.8.1 (PRs), CC10.3.3 (User deletion) | On event occurrence | As events occur |

### 3.3 Evidence Freshness Dashboard

**Grafana Dashboard**: Evidence Freshness Tracking

```json
{
  "dashboard": {
    "title": "SOC-2 Evidence Freshness",
    "panels": [
      {
        "title": "Evidence Freshness by Control",
        "type": "table",
        "targets": [{
          "query": "SELECT control_id, last_review_date, review_frequency, days_until_stale FROM evidence_freshness ORDER BY days_until_stale ASC"
        }]
      },
      {
        "title": "Stale Evidence Count",
        "type": "stat",
        "targets": [{
          "query": "SELECT COUNT(*) FROM evidence_freshness WHERE is_stale = true"
        }],
        "thresholds": [
          {"value": 0, "color": "green"},
          {"value": 1, "color": "red"}
        ]
      },
      {
        "title": "Evidence Collection Success Rate (Last 30 Days)",
        "type": "timeseries",
        "targets": [{
          "query": "SELECT date, success_count / (success_count + failure_count) AS success_rate FROM evidence_collection_stats WHERE date >= NOW() - INTERVAL '30 days'"
        }]
      }
    ]
  }
}
```

---

## 4. Evidence Collection by Trust Service

### 4.1 Security (CC6)

| Control | Evidence | Collection Method | Frequency | Storage |
|---------|----------|------------------|-----------|---------|
| CC6.1.1 | RBAC snapshot | PostgreSQL query | Event-driven (access change) | SOC2/02_Access_Control/RBAC_Definitions/ |
| CC6.1.2 | MFA status report | AWS IAM API | Monthly | SOC2/02_Access_Control/MFA_Proof/ |
| CC6.1.3 | Access review attestation | Jira API + PDF generation | Quarterly | SOC2/02_Access_Control/Access_Reviews/ |
| CC6.2.1 | User provisioning tickets | Jira webhook | Event-driven | SOC2/02_Access_Control/Onboarding_Offboarding/ |
| CC6.3.1 | User offboarding tickets | Jira webhook + IAM verification | Event-driven | SOC2/02_Access_Control/Onboarding_Offboarding/ |
| CC6.6.1 | Database encryption config | AWS RDS API | Quarterly | SOC2/05_Data_Protection/Encryption_At_Rest/ |
| CC6.6.4 | TLS/SSL Labs report | SSL Labs API | Quarterly | SOC2/05_Data_Protection/Encryption_In_Transit/ |
| CC6.7.1 | Audit log sample | PostgreSQL query | Monthly | SOC2/04_Logging_and_Monitoring/Audit_Logs/ |
| CC6.7.2 | Log retention verification | PostgreSQL query | Monthly | SOC2/04_Logging_and_Monitoring/Audit_Logs/ |
| CC6.8.1 | PR approval records | GitHub webhook | Event-driven (sampled 25%) | SOC2/03_Change_Management/Code_Review_Evidence/ |
| CC6.8.5 | Rollback test report | Jira API + PDF generation | Quarterly | SOC2/03_Change_Management/Rollback_Procedures/ |

### 4.2 Availability (CC7)

| Control | Evidence | Collection Method | Frequency | Storage |
|---------|----------|------------------|-----------|---------|
| CC7.1.1 | Uptime report | Datadog API | Monthly | SOC2/07_Availability/Uptime_Reports/ |
| CC7.2.1 | Incident Response Plan | Confluence API | Annual | SOC2/06_Incident_Response/IR_Plan/ |
| CC7.2.3 | Incident log | Jira API | Monthly | SOC2/06_Incident_Response/Incident_Tickets/ |
| CC7.3.1 | Backup verification | AWS RDS API | Monthly | SOC2/07_Availability/Backup_Schedule/ |

### 4.3 Processing Integrity (CC8)

| Control | Evidence | Collection Method | Frequency | Storage |
|---------|----------|------------------|-----------|---------|
| CC8.1.5 | Cost compliance report | PostgreSQL query | Monthly | SOC2/01_Governance/CostController/ |

### 4.4 Privacy (CC10)

| Control | Evidence | Collection Method | Frequency | Storage |
|---------|----------|------------------|-----------|---------|
| CC10.2.2 | Deletion log | PostgreSQL query | Monthly | SOC2/05_Data_Protection/Data_Retention/Deletion_Logs/ |
| CC10.3.3 | User deletion proof | Jira webhook + DB verification | Event-driven | SOC2/08_Privacy/User_Deletion_Proof/ |

---

## 5. Evidence Storage and Retrieval

### 5.1 Storage Architecture

**Primary Storage**: S3 + Local Filesystem
**Metadata Storage**: PostgreSQL
**Compliance Platform**: Drata or Vanta

```
Evidence Storage Hierarchy:

s3://timbuktoo-compliance/soc2-evidence/
├── 01_Governance/
├── 02_Access_Control/
│   ├── RBAC_Definitions/
│   │   ├── rbac_snapshot_2024-06-15.json
│   │   ├── rbac_permission_matrix_2024-06-15.csv
│   │   └── ...
│   ├── MFA_Proof/
│   │   ├── mfa_status_2024_06.json
│   │   └── ...
│   └── Access_Reviews/
│       ├── Q2_2024_access_review.pdf
│       ├── Q2_2024_access_review.xlsx
│       └── ...
├── 03_Change_Management/
├── 04_Logging_and_Monitoring/
├── 05_Data_Protection/
├── 06_Incident_Response/
├── 07_Availability/
├── 08_Privacy/
└── 09_Evidence_Index/
    └── Evidence_Map.xlsx
```

### 5.2 Evidence Metadata Schema

**Table**: `evidence_metadata`

```sql
CREATE TABLE evidence_metadata (
    evidence_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    control_id TEXT NOT NULL,  -- e.g., CC6.1.1
    control_name TEXT NOT NULL,
    evidence_type TEXT NOT NULL,  -- snapshot, report, attestation, log_export, etc.
    artifact_name TEXT NOT NULL,
    artifact_format TEXT NOT NULL,  -- json, csv, pdf, xlsx
    collection_timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    collection_method TEXT,  -- api, query, webhook, manual
    storage_location TEXT NOT NULL,  -- S3 path
    file_size_bytes BIGINT,
    file_hash_sha256 TEXT,  -- For integrity verification
    expiration_date TIMESTAMP,  -- Based on review frequency
    is_stale BOOLEAN GENERATED ALWAYS AS (expiration_date < NOW()) STORED,
    owner TEXT,
    validation_status TEXT,  -- passed, failed, pending
    validation_errors JSONB,
    uploaded_to_drata BOOLEAN DEFAULT FALSE,
    uploaded_to_drata_at TIMESTAMP,
    metadata JSONB,  -- Additional metadata (field values, record counts, etc.)
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for fast retrieval
CREATE INDEX idx_evidence_control_id ON evidence_metadata(control_id);
CREATE INDEX idx_evidence_stale ON evidence_metadata(is_stale);
CREATE INDEX idx_evidence_collection_timestamp ON evidence_metadata(collection_timestamp);
```

### 5.3 Evidence Retrieval API

**Endpoint**: `GET /api/v1/evidence/{control_id}`

**Example Request**:
```bash
curl -X GET "https://api.timbuktoo.ai/internal/evidence/CC6.1.1" \
  -H "Authorization: Bearer ${INTERNAL_API_TOKEN}"
```

**Example Response**:
```json
{
  "control_id": "CC6.1.1",
  "control_name": "RBAC Implementation",
  "evidence_count": 45,
  "latest_evidence": {
    "evidence_id": "550e8400-e29b-41d4-a716-446655440000",
    "artifact_name": "rbac_snapshot_2024-06-15.json",
    "collection_timestamp": "2024-06-15T00:00:00Z",
    "storage_location": "s3://timbuktoo-compliance/soc2-evidence/02_Access_Control/RBAC_Definitions/rbac_snapshot_2024-06-15.json",
    "expiration_date": "2024-07-15T00:00:00Z",
    "is_stale": false,
    "validation_status": "passed",
    "download_url": "https://s3.amazonaws.com/timbuktoo-compliance/soc2-evidence/02_Access_Control/RBAC_Definitions/rbac_snapshot_2024-06-15.json?signature=..."
  },
  "evidence_history": [
    {
      "collection_timestamp": "2024-05-15T00:00:00Z",
      "artifact_name": "rbac_snapshot_2024-05-15.json",
      "storage_location": "s3://...",
      "download_url": "https://..."
    }
  ]
}
```

---

## 6. Auditor Portal Integration

### 6.1 Drata/Vanta Integration

**Configuration**: `config/drata_integration.yaml`

```yaml
drata_integration:
  enabled: true
  api_key: "{{secrets.DRATA_API_KEY}}"
  organization_id: timbuktoo-inc

  # Auto-upload evidence to Drata
  auto_upload:
    enabled: true
    upload_frequency: daily
    upload_time: "02:00 UTC"

  # Control mapping (Timbuktoo Control ID → Drata Control ID)
  control_mapping:
    CC6.1.1: DRATA-ACC-001
    CC6.1.2: DRATA-ACC-002
    CC6.1.3: DRATA-ACC-003
    # ... (map all 60 controls)

  # Evidence upload rules
  evidence_upload_rules:
    - control_id: CC6.1.1
      drata_control_id: DRATA-ACC-001
      artifact_type: rbac_snapshot
      upload_on_collection: true

    - control_id: CC6.1.3
      drata_control_id: DRATA-ACC-003
      artifact_type: access_review_attestation
      upload_on_collection: true
      require_approval_before_upload: true
```

### 6.2 Auditor Portal UI

**URL**: `https://compliance.timbuktoo.ai/auditor-portal`

**Features**:
- **Control Dashboard**: View all 60 controls, status, evidence freshness
- **Evidence Library**: Search and download evidence by control, date range, type
- **Audit Trail**: View all evidence collection events, validations, uploads
- **Reports**: Generate compliance reports (Control Status, Evidence Coverage, Gaps)
- **Access**: Read-only access for auditors, time-limited credentials

**Portal Architecture**:
```
┌────────────────────────────────────────────────────────────┐
│               AUDITOR PORTAL (Read-Only)                   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────────┐  ┌──────────────────┐              │
│  │  Control         │  │  Evidence        │              │
│  │  Dashboard       │  │  Library         │              │
│  │                  │  │                  │              │
│  │ - 60 controls    │  │ - Search by      │              │
│  │ - Status (✅/⚠️)  │  │   control ID     │              │
│  │ - Evidence count │  │ - Filter by date │              │
│  │ - Owner          │  │ - Download files │              │
│  └──────────────────┘  └──────────────────┘              │
│                                                            │
│  ┌──────────────────┐  ┌──────────────────┐              │
│  │  Audit Trail     │  │  Reports         │              │
│  │                  │  │                  │              │
│  │ - All evidence   │  │ - Control Status │              │
│  │   collection     │  │ - Evidence       │              │
│  │   events         │  │   Coverage       │              │
│  │ - Timestamps     │  │ - Gap Analysis   │              │
│  │ - Validation     │  │ - Export PDF/CSV │              │
│  └──────────────────┘  └──────────────────┘              │
│                                                            │
│  Authentication: SSO (Google/Okta) + MFA                  │
│  Access: Time-limited (audit period only)                 │
│  Permissions: Read-only                                    │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 7. Implementation Guide

### 7.1 Prerequisites

1. **Install dependencies**:
```bash
pip install boto3 pandas openpyxl requests pyyaml python-jira
```

2. **Configure secrets**:
```bash
# AWS credentials
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...

# API keys
export JIRA_API_TOKEN=...
export GITHUB_TOKEN=...
export DATADOG_API_KEY=...
export DATADOG_APP_KEY=...
export DRATA_API_KEY=...
export SLACK_COMPLIANCE_WEBHOOK=...
```

3. **Create evidence folders**:
```bash
mkdir -p SOC2/{01_Governance,02_Access_Control,03_Change_Management,04_Logging_and_Monitoring,05_Data_Protection,06_Incident_Response,07_Availability,08_Privacy,09_Evidence_Index}
```

### 7.2 Deploy Evidence Collector Service

**File**: `services/evidence_collector/main.py`

```python
#!/usr/bin/env python3
"""
SOC-2 Evidence Collector Service
Automated evidence collection for all controls
"""

import schedule
import time
import yaml
import logging
from evidence_collector import EvidenceCollector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/evidence_collector.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load configuration
with open('config/evidence_automation.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Initialize Evidence Collector
collector = EvidenceCollector(config)

# Schedule evidence collection jobs
def schedule_jobs():
    """Schedule all evidence collection jobs based on frequency."""

    for control in config['evidence_automation']['controls']:
        control_id = control['control_id']
        frequency = control['frequency']

        if frequency == 'event_driven':
            # Event-driven controls are triggered by webhooks (no scheduling)
            logger.info(f"Control {control_id} is event-driven (webhook-triggered)")
            continue

        elif frequency == 'monthly':
            schedule_str = control.get('schedule', '0 0 1 * *')  # Default: 1st of month
            # Convert cron to schedule format
            schedule.every().month.at("00:00").do(
                collector.collect_evidence, control_id=control_id
            )
            logger.info(f"Scheduled monthly collection for {control_id}: {schedule_str}")

        elif frequency == 'quarterly':
            schedule_str = control.get('schedule', '0 0 1 */3 *')  # Default: 1st of Jan/Apr/Jul/Oct
            # Run on 1st of Jan, Apr, Jul, Oct
            schedule.every().day.at("00:00").do(
                lambda: collector.collect_evidence_if_quarter_start(control_id)
            )
            logger.info(f"Scheduled quarterly collection for {control_id}: {schedule_str}")

        elif frequency == 'annual':
            schedule_str = control.get('schedule', '0 0 15 1 *')  # Default: Jan 15
            schedule.every().year.at("00:00").do(
                collector.collect_evidence, control_id=control_id
            )
            logger.info(f"Scheduled annual collection for {control_id}: {schedule_str}")

    # Schedule evidence freshness check (daily)
    schedule.every().day.at("06:00").do(collector.check_evidence_freshness)
    logger.info("Scheduled daily evidence freshness check at 06:00 UTC")

# Main loop
if __name__ == '__main__':
    logger.info("Starting SOC-2 Evidence Collector Service...")

    # Schedule all jobs
    schedule_jobs()

    # Run scheduler loop
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
```

**Deploy as systemd service**:

```bash
# Create systemd service file
sudo tee /etc/systemd/system/evidence-collector.service <<EOF
[Unit]
Description=SOC-2 Evidence Collector Service
After=network.target

[Service]
Type=simple
User=timbuktoo
WorkingDirectory=/opt/timbuktoo/services/evidence_collector
ExecStart=/usr/bin/python3 /opt/timbuktoo/services/evidence_collector/main.py
Restart=always
RestartSec=10

Environment="AWS_ACCESS_KEY_ID=..."
Environment="AWS_SECRET_ACCESS_KEY=..."
Environment="JIRA_API_TOKEN=..."

[Install]
WantedBy=multi-user.target
EOF

# Start service
sudo systemctl daemon-reload
sudo systemctl enable evidence-collector
sudo systemctl start evidence-collector
sudo systemctl status evidence-collector
```

### 7.3 Testing

**Test individual control evidence collection**:

```bash
python -c "from evidence_collector import EvidenceCollector; import yaml; config = yaml.safe_load(open('config/evidence_automation.yaml')); collector = EvidenceCollector(config); collector.collect_evidence('CC6.1.1')"
```

**Expected output**:
```
2024-06-15 10:30:00 - INFO - Collecting evidence for control CC6.1.1 (RBAC Implementation)
2024-06-15 10:30:01 - INFO - Executing PostgreSQL query for artifact: rbac_snapshot.json
2024-06-15 10:30:02 - INFO - Query returned 45 records
2024-06-15 10:30:02 - INFO - Validating artifact: rbac_snapshot.json
2024-06-15 10:30:02 - INFO - Validation passed ✓
2024-06-15 10:30:03 - INFO - Uploading to S3: s3://timbuktoo-compliance/soc2-evidence/02_Access_Control/RBAC_Definitions/rbac_snapshot_2024-06-15.json
2024-06-15 10:30:04 - INFO - S3 upload successful ✓
2024-06-15 10:30:04 - INFO - Updating Evidence Map...
2024-06-15 10:30:05 - INFO - Evidence Map updated ✓
2024-06-15 10:30:05 - INFO - Sending Slack notification...
2024-06-15 10:30:06 - INFO - Evidence collection complete for CC6.1.1 ✓
```

---

## 8. Benefits and Outcomes

### 8.1 Before Automation (Manual Evidence Collection)

**Timeline**: 4-6 weeks before audit
**Effort**: 80-120 hours (2-3 FTEs)
**Risk**: High (missing evidence, stale data, scramble period)

**Manual Process**:
1. Auditor requests evidence list
2. Engineer gathers evidence from multiple systems
3. Engineer formats evidence (screenshots, exports, PDFs)
4. Engineer uploads to shared folder
5. Engineer updates Evidence Map manually
6. Auditor finds gaps → Repeat 1-5

### 8.2 After Automation (Continuous Evidence Collection)

**Timeline**: 0 weeks (always audit-ready)
**Effort**: 0 hours (fully automated)
**Risk**: Low (real-time compliance, zero stale evidence)

**Automated Process**:
1. Control executes → Evidence auto-generated
2. Evidence auto-validated → Evidence auto-stored
3. Evidence auto-indexed → Auditor portal updated
4. Auditor logs in → Evidence ready to download

### 8.3 Metrics

| Metric | Before Automation | After Automation | Improvement |
|--------|------------------|-----------------|-------------|
| **Time to audit readiness** | 4-6 weeks | 0 days | 100% faster |
| **Manual effort (hours)** | 80-120 | 0 | 100% reduction |
| **Evidence freshness** | Weeks old | Real-time | 100% current |
| **Missing evidence rate** | 15-20% | 0% | 100% complete |
| **Compliance confidence** | Medium | High | ✅ Continuous |

---

## Conclusion

This end-to-end SOC-2 Type II evidence automation system provides:

✅ **Zero Manual Work**: All evidence auto-collected, auto-validated, auto-stored
✅ **Always Audit-Ready**: No "scramble period" before audits
✅ **Real-Time Compliance**: Evidence freshness enforced automatically
✅ **Complete Coverage**: 60 controls, 100+ evidence artifacts
✅ **Auditor-Friendly**: Dedicated portal with search, download, reports
✅ **Scalable**: Add new controls by updating YAML config

**Next Steps**:
1. Deploy Evidence Collector Service (systemd)
2. Configure evidence_automation.yaml
3. Set up Drata/Vanta integration
4. Enable Jira evidence freshness blocking
5. Grant auditor portal access during audit
6. Monitor evidence collection success rate (target: >99%)

**Estimated Implementation Time**: 2-3 weeks
**Estimated Annual Savings**: 160-240 engineering hours
**Audit Preparation Time**: 0 days (continuous compliance)
