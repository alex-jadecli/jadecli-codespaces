# Documentation Master Index

Complete table of contents for jadecli-codespaces documentation with links and quick navigation.

Generated: February 2026 | Total: 200 MD files across 9 categories | ~1.0MB

---

## Quick Links

- **Getting Started:** [Claude Setup](setup-claude/README.md) | [Python Tools](uv/concepts/README.md) | [Code Quality](ruff/README.md)
- **Daily Workflows:** [Type Checking](ty/README.md) | [Linting & Format](ruff/02-ruff-linter.md) | [Package Management](uv/guides/04-working-on-projects.md)
- **Anthropic Resources:** [Claude API Primer](platform-claude/claude-api-primer.md) | [Prompt Library](platform-claude/prompt-library.md)
- **Terminal Setup:** [Claude Code Terminal](wslg/claude-code-terminal-config.md) | [Kitty Config](wslg/kitty-config.md) | [Ghostty Config](wslg/ghostty-config.md)

---

## Documentation by Category

### 1. Setup & Claude (14 files, ~29KB)

**Getting Claude Platform Running**

| File | Purpose | Size |
|------|---------|------|
| [README](setup-claude/README.md) | Overview of Claude setup features | 3.9KB |
| [01-configuring-styles](setup-claude/01-configuring-and-using-styles.md) | Use different interaction styles | 1.1KB |
| [02-chat-search-memory](setup-claude/02-chat-search-and-memory.md) | Chat history and memory features | 1.2KB |
| [03-personalization](setup-claude/03-personalization-features.md) | Customize your Claude experience | 1.5KB |
| [04-project-management](setup-claude/04-create-and-manage-projects.md) | Create and organize projects | 908B |
| [05-visibility-sharing](setup-claude/05-project-visibility-and-sharing.md) | Control project access | 1.1KB |
| [06-google-drive](setup-claude/06-google-drive-integration.md) | Google Drive integration | 936B |
| [07-connect-tools](setup-claude/07-connect-your-tools.md) | Connect external tools | 1.1KB |
| [08-gmail-calendar](setup-claude/08-gmail-google-calendar-integrations.md) | Email and calendar setup | 1.0KB |
| [09-integrations-setup](setup-claude/09-setting-up-integrations.md) | Integration configuration | 1.0KB |
| [10-ios-shortcuts](setup-claude/10-ios-intents-shortcuts-widgets.md) | iOS integration and shortcuts | 1.1KB |

---

### 2. Python Package Manager: UV (42 files, ~71KB)

**Fast Python package management and virtual environment tooling**

#### Concepts (11 files)
Essential UV concepts and architecture:
- [Projects Structure](uv/concepts/01-projects.md) - How uv organizes projects
- [Tools & Isolation](uv/concepts/02-tools.md) - Running isolated tool environments
- [Python Versions](uv/concepts/03-python-versions.md) - Managing multiple Python versions
- [Configuration Files](uv/concepts/04-configuration-files.md) - pyproject.toml, uv.lock
- [Package Indexes](uv/concepts/05-package-indexes.md) - PyPI and custom indexes
- [Dependency Resolution](uv/concepts/06-resolution.md) - How uv resolves dependencies
- [Build Backend](uv/concepts/07-uv-build-backend.md) - Building packages
- [Authentication](uv/concepts/08-authentication.md) - Private package access
- [Caching](uv/concepts/09-caching.md) - Speed optimization
- [Pip Interface](uv/concepts/10-pip-interface.md) - Compatibility layer

#### Guides (7 files)
Step-by-step workflows:
- [Installing Python](uv/guides/01-installing-python.md) - Get Python with uv
- [Running Scripts](uv/guides/02-running-scripts.md) - Script execution
- [Using Tools](uv/guides/03-using-tools.md) - uvx and tool environments
- [Working on Projects](uv/guides/04-working-on-projects.md) - Project development
- [Publishing Packages](uv/guides/05-publishing-packages.md) - Release workflow
- [Migration Guide](uv/guides/06-migration.md) - Migrate from pip/poetry
- [Integrations](uv/guides/07-integrations.md) - GitHub, pre-commit, etc.

#### Reference (5 files)
API and configuration reference:
- [Commands](uv/reference/01-commands.md) - Complete command listing
- [Settings](uv/reference/02-settings.md) - Configuration options
- [Environment Variables](uv/reference/03-environment-variables.md) - Env var reference
- [Storage](uv/reference/04-storage.md) - Cache and storage locations
- [Installer Options](uv/reference/05-installer-options.md) - Installation flags

---

### 3. Python Linter & Formatter: Ruff (7 files, ~17KB)

**Fast Python code quality: linting, formatting, import organization**

