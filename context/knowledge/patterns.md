---
locked_by: null
locked_at: null
status: available
last_edited_by: setup-initial
last_edited_at: 2026-01-22T15:45:00Z
edit_history:
  - agent: setup-initial
    action: checkin
    at: 2026-01-22T15:45:00Z
---

# Patterns & Learnings

Reusable patterns discovered during jadecli development.

---

## Multi-Agent Collaboration

### File Locking Pattern

```yaml
# Frontmatter for lockable files
---
locked_by: null
locked_at: null
status: available
last_edited_by: <agent-id>
last_edited_at: <ISO-8601>
edit_history: [...]
---
```

**When to use**: Any shared file that multiple agents might edit.

---

## Claude Code Patterns

### Hook for Pre-Edit Validation

```bash
#!/usr/bin/env bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.input.file_path // empty')
# Validate before allowing edit
```

### Command Skill Structure

```markdown
# /command-name

Description of what the command does.

## Usage
/command-name <args>

## Behavior
1. Step one
2. Step two

## Implementation
[Code example]
```

---

## Git Patterns

### Conventional Commits for Context

```
context: update sessions/2026-01-22 - added decisions
context: checkin knowledge/patterns - new section
context: force-unlock stale file
```

---

## To Be Added

- WSL optimization patterns
- Codespace configuration patterns
- Claude-assist integration patterns
