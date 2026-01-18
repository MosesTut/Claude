# Jira Automation Rules for Timbuktoo Project

**Project Key**: TRVL
**Purpose**: Automated workflow management, notifications, and quality gates

---

## Rule 1: Auto-Link Stories to Epics

**Trigger**: Issue created
**Condition**: Issue type = Story OR Task
**Action**:
- Extract Epic key from Issue Key (e.g., TRVL-101 → TRVL-CORE-001)
- Link to parent Epic
- Add Epic label to story

**JQL for Manual Backfill**:
```jql
project = TRVL AND issuetype in (Story, Task) AND "Epic Link" is EMPTY
```

**Automation YAML**:
```yaml
name: Auto-Link Stories to Epics
trigger:
  - type: issue_created
conditions:
  - type: issue_type
    values: [Story, Task]
actions:
  - type: link_to_epic
    epic_key: "{{issue.key.substring(0,13)}}"  # Extract TRVL-XXX-001
  - type: add_label
    label: "{{epic.name}}"
```

---

## Rule 2: Assign Based on Component Area

**Trigger**: Issue created OR Component Area changed
**Condition**: Component Area is set
**Action**: Auto-assign based on mapping

**Component → Assignee Mapping**:
- **Backend** → Backend Engineering Lead
- **Frontend** → Frontend Engineering Lead
- **ML** → ML Engineering Lead
- **Data** → Data Engineering Lead
- **Platform** → DevOps Lead
- **Full Stack** → Full Stack Engineering Lead

**Automation YAML**:
```yaml
name: Auto-Assign by Component
trigger:
  - type: issue_created
  - type: field_changed
    field: Component Area
conditions:
  - type: field_not_empty
    field: Component Area
actions:
  - type: assign_user
    user: "{{#if Component Area == 'Backend'}}backend.lead@timbuktoo.ai{{/if}}"
    user: "{{#if Component Area == 'ML'}}ml.lead@timbuktoo.ai{{/if}}"
    user: "{{#if Component Area == 'Data'}}data.lead@timbuktoo.ai{{/if}}"
    user: "{{#if Component Area == 'Platform'}}devops.lead@timbuktoo.ai{{/if}}"
```

---

## Rule 3: SLO Impact Alert for High-Priority Issues

**Trigger**: Issue created OR Priority changed
**Condition**: SLO Impact = "High" AND Priority = "P0"
**Action**:
- Send Slack notification to #engineering-alerts
- Tag VP Engineering
- Set due date to 7 days from creation

**Automation YAML**:
```yaml
name: SLO High-Impact Alert
trigger:
  - type: issue_created
  - type: field_changed
    field: Priority
conditions:
  - type: field_equals
    field: SLO Impact
    value: High
  - type: field_equals
    field: Priority
    value: P0
actions:
  - type: send_slack_message
    channel: "#engineering-alerts"
    message: "🚨 High SLO Impact Issue Created: {{issue.key}} - {{issue.summary}}\nAssignee: {{issue.assignee}}\nDue: 7 days"
  - type: mention_user
    user: "vp.engineering@timbuktoo.ai"
  - type: set_due_date
    days_from_now: 7
```

---

## Rule 4: Data Sensitivity Workflow Gate

**Trigger**: Issue transitioned to "In Review"
**Condition**: Data Sensitivity = "High" OR "Medium"
**Action**:
- Require security review approval
- Add "security-review-required" label
- Assign to Security Lead for review

**Automation YAML**:
```yaml
name: Security Review Gate
trigger:
  - type: issue_transitioned
    to_status: In Review
conditions:
  - type: field_in
    field: Data Sensitivity
    values: [High, Medium]
actions:
  - type: add_label
    label: security-review-required
  - type: add_comment
    comment: "⚠️ This issue handles sensitive data. Security review required before deployment.\n\nReviewer: @security.lead"
  - type: assign_reviewer
    reviewer: "security.lead@timbuktoo.ai"
  - type: block_transition
    until: security_approval_received
```

---

## Rule 5: Cost Tier Budget Tracking

**Trigger**: Issue transitioned to "Done"
**Condition**: Cost Tier is set
**Action**:
- Update Epic budget spent field
- Alert if Epic budget > 80% consumed

**Automation YAML**:
```yaml
name: Cost Tier Budget Tracking
trigger:
  - type: issue_transitioned
    to_status: Done
conditions:
  - type: field_not_empty
    field: Cost Tier
actions:
  - type: update_epic_field
    field: Budget Spent
    value: "{{epic.budgetSpent + story.costTier}}"
  - type: conditional_alert
    condition: "{{epic.budgetSpent / epic.budgetTotal > 0.8}}"
    action:
      type: send_slack_message
      channel: "#finops-alerts"
      message: "💰 Epic {{epic.key}} is 80%+ over budget. Current: ${{epic.budgetSpent}} / ${{epic.budgetTotal}}"
```

