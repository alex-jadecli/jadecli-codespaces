# jadecli-codespaces

<!-- @meta version: 2.0 | updated: 2026-01-22 | owner: alex-jadecli -->

---

## Purpose

Shared context repository for **multi-agent Claude collaboration** across:
- Local WSL sessions (26.04-jadecli)
- GitHub Codespaces
- Multiple concurrent Claude Code instances

**Key Features:**
- AST-based entity indexing with Tree-sitter/Python AST
- Frontmatter-based dependency tracking for breaking change detection
- Parallel Claude API support via Python/TypeScript SDKs
- Architecture visualization and sequence diagrams

---

## ⚠️ IMPORTANT: Configuration & Secrets

### Never Hardcode Secrets

All secrets and configuration MUST be accessed through `cli/settings.py`:

```python
# ✅ CORRECT
from cli.settings import settings
api_key = settings.parallel_apikey

# ❌ WRONG - Never do this
api_key = "sk-abc123..."  # Hardcoded
api_key = os.environ["API_KEY"]  # Direct env access
```

### Settings Files

| File | Purpose | Committed? |
|------|---------|------------|
| `cli/settings.py` | Pydantic Settings class | ✅ Yes |
| `.env` | Local secrets | ❌ No (gitignored) |
| `.env.example` | Template for .env | ✅ Yes |
| GitHub Secrets | CI/CD secrets | N/A |

See `.claude/rules/settings.md` for full documentation.

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

---

## Entity Store System

### Overview

AST-based indexing system that extracts entities from code and tracks dependencies for:
- **Token Reduction**: Query metadata without reading full files
- **Breaking Change Detection**: Trace dependencies up/down the chain
- **Architecture Diagrams**: Auto-generate ASCII visualizations
- **Sequence Diagrams**: Actor interactions (dev, claude, user, coderabbit)

### Enhanced Frontmatter Schema

Every code file should have frontmatter with dependency tracking:

```python
# ---
# entity_id: module-settings
# entity_name: Centralized Settings
# entity_type_id: module
# entity_path: cli/settings.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T17:00:00Z
#
# Dependencies (for graph construction):
# entity_imports: [pydantic_settings]
# entity_exports: [Settings, settings, get_settings]
# entity_dependencies: [pydantic_settings]
#
# Call Graph (for sequence diagrams):
# entity_callers: [entity_store, entity_cli, hooks]
# entity_callees: []
#
# Versioning (for breaking change detection):
# entity_semver_impact: major
# entity_breaking_change_risk: high
# entity_public_api: true
#
# Actors (for sequence diagrams):
# entity_actors: [dev, claude]
# ---
```

### Frontmatter Fields

| Field | Purpose |
|-------|---------|
| `entity_id` | Unique identifier |
| `entity_name` | Human-readable name |
| `entity_type_id` | class/function/method/module/config |
| `entity_imports` | Modules this entity imports |
| `entity_exports` | Symbols this entity exports |
| `entity_dependencies` | Entity IDs this depends on |
| `entity_callers` | Entities that call this (incoming) |
| `entity_callees` | Entities this calls (outgoing) |
| `entity_semver_impact` | major/minor/patch |
| `entity_breaking_change_risk` | high/medium/low |
| `entity_actors` | dev/claude/user/coderabbit |

### Entity Commands

| Command | Purpose |
|---------|---------|
| `/entity-query` | Query entities with filters |
| `/entity-list` | List entities (table or tree) |
| `/entity-register` | Register new entity |

### Benefits for Claude

1. **Fewer file reads**: Query frontmatter instead of parsing full files
2. **Dependency awareness**: Know what breaks before making changes
3. **Architecture context**: Understand structure without exploration
4. **Token savings**: ~90% reduction via field projection

---

## Documentation Indexing System

### Overview

Semantic search over local docs (anthropic, guides, platform-claude, ruff, ty, uv, wslg, chezmoi) using:
- Embeddings via Anthropic API (cached in Redis)
- Vector similarity search in Dragonfly
- Automatic indexing on session start

### Usage

**Search docs:**
```bash
doc-index search "your query" --top-k 5
```

**Or use `/doc-lookup` skill** in Claude sessions.

### Benefits for Claude

1. **No guessing**: Search docs before answering
2. **Token savings**: Cached embeddings, no repeated API calls
3. **Accurate answers**: Cite actual documentation
4. **Fast**: <100ms vector search

See `doc_index/README.md` for details.

---

## Conventional Commits & Semver

