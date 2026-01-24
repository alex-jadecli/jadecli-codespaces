#!/usr/bin/env bash
# ---
# entity_id: script-jade-research-init
# entity_name: Jade IDE Research Orchestration Script
# entity_type_id: script
# entity_path: research/jade-ide/init.sh
# entity_language: bash
# entity_state: active
# entity_created: 2026-01-23T00:00:00Z
# entity_exports: [init_research, launch_agents]
# entity_dependencies: [parallel-api, chezmoi, claude-code]
# entity_actors: [dev, claude]
# ---

#==============================================================================
# JADE IDE RESEARCH ORCHESTRATION
#==============================================================================
# Optimized multi-agent research launcher for:
# - VS Code fork architecture (Cursor, Kiro, Gemini patterns)
# - Ubuntu 26.04 Claude Code + Ollama optimization
# - Enterprise dotfiles management (chezmoi, multi-tier .claude)
# - Team-oriented Git culture and practices
# - Agent protocols (ACP, MCP, A2A)
#==============================================================================

set -euo pipefail

# Configuration
RESEARCH_ROOT="${RESEARCH_ROOT:-$(dirname "$0")}"
PROGRESS_LOG="${RESEARCH_ROOT}/2604-research-append-progress.txt"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# System context (from user specification)
export JADE_HOST_OS="Windows 10"
export JADE_WSL_DISTRO="Ubuntu 26.04"
export JADE_RAM_GB="128"
export JADE_VRAM_GB="11"
export JADE_CPU_THREADS="24"

#==============================================================================
# LOGGING FUNCTIONS
#==============================================================================

log_progress() {
    local domain="$1"
    local message="$2"
    echo "[${TIMESTAMP}] [${domain}] ${message}" >> "${PROGRESS_LOG}"
}

log_finding() {
    local domain="$1"
    local category="$2"
    local finding="$3"
    cat >> "${PROGRESS_LOG}" << EOF

--- FINDING: ${domain} / ${category} ---
${finding}
--- END FINDING ---

EOF
}

#==============================================================================
# RESEARCH DOMAINS
#==============================================================================

# Domain 1: VS Code Fork Architecture
research_vscode_fork() {
    log_progress "VSCODE-FORK" "Starting VS Code fork architecture research"

    cat >> "${PROGRESS_LOG}" << 'EOF'

================================================================================
DOMAIN 1: VS CODE FORK ARCHITECTURE
================================================================================

## Key Competitors Analysis

### Cursor IDE
- Fork of VS Code with native AI integration
- Custom extension host for AI context
- Proprietary AI backend (Claude, GPT-4)
- Tab completion + chat + composer modes

### Kiro (AWS)
- Amazon's VS Code fork
- Deep AWS integration
- Spec-driven development approach
- Agent-based architecture

### Gemini Code Assist (Google)
- VS Code extension (not fork)
- Integration via Agent Client Protocol
- Gemini model backend
- Focus on enterprise compliance

### Zed + ACP
- Not VS Code fork (Rust-native)
- Open Agent Client Protocol pioneer
- Collaborating with JetBrains on ACP
- Claude integration via SDK adapter

## Architecture Patterns to Study

1. Extension Host Modifications
   - How Cursor intercepts completions
   - Custom LSP extensions
   - Context window management

2. AI Context Pipeline
   - File indexing strategies
   - Semantic search integration
   - RAG patterns for codebase

3. Multi-Model Support
   - Model routing architecture
   - Fallback strategies
   - Cost optimization

4. Telemetry & Privacy
   - Enterprise data residency
   - Opt-out mechanisms
   - Audit logging

================================================================================
EOF

    log_progress "VSCODE-FORK" "Completed initial architecture mapping"
}

