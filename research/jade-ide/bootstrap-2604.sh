#!/usr/bin/env bash
# ---
# entity_id: script-bootstrap-2604
# entity_name: Ubuntu 26.04 Bootstrap Script for Jade IDE Development
# entity_type_id: script
# entity_path: research/jade-ide/bootstrap-2604.sh
# entity_language: bash
# entity_state: active
# entity_created: 2026-01-23T00:00:00Z
# entity_exports: [setup_mise, setup_uv, setup_claude_code, setup_ollama]
# entity_dependencies: [curl, git]
# entity_actors: [dev]
# ---

#==============================================================================
# UBUNTU 26.04 BOOTSTRAP SCRIPT
# For Jade IDE Development Environment
#==============================================================================
# System Requirements:
#   - Windows 10/11 with WSL2
#   - Ubuntu 26.04 LTS
#   - 128 GB RAM (96GB allocated to WSL)
#   - 11 GB VRAM (NVIDIA GPU)
#   - 24 CPU threads (20 allocated to WSL)
#==============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

#==============================================================================
# PHASE 0: PREREQUISITES CHECK
#==============================================================================

check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check if running in WSL
    if ! grep -qi microsoft /proc/version 2>/dev/null; then
        log_warn "Not running in WSL. Some configurations may not apply."
    fi

    # Check Ubuntu version
    if [[ -f /etc/os-release ]]; then
        source /etc/os-release
        log_info "Detected: $PRETTY_NAME"
    fi

    # Check for sudo
    if ! command -v sudo &> /dev/null; then
        log_error "sudo is required. Please install it first."
        exit 1
    fi

    log_success "Prerequisites check passed"
}

#==============================================================================
# PHASE 1: SYSTEM UPDATE & ESSENTIALS
#==============================================================================

setup_system_essentials() {
    log_info "Updating system and installing essentials..."

    sudo apt-get update
    sudo apt-get upgrade -y

    # Essential build tools
    sudo apt-get install -y \
        build-essential \
        curl \
        wget \
        git \
        unzip \
        jq \
        ripgrep \
        fd-find \
        bat \
        fzf \
        htop \
        tmux \
        zsh \
        tree \
        ca-certificates \
        gnupg \
        lsb-release

    log_success "System essentials installed"
}

#==============================================================================
# PHASE 2: MISE (Polyglot Version Manager)
#==============================================================================

setup_mise() {
    log_info "Installing mise (polyglot version manager)..."

    # Install mise
    curl https://mise.run | sh

    # Add to shell profile
    if [[ -f ~/.bashrc ]]; then
        if ! grep -q 'mise activate' ~/.bashrc; then
            echo 'eval "$(~/.local/bin/mise activate bash)"' >> ~/.bashrc
        fi
    fi

    if [[ -f ~/.zshrc ]]; then
        if ! grep -q 'mise activate' ~/.zshrc; then
            echo 'eval "$(~/.local/bin/mise activate zsh)"' >> ~/.zshrc
        fi
    fi

    # Source mise for current session
    export PATH="$HOME/.local/bin:$PATH"
    eval "$(~/.local/bin/mise activate bash)"

    log_success "mise installed"

    # Install common runtimes
    log_info "Installing Node.js and Python via mise..."
    mise use --global node@lts
    mise use --global python@3.12

    log_success "Node.js and Python installed via mise"
}

#==============================================================================
# PHASE 3: UV (Fast Python Package Manager)
#==============================================================================

setup_uv() {
    log_info "Installing uv (Astral's fast Python package manager)..."

    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Add to PATH
    export PATH="$HOME/.local/bin:$PATH"

    # Verify installation
    if command -v uv &> /dev/null; then
        log_success "uv installed: $(uv --version)"
    else
        log_error "uv installation failed"
        exit 1
    fi
}

#==============================================================================
# PHASE 4: PNPM (Efficient Node Package Manager)
#==============================================================================

setup_pnpm() {
    log_info "Installing pnpm..."

    # Install pnpm via corepack (comes with Node.js)
    corepack enable
    corepack prepare pnpm@latest --activate

    # Verify
    if command -v pnpm &> /dev/null; then
        log_success "pnpm installed: $(pnpm --version)"
    else
        log_error "pnpm installation failed"
        exit 1
    fi
}

#==============================================================================
# PHASE 5: CHEZMOI (Dotfiles Manager)
#==============================================================================

setup_chezmoi() {
    log_info "Installing chezmoi..."

    sh -c "$(curl -fsLS get.chezmoi.io)"

    # Verify
    if command -v chezmoi &> /dev/null; then
        log_success "chezmoi installed: $(chezmoi --version)"
    else
        log_error "chezmoi installation failed"
        exit 1
    fi

    # Create initial config directory
    mkdir -p ~/.config/chezmoi
    mkdir -p ~/.local/share/chezmoi

    log_info "Chezmoi directories created. Initialize with: chezmoi init"
}

#==============================================================================
# PHASE 6: CLAUDE CODE CLI
#==============================================================================

setup_claude_code() {
    log_info "Installing Claude Code CLI..."

    # Install via npm (requires Node.js)
    npm install -g @anthropic/claude-code

    # Create .claude directory structure
    mkdir -p ~/.claude/{rules,commands,hooks}

    # Create default settings.json
    cat > ~/.claude/settings.json << 'EOF'
{
  "model": "claude-sonnet-4-20250514",
  "maxTokens": 200000,
  "contextWindow": "auto",
  "permissions": {
    "allowBash": true,
    "allowEdit": true,
    "allowMcp": true
  },
  "mcp": {
    "servers": {}
  }
}
EOF

    # Verify
    if command -v claude &> /dev/null; then
        log_success "Claude Code CLI installed"
    else
        log_warn "Claude Code CLI installed but not in PATH. Restart shell."
    fi

    log_info "Configure API key: export ANTHROPIC_API_KEY=your-key"
}

