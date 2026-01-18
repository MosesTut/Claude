# Jira Automation Rules - SOC-2 & Agent-Specific (Comprehensive)
## Timbuktoo Travel Concierge

**Purpose**: Automated compliance tracking, agent change control, and incident management
**Project Key**: TRVL
**Integration**: Slack, GitHub, PagerDuty, SOC-2 evidence repository

---

## Rule 1: SOC-2 Evidence Tracking (Comprehensive)

### Overview
**Trigger**: Issue transitioned to "Ready for Audit"
**Condition**: Issue type = Compliance
**Purpose**: Automate SOC-2 evidence collection, tracking, and audit preparation

### Detailed Configuration

**Rule ID**: `TRVL-AUTO-001`
**Priority**: Critical
**Execution**: Synchronous
**Retry Logic**: Up to 3 attempts with exponential backoff

### Trigger Configuration
```yaml
trigger:
  type: issue_transitioned
  to_status:
    - "Ready for Audit"
    - "Audit Pending"
  conditions:
    issue_type: [Compliance, Security, Data Protection]
    project: TRVL
```

### Conditions (All Must Pass)
```yaml
conditions:
  - type: issue_type
    operator: equals
    value: Compliance

  - type: custom_field_not_empty
    field: SOC-2 Control ID
    error_message: "SOC-2 Control ID required before audit preparation"

  - type: custom_field_not_empty
    field: Evidence Location
    error_message: "Evidence Location path required"

  - type: assignee_not_empty
    error_message: "Control Owner must be assigned"
```

### Actions (Sequential Execution)

#### Action 1: Add SOC-2 Evidence Label
```yaml
action: add_label
labels:
  - soc2-evidence
  - audit-ready
  - "{{issue.customField.trustServiceCriteria}}"  # e.g., "security-cc6", "availability-cc7"
```

#### Action 2: Set Evidence Status Custom Field
```yaml
action: set_custom_field
field: Evidence Status
value: Pending Collection
allowed_values:
  - Pending Collection
  - Collection In Progress
  - Collected
  - Verified
  - Audit Approved
```

#### Action 3: Create Evidence Upload Sub-Task
```yaml
action: create_subtask
subtask_config:
  summary: "Upload Evidence for {{issue.key}} - {{issue.customField.controlID}}"
  description: |
    **SOC-2 Control**: {{issue.customField.controlID}}
    **Control Description**: {{issue.customField.controlDescription}}
    **Evidence Required**: {{issue.customField.evidenceRequired}}
    **Evidence Location**: `SOC2/{{issue.customField.evidenceLocation}}`

    ## Evidence Collection Checklist
    - [ ] Gather evidence files (screenshots, configs, code, logs)
    - [ ] Verify evidence completeness
    - [ ] Upload to `SOC2/{{issue.customField.evidenceLocation}}/`
    - [ ] Update Evidence Map spreadsheet
    - [ ] Link evidence files in this ticket
    - [ ] Request peer review
    - [ ] Mark as "Collected" in Evidence Status field

    ## Evidence Quality Standards
    - Source code: Include Git commit SHA
    - Screenshots: Timestamp + URL in metadata
    - Logs: Minimum 30-day export
    - Configs: Redact secrets, include validation proof
    - Signed docs: Include e-signature verification link

    **Due Date**: {{issue.dueDate}} (7 days from now)
    **Owner**: {{issue.assignee}} (Control Owner)

  assignee: "{{issue.assignee}}"
  due_date: "+7d"
  priority: "{{issue.priority}}"
  labels:
    - evidence-upload
    - "{{issue.customField.controlID}}"
```

#### Action 4: Set Parent Issue Due Date (if not set)
```yaml
action: set_due_date
condition: due_date_is_empty
days_from_now: 14
comment: "Auto-set due date to 14 days for audit evidence collection"
```