# Domain 2: Ubuntu 26.04 Optimization
research_ubuntu_optimization() {
    log_progress "UBUNTU-26.04" "Starting Ubuntu optimization research"

    cat >> "${PROGRESS_LOG}" << 'EOF'

================================================================================
DOMAIN 2: UBUNTU 26.04 OPTIMIZATION FOR CLAUDE CODE + OLLAMA
================================================================================

## System Specifications
- Host: Windows 10 + WSL2
- Distro: Ubuntu 26.04 LTS
- RAM: 128 GB
- VRAM: 11 GB (likely RTX 3080/4080 or similar)
- CPU: 24 threads (likely 12-core with HT)

## WSL2 Configuration

### .wslconfig (Windows side: %USERPROFILE%\.wslconfig)
```ini
[wsl2]
memory=96GB           # Reserve 32GB for Windows
processors=20         # Leave 4 threads for Windows
swap=32GB             # Enable swap for model loading
localhostForwarding=true

[experimental]
autoMemoryReclaim=gradual
sparseVhd=true
```

### /etc/wsl.conf (Ubuntu side)
```ini
[boot]
systemd=true

[interop]
enabled=true
appendWindowsPath=false

[network]
generateResolvConf=false
```

## Package Manager Strategy

### Modern Stack (2026)
1. **mise** (formerly rtx) - Polyglot version manager
   - Replaces: nvm, pyenv, rbenv, etc.
   - Config: ~/.config/mise/config.toml
   - Per-project: .mise.toml

2. **uv** - Fast Python package manager (Astral)
   - Replaces: pip, pip-tools, poetry, pyenv
   - 10-100x faster than pip
   - Lock files: uv.lock

3. **pnpm** - Efficient Node package manager
   - Content-addressable storage
   - Strict dependency isolation

4. **cargo** - Rust ecosystem

## Claude Code Optimization

### Environment Variables
```bash
# ~/.bashrc or ~/.zshrc
export ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY}"
export CLAUDE_CODE_TELEMETRY=0
export CLAUDE_CODE_MAX_TOKENS=200000
export CLAUDE_CODE_MODEL="claude-sonnet-4-20250514"

# Memory optimization
export NODE_OPTIONS="--max-old-space-size=8192"
```

### Claude Code Settings (~/.claude/settings.json)
```json
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
    "servers": []
  }
}
```

## Ollama Local Setup

### Installation
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### GPU Configuration (11GB VRAM)
```bash
# Models that fit in 11GB VRAM
ollama pull codellama:13b-instruct-q4_K_M  # ~7.4GB
ollama pull deepseek-coder:6.7b-instruct   # ~3.8GB
ollama pull qwen2.5-coder:7b               # ~4.4GB

# For larger models, use CPU offloading
OLLAMA_NUM_GPU=35  # Layers on GPU
```

### Ollama + Claude Code Integration
```bash
# MCP server for Ollama
npm install -g @anthropic/mcp-server-ollama

# Add to ~/.claude/settings.json
{
  "mcp": {
    "servers": {
      "ollama": {
        "command": "mcp-server-ollama",
        "args": ["--model", "codellama:13b-instruct"]
      }
    }
  }
}
```

## Performance Tuning

### Kernel Parameters (/etc/sysctl.d/99-jade.conf)
```
vm.swappiness=10
vm.dirty_ratio=60
vm.dirty_background_ratio=2
fs.inotify.max_user_watches=524288
fs.file-max=2097152
```

### systemd Services
```bash
# Enable Ollama service
sudo systemctl enable ollama
sudo systemctl start ollama

# GPU memory management
nvidia-smi -pm 1  # Persistence mode
```

================================================================================
EOF

    log_progress "UBUNTU-26.04" "Completed optimization guidelines"
}

