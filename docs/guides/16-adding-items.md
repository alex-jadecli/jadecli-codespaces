# Adding Items to Projects

> Add issues, pull requests, and draft issues to your project.

## Key Concepts

- Items = issues, PRs, or draft issues
- Multiple ways to add: URL, search, bulk, auto-add
- Draft issues exist only in project until converted
- Auto-add workflows continuously add matching items

## Adding Methods

### Individual

| Method | How |
|--------|-----|
| Paste URL | Paste issue/PR URL in bottom row, Enter |
| Search | Type `#` then number or title |
| From sidebar | Open issue/PR > Projects section > Add |
| Command palette | Cmd/Ctrl+K > add to project |

### Bulk

| Method | How |
|--------|-----|
| From repository | "Add item from repository" > filter (e.g., `label:bug`) |
| Multi-select | Issues list > select multiple > Projects button |

### Draft Issues

- Type directly in project bottom row
- Exists only in project
- Convert to real issue later

## Auto-Add Workflows

- Configure in project settings
- Automatically adds issues/PRs matching criteria
- Example: Add all issues with `priority:high` label
- Runs continuously on matching items

## CLI Commands

```bash
# Add issue to project
gh project item-add PROJECT_NUMBER --owner OWNER --url ISSUE_URL

# Add PR to project
gh project item-add PROJECT_NUMBER --owner OWNER --url PR_URL

# Create draft issue in project
gh project item-create PROJECT_NUMBER --owner OWNER --title "Draft title"

# List items in project
gh project item-list PROJECT_NUMBER --owner OWNER
```

## Limits

- **50,000 items** maximum per project (active + archived combined)

## Tips

- Use auto-archive to manage item limit
- Draft issues good for capturing ideas quickly
- Bulk add from repo for backlog grooming

## See Also

- [Full documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-items-in-your-project/adding-items-to-your-project)