#### Action 5: Send Slack Notification to #compliance-events
```yaml
action: send_slack_message
channel: "#compliance-events"
message: |
  🔍 **SOC-2 Evidence Collection Started**

  **Control**: {{issue.customField.controlID}} - {{issue.summary}}
  **Trust Principle**: {{issue.customField.trustServiceCriteria}}
  **Owner**: {{issue.assignee}}
  **Due Date**: {{issue.dueDate}}

  **Evidence Location**: `SOC2/{{issue.customField.evidenceLocation}}/`

  **Sub-task Created**: {{subtask.key}} (Evidence Upload)

  [View Issue]({{issue.url}}) | [Evidence Checklist]({{subtask.url}})
attachments:
  - color: "#36a64f"
    fields:
      - title: "Control ID"
        value: "{{issue.customField.controlID}}"
        short: true
      - title: "Owner"
        value: "{{issue.assignee}}"
        short: true
      - title: "Status"
        value: "Pending Collection"
        short: true
      - title: "Due"
        value: "{{issue.dueDate}}"
        short: true
```

#### Action 6: Update Evidence Map Spreadsheet (API Call)
```yaml
action: custom_api_call
api_config:
  method: POST
  url: "https://api.timbuktoo.ai/internal/evidence-map/update"
  headers:
    Authorization: "Bearer {{secrets.INTERNAL_API_TOKEN}}"
    Content-Type: "application/json"
  body:
    control_id: "{{issue.customField.controlID}}"
    jira_issue_key: "{{issue.key}}"
    status: "Pending Collection"
    owner: "{{issue.assignee.email}}"
    evidence_location: "SOC2/{{issue.customField.evidenceLocation}}/"
    last_updated: "{{now}}"
  retry: 3
  timeout_seconds: 10
```

#### Action 7: Create Reminder Automation (3 days before due)
```yaml
action: schedule_reminder
schedule:
  days_before_due: 3
reminder_action:
  type: send_slack_dm
  user: "{{issue.assignee}}"
  message: |
    ⏰ **Evidence Collection Reminder**

    Your SOC-2 evidence for control {{issue.customField.controlID}} is due in 3 days.

    **Issue**: {{issue.key}} - {{issue.summary}}
    **Due Date**: {{issue.dueDate}}
    **Status**: {{issue.customField.evidenceStatus}}

    [View Issue]({{issue.url}}) | [Evidence Upload Task]({{subtask.url}})
```

### Error Handling
```yaml
error_handling:
  on_condition_failure:
    action: add_comment
    comment: |
      ❌ **Automation Failed**: Cannot transition to "Ready for Audit"

      **Missing Requirements**:
      {{error.missing_fields}}

      Please complete the following:
      - SOC-2 Control ID (required)
      - Evidence Location path (required)
      - Assign Control Owner (required)

      [See Evidence Map](https://timbuktoo.drata.com) for control details.

  on_action_failure:
    action: send_slack_message
    channel: "#compliance-alerts"
    message: "⚠️ SOC-2 automation failed for {{issue.key}}: {{error.message}}"
```

### Audit Trail
```yaml
audit_logging:
  enabled: true
  log_destination: SOC2/04_Logging_and_Monitoring/Automation_Logs/
  fields_logged:
    - issue_key
    - control_id
    - trigger_timestamp
    - actions_executed
    - assignee_email
    - evidence_location
    - subtask_created
  retention_days: 365
```

### Testing Checklist
- [ ] Create Compliance issue with SOC-2 Control ID
- [ ] Transition to "Ready for Audit"
- [ ] Verify label "soc2-evidence" added
- [ ] Verify Evidence Status set to "Pending Collection"
- [ ] Verify sub-task created with correct owner and due date
- [ ] Verify Slack message sent to #compliance-events
- [ ] Verify Evidence Map API call succeeded
- [ ] Verify reminder scheduled (check 3 days before due date)

---

## Rule 2: Agent Change Risk Control (Comprehensive)

### Overview
**Trigger**: Pull Request merged OR Jira issue status = Done
**Condition**: Component = Agent Logic
**Purpose**: Enforce security review and change control for AI agent modifications

### Detailed Configuration

**Rule ID**: `TRVL-AUTO-002`
**Priority**: Critical
**Execution**: Synchronous (blocks deployment)
**Risk Level**: High (agent changes affect user-facing outputs)

