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

# ADR-001: File Locking System for Multi-Agent Collaboration

## Status

Accepted

## Context

Multiple Claude Code agents may work simultaneously in the same Codespace or repository. Without coordination, agents could:
- Overwrite each other's changes
- Create merge conflicts
- Lose work due to race conditions

## Decision

Implement a **frontmatter-based file locking system** with:

1. **Lock metadata in YAML frontmatter** at the top of each context file
2. **Checkout/Checkin commands** to acquire and release locks
3. **Pre-edit hooks** to warn about locked files
4. **Lock status command** to view all locks

### Frontmatter Schema

```yaml
---
locked_by: <agent-id | null>
locked_at: <ISO-8601 | null>
status: <available | editing | review>
last_edited_by: <agent-id>
last_edited_at: <ISO-8601>
edit_history: [...]
---
```

## Alternatives Considered

### 1. External Lock Files (.lock)
- Pros: Doesn't modify content files
- Cons: Can get out of sync, not visible in file

### 2. Git Branch Per Agent
- Pros: Full isolation
- Cons: Complex merge process, overhead

### 3. Database-Based Locks
- Pros: Robust, supports TTL
- Cons: Requires external service, network dependency

### 4. No Locking (Last Write Wins)
- Pros: Simple
- Cons: Data loss risk

## Consequences

### Positive
- Self-documenting (lock state visible in file)
- Works offline and in git
- Edit history provides audit trail
- No external dependencies

### Negative
- Frontmatter adds overhead to each file
- Requires discipline (agents must follow protocol)
- Stale locks need manual cleanup

## Implementation

- Commands in `.claude/commands/`
- Rules in `.claude/rules/file-locking.md`
- Hooks in `.claude/hooks/`
