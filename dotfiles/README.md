# ---
# entity_id: doc-dotfiles-readme
# entity_name: Dotfile Management Documentation
# entity_type_id: document
# entity_path: dotfiles/README.md
# entity_language: markdown
# entity_state: active
# entity_created: 2026-01-23T00:00:00Z
# ---

# Dotfile Management

Chezmoi-style layered dotfile management for multi-agent environments.

## Overview

This system manages configuration files across three layers:

| Layer | Purpose | Committed | Precedence |
|-------|---------|-----------|------------|
| `org/` | Organization defaults | Yes | Lowest |
| `project/` | Project-specific | Yes | Middle |
| `local/` | Machine-specific | No | Highest |

Files in higher-precedence layers override those in lower layers.

## Directory Structure

```
dotfiles/
├── org/                    # Organization-wide defaults
│   ├── .claude/
│   │   └── settings.json   # Default Claude permissions
│   └── .config/
│       └── git/
│           └── config      # Git defaults
├── project/                # Project-specific overrides
│   ├── .claude/
│   │   └── settings.json   # Project permissions
│   └── .config/
│       └── ruff.toml       # Project linting
└── local/                  # Machine-specific (gitignored)
    ├── .claude/
    │   └── settings.local.json
    ├── .env.local
    └── .config/
        └── ollama/
            └── models.json
```

## Usage

### Initialize

```bash
make dotfiles-init
```

This creates the directory structure and default templates.

### View Differences

```bash
make dotfiles-diff
```

Shows what would change if dotfiles were applied.

### Apply Configuration

```bash
# Apply all layers
make dotfiles-apply

# Apply specific layer
python -m agents.dotfiles apply --layer=org
python -m agents.dotfiles apply --layer=project
python -m agents.dotfiles apply --layer=local

# Dry run (preview only)
python -m agents.dotfiles apply --dry-run
```

## Layer Details

### Organization Layer (`org/`)

Contains defaults that apply to all projects in the organization:

- Default Claude Code permissions
- Git configuration (user.name, user.email)
- Editor preferences
- Shell aliases

**Committed to repo**: Yes (shared across team)

### Project Layer (`project/`)

Contains project-specific overrides:

- Claude permissions for this project
- Linting/formatting rules
- Test configuration
- Build settings

**Committed to repo**: Yes (project-specific)

### Local Layer (`local/`)

Contains machine-specific settings:

- API keys (via .env.local)
- Local paths
- Hardware-specific tuning
- Personal preferences

**Committed to repo**: No (gitignored)

## Merge Strategies

Files are merged based on their type:

| Extension | Strategy | Description |
|-----------|----------|-------------|
| `.json` | Deep merge | Objects merged recursively |
| `.yaml/.yml` | Deep merge | Objects merged recursively |
| `.env` | Append | Variables appended |
| `.sh/.bash` | Append | Scripts concatenated |
| Others | Replace | Later layer replaces |

## Templates

Files with `.tmpl` extension are processed as templates:

```json
// settings.json.tmpl
{
  "machine": "{{ MACHINE_ID }}",
  "user": "{{ USER }}"
}
```

Variables come from:
1. Environment variables
2. `DotfileConfig.variables` dict

## Example: Setting Up a New Machine

```bash
# 1. Clone the repo
git clone https://github.com/alex-jadecli/jadecli-codespaces.git
cd jadecli-codespaces

# 2. Initialize dotfiles
make dotfiles-init

# 3. Copy local environment template
cp dotfiles/local/.env.local.example dotfiles/local/.env.local

# 4. Edit local settings
vim dotfiles/local/.env.local

# 5. Apply all dotfiles
make dotfiles-apply

# 6. Verify
make dotfiles-diff  # Should show no changes
```

## Integration with Makefile

The Makefile provides convenience targets:

```makefile
make dotfiles-init   # Create directory structure
make dotfiles-apply  # Apply all layers
make dotfiles-diff   # Show differences
```

## Best Practices

1. **Keep secrets in local layer** - Never commit API keys
2. **Use org for team standards** - Consistency across machines
3. **Project overrides sparingly** - Only when necessary
4. **Template for machine-specific values** - Don't hardcode paths
5. **Review diffs before applying** - Know what's changing
