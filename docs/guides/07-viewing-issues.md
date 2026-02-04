# Viewing All Issues and PRs

> Dashboards and saved views for cross-repo issue/PR monitoring.

## Key Concepts
- Dashboards accessible from top nav (Issues / Pull requests)
- Shows: created by you, assigned to you, @mentions, review requests
- Saved views = custom filtered views across multiple repos
- Use `is:pr` filter to include PRs in views

## CLI Commands
```bash
# List your issues across repos
gh issue list --state open

# List issues assigned to you
gh issue list --assignee "@me"

# List PRs needing your review
gh pr list --search "review-requested:@me"

# List your PRs
gh pr list --author "@me"
```

## Limits
- **Max 25 saved views** per user

## See Also
- [Full docs](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/viewing-all-of-your-issues-and-pull-requests)
