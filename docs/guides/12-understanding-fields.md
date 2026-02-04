# Understanding Fields

> Field types for tracking metadata on project items.

## Key Concepts

- Fields add metadata to issues/PRs in projects
- Custom fields created per project
- Built-in fields from GitHub (assignees, labels, milestone)
- Fields enable filtering, grouping, sorting in views

## Field Types

| Type | Use Case |
|------|----------|
| Text | Notes, descriptions |
| Number | Estimates, points, complexity |
| Date | Deadlines, target dates |
| Single Select | Priority, status, category |
| Iteration | Sprints, time-boxed work periods |
| Parent issue | Hierarchy tracking |
| Sub-issue progress | Completion percentage |
| Pull request | Linked PR status |
| Issue type | Categorization |

## Creating Fields

1. Open project
2. Click `+` in rightmost column header
3. Select "New field"
4. Choose field type
5. Configure options (for single select, iteration)
6. Save

## Single Select Options

- Create preset values (e.g., High/Medium/Low)
- Easy filtering and grouping
- Color-code options

## Iteration Fields

- Configure duration (days or weeks)
- Add breaks between iterations
- Auto-advance support

## CLI Commands

```bash
# List fields in a project
gh project field-list PROJECT_NUMBER --owner OWNER

# Create a field
gh project field-create PROJECT_NUMBER --owner OWNER \
  --name "Priority" --data-type "SINGLE_SELECT"
```

## Limits

- None specified

## See Also

- [Full documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields)