# Domain 3: Dotfiles Management
research_dotfiles() {
    log_progress "DOTFILES" "Starting dotfiles management research"

    cat >> "${PROGRESS_LOG}" << 'EOF'

================================================================================
DOMAIN 3: DOTFILES MANAGEMENT - MULTI-TIER .CLAUDE CONFIGURATION
================================================================================

## The 4-Tier .claude Configuration Problem

### Tier 1: Personal (~/.claude)
- Engineer's personal preferences
- API keys, personal settings
- Not committed to any repo

### Tier 2: Project (~/<org>/<project>/.claude)
- Project-specific rules and context
- CLAUDE.md with codebase conventions
- Committed to project repo

### Tier 3: Enterprise/Organization
- IT-managed compliance settings
- Model restrictions, audit logging
- Deployed via MDM or config management

### Tier 4: Shared Dotfiles (GitHub Organization)
- Reusable .claude templates
- Organization-wide CLAUDE.md snippets
- Managed as separate repo/package

## Chezmoi for Dotfiles

### Why Chezmoi?
- Template support (Go templates)
- Secret management (1Password, Bitwarden, age)
- Multi-machine support
- Git-based versioning
- Script execution hooks

### Chezmoi Structure for Claude
```
~/.local/share/chezmoi/
├── .chezmoi.toml.tmpl          # Machine-specific config
├── dot_claude/
│   ├── settings.json.tmpl      # Personal settings (templated)
│   ├── private_api_keys        # Encrypted secrets
│   └── rules/
│       └── personal.md
├── .chezmoiignore              # Machine-specific ignores
└── .chezmoiscripts/
    └── run_once_setup-claude.sh
```

### Chezmoi Template Example
```gotemplate
{{/* dot_claude/settings.json.tmpl */}}
{
  "model": {{ .claude_model | quote }},
  "maxTokens": {{ .claude_max_tokens }},
  {{- if .work_machine }}
  "permissions": {
    "allowBash": false,
    "requireApproval": true
  }
  {{- else }}
  "permissions": {
    "allowBash": true
  }
  {{- end }}
}
```

### Multi-Tier Resolution Strategy

```bash
# Resolution order (later overrides earlier):
1. /etc/claude/settings.json          # Enterprise (IT-managed)
2. ~/.config/claude/settings.json     # XDG config (chezmoi managed)
3. ~/.claude/settings.json            # Legacy personal location
4. ./<project>/.claude/settings.json  # Project-specific
5. Environment variables              # Runtime overrides
```

## Organization-Level Shared Dotfiles

### GitHub Organization Repository Pattern
```
github.com/<org>/dotfiles-claude/
├── README.md
├── templates/
│   ├── settings.json.tmpl
│   ├── CLAUDE.md.tmpl
│   └── rules/
│       ├── security.md
│       ├── testing.md
│       └── code-style.md
├── scripts/
│   └── sync-to-project.sh
└── .chezmoi/
    └── external.toml     # Pull into personal dotfiles
```

### Chezmoi External for Org Templates
```toml
# ~/.config/chezmoi/chezmoi.toml
[data.org]
  name = "jade-ide"

# dot_claude/rules/.chezmoiexternal.toml
["security.md"]
    type = "file"
    url = "https://raw.githubusercontent.com/jade-ide/dotfiles-claude/main/templates/rules/security.md"
    refreshPeriod = "168h"  # Weekly refresh
```

## Modern Alternatives to Consider

### 1. Nix Home Manager
- Declarative, reproducible
- Complex learning curve
- Best for full-stack reproducibility

### 2. Ansible for Dotfiles
- Enterprise-friendly
- Idempotent operations
- Good for IT-managed configs

### 3. YADM (Yet Another Dotfiles Manager)
- Git wrapper approach
- Simpler than chezmoi
- Less powerful templating

### 4. mise + dotenvx
- Modern polyglot approach
- .env file management
- Simpler than chezmoi

## Recommended Stack for Jade IDE

```
┌─────────────────────────────────────────────────────────┐
│                    CONFIGURATION LAYERS                  │
├─────────────────────────────────────────────────────────┤
│ Layer 4: Enterprise    │ Ansible/Salt/Puppet            │
│         (IT/Ops)       │ /etc/claude/                   │
├─────────────────────────────────────────────────────────┤
│ Layer 3: Organization  │ GitHub Org repo                │
│         (Templates)    │ dotfiles-claude/               │
├─────────────────────────────────────────────────────────┤
│ Layer 2: Personal      │ Chezmoi                        │
│         (Engineer)     │ ~/.claude/                     │
├─────────────────────────────────────────────────────────┤
│ Layer 1: Project       │ Git (in-repo)                  │
│         (Team)         │ .claude/                       │
└─────────────────────────────────────────────────────────┘
```

================================================================================
EOF

    log_progress "DOTFILES" "Completed multi-tier configuration mapping"
}

