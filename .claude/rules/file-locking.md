# File Locking Rule for Multi-Agent Collaboration

> Prevents conflicts when multiple Claude agents work in the same Codespace.

## When This Rule Applies

This rule applies to ALL files in the `context/` directory:
- `context/sessions/*.md`
- `context/decisions/*.md`
- `context/knowledge/*.md`

## Required Frontmatter

Every context file MUST have this frontmatter structure:

```yaml
---
locked_by: <agent-id | null>
locked_at: <ISO-8601 timestamp | null>
status: <available | editing | review>
last_edited_by: <agent-id | null>
last_edited_at: <ISO-8601 timestamp | null>
edit_history:
  - agent: <agent-id>
    action: <checkout | checkin | force-unlock>
    at: <ISO-8601 timestamp>
---
```

## Before Editing Any File

1. **READ the file first** to check the frontmatter
2. **If `status: editing`** - DO NOT edit. The file is locked.
3. **If `status: available`** - Proceed with checkout

## Checkout Procedure

Before editing, update the frontmatter:

```yaml
---
locked_by: <your-agent-id>
locked_at: <current ISO-8601 timestamp>
status: editing
# ... rest unchanged
edit_history:
  - agent: <your-agent-id>
    action: checkout
    at: <current ISO-8601 timestamp>
  # ... previous history
---
```

## Checkin Procedure

After editing, update the frontmatter:

```yaml
---
locked_by: null
locked_at: null
status: available
last_edited_by: <your-agent-id>
last_edited_at: <current ISO-8601 timestamp>
edit_history:
  - agent: <your-agent-id>
    action: checkin
    at: <current ISO-8601 timestamp>
  # ... previous history
---
```

## Agent ID Format

Use a consistent identifier:
- Format: `<session-type>-<short-hash>`
- Examples: `wsl-a1b2c3`, `codespace-x4y5z6`, `local-m7n8o9`

Generate with:
```bash
echo "$(hostname)-$(head -c 3 /dev/urandom | xxd -p)"
```

## Conflict Resolution

If you encounter a stale lock (locked_at > 1 hour ago):

1. Check if the locking agent is still active
2. If not, use force-unlock with documentation
3. Add note to edit_history explaining the force-unlock

## DO NOT

- Edit files without checking frontmatter first
- Hold locks for more than 30 minutes
- Force-unlock without documenting reason
- Edit frontmatter of files you don't have locked

## DO

- Always checkout before editing
- Checkin immediately after finishing
- Use atomic, focused changes
- Document your changes in the file content