### Trigger Configuration
```yaml
triggers:
  - type: github_webhook
    event: pull_request
    action: closed
    merged: true
    conditions:
      - files_changed_pattern: "timbuktoo/agents/**/*.py"

  - type: issue_transitioned
    to_status: Done
    conditions:
      - component: Agent Logic
      - labels_contains: [agent-change, prompt-update, model-update]
```

### Conditions (All Must Pass)

#### Condition 1: Component Validation
```yaml
condition: component_equals
value: Agent Logic
error_message: "This rule applies only to Agent Logic component"
```

#### Condition 2: Security Review Required
```yaml
condition: custom_field_equals
field: Security Review Status
value: [Approved, Not Required]
blocking: true
error_message: |
  ⛔ **Security Review Required**

  Agent logic changes require security approval before deployment.

  **Required Actions**:
  1. Request security review from @security.lead
  2. Complete security checklist:
     - [ ] No PII in prompts
     - [ ] Input validation present
     - [ ] Output sanitization present
     - [ ] Cost controls enforced
     - [ ] Error handling tested
  3. Update "Security Review Status" to "Approved"

  **Reviewer**: @security.lead@timbuktoo.ai
```

#### Condition 3: Test Coverage Check
```yaml
condition: github_pr_check
check_name: "codecov/patch"
status: success
min_coverage: 80
blocking: true
error_message: |
  ⛔ **Insufficient Test Coverage**

  Agent changes require ≥80% test coverage.

  **Current Coverage**: {{github.pr.coverage.patch}}%
  **Required**: 80%

  Add tests before merging.
```

#### Condition 4: A/B Test Impact Assessment
```yaml
condition: custom_field_not_empty
field: A/B Test Impact
allowed_values:
  - No Impact (non-variant change)
  - Affects Control Variant
  - Affects Slow Hidden Gems Variant
  - Affects Both Variants
blocking: true
error_message: "Assess A/B test impact before deploying agent changes"
```

### Actions (Sequential Execution)

#### Action 1: Require Security Lead Approval
```yaml
action: require_approval
approvers:
  - email: security.lead@timbuktoo.ai
    role: Security Lead
    required: true
    timeout_hours: 24
approval_message: |
  🔐 **Security Review Required**

  **Change Type**: Agent Logic Modification
  **Issue**: {{issue.key}} - {{issue.summary}}
  **Component**: {{issue.component}}
  **Files Changed**: {{github.pr.files_changed_count}}

  **Security Checklist**:
  - [ ] No PII in LLM prompts
  - [ ] Input validation enforced
  - [ ] Output sanitization present
  - [ ] Cost controls not bypassed
  - [ ] Error handling comprehensive
  - [ ] Rollback plan documented

  **PR**: {{github.pr.url}}
  **Jira Issue**: {{issue.url}}

  **Approve or Reject**: [Approval Link]({{approval.url}})

  **Note**: Deployment blocked until approved.

rejection_action:
  - transition_issue: "In Progress"
  - add_comment: "Security review rejected. Address findings before re-submitting."
  - send_slack_message:
      channel: "#agent-changes"
      message: "⛔ Security review rejected for {{issue.key}}: {{rejection.reason}}"
```

#### Action 2: Log Change Event to SOC-2 Evidence
```yaml
action: write_file
destination: SOC2/03_Change_Management/Agent_Changes_Log.csv
format: csv_append
content:
  timestamp: "{{now}}"
  issue_key: "{{issue.key}}"
  pr_number: "{{github.pr.number}}"
  pr_url: "{{github.pr.url}}"
  agent_type: "{{issue.customField.agentType}}"  # City Selection, Local Expert, Concierge
  change_description: "{{issue.summary}}"
  files_changed: "{{github.pr.files_changed}}"
  lines_added: "{{github.pr.additions}}"
  lines_removed: "{{github.pr.deletions}}"
  security_reviewer: "{{approval.approver}}"
  approval_timestamp: "{{approval.timestamp}}"
  deployed_by: "{{github.pr.merged_by}}"
  deployment_timestamp: "{{github.pr.merged_at}}"
  rollback_plan_link: "{{issue.customField.rollbackPlanUrl}}"
  ab_test_impact: "{{issue.customField.abTestImpact}}"
```