### Commit Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Semver | Description |
|------|--------|-------------|
| `feat` | MINOR | New feature |
| `fix` | PATCH | Bug fix |
| `feat!` | MAJOR | Breaking change |
| `docs` | - | Documentation |
| `refactor` | PATCH | Code refactoring |
| `perf` | PATCH | Performance |
| `test` | - | Tests |
| `chore` | - | Maintenance |

### Breaking Changes

For breaking changes:
1. Use `feat!:` or `fix!:` prefix
2. Or add `BREAKING CHANGE:` in footer
3. This triggers MAJOR version bump

### Pre-commit Hooks

```bash
# Install pre-commit
uv pip install pre-commit
pre-commit install --install-hooks

# Hooks will run on:
# - pre-commit: Linting, formatting, frontmatter validation
# - commit-msg: Conventional commit enforcement
# - pre-push: Breaking change analysis
```

---

## Parallel API Usage

### Configuration

Set up parallel Claude API access:

```bash
# In .env (local)
PARALLEL_APIKEY=your-api-key

# In cli/settings.py (code)
from cli.settings import settings
api_key = settings.parallel_apikey
```

### Python SDK

```python
from anthropic import Anthropic
from cli.settings import settings

client = Anthropic(api_key=settings.parallel_apikey)
```

### TypeScript SDK

```typescript
import Anthropic from '@anthropic-ai/sdk';
// API key loaded from environment via bridge

const client = new Anthropic();
```

---

## Directory Structure

```
jadecli-codespaces/
├── .claude/
│   ├── settings.json
│   ├── rules/
│   │   ├── file-locking.md
│   │   ├── entity-store.md
│   │   └── settings.md         # ← Configuration rule
│   ├── commands/
│   │   ├── checkout.md
│   │   ├── checkin.md
│   │   ├── entity-query.md     # ← Entity queries
│   │   ├── entity-list.md
│   │   └── entity-register.md
│   └── hooks/
│       ├── session-start.py     # ← Entity indexing
│       └── post-tool-use.py     # ← Cache invalidation
├── cli/
│   ├── __init__.py
│   └── settings.py              # ← Centralized settings
├── entity_store/
│   ├── __init__.py
│   ├── models.py                # ← Entity Pydantic models
│   ├── frontmatter.py           # ← Enhanced frontmatter
│   ├── registry.py
│   ├── neon_client.py
│   ├── cache.py
│   ├── visualize.py             # ← ASCII diagrams
│   ├── validate_frontmatter.py  # ← Pre-commit hook
│   ├── check_breaking_changes.py
│   ├── parsers/
│   │   ├── python_parser.py
│   │   ├── typescript_parser.py
│   │   └── markdown_parser.py
│   └── query/
│       └── graphql.py
├── entity_cli/                   # ← React Ink CLI
├── context/
│   ├── sessions/
│   ├── decisions/
│   └── knowledge/
├── .env.example                  # ← Environment template
├── .pre-commit-config.yaml       # ← Pre-commit hooks
├── .releaserc.json               # ← Semantic release
├── pyproject.toml
└── schema.sql                    # ← Neon PostgreSQL schema
```

---

## Visualization Examples

### Architecture Tree

```
entity_store/
├── models.py [Entity, EntityType] ⚠️
│   ├── [class] Entity
│   └── [class] EntityType
├── registry.py [EntityRegistry]
│   └── [class] EntityRegistry
└── parsers/
    ├── python_parser.py [PythonParser]
    └── typescript_parser.py
```

### Dependency Graph

```
UPSTREAM (dependencies):
├── pydantic.BaseModel
├── datetime.datetime
└── uuid.UUID

══════════════════════════════════════════════════
         ┌─────────┐
         │ Entity  │ ⚠️ HIGH RISK
         └─────────┘
══════════════════════════════════════════════════

DOWNSTREAM (dependents):
├── EntityRegistry
│   ├── parse_file()
│   └── register()
├── PythonParser
└── EntityCache
```

### Sequence Diagram

```
    dev          claude       registry      neon
     │             │             │            │
     │──request───>│             │            │
     │             │──parse─────>│            │
     │             │             │──query────>│
     │             │             │<───data────│
     │             │<──entities──│            │
     │<──response──│             │            │
```

---

## Quick Reference

### Environment Setup

```bash
# Install dependencies
uv pip install -e ".[dev]"

# Set up pre-commit
pre-commit install --install-hooks

# Copy env template
cp .env.example .env
# Edit .env with your keys
```

### Daily Workflow

```bash
# 1. Pull latest
git pull --rebase

# 2. Check lock status
/lock-status

# 3. Checkout file
/checkout <file>

# 4. Make changes

# 5. Checkin
/checkin <file>

# 6. Commit (conventional)
git commit -m "feat(entity): add dependency tracking"

# 7. Push
git push
```
