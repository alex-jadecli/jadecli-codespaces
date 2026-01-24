# ---
# entity_id: document-claude-multi-tier
# entity_name: Multi-Tier Claude Configuration Architecture
# entity_type_id: document
# entity_path: research/jade-ide/config/claude-multi-tier.md
# entity_language: markdown
# entity_state: active
# entity_created: 2026-01-23T00:00:00Z
# entity_exports: [config_resolution_order, tier_definitions]
# entity_dependencies: [chezmoi, claude-code]
# entity_actors: [dev, claude]
# ---

# Multi-Tier .claude Configuration Architecture

> Solving the complexity of managing Claude configurations across personal, project, enterprise, and organizational levels.

## The Problem

An engineer at a modern AI-native organization may have 20+ `.claude` configurations:

```
~/.claude/                          # Personal (Tier 1)
~/work/org-a/project-1/.claude/     # Project (Tier 2)
~/work/org-a/project-2/.claude/     # Project (Tier 2)
~/work/org-a/project-3/.claude/     # Project (Tier 2)
~/work/org-b/project-1/.claude/     # Project (Tier 2)
/etc/claude/                        # Enterprise (Tier 3)
[GitHub Org Templates]              # Organization (Tier 4)
```

## The Four Tiers

### Tier 1: Personal (~/.claude)

**Owner**: Individual engineer
**Managed by**: Chezmoi (personal dotfiles)
**Purpose**: Personal preferences, API keys, global settings
**Committed**: Never (contains secrets)

```
~/.claude/
├── settings.json           # Personal model preferences
├── api_keys.json          # Encrypted API keys (age)
├── rules/
│   └── personal.md        # Personal coding style rules
├── commands/
│   └── my-shortcuts.md    # Personal custom commands
└── hooks/
    └── my-hooks.sh        # Personal automation
```

**Example settings.json:**
```json
{
  "model": "claude-sonnet-4-20250514",
  "maxTokens": 200000,
  "defaultPermissions": {
    "allowBash": true,
    "allowEdit": true
  },
  "theme": "dark",
  "editorIntegration": "vscode"
}
```

### Tier 2: Project (~/<org>/<project>/.claude)

**Owner**: Project team
**Managed by**: Git (in-repo)
**Purpose**: Project-specific context, rules, commands
**Committed**: Yes (no secrets)

```
project-repo/.claude/
├── settings.json          # Project overrides
├── rules/
│   ├── architecture.md    # Project architecture rules
│   ├── testing.md         # Testing conventions
│   └── security.md        # Security requirements
├── commands/
│   ├── deploy.md          # Project-specific deployment
│   └── test.md            # Run project tests
└── CLAUDE.md              # Main context file
```

**Example settings.json:**
```json
{
  "extends": "~/.claude/settings.json",
  "projectContext": {
    "language": "typescript",
    "framework": "next.js",
    "testing": "jest"
  },
  "permissions": {
    "allowBash": true,
    "restrictedPaths": ["./secrets/", "./.env*"]
  }
}
```

### Tier 3: Enterprise (/etc/claude)

**Owner**: IT/Security team
**Managed by**: Ansible/Salt/Puppet, MDM
**Purpose**: Compliance, audit logging, model restrictions
**Committed**: Separate config management repo

```
/etc/claude/
├── enterprise.json        # Enterprise-wide settings
├── compliance/
│   ├── data-handling.md   # Data classification rules
│   └── audit-policy.md    # Audit logging requirements
└── allowed-models.json    # Approved model list
```

**Example enterprise.json:**
```json
{
  "priority": "override",
  "modelRestrictions": {
    "allowList": [
      "claude-sonnet-4-20250514",
      "claude-haiku-3-5-20250616"
    ],
    "denyExternalModels": true
  },
  "auditLogging": {
    "enabled": true,
    "destination": "syslog",
    "includePrompts": false,
    "retentionDays": 90
  },
  "permissions": {
    "requireApprovalFor": ["bash", "network", "filesystem"],
    "denyPatterns": ["rm -rf", "sudo", "chmod 777"]
  },
  "dataClassification": {
    "scanForPII": true,
    "blockSecretPatterns": true
  }
}
```

### Tier 4: Organization (GitHub Org Templates)

**Owner**: Platform/DevEx team
**Managed by**: GitHub org repo + Chezmoi external
**Purpose**: Shared templates, reusable rules, standardization
**Committed**: Dedicated dotfiles-claude repo

```
github.com/jade-ide/dotfiles-claude/
├── README.md
├── templates/
│   ├── settings/
│   │   ├── default.json.tmpl
│   │   ├── web-project.json.tmpl
│   │   └── api-project.json.tmpl
│   ├── rules/
│   │   ├── code-style.md
│   │   ├── security.md
│   │   ├── testing.md
│   │   ├── documentation.md
│   │   └── git-conventions.md
│   └── CLAUDE.md.tmpl
├── scripts/
│   ├── init-project.sh     # Bootstrap new project
│   ├── sync-rules.sh       # Sync rules to projects
│   └── validate.sh         # Validate configs
└── .chezmoi/
    └── external.toml       # Chezmoi external config
```

## Configuration Resolution Order

