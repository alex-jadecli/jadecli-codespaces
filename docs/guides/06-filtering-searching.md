# Filtering and Searching Issues

> Search syntax and filters for issues and pull requests.

## Key Concepts
- Default filters: open, created by you, assigned to you, @mentioned
- Filter by: assignee, label, issue type, review status
- Boolean operators: `AND`, `OR`, parentheses (max 5 levels)
- URLs auto-update with filters for sharing

## CLI Commands
```bash
# List issues with search
gh issue list --search 'state:open label:"bug" assignee:@me'

# Complex search
gh issue list --search 'no:assignee label:"help wanted",bug sort:created-asc'

# List PRs with search
gh pr list --search "review:required"
gh pr list --search "is:draft"
gh pr list --search "team:octo-org/octo-team"
```

## Search Qualifiers
```
author:username          # by creator
assignee:username        # by assignee
label:"bug"             # by label (comma = OR, separate filters = AND)
state:open              # by state
type:"Bug"              # by issue type
review:none             # PR review status
review:approved
review:changes_requested
is:draft                # draft PRs
is:merged               # merged PRs
```

## Limits
- Parentheses nesting: max 5 levels

## See Also
- [Full docs](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/filtering-and-searching-issues-and-pull-requests)
