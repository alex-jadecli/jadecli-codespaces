# Creating an Issue

> Multiple methods to create issues: web UI, CLI, URLs, comments, code, discussions.

## Key Concepts
- Create from: repo Issues tab, comments, code selection, discussions, projects, task lists
- Pre-fill via URL query params: `?title=...&labels=...&assignees=...`
- Copilot Chat can create issues from natural language (public preview)
- Read access required (if repo allows)

## CLI Commands
```bash
# Basic issue creation
gh issue create --title "Bug: login fails" --body "Steps to reproduce..."

# With metadata
gh issue create --title "Feature request" \
  --body "Description here" \
  --assignee "@me" \
  --label "enhancement" \
  --milestone "v1.0" \
  --project "Roadmap"

# Interactive mode
gh issue create
```

## Limits
- URL too long: returns 414 error
- Invalid URL/no permission: returns 404

## See Also
- [Full docs](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue)