| File | Purpose | Dependencies |
|------|---------|---|
| [README](ruff/README.md) | Overview (Ruff = linter + formatter + isort) | - |
| [Installation](ruff/01-installing-ruff.md) | Install ruff (uv add --dev ruff) | uv |
| [Linter](ruff/02-ruff-linter.md) | Finding and fixing code issues | ruff |
| [Formatter](ruff/03-ruff-formatter.md) | Code formatting (ruff format) | ruff |
| [Configuration](ruff/04-configuring-ruff.md) | pyproject.toml setup | ruff |
| [Index](ruff/index.md) | Quick reference | - |
| [Tutorial](ruff/tutorial.md) | Hands-on walkthrough | ruff |

**Quick Commands:**
```bash
ruff check .              # Find issues
ruff check --fix .        # Auto-fix issues
ruff format .             # Format code
```

---

### 4. Python Type Checker: Ty (7 files, ~18KB)

**Static type checking for safer, more reliable Python code**

| File | Purpose | Python | Status |
|------|---------|--------|--------|
| [README](ty/README.md) | Overview (type safety without runtime cost) | 3.8+ | Core |
| [Installation](ty/01-installation.md) | Install ty (uv add --dev ty) | 3.8+ | Core |
| [Type Checking](ty/02-type-checking.md) | How type checking works | 3.8+ | Core |
| [Editor Integration](ty/03-editor-integration.md) | IDE support setup | 3.8+ | Integration |
| [Configuration](ty/04-configuration.md) | pyproject.toml setup | 3.8+ | Core |
| [Rules](ty/05-rules.md) | Type checking rules explained | 3.8+ | Reference |
| [Reference](ty/06-reference.md) | Complete API reference | 3.8+ | Reference |

**Quick Commands:**
```bash
ty check .                    # Check types
ty check --show-diagnostics . # Detailed output
```

**Typical Workflow:** uv (dependency management) → ruff (linting/format) → ty (type safety)

---

### 5. GitHub Issues & Projects (22 files, ~29KB)

**Comprehensive guides for GitHub's issue and project management**

#### Issues (7 guides)
- [01-quickstart](guides/01-quickstart-issues.md) - Get started with issues
- [02-creating-issue](guides/02-creating-issue.md) - Create and describe issues
- [03-sub-issues](guides/03-sub-issues.md) - Break work into smaller units
- [04-dependencies](guides/04-issue-dependencies.md) - Link related issues
- [05-types](guides/05-issue-types.md) - Bug/Feature/Documentation types
- [06-filtering](guides/06-filtering-searching.md) - Find issues quickly
- [07-viewing](guides/07-viewing-issues.md) - Review all issues/PRs

#### Projects (10 guides)
- [08-quickstart](guides/08-quickstart-projects.md) - Projects overview
- [09-planning](guides/09-planning-tracking.md) - Track work with projects
- [10-best-practices](guides/10-best-practices.md) - Proven patterns
- [11-creating](guides/11-creating-project.md) - Create new project
- [12-fields](guides/12-understanding-fields.md) - Custom field setup
- [13-views](guides/13-customizing-views.md) - Table/board/roadmap views
- [14-charts](guides/14-creating-charts.md) - Burndown and status charts
- [15-templates](guides/15-project-templates.md) - Reusable templates
- [16-adding-items](guides/16-adding-items.md) - Add issues to project
- [17-labels](guides/17-managing-labels.md) - Organize with labels
- [18-milestones](guides/18-milestones.md) - Release planning
- [19-automations](guides/19-built-in-automations.md) - Auto-move, auto-archive
- [20-api-projects](guides/20-api-projects.md) - GraphQL project API
- [21-actions](guides/21-actions-automation.md) - Custom workflows

---

### 6. Claude API & Platform (4 files, ~823KB)

**API documentation, cookbooks, prompt examples, and glossary**

| File | Size | Purpose |
|------|------|---------|
| [claude-api-primer.md](platform-claude/claude-api-primer.md) | 18KB | API basics: models, messages, tools, vision, streaming |
| [cookbooks.md](platform-claude/cookbooks.md) | 154KB | 50+ recipes: RAG, agents, vision, batch processing |
| [prompt-library.md](platform-claude/prompt-library.md) | 316KB | 100+ prompts: writing, analysis, coding, etc. |
| [glossary.md](platform-claude/glossary.md) | 354KB | Complete AI/Claude terminology reference |
| [llms.txt](platform-claude/llms.txt) | 56KB | Structured model capability data |

**Key Entry Points:**
- **New to Claude API?** → [claude-api-primer.md](platform-claude/claude-api-primer.md)
- **Want example code?** → [cookbooks.md](platform-claude/cookbooks.md)
- **Need a prompt?** → [prompt-library.md](platform-claude/prompt-library.md)
- **Technical term?** → [glossary.md](platform-claude/glossary.md)

---

### 7. Terminal & Shell Configuration (5 files, ~44KB)

