# Planning and Tracking Work

> Use issues, projects, labels, and milestones to organize team work.

## Key Concepts

- **Repositories**: Contain files and serve as collaboration foundation
- **Issues**: Track bugs, features, releases, initiatives
- **Projects**: Customizable spreadsheet integrated with issues/PRs
- **Labels**: Categorize and filter work
- **Milestones**: Track progress toward goals
- **Sub-issues**: Break complex work into hierarchy

## How Issues and Projects Work Together

- Issues are the primary unit of work
- Add issues to projects for visualization
- Projects provide multiple views (table, board, roadmap) of same data
- No data duplication when filtering/organizing

## Team Workflows

- Create issue templates for standardized submissions
- Use task lists within issues for sub-tasks
- Apply labels for categorization and filtering
- Add status updates in comments for transparency
- Create issue dependencies to show blockers
- Organize work through projects with customizable views

## Best Practices

- Use README.md and CONTRIBUTING.md for team communication
- Create issue templates matching common work types
- Implement labels for goals, status, work categorization
- Break large work into sub-issues and task lists
- Document dependencies between issues

## CLI Commands

```bash
# Create an issue
gh issue create --title "Bug report" --body "Description"

# List issues with label
gh issue list --label "bug"

# View issue
gh issue view 123
```

## Limits

- None specified

## See Also

- [Full documentation](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/planning-and-tracking-work-for-your-team-or-project)
