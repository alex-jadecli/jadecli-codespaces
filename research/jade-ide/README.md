# ---
# entity_id: document-jade-research-readme
# entity_name: Jade IDE Research Documentation
# entity_type_id: document
# entity_path: research/jade-ide/README.md
# entity_language: markdown
# entity_state: active
# entity_created: 2026-01-23T00:00:00Z
# entity_actors: [dev, claude]
# locked_by: null
# locked_at: null
# status: available
# ---

# Jade IDE Research

> Multi-agent research framework for building a VS Code fork with integrated Claude Code CLI.

## Overview

This research initiative explores building **Jade IDE**, a VS Code fork similar to Cursor, Kiro (AWS), and Google's Gemini integrations, with a companion CLI extension that works standalone or embedded.

## System Context

| Component | Specification |
|-----------|---------------|
| Host OS | Windows 10 |
| WSL Distro | Ubuntu 26.04 LTS |
| RAM | 128 GB |
| VRAM | 11 GB |
| CPU | 24 threads |
| Primary Stack | Claude Code + Ollama |

## Research Domains

### 1. VS Code Fork Architecture
- Cursor, Kiro, Gemini patterns
- Extension host modifications
- AI context pipeline design
- Licensing considerations (MIT vs proprietary)

### 2. Ubuntu 26.04 Optimization
- WSL2 configuration for high-memory workloads
- Modern package managers (mise, uv, pnpm)
- Ollama GPU optimization
- Claude Code CLI tuning

### 3. Dotfiles Management
- Chezmoi for multi-machine config
- 4-tier .claude configuration:
  - Personal (`~/.claude`)
  - Project (`./<project>/.claude`)
  - Enterprise (`/etc/claude`)
  - Organization (GitHub org templates)

### 4. Team Git Culture
- Conventional commits
- CODEOWNERS for AI-generated code
- Branch strategies with AI agents
- Pre-commit hooks

### 5. Agent Protocols
- ACP (Agent Client Protocol) - Zed
- MCP (Model Context Protocol) - Anthropic
- A2A (Agent-to-Agent) - Google/Linux Foundation

## File Structure

```
research/jade-ide/
├── README.md                           # This file
├── unmodified_prompt.md                # Original research prompt
├── init.sh                             # Research orchestration script
├── 2604-research-append-progress.txt   # Append-only research log
├── bootstrap-2604.sh                   # Ubuntu 26.04 setup script
└── config/
    ├── wslconfig.example               # Windows .wslconfig template
    ├── wsl.conf.example                # Ubuntu /etc/wsl.conf template
    └── chezmoi.toml.example            # Chezmoi config template
```

## Running Research

```bash
# Execute the research orchestration
./init.sh

# View progress log
tail -f 2604-research-append-progress.txt

# Bootstrap a new Ubuntu 26.04 environment
./bootstrap-2604.sh
```

## Multi-Agent Research

The `init.sh` script launches parallel research agents that:
1. Conduct web searches on each domain
2. Append structured findings to the progress log
3. Synthesize recommendations

## Key Decisions Pending

- [ ] VS Code fork vs extension-only approach
- [ ] ACP vs MCP as primary protocol
- [ ] Chezmoi vs alternatives for dotfiles
- [ ] GitHub organization structure

## References

- [Zed Agent Client Protocol](https://zed.dev/acp)
- [Anthropic MCP Specification](https://github.com/anthropics/mcp)
- [Chezmoi Documentation](https://www.chezmoi.io/)
- [Cursor Architecture](https://cursor.sh/)

---

*Research initiated: 2026-01-23*
