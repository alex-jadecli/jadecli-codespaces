# FastMCP 3.0 Template Server

A production-ready MCP (Model Context Protocol) server template built with FastMCP 3.0, optimized for claude-code integration.

## 🚀 Features

### FastMCP 3.0 Capabilities

- **Tools** - Functions that LLMs can call to perform actions
- **Resources** - Data sources that LLMs can read
- **Prompts** - Reusable templates for LLM interactions
- **Context Injection** - Dependency injection for handlers
- **Lifespan Management** - Initialize/cleanup shared resources
- **OpenTelemetry Ready** - Built-in observability support

### Claude-Code Optimizations

- **Modular Architecture** - Separate tools, resources, and prompts
- **Secure Configuration** - Environment variable support
- **Comprehensive Logging** - Detailed request/response logging
- **Clear Documentation** - LLM-friendly docstrings
- **Type Safety** - Full type hints with Pydantic validation

## 📦 Installation

```bash
# Install dependencies
uv sync

# Or with pip
pip install -e .
```

## 🏃 Running the Server

### With FastMCP CLI (Recommended)

```bash
# Run directly
uv run fastmcp run mcp_server/server.py

# With development mode (auto-reload)
uv run fastmcp dev mcp_server/server.py
```

### As Python Module

```bash
python -m mcp_server
```

### With Custom Configuration

```bash
LOG_LEVEL=DEBUG uv run fastmcp run mcp_server/server.py
```

## 🔧 Claude-Code Integration

### Project-Level Configuration

The `.mcp.json` file is already configured for claude-code:

```json
{
  "mcpServers": {
    "template": {
      "command": "uv",
      "args": ["run", "fastmcp", "run", "mcp_server/server.py"],
      "env": {
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### User-Level Configuration

Add to `~/.claude.json` for global availability:

```json
{
  "mcpServers": {
    "my-tools": {
      "command": "uv",
      "args": ["--directory", "/path/to/project", "run", "fastmcp", "run", "mcp_server/server.py"]
    }
  }
}
```

## 📚 Available Components

### Tools

| Name | Description | Tags |
|------|-------------|------|
| `add` | Add two numbers together | math, arithmetic |
| `get_current_time` | Get current timestamp in ISO format | time, utility |
| `parse_json` | Parse and validate JSON data | json, validation |
| `search_items` | Search and filter a list of items | search, data |
| `summarize_text` | Generate text statistics and summary | text, analysis |

### Resources

| URI | Name | Description |
|-----|------|-------------|
| `config://server/info` | Server Information | Server configuration and status |
| `data://examples/{category}` | Example Data | Sample data (users, products, tasks) |
| `docs://readme` | Project README | Documentation and usage guide |
| `schema://tool/{tool_name}` | Tool Schema | JSON schema for tools |

### Prompts

| Name | Description | Arguments |
|------|-------------|-----------|
| `code_review` | Generate code review feedback | code, language, focus_areas |
| `explain_code` | Explain code functionality | code, language, detail_level |
| `generate_tests` | Generate test cases | code, language, test_framework, coverage_goal |
| `debug_error` | Help debug errors | error_message, code_context, stack_trace |
| `refactor_code` | Suggest refactoring improvements | code, language, goals |

## 🏗️ Project Structure

```
mcp_server/
├── __init__.py          # Package exports
├── __main__.py          # Module entry point
├── server.py            # Main server with tools, resources, prompts
└── README.md            # This documentation
```

## 🔌 Extending the Server

### Adding a New Tool

In `mcp_server/server.py`, add after the existing tools:

```python
@mcp.tool(
    description="Your tool description",
    tags={"category1", "category2"},
)
def my_new_tool(
    param1: Annotated[str, "Parameter description"],
    param2: Annotated[int, "Another parameter"] = 10,
) -> dict:
    """
    Detailed docstring for LLM understanding.
    
    Examples:
        my_new_tool("value", 20) -> {"result": "..."}
    """
    return {"result": "processed"}
```

### Adding a New Resource

In `mcp_server/server.py`, add after the existing resources:

```python
@mcp.resource(
    uri="mydata://category/{item_id}",
    name="My Data Resource",
    description="Description for LLM",
)
def get_my_data(item_id: str) -> str:
    """Fetch data for the specified item."""
    data = fetch_data(item_id)
    return json.dumps(data)
```

### Adding a New Prompt

In `mcp_server/server.py`, add after the existing prompts:

```python
@mcp.prompt(
    name="my_prompt",
    description="Description of what this prompt does",
)
def my_prompt_template(
    required_arg: str,
    optional_arg: str = "default",
) -> str:
    """Generate a custom prompt template."""
    return f"""Your prompt template here with {required_arg} and {optional_arg}."""
```

## 🔍 Observability

### Enable OpenTelemetry

```bash
# Install observability dependencies
uv sync --extra observability

# Configure OTEL
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"
export OTEL_SERVICE_NAME="fastmcp-template"

# Run with tracing
uv run fastmcp run mcp_server/server.py
```

## 🧪 Testing

```bash
# Run tests
uv run pytest

# With coverage
uv run pytest --cov=mcp_server
```

## 📖 Best Practices

### For Claude-Code Integration

1. **Keep tools focused** - Each tool should do one thing well
2. **Write clear docstrings** - LLMs use these to understand tool usage
3. **Use type hints** - Enables automatic schema generation
4. **Handle errors gracefully** - Return meaningful error messages
5. **Log important actions** - Helps with debugging

### For Production

1. **Use environment variables** - Never hardcode secrets
2. **Enable observability** - Use OpenTelemetry for tracing
3. **Implement rate limiting** - Protect against abuse
4. **Add authentication** - Secure sensitive tools
5. **Monitor performance** - Track response times and errors

## 📄 License

MIT License - See [LICENSE](../LICENSE) for details.
