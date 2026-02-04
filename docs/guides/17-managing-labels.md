# Managing Labels

> Repository-level tags for categorizing issues and PRs; anyone with write access can create/edit/delete.

## Key Concepts
- Labels are repository-specific (changes don't affect other repos)
- Nine default labels auto-created: `bug`, `documentation`, `duplicate`, `enhancement`, `good first issue`, `help wanted`, `invalid`, `question`, `wontfix`
- `good first issue` label populates the repo's contribution page
- Organization owners can customize default labels org-wide
- Triage access required to apply labels; write access to create/edit/delete

## CLI Commands
```bash
# List labels
gh label list

# Create label
gh label create "priority:high" --description "High priority" --color "FF0000"

# Edit label
gh label edit "bug" --new-name "type:bug" --color "d73a4a"

# Delete label
gh label delete "wontfix" --yes

# Clone labels from another repo
gh label clone owner/source-repo --force
```

## Limits
- No documented limit on number of labels per repository

## See Also
- [Full documentation](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)
