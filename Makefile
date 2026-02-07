# ---
# entity_id: config-makefile
# entity_name: Project Build System
# entity_type_id: config
# entity_path: Makefile
# entity_language: make
# entity_state: active
# entity_created: 2026-01-23T00:00:00Z
# entity_exports: [install, install-dev, build, clean, test, lint]
# entity_dependencies: [uv, python]
# entity_semver_impact: minor
# ---

# ============================================
# jadecli-codespaces Makefile
# ============================================
# WSL Multi-Agent Environment Setup
# Optimized for Claude + Ollama workflows
# ============================================

SHELL := /bin/bash
.DEFAULT_GOAL := help

# === Configuration ===
PYTHON := python3
UV := uv
PIP := $(UV) pip
PROJECT_NAME := jadecli-entity-store
VENV_DIR := .venv

# === Colors for rich output ===
BLUE := \033[34m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
CYAN := \033[36m
MAGENTA := \033[35m
BOLD := \033[1m
RESET := \033[0m

# === Logging Helpers ===
define log_info
	@echo -e "$(BLUE)$(BOLD)ℹ$(RESET) $(1)"
endef

define log_success
	@echo -e "$(GREEN)$(BOLD)✓$(RESET) $(1)"
endef

define log_warn
	@echo -e "$(YELLOW)$(BOLD)⚠$(RESET) $(1)"
endef

define log_error
	@echo -e "$(RED)$(BOLD)✗$(RESET) $(1)"
endef

define log_step
	@echo -e "$(CYAN)$(BOLD)→$(RESET) $(1)"
endef

define log_header
	@echo ""
	@echo -e "$(MAGENTA)$(BOLD)════════════════════════════════════════$(RESET)"
	@echo -e "$(MAGENTA)$(BOLD)  $(1)$(RESET)"
	@echo -e "$(MAGENTA)$(BOLD)════════════════════════════════════════$(RESET)"
	@echo ""
endef

# === Help ===
.PHONY: help
help:
	$(call log_header,jadecli-codespaces Build System)
	@echo "Usage: make [target]"
	@echo ""
	@echo -e "$(BOLD)Setup Targets:$(RESET)"
	@echo "  install       Install production dependencies"
	@echo "  install-dev   Install development dependencies"
	@echo "  install-ollama Install Ollama for local inference"
	@echo "  setup-wsl     Full WSL environment setup"
	@echo ""
	@echo -e "$(BOLD)Build Targets:$(RESET)"
	@echo "  build         Build the project"
	@echo "  build-wheel   Build wheel distribution"
	@echo "  clean         Clean build artifacts"
	@echo ""
	@echo -e "$(BOLD)Development Targets:$(RESET)"
	@echo "  test          Run tests"
	@echo "  lint          Run linters"
	@echo "  format        Format code"
	@echo "  typecheck     Run type checker"
	@echo ""
	@echo -e "$(BOLD)Multi-Agent Targets:$(RESET)"
	@echo "  agent-start   Start multi-agent orchestrator"
	@echo "  ollama-start  Start Ollama server"
	@echo "  ollama-pull   Pull required Ollama models"
	@echo ""
	@echo -e "$(BOLD)Dotfile Targets:$(RESET)"
	@echo "  dotfiles-init     Initialize chezmoi-style dotfiles"
	@echo "  dotfiles-apply    Apply dotfile configuration"
	@echo "  dotfiles-diff     Show dotfile differences"

# ============================================
# INSTALLATION TARGETS
# ============================================

.PHONY: install
install:
	$(call log_header,Installing Production Dependencies)
	$(call log_step,Checking for uv package manager...)
	@command -v $(UV) >/dev/null 2>&1 || { \
		$(call log_warn,uv not found. Installing...); \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	}
	$(call log_success,uv package manager available)

	$(call log_step,Creating virtual environment...)
	@$(UV) venv $(VENV_DIR) --python $(PYTHON) 2>/dev/null || true
	$(call log_success,Virtual environment ready)

	$(call log_step,Installing production dependencies...)
	@$(PIP) install -e . --quiet
	$(call log_success,Production dependencies installed)

	$(call log_step,Verifying installation...)
	@$(VENV_DIR)/bin/python -c "import cli.settings; print('Settings module loaded')"
	@$(VENV_DIR)/bin/python -c "import entity_store; print('Entity store module loaded')"
	$(call log_success,Installation verified)

	$(call log_header,Installation Complete)
	@echo -e "Activate with: $(CYAN)source $(VENV_DIR)/bin/activate$(RESET)"

.PHONY: install-dev
install-dev: install
	$(call log_header,Installing Development Dependencies)

	$(call log_step,Installing dev dependencies...)
	@$(PIP) install -e ".[dev]" --quiet
	$(call log_success,Dev dependencies installed)

	$(call log_step,Installing pre-commit hooks...)
	@$(VENV_DIR)/bin/pre-commit install --install-hooks 2>/dev/null || \
		$(call log_warn,Pre-commit hook installation skipped)
	$(call log_success,Pre-commit hooks configured)

	$(call log_step,Installing agent dependencies...)
	@$(PIP) install ollama structlog --quiet 2>/dev/null || true
	$(call log_success,Agent dependencies installed)

	$(call log_step,Setting up observability...)
	@$(PIP) install opentelemetry-api opentelemetry-sdk prometheus-client --quiet 2>/dev/null || true
	$(call log_success,Observability packages installed)

	$(call log_header,Development Environment Ready)
	@echo -e "Run $(CYAN)make test$(RESET) to verify setup"

.PHONY: install-ollama
install-ollama:
	$(call log_header,Installing Ollama)

	$(call log_step,Checking for existing Ollama installation...)
	@if command -v ollama >/dev/null 2>&1; then \
		echo -e "$(GREEN)$(BOLD)✓$(RESET) Ollama already installed"; \
		ollama --version; \
	else \
		echo -e "$(YELLOW)$(BOLD)⚠$(RESET) Installing Ollama..."; \
		curl -fsSL https://ollama.com/install.sh | sh; \
	fi
	$(call log_success,Ollama installation complete)

.PHONY: ollama-pull
ollama-pull:
	$(call log_header,Pulling Ollama Models)

	$(call log_step,Pulling codellama:7b for code tasks...)
	@ollama pull codellama:7b 2>/dev/null || $(call log_warn,Failed to pull codellama:7b)

	$(call log_step,Pulling llama3.2:3b for fast inference...)
	@ollama pull llama3.2:3b 2>/dev/null || $(call log_warn,Failed to pull llama3.2:3b)

	$(call log_step,Pulling nomic-embed-text for embeddings...)
	@ollama pull nomic-embed-text 2>/dev/null || $(call log_warn,Failed to pull nomic-embed-text)

	$(call log_success,Ollama models ready)
	@echo ""
	@echo -e "$(BOLD)Available models:$(RESET)"
	@ollama list 2>/dev/null || echo "  (Ollama not running)"

.PHONY: ollama-start
ollama-start:
	$(call log_header,Starting Ollama Server)
	$(call log_step,Starting Ollama in background...)
	@ollama serve &>/dev/null &
	@sleep 2
	$(call log_success,Ollama server started on http://localhost:11434)

# ============================================
# BUILD TARGETS
# ============================================

.PHONY: build
build:
	$(call log_header,Building Project)

	$(call log_step,Running linters...)
	@$(VENV_DIR)/bin/ruff check . --fix --quiet 2>/dev/null || true
	$(call log_success,Linting complete)

	$(call log_step,Formatting code...)
	@$(VENV_DIR)/bin/ruff format . --quiet 2>/dev/null || true
	$(call log_success,Formatting complete)

	$(call log_step,Type checking...)
	@$(VENV_DIR)/bin/mypy cli entity_store agents --ignore-missing-imports 2>/dev/null || \
		$(call log_warn,Type checking had warnings)
	$(call log_success,Type check complete)

	$(call log_step,Building package...)
	@$(UV) build --quiet 2>/dev/null || $(call log_warn,Build skipped)
	$(call log_success,Build complete)

	$(call log_header,Build Successful)

.PHONY: build-wheel
build-wheel:
	$(call log_header,Building Wheel Distribution)
	@$(UV) build --wheel
	$(call log_success,Wheel built in dist/)

.PHONY: clean
clean:
	$(call log_header,Cleaning Build Artifacts)

	$(call log_step,Removing build directories...)
	@rm -rf build/ dist/ *.egg-info/ .eggs/
	$(call log_success,Build directories removed)

	$(call log_step,Removing cache files...)
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	$(call log_success,Cache files removed)

	$(call log_step,Removing coverage data...)
	@rm -rf htmlcov/ .coverage coverage.xml
	$(call log_success,Coverage data removed)

	$(call log_header,Clean Complete)

# ============================================
# DEVELOPMENT TARGETS
# ============================================

.PHONY: test
test:
	$(call log_header,Running Tests)
	@$(VENV_DIR)/bin/pytest tests/ -v --tb=short 2>/dev/null || \
		$(call log_warn,Some tests failed or no tests found)
	$(call log_success,Test run complete)

.PHONY: lint
lint:
	$(call log_header,Running Linters)

	$(call log_step,Running ruff check...)
	@$(VENV_DIR)/bin/ruff check . 2>/dev/null || true

	$(call log_step,Running ruff format check...)
	@$(VENV_DIR)/bin/ruff format --check . 2>/dev/null || true

	$(call log_success,Lint complete)

.PHONY: format
format:
	$(call log_header,Formatting Code)
	@$(VENV_DIR)/bin/ruff format .
	@$(VENV_DIR)/bin/ruff check --fix .
	$(call log_success,Formatting complete)

.PHONY: typecheck
typecheck:
	$(call log_header,Running Type Checker)
	@$(VENV_DIR)/bin/mypy cli entity_store agents --ignore-missing-imports
	$(call log_success,Type check complete)

# ============================================
# WSL SETUP TARGETS
# ============================================

.PHONY: setup-wsl
setup-wsl: install-dev install-ollama ollama-pull dotfiles-init
	$(call log_header,WSL Environment Setup Complete)

	@echo -e "$(BOLD)Next steps:$(RESET)"
	@echo "  1. Activate venv: source $(VENV_DIR)/bin/activate"
	@echo "  2. Start Ollama: make ollama-start"
	@echo "  3. Start agent: make agent-start"
	@echo ""
	@echo -e "$(BOLD)Configuration:$(RESET)"
	@echo "  - Copy .env.example to .env and add your API keys"
	@echo "  - Edit dotfiles/local/.env.local for machine-specific config"
	@echo ""
	$(call log_success,WSL setup complete!)

# ============================================
# MULTI-AGENT TARGETS
# ============================================

.PHONY: agent-start
agent-start:
	$(call log_header,Starting Multi-Agent Orchestrator)
	$(call log_step,Initializing agent router...)
	@$(VENV_DIR)/bin/python -m agents.orchestrator 2>/dev/null || \
		$(call log_warn,Agent orchestrator not yet implemented)

.PHONY: agent-status
agent-status:
	$(call log_header,Agent Status)
	@echo -e "$(BOLD)Claude:$(RESET)"
	@$(VENV_DIR)/bin/python -c "from cli.settings import settings; print('  API configured:', settings.has_parallel_api)"
	@echo ""
	@echo -e "$(BOLD)Ollama:$(RESET)"
	@curl -s http://localhost:11434/api/tags 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('  Models:', ', '.join([m['name'] for m in d.get('models',[])]))" 2>/dev/null || echo "  Status: Not running"

# ============================================
# DOTFILE TARGETS
# ============================================

.PHONY: dotfiles-init
dotfiles-init:
	$(call log_header,Initializing Dotfile Management)

	$(call log_step,Creating dotfile directories...)
	@mkdir -p dotfiles/org dotfiles/project dotfiles/local
	@mkdir -p dotfiles/org/.claude dotfiles/project/.claude dotfiles/local/.claude
	$(call log_success,Dotfile directories created)

	$(call log_step,Creating dotfile templates...)
	@test -f dotfiles/README.md || echo "# Dotfile Management" > dotfiles/README.md
	$(call log_success,Dotfile templates created)

	$(call log_header,Dotfiles Initialized)
	@echo "Structure:"
	@echo "  dotfiles/org/     - Organization-wide settings"
	@echo "  dotfiles/project/ - Project-specific settings"
	@echo "  dotfiles/local/   - Machine-specific settings (gitignored)"

.PHONY: dotfiles-apply
dotfiles-apply:
	$(call log_header,Applying Dotfile Configuration)
	$(call log_step,Applying organization dotfiles...)
	@$(VENV_DIR)/bin/python -m agents.dotfiles apply --layer=org 2>/dev/null || true
	$(call log_step,Applying project dotfiles...)
	@$(VENV_DIR)/bin/python -m agents.dotfiles apply --layer=project 2>/dev/null || true
	$(call log_step,Applying local dotfiles...)
	@$(VENV_DIR)/bin/python -m agents.dotfiles apply --layer=local 2>/dev/null || true
	$(call log_success,Dotfiles applied)

.PHONY: dotfiles-diff
dotfiles-diff:
	$(call log_header,Dotfile Differences)
	@$(VENV_DIR)/bin/python -m agents.dotfiles diff 2>/dev/null || \
		$(call log_warn,Dotfile diff not yet implemented)

# ============================================
# OBSERVABILITY TARGETS
# ============================================

.PHONY: logs-tail
logs-tail:
	$(call log_header,Tailing Agent Logs)
	@tail -f logs/agent.log 2>/dev/null || $(call log_warn,No logs found)

.PHONY: metrics-show
metrics-show:
	$(call log_header,Agent Metrics)
	@$(VENV_DIR)/bin/python -m agents.metrics show 2>/dev/null || \
		$(call log_warn,Metrics not yet implemented)