#==============================================================================
# PHASE 7: OLLAMA (Local LLM)
#==============================================================================

setup_ollama() {
    log_info "Installing Ollama..."

    curl -fsSL https://ollama.com/install.sh | sh

    # Start Ollama service
    if command -v systemctl &> /dev/null; then
        sudo systemctl enable ollama
        sudo systemctl start ollama
        log_success "Ollama service enabled and started"
    else
        log_warn "systemd not available. Start Ollama manually: ollama serve"
    fi

    # Pull recommended models for 11GB VRAM
    log_info "Pulling recommended models for 11GB VRAM..."
    ollama pull qwen2.5-coder:7b
    ollama pull codellama:7b-instruct

    log_success "Ollama installed with coding models"
}

#==============================================================================
# PHASE 8: GIT CONFIGURATION
#==============================================================================

setup_git() {
    log_info "Configuring Git..."

    # Skip if already configured
    if git config --global user.email &> /dev/null; then
        log_info "Git already configured for: $(git config --global user.email)"
        return
    fi

    read -p "Enter your Git email: " git_email
    read -p "Enter your Git name: " git_name

    git config --global user.email "$git_email"
    git config --global user.name "$git_name"
    git config --global init.defaultBranch main
    git config --global pull.rebase true
    git config --global fetch.prune true
    git config --global core.autocrlf input
    git config --global core.editor "code --wait"

    # Enable Git credential helper for WSL
    if grep -qi microsoft /proc/version 2>/dev/null; then
        git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"
    fi

    log_success "Git configured"
}

#==============================================================================
# PHASE 9: KERNEL TUNING
#==============================================================================

setup_kernel_tuning() {
    log_info "Applying kernel tuning for LLM workloads..."

    # Create sysctl config
    sudo tee /etc/sysctl.d/99-jade.conf > /dev/null << 'EOF'
# Jade IDE Development Environment Tuning
# For high-memory LLM workloads

# Reduce swappiness (prefer RAM)
vm.swappiness=10

# Increase dirty page ratios for batch writes
vm.dirty_ratio=60
vm.dirty_background_ratio=2

# Increase inotify watches for large codebases
fs.inotify.max_user_watches=524288
fs.inotify.max_user_instances=512

# Increase file descriptors
fs.file-max=2097152

# Network tuning for API calls
net.core.somaxconn=65535
net.core.netdev_max_backlog=65535
EOF

    # Apply immediately
    sudo sysctl --system

    log_success "Kernel tuning applied"
}

#==============================================================================
# PHASE 10: SHELL CONFIGURATION
#==============================================================================

setup_shell() {
    log_info "Setting up shell configuration..."

    # Install Oh My Zsh if zsh is available
    if command -v zsh &> /dev/null; then
        if [[ ! -d ~/.oh-my-zsh ]]; then
            sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
            log_success "Oh My Zsh installed"
        fi
    fi

    # Add Jade-specific aliases
    cat >> ~/.bashrc << 'EOF'

# ==== Jade IDE Development Aliases ====
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias gs='git status'
alias gd='git diff'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline -20'

# Claude Code
alias cc='claude'
alias ccc='claude --continue'

# Ollama
alias oll='ollama list'
alias ollr='ollama run'

# mise
alias mr='mise run'
alias mx='mise exec'

# Quick navigation
alias cdjde='cd ~/jade-ide'
alias cdjcli='cd ~/jade-cli'
# ==== End Jade Aliases ====
EOF

    log_success "Shell aliases configured"
}

#==============================================================================
# PHASE 11: PRE-COMMIT SETUP
#==============================================================================

setup_precommit() {
    log_info "Installing pre-commit..."

    uv tool install pre-commit

    log_success "pre-commit installed globally"
}

#==============================================================================
# PHASE 12: GITHUB CLI
#==============================================================================

setup_gh() {
    log_info "Installing GitHub CLI..."

    # Add GitHub CLI repo
    (type -p wget >/dev/null || sudo apt install wget -y) \
        && sudo mkdir -p -m 755 /etc/apt/keyrings \
        && wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
        && sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
        && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
        && sudo apt update \
        && sudo apt install gh -y

    log_success "GitHub CLI installed"
    log_info "Authenticate with: gh auth login"
}

#==============================================================================
# MAIN EXECUTION
#==============================================================================

main() {
    echo "=========================================="
    echo "  JADE IDE DEVELOPMENT ENVIRONMENT"
    echo "  Ubuntu 26.04 Bootstrap Script"
    echo "=========================================="
    echo ""

    check_prerequisites

    # Run setup phases
    setup_system_essentials
    setup_mise
    setup_uv
    setup_pnpm
    setup_chezmoi
    setup_claude_code
    setup_ollama
    setup_git
    setup_kernel_tuning
    setup_shell
    setup_precommit
    setup_gh

    echo ""
    echo "=========================================="
    echo "  BOOTSTRAP COMPLETE"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "  1. Restart your shell: exec \$SHELL"
    echo "  2. Set API key: export ANTHROPIC_API_KEY=your-key"
    echo "  3. Auth GitHub: gh auth login"
    echo "  4. Init chezmoi: chezmoi init --apply <your-dotfiles-repo>"
    echo "  5. Verify Claude: claude --version"
    echo ""
    echo "WSL Configuration (run on Windows):"
    echo "  Create %USERPROFILE%\\.wslconfig with memory/processor limits"
    echo ""
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
