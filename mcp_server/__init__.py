"""
FastMCP Template Server

An MCP server template optimized for claude-code integration.

Features:
- Tools with proper decorators and validation
- Resources with templated URIs
- Prompts for LLM interaction
"""

from .server import main, mcp

__all__ = ["mcp", "main"]
__version__ = "0.1.0"
