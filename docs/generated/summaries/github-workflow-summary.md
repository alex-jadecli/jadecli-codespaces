# GitHub Issues & Projects Summary

Optimized for LLM consumption. Essential concepts for issue and project management.

## Core Concepts

**Issues:** Trackable units of work (bugs, features, tasks).

**Projects:** Collections of issues organized with custom fields and views.

**Automation:** Workflows that move issues between states automatically.

---

## Issues Workflow

### Creating an Issue

**Essential Fields:**
- **Title:** Clear, specific description (e.g., "Fix login button styling on mobile")
- **Description:** Context, acceptance criteria, environment
- **Labels:** Categories (bug, feature, documentation, urgent, etc.)
- **Assignee:** Who owns the work
- **Milestone:** Release or sprint target

**Example:**
```
Title: Add rate limiting to API

Description:
## Problem
API can be called unlimited times, causing performance issues.

## Solution
Implement rate limiting using token bucket algorithm.
Max 100 requests/min per user.

## Acceptance Criteria
- [ ] Rate limiter middleware implemented
- [ ] Returns 429 Too Many Requests
- [ ] Tests pass with >80% coverage
```

### Organizing Issues

**Sub-issues:** Break large issues into smaller tasks
- Parent issue tracks progress
- Child issues are actionable units
- Dependencies between sub-issues

**Dependencies:** Link related issues
- "blocks" - blocks another issue
- "is blocked by" - waiting on another issue
- "duplicates" - same issue reported twice
- "relates to" - contextually related

---

## Project Structure

### Creating a Project

**Types:**
- **Table:** Spreadsheet-like view, good for detailed info
- **Board:** Kanban columns (To Do, In Progress, Done)
- **Roadmap:** Timeline view, good for release planning

**Custom Fields:**
- Status (default)
- Priority (Low/Medium/High/Urgent)
- Effort (S/M/L/XL - story points)
- Assignee (who's working on it)
- Milestone (release target)
- Date (deadline or target date)
- Single/multiple select
- Text fields

### Common Field Configurations

**Startup/Agile:**
- Status: Backlog, Ready, In Progress, In Review, Done
- Priority: Low, Medium, High, Urgent
- Effort: 1-5 (story points)

**Enterprise:**
- Status: New, Triaged, In Progress, In QA, In Review, Done, Archived
- Priority: P0 (critical), P1, P2, P3 (nice to have)
- Effort: hours (1, 2, 4, 8, 16)
- Owner, Team, Cost Center

---

## Views & Visibility

**Table View:** See all fields, filter/sort by any
```
Issue | Status | Priority | Effort | Assignee | Deadline
```

**Board View:** Columns by status
```
To Do | In Progress | In Review | Done
```

**Roadmap View:** Timeline with issue dates
```
Jan: Feature A, B
Feb: Feature C, D
```

**Filtering:**
- By label, assignee, status
- By date range
- Custom filters

---

## Automation Patterns

### Auto-status

When issue properties change, status updates automatically.

**Example:** "When PR is merged, mark issue as Done"

### Auto-archive

Close/hide completed work automatically.

**Example:** "Archive issues marked 'Done' after 30 days"

### Auto-notify

Notify team when items change state.

**Example:** "Comment @channel when issue becomes blocked"

### Workflow Automations

GitHub Actions + Issues API for complex workflows.

**Example:** Create sub-issues automatically when Epic created

---

## Tracking Progress

### Burndown Chart

Shows work completed over time.

**Create:**
1. Configure chart with Status field
2. Select "Done" as complete status
3. Display weekly/daily burn

**Usage:** Sprint velocity, release planning

### Velocity Chart

Completed work per sprint.

**Shows:** Consistent capacity planning

### Custom Metrics

**Examples:**
- Issues by priority (how much urgent work)
- Time to close (issue lifecycle)
- Work distribution (load balancing)

---

## Best Practices

### Issue Quality

1. **Clear titles:** "API rate limiting" not "Fix API"
2. **Detailed description:** Context + acceptance criteria
3. **Right labels:** Use for categorization
4. **Proper milestone:** Link to release/sprint
5. **Estimate effort:** For planning

### Project Management

1. **Define status workflow:** What statuses are used?
2. **Set up automations:** Reduce manual work
3. **Regular grooming:** Update stale issues
4. **Use views:** Different views for different roles
5. **Track metrics:** Monitor progress

### Team Coordination

1. **Assign owners:** Clear responsibility
2. **Link dependencies:** Show blockers
3. **Use milestones:** Release planning
4. **Comment regularly:** Keep status visible
5. **Close promptly:** Archive completed work

---

## API Integration

### Common Operations

```graphql
# Get issues by label
query {
  repository {
    issues(labels: "bug", first: 10) {
      nodes {
        title
        labels(first: 5) { nodes { name } }
        milestone { title dueOn }
      }
    }
  }
}

# Update issue field
mutation {
  updateIssue(input: {
    id: "ISSUE_ID"
    state: CLOSED
  }) {
    issue { state }
  }
}
```

### Automation via Actions

```yaml
# Create issue on PR review
- name: Comment on PR
  if: github.event.pull_request
  uses: actions/github-script@v6
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: 'PR reviewed'
      })
```

---

## Common Workflows

### Feature Development

1. Create issue with acceptance criteria
2. Create project milestone for release
3. Add to project board
4. Assign to developer
5. Create branch from issue
6. Auto-link PR to issue (`fixes #123`)
7. Auto-move to "In Review" when PR created
8. Auto-close when PR merged

### Bug Triage

1. Create issue with repro steps
2. Label "bug"
3. Set priority
4. Add to current sprint
5. Assign to on-call
6. Create linked PR with fix
7. Auto-verify with automated tests

### Release Planning

1. Create milestone with deadline
2. Backlog: Add candidate features/fixes
3. Refine: Estimate and prioritize
4. Sprint: Move to "In Progress"
5. Review: Track "In Review" work
6. Release: Verify all "Done"
7. Archive: Close milestone

---

## Token Count: ~900 tokens

Used for: Workflow selection, automation suggestions, progress reports.
