# Terminal & Development Environment Summary

Optimized for LLM consumption. Essential setup for WSL2 development.

## Environment Stack

```
Windows 11
    ↓
WSL2 (Ubuntu 26.04)
    ↓
Terminal Emulator (Kitty/Ghostty/WezTerm)
    ↓
Claude Code IDE or Shell (zsh)
    ↓
Tools (uv, ruff, ty, git, etc.)
```

---

## WSL2 Basics

**What:** Windows Subsystem for Linux - native Linux on Windows

**Key Features:**
- Native filesystem access (drive integration)
- GPU support (WSLg)
- GUI app rendering on Windows
- Performance nearly equals native Linux

**Allocation:** ~96GB RAM allocated by default (configurable in .wslconfig)

**Important Paths:**
- Windows from WSL: `/mnt/c/Users/...`
- WSL from Windows: `\\wsl.localhost\Ubuntu\home\...`

---

## Terminal Emulator Choices

### Kitty
**Strengths:** GPU-accelerated, modern features, extremely fast

**Key Config:**
```
font_family: "Droid Sans Mono"
font_size: 12
enable_ligatures: yes
mouse_hide_wait: 3
```

**Best For:** High-performance work, many split panes

### Ghostty
**Strengths:** Fast, modern, simple configuration

**Key Features:**
- Quick launch
- Minimal config
- Good macOS/Windows parity

**Best For:** Quick iteration, minimal complexity

### WezTerm
**Strengths:** Powerful Lua config, multiplexing, cross-platform

**Key Feature:** Lua scripting for advanced customization

**Best For:** Advanced users, complex workflows

### Claude Code IDE Terminal
**Strengths:** Integrated into IDE, context-aware

**Configured Via:**
- Terminal settings in Claude Code
- Font, colors, keybindings
- Right-click context menus

**Best For:** IDE-based development

---

## Shell Configuration

**Primary Shell:** zsh

**Plugin Manager:** zinit (plugin manager, completions, themes)

**Prompt:** Starship (fast, customizable, shows Git status)

**Common Tools:**
- `eza` - ls replacement
- `bat` - cat with syntax highlighting
- `fd` - find replacement
- `rg` (ripgrep) - grep replacement
- `fzf` - fuzzy finder
- `zoxide` - smart cd history

---

## Development Setup

### Python Tools

**Package Manager:** uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
```

**Type Checker:** ty
```bash
uv add --dev ty
```

**Linter/Formatter:** ruff
```bash
uv add --dev ruff
```

### Node.js Tools

**Version Manager:** mise
```bash
mise install node@22
```

**Package Manager:** npm (built-in with Node)

### Docker

**For:** Local services (PostgreSQL, MongoDB, Redis)

**Start:** `docker compose up -d` (from jadecli-infra project)

---

## File System Integration

**Key Locations:**

| Path | Purpose |
|------|---------|
| `/home/alex-jadecli` | WSL home directory |
| `/mnt/c/Users/alex` | Windows home |
| `~/.claude` | Claude Code config |
| `~/.jade` | Jade ecosystem config |
| `~/projects` | Source code |

**Performance Notes:**
- Use WSL filesystem when possible (faster)
- Avoid accessing Windows filesystem for intensive work
- IDE files should be on WSL side

---

## GPU Support (WSLg)

**Available:** RTX 2080 Ti 11GB VRAM

**Use Cases:**
- GPU-accelerated terminal rendering (Kitty)
- CUDA for ML workloads
- Ollama for local LLMs

**Check GPU:**
```bash
nvidia-smi
# Shows GPU utilization
```

---

## Configuration Management

**Tool:** Chezmoi (dotfiles management)

**Key Concepts:**
- Store dotfiles in Git
- Templates for machine-specific config
- Encryption support (AGE)

**Setup:**
```bash
chezmoi init https://github.com/user/dotfiles.git
chezmoi apply
```

**Managed Files:**
- .zshrc
- .vimrc
- Terminal configs
- IDE settings

---

## IDE Integration

### Claude Code

**Terminal Access:**
- Integrated terminal (Ctrl+`)
- Multiple split terminals
- Environment inherits project context

**Settings Sync:**
- Workspace-level settings
- Project-level settings
- User global settings

**Useful Commands:**
- Cmd+K: Open command palette
- Cmd+P: Quick file open
- Ctrl+`: Toggle terminal

### VS Code

**Extensions:**
- Python (Pylance)
- Ruff (linting)
- GitLens
- Remote - SSH (for remote dev)

**Integration:**
- Linting: Real-time with ruff
- Type checking: Real-time with ty
- Formatting: On save with ruff

---

## Fonts

**Recommended:** Monospace fonts with ligatures

**Options:**
- Droid Sans Mono
- Fira Code
- JetBrains Mono
- Meslo Nerd Font

**Install in Terminal Config:**
```
font_family = "JetBrains Mono"
font_size = 12
```

---

## Performance Tuning

### WSL2 Config (.wslconfig)

```ini
[wsl2]
memory=96GB
processors=12
swap=0
localhostForwarding=true
```

### Terminal Performance

- **Kitty:** Fastest rendering, GPU acceleration
- **Ghostty:** Good balance of speed and simplicity
- **WezTerm:** Slower but more customizable

### Caching

- UV caches packages: `~/.cache/uv`
- Docker images: `/var/lib/docker`
- Clear if low disk: `uv cache prune`

---

## Common Workflows

### Opening New Project

```bash
# 1. Navigate to project
cd ~/projects/my-project

# 2. Claude Code opens it
claude .

# 3. Terminal ready with environment
uv sync  # Install dependencies
ruff check .  # Check quality
```

### Switching Terminal Emulator

```bash
# 1. Choose new emulator (Kitty, Ghostty, WezTerm)
# 2. Copy config file to home directory
# 3. Customize as needed
# 4. Restart terminal
```

### Managing Dotfiles

```bash
# 1. Add file to chezmoi
chezmoi add ~/.vimrc

# 2. Make changes
chezmoi edit ~/.vimrc

# 3. Apply across machines
chezmoi apply
```

---

## Troubleshooting

**GPU not detected:**
```bash
# Check driver
nvidia-smi

# Update WSL kernel
wsl --update
```

**Slow file access:**
- Avoid `/mnt/c/...` for intensive work
- Keep projects on WSL side (`~/projects`)

**Terminal not rendering:**
- Upgrade WSL: `wsl --update`
- Reinstall terminal emulator

**Dotfiles out of sync:**
```bash
# Pull latest
chezmoi git pull

# Apply
chezmoi apply
```

---

## Token Count: ~850 tokens

Used for: Setup guides, troubleshooting decisions, environment validation.
