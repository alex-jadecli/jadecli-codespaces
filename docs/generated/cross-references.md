# Cross-References: How Documentation Tools Connect

This document maps relationships between tools and documentation, showing how they work together in common workflows.

## Python Development Workflow

### The Python Quality Chain

```
uv (Package Mgmt)
    ↓
ruff (Lint/Format)
    ↓
ty (Type Check)
    ↓
pytest (Test)
```

**When to use each:**

1. **UV** → `uv add`, `uv sync`, `uv run`
   - Manages dependencies (replaces pip, poetry)
   - Creates/maintains lock file
   - Provides isolated environments

2. **Ruff** → `ruff check --fix`, `ruff format`
   - Catches style violations and bugs
   - Auto-formats code
   - Organizes imports (isort replacement)
   - **Runs after:** adding code
   - **Before:** type checking

3. **Ty** → `ty check`
   - Finds type mismatches
   - Requires type annotations (Python 3.8+)
   - Catches logic errors at compile-time
   - **Runs after:** ruff fixes code style
   - **Before:** testing/deployment

4. **Pytest** → `uv run pytest`
   - Validates runtime behavior
   - Uses uv to manage test dependencies

**Example Workflow:**

```bash
# 1. Start project
uv init my_app && cd my_app

# 2. Add dependencies
uv add requests
uv add --dev ruff ty pytest

# 3. Write code
# ... create src/main.py

# 4. Run quality checks (pre-commit or manual)
ruff check --fix src/         # Fix style
ruff format src/              # Format
ty check src/                 # Type errors
uv run pytest                 # Test

# 5. Commit
git commit -m "feat: add API client"
```

---

## Claude API Development

### API Usage Decision Tree

```
                    Need Claude?
                        |
            ____________|____________
           |                        |
      Simple Chat              Complex Task
           |                        |
    - Claude.ai              Use Claude API
    - Claude on platform     - Tool use
                             - Vision
                             - Streaming
                             - Batch processing
```

**Documentation Paths:**

1. **Understanding Claude API** → [claude-api-primer.md](../platform-claude/claude-api-primer.md)
   - Models and pricing
   - Basic API structure
   - Message format
   - Token counting

2. **Implementing Patterns** → [cookbooks.md](../platform-claude/cookbooks.md)
   - RAG (retrieval-augmented generation)
   - Agents and tool use
   - Vision processing
   - Batch processing
   - Streaming responses

3. **Prompt Optimization** → [prompt-library.md](../platform-claude/prompt-library.md)
   - 100+ example prompts
   - Writing, analysis, coding
   - System prompts
   - Few-shot examples

4. **Technical Terms** → [glossary.md](../platform-claude/glossary.md)
   - LLM terminology
   - Claude-specific concepts
   - Architecture terms

**Example Implementation:**

```python
# 1. Read primer to understand basics
# (docs/platform-claude/claude-api-primer.md)

# 2. Find similar cookbook pattern
# (docs/platform-claude/cookbooks.md)

# 3. Adapt example code
import anthropic
client = anthropic.Anthropic()

# 4. Check glossary for unfamiliar terms
# (docs/platform-claude/glossary.md)

# 5. Copy prompt template from library
# (docs/platform-claude/prompt-library.md)

prompt = """
[Your adapted prompt from library]
"""

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)
```

---

## GitHub Project Management

### Issue Workflow

```
Create Issue → Categorize → Link to Project → Track Progress → Close
    |              |            |                 |              |
 [02]           [05]          [11]              [09]           [17]
                [17]          [16]              [19]           [18]
```

**Documentation Path:**

1. **Learn Basics** → [01-quickstart-issues.md](../guides/01-quickstart-issues.md)
   - Create your first issue
   - Basic fields

2. **Create Issues** → [02-creating-issue.md](../guides/02-creating-issue.md)
   - Title, description, labels
   - Assignees, milestones

3. **Organize** → [05-issue-types.md](../guides/05-issue-types.md) + [17-managing-labels.md](../guides/17-managing-labels.md)
   - Bug vs Feature vs Documentation
   - Custom labels

4. **Link Issues** → [03-sub-issues.md](../guides/03-sub-issues.md) + [04-issue-dependencies.md](../guides/04-issue-dependencies.md)
   - Parent-child relationships
   - Blocking dependencies

5. **Track in Project** → [11-creating-project.md](../guides/11-creating-project.md)
   - Create project board
   - Configure views (table, board, roadmap)

6. **Manage Progress** → [09-planning-tracking.md](../guides/09-planning-tracking.md) + [19-built-in-automations.md](../guides/19-built-in-automations.md)
   - Move between status columns
   - Auto-archive completed
   - Burndown charts

7. **Set Targets** → [18-milestones.md](../guides/18-milestones.md)
   - Milestone deadlines
   - Release planning

**Typical Project Setup:**

```bash
# 1. Create project (see 11-creating-project.md)
# 2. Add fields (see 12-understanding-fields.md)
# 3. Create view (see 13-customizing-views.md)
# 4. Add automation rules (see 19-built-in-automations.md)
# 5. Start adding issues (see 16-adding-items.md)
```

---

## Terminal & IDE Setup

### Environment Stack

```
WSL2 (Windows Subsystem Linux)
    ↓
Terminal Emulator (Kitty/Ghostty/WezTerm)
    ↓
Claude Code IDE
    ↓
Python Tools (uv, ruff, ty)
```

**Documentation:**

1. **WSL2 Overview** → [wslg/README.md](../wslg/README.md)
   - Windows Subsystem for Linux graphics
   - GPU support
   - File system integration

