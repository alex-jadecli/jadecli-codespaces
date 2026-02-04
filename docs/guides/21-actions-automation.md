# Actions Automation

> GitHub Actions workflows for advanced project automation; requires App token or PAT (not GITHUB_TOKEN).

## Key Concepts
- `GITHUB_TOKEN` cannot access projects (repo-scoped only)
- Use GitHub App token (org projects) or PAT (user projects)
- Projects span repos but workflows are repo-specific
- Common triggers: `pull_request`, `issues`, `schedule`

## Workflow Example
```yaml
name: Add PR to Project
on:
  pull_request:
    types: [ready_for_review]

jobs:
  add-to-project:
    runs-on: ubuntu-latest
    steps:
      - name: Generate token
        id: app-token
        uses: actions/create-github-app-token@v2
        with:
          app-id: ${{ vars.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}
          owner: ${{ github.repository_owner }}

      - name: Add to project
        env:
          GH_TOKEN: ${{ steps.app-token.outputs.token }}
        run: |
          gh project item-add 1 --owner "${{ github.repository_owner }}" \
            --url "${{ github.event.pull_request.html_url }}"
```

## GraphQL in Actions
```yaml
- name: Update project item
  env:
    GH_TOKEN: ${{ steps.app-token.outputs.token }}
  run: |
    gh api graphql -f query='
      mutation($project: ID!, $item: ID!, $field: ID!, $value: String!) {
        updateProjectV2ItemFieldValue(input: {
          projectId: $project
          itemId: $item
          fieldId: $field
          value: { singleSelectOptionId: $value }
        }) {
          projectV2Item { id }
        }
      }' -f project="$PROJECT_ID" -f item="$ITEM_ID" \
         -f field="$FIELD_ID" -f value="$OPTION_ID"
```

## Auth Options
| Method | Use Case | Setup |
|--------|----------|-------|
| GitHub App | Org projects | Create App, store ID + private key |
| PAT | User projects | Store as `secrets.PAT` |

## Limits
- Workflow must exist in each repo you want to track
- App must have project read/write permissions
- Rate limits apply to GraphQL calls

## See Also
- [Full documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/automating-projects-using-actions)