Claude Code resolves settings in this order (later overrides earlier):

```
┌─────────────────────────────────────────────────────────────────┐
│                    RESOLUTION PRIORITY                           │
│                    (Highest to Lowest)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  5. Environment Variables    ─────────────  ANTHROPIC_API_KEY   │
│     (Runtime overrides)                     CLAUDE_CODE_MODEL    │
│                                                                  │
│  4. Project Settings         ─────────────  ./.claude/settings  │
│     (Team-specific)                         ./CLAUDE.md          │
│                                                                  │
│  3. Personal Settings        ─────────────  ~/.claude/settings  │
│     (Individual prefs)                                           │
│                                                                  │
│  2. XDG Config               ─────────────  ~/.config/claude/   │
│     (Chezmoi-managed)                                            │
│                                                                  │
│  1. Enterprise Settings      ─────────────  /etc/claude/        │
│     (IT-managed, can OVERRIDE all)          (with priority:      │
│                                              "override" flag)    │
│                                                                  │
│  0. Defaults                 ─────────────  Claude Code built-in│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Implementation with Chezmoi

### Personal Dotfiles Structure

```
~/.local/share/chezmoi/
├── .chezmoi.toml.tmpl
├── private_dot_claude/
│   ├── settings.json.tmpl
│   ├── private_api_keys.json.age  # Encrypted
│   └── rules/
│       └── personal.md
├── dot_config/
│   └── chezmoi/
│       └── chezmoi.toml
└── .chezmoiexternal.toml          # Pull org templates
```

### Chezmoi External for Org Templates

```toml
# ~/.local/share/chezmoi/.chezmoiexternal.toml

# Pull organization rules
[".claude/rules/org-security.md"]
    type = "file"
    url = "https://raw.githubusercontent.com/jade-ide/dotfiles-claude/main/templates/rules/security.md"
    refreshPeriod = "168h"  # Weekly

[".claude/rules/org-testing.md"]
    type = "file"
    url = "https://raw.githubusercontent.com/jade-ide/dotfiles-claude/main/templates/rules/testing.md"
    refreshPeriod = "168h"

[".claude/rules/org-code-style.md"]
    type = "file"
    url = "https://raw.githubusercontent.com/jade-ide/dotfiles-claude/main/templates/rules/code-style.md"
    refreshPeriod = "168h"
```

### Templated Settings

```gotemplate
{{/* private_dot_claude/settings.json.tmpl */}}
{
  "model": {{ .claude_model | quote }},
  "maxTokens": {{ .claude_max_tokens }},
  {{- if eq .machine_type "work" }}
  "permissions": {
    "allowBash": true,
    "requireApproval": ["rm", "sudo"],
    "restrictedPaths": ["/etc", "/root"]
  },
  "auditLogging": true,
  {{- else }}
  "permissions": {
    "allowBash": true
  },
  {{- end }}
  "mcp": {
    "servers": {
      {{- if .enable_ollama }}
      "ollama": {
        "command": "mcp-server-ollama",
        "args": ["--model", "qwen2.5-coder:7b"]
      }
      {{- end }}
    }
  }
}
```

## Sync Workflow

### Daily Developer Workflow

```bash
# Morning: Pull latest org templates
chezmoi update

# Working on project: Claude uses merged config
cd ~/work/jade-ide/jade-cli
claude  # Merges: /etc + ~/.claude + ./.claude

# End of day: Push any personal config changes
chezmoi add ~/.claude/rules/personal.md
chezmoi git commit -m "chore: update personal rules"
chezmoi git push
```

### Project Setup Workflow

```bash
# Clone project
git clone git@github.com:jade-ide/jade-cli.git
cd jade-cli

# Project already has .claude/ (Tier 2)
# Personal ~/.claude/ applied automatically (Tier 1)
# Enterprise /etc/claude/ applied if present (Tier 3)

# Optionally sync org templates to project
./scripts/sync-org-rules.sh  # Copies from Tier 4 to Tier 2
```

### Enterprise Deployment (IT)

```yaml
# ansible/roles/claude-config/tasks/main.yml
- name: Create /etc/claude directory
  file:
    path: /etc/claude
    state: directory
    mode: '0755'

- name: Deploy enterprise settings
  template:
    src: enterprise.json.j2
    dest: /etc/claude/enterprise.json
    mode: '0644'

- name: Deploy compliance rules
  copy:
    src: "{{ item }}"
    dest: /etc/claude/compliance/
  loop:
    - data-handling.md
    - audit-policy.md
```

## Benefits

| Tier | Benefit |
|------|---------|
| Personal | Individual productivity, portable across projects |
| Project | Team consistency, context sharing, reviewable |
| Enterprise | Compliance, security, audit trail |
| Organization | Standardization, reduced duplication, easy updates |

## Anti-Patterns to Avoid

1. **Secrets in Project .claude** - Never commit API keys
2. **Enterprise Override Everything** - Allow project customization
3. **No Version Control** - Track all configs except secrets
4. **Stale Org Templates** - Automate refresh with chezmoi
5. **Manual Sync** - Use scripts/automation for updates

---

*Architecture designed for Jade IDE - 2026*