2. **Terminal Choice** → Pick one:
   - Kitty: GPU-accelerated, modern ([kitty-config.md](../wslg/kitty-config.md))
   - Ghostty: Fast, feature-rich ([ghostty-config.md](../wslg/ghostty-config.md))
   - WezTerm: Lua config, multiplexing ([wezterm-config.md](../wslg/wezterm-config.md))

3. **Claude Code Terminal** → [claude-code-terminal-config.md](../wslg/claude-code-terminal-config.md)
   - IDE-integrated terminal setup
   - Font, colors, keyboard shortcuts

4. **Dotfiles** → [chezmoi/README.md](../chezmoi/README.md)
   - Sync config across machines
   - Template examples

---

## Setup & Configuration

### Platform Features Chain

```
Create Account
    ↓
Configure Styles ([01](../setup-claude/01-configuring-and-using-styles.md))
    ↓
Add Chat Memory ([02](../setup-claude/02-chat-search-and-memory.md))
    ↓
Customize Profile ([03](../setup-claude/03-personalization-features.md))
    ↓
Create Projects ([04](../setup-claude/04-create-and-manage-projects.md))
    ↓
Share & Collaborate ([05](../setup-claude/05-project-visibility-and-sharing.md))
    ↓
Connect Tools ([06-09](../setup-claude/))
    ↓
Mobile Integration ([10](../setup-claude/10-ios-intents-shortcuts-widgets.md))
```

---

## Common Use Cases

### "I'm starting a new Python project"

1. Read: [uv/guides/04-working-on-projects.md](../uv/guides/04-working-on-projects.md)
   - Project structure
   - Dependency management

2. Configure: [ty/04-configuration.md](../ty/04-configuration.md)
   - Type checking in pyproject.toml

3. Configure: [ruff/04-configuring-ruff.md](../ruff/04-configuring-ruff.md)
   - Linting and formatting rules

4. Result: Solid foundation with quality gates in place

### "I need to call Claude API"

1. Read: [platform-claude/claude-api-primer.md](../platform-claude/claude-api-primer.md)
   - Understand basics (models, messages, tools)

2. Find: [platform-claude/cookbooks.md](../platform-claude/cookbooks.md)
   - Pattern similar to your use case

3. Use: [platform-claude/prompt-library.md](../platform-claude/prompt-library.md)
   - Adapt a prompt template

4. Reference: [platform-claude/glossary.md](../platform-claude/glossary.md)
   - Look up technical terms as needed

### "I'm managing a team project"

1. Create: [guides/11-creating-project.md](../guides/11-creating-project.md)
   - New GitHub project

2. Configure: [guides/12-understanding-fields.md](../guides/12-understanding-fields.md)
   - Custom fields (priority, effort, etc.)

3. Setup: [guides/13-customizing-views.md](../guides/13-customizing-views.md)
   - Board view for sprints
   - Roadmap view for timeline

4. Automate: [guides/19-built-in-automations.md](../guides/19-built-in-automations.md)
   - Auto-move on status change
   - Auto-archive completed items

5. Track: [guides/14-creating-charts.md](../guides/14-creating-charts.md)
   - Burndown and velocity charts

### "I'm setting up a developer machine"

1. Configure: [chezmoi/README.md](../chezmoi/README.md)
   - Dotfiles management

2. Install: [uv/guides/01-installing-python.md](../uv/guides/01-installing-python.md)
   - Python + uv

3. Pick: Terminal ([wslg/](../wslg/))
   - Kitty, Ghostty, or WezTerm

4. Configure: [wslg/claude-code-terminal-config.md](../wslg/claude-code-terminal-config.md)
   - IDE terminal setup

5. Read: [setup-claude/](../setup-claude/)
   - Platform features and integrations

---

## Dependencies & Compatibility

### Tool Versions

| Tool | Latest | Requires | Tested With |
|------|--------|----------|-------------|
| uv | 0.x | Python 3.8+ | 3.10, 3.11, 3.12 |
| ruff | 0.x | Python 3.8+ | All versions |
| ty | Latest | Python 3.8+ | All versions |
| pytest | Latest | Python 3.7+ | 3.10, 3.11, 3.12 |

### Documentation Cross-Links

- **Python Tools:** uv ← → ruff, ty, pytest
- **API Tools:** Claude API ← → Anthropic docs, cookbook patterns
- **Project Management:** GitHub Issues ← → Projects, automation
- **System Setup:** WSL2 ← → Terminal ← → Claude Code ← → Python tools

---

## Quick Navigation by Task

| Task | Documents |
|------|-----------|
| Start Python project | [uv guides](../uv/guides/) + [ruff config](../ruff/) + [ty config](../ty/) |
| Add dependency | [uv concepts](../uv/concepts/) + [uv guides](../uv/guides/) |
| Fix code quality | [ruff linter](../ruff/02-ruff-linter.md) + [ruff formatter](../ruff/03-ruff-formatter.md) |
| Type check code | [ty type checking](../ty/02-type-checking.md) + [ty rules](../ty/05-rules.md) |
| Call Claude API | [primer](../platform-claude/claude-api-primer.md) + [cookbooks](../platform-claude/cookbooks.md) |
| Create GitHub issue | [issue guides](../guides/01-quickstart-issues.md) through [07-viewing-issues.md](../guides/07-viewing-issues.md) |
| Track project | [project guides](../guides/08-quickstart-projects.md) through [21-actions-automation.md](../guides/21-actions-automation.md) |
| Setup terminal | [wslg README](../wslg/README.md) + pick terminal config |
| Configure dotfiles | [chezmoi README](../chezmoi/README.md) |

---

**Last Updated:** February 2026
