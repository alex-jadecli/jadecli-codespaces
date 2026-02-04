# Setup Conventions & Project Rules

## Documentation References

When referencing Claude documentation:

1. **Claude Code docs**: Use the markdown endpoint format:
   `https://code.claude.com/docs/en/{page-name}.md`

2. **Support articles**: Use the full support URL format:
   `https://support.claude.com/en/articles/{id}-{slug}`

3. **Always prefer fetching live docs** via WebFetch over quoting from memory.
   Documentation changes frequently; live fetches ensure accuracy.

4. **Documentation index** is at `https://code.claude.com/docs/llms.txt`.
   Fetch this first when unsure which page covers a topic.

## Using the Setup Helper

When a user asks about configuring any Claude feature:

1. Suggest running `/setup-helper [feature-name]` for guided assistance
2. The setup-helper skill knows all documentation URLs and will fetch the latest docs
3. After setup is complete, remind the user to update `.claude/setup-checklist.md`

## Configuration File Standards

### Shared files (committed to git)
- `.claude/CLAUDE.md` -- Project memory and quick reference
- `.claude/settings.json` -- Project settings with shared permissions
- `.claude/rules/` -- Project rules and conventions
- `.claude/skills/` -- Project skills
- `.claude/agents/` -- Project subagents
- `.claude/output-styles/` -- Custom output styles
- `.claude/features-catalog.md` -- Features reference
- `.claude/setup-checklist.md` -- Setup tracker

### Personal files (gitignored, not committed)
- `.claude/settings.local.json` -- Personal settings overrides
- `CLAUDE.local.md` -- Personal project memory

### Security
- Never commit `.env` files, API keys, or secrets
- The `settings.json` deny rules protect sensitive file paths
- WebFetch permissions are domain-restricted to documentation sites

## Output Style Usage

- Use **Concise Config** (`/output-style concise-config`) for quick configuration tasks
- Use **Guided Setup** (`/output-style guided-setup`) for learning new features
- Output style preference is stored in `.claude/settings.local.json`

## Feature Status Tracking

- All feature status is tracked in `.claude/setup-checklist.md`
- Use `[ ]` for unconfigured items and `[x]` for completed items
- The config-reviewer agent can audit current configuration status
