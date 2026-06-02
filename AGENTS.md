# Repository Guidelines

## Project Structure & Module Organization
This is a small Python package built with `hatchling` and a `src` layout.

- `src/mcp_file/`: core package code.
- `src/mcp_file/server.py`: MCP tool registrations and JSON response helpers.
- `src/mcp_file/service.py`: validation and business logic.
- `src/mcp_file/repository.py`: filesystem access implementation.
- `src/mcp_file/models.py` and `exceptions.py`: shared data structures and error types.
- `tests/`: unit tests, currently centered on `tests/test_service.py`.
- `mcp_config.json`: local MCP configuration used by the server runtime.

## Build, Test, and Development Commands
Use Python 3.11 or newer.

- `python -m pip install -e .[dev]`: install the package in editable mode with test dependencies.
- `python -m pytest`: run the unit test suite under `tests/`.
- `python -m mcp_file`: start the MCP server through the package entrypoint.
- `python -m build`: create distribution artifacts if `build` is installed locally.

## Coding Style & Naming Conventions
Follow standard Python style: 4-space indentation, `snake_case` for functions and variables, `PascalCase` for classes, and type hints on public methods. Keep modules focused and prefer small, explicit helpers over implicit behavior. There is no formatter or linter configured in this repo, so match the surrounding style and keep changes PEP 8 friendly.

## Testing Guidelines
Tests use `pytest` with `unittest`-style test cases. Place new tests in `tests/` and name files `test_*.py`; keep test methods descriptive, such as `test_raises_on_missing_file`. Prefer temporary directories and isolated filesystem fixtures so tests do not depend on local state. Run `python -m pytest` before opening a PR.

## Commit & Pull Request Guidelines
The Git history currently contains only an initial commit, so no strict project convention is established yet. Use short, imperative commit messages such as `Add directory listing tests`. Pull requests should include a clear summary, the behavior changed, and evidence of validation (`pytest` output or reproduction steps). Include screenshots only if a change affects a UI or rendered output.

## Security & Configuration Tips
This server performs filesystem operations. Treat paths carefully, avoid broad destructive changes in tests, and prefer isolated temp directories when exercising delete/move/copy behavior. Keep `mcp_config.json` aligned with the local runtime setup.
