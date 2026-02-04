"""
FastMCP Server - Main Entry Point

Optimized per claude-code MCP recommendations:
- Modular architecture with separate concerns
- Clear tool/resource/prompt documentation
"""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from typing import Annotated, Any

from fastmcp import FastMCP

logger = logging.getLogger(__name__)

# Create the server instance
mcp = FastMCP(
    name="FastMCP Template Server",
)


# =============================================================================
# TOOLS - Functions that LLMs can call to perform actions
# =============================================================================


@mcp.tool(
    description="Add two numbers together",
    tags={"math", "arithmetic"},
)
def add(
    a: Annotated[int | float, "First number to add"],
    b: Annotated[int | float, "Second number to add"],
) -> int | float:
    """
    Add two numbers and return the result.

    This is a simple arithmetic tool demonstrating FastMCP's
    type annotation and documentation features.

    Examples:
        add(2, 3) -> 5
        add(1.5, 2.5) -> 4.0
    """
    result = a + b
    logger.info(f"add({a}, {b}) = {result}")
    return result


@mcp.tool(
    description="Get the current date and time in UTC ISO format",
    tags={"time", "utility"},
)
def get_current_time() -> str:
    """
    Get the current date and time in UTC.

    Returns the current timestamp in ISO 8601 format.
    Always uses UTC timezone for consistency.

    Examples:
        get_current_time() -> "2024-01-15T10:30:00+00:00"
    """
    now = datetime.now(UTC)
    return now.isoformat()


@mcp.tool(
    description="Parse and validate JSON data",
    tags={"json", "validation", "utility"},
)
def parse_json(
    json_string: Annotated[str, "JSON string to parse and validate"],
) -> Any:
    """
    Parse a JSON string and return the parsed object.

    This tool validates that the input is valid JSON and returns
    the parsed Python object (dict, list, str, int, float, bool, or None).
    Useful for processing structured data from various sources.

    Examples:
        parse_json('{"key": "value"}') -> {"key": "value"}
        parse_json('[1, 2, 3]') -> [1, 2, 3]
        parse_json('"hello"') -> "hello"

    Raises:
        ValueError: If the input is not valid JSON
    """
    try:
        result = json.loads(json_string)
        logger.info(f"Successfully parsed JSON: {type(result).__name__}")
        return result
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON: {e.msg} at position {e.pos}"
        logger.error(error_msg)
        raise ValueError(error_msg) from e


@mcp.tool(
    description="Search and filter a list of items",
    tags={"search", "filter", "data"},
)
def search_items(
    items: Annotated[list[dict[str, Any]], "List of items to search"],
    query: Annotated[str, "Search query string"],
    field: Annotated[str, "Field name to search in"] = "name",
    case_sensitive: Annotated[bool, "Whether search is case-sensitive"] = False,
) -> list[dict[str, Any]]:
    """
    Search through a list of items by a specific field.

    Filters items where the specified field contains the query string.
    Useful for searching through collections of data.

    Examples:
        search_items(
            [{"name": "Alice"}, {"name": "Bob"}],
            query="ali",
            field="name"
        ) -> [{"name": "Alice"}]
    """
    results = []
    search_query = query if case_sensitive else query.lower()

    for item in items:
        if field in item:
            field_value = str(item[field])
            if not case_sensitive:
                field_value = field_value.lower()
            if search_query in field_value:
                results.append(item)

    logger.info(f"Search found {len(results)} matching items")
    return results


@mcp.tool(
    description="Generate a summary of text content",
    tags={"text", "summary", "analysis"},
)
def summarize_text(
    text: Annotated[str, "Text content to summarize"],
    max_sentences: Annotated[int, "Maximum sentences in summary"] = 3,
) -> dict[str, Any]:
    """
    Generate statistics and a brief summary of text content.

    Analyzes the text and returns word count, sentence count,
    and the first few sentences as a summary.

    Useful for quickly understanding long documents.
    """
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    words = text.split()

    summary_sentences = sentences[:max_sentences]
    summary = ". ".join(summary_sentences)
    if summary and not summary.endswith("."):
        summary += "."

    result = {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "character_count": len(text),
        "summary": summary,
    }

    logger.info(f"Summarized text: {result['word_count']} words")
    return result


