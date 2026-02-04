# Claude Code Terminal Configuration Guide

This guide covers configuring your terminal for the best Claude Code experience on WSLg.

## Table of Contents

- [Overview](#overview)
- [Recommended Terminal Settings](#recommended-terminal-settings)
- [Shell Configuration](#shell-configuration)
- [Claude Code Settings](#claude-code-settings)
- [Terminal Emulator Quick Reference](#terminal-emulator-quick-reference)

## Overview

Claude Code works best with terminal emulators that support:

- Large scrollback buffers (10,000+ lines)
- GPU acceleration for smooth rendering
- Shell integration
- Unicode and emoji support
- Good clipboard integration

## Recommended Terminal Settings

### Essential Settings for All Terminals

| Setting | Recommended Value | Why |
|---------|------------------|-----|
| Scrollback lines | 50,000 - 100,000 | Long Claude Code conversations |
| Cursor style | Block, non-blinking | Better focus, less distraction |
| Font | JetBrains Mono 12pt | Excellent readability, ligatures |
| GPU acceleration | Enabled | Smooth scrolling |
| Shell integration | Enabled | Better command tracking |

### Installing JetBrains Mono

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y fonts-jetbrains-mono

# Or download manually
cd /tmp
wget https://github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip
unzip JetBrainsMono-2.304.zip -d jetbrains-mono
sudo mkdir -p /usr/share/fonts/truetype/jetbrains-mono
sudo cp jetbrains-mono/fonts/ttf/*.ttf /usr/share/fonts/truetype/jetbrains-mono/
sudo fc-cache -fv
```

## Shell Configuration

### Bash Configuration

Add to `~/.bashrc`:

```bash
# =============================================================================
# Bash Configuration for Claude Code
# =============================================================================

# History settings - keep long history for reference
HISTSIZE=50000
HISTFILESIZE=100000
HISTCONTROL=ignoreboth:erasedups
shopt -s histappend

# Better command line editing
set -o emacs

# Enable color support
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias grep='grep --color=auto'
fi

# Useful aliases for development
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'

# Git aliases
alias gs='git status'
alias gd='git diff'
alias gl='git log --oneline -20'
alias gp='git pull'

# Claude Code prompt indicator (optional)
# This helps visually identify when you're in a Claude Code session
if [ -n "$CLAUDE_CODE" ]; then
    PS1="[\[\033[1;36m\]Claude\[\033[0m\]] $PS1"
fi
```

### Zsh Configuration

If using Zsh, add to `~/.zshrc`:

```zsh
# =============================================================================
# Zsh Configuration for Claude Code
# =============================================================================

# History settings
HISTSIZE=50000
SAVEHIST=100000
HISTFILE=~/.zsh_history
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_SAVE_NO_DUPS
setopt SHARE_HISTORY

# Better completion
autoload -Uz compinit && compinit

# Git integration
autoload -Uz vcs_info
precmd() { vcs_info }
zstyle ':vcs_info:git:*' formats '%b '
setopt PROMPT_SUBST
PROMPT='%F{cyan}%n%f:%F{blue}%~%f ${vcs_info_msg_0_}%# '

# Useful aliases
alias ll='ls -alF'
alias la='ls -A'
alias gs='git status'
alias gd='git diff'
```

## Claude Code Settings

### Official Documentation Links

- [Terminal Config](https://code.claude.com/docs/en/terminal-config) - Terminal setup
- [Settings](https://code.claude.com/docs/en/settings) - General settings
- [Keybindings](https://code.claude.com/docs/en/keybindings) - Keyboard shortcuts
- [Memory](https://code.claude.com/docs/en/memory) - Memory configuration
- [Model Config](https://code.claude.com/docs/en/model-config) - Model settings
- [Output Styles](https://code.claude.com/docs/en/output-styles) - Output formatting
- [Statusline](https://code.claude.com/docs/en/statusline) - Status line options

### Environment Variables

```bash
# Add to ~/.bashrc or ~/.zshrc

# Claude Code environment variables (if applicable)
export CLAUDE_CODE_THEME="dark"
export CLAUDE_CODE_FONT_SIZE=12
```

## Terminal Emulator Quick Reference

### Ghostty

**Installation:**
```bash
# Build from source (see ghostty-config.md for details)
```

**Key features:**
- Fast GPU-accelerated rendering
- Native platform UI
- Built-in shell integration

**Config location:** `~/.config/ghostty/config`

[Full configuration guide](./ghostty-config.md)

---

### kitty

**Installation:**
```bash
curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin
```

**Key features:**
- GPU-based rendering
- Kitten extensions
- Image protocol support

**Config location:** `~/.config/kitty/kitty.conf`

[Full configuration guide](./kitty-config.md)

---

### WezTerm

**Installation:**
```bash
curl -fsSL https://apt.fury.io/wez/gpg.key | sudo gpg --yes --dearmor -o /usr/share/keyrings/wezterm-fury.gpg
echo 'deb [signed-by=/usr/share/keyrings/wezterm-fury.gpg] https://apt.fury.io/wez/ * *' | sudo tee /etc/apt/sources.list.d/wezterm.list
sudo apt update && sudo apt install -y wezterm
```

**Key features:**
- Built-in multiplexer
- Lua configuration
- Cross-platform consistency

**Config location:** `~/.config/wezterm/wezterm.lua`

[Full configuration guide](./wezterm-config.md)

---

## Comparison Table

| Feature | Ghostty | kitty | WezTerm |
|---------|---------|-------|---------|
| GPU Acceleration | ✅ | ✅ | ✅ |
| Shell Integration | ✅ | ✅ | ✅ |
| Multiplexer | ❌ | ❌ | ✅ Built-in |
| Config Language | INI | Custom | Lua |
| Image Support | Limited | ✅ | ✅ |
| Cross-platform | Linux, macOS | Linux, macOS | Linux, macOS, Windows |
| WSLg Support | ✅ | ✅ | ✅ |

## Recommended Choice

For Claude Code on WSLg, we recommend:

1. **WezTerm** - Best overall experience with built-in multiplexer and excellent WSL support
2. **kitty** - Great performance and extensive feature set
3. **Ghostty** - Excellent for those who prefer minimal, fast terminals

## Additional Resources

- [Awesome Claude Skills](https://github.com/ComposioHQ/awesome-claude-skills)
- [Awesome Claude Code Subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
- [Awesome Claude Code](https://github.com/hesreallyhim/awesome-claude-code)
- [Claude Code GitHub Action](https://github.com/anthropics/claude-code-action)
- [Claude Code Changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
