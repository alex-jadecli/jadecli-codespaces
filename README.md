# jadecli-codespaces

Shared Codespace for multi-agent Claude collaboration.

## Quick Start

### In Codespace

1. Click "Code" → "Codespaces" → "Create codespace"
2. Wait for environment setup
3. Run `/lock-status` to see file states
4. Use `/checkout <file>` before editing
5. Use `/checkin <file>` when done

### Local Clone

```bash
git clone https://github.com/alex-jadecli/jadecli-codespaces.git
cd jadecli-codespaces
```

## File Locking

This repo uses frontmatter-based locking for multi-agent safety:

```yaml
---
locked_by: agent-id
locked_at: 2026-01-22T15:30:00Z
status: editing
---
```

### Commands

| Command | Purpose |
|---------|---------|
| `/checkout <file>` | Lock file for editing |
| `/checkin <file>` | Release lock |
| `/lock-status` | View all locks |

## Structure

```
.devcontainer/       # Codespace config
.claude/
  rules/             # Agent rules
  commands/          # Slash commands
  hooks/             # Pre/post edit hooks
context/
  sessions/          # Daily session logs
  decisions/         # ADR records
  knowledge/         # Shared patterns
```

## Sync

```bash
./scripts/sync.sh
```

## License

Private repository for jadecli project.