# =============================================================================
# RESOURCES - Data sources that LLMs can read
# =============================================================================


@mcp.resource(
    uri="config://server/info",
    name="Server Information",
    description="Get information about the MCP server configuration",
)
def get_server_info() -> str:
    """
    Return server configuration and status information.

    Provides metadata about the running server instance,
    useful for debugging and monitoring.
    """
    info = {
        "name": "FastMCP Template Server",
        "version": "0.1.0",
        "features": [
            "tools",
            "resources",
            "prompts",
        ],
        "status": "running",
        "timestamp": datetime.now(UTC).isoformat(),
    }
    return json.dumps(info, indent=2)


@mcp.resource(
    uri="data://examples/{category}",
    name="Example Data",
    description="Get example data for a specific category",
)
def get_example_data(category: str) -> str:
    """
    Return example data for the specified category.

    Available categories:
    - users: Sample user records
    - products: Sample product catalog
    - tasks: Sample task list

    Args:
        category: The data category to retrieve
    """
    examples: dict[str, list[dict[str, Any]]] = {
        "users": [
            {"id": 1, "name": "Alice Johnson", "email": "alice@example.com", "role": "admin"},
            {"id": 2, "name": "Bob Smith", "email": "bob@example.com", "role": "user"},
            {"id": 3, "name": "Carol White", "email": "carol@example.com", "role": "user"},
        ],
        "products": [
            {"id": 101, "name": "Widget A", "price": 29.99, "stock": 150},
            {"id": 102, "name": "Gadget B", "price": 49.99, "stock": 75},
            {"id": 103, "name": "Tool C", "price": 19.99, "stock": 200},
        ],
        "tasks": [
            {"id": 1, "title": "Review PR", "status": "pending", "priority": "high"},
            {"id": 2, "title": "Update docs", "status": "in_progress", "priority": "medium"},
            {"id": 3, "title": "Fix bug #42", "status": "completed", "priority": "high"},
        ],
    }

    if category not in examples:
        available = ", ".join(examples.keys())
        return json.dumps(
            {
                "error": f"Unknown category: {category}",
                "available_categories": list(examples.keys()),
                "hint": f"Try one of: {available}",
            },
            indent=2,
        )

    return json.dumps(
        {
            "category": category,
            "count": len(examples[category]),
            "data": examples[category],
        },
        indent=2,
    )


@mcp.resource(
    uri="docs://readme",
    name="Project README",
    description="Get the project README and documentation",
)
def get_readme() -> str:
    """
    Return the project documentation.

    Provides an overview of the FastMCP template server,
    its features, and usage instructions.
    """
    readme = """
# FastMCP 3.0 Template Server

A production-ready MCP server template optimized for claude-code integration.

## Features

### Tools
- `add` - Add two numbers
- `get_current_time` - Get current timestamp
- `parse_json` - Parse and validate JSON
- `search_items` - Search through data
- `summarize_text` - Generate text summaries

### Resources
- `config://server/info` - Server configuration
- `data://examples/{category}` - Example data (users, products, tasks)
- `docs://readme` - This documentation

### Prompts
- `code_review` - Generate code review feedback
- `explain_code` - Explain code functionality
- `generate_tests` - Generate test cases
- `debug_error` - Help debug errors and exceptions
- `refactor_code` - Suggest refactoring improvements

## Usage

```bash
# Run the server
fastmcp run mcp_server/server.py

# Or with development mode
fastmcp dev mcp_server/server.py
```

## Configuration

Configure via environment variables or `.env` file:
- `LOG_LEVEL` - Logging verbosity (DEBUG, INFO, WARNING, ERROR)
- `OTEL_ENABLED` - Enable OpenTelemetry tracing

## Claude-Code Integration

Add to your `.mcp.json`:
```json
{
  "mcpServers": {
    "template": {
      "command": "fastmcp",
      "args": ["run", "mcp_server/server.py"]
    }
  }
}
```
"""
    return readme.strip()


