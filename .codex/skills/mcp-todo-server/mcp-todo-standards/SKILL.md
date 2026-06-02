---
name: mcp-todo-standards
description: Repository-specific guidance for working in the mcp-todo-server codebase. Use when editing, extending, testing, or reviewing this Python MCP todo server.
---

# MCP Todo Standards

## Scope
Use this skill for changes in this repository. Follow the existing package layout and keep edits small and targeted.

## Code Layout
- Application code lives in `src/mcp_todo/`.
- Tests live in `tests/` and currently use `unittest` with `pytest` as the runner.
- Keep MCP wiring in `server.py`, business rules in `service.py`, persistence in `repository.py`, and data models in `models.py`.

## Implementation Rules
- Prefer standard Python 3.11 style: 4-space indentation, `snake_case` for functions and modules, `PascalCase` for classes.
- Preserve current domain behavior unless the task explicitly changes it.
- Validate user input in the service layer and raise the existing domain exceptions instead of introducing new error types.
- Keep the in-memory repository behavior deterministic and easy to test.

## Testing Rules
- Add or update focused tests in `tests/test_service.py` or a new `tests/test_*.py` file.
- Use fixed datetimes or injected clocks for time-sensitive behavior.
- Cover success paths and expected validation failures.
- Run `python -m pytest` before finishing any change.

## Working Style
- Prefer small refactors over broad rewrites.
- Reuse existing models, exceptions, and repository interfaces when possible.
- Keep the CLI entry point (`mcp-todo`) and MCP server contract stable unless the task requires a breaking change.
