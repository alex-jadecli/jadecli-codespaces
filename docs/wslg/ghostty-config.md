# Ghostty Terminal Configuration for Claude Code on WSLg

[Ghostty](https://github.com/ghostty-org/ghostty) is a fast, feature-rich, and cross-platform terminal emulator that uses platform-native UI and GPU acceleration.

## Installation

### Prerequisites

Ensure you have WSLg properly configured. See the [main WSLg guide](./README.md) for setup instructions.

### Building from Source

Ghostty requires Zig to build:

```bash
# Install dependencies
sudo apt update
sudo apt install -y build-essential pkg-config libgtk-4-dev libadwaita-1-dev

# Install Zig (check https://ziglang.org/download/ for latest version)
cd /tmp
wget https://ziglang.org/download/0.11.0/zig-linux-x86_64-0.11.0.tar.xz
tar xf zig-linux-x86_64-0.11.0.tar.xz
sudo mv zig-linux-x86_64-0.11.0 /opt/zig
echo 'export PATH=$PATH:/opt/zig' >> ~/.bashrc
source ~/.bashrc

# Clone and build Ghostty
cd ~
git clone https://github.com/ghostty-org/ghostty.git
cd ghostty
zig build -Doptimize=ReleaseFast

# Install
sudo cp zig-out/bin/ghostty /usr/local/bin/
```

## Configuration

Create the configuration directory:

```bash
mkdir -p ~/.config/ghostty
```

### Basic Configuration

Create `~/.config/ghostty/config`:

```ini
# =============================================================================
# Ghostty Configuration for Claude Code on WSLg
# =============================================================================

# -----------------------------------------------------------------------------
# Font Settings
# -----------------------------------------------------------------------------
font-family = "JetBrains Mono"
font-size = 12
font-thicken = true

# Fallback fonts for special characters
font-family-bold = "JetBrains Mono Bold"
font-family-italic = "JetBrains Mono Italic"
font-family-bold-italic = "JetBrains Mono Bold Italic"

# -----------------------------------------------------------------------------
# Terminal Settings
# -----------------------------------------------------------------------------
scrollback-lines = 50000
cursor-style = block
cursor-blink = false
mouse-hide-while-typing = true

# -----------------------------------------------------------------------------
# Window Settings
# -----------------------------------------------------------------------------
window-padding-x = 8
window-padding-y = 8
window-decoration = true
window-title-font-family = "JetBrains Mono"
confirm-close-surface = false

# -----------------------------------------------------------------------------
# Colors - Catppuccin Mocha Theme
# -----------------------------------------------------------------------------
background = #1e1e2e
foreground = #cdd6f4
selection-background = #45475a
selection-foreground = #cdd6f4

# Normal colors
palette = 0=#45475a
palette = 1=#f38ba8
palette = 2=#a6e3a1
palette = 3=#f9e2af
palette = 4=#89b4fa
palette = 5=#f5c2e7
palette = 6=#94e2d5
palette = 7=#bac2de

# Bright colors
palette = 8=#585b70
palette = 9=#f38ba8
palette = 10=#a6e3a1
palette = 11=#f9e2af
palette = 12=#89b4fa
palette = 13=#f5c2e7
palette = 14=#94e2d5
palette = 15=#a6adc8

# -----------------------------------------------------------------------------
# Performance - Optimized for WSLg
# -----------------------------------------------------------------------------
gtk-single-instance = true
gtk-tabs-location = top

# GPU acceleration
# Note: Ensure GPU passthrough is enabled in WSL
# See: https://learn.microsoft.com/en-us/windows/wsl/tutorials/gpu-compute

# -----------------------------------------------------------------------------
# Shell Integration
# -----------------------------------------------------------------------------
shell-integration = detect
shell-integration-features = cursor,sudo,title

# -----------------------------------------------------------------------------
# Keybindings
# -----------------------------------------------------------------------------
# Copy/Paste
keybind = ctrl+shift+c=copy_to_clipboard
keybind = ctrl+shift+v=paste_from_clipboard

# Font size adjustment
keybind = ctrl+plus=increase_font_size:1
keybind = ctrl+minus=decrease_font_size:1
keybind = ctrl+0=reset_font_size

# Tab management
keybind = ctrl+shift+t=new_tab
keybind = ctrl+shift+w=close_surface
keybind = ctrl+tab=next_tab
keybind = ctrl+shift+tab=previous_tab

# Split panes
keybind = ctrl+shift+enter=new_split:right
keybind = ctrl+shift+alt+enter=new_split:down

# Navigation
keybind = ctrl+shift+up=scroll_page_up
keybind = ctrl+shift+down=scroll_page_down
keybind = ctrl+shift+home=scroll_to_top
keybind = ctrl+shift+end=scroll_to_bottom
```

### Claude Code Optimized Settings

For the best Claude Code experience, add these additional settings:

```ini
# -----------------------------------------------------------------------------
# Claude Code Optimizations
# -----------------------------------------------------------------------------

# Large scrollback for reviewing long outputs
scrollback-lines = 100000

# Disable cursor blinking for focus
cursor-blink = false

# Enable mouse support for scrolling through output
mouse-scroll-multiplier = 3

# Quick response time
repaint-delay = 10

# Shell integration for better command tracking
shell-integration = detect
```

## Launching Ghostty in WSLg

After installation, launch Ghostty:

```bash
ghostty &
```

Or create a desktop entry for easy access:

```bash
cat > ~/.local/share/applications/ghostty.desktop << 'EOF'
[Desktop Entry]
Name=Ghostty
Comment=Fast GPU-accelerated terminal
Exec=/usr/local/bin/ghostty
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=System;TerminalEmulator;
EOF
```

## Troubleshooting

### GPU Acceleration Issues

If GPU acceleration isn't working:

1. Verify GPU passthrough is enabled in WSL:
   ```bash
   nvidia-smi  # For NVIDIA GPUs
   ```

2. Check WSLg is functioning:
   ```bash
   echo $DISPLAY
   # Should output something like :0
   ```

3. Fall back to software rendering if needed:
   ```ini
   # Add to ~/.config/ghostty/config
   gtk-renderer = broadway
   ```

### Font Issues

If fonts aren't rendering correctly:

```bash
# Install JetBrains Mono
sudo apt install -y fonts-jetbrains-mono

# Or download and install manually
cd /tmp
wget https://github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip
unzip JetBrainsMono-2.304.zip -d jetbrains-mono
sudo mkdir -p /usr/share/fonts/truetype/jetbrains-mono
sudo cp jetbrains-mono/fonts/ttf/*.ttf /usr/share/fonts/truetype/jetbrains-mono/
sudo fc-cache -fv
```

## References

- [Ghostty GitHub](https://github.com/ghostty-org/ghostty)
- [Ghostty Documentation](https://ghostty.org/docs)
- [WSLg GPU Compute](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gpu-compute)