#### Action 3: Post Slack Alert to #compliance-events
```yaml
action: send_slack_message
channel: "#compliance-events"
message: |
  🤖 **Agent Logic Change Deployed**

  **Agent**: {{issue.customField.agentType}}
  **Change**: {{issue.summary}}
  **Jira**: {{issue.key}}
  **PR**: {{github.pr.url}}

  **Security Review**: ✅ Approved by {{approval.approver}}
  **Test Coverage**: {{github.pr.coverage.patch}}%
  **A/B Test Impact**: {{issue.customField.abTestImpact}}

  **Deployment**:
  - Merged by: {{github.pr.merged_by}}
  - Timestamp: {{github.pr.merged_at}}
  - Rollback Plan: {{issue.customField.rollbackPlanUrl}}

  **Change Log**: `SOC2/03_Change_Management/Agent_Changes_Log.csv`
attachments:
  - color: "#FF9800"  # Orange for agent changes
    fields:
      - title: "Agent Type"
        value: "{{issue.customField.agentType}}"
        short: true
      - title: "Security Reviewer"
        value: "{{approval.approver}}"
        short: true
      - title: "Files Changed"
        value: "{{github.pr.files_changed_count}}"
        short: true
      - title: "Coverage"
        value: "{{github.pr.coverage.patch}}%"
        short: true
```

#### Action 4: Create Post-Deployment Monitoring Task
```yaml
action: create_followup_task
task_config:
  summary: "Post-Deployment Monitoring: {{issue.key}} ({{issue.customField.agentType}})"
  description: |
    Monitor agent performance after deployment for 48 hours.

    **Deployed Change**: {{issue.summary}}
    **Agent**: {{issue.customField.agentType}}
    **Deployment Time**: {{github.pr.merged_at}}

    ## Monitoring Checklist (48 hours)
    - [ ] Error rate < 1% (check Grafana dashboard)
    - [ ] Latency P95 < 90 seconds
    - [ ] Cost per trip within $0.35-$0.50 range
    - [ ] No anomalous token usage spikes
    - [ ] A/B test variant split remains 50/50
    - [ ] No user complaints in feedback
    - [ ] Zero hallucination incidents reported

    ## Rollback Triggers
    - Error rate >5% for >5 minutes
    - Cost per trip >$0.70 consistently
    - User satisfaction rating drops >20%
    - Critical bug detected

    **Rollback Plan**: {{issue.customField.rollbackPlanUrl}}
    **Monitoring Dashboard**: https://grafana.timbuktoo.ai/d/agent-performance

  assignee: "{{github.pr.merged_by}}"
  due_date: "+2d"  # 48 hours
  priority: High
  labels:
    - post-deployment-monitoring
    - agent-change
    - "{{issue.customField.agentType}}"
```

#### Action 5: Update A/B Test Experiment Tracker (if applicable)
```yaml
action: conditional_api_call
condition: "{{issue.customField.abTestImpact != 'No Impact'}}"
api_config:
  method: POST
  url: "https://api.timbuktoo.ai/internal/ab-tests/record-change"
  body:
    issue_key: "{{issue.key}}"
    agent_type: "{{issue.customField.agentType}}"
    change_description: "{{issue.summary}}"
    variants_affected: "{{issue.customField.abTestImpact}}"
    deployment_timestamp: "{{github.pr.merged_at}}"
    monitoring_task: "{{followup_task.key}}"
  headers:
    Authorization: "Bearer {{secrets.INTERNAL_API_TOKEN}}"
```

#### Action 6: Add Compliance Documentation Link
```yaml
action: add_comment
comment: |
  ✅ **Agent Change Deployed Successfully**

  **Compliance Documentation**:
  - Change logged to: `SOC2/03_Change_Management/Agent_Changes_Log.csv`
  - Security review: Approved by {{approval.approver}}
  - Post-deployment monitoring: {{followup_task.key}} (48-hour watch)

  **Rollback Instructions**:
  1. Revert PR: {{github.pr.url}}
  2. Follow rollback plan: {{issue.customField.rollbackPlanUrl}}
  3. Notify #engineering and #compliance-events

  **Next Steps**:
  - Monitor {{followup_task.key}} for 48 hours
  - If issues detected, execute rollback immediately
  - Complete monitoring checklist before closing
```

