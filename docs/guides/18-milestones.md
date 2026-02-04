# Milestones

> Group issues/PRs into time-boxed iterations with progress tracking; deleting milestones preserves associated items.

## Key Concepts
- Milestones have title, description (Markdown supported), and optional due date
- Progress shown as percentage of closed issues/PRs
- Deleting a milestone does NOT affect associated issues/PRs
- Filter issues/PRs by milestone in list views

## CLI Commands
```bash
# List milestones
gh api repos/{owner}/{repo}/milestones

# Create milestone
gh api repos/{owner}/{repo}/milestones \
  -f title="v1.0" \
  -f description="First release" \
  -f due_on="2026-03-01T00:00:00Z" \
  -f state="open"

# Edit milestone
gh api repos/{owner}/{repo}/milestones/{number} \
  -X PATCH \
  -f title="v1.0-final" \
  -f state="closed"

# Delete milestone
gh api repos/{owner}/{repo}/milestones/{number} -X DELETE

# Associate issue with milestone
gh issue edit {number} --milestone "v1.0"

# List issues in milestone
gh issue list --milestone "v1.0"
```

## Limits
- No documented limit on milestones per repository

## See Also
- [Full documentation](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/creating-and-editing-milestones-for-issues-and-pull-requests)
