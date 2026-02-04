# Complete Features & Personalization Catalog

## 1. Styles (claude.ai)

Styles customize how Claude communicates — tone, format, and delivery of responses.

### Preset Styles
- **Normal** — Default responses (always visible, cannot be hidden)
- **Concise** — Shorter, more direct responses (always visible, cannot be hidden)
- **Formal** — Clear and polished responses (can be hidden)
- **Explanatory** — Educational responses for learning new concepts (can be hidden)

### Custom Styles
Create unlimited custom styles via:
- **Upload Writing Samples** — PDF, DOC, or TXT file; Claude analyzes and generates a matching style
- **Describe Your Style** — Pick a starting point, describe preferences, or use advanced custom instructions

### Management
- Reorder (drag handle), rename, preview, edit instructions (with Claude or manually), delete
- Access: Search and tools menu > Use style > Create & edit styles

### Docs
- https://support.claude.com/en/articles/10181068-configuring-and-using-styles

---

## 2. Profile Preferences (claude.ai)

Account-wide settings applied to ALL conversations. Include:
- Preferred approaches or methods
- Common terms or concepts
- Typical scenarios
- General communication preferences

### Setup
Click initials (lower left) > Settings > "What preferences should Claude consider in responses?"

### Docs
- https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features

---

## 3. Memory & Chat Search (claude.ai)

### Chat Search (RAG) — Pro, Max, Team, Enterprise
- Claude searches conversation history using RAG
- Searches non-project chats and within individual projects separately
- Toggle: Settings > Capabilities > "Search and reference chats"
- Incognito chats are excluded (available to all plans)

### Memory — Pro, Max, Team, Enterprise
- Auto-summarizes conversations into persistent memory (updated every 24 hours)
- Separate memory space per project
- Claude remembers: role, projects, professional context, communication/working style, technical preferences, coding style, project details, ongoing work
- View/edit: Settings > Capabilities > "View and edit memory"
- Can also tell Claude directly in conversation what to remember
- Pause memory (keeps existing, stops new) or Reset memory (permanent delete)
- Import/export memory between Claude and other AI tools

### Docs
- https://support.claude.com/en/articles/11817273-using-claude-s-chat-search-and-memory-to-build-on-previous-context

---

## 4. Projects (claude.ai)

### Features (all plans, free users max 5 projects)
- Create projects with name and description
- Project knowledge base (upload docs, text, code as persistent context)
- Project instructions (custom behavior/response guidelines for the project)
- RAG mode (auto-enabled when knowledge approaches context limit, paid plans)
- Star projects for quick sidebar access
- Move chats into/out of projects (individually or in bulk)
- Archive projects (declutter, resets sharing permissions)

### Visibility & Sharing (Team/Enterprise only)
- Public projects — visible to entire organization
- Private projects — only invited members
- Share with members: Can View or Can Edit permissions
- Bulk member adding (paste email addresses)
- Share individual chats (shareable link snapshots)

### Docs
- https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects
- https://support.claude.com/en/articles/9519189-project-visibility-and-sharing

---

## 5. Integrations & Connectors (claude.ai)

### First-Party Integrations (availability: Free/Pro/Max/Team/Enterprise)
- **GitHub** — all plans
- **Google Drive** — all plans (Google Docs only, up to 10MB, text only, stays synced)
- **Gmail** — all plans (read-only, auto-detects, includes citations)
- **Google Calendar** — all plans (read-only, auto-detects, includes citations)
- **Google Drive Cataloging** — Enterprise only

### Setup
- Individuals: Settings > Connectors > Connect > Authenticate
- Team/Enterprise: Admin settings > Connectors > Enable (Owner first, then users authenticate)
- Security: All transfers encrypted, permission-gated, private projects only on Team/Enterprise

### Connectors Directory (MCP-powered)
- Browse at https://claude.ai/directory
- **Web connectors** — Google Drive, Gmail, Asana, Notion, Canva, Linear, etc.
- **Desktop extensions** (app only) — Apple Notes, local files, code files, messages
- Setup: In chat > Search and tools menu > Add connectors > Select > Connect > Authenticate

### Docs
- https://support.claude.com/en/articles/10168395-setting-up-claude-integrations
- https://support.claude.com/en/articles/10166901-using-the-google-drive-integration
- https://support.claude.com/en/articles/11088742-using-the-gmail-and-google-calendar-integrations
- https://support.claude.com/en/articles/11817150-connect-your-tools-to-unlock-a-smarter-more-capable-ai-companion

---

## 6. Claude Code — Configuration & Extensibility

### Memory (CLAUDE.md)

| Type | Location | Scope |
|---|---|---|
| Managed policy | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | All users (org-wide) |
| Project memory | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team (via git) |
| Project rules | `./.claude/rules/*.md` | Team (via git) |
| User memory | `~/.claude/CLAUDE.md` | Personal (all projects) |
| Local project memory | `./CLAUDE.local.md` | Personal (this project) |

- Bootstrap: `/init`
- Edit: `/memory`
- Supports `@path/to/import` syntax
- Docs: https://code.claude.com/docs/en/memory.md

### Output Styles

| Style | Description |
|---|---|
| Default | Standard software engineering system prompt |
| Explanatory | Educational "Insights" while coding |
| Learning | Collaborative learn-by-doing with `TODO(human)` markers |
| Custom | `.md` files in `~/.claude/output-styles/` or `.claude/output-styles/` |

