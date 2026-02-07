# Generated Documentation Artifacts

Auto-generated indexes, summaries, and quick references for jadecli-codespaces documentation.

Generated: February 2026 | Source: 200 markdown files across 9 categories | Total content: ~1.0MB

---

## Contents

### 1. Master Index

**File:** [master-index.md](master-index.md)

Complete table of contents for all documentation with:
- Organized by category (9 categories, 200 files)
- File sizes and descriptions
- Quick links section for common tasks
- Statistics and file organization
- Common workflows indexed

**Use when:**
- You're new to the documentation
- You need to find something but don't know where
- You want an overview of what's available

---

### 2. Quick Reference Cheat Sheets

Location: `quick-reference/`

**Five one-page reference cards:**

| File | Purpose | Length |
|------|---------|--------|
| [uv-quick-ref.md](quick-reference/uv-quick-ref.md) | Package manager commands | ~1 page |
| [ruff-quick-ref.md](quick-reference/ruff-quick-ref.md) | Linter/formatter commands | ~1 page |
| [ty-quick-ref.md](quick-reference/ty-quick-ref.md) | Type checker commands | ~1 page |
| [platform-claude-quick-ref.md](quick-reference/platform-claude-quick-ref.md) | Claude API essentials | ~1 page |
| [anthropic-quick-ref.md](quick-reference/anthropic-quick-ref.md) | Anthropic company overview | ~1 page |

**Use when:**
- You need a command syntax quickly
- You want examples without detailed explanation
- You're mid-coding and need a reminder

---

### 3. Cross-References Map

**File:** [cross-references.md](cross-references.md)

Shows how documentation tools connect:
- Python development workflow (uv → ruff → ty → pytest)
- Claude API decision tree
- GitHub project management workflow
- Terminal & IDE setup stack
- Common use cases with mapped docs

**Use when:**
- You're starting something new (project, API call, team setup)
- You want to understand tool relationships
- You're choosing between multiple docs

---

### 4. LLM-Optimized Summaries

Location: `summaries/`

**Five cached summaries (<1K tokens each):**

| File | Topic | Purpose |
|------|-------|---------|
| [python-tools-summary.md](summaries/python-tools-summary.md) | uv, ruff, ty | Essential concepts + architecture + patterns |
| [claude-api-summary.md](summaries/claude-api-summary.md) | Claude API | Core concepts + patterns + parameters |
| [github-workflow-summary.md](summaries/github-workflow-summary.md) | Issues & Projects | Concepts + automation + tracking |
| [terminal-setup-summary.md](summaries/terminal-setup-summary.md) | WSL2, terminals | Stack + choices + config basics |
| [anthropic-resources-summary.md](summaries/anthropic-resources-summary.md) | Anthropic company | Overview + research + careers |

**Optimizations for LLM consumption:**
- Structured information (tables, lists, code examples)
- Cross-links to full docs
- Token-efficient wording
- Clear categories and sections

**Use when:**
- You're an AI agent making decisions
- You need context optimization for token budget
- You want comprehensive overview in <1K tokens

---

## Navigation Guide

### By User Type

**New Developer:**
1. Start: [master-index.md](master-index.md) → "Getting Started" section
2. Reference: Pick relevant quick-ref (uv, ruff, ty)
3. Details: Follow links to full documentation

**Python Developer:**
1. Overview: [python-tools-summary.md](summaries/python-tools-summary.md)
2. Setup: [uv-quick-ref.md](quick-reference/uv-quick-ref.md)
3. Quality: [ruff-quick-ref.md](quick-reference/ruff-quick-ref.md) + [ty-quick-ref.md](quick-reference/ty-quick-ref.md)

**Claude API Developer:**
1. Start: [platform-claude-quick-ref.md](quick-reference/platform-claude-quick-ref.md)
2. Patterns: [claude-api-summary.md](summaries/claude-api-summary.md)
3. Examples: [../platform-claude/cookbooks.md](../platform-claude/cookbooks.md)

**Project Manager:**
1. Overview: [cross-references.md](cross-references.md) → "GitHub Project Management"
2. Details: [github-workflow-summary.md](summaries/github-workflow-summary.md)
3. Full docs: [../guides/](../guides/)

**DevOps/Terminal Setup:**
1. Stack: [terminal-setup-summary.md](summaries/terminal-setup-summary.md)
2. Choices: [cross-references.md](cross-references.md) → "Terminal & IDE Setup"
3. Config: [../wslg/](../wslg/)

**AI Agent (LLM Context):**
1. Use: `summaries/` for decision making
2. Reference: `quick-reference/` for specific commands
3. Full info: Links to source docs

---

## File Organization

```
docs/generated/
├── README.md (this file)
├── master-index.md (complete TOC)
├── cross-references.md (tool relationships)
├── quick-reference/
│   ├── uv-quick-ref.md
│   ├── ruff-quick-ref.md
│   ├── ty-quick-ref.md
│   ├── platform-claude-quick-ref.md
│   └── anthropic-quick-ref.md
└── summaries/
    ├── python-tools-summary.md
    ├── claude-api-summary.md
    ├── github-workflow-summary.md
    ├── terminal-setup-summary.md
    └── anthropic-resources-summary.md
```

---

## Statistics

| Artifact | Files | Type | Tokens |
|----------|-------|------|--------|
| master-index.md | 1 | Index | ~1,200 |
| cross-references.md | 1 | Map | ~900 |
| Quick refs | 5 | Cheat sheets | 400-500 each |
| Summaries | 5 | LLM-optimized | 800-950 each |
| **TOTAL** | **12** | Mixed | **~8.5K** |

**Token Budget:** All artifacts fit within 40K token limit (actual: ~8.5K)

---

## Best Practices

### For Humans

1. **First time?** → Read master-index.md "Quick Links"
2. **Need syntax?** → Find quick-reference cheat sheet
3. **Understanding flow?** → Check cross-references.md
4. **Deep dive?** → Follow links to full documentation

### For AI Agents

1. **Decision needed?** → Check relevant summary first
2. **Context limited?** → Use summaries instead of full docs
3. **Token budget?** → Summaries are 5-10x more concise
4. **Implementation?** → Use quick-refs for commands
5. **Full details?** → Link to source docs as needed

### For Documentation Maintenance

- Master index auto-generated from directory structure
- Summaries manually crafted for clarity
- Quick refs extracted from full documentation
- Cross-references show tool relationships
- All links use relative paths

---

## Updating These Artifacts

**When to regenerate:**
- New documentation category added
- File structure changes
- Major version updates to tools
- Adding new quick-reference tools

**How to regenerate:**
1. Scan documentation directory structure
2. Update file counts and sizes
3. Regenerate master index
4. Verify all links
5. Update this README

---

## Related Resources

- **Full documentation:** [../](../)
- **Source index:** [../anthropic/index.md](../anthropic/index.md)
- **Project docs:** [../../jade-dev-assist/](../../jade-dev-assist/)

---

## Notes

- All links are relative and should work from this directory
- Summaries optimized for token efficiency, not comprehensiveness
- Quick refs assume basic familiarity with tools
- Cross-references show primary use patterns, not all possible combinations

---

Generated: February 4, 2026 | Last Updated: 2026-02-04