@mcp.resource(
    uri="schema://tool/{tool_name}",
    name="Tool Schema",
    description="Get the JSON schema for a specific tool",
)
def get_tool_schema(tool_name: str) -> str:
    """
    Return the JSON schema for a specified tool.

    Useful for understanding tool parameters and return types.

    Args:
        tool_name: Name of the tool to get schema for
    """
    schemas: dict[str, dict[str, Any]] = {
        "add": {
            "name": "add",
            "description": "Add two numbers together",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
            "returns": {"type": "number"},
        },
        "get_current_time": {
            "name": "get_current_time",
            "description": "Get current date and time in UTC ISO format",
            "parameters": {"type": "object", "properties": {}},
            "returns": {"type": "string", "format": "date-time"},
        },
        "parse_json": {
            "name": "parse_json",
            "description": "Parse and validate JSON data",
            "parameters": {
                "type": "object",
                "properties": {
                    "json_string": {"type": "string", "description": "JSON string to parse"},
                },
                "required": ["json_string"],
            },
            "returns": {"type": "any"},
        },
        "search_items": {
            "name": "search_items",
            "description": "Search and filter a list of items",
            "parameters": {
                "type": "object",
                "properties": {
                    "items": {"type": "array", "description": "List of items to search"},
                    "query": {"type": "string", "description": "Search query string"},
                    "field": {
                        "type": "string",
                        "description": "Field name to search in",
                        "default": "name",
                    },
                    "case_sensitive": {
                        "type": "boolean",
                        "description": "Case-sensitive search",
                        "default": False,
                    },
                },
                "required": ["items", "query"],
            },
            "returns": {"type": "array"},
        },
        "summarize_text": {
            "name": "summarize_text",
            "description": "Generate statistics and a brief summary of text content",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text content to summarize"},
                    "max_sentences": {
                        "type": "integer",
                        "description": "Maximum sentences in summary",
                        "default": 3,
                    },
                },
                "required": ["text"],
            },
            "returns": {"type": "object"},
        },
    }

    if tool_name not in schemas:
        return json.dumps(
            {
                "error": f"Unknown tool: {tool_name}",
                "available_tools": list(schemas.keys()),
            },
            indent=2,
        )

    return json.dumps(schemas[tool_name], indent=2)


# =============================================================================
# PROMPTS - Reusable templates for LLM interactions
# =============================================================================


@mcp.prompt(
    name="code_review",
    description="Generate a thorough code review with actionable feedback",
)
def code_review_prompt(
    code: str,
    language: str = "python",
    focus_areas: str = "all",
) -> str:
    """
    Generate a code review prompt.

    Args:
        code: The code to review
        language: Programming language of the code
        focus_areas: Areas to focus on (security, performance, style, all)
    """
    return f"""Please review the following {language} code and provide detailed feedback.

## Code to Review
```{language}
{code}
```

## Review Focus
Focus areas: {focus_areas}

## Review Guidelines
Please provide feedback on:

1. **Correctness**: Are there any bugs or logical errors?
2. **Security**: Are there any security vulnerabilities?
3. **Performance**: Are there any performance issues or optimizations?
4. **Readability**: Is the code clear and well-documented?
5. **Best Practices**: Does the code follow {language} best practices?

## Expected Output Format
For each issue found, please provide:
- **Location**: Line number or code section
- **Severity**: Critical / Major / Minor / Suggestion
- **Issue**: Description of the problem
- **Recommendation**: How to fix or improve

End with a summary of the overall code quality and key recommendations."""


@mcp.prompt(
    name="explain_code",
    description="Explain code functionality in detail",
)
def explain_code_prompt(
    code: str,
    language: str = "python",
    detail_level: str = "intermediate",
) -> str:
    """
    Generate a code explanation prompt.

    Args:
        code: The code to explain
        language: Programming language of the code
        detail_level: Level of detail (beginner, intermediate, advanced)
    """
    detail_instructions = {
        "beginner": "Use simple terms and explain every concept. Assume no prior programming knowledge.",
        "intermediate": "Explain the logic and patterns used. Assume basic programming knowledge.",
        "advanced": "Focus on design decisions, trade-offs, and edge cases. Assume expert knowledge.",
    }

    instruction = detail_instructions.get(detail_level, detail_instructions["intermediate"])

    return f"""Please explain the following {language} code.

## Code to Explain
```{language}
{code}
```

## Explanation Level
{detail_level.capitalize()}: {instruction}

## Please Include
1. **Overview**: What does this code do at a high level?
2. **Step-by-Step**: Walk through the code execution flow
3. **Key Concepts**: Explain any important patterns or techniques used
4. **Dependencies**: What does this code depend on?
5. **Usage**: How would someone use this code?

If there are any potential issues or improvements, mention them at the end."""


