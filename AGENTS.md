# Repository Guidelines

## Project Structure & Module Organization
This repository is a small Python package for an MCP todo server.

- `src/mcp_todo/`: application code
  - `server.py`: MCP server wiring and tool registration
  - `service.py`: todo business logic
  - `repository.py`: storage abstraction and in-memory implementation
  - `models.py`: request/response and domain types
  - `exceptions.py`: domain-specific errors
  - `__main__.py`: CLI entry point for `mcp-todo`
- `tests/`: unit tests, currently focused on service behavior
- `mcp_config.json`: local MCP configuration
- `pyproject.toml`: build metadata and test configuration

## Build, Test, and Development Commands
Use Python 3.11 or newer.

- `python -m pip install -e .[dev]`: install the package in editable mode with test dependencies
- `python -m pytest`: run the test suite in `tests/`
- `mcp-todo`: start the server via the console script entry point
- `python -m mcp_todo`: alternate module-based entry point if needed

## Coding Style & Naming Conventions
Follow standard Python conventions:

- 4-space indentation
- snake_case for functions, variables, modules, and test methods
- PascalCase for classes and dataclasses
- keep public exceptions and request models descriptive and domain-specific

The codebase does not currently enforce a formatter or linter, so keep changes consistent with the existing style in `src/mcp_todo/` and `tests/`.

## Testing Guidelines
Tests use `pytest`, but the current suite is written with `unittest` in `tests/test_service.py`.

- Name tests `test_*`
- Prefer focused unit tests for service and repository behavior
- Use deterministic fixtures where possible, such as fixed datetimes
- Run `python -m pytest` before submitting changes

## Commit & Pull Request Guidelines
The Git history currently contains only the initial commit, so no commit convention is established yet. Use clear, imperative commit messages such as `Add todo validation tests`.

Pull requests should include:

- a short summary of behavior changes
- related issue links, if applicable
- test results or notes about validation
- screenshots only if a change affects a UI or rendered output

## Agent-Specific Notes
Prefer small, targeted edits. Keep the MCP server contract stable unless the task explicitly requires a protocol or API change.