### Error Handling
```yaml
error_handling:
  on_security_review_timeout:
    action: send_pagerduty_alert
    severity: high
    message: "Security review timeout for agent change {{issue.key}}"
    escalate_to: security.lead@timbuktoo.ai

  on_test_coverage_failure:
    action: block_merge
    message: "Test coverage below 80%. Add tests before merging."

  on_api_call_failure:
    action: log_error
    destination: SOC2/04_Logging_and_Monitoring/Automation_Errors.log
    continue: true  # Don't block deployment for logging failures
```

### Testing Checklist
- [ ] Create PR changing `timbuktoo/agents/concierge/concierge.py`
- [ ] Verify security review required before merge
- [ ] Complete security checklist and approve
- [ ] Merge PR and verify Jira transition to "Done"
- [ ] Verify change logged to `Agent_Changes_Log.csv`
- [ ] Verify Slack alert sent to #compliance-events
- [ ] Verify post-deployment monitoring task created
- [ ] Verify A/B test tracker updated (if applicable)

---

## Rule 3: Incident → Root Cause Enforcement (Comprehensive)

### Overview
**Trigger**: Issue type = Incident, Priority ≥ High
**Purpose**: Ensure all high-severity incidents have documented root cause analysis and prevent recurrence

### Detailed Configuration

**Rule ID**: `TRVL-AUTO-003`
**Priority**: Critical
**Execution**: Synchronous
**SLA Enforcement**: SEV1 (4hr), SEV2 (24hr)

### Trigger Configuration
```yaml
triggers:
  - type: issue_created
    issue_type: Incident
    conditions:
      - priority_in: [P0, P1]  # SEV1 = P0, SEV2 = P1

  - type: pagerduty_webhook
    event: incident.triggered
    severity: [SEV1, SEV2]
    auto_create_jira: true  # Create Jira issue from PagerDuty
```

### Conditions

#### Condition 1: Severity Classification
```yaml
condition: custom_field_in
field: Incident Severity
values: [SEV1, SEV2]
error_message: "This rule applies to SEV1 and SEV2 incidents only"
```

#### Condition 2: Incident Type Defined
```yaml
condition: custom_field_not_empty
field: Incident Type
allowed_values:
  - System Outage
  - Performance Degradation
  - Security Breach
  - Data Integrity Issue
  - Cost Overrun
  - Agent Malfunction
  - API Failure
required: true
```

### Actions (Sequential Execution)

#### Action 1: Auto-Create Linked RCA Ticket
```yaml
action: create_linked_issue
link_type: "is caused by"
issue_config:
  issue_type: Task
  summary: "Root Cause Analysis: {{incident.key}} - {{incident.summary}}"
  description: |
    **Incident**: {{incident.key}} - {{incident.summary}}
    **Severity**: {{incident.customField.incidentSeverity}}
    **Incident Type**: {{incident.customField.incidentType}}
    **Started**: {{incident.created}}
    **Detected By**: {{incident.reporter}}

    ---

    ## Root Cause Analysis Template

    ### 1. Incident Summary
    - **What happened?**: [Brief description]
    - **User impact**: [Number of users/tenants affected]
    - **Duration**: [Start time → Resolution time]
    - **Detection method**: [Monitoring alert, user report, etc.]

    ### 2. Timeline (in UTC)
    | Time | Event | Actor |
    |------|-------|-------|
    | {{incident.created}} | Incident detected | {{incident.reporter}} |
    | [HH:MM] | Investigation started | [Name] |
    | [HH:MM] | Root cause identified | [Name] |
    | [HH:MM] | Fix deployed | [Name] |
    | [HH:MM] | Incident resolved | [Name] |

    ### 3. Root Cause
    **Primary Cause**: [What was the underlying technical cause?]

    **Contributing Factors**:
    - Factor 1: [e.g., Insufficient monitoring]
    - Factor 2: [e.g., Missing error handling]
    - Factor 3: [e.g., Lack of failover]

    **Why it wasn't caught earlier**: [Pre-production testing gap, monitoring gap, etc.]

    ### 4. Resolution
    **Immediate Fix**: [What was done to restore service?]
    **Permanent Fix**: [What will prevent recurrence?]

    ### 5. Action Items
    - [ ] Action 1: [Description] (Owner: [Name], Due: [Date])
    - [ ] Action 2: [Description] (Owner: [Name], Due: [Date])
    - [ ] Action 3: [Description] (Owner: [Name], Due: [Date])

    ### 6. Lessons Learned
    - **What went well**: [e.g., Fast detection, good communication]
    - **What could improve**: [e.g., Better monitoring, faster rollback]

    ### 7. Follow-Up
    - [ ] Update runbooks
    - [ ] Add monitoring alerts
    - [ ] Improve documentation
    - [ ] Share postmortem with team

    ---

    **RCA Due**: {{rca.dueDate}} (5 business days from incident resolution)
    **Owner**: {{incident.assignee}}

  assignee: "{{incident.assignee}}"
  priority: "{{incident.priority}}"
  labels:
    - rca
    - postmortem
    - "{{incident.customField.incidentSeverity}}"
    - "{{incident.customField.incidentType}}"
  due_date: "+5bd"  # 5 business days from creation
```

