# Project Templates

> Create and manage organization-wide project templates.

## Key Concepts

- Templates standardize project setup across organization
- Created from scratch or copied from existing projects
- Include views, fields, draft issues, workflows, insights
- Recommended templates appear first in creation dialog

## What Gets Copied

- Views and layout configurations
- Custom fields
- Draft issues with field values
- Configured workflows (except auto-add)
- Insights/charts

## What Does NOT Copy

- Actual issues/PRs (only draft issues)
- Auto-add workflows
- Project-specific data

## Creating Templates

**New template:**
1. Organizations > Projects > Templates
2. Click "New template"
3. Configure views, fields, workflows
4. Save

**From existing project:**
1. Open project > Settings
2. Templates section > "Copy as template"

## Using Templates

1. Create new project
2. Templates appear in "Create a project" dialog
3. Select preferred template
4. New project inherits template configuration

## Permissions

| Action | Required Permission |
|--------|---------------------|
| Set project as template | Admin |
| Copy project as template | Admin or Write |

## CLI Commands

```bash
# No direct CLI for template management
# Use web interface for templates

# Copy a project (similar to template)
gh project copy PROJECT_NUMBER --owner OWNER --title "New Project"
```

## Limits

- **6 recommended templates** per organization maximum

## See Also

- [Full documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-your-project/managing-project-templates-in-your-organization)