**Cost Tier → Dollar Mapping**:
- Low = $5,000
- Medium = $15,000
- High = $30,000

---

## Rule 6: Release Phase Validation

**Trigger**: Issue transitioned to "Ready for Release"
**Condition**: Release Phase = "GA"
**Action**:
- Validate all sub-tasks complete
- Require QA approval
- Check SOC-2 compliance for security stories

**Automation YAML**:
```yaml
name: GA Release Validation
trigger:
  - type: issue_transitioned
    to_status: Ready for Release
conditions:
  - type: field_equals
    field: Release Phase
    value: GA
actions:
  - type: validate_subtasks
    required: all_complete
    failure_message: "❌ Cannot release to GA: {{subtask.incomplete.count}} sub-tasks incomplete"
  - type: require_approval
    approvers: [qa.lead@timbuktoo.ai]
    approval_message: "QA sign-off required for GA release"
  - type: conditional_check
    condition: "{{issue.labels contains 'security'}}"
    action:
      type: validate_field
      field: SOC-2 Control
      required: not_empty
      failure_message: "Security issues must have SOC-2 control mapping for GA"
```

---

## Rule 7: Agent Type Notification Routing

**Trigger**: Issue created
**Condition**: Agent Type is set (not "None")
**Action**:
- Send notification to relevant agent team Slack channel
- Add agent-specific label

**Agent Type → Slack Channel Mapping**:
- **City Selection** → #agent-city-selection
- **Local Expert** → #agent-local-expert
- **Travel Concierge** → #agent-concierge
- **All** → #agent-orchestration

**Automation YAML**:
```yaml
name: Agent Team Notification
trigger:
  - type: issue_created
conditions:
  - type: field_not_equals
    field: Agent Type
    value: None
actions:
  - type: send_slack_message
    channel: "#agent-{{issue.agentType.lowercase}}"
    message: "🤖 New issue for {{issue.agentType}} agent: {{issue.key}} - {{issue.summary}}\nAssignee: {{issue.assignee}}\nPriority: {{issue.priority}}"
  - type: add_label
    label: "agent-{{issue.agentType}}"
```

---

## Rule 8: Epic Completion Summary

**Trigger**: All stories in Epic transitioned to "Done"
**Condition**: Epic has no open stories
**Action**:
- Post Epic completion summary to #engineering channel
- Update Epic status to "Complete"
- Generate completion report with story points delivered

**Automation YAML**:
```yaml
name: Epic Completion Summary
trigger:
  - type: epic_all_stories_done
conditions:
  - type: epic_has_no_open_issues
actions:
  - type: send_slack_message
    channel: "#engineering"
    message: |
      ✅ Epic Complete: {{epic.key}} - {{epic.summary}}

      📊 Summary:
      - Total Stories: {{epic.stories.count}}
      - Story Points Delivered: {{epic.storyPoints.sum}}
      - Duration: {{epic.startDate}} → {{epic.completionDate}}
      - Components: {{epic.components.unique.join(', ')}}

      🎉 Great work team!
  - type: transition_epic
    to_status: Complete
  - type: generate_report
    template: epic_completion_report
    output: confluence
```

---

## Rule 9: Overdue Issue Escalation

**Trigger**: Daily at 9:00 AM
**Condition**: Issue due date < TODAY AND status != "Done"
**Action**:
- Send Slack DM to assignee
- Tag manager if overdue > 3 days
- Escalate to VP Engineering if overdue > 7 days

**Automation YAML**:
```yaml
name: Overdue Issue Escalation
trigger:
  - type: scheduled
    cron: "0 9 * * *"  # Daily 9 AM
conditions:
  - type: jql
    query: "project = TRVL AND due < now() AND status != Done"
actions:
  - type: send_slack_dm
    user: "{{issue.assignee}}"
    message: "⏰ Reminder: {{issue.key}} is overdue (Due: {{issue.dueDate}})"
  - type: conditional_action
    condition: "{{issue.overdueDays > 3}}"
    action:
      type: send_slack_dm
      user: "{{issue.assignee.manager}}"
      message: "⚠️ {{issue.key}} assigned to {{issue.assignee}} is {{issue.overdueDays}} days overdue"
  - type: conditional_action
    condition: "{{issue.overdueDays > 7}}"
    action:
      type: send_slack_message
      channel: "#engineering-escalations"
      message: "🚨 CRITICAL: {{issue.key}} is {{issue.overdueDays}} days overdue\nAssignee: {{issue.assignee}}\nPriority: {{issue.priority}}"
```

