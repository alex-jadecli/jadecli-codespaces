# Built-In Automations

> Zero-config workflows that auto-update Status field based on issue/PR state changes.

## Key Concepts
- Built-in workflows operate on the **Status** field only
- Two workflows enabled by default on new projects:
  - Issue closed -> Status = Done
  - PR merged -> Status = Done
- Additional configurable workflows:
  - Item added -> Status = Todo
  - Issue reopened -> Status = In Progress
  - PR reopened -> Status = In Progress
  - Auto-archive items matching criteria
  - Auto-add items from repo matching filter

## Configuration
1. Click project menu (three dots, top-right)
2. Select **Workflows**
3. Choose workflow under "Default workflows"
4. Click **Edit** to modify target Status value
5. Click **Save and turn on workflow**

## CLI Commands
```bash
# No direct CLI for built-in automations
# Use API or web UI to configure

# View project workflows via API
gh api graphql -f query='
  query($org: String!, $number: Int!) {
    organization(login: $org) {
      projectV2(number: $number) {
        workflows(first: 20) {
          nodes { name enabled }
        }
      }
    }
  }' -f org="OWNER" -F number=1
```

## Limits
- Only affects Status field (single select)
- Cannot trigger custom field updates
- For advanced automation, use Actions or API

## See Also
- [Full documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations)
