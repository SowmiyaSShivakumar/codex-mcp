# Repository Guidelines

## Project Structure & Module Organization
This is a small Python MCP server with a `src` layout.

- `src/math_server/`: runtime package code
- `src/math_server/server.py`: MCP tool registration and server wiring
- `src/math_server/operations.py`: arithmetic helpers used by the tools
- `src/math_server/__main__.py`: CLI entry point for `python -m math_server`
- `tests/`: unit tests, currently centered on `tests/test_operations.py`
- `mcp_config.json`: local MCP launch configuration

## Build, Test, and Development Commands
Use Python 3.11 or newer.

- `python -m pip install -e .[dev]`: install the package in editable mode with test dependencies
- `python -m pytest`: run the test suite under `tests/`
- `python -m math_server`: start the MCP server locally

## Coding Style & Naming Conventions
Follow standard Python style: 4-space indentation, `snake_case` for functions and modules, and `PascalCase` for classes and test cases. Keep arithmetic helpers small and pure, with explicit type hints on public functions when practical. No formatter or linter is configured, so match the surrounding style.

## Testing Guidelines
Tests use `pytest`, but the current tests are written with `unittest` in `tests/test_operations.py`. Name new tests `test_*.py` and prefer focused cases for each arithmetic operation, including edge cases such as division by zero. Use fixed inputs and deterministic assertions.

## Commit & Pull Request Guidelines
The repository history does not establish a strict commit convention, so use short, imperative messages such as `Add divide error test`. Pull requests should include a brief summary, the commands run to validate the change, and any behavior changes to the MCP tool responses.

## Security & Configuration Tips
Keep filesystem and config edits narrow. Avoid broad changes to `mcp_config.json` unless you are updating the local runtime setup, and prefer isolated test data over environment-dependent behavior.