# Domain 4: Git Culture
research_git_culture() {
    log_progress "GIT-CULTURE" "Starting Git culture research"

    cat >> "${PROGRESS_LOG}" << 'EOF'

================================================================================
DOMAIN 4: TEAM-ORIENTED GIT CULTURE & PROJECT MANAGEMENT
================================================================================

## Anti-Patterns to Avoid (Learned from Industry)

### 1. The Monolithic .env Problem
- Anti-pattern: Single .env with all secrets
- Solution: Tiered config with clear ownership

### 2. "Works on My Machine"
- Anti-pattern: Undocumented local dependencies
- Solution: mise/.tool-versions + devcontainer.json

### 3. Commit Message Chaos
- Anti-pattern: "fix stuff", "wip", "asdf"
- Solution: Conventional Commits + commitlint

### 4. Review Bottlenecks
- Anti-pattern: PRs waiting days for review
- Solution: CODEOWNERS + async review culture

### 5. Main Branch Instability
- Anti-pattern: Breaking changes on main
- Solution: Required CI + branch protection

## Modern Git Practices for AI-Assisted Teams

### 1. Conventional Commits
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore

### 2. Branch Strategy for AI Collaboration

```
main
├── develop
│   ├── feature/jade-123-new-feature
│   ├── claude/session-abc123          # AI-generated branches
│   └── fix/jade-456-bug-fix
└── release/v1.0.0
```

### 3. AI-Aware CODEOWNERS
```
# CODEOWNERS
* @jade-ide/core-team

# AI-assisted files need human review
.claude/ @jade-ide/ai-governance
CLAUDE.md @jade-ide/ai-governance

# Auto-generated code needs extra scrutiny
*.generated.ts @jade-ide/code-quality
```

### 4. GitHub Actions for AI Projects
```yaml
# .github/workflows/ai-review.yml
name: AI Code Review
on: [pull_request]

jobs:
  ai-safety-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check AI-generated code markers
        run: |
          # Ensure AI-generated code is marked
          git diff --name-only origin/main | xargs grep -L "AI-GENERATED" || true

      - name: Validate CLAUDE.md
        run: |
          # Ensure CLAUDE.md is valid
          npx claude-md-lint CLAUDE.md
```

### 5. Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.29.0
    hooks:
      - id: commitizen
        stages: [commit-msg]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json

  - repo: local
    hooks:
      - id: validate-claude-md
        name: Validate CLAUDE.md
        entry: ./scripts/validate-claude-md.sh
        language: script
        files: CLAUDE\.md$
```

## GitHub Organization Setup for Jade IDE

### Repository Structure
```
github.com/jade-ide/
├── jade-ide                  # Main IDE fork
├── jade-cli                  # CLI extension
├── dotfiles-claude           # Shared .claude configs
├── .github                   # Org-wide workflows
├── terraform-infrastructure  # IaC
└── docs                      # Documentation site
```

### Org-Wide Settings (.github repo)
```
.github/
├── ISSUE_TEMPLATE/
│   ├── bug_report.yml
│   ├── feature_request.yml
│   └── config.yml
├── PULL_REQUEST_TEMPLATE.md
├── CODEOWNERS
├── SECURITY.md
├── FUNDING.yml
└── workflows/
    └── org-ci.yml
```

### Branch Protection Rules
- Require PR reviews (2 approvers)
- Require status checks
- Require conversation resolution
- Require signed commits (optional)
- Include administrators in restrictions

================================================================================
EOF

    log_progress "GIT-CULTURE" "Completed Git culture documentation"
}

# Domain 5: Agent Protocols
research_agent_protocols() {
    log_progress "AGENT-PROTOCOLS" "Starting agent protocol research"

    cat >> "${PROGRESS_LOG}" << 'EOF'

================================================================================
DOMAIN 5: AGENT PROTOCOLS (ACP, MCP, A2A)
================================================================================

## Protocol Landscape (2026)

### 1. Agent Client Protocol (ACP) - Zed
- **Purpose**: IDE <-> Agent communication
- **License**: Apache 2.0
- **Key Adopters**: Zed, JetBrains, Gemini CLI
- **Claude Integration**: Via Zed SDK adapter

```
┌─────────────┐     ACP      ┌─────────────┐
│    IDE      │◄────────────►│   Agent     │
│ (Zed, JB)   │              │ (Claude)    │
└─────────────┘              └─────────────┘
```

### 2. Model Context Protocol (MCP) - Anthropic
- **Purpose**: LLM <-> Tools/Data communication
- **Specification**: JSON-RPC 2.0 over stdio/HTTP
- **Key Feature**: Bidirectional, tool exposure

```
┌─────────────┐     MCP      ┌─────────────┐
│   Claude    │◄────────────►│ MCP Server  │
│             │              │ (Tools)     │
└─────────────┘              └─────────────┘
```

### 3. Agent-to-Agent (A2A) - Google/Linux Foundation
- **Purpose**: Multi-agent orchestration
- **Status**: Merged with ACP under LF
- **Key Feature**: Agent discovery, delegation

### Protocol Comparison

| Feature              | ACP       | MCP       | A2A       |
|----------------------|-----------|-----------|-----------|
| Primary Use          | IDE ↔ AI  | AI ↔ Tools| AI ↔ AI   |
| Transport            | HTTP/WS   | stdio/HTTP| HTTP/WS   |
| Specification        | REST      | JSON-RPC  | REST      |
| Discovery            | Yes       | Limited   | Yes       |
| Anthropic Support    | Via SDK   | Native    | Indirect  |

## Jade IDE Protocol Strategy

### Recommended Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      JADE IDE                            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Editor    │  │  Debugger   │  │  Terminal   │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │             │
│         ▼                ▼                ▼             │
│  ┌──────────────────────────────────────────────┐      │
│  │            JADE PROTOCOL BRIDGE               │      │
│  │  ┌────────┐  ┌────────┐  ┌────────┐          │      │
│  │  │  ACP   │  │  MCP   │  │  A2A   │          │      │
│  │  │Adapter │  │Adapter │  │Adapter │          │      │
│  │  └────┬───┘  └────┬───┘  └────┬───┘          │      │
│  └───────┼───────────┼───────────┼──────────────┘      │
│          │           │           │                      │
└──────────┼───────────┼───────────┼──────────────────────┘
           │           │           │
           ▼           ▼           ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │  Claude  │ │  Ollama  │ │  Other   │
    │  (API)   │ │ (Local)  │ │  Agents  │
    └──────────┘ └──────────┘ └──────────┘
```

### MCP Server Implementation for Jade

```typescript
// jade-cli/src/mcp/server.ts
import { McpServer } from "@anthropic/mcp-server";

const server = new McpServer({
  name: "jade-cli",
  version: "1.0.0",
});

// Expose Jade-specific tools
server.tool("jade/edit-file", {
  description: "Edit a file with AI assistance",
  inputSchema: {
    type: "object",
    properties: {
      path: { type: "string" },
      instruction: { type: "string" }
    }
  },
  handler: async (input) => {
    // Implementation
  }
});

server.tool("jade/run-test", {
  description: "Run tests for current project",
  inputSchema: {
    type: "object",
    properties: {
      pattern: { type: "string" }
    }
  },
  handler: async (input) => {
    // Implementation
  }
});
```

### ACP Integration for External Agents

```typescript
// jade-ide/src/acp/client.ts
import { AcpClient } from "@zed/acp-sdk";

const client = new AcpClient({
  endpoint: "http://localhost:8080/acp",
});

// Connect to external agents
await client.connect("gemini-cli");
await client.connect("claude-code");

// Delegate task
const result = await client.delegate({
  agent: "claude-code",
  task: "refactor-function",
  context: { file: "src/main.ts", function: "processData" }
});
```

================================================================================
EOF

    log_progress "AGENT-PROTOCOLS" "Completed protocol architecture documentation"
}