#### Action 2: Block Incident Closure Until RCA Complete
```yaml
action: add_workflow_condition
workflow_name: "Incident Workflow"
transition: "Close Incident"
condition:
  type: linked_issue_status
  link_type: "is caused by"
  linked_issue_type: Task
  required_status: Done
  blocking: true
  error_message: |
    ⛔ **Cannot Close Incident**

    Root Cause Analysis (RCA) must be completed before closing this incident.

    **RCA Ticket**: {{rca.key}} (Status: {{rca.status}})

    **Required Actions**:
    1. Complete RCA template in {{rca.key}}
    2. Document root cause and action items
    3. Transition {{rca.key}} to "Done"
    4. Then close this incident

    [View RCA Ticket]({{rca.url}})
```

#### Action 3: Attach Uptime and Agent Logs Automatically
```yaml
action: fetch_and_attach_logs
log_sources:
  - type: datadog_logs
    query: |
      service:timbuktoo-api status:error
      @timestamp:[{{incident.created_timestamp - 1h}} TO {{incident.created_timestamp + 1h}}]
    filename: "datadog_error_logs_{{incident.key}}.json"
    max_lines: 1000

  - type: prometheus_metrics
    query: |
      timbuktoo_trip_cost_usd{
        timestamp >= {{incident.created_timestamp - 1h}},
        timestamp <= {{incident.created_timestamp + 1h}}
      }
    filename: "cost_metrics_{{incident.key}}.csv"

  - type: postgresql_query
    query: |
      SELECT *
      FROM audit_logs
      WHERE created_at >= '{{incident.created_timestamp - 1h}}'::timestamp
        AND created_at <= '{{incident.created_timestamp + 1h}}'::timestamp
        AND event_type IN ('error', 'failure', 'timeout')
      ORDER BY created_at DESC
      LIMIT 500;
    filename: "audit_logs_{{incident.key}}.csv"

  - type: github_commits
    repository: MosesTut/Claude
    branch: main
    time_range:
      from: "{{incident.created_timestamp - 24h}}"
      to: "{{incident.created_timestamp}}"
    filename: "recent_deployments_{{incident.key}}.txt"

upload_to: "{{incident.key}}/logs/"
add_comment: |
  📊 **Logs Attached Automatically**

  The following logs have been attached to assist with RCA:
  - Datadog error logs (1 hour window): `datadog_error_logs_{{incident.key}}.json`
  - Cost metrics (1 hour window): `cost_metrics_{{incident.key}}.csv`
  - Audit logs (1 hour window): `audit_logs_{{incident.key}}.csv`
  - Recent deployments (24 hours): `recent_deployments_{{incident.key}}.txt`

  **Time Window**: {{incident.created_timestamp - 1h}} → {{incident.created_timestamp + 1h}} UTC

  Use these logs to complete the RCA: {{rca.key}}
```

