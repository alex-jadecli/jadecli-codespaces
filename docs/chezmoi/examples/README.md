# Chezmoi Template Examples

Example templates for managing Claude Code configuration with Chezmoi.

## Contents

- [settings.json.tmpl](./settings.json.tmpl) - User settings template
- [dot_claude.json.tmpl](./dot_claude.json.tmpl) - MCP server configuration template
- [CLAUDE.md.tmpl](./CLAUDE.md.tmpl) - User memory template

## Usage

1. Copy these templates to your Chezmoi source directory.
   From the repository root, run:
   ```bash
   # Copy settings template
   cp docs/chezmoi/examples/settings.json.tmpl ~/.local/share/chezmoi/dot_claude/settings.json.tmpl
   
   # Copy MCP server config template (goes in home directory as .claude.json)
   cp docs/chezmoi/examples/dot_claude.json.tmpl ~/.local/share/chezmoi/dot_claude.json.tmpl
   
   # Copy memory template
   cp docs/chezmoi/examples/CLAUDE.md.tmpl ~/.local/share/chezmoi/dot_claude/CLAUDE.md.tmpl
   
   # Copy example chezmoi config
   mkdir -p ~/.config/chezmoi
   cp docs/chezmoi/examples/chezmoi.toml.example ~/.config/chezmoi/chezmoi.toml
   ```

2. Configure your Chezmoi data in `~/.config/chezmoi/chezmoi.toml`:
   ```toml
   [data]
   claude_model = "claude-sonnet-4-20250514"
   work_machine = false
   ```

3. Apply with Chezmoi:
   ```bash
   chezmoi apply
   ```

## Template Variables

| Variable | Type | Description | Example |
|----------|------|-------------|---------|
| `claude_model` | string | Default Claude model | `"claude-sonnet-4-20250514"` |
| `work_machine` | bool | Is this a work machine? | `true` |
| `mcp_servers.filesystem` | bool | Enable filesystem MCP | `true` |
| `mcp_servers.github` | bool | Enable GitHub MCP | `true` |

## Built-in Chezmoi Variables

These are automatically available:

- `{{ .chezmoi.hostname }}` - Machine hostname
- `{{ .chezmoi.os }}` - Operating system (darwin, linux, windows)
- `{{ .chezmoi.arch }}` - CPU architecture (amd64, arm64)
- `{{ .chezmoi.username }}` - Current username
- `{{ .chezmoi.homeDir }}` - Home directory path