#==============================================================================
# MAIN ORCHESTRATION
#==============================================================================

main() {
    echo "=========================================="
    echo "JADE IDE RESEARCH ORCHESTRATION"
    echo "=========================================="
    echo "Starting parallel research agents..."
    echo ""

    log_progress "MAIN" "Research orchestration started"

    # Run research functions (can be parallelized with & and wait)
    research_vscode_fork
    research_ubuntu_optimization
    research_dotfiles
    research_git_culture
    research_agent_protocols

    # Final summary
    cat >> "${PROGRESS_LOG}" << EOF

================================================================================
RESEARCH SESSION COMPLETE
================================================================================
Timestamp: ${TIMESTAMP}
Domains Researched: 5
  1. VS Code Fork Architecture
  2. Ubuntu 26.04 Optimization
  3. Dotfiles Management (Chezmoi + Multi-Tier .claude)
  4. Git Culture & Team Practices
  5. Agent Protocols (ACP, MCP, A2A)

Next Steps:
- [ ] Create detailed implementation plan
- [ ] Set up jade-ide GitHub organization
- [ ] Initialize dotfiles-claude repository
- [ ] Configure Ubuntu 26.04 base environment
- [ ] Implement MCP server for jade-cli

================================================================================
EOF

    log_progress "MAIN" "Research orchestration complete"

    echo ""
    echo "Research complete! Results saved to:"
    echo "  ${PROGRESS_LOG}"
    echo ""
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
