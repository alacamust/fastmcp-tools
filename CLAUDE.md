# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies (creates .venv automatically)
uv venv && uv pip install -e .

# Start the MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_pdf
```

## Architecture

This is a Python MCP (Model Context Protocol) server built with `FastMCP`. It exposes tools to AI assistants over the MCP protocol.

**Entry point:** [main.py](main.py) creates a `FastMCP` instance and registers tools by calling `mcp.tool()(function)` for each function to expose.

**Tool implementations** live in [tools/](tools/) as plain Python functions — no MCP-specific code inside them. This keeps tools independently testable.

**Tests** in [tests/](tests/) test tool implementations directly (not through MCP), using binary fixture files in [tests/fixtures/](tests/fixtures/).

## Defining MCP Tools

Tools are plain Python functions registered with `mcp.tool()()` in [main.py](main.py):

```python
# In main.py
from tools.my_module import my_function
mcp.tool()(my_function)
```

Use `Field` from pydantic for parameter descriptions — these become the tool's parameter schema exposed to the AI:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does"),
) -> ReturnType:
    """One-line summary.

    Detailed explanation of functionality.

    When to use:
    - Appropriate use case
    - Another appropriate use case

    When NOT to use:
    - Inappropriate use case

    Examples:
    >>> my_tool("hello", 42)
    "expected output"
    """
```

Docstring quality matters — the AI assistant reads the docstring to decide when and how to call the tool. Include: one-line summary, detailed explanation, when to use/not use, and examples with expected output.

All function parameters and return types must have explicit type annotations.
