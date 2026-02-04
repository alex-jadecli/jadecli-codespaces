# WezTerm Configuration for Claude Code on WSLg

[WezTerm](https://wezfurlong.org/wezterm/) is a powerful, GPU-accelerated cross-platform terminal emulator and multiplexer written in Rust.

## Installation

### Prerequisites

Ensure you have WSLg properly configured. See the [main WSLg guide](./README.md) for setup instructions.

### Installing via Package Manager

```bash
# Add WezTerm repository
curl -fsSL https://apt.fury.io/wez/gpg.key | sudo gpg --yes --dearmor -o /usr/share/keyrings/wezterm-fury.gpg
echo 'deb [signed-by=/usr/share/keyrings/wezterm-fury.gpg] https://apt.fury.io/wez/ * *' | sudo tee /etc/apt/sources.list.d/wezterm.list

# Install WezTerm
sudo apt update
sudo apt install -y wezterm
```

### Installing from GitHub Releases

```bash
# Download latest release (check https://github.com/wez/wezterm/releases for version)
cd /tmp
wget https://github.com/wez/wezterm/releases/download/20230712-072601-f4abf8fd/wezterm-20230712-072601-f4abf8fd.Ubuntu22.04.deb
sudo dpkg -i wezterm-*.deb
sudo apt install -f -y
```

### Building from Source

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# Install dependencies
sudo apt install -y cmake libfontconfig1-dev libfreetype6-dev libxcb-render0-dev \
    libxcb-shape0-dev libxcb-xfixes0-dev libxkbcommon-dev libssl-dev \
    libwayland-dev libwayland-egl-backend-dev

# Clone and build
git clone --depth=1 --branch=main https://github.com/wez/wezterm.git
cd wezterm
git submodule update --init --recursive
cargo build --release
sudo cp target/release/wezterm /usr/local/bin/
```

## Configuration

WezTerm uses Lua for configuration. Create the configuration directory:

```bash
mkdir -p ~/.config/wezterm
```

### Complete Configuration

Create `~/.config/wezterm/wezterm.lua`:

```lua
-- =============================================================================
-- WezTerm Configuration for Claude Code on WSLg
-- =============================================================================

local wezterm = require 'wezterm'
local act = wezterm.action
local config = wezterm.config_builder()

-- =============================================================================
-- Font Configuration
-- =============================================================================
config.font = wezterm.font_with_fallback {
  'JetBrains Mono',
  'Noto Color Emoji',
  'Symbols Nerd Font',
}
config.font_size = 12.0
config.line_height = 1.0
config.cell_width = 1.0

-- Font rendering
config.freetype_load_target = 'Light'
config.freetype_render_target = 'HorizontalLcd'

-- =============================================================================
-- Appearance
-- =============================================================================
-- Color scheme - Catppuccin Mocha
config.color_scheme = 'Catppuccin Mocha'

-- Or define custom colors
config.colors = {
  foreground = '#cdd6f4',
  background = '#1e1e2e',
  cursor_bg = '#f5e0dc',
  cursor_fg = '#1e1e2e',
  cursor_border = '#f5e0dc',
  selection_fg = '#1e1e2e',
  selection_bg = '#f5e0dc',
  scrollbar_thumb = '#585b70',
  split = '#6c7086',
  
  ansi = {
    '#45475a', -- black
    '#f38ba8', -- red
    '#a6e3a1', -- green
    '#f9e2af', -- yellow
    '#89b4fa', -- blue
    '#f5c2e7', -- magenta
    '#94e2d5', -- cyan
    '#bac2de', -- white
  },
  brights = {
    '#585b70', -- bright black
    '#f38ba8', -- bright red
    '#a6e3a1', -- bright green
    '#f9e2af', -- bright yellow
    '#89b4fa', -- bright blue
    '#f5c2e7', -- bright magenta
    '#94e2d5', -- bright cyan
    '#a6adc8', -- bright white
  },
  
  tab_bar = {
    background = '#11111b',
    active_tab = {
      bg_color = '#cba6f7',
      fg_color = '#11111b',
    },
    inactive_tab = {
      bg_color = '#181825',
      fg_color = '#cdd6f4',
    },
    inactive_tab_hover = {
      bg_color = '#313244',
      fg_color = '#cdd6f4',
    },
    new_tab = {
      bg_color = '#181825',
      fg_color = '#cdd6f4',
    },
    new_tab_hover = {
      bg_color = '#313244',
      fg_color = '#cdd6f4',
    },
  },
}

-- Window appearance
config.window_background_opacity = 0.95
config.window_padding = {
  left = 8,
  right = 8,
  top = 8,
  bottom = 8,
}
config.window_decorations = 'RESIZE'
config.initial_cols = 120
config.initial_rows = 30

-- =============================================================================
-- Cursor Configuration
-- =============================================================================
config.default_cursor_style = 'SteadyBlock'
config.cursor_blink_rate = 0
config.cursor_blink_ease_in = 'Constant'
config.cursor_blink_ease_out = 'Constant'

-- =============================================================================
-- Tab Bar Configuration
-- =============================================================================
config.enable_tab_bar = true
config.hide_tab_bar_if_only_one_tab = false
config.tab_bar_at_bottom = false
config.use_fancy_tab_bar = true
config.tab_max_width = 25

-- =============================================================================
-- Scrollback Configuration
-- =============================================================================
config.scrollback_lines = 100000
config.enable_scroll_bar = true

-- =============================================================================
-- Performance - Optimized for WSLg
-- =============================================================================
-- Use WebGpu for best performance (fall back to OpenGL if needed)
config.front_end = 'WebGpu'
config.webgpu_power_preference = 'HighPerformance'

-- If WebGpu doesn't work, try:
-- config.front_end = 'OpenGL'

-- Animation settings
config.animation_fps = 60
config.max_fps = 60

-- =============================================================================
-- Shell Integration
-- =============================================================================
config.term = 'wezterm'
config.set_environment_variables = {
  TERM = 'wezterm',
}

-- Default shell
config.default_prog = { '/bin/bash', '-l' }

-- =============================================================================
-- Key Bindings
-- =============================================================================
config.keys = {
  -- Copy/Paste
  { key = 'c', mods = 'CTRL|SHIFT', action = act.CopyTo 'Clipboard' },
  { key = 'v', mods = 'CTRL|SHIFT', action = act.PasteFrom 'Clipboard' },
  
  -- Font size
  { key = '=', mods = 'CTRL', action = act.IncreaseFontSize },
  { key = '-', mods = 'CTRL', action = act.DecreaseFontSize },
  { key = '0', mods = 'CTRL', action = act.ResetFontSize },
  
  -- Tab management
  { key = 't', mods = 'CTRL|SHIFT', action = act.SpawnTab 'CurrentPaneDomain' },
  { key = 'w', mods = 'CTRL|SHIFT', action = act.CloseCurrentTab { confirm = false } },
  { key = 'Tab', mods = 'CTRL', action = act.ActivateTabRelative(1) },
  { key = 'Tab', mods = 'CTRL|SHIFT', action = act.ActivateTabRelative(-1) },
  
  -- Direct tab access
  { key = '1', mods = 'ALT', action = act.ActivateTab(0) },
  { key = '2', mods = 'ALT', action = act.ActivateTab(1) },
  { key = '3', mods = 'ALT', action = act.ActivateTab(2) },
  { key = '4', mods = 'ALT', action = act.ActivateTab(3) },
  { key = '5', mods = 'ALT', action = act.ActivateTab(4) },
  { key = '6', mods = 'ALT', action = act.ActivateTab(5) },
  { key = '7', mods = 'ALT', action = act.ActivateTab(6) },
  { key = '8', mods = 'ALT', action = act.ActivateTab(7) },
  { key = '9', mods = 'ALT', action = act.ActivateTab(-1) },
  
  -- Pane management
  { key = '|', mods = 'CTRL|SHIFT', action = act.SplitHorizontal { domain = 'CurrentPaneDomain' } },
  { key = '_', mods = 'CTRL|SHIFT', action = act.SplitVertical { domain = 'CurrentPaneDomain' } },
  { key = 'z', mods = 'CTRL|SHIFT', action = act.TogglePaneZoomState },
  
  -- Pane navigation
  { key = 'LeftArrow', mods = 'CTRL|SHIFT', action = act.ActivatePaneDirection 'Left' },
  { key = 'RightArrow', mods = 'CTRL|SHIFT', action = act.ActivatePaneDirection 'Right' },
  { key = 'UpArrow', mods = 'CTRL|SHIFT', action = act.ActivatePaneDirection 'Up' },
  { key = 'DownArrow', mods = 'CTRL|SHIFT', action = act.ActivatePaneDirection 'Down' },
  
  -- Scrolling
  { key = 'PageUp', mods = 'SHIFT', action = act.ScrollByPage(-1) },
  { key = 'PageDown', mods = 'SHIFT', action = act.ScrollByPage(1) },
  { key = 'Home', mods = 'SHIFT', action = act.ScrollToTop },
  { key = 'End', mods = 'SHIFT', action = act.ScrollToBottom },
  
  -- Search
  { key = 'f', mods = 'CTRL|SHIFT', action = act.Search { CaseSensitiveString = '' } },
  
  -- Quick select mode (for URLs, paths, etc.)
  { key = 'Space', mods = 'CTRL|SHIFT', action = act.QuickSelect },
  
  -- Command palette
  { key = 'p', mods = 'CTRL|SHIFT', action = act.ActivateCommandPalette },
  
  -- Debug overlay
  { key = 'l', mods = 'CTRL|SHIFT', action = act.ShowDebugOverlay },
  
  -- Reload config
  { key = 'r', mods = 'CTRL|SHIFT', action = act.ReloadConfiguration },
}

-- =============================================================================
-- Mouse Bindings
-- =============================================================================
config.mouse_bindings = {
  -- Right click paste
  {
    event = { Down = { streak = 1, button = 'Right' } },
    mods = 'NONE',
    action = act.PasteFrom 'Clipboard',
  },
  -- Ctrl+Click to open URLs
  {
    event = { Up = { streak = 1, button = 'Left' } },
    mods = 'CTRL',
    action = act.OpenLinkAtMouseCursor,
  },
}

-- =============================================================================
-- Quick Select Patterns (for selecting URLs, paths, etc.)
-- =============================================================================
config.quick_select_patterns = {
  -- Git hashes
  '[0-9a-f]{7,40}',
  -- URLs
  'https?://[^\\s]+',
  -- File paths
  '[\\w\\-\\.]+/[\\w\\-\\./]+',
  -- IP addresses
  '\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}',
  -- UUIDs
  '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
}

-- =============================================================================
-- Hyperlink Rules
-- =============================================================================
config.hyperlink_rules = wezterm.default_hyperlink_rules()

-- Add custom rules
table.insert(config.hyperlink_rules, {
  regex = [[\b[A-Za-z0-9_-]+/[A-Za-z0-9_-]+#\d+\b]],
  format = 'https://github.com/$0',
})

-- =============================================================================
-- SSH Configuration
-- =============================================================================
-- WezTerm has built-in SSH support with multiplexing
-- Use with: wezterm connect SSH:hostname

-- =============================================================================
-- Multiplexer Configuration
-- =============================================================================
config.unix_domains = {
  {
    name = 'unix',
  },
}

-- =============================================================================
-- Status Bar (right side)
-- =============================================================================
wezterm.on('update-right-status', function(window, pane)
  local date = wezterm.strftime '%Y-%m-%d %H:%M'
  
  window:set_right_status(wezterm.format {
    { Text = date },
  })
end)

return config
```

### Claude Code Specific Optimizations

The configuration above includes these Claude Code optimizations:

```lua
-- Large scrollback for reviewing long outputs
config.scrollback_lines = 100000

-- No cursor blink for focus
config.default_cursor_style = 'SteadyBlock'
config.cursor_blink_rate = 0

-- High performance rendering
config.front_end = 'WebGpu'
config.webgpu_power_preference = 'HighPerformance'

-- Shell integration
config.term = 'wezterm'
```

## Launching WezTerm in WSLg

After installation, launch WezTerm:

```bash
wezterm &
```

Or start with a specific configuration:

```bash
wezterm --config-file ~/.config/wezterm/wezterm.lua &
```

## WezTerm Features for Claude Code

### Built-in Multiplexer

WezTerm includes a multiplexer similar to tmux:

```bash
# Start a new multiplexer session
wezterm connect unix

# List sessions
wezterm cli list
```

### Quick Select Mode

Press `Ctrl+Shift+Space` to enter quick select mode for rapid selection of:
- URLs
- File paths
- Git hashes
- IP addresses

### Command Palette

Press `Ctrl+Shift+P` to open the command palette for quick access to all features.

### Search

Press `Ctrl+Shift+F` to search within the scrollback buffer.

## Troubleshooting

### Display Issues in WSLg

```bash
# Check DISPLAY
echo $DISPLAY

# Try explicit display
DISPLAY=:0 wezterm
```

### GPU/Rendering Issues

If WebGpu doesn't work, try OpenGL:

```lua
-- In wezterm.lua
config.front_end = 'OpenGL'
```

Or force software rendering:

```lua
config.front_end = 'Software'
```

### Font Issues

```bash
# Install JetBrains Mono
sudo apt install -y fonts-jetbrains-mono

# List available fonts in WezTerm
wezterm ls-fonts

# Check for specific font
wezterm ls-fonts --text "ABC"
```

### Configuration Debugging

```bash
# Validate configuration
wezterm show-keys

# Check for errors
wezterm --config-file ~/.config/wezterm/wezterm.lua

# Enable debug overlay (Ctrl+Shift+L in WezTerm)
```

### Performance Issues

For slower systems:

```lua
config.animation_fps = 30
config.max_fps = 30
config.front_end = 'OpenGL'
```

## Useful Commands

```bash
# Version info
wezterm --version

# List available color schemes
wezterm ls-colors

# List key bindings
wezterm show-keys

# Connect to remote host with multiplexing
wezterm connect SSH:user@hostname

# Spawn new window with specific working directory
wezterm start --cwd /path/to/directory
```

## References

- [WezTerm Documentation](https://wezfurlong.org/wezterm/)
- [WezTerm GitHub](https://github.com/wez/wezterm)
- [WezTerm Configuration Reference](https://wezfurlong.org/wezterm/config/files.html)
- [WezTerm Color Schemes](https://wezfurlong.org/wezterm/colorschemes/index.html)
