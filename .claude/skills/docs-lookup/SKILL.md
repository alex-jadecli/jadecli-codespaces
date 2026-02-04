---
description: Fetch and display any Claude Code or Claude.ai documentation page. Use when the user asks about Claude features, wants to read documentation, or needs reference material about Claude Code capabilities.
argument-hint: [topic-or-url]
allowed-tools: Read, WebFetch
---

# Documentation Lookup

Fetch and display documentation for the user.

## Resolution Order

Process `$ARGUMENTS` in this priority order:

1. **Full URL** — If the argument starts with `http`, fetch it directly with WebFetch
2. **Claude Code page name** — If it matches a known page name, construct:
   `https://code.claude.com/docs/en/{page-name}.md`
   Known pages: settings, memory, skills, output-styles, sub-agents, mcp, hooks-guide,
   hooks, plugins, discover-plugins, cli-reference, interactive-mode,
   how-claude-code-works, common-workflows, best-practices, features-overview,
   overview, sandboxing, checkpointing, keybindings, terminal-config, troubleshooting
3. **Support topic** — If it matches a support keyword, use the corresponding URL:

| Keyword | URL |
|---|---|
| `styles` | https://support.claude.com/en/articles/10181068-configuring-and-using-styles |
| `chat-search` or `memory` | https://support.claude.com/en/articles/11817273-using-claude-s-chat-search-and-memory-to-build-on-previous-context |
| `personalization` | https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features |
| `projects` | https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects |
| `project-sharing` | https://support.claude.com/en/articles/9519189-project-visibility-and-sharing |
| `google-drive` | https://support.claude.com/en/articles/10166901-using-the-google-drive-integration |
| `connectors` | https://support.claude.com/en/articles/11817150-connect-your-tools-to-unlock-a-smarter-more-capable-ai-companion |
| `gmail` or `calendar` | https://support.claude.com/en/articles/11088742-using-the-gmail-and-google-calendar-integrations |
| `integrations` | https://support.claude.com/en/articles/10168395-setting-up-claude-integrations |

4. **Index** — If the argument is `index` or `all`, fetch: `https://code.claude.com/docs/llms.txt`
5. **Full corpus** — If the argument is `full`, fetch: `https://code.claude.com/docs/llms-full.txt`
6. **Ambiguous** — Read `.claude/features-catalog.md` to find the best match, then fetch
   `https://code.claude.com/docs/llms.txt` to search the index for the topic

## Presentation

- Show the source URL at the top of your response
- Preserve the original heading structure from the fetched content
- Highlight the most relevant sections if the content is long
- If the content mentions related pages, note them for further lookup
