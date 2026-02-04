# WSLg Setup and Terminal Emulators for Claude Code

This guide covers setting up WSLg (Windows Subsystem for Linux GUI) and configuring terminal emulators optimized for Claude Code development.

## Table of Contents

- [Prerequisites](#prerequisites)
- [WSLg Installation](#wslg-installation)
- [Terminal Emulators](#terminal-emulators)
  - [Ghostty](#ghostty)
  - [kitty](#kitty)
  - [WezTerm](#wezterm)
- [Claude Code Configuration](#claude-code-configuration)
- [Resources](#resources)

## Prerequisites

- Windows 10 Insiders preview build 21364 or higher, or Windows 11
- WSL 2 enabled
- GPU compute support recommended for best performance

## WSLg Installation

### New WSL Installation

If you don't have WSL installed, run from an elevated PowerShell:

```powershell
wsl --install
```

WSLg is automatically included in the initial setup.

### Existing WSL Installation

If you already have WSL installed, update to include WSLg:

```powershell
wsl --update
```

### Verify WSL Version

Ensure your distro is running WSL 2 (required for WSLg):

```powershell
wsl --list -v
```

If running WSL 1, convert to WSL 2:

```powershell
wsl --set-version <distro_name> 2
```

### Restart WSL

After updates, restart WSL:

```powershell
wsl --shutdown
```

WSL will automatically restart when you launch a WSL application.

## Terminal Emulators

### Ghostty

[Ghostty](https://github.com/ghostty-org/ghostty) is a fast, feature-rich terminal emulator built in Zig.

#### Installation on Ubuntu/Debian (WSL)

```bash
# Add Ghostty repository (if available)
# Note: Check https://github.com/ghostty-org/ghostty for latest installation instructions

# Build from source (requires Zig)
sudo apt update
sudo apt install -y build-essential pkg-config libgtk-4-dev

# Install Zig (check for latest version)
wget https://ziglang.org/download/0.11.0/zig-linux-x86_64-0.11.0.tar.xz
tar xf zig-linux-x86_64-0.11.0.tar.xz
export PATH=$PATH:$PWD/zig-linux-x86_64-0.11.0

# Clone and build Ghostty
git clone https://github.com/ghostty-org/ghostty.git
cd ghostty
zig build -Doptimize=ReleaseFast
```

#### Configuration for Claude Code

Create `~/.config/ghostty/config`:

```ini
# Font settings
font-family = "JetBrains Mono"
font-size = 12

# Terminal settings
scrollback-lines = 10000
cursor-style = block
cursor-blink = false

# Colors optimized for code
background = #1e1e2e
foreground = #cdd6f4

# Shell integration for Claude Code
shell-integration = detect
```

### kitty

[kitty](https://sw.kovidgoyal.net/kitty/) is a fast, GPU-based terminal emulator.

#### Installation on Ubuntu/Debian (WSL)

```bash
# Install via apt
sudo apt update
sudo apt install -y kitty

# Or install latest version
curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin
```

#### Configuration for Claude Code

Create `~/.config/kitty/kitty.conf`:

```conf
# Font settings
font_family      JetBrains Mono
bold_font        auto
italic_font      auto
bold_italic_font auto
font_size        12.0

# Cursor settings
cursor_shape block
cursor_blink_interval 0

# Scrollback
scrollback_lines 10000

# Performance - optimized for WSLg
sync_to_monitor yes
repaint_delay 10
input_delay 3

# Terminal bell
enable_audio_bell no

# Colors
background #1e1e2e
foreground #cdd6f4

# URL handling
url_style curly
open_url_with default

# Shell integration for Claude Code
shell_integration enabled

# Tab bar
tab_bar_style powerline
tab_powerline_style slanted
```

### WezTerm

[WezTerm](https://wezfurlong.org/wezterm/) is a GPU-accelerated cross-platform terminal emulator and multiplexer.

#### Installation on Ubuntu/Debian (WSL)

```bash
# Add WezTerm repository
curl -fsSL https://apt.fury.io/wez/gpg.key | sudo gpg --yes --dearmor -o /usr/share/keyrings/wezterm-fury.gpg
echo 'deb [signed-by=/usr/share/keyrings/wezterm-fury.gpg] https://apt.fury.io/wez/ * *' | sudo tee /etc/apt/sources.list.d/wezterm.list

# Install WezTerm
sudo apt update
sudo apt install -y wezterm
```

#### Configuration for Claude Code

Create `~/.config/wezterm/wezterm.lua`:

```lua
local wezterm = require 'wezterm'
local config = wezterm.config_builder()

-- Font settings
config.font = wezterm.font('JetBrains Mono')
config.font_size = 12.0

-- Appearance
config.color_scheme = 'Catppuccin Mocha'
config.window_background_opacity = 0.95
config.enable_tab_bar = true
config.hide_tab_bar_if_only_one_tab = true

-- Cursor settings
config.default_cursor_style = 'SteadyBlock'

-- Performance optimizations for WSLg
config.front_end = 'WebGpu'
config.webgpu_power_preference = 'HighPerformance'

-- Scrollback
config.scrollback_lines = 10000

-- Key bindings optimized for Claude Code
config.keys = {
  { key = 'v', mods = 'CTRL|SHIFT', action = wezterm.action.PasteFrom 'Clipboard' },
  { key = 'c', mods = 'CTRL|SHIFT', action = wezterm.action.CopyTo 'Clipboard' },
}

-- Shell integration
config.term = 'wezterm'

return config
```

## Claude Code Configuration

### Terminal Configuration

Configure your terminal for optimal Claude Code experience. See the official documentation:
- [Terminal Config](https://code.claude.com/docs/en/terminal-config)
- [Settings](https://code.claude.com/docs/en/settings)
- [Keybindings](https://code.claude.com/docs/en/keybindings)

### Recommended Settings

Create or update `~/.claude/settings.json`:

```json
{
  "terminal": {
    "fontSize": 12,
    "fontFamily": "JetBrains Mono, Menlo, Monaco, monospace",
    "cursorStyle": "block",
    "cursorBlink": false
  }
}
```

### Memory and Project Configuration

- [Memory](https://code.claude.com/docs/en/memory) - Configure Claude Code memory settings
- [Model Config](https://code.claude.com/docs/en/model-config) - Model configuration options
- [Output Styles](https://code.claude.com/docs/en/output-styles) - Customize output formatting
- [Statusline](https://code.claude.com/docs/en/statusline) - Status line configuration

## Resources

### Official Documentation

- [WSLg GitHub Repository](https://github.com/microsoft/wslg)
- [WSL Documentation](https://learn.microsoft.com/en-us/windows/wsl/)
- [Claude Code GitHub Action](https://github.com/anthropics/claude-code-action)
- [Claude Code Changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)

### Microsoft WSL Tutorials

- [WSL with VS Code](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-vscode)
- [WSL Database Setup](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-database)
- [WSL Git Integration](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-git)
- [Linux on WSL](https://learn.microsoft.com/en-us/windows/wsl/tutorials/linux)
- [GUI Apps on WSL](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps)
- [GPU Compute on WSL](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gpu-compute)
- [WSL Containers](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-containers)

### Development Environment

- [Node.js on WSL](https://learn.microsoft.com/en-us/windows/dev-environment/javascript/nodejs-on-wsl)
- [React on WSL](https://learn.microsoft.com/en-us/windows/dev-environment/javascript/react-on-wsl)
- [Windows AI](https://learn.microsoft.com/en-us/windows/ai/)

### WSL Configuration

- [Using Custom Distros](https://learn.microsoft.com/en-us/windows/wsl/use-custom-distro)
- [WSL Config Options](https://learn.microsoft.com/en-us/windows/wsl/wsl-config)

### Claude Code Resources

- [Awesome Claude Skills](https://github.com/ComposioHQ/awesome-claude-skills)
- [Awesome Claude Code Subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
- [Awesome Claude Code](https://github.com/hesreallyhim/awesome-claude-code)
- [Awesome ChatGPT Prompts](https://github.com/f/awesome-chatgpt-prompts)

### Terminal Emulator Projects

- [Ghostty](https://github.com/ghostty-org/ghostty)
- [kitty](https://sw.kovidgoyal.net/kitty/)
- [WezTerm](https://wezfurlong.org/wezterm/)

## Note About iTerm2

iTerm2 is a macOS-only terminal emulator and is not available for WSL/Linux. For WSL users, we recommend using Ghostty, kitty, or WezTerm as alternatives with similar features.

If you're using macOS with Claude Code, see the [iTerm2 documentation](https://iterm2.com/) for configuration options.
