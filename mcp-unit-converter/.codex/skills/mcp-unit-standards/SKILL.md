---
name: mcp-unit-standards
description: Repository-specific standards for the mcp-unit-converter project. Use when editing the MCP server, conversion helpers, or tests so changes stay consistent with the package layout, pure-function helpers, pytest tests, and stable JSON tool outputs.
---

# MCP Unit Standards

## Scope
Use these standards when changing code under `src/mcp_unit_converter/` or `tests/`.

## Required Conventions

- Keep conversion logic in `conversions.py` pure and side-effect free.
- Keep MCP tool wrappers in `server.py` thin; return JSON strings with stable keys.
- Use `pytest`-style test files in `tests/test_*.py`.
- Prefer 4-space indentation and standard Python naming.
- Preserve existing output key names unless a breaking change is intended.

## Implementation Notes

- Add or update round-trip tests when introducing inverse conversions.
- Use `python -m pytest` to verify behavior after changes.
- Keep new code aligned with the current `src/` layout and `python -m mcp_unit_converter` entry point.