#### Action 4: Send Slack Alert to #incidents
```yaml
action: send_slack_message
channel: "#incidents"
message: |
  🚨 **{{incident.customField.incidentSeverity}} Incident Created**

  **Incident**: {{incident.key}} - {{incident.summary}}
  **Type**: {{incident.customField.incidentType}}
  **Priority**: {{incident.priority}}
  **Started**: {{incident.created}}
  **Assigned**: {{incident.assignee}}

  **Impact**:
  - Severity: {{incident.customField.incidentSeverity}}
  - SLA: {{#if incident.customField.incidentSeverity == 'SEV1'}}4 hours{{else}}24 hours{{/if}}

  **RCA Ticket**: {{rca.key}} (Auto-created)

  **Logs Attached**:
  - Datadog error logs
  - Cost metrics
  - Audit logs
  - Recent deployments

  **Next Steps**:
  1. Investigate and resolve incident: {{incident.key}}
  2. Complete RCA within 5 business days: {{rca.key}}
  3. Implement action items to prevent recurrence

  [View Incident]({{incident.url}}) | [View RCA]({{rca.url}})
attachments:
  - color: "#D32F2F"  # Red for incidents
    fields:
      - title: "Severity"
        value: "{{incident.customField.incidentSeverity}}"
        short: true
      - title: "Type"
        value: "{{incident.customField.incidentType}}"
        short: true
      - title: "SLA"
        value: "{{#if incident.customField.incidentSeverity == 'SEV1'}}4 hours{{else}}24 hours{{/if}}"
        short: true
      - title: "RCA Due"
        value: "{{rca.dueDate}}"
        short: true
```

#### Action 5: Create SOC-2 Incident Documentation Entry
```yaml
action: write_file
destination: SOC2/06_Incident_Response/Incidents_Log.csv
format: csv_append
content:
  incident_key: "{{incident.key}}"
  severity: "{{incident.customField.incidentSeverity}}"
  incident_type: "{{incident.customField.incidentType}}"
  started_at: "{{incident.created}}"
  detected_by: "{{incident.reporter}}"
  assignee: "{{incident.assignee}}"
  rca_ticket: "{{rca.key}}"
  rca_due_date: "{{rca.dueDate}}"
  status: "Open"
  resolution_time: ""
  root_cause: ""
  action_items_count: ""
  logs_attached: "datadog, prometheus, postgresql, github"
```

#### Action 6: Schedule SLA Reminder
```yaml
action: schedule_reminder
schedule:
  sev1_sla_hours: 4
  sev2_sla_hours: 24
  reminder_before_breach_hours: 1
reminder_action:
  type: send_pagerduty_alert
  severity: high
  message: |
    ⏰ **Incident SLA Breach Warning**

    Incident {{incident.key}} is 1 hour from SLA breach.

    **Severity**: {{incident.customField.incidentSeverity}}
    **SLA**: {{#if incident.customField.incidentSeverity == 'SEV1'}}4 hours{{else}}24 hours{{/if}}
    **Time Remaining**: 1 hour
    **Status**: {{incident.status}}

    [View Incident]({{incident.url}})

  escalate_to: "{{incident.assignee.manager}}"
```

#### Action 7: Add RCA Completion Reminder (3 days before due)
```yaml
action: schedule_reminder
schedule:
  days_before_rca_due: 3
reminder_action:
  type: send_slack_dm
  user: "{{incident.assignee}}"
  message: |
    ⏰ **RCA Due in 3 Days**

    Your Root Cause Analysis for incident {{incident.key}} is due in 3 days.

    **RCA Ticket**: {{rca.key}}
    **Due Date**: {{rca.dueDate}}
    **Status**: {{rca.status}}

    **Reminder**: Incident {{incident.key}} cannot be closed until RCA is complete.

    [Complete RCA]({{rca.url}}) | [View Incident]({{incident.url}})
```

### Post-Resolution Actions (Triggered when RCA Status = Done)

