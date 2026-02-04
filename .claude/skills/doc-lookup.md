# Doc Lookup Skill

Use this skill to search local documentation before making API calls or guessing.

## When to Use

- User asks about tools (ruff, uv, ty, chezmoi)
- User asks about platforms (Anthropic, Claude, WSL)
- You need to verify a command/flag
- You're unsure about an API

## How to Use

**Step 1: Formulate query**
- What specific info do you need?
- Example: "ruff select rule syntax"

**Step 2: Run search**
```bash
doc-index search "your query" --top-k 3
```

**Step 3: Review results**
- Read the top result content
- If not helpful, refine query and try again

**Step 4: Apply knowledge**
- Use the documentation info in your response
- Cite the source file

## Examples

```bash
# Find ruff configuration
doc-index search "ruff pyproject.toml configuration"

# Find uv usage
doc-index search "uv pip install package"

# Find Anthropic API docs
doc-index search "anthropic messages api prompt caching"
```

## Cache Benefits

- Embeddings cached in Redis (24hr TTL)
- Repeated queries use cache → no API calls
- jade-swarm can query docs without token cost