---

## Rule 10: Dependency Blocker Alert

**Trigger**: Issue status changed to "Blocked"
**Condition**: Issue has "is blocked by" link to another issue
**Action**:
- Notify blocker issue assignee
- Add "blocking-others" label to blocker
- Update blocker priority if necessary

**Automation YAML**:
```yaml
name: Dependency Blocker Alert
trigger:
  - type: issue_transitioned
    to_status: Blocked
conditions:
  - type: has_issue_link
    link_type: is blocked by
actions:
  - type: add_comment
    target: blocker_issue
    comment: "⚠️ This issue is blocking {{issue.key}} - {{issue.summary}}\nBlocked assignee: {{issue.assignee}}"
  - type: add_label
    target: blocker_issue
    label: blocking-others
  - type: send_slack_dm
    user: "{{blocker.assignee}}"
    message: "🔴 Your issue {{blocker.key}} is blocking {{issue.key}}. Please prioritize!"
  - type: conditional_action
    condition: "{{blocker.priority > issue.priority}}"
    action:
      type: update_priority
      target: blocker_issue
      priority: "{{issue.priority}}"
```

---

## Rule 11: Code Review Reminder

**Trigger**: Issue transitioned to "In Review"
**Condition**: Issue has GitHub PR link
**Action**:
- Remind reviewers daily until approved
- Auto-transition to "Done" when PR merged

**Automation YAML**:
```yaml
name: Code Review Reminder
trigger:
  - type: issue_transitioned
    to_status: In Review
  - type: scheduled
    cron: "0 10 * * *"  # Daily 10 AM
conditions:
  - type: has_web_link
    url_contains: github.com/pull
  - type: github_pr_status
    status: open
actions:
  - type: send_slack_message
    channel: "#code-reviews"
    message: "👀 Code review needed: {{issue.key}} - {{issue.summary}}\nPR: {{issue.githubPR.url}}\nAuthor: {{issue.assignee}}"
  - type: conditional_action
    condition: "{{github.pr.status == 'merged'}}"
    action:
      type: transition_issue
      to_status: Done
      add_comment: "✅ PR merged. Auto-transitioning to Done."
```

---

## Rule 12: Testing Coverage Gate

**Trigger**: Issue transitioned to "Ready for QA"
**Condition**: Component Area = "Backend" OR "ML"
**Action**:
- Check if test coverage >= 80%
- Block transition if coverage < 80%

**Automation YAML**:
```yaml
name: Test Coverage Gate
trigger:
  - type: issue_transitioned
    to_status: Ready for QA
conditions:
  - type: field_in
    field: Component Area
    values: [Backend, ML]
actions:
  - type: check_coverage
    min_threshold: 80
    failure_action:
      type: transition_back
      to_status: In Progress
      add_comment: "❌ Test coverage is {{coverage.percent}}% (minimum 80% required). Please add more tests."
  - type: conditional_action
    condition: "{{coverage.percent >= 80}}"
    action:
      type: add_comment
      comment: "✅ Test coverage: {{coverage.percent}}% (meets 80% threshold)"
```

---

## Rule 13: Production Incident Auto-Create

**Trigger**: PagerDuty incident created (webhook)
**Condition**: Severity = SEV1 OR SEV2
**Action**:
- Auto-create Jira issue with incident details
- Link to on-call engineer
- Set priority based on severity

**Automation YAML**:
```yaml
name: Production Incident Auto-Create
trigger:
  - type: webhook
    source: pagerduty
    event: incident.triggered
conditions:
  - type: webhook_field
    field: severity
    values: [SEV1, SEV2]
actions:
  - type: create_issue
    issue_type: Bug
    summary: "[{{webhook.severity}}] {{webhook.title}}"
    description: |
      Production incident detected:

      **PagerDuty ID**: {{webhook.incident_id}}
      **Severity**: {{webhook.severity}}
      **Service**: {{webhook.service}}
      **Triggered At**: {{webhook.created_at}}
      **On-Call Engineer**: {{webhook.assignee}}

      **Incident URL**: {{webhook.html_url}}
    priority: "{{#if webhook.severity == 'SEV1'}}P0{{else}}P1{{/if}}"
    component: Platform
    assignee: "{{webhook.assignee}}"
    labels: [production-incident, "{{webhook.severity}}"]
  - type: send_slack_message
    channel: "#incidents"
    message: "🚨 {{webhook.severity}} Incident: Jira issue {{issue.key}} created for {{webhook.title}}"
```

---

## Rule 14: Release Phase Promotion