- Switch: `/output-style` or `/output-style [name]`
- Docs: https://code.claude.com/docs/en/output-styles.md

### Skills (Custom Slash Commands)
- `~/.claude/skills/` — personal (all projects)
- `.claude/skills/` — project (shared via git)
- `.claude/commands/` — legacy (still works)
- Invoke: `/skill-name` or auto-loaded when relevant
- Docs: https://code.claude.com/docs/en/skills.md

### Subagents
- `~/.claude/agents/` — personal
- `.claude/agents/` — project (shared via git)
- Manage: `/agents` command or `--agents` CLI flag
- Docs: https://code.claude.com/docs/en/sub-agents.md

### MCP Servers
- `~/.claude.json` — user-level
- `.mcp.json` — project-level
- Manage: `/mcp` command or `claude mcp` CLI
- Docs: https://code.claude.com/docs/en/mcp.md

### Hooks

| Event | When It Runs |
|---|---|
| PreToolUse | Before a tool executes |
| PostToolUse | After a tool executes |
| SessionStart | When a session begins |

- Configure in `.claude/settings.json` under `"hooks"`
- Docs: https://code.claude.com/docs/en/hooks-guide.md / https://code.claude.com/docs/en/hooks.md

### Plugins
- Manage: `/plugin` command
- Docs: https://code.claude.com/docs/en/plugins.md / https://code.claude.com/docs/en/discover-plugins.md

### Settings Files

| File | Scope | Shared |
|---|---|---|
| `~/.claude/settings.json` | User (all projects) | No |
| `.claude/settings.json` | Project (team) | Yes (git) |
| `.claude/settings.local.json` | Local project | No (gitignored) |
| Managed `managed-settings.json` | Organization | Yes (IT deployed) |

- Key settings: permissions, model, env, hooks, outputStyle, sandbox, attribution, alwaysThinkingEnabled, language, spinnerVerbs
- Docs: https://code.claude.com/docs/en/settings.md

---

## 7. Documentation Access

| Resource | URL | Description |
|---|---|---|
| Docs Index | https://code.claude.com/docs/llms.txt | Index of all doc pages with .md URLs |
| Full Docs | https://code.claude.com/docs/llms-full.txt | Entire documentation in one file |
| Any Page (md) | `https://code.claude.com/docs/en/{page-name}.md` | Markdown version of any doc page |
| Any Page (html) | `https://code.claude.com/docs/en/{page-name}` | Rendered HTML version |

### Claude Code Doc Pages

| Topic | Markdown URL |
|---|---|
| Overview | https://code.claude.com/docs/en/overview.md |
| Settings | https://code.claude.com/docs/en/settings.md |
| Memory | https://code.claude.com/docs/en/memory.md |
| Skills | https://code.claude.com/docs/en/skills.md |
| Output Styles | https://code.claude.com/docs/en/output-styles.md |
| Subagents | https://code.claude.com/docs/en/sub-agents.md |
| MCP | https://code.claude.com/docs/en/mcp.md |
| Hooks Guide | https://code.claude.com/docs/en/hooks-guide.md |
| Hooks Reference | https://code.claude.com/docs/en/hooks.md |
| Plugins | https://code.claude.com/docs/en/plugins.md |
| Discover Plugins | https://code.claude.com/docs/en/discover-plugins.md |
| CLI Reference | https://code.claude.com/docs/en/cli-reference.md |
| Interactive Mode | https://code.claude.com/docs/en/interactive-mode.md |
| How Claude Code Works | https://code.claude.com/docs/en/how-claude-code-works.md |
| Common Workflows | https://code.claude.com/docs/en/common-workflows.md |
| Best Practices | https://code.claude.com/docs/en/best-practices.md |
| Features Overview | https://code.claude.com/docs/en/features-overview.md |
| Sandboxing | https://code.claude.com/docs/en/sandboxing.md |
| Checkpointing | https://code.claude.com/docs/en/checkpointing.md |
| Keybindings | https://code.claude.com/docs/en/keybindings.md |
| Terminal Config | https://code.claude.com/docs/en/terminal-config.md |
| Troubleshooting | https://code.claude.com/docs/en/troubleshooting.md |

### Support Articles (claude.ai features)

| Topic | URL |
|---|---|
| Styles | https://support.claude.com/en/articles/10181068-configuring-and-using-styles |
| Chat Search & Memory | https://support.claude.com/en/articles/11817273-using-claude-s-chat-search-and-memory-to-build-on-previous-context |
| Personalization Features | https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features |
| Creating Projects | https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects |
| Project Sharing | https://support.claude.com/en/articles/9519189-project-visibility-and-sharing |
| Google Drive | https://support.claude.com/en/articles/10166901-using-the-google-drive-integration |
| Connectors | https://support.claude.com/en/articles/11817150-connect-your-tools-to-unlock-a-smarter-more-capable-ai-companion |
| Gmail & Calendar | https://support.claude.com/en/articles/11088742-using-the-gmail-and-google-calendar-integrations |
| Setting Up Integrations | https://support.claude.com/en/articles/10168395-setting-up-claude-integrations |
| Connectors Directory | https://claude.ai/directory |