**Terminal emulator setup: Kitty, Ghostty, WezTerm, and Claude Code terminal**

| File | Size | Emulator | Focus |
|------|------|----------|-------|
| [README](wslg/README.md) | 8.2KB | Overview | WSL2 GUI apps |
| [claude-code-terminal-config](wslg/claude-code-terminal-config.md) | 6.6KB | Claude Code | IDE terminal setup |
| [kitty-config](wslg/kitty-config.md) | 10KB | Kitty | GPU rendering, fonts, keybinds |
| [ghostty-config](wslg/ghostty-config.md) | 6.7KB | Ghostty | Modern terminal features |
| [wezterm-config](wslg/wezterm-config.md) | 14KB | WezTerm | Lua config, multiplexing |

---

### 8. Dotfiles & Configuration Management (2 files, ~8KB)

**Chezmoi for managing dotfiles across machines**

| File | Purpose |
|------|---------|
| [README](chezmoi/README.md) | Chezmoi overview: manage dotfiles with Git |
| [examples/](chezmoi/examples/) | Template examples and patterns |

---

### 9. Anthropic Company Documentation (100 files, ~24KB)

**Internal resources: company info, engineering practices, careers**

#### Structure
- **ai-for-science-program-rules/** - AI for science program guidelines
- **candidate-ai-guidance/** - Guidance for AI candidates
- **careers/** - Career information and opportunities
- **claude/** - Claude-specific documentation and announcements
- **company/** - Company information and policies
- **constitution/** - Constitutional AI principles
- **economic-futures/** - Economic research and policy
- **engineering/** - Engineering practices and standards
- **events/** - Conference and event information
- **learn/** - Learning resources
- **legal/** - Legal and compliance documents
- **news/** - Company news and updates

---

## File Organization

```
docs/
├── generated/              # Generated artifacts (this content)
│   ├── master-index.md    # This file
│   ├── cross-references.md
│   ├── quick-reference/   # Cheat sheets
│   │   ├── anthropic-quick-ref.md
│   │   ├── platform-claude-quick-ref.md
│   │   ├── uv-quick-ref.md
│   │   ├── ruff-quick-ref.md
│   │   └── ty-quick-ref.md
│   └── summaries/         # LLM-optimized summaries
│       ├── python-tools-summary.md
│       ├── github-workflow-summary.md
│       ├── claude-api-summary.md
│       ├── terminal-setup-summary.md
│       └── anthropic-resources-summary.md
├── setup-claude/          # Claude platform configuration
├── uv/                    # Package manager and Python tools
├── ruff/                  # Linter and formatter
├── ty/                    # Type checker
├── guides/                # GitHub Issues & Projects
├── platform-claude/       # Claude API docs
├── wslg/                  # Terminal configuration
├── chezmoi/               # Dotfiles management
└── anthropic/             # Company resources
```

---

## Common Workflows

### Setting Up New Python Project
1. [Create project with uv](uv/guides/04-working-on-projects.md)
2. [Configure type checking](ty/04-configuration.md)
3. [Set up linting/formatting](ruff/04-configuring-ruff.md)
4. Run checks: `uv run ruff check . && ty check . && uv run pytest`

### Using Claude API
1. [API Primer](platform-claude/claude-api-primer.md) - Understand basics
2. [Cookbooks](platform-claude/cookbooks.md) - Find relevant pattern
3. [Prompt Library](platform-claude/prompt-library.md) - Adapt prompt for use case
4. Implement and test

### Managing GitHub Project
1. [Create issues](guides/02-creating-issue.md)
2. [Set up project](guides/11-creating-project.md)
3. [Configure automations](guides/19-built-in-automations.md)
4. [Track progress](guides/09-planning-tracking.md)

### Terminal Setup
1. [Choose emulator](wslg/README.md)
2. [Install config file](wslg/kitty-config.md) (or ghostty/wezterm)
3. [Optional: Claude Code terminal](wslg/claude-code-terminal-config.md)

---

## Statistics

| Category | Files | Size | Type |
|----------|-------|------|------|
| Anthropic Resources | 100 | 24KB | Company docs |
| GitHub Guides | 22 | 29KB | How-to guides |
| UV (Package Manager) | 42 | 71KB | Tool docs |
| Platform Claude | 4 | 823KB | API docs + examples |
| WSL/Terminal | 5 | 44KB | Config guides |
| Ruff (Linter) | 7 | 17KB | Tool docs |
| Ty (Type Checker) | 7 | 18KB | Tool docs |
| Setup Claude | 11 | 14KB | Platform guides |
| Chezmoi | 2 | 8KB | Dotfiles guide |
| **TOTAL** | **200** | **~1.0MB** | Mixed |

---

## Generated: February 2026

This index is auto-generated from the documentation structure. Last updated: 2026-02-04
