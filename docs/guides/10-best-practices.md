# Best Practices for Projects

> Recommendations for fields, views, automation, and project organization.

## Key Concepts

- Single source of truth prevents data sync issues
- Automate to reduce manual overhead
- Use custom views for different perspectives
- Link projects to teams and repositories for visibility

## Best Practices List

1. **Communicate across items** - Use @mentions, assign collaborators, link related items
2. **Break down large issues** - Create sub-issues for parallel work
3. **Document with description/README** - Explain project purpose and views
4. **Create customized views** - Table, board, roadmap for different needs
5. **Use field types for metadata** - Dates, numbers, priorities
6. **Automate tasks** - Less manual work = better maintained project
7. **Create charts and insights** - Visualize progress for stakeholders
8. **Create project templates** - Standardize workflows across org
9. **Link to teams and repositories** - Improve visibility and access
10. **Maintain single source of truth** - Prevent information drift

## Field Recommendations

- **Date**: Target ship dates
- **Number**: Task complexity/estimates
- **Single Select**: Priority (Low/Medium/High)
- **Text**: Quick notes
- **Iteration**: Week-by-week planning with breaks

## View Recommendations

- Filter by status: View un-started items
- Group by priority: Monitor high-priority volume
- Sort by date: Track target ship dates
- Slice by assignee: View team capacity
- Display field sums: Total complexity estimates
- Column limits on boards: Maintain focus

## Automation Tips

- Built-in: Auto-set status to "Done" when issues close
- Auto-archive items meeting criteria
- Auto-add items from repos matching filters
- GitHub Actions + GraphQL API for custom automation

## CLI Commands

```bash
# No specific best practices CLI commands
# Use gh project commands from other guides
```

## Limits

- None specified

## See Also

- [Full documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects)
