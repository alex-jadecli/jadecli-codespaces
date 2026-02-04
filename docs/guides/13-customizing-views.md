# Customizing Views

> Configure table, board, and roadmap layouts with filters, sorting, and grouping.

## Key Concepts

- Views are saved configurations of layout + filters + sorting
- Multiple views per project for different perspectives
- Three layout types with different strengths
- Changes to items reflect across all views

## Layout Types

| Layout | Description | Best For |
|--------|-------------|----------|
| Table | High-density spreadsheet | Bulk editing, sorting, detailed data |
| Board | Kanban columns | Status workflow, visual progress |
| Roadmap | Timeline view | Date-based planning, milestones |

## Filtering

- Filter by any field value
- Combine multiple filters
- Save filters as part of view
- Example: `status:todo assignee:@me`

## Sorting

- Sort by any field
- Ascending or descending
- Multiple sort levels

## Grouping

- Group by single select fields
- Group by assignee, milestone, iteration
- Collapse/expand groups

## View Configuration

- Show/hide columns (table)
- Configure column order
- Set column limits (board)
- Adjust date range (roadmap)

## CLI Commands

```bash
# List views in a project
gh project view PROJECT_NUMBER --owner OWNER

# No direct CLI for view customization
# Use web interface for view configuration
```

## Limits

- None specified

## See Also

- [Full documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project)