@mcp.prompt(
    name="generate_tests",
    description="Generate comprehensive test cases for code",
)
def generate_tests_prompt(
    code: str,
    language: str = "python",
    test_framework: str = "pytest",
    coverage_goal: str = "comprehensive",
) -> str:
    """
    Generate a test generation prompt.

    Args:
        code: The code to generate tests for
        language: Programming language of the code
        test_framework: Testing framework to use
        coverage_goal: Testing coverage goal (basic, comprehensive, exhaustive)
    """
    coverage_instructions = {
        "basic": "Cover the main happy path and one error case",
        "comprehensive": "Cover happy paths, edge cases, and error handling",
        "exhaustive": "Cover all code paths, boundary conditions, and integration scenarios",
    }

    instruction = coverage_instructions.get(coverage_goal, coverage_instructions["comprehensive"])

    return f"""Please generate test cases for the following {language} code using {test_framework}.

## Code to Test
```{language}
{code}
```

## Coverage Goal
{coverage_goal.capitalize()}: {instruction}

## Test Requirements
1. **Test Structure**: Use {test_framework} conventions and best practices
2. **Naming**: Use descriptive test names that explain what is being tested
3. **Assertions**: Use appropriate assertions with clear failure messages
4. **Fixtures**: Create necessary fixtures or setup/teardown methods
5. **Mocking**: Mock external dependencies where appropriate

## Test Categories to Include
- **Unit Tests**: Test individual functions/methods in isolation
- **Edge Cases**: Test boundary conditions and unusual inputs
- **Error Handling**: Test that errors are handled correctly
- **Integration**: Test interactions between components (if applicable)

## Output Format
Provide complete, runnable test code with comments explaining each test case."""


@mcp.prompt(
    name="debug_error",
    description="Help debug an error or exception",
)
def debug_error_prompt(
    error_message: str,
    code_context: str = "",
    stack_trace: str = "",
) -> str:
    """
    Generate a debugging prompt.

    Args:
        error_message: The error message or exception
        code_context: Relevant code that caused the error
        stack_trace: Full stack trace if available
    """
    context_section = ""
    if code_context:
        context_section = f"""
## Relevant Code
```
{code_context}
```
"""

    trace_section = ""
    if stack_trace:
        trace_section = f"""
## Stack Trace
```
{stack_trace}
```
"""

    return f"""Please help debug the following error.

## Error Message
```
{error_message}
```
{context_section}{trace_section}
## Analysis Request
Please provide:

1. **Error Explanation**: What does this error mean?
2. **Root Cause**: What is likely causing this error?
3. **Solution**: How can this error be fixed?
4. **Prevention**: How can similar errors be prevented in the future?

If you need more information to diagnose the issue, please specify what additional context would be helpful."""


@mcp.prompt(
    name="refactor_code",
    description="Suggest refactoring improvements for code",
)
def refactor_code_prompt(
    code: str,
    language: str = "python",
    goals: str = "readability,maintainability",
) -> str:
    """
    Generate a refactoring prompt.

    Args:
        code: The code to refactor
        language: Programming language of the code
        goals: Comma-separated refactoring goals
    """
    goal_list = [g.strip() for g in goals.split(",")]
    goal_bullets = "\n".join(f"- {g.capitalize()}" for g in goal_list)

    return f"""Please suggest refactoring improvements for the following {language} code.

## Code to Refactor
```{language}
{code}
```

## Refactoring Goals
{goal_bullets}

## Guidelines
1. **Preserve Functionality**: The refactored code must produce the same results
2. **Incremental Changes**: Break down refactoring into small, safe steps
3. **Explain Trade-offs**: Discuss pros and cons of suggested changes
4. **Modern Practices**: Use current {language} idioms and best practices

## Output Format
For each refactoring suggestion:
1. **Change**: What to change
2. **Reason**: Why this improves the code
3. **Before/After**: Show the code transformation
4. **Risk**: Any risks or considerations

End with the complete refactored code."""


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================


def main() -> None:
    """Run the MCP server."""
    logger.info("Starting FastMCP server...")
    mcp.run()


if __name__ == "__main__":
    main()
