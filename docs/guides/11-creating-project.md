# Creating a Project

> Create organization or user projects with templates or blank layouts.

## Key Concepts

- **Organization projects**: Track issues/PRs from org repositories
- **User projects**: Track issues/PRs from personal account repos
- Templates provide pre-configured fields, views, workflows
- Three blank layouts: Table, Roadmap, Board

## Creating an Organization Project

1. Click profile > Organizations
2. Select organization
3. Click Projects tab
4. Click "New project"
5. Choose blank layout or template
6. Enter project name
7. Optionally import items from repository
8. Click "Create project"

## Creating a User Project

1. Click profile > "Your profile"
2. Click Projects tab
3. Click "New project"
4. Select project type
5. Enter project name
6. Click "Create project"

## Template Options

- Built-in GitHub templates
- Organization-created templates
- Recommended templates (org-designated)
- Blank: Table, Roadmap, Board

## CLI Commands

```bash
# Create a project (org)
gh project create --owner ORG_NAME --title "Project Title"

# Create a project (user)
gh project create --owner @me --title "Project Title"

# List projects
gh project list --owner ORG_NAME
```

## Limits

- None specified for project creation

## See Also

- [Full documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/creating-projects/creating-a-project)
