# jadecli-codespaces

<!-- @meta version: 1.0 | updated: 2026-01-22 | owner: alex-jadecli -->

---

## Purpose

Shared context repository for **multi-agent Claude collaboration** across:
- Local WSL sessions (26.04-jadecli)
- GitHub Codespaces
- Multiple concurrent Claude Code instances

---

## File Locking System

This repo uses **frontmatter-based file locking** to prevent conflicts when multiple agents edit files.

### Lock States

| Status | Meaning |
|--------|---------|
| `available` | File can be checked out |
| `editing` | File is locked by an agent |
| `review` | File awaiting review before unlock |

### Frontmatter Format

```yaml
---
locked_by: null
locked_at: null
status: available
last_edited_by: agent-id
last_edited_at: 2026-01-22T15:30:00Z
edit_history:
  - agent: agent-id
    action: checkout
    at: 2026-01-22T15:00:00Z
  - agent: agent-id
    action: checkin
    at: 2026-01-22T15:30:00Z
---
```

### Workflow

```
1. CHECKOUT: Run /checkout <file> before editing
   - Sets locked_by, locked_at, status: editing
   - Fails if already locked

2. EDIT: Make your changes to the file content

3. CHECKIN: Run /checkin <file> when done
   - Clears lock, sets status: available
   - Updates last_edited_by, last_edited_at
   - Appends to edit_history
```

---

## Commands

| Command | Purpose |
|---------|---------|
| `/checkout <file>` | Lock file for editing |
| `/checkin <file>` | Unlock file after editing |
| `/lock-status` | Show all locked files |
| `/force-unlock <file>` | Emergency unlock (admin) |

---

## Directory Structure

```
jadecli-codespaces/
├── .devcontainer/        # Codespace configuration
├── .claude/
│   ├── settings.json     # Shared settings
│   ├── rules/
│   │   └── file-locking.md
│   ├── commands/
│   │   ├── checkout.md
│   │   ├── checkin.md
│   │   └── lock-status.md
│   └── hooks/
│       └── pre-edit-check.sh
├── context/
│   ├── sessions/         # Daily session summaries
│   ├── decisions/        # ADR-style decisions
│   └── knowledge/        # Extracted patterns
├── scripts/
│   └── sync.sh
└── CLAUDE.md
```

---

## Context Files

### Sessions (`context/sessions/YYYY-MM-DD.md`)
Daily summaries of work done, decisions made, open questions.

### Decisions (`context/decisions/NNN-title.md`)
Architectural Decision Records with context, options, outcome.

### Knowledge (`context/knowledge/*.md`)
Extracted patterns, learnings, reusable solutions.

---

## Multi-Agent Etiquette

1. **Always checkout before editing** - Never edit without locking
2. **Checkin promptly** - Don't hold locks longer than needed
3. **Check lock-status first** - See what others are working on
4. **Use sessions for coordination** - Note what you're doing in session files
5. **Atomic changes** - One concern per checkin

---

## Sync with Local

```bash
# Pull latest context
git pull --rebase

# Push your changes
git add -A && git commit -m "context: <summary>" && git push
```

---

## Integration

### With claude-assist (PostgreSQL)
Export decisions to database for long-term search:
```bash
./scripts/export-to-db.sh
```

### With WSL
Clone to `~/jadecli-codespaces` and sync regularly.

---

## Accessing from Local Claude Code

Use your existing Claude Code subscription to work in this Codespace.

### Option 1: SSH into Codespace

```bash
# List your codespaces
gh codespace list

# SSH into the codespace
gh codespace ssh -c <codespace-name>

# Run Claude Code inside
claude
```

### Option 2: Clone Locally + Sync

```bash
# Clone to local WSL
cd ~
git clone https://github.com/alex-jadecli/jadecli-codespaces.git

# Work locally with Claude Code (your subscription)
cd jadecli-codespaces
claude

# Sync changes
./scripts/sync.sh
```

### Option 3: VS Code Remote

1. Install "GitHub Codespaces" extension in VS Code
2. Connect to codespace from VS Code
3. Open terminal in VS Code
4. Run `claude` (uses your subscription via VS Code terminal)

---

## Getting Started

1. Clone locally or SSH into Codespace
2. Run `/lock-status` to see current state
3. Use `/checkout` before any edits
4. Use `/checkin` when done