#### Action 8: Update Incident Log with RCA Summary
```yaml
trigger: linked_issue_transitioned
link_type: "is caused by"
to_status: Done

action: update_csv_row
destination: SOC2/06_Incident_Response/Incidents_Log.csv
row_identifier: "{{incident.key}}"
updates:
  status: "RCA Complete"
  resolution_time: "{{rca.resolved_timestamp - incident.created_timestamp}}"
  root_cause: "{{rca.customField.rootCause}}"
  action_items_count: "{{rca.subtasks.count}}"
```

#### Action 9: Send RCA Completion Notification
```yaml
action: send_slack_message
channel: "#incidents"
message: |
  ✅ **Root Cause Analysis Complete**

  **Incident**: {{incident.key}} - {{incident.summary}}
  **RCA**: {{rca.key}}
  **Completed By**: {{rca.assignee}}

  **Root Cause**: {{rca.customField.rootCause}}

  **Action Items** ({{rca.subtasks.count}}):
  {{#each rca.subtasks}}
  - {{this.summary}} (Owner: {{this.assignee}}, Due: {{this.dueDate}})
  {{/each}}

  **Next Steps**:
  - Monitor action item completion
  - Update runbooks and documentation
  - Share lessons learned with team

  [View RCA]({{rca.url}}) | [View Incident]({{incident.url}})
```

### Error Handling
```yaml
error_handling:
  on_log_fetch_failure:
    action: add_comment
    comment: "⚠️ Failed to auto-attach logs. Manually attach logs from {{incident.created_timestamp - 1h}} to {{incident.created_timestamp + 1h}}."
    continue: true

  on_sla_breach:
    action: escalate_to_vp
    notify: vp.engineering@timbuktoo.ai
    message: "SLA breach for {{incident.customField.incidentSeverity}} incident {{incident.key}}"
```

### Testing Checklist
- [ ] Create P0 incident with type "System Outage"
- [ ] Verify RCA ticket auto-created with template
- [ ] Verify logs attached (Datadog, Prometheus, audit logs, GitHub)
- [ ] Verify Slack alert sent to #incidents
- [ ] Verify incident logged to `Incidents_Log.csv`
- [ ] Verify SLA reminder scheduled
- [ ] Attempt to close incident (should be blocked)
- [ ] Complete and close RCA ticket
- [ ] Verify incident can now be closed
- [ ] Verify RCA completion notification sent

---

## Implementation Guide

### Prerequisites
1. Create custom fields in Jira:
   - SOC-2 Control ID (text)
   - Evidence Location (text)
   - Evidence Status (select)
   - Trust Service Criteria (select)
   - Security Review Status (select)
   - A/B Test Impact (select)
   - Incident Severity (select)
   - Incident Type (select)
   - Rollback Plan URL (URL)

2. Configure Jira workflows:
   - Add "Ready for Audit" status to Compliance issues
   - Add workflow condition for incident closure (RCA required)

3. Set up integrations:
   - Slack app: Install Jira for Slack
   - GitHub app: Install Jira GitHub integration
   - PagerDuty: Configure webhook to Jira
   - Internal API: Set up `INTERNAL_API_TOKEN` secret

### Installation Steps

1. Navigate to **Project Settings** → **Automation** in Jira
2. Click **Create Rule**
3. For each rule above:
   - Copy the YAML configuration
   - Paste into Jira automation builder (or use UI)
   - Test with sample issue
   - Enable rule

### Monitoring

Track automation health:
- Success rate: >95% target
- Average execution time: <10 seconds
- Failed executions: Alert on >5% failure rate

Dashboard: **Project Settings** → **Automation** → **Audit Log**

---

## Conclusion

These three comprehensive automation rules provide:

1. **SOC-2 Evidence Tracking**: Automated compliance artifact collection
2. **Agent Change Risk Control**: Security-first AI agent modification workflow
3. **Incident → RCA Enforcement**: Systematic incident resolution and learning

All rules include error handling, audit logging, Slack notifications, and SOC-2 evidence generation.

**Estimated Setup Time**: 4-6 hours
**Maintenance**: Quarterly review of rules and thresholds
**ROI**: 80% reduction in manual compliance work, 100% RCA completion rate
