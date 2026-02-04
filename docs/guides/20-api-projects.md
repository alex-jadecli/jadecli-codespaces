# API for Projects

> GraphQL API for programmatic project management; requires `project` scope for mutations.

## Key Concepts
- Use GraphQL API (not REST) for Projects v2
- Token scopes: `read:project` (queries), `project` (mutations)
- Must add item first, then update fields (cannot combine operations)
- Field types: text, number, date, single select, iteration

## GraphQL Mutations
```graphql
# Add issue/PR to project
mutation {
  addProjectV2ItemById(input: {
    projectId: "PROJECT_NODE_ID"
    contentId: "ISSUE_OR_PR_NODE_ID"
  }) {
    item { id }
  }
}

# Add draft issue
mutation {
  addProjectV2DraftIssue(input: {
    projectId: "PROJECT_NODE_ID"
    title: "Draft title"
    body: "Description"
  }) {
    projectItem { id }
  }
}

# Update field value
mutation {
  updateProjectV2ItemFieldValue(input: {
    projectId: "PROJECT_NODE_ID"
    itemId: "ITEM_NODE_ID"
    fieldId: "FIELD_NODE_ID"
    value: { singleSelectOptionId: "OPTION_NODE_ID" }
  }) {
    projectV2Item { id }
  }
}

# Delete item from project
mutation {
  deleteProjectV2Item(input: {
    projectId: "PROJECT_NODE_ID"
    itemId: "ITEM_NODE_ID"
  }) {
    deletedItemId
  }
}
```

## CLI Commands
```bash
# Get project ID
gh project list --owner OWNER --format json | jq '.projects[] | select(.number==1) | .id'

# Add issue to project
gh project item-add 1 --owner OWNER --url https://github.com/OWNER/REPO/issues/123

# List project items
gh project item-list 1 --owner OWNER --format json

# Edit item field
gh project item-edit --project-id PROJECT_ID --id ITEM_ID --field-id FIELD_ID --single-select-option-id OPTION_ID
```

## Limits
- Rate limits apply per GraphQL query complexity
- Max 100 nodes per connection query

## See Also
- [Full documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects)
