# Chezmoi Configuration for Claude Code

Guide for managing Claude Code configuration files with [Chezmoi](https://www.chezmoi.io/), the dotfile manager.

## Contents

- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Static Files vs Templates](#static-files-vs-templates)
- [Environment Variables](#environment-variables)
- [Terminal Configuration](#terminal-configuration)
- [GPU & CPU Optimization](#gpu--cpu-optimization)
- [Example Chezmoi Setup](#example-chezmoi-setup)

## Overview

Chezmoi helps you manage your dotfiles across multiple machines. This guide covers how to structure your Claude Code configuration for effective management with Chezmoi.

### Key Directories

| Directory | Purpose | Chezmoi Strategy |
|-----------|---------|------------------|
| `~/.claude/` | User-level Claude Code config | Template for machine-specific settings |
| `~/.claude/commands/` | Personal slash commands | Direct copy (reusable) |
| `~/.claude/settings.json` | User settings | Template (environment-specific) |
| `.claude/` | Project-level config | Git-tracked (not Chezmoi) |
| `.claude-plugin/` | Plugin marketplace config | Direct copy (static) |
| `~/.claude.json` | User MCP server config | Template (environment-specific) |

## Directory Structure

### `~/.claude/` - User Configuration

```
~/.claude/
├── CLAUDE.md              # Personal memory (template or static)
├── settings.json          # User settings (use template)
├── settings.local.json    # Local overrides (machine-specific)
├── commands/              # Personal slash commands (static)
│   ├── commit-push-pr.md
│   ├── dedupe.md
│   └── oncall-triage.md
├── skills/                # Personal skills (static)
│   └── my-skill/SKILL.md
├── agents/                # Personal subagents (static)
│   └── my-agent.md
└── output-styles/         # Personal output styles (static)
    └── my-style.md
```

### `.claude-plugin/` - Plugin Configuration

```
.claude-plugin/
└── marketplace.json       # Plugin marketplace configuration (static)
```

This directory is for plugin developers. The `marketplace.json` file defines plugin metadata for distribution.

## Static Files vs Templates

### Reusable Static Files (Direct Copy)

These files are the same across all machines. Add them to your Chezmoi source directory as-is (no `.tmpl` extension needed):

```
~/.local/share/chezmoi/
├── dot_claude/
│   ├── commands/           # Personal slash commands
│   ├── skills/             # Personal skills
│   ├── agents/             # Personal subagents
│   └── output-styles/      # Personal output styles
└── dot_claude-plugin/
    └── marketplace.json    # Plugin marketplace config
```

### Templated Files (Environment-Specific)

Use Chezmoi templates for files that vary by machine:

#### `~/.claude/settings.json` Template

```json
{
  "permissions": {
    "allow": [
      "Bash(cat *)",
      "Bash(ls *)",
      "Read"
    ]
  }
{{- if eq .chezmoi.hostname "work-laptop" }},
  "model": "claude-sonnet-4-20250514",
  "env": {
    "WORK_PROJECT": "true"
  }
{{- else }},
  "model": "claude-sonnet-4-20250514"
{{- end }}
}
```

#### `~/.claude.json` MCP Server Template

```json
{
  "mcpServers": {
{{- if or (eq .chezmoi.os "darwin") (eq .chezmoi.os "linux") }}
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-filesystem", "{{ .chezmoi.homeDir }}"]
    }
{{- end }}
  }
}
```

## Environment Variables

Claude Code supports environment variables for configuration. You can manage these through Chezmoi shell templates:

```bash
# ~/.local/share/chezmoi/dot_zshrc.tmpl or similar

# Claude Code environment overrides
{{- if .claude_env_vars }}
{{- range $key, $value := .claude_env_vars }}
export {{ $key }}={{ $value }}
{{- end }}
{{- end }}
```

Refer to the [Claude Code documentation](https://code.claude.com/docs/) for current environment variable options.

## Terminal Configuration

### Shift+Enter Support

Claude Code provides **automatic Shift+Enter support** for modern terminals:

- **iTerm2** - Works out of the box
- **WezTerm** - Works out of the box
- **Ghostty** - Works out of the box
- **Kitty** - Works out of the box

**No terminal configuration required.** Claude Code automatically detects the terminal type and maps keys without user configuration.

## GPU & CPU Optimization

### GPU-Accelerated Terminals

Modern terminals use GPU rendering by default:

| Terminal | Rendering | Platform | Notes |
|----------|-----------|----------|-------|
| **WezTerm** | GPU-accelerated | Cross-platform | Rust-based, feature-rich |
| **Kitty** | GPU-based | Cross-platform | Fast, highly configurable |
| **Ghostty** | Platform-native GPU | macOS, Linux | Native UI with GPU acceleration |
| **iTerm2** | GPU-accelerated | macOS | Metal rendering |

### Notes

These GPU-accelerated terminals use GPU rendering by default. No special dotfile configuration is required for Claude Code terminal performance.

## Example Chezmoi Setup

### Directory Structure

```
~/.local/share/chezmoi/
├── .chezmoiignore
├── dot_claude/
│   ├── CLAUDE.md                    # Static (or .tmpl for template)
│   ├── settings.json.tmpl           # Template
│   ├── commands/
│   │   ├── commit-push-pr.md
│   │   ├── dedupe.md
│   │   └── oncall-triage.md
│   ├── skills/
│   │   └── my-skill/SKILL.md
│   └── output-styles/
│       └── my-style.md
├── dot_claude.json.tmpl             # MCP servers template
└── dot_zshrc.tmpl                   # Shell config with Claude vars
```

### Example `.chezmoiignore`

```
# Ignore local-only files
**/*.local.*
**/settings.local.json

# Ignore machine-generated files
**/.cache/
```

### Example `chezmoi.toml`

```toml
[data]
claude_tasks_enabled = true
claude_model = "claude-sonnet-4-20250514"

[data.mcp_servers]
filesystem = true
github = true
```

## Summary

| What to Configure | Chezmoi Strategy | Notes |
|-------------------|------------------|-------|
| `~/.claude/commands/` | Direct copy | Personal slash commands |
| `~/.claude/skills/` | Direct copy | Personal skills |
| `~/.claude/agents/` | Direct copy | Personal subagents |
| `~/.claude/settings.json` | Template | Machine-specific settings |
| `~/.claude.json` | Template | MCP servers vary by environment |
| `.claude-plugin/` | Direct copy | Plugin marketplace config |
| Terminal config | **Not needed** | Shift+Enter works automatically |
| GPU optimization | **Not needed** | Modern terminals auto-optimize |
| Environment vars | Shell template | Add to `.zshrc.tmpl` if needed |

## Additional Resources

- [Chezmoi Documentation](https://www.chezmoi.io/)
- [Claude Code Documentation](https://code.claude.com/docs/)
- [Claude Code Settings Reference](https://code.claude.com/docs/en/settings.md)
- [Claude Code MCP Guide](https://code.claude.com/docs/en/mcp.md)
- [Claude Code Skills Guide](https://code.claude.com/docs/en/skills.md)