**Trigger**: Issue transitioned to "Done"
**Condition**: Release Phase = "Beta" AND all acceptance criteria met
**Action**:
- Suggest promotion to "GA"
- Require PM approval for promotion

**Automation YAML**:
```yaml
name: Release Phase Promotion
trigger:
  - type: issue_transitioned
    to_status: Done
conditions:
  - type: field_equals
    field: Release Phase
    value: Beta
  - type: all_subtasks_complete
actions:
  - type: add_comment
    comment: |
      ✅ Beta release complete. Consider promoting to GA:

      **Checklist for GA Promotion**:
      - [ ] No critical bugs reported in 30 days
      - [ ] Performance benchmarks met
      - [ ] Security review complete
      - [ ] Documentation published

      @product.manager - Please review and approve GA promotion.
  - type: create_subtask
    summary: "Promote {{issue.key}} to GA Release"
    assignee: "product.manager@timbuktoo.ai"
```

---

## Rule 15: SLA Breach Warning

**Trigger**: Every hour
**Condition**: Issue created > SLA threshold AND status != "Done"
**Action**:
- Alert assignee and manager
- Add "sla-at-risk" label

**SLA Thresholds by Priority**:
- P0: 24 hours
- P1: 72 hours (3 days)
- P2: 168 hours (7 days)
- P3: 720 hours (30 days)

**Automation YAML**:
```yaml
name: SLA Breach Warning
trigger:
  - type: scheduled
    cron: "0 * * * *"  # Every hour
conditions:
  - type: jql
    query: |
      project = TRVL AND status != Done AND (
        (priority = P0 AND created < -24h) OR
        (priority = P1 AND created < -72h) OR
        (priority = P2 AND created < -7d) OR
        (priority = P3 AND created < -30d)
      )
actions:
  - type: add_label
    label: sla-at-risk
  - type: send_slack_dm
    user: "{{issue.assignee}}"
    message: "⏰ SLA Warning: {{issue.key}} is approaching SLA breach ({{issue.ageHours}}h since creation)"
  - type: send_slack_dm
    user: "{{issue.assignee.manager}}"
    message: "⚠️ SLA at risk: {{issue.key}} assigned to {{issue.assignee}} (Age: {{issue.ageHours}}h, SLA: {{issue.slaThreshold}}h)"
```

---

## Implementation Guide

### Step 1: Enable Automation in Jira
1. Navigate to **Project Settings** → **Automation**
2. Click **Create Rule**
3. Copy YAML configuration from above
4. Test with sample issues before enabling

### Step 2: Configure Slack Integration
1. Install Jira Slack app: https://slack.com/apps/A2RPP3NFR-jira-cloud
2. Configure webhook URL in Jira automation
3. Map Jira users to Slack users (email match)

### Step 3: Set Up Custom Fields
Ensure these custom fields exist in Jira:
- Component Area (Select: Backend, Frontend, ML, Data, Platform, Full Stack)
- Agent Type (Select: City Selection, Local Expert, Travel Concierge, All, None)
- Data Sensitivity (Select: High, Medium, Low, None)
- SLO Impact (Select: High, Medium, Low)
- Cost Tier (Select: High, Medium, Low)
- Release Phase (Select: GA, Beta, Alpha, Internal)
- SOC-2 Control (Text field for control IDs)

### Step 4: Configure GitHub Integration
1. Install Jira GitHub app: https://github.com/marketplace/jira-software-github
2. Link repository: MosesTut/Claude
3. Enable PR → Jira issue auto-linking via commit messages

### Step 5: PagerDuty Webhook Setup
1. Create Jira webhook in PagerDuty: **Settings** → **Integrations** → **Jira**
2. Map PagerDuty severities to Jira priorities
3. Test with sample incident

---

## Testing Checklist

- [ ] Test Rule 1: Create story TRVL-101, verify Epic link
- [ ] Test Rule 3: Create P0 issue with SLO Impact=High, verify Slack alert
- [ ] Test Rule 4: Transition issue with Data Sensitivity=High to "In Review", verify security review gate
- [ ] Test Rule 9: Create overdue issue, verify daily reminder
- [ ] Test Rule 11: Link GitHub PR, verify auto-transition when merged
- [ ] Test Rule 13: Trigger PagerDuty incident, verify Jira issue creation

---

## Monitoring Automation Health

**Metrics Dashboard** (Jira Automation Logs):
- Total rules: 15
- Total executions/day: ~50-100
- Success rate target: >95%
- Average execution time: <5 seconds

**Alert on**:
- Automation failure rate >10%
- Slack webhook errors
- GitHub integration failures

**Monthly Review**:
- Review automation logs for failures
- Update rules based on team feedback
- Add new rules as needed
