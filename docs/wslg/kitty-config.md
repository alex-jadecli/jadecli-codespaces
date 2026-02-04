# kitty Terminal Configuration for Claude Code on WSLg

[kitty](https://sw.kovidgoyal.net/kitty/) is a fast, feature-rich, GPU-based terminal emulator designed for power users.

## Installation

### Prerequisites

Ensure you have WSLg properly configured. See the [main WSLg guide](./README.md) for setup instructions.

### Installing via Package Manager

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y kitty

# This may install an older version. For the latest version, use the installer below.
```

### Installing Latest Version

```bash
# Official installer (recommended)
curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin

# Add to PATH
echo 'export PATH=$PATH:~/.local/kitty.app/bin' >> ~/.bashrc
source ~/.bashrc

# Create desktop entry
cp ~/.local/kitty.app/share/applications/kitty.desktop ~/.local/share/applications/
cp ~/.local/kitty.app/share/applications/kitty-open.desktop ~/.local/share/applications/
sed -i "s|Icon=kitty|Icon=/home/$USER/.local/kitty.app/share/icons/hicolor/256x256/apps/kitty.png|g" ~/.local/share/applications/kitty*.desktop
sed -i "s|Exec=kitty|Exec=/home/$USER/.local/kitty.app/bin/kitty|g" ~/.local/share/applications/kitty*.desktop
```

## Configuration

Create the configuration directory:

```bash
mkdir -p ~/.config/kitty
```

### Complete Configuration

Create `~/.config/kitty/kitty.conf`:

```conf
# =============================================================================
# kitty Configuration for Claude Code on WSLg
# =============================================================================

# -----------------------------------------------------------------------------
# Font Settings
# -----------------------------------------------------------------------------
font_family      JetBrains Mono
bold_font        JetBrains Mono Bold
italic_font      JetBrains Mono Italic
bold_italic_font JetBrains Mono Bold Italic
font_size        12.0

# Adjust line height/width for better readability
adjust_line_height  0
adjust_column_width 0

# Disable ligatures if preferred
disable_ligatures never

# -----------------------------------------------------------------------------
# Cursor Settings
# -----------------------------------------------------------------------------
cursor_shape block
cursor_blink_interval 0
cursor_stop_blinking_after 0

# -----------------------------------------------------------------------------
# Scrollback
# -----------------------------------------------------------------------------
scrollback_lines 100000
scrollback_pager less --chop-long-lines --RAW-CONTROL-CHARS +INPUT_LINE_NUMBER
scrollback_pager_history_size 100

# -----------------------------------------------------------------------------
# Mouse
# -----------------------------------------------------------------------------
mouse_hide_wait 3.0
url_style curly
open_url_with default
url_prefixes http https file ftp gemini irc gopher mailto news git
detect_urls yes
copy_on_select clipboard
strip_trailing_spaces smart

# -----------------------------------------------------------------------------
# Terminal Bell
# -----------------------------------------------------------------------------
enable_audio_bell no
visual_bell_duration 0.0
window_alert_on_bell yes
bell_on_tab "🔔 "

# -----------------------------------------------------------------------------
# Window Settings
# -----------------------------------------------------------------------------
window_padding_width 8
placement_strategy center
hide_window_decorations no
confirm_os_window_close 0

# -----------------------------------------------------------------------------
# Tab Bar
# -----------------------------------------------------------------------------
tab_bar_edge top
tab_bar_style powerline
tab_powerline_style slanted
tab_title_template "{index}: {title}"
active_tab_title_template "{index}: {title} *"

# -----------------------------------------------------------------------------
# Color Scheme - Catppuccin Mocha
# -----------------------------------------------------------------------------
# The basic colors
foreground              #cdd6f4
background              #1e1e2e
selection_foreground    #1e1e2e
selection_background    #f5e0dc

# Cursor colors
cursor                  #f5e0dc
cursor_text_color       #1e1e2e

# URL underline color when hovering with mouse
url_color               #f5e0dc

# Kitty window border colors
active_border_color     #b4befe
inactive_border_color   #6c7086
bell_border_color       #f9e2af

# Tab bar colors
active_tab_foreground   #11111b
active_tab_background   #cba6f7
inactive_tab_foreground #cdd6f4
inactive_tab_background #181825
tab_bar_background      #11111b

# Colors for marks (marked text in the terminal)
mark1_foreground #1e1e2e
mark1_background #b4befe
mark2_foreground #1e1e2e
mark2_background #cba6f7
mark3_foreground #1e1e2e
mark3_background #74c7ec

# The 16 terminal colors

# black
color0 #45475a
color8 #585b70

# red
color1 #f38ba8
color9 #f38ba8

# green
color2  #a6e3a1
color10 #a6e3a1

# yellow
color3  #f9e2af
color11 #f9e2af

# blue
color4  #89b4fa
color12 #89b4fa

# magenta
color5  #f5c2e7
color13 #f5c2e7

# cyan
color6  #94e2d5
color14 #94e2d5

# white
color7  #bac2de
color15 #a6adc8

# -----------------------------------------------------------------------------
# Performance - Optimized for WSLg
# -----------------------------------------------------------------------------
repaint_delay 10
input_delay 3
sync_to_monitor yes

# GPU rendering
# kitty uses GPU by default, but can fall back to software if needed

# -----------------------------------------------------------------------------
# Shell Integration
# -----------------------------------------------------------------------------
shell_integration enabled

# -----------------------------------------------------------------------------
# Keyboard Shortcuts
# -----------------------------------------------------------------------------

# Clear default shortcuts (optional)
# clear_all_shortcuts no

# Clipboard
map ctrl+shift+c copy_to_clipboard
map ctrl+shift+v paste_from_clipboard

# Font size
map ctrl+shift+equal change_font_size all +1.0
map ctrl+shift+minus change_font_size all -1.0
map ctrl+shift+backspace change_font_size all 0

# Scrolling
map ctrl+shift+up        scroll_line_up
map ctrl+shift+down      scroll_line_down
map ctrl+shift+page_up   scroll_page_up
map ctrl+shift+page_down scroll_page_down
map ctrl+shift+home      scroll_home
map ctrl+shift+end       scroll_end
map ctrl+shift+h         show_scrollback

# Tab management
map ctrl+shift+t new_tab
map ctrl+shift+w close_tab
map ctrl+shift+right next_tab
map ctrl+shift+left  previous_tab
map ctrl+shift+. move_tab_forward
map ctrl+shift+, move_tab_backward
map ctrl+shift+alt+t set_tab_title

# Window management
map ctrl+shift+enter new_window
map ctrl+shift+n new_os_window
map ctrl+shift+] next_window
map ctrl+shift+[ previous_window
map ctrl+shift+f move_window_forward
map ctrl+shift+b move_window_backward
map ctrl+shift+` move_window_to_top
map ctrl+shift+r start_resizing_window
map ctrl+shift+1 first_window
map ctrl+shift+2 second_window
map ctrl+shift+3 third_window
map ctrl+shift+4 fourth_window
map ctrl+shift+5 fifth_window

# Layout management
map ctrl+shift+l next_layout

# Search (requires fzf: sudo apt install fzf)
# Alternative: Use kitty's built-in search with ctrl+shift+h to view scrollback
map ctrl+shift+/ launch --type=overlay --stdin-source=@screen_scrollback fzf --no-sort --no-mouse -i

# Hints (for quick URL/path selection)
map ctrl+shift+e open_url_with_hints
map ctrl+shift+p>f kitten hints --type path --program -
map ctrl+shift+p>shift+f kitten hints --type path
map ctrl+shift+p>l kitten hints --type line --program -
map ctrl+shift+p>w kitten hints --type word --program -
map ctrl+shift+p>h kitten hints --type hash --program -

# -----------------------------------------------------------------------------
# Advanced Features
# -----------------------------------------------------------------------------

# Remote control (useful for scripting)
allow_remote_control socket-only
listen_on unix:/tmp/kitty

# Term info
term xterm-kitty
```

### Claude Code Specific Optimizations

For the best Claude Code experience, ensure these settings are included:

```conf
# Large scrollback for reviewing long Claude Code outputs
scrollback_lines 100000
scrollback_pager_history_size 100

# Fast response
repaint_delay 10
input_delay 3

# Shell integration for proper command tracking
shell_integration enabled

# No cursor blink for focus
cursor_blink_interval 0
```

## Launching kitty in WSLg

After installation, launch kitty:

```bash
kitty &
```

Or with a specific configuration:

```bash
kitty --config ~/.config/kitty/kitty.conf &
```

## kitty Kitten Extensions

kitty includes powerful extensions called "kittens":

### SSH Kitten

For seamless SSH with full terminal features:

```bash
kitty +kitten ssh user@hostname
```

### Diff Kitten

For visual diffs:

```bash
kitty +kitten diff file1 file2
```

### Unicode Input

```bash
kitty +kitten unicode_input
```

## Troubleshooting

### Display Issues in WSLg

If kitty doesn't display properly:

```bash
# Check DISPLAY is set
echo $DISPLAY

# Try explicit display
DISPLAY=:0 kitty
```

### GPU Acceleration Issues

```bash
# Check OpenGL support
glxinfo | grep "OpenGL version"

# Force software rendering if needed (add to kitty.conf)
# linux_display_server wayland
```

### Font Issues

```bash
# Install JetBrains Mono
sudo apt install -y fonts-jetbrains-mono

# List available fonts
kitty +list-fonts | grep -i jetbrains

# Rebuild font cache
fc-cache -fv
```

### Performance Tuning

For slower systems, try:

```conf
# Add to kitty.conf
repaint_delay 20
input_delay 5
sync_to_monitor no
```

## Useful Commands

```bash
# Reload configuration
kitty @ set-colors --all --configured ~/.config/kitty/kitty.conf

# List all shortcuts
kitty --debug-keyboard

# Check kitty version
kitty --version
```

## References

- [kitty Documentation](https://sw.kovidgoyal.net/kitty/)
- [kitty GitHub](https://github.com/kovidgoyal/kitty)
- [kitty FAQ](https://sw.kovidgoyal.net/kitty/faq/)
- [kitty Themes](https://github.com/dexpota/kitty-themes)
