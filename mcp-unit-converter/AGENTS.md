# Repository Guidelines

## Project Structure & Module Organization
This repository is a small Python MCP server.

- `src/mcp_unit_converter/` contains the runtime package.
- `src/mcp_unit_converter/server.py` defines the MCP tools.
- `src/mcp_unit_converter/conversions.py` holds pure conversion helpers.
- `src/mcp_unit_converter/__main__.py` is the CLI entry point for `python -m mcp_unit_converter`.
- `tests/` contains unit tests, currently centered on conversion logic.
- `mcp_config.json` shows the local MCP server launch configuration.

## Build, Test, and Development Commands
Use Python 3.11 or newer.

- `python -m pip install -e .[dev]` installs the package in editable mode with test dependencies.
- `python -m pytest` runs the full test suite under `tests/`.
- `python -m mcp_unit_converter` starts the MCP server locally.

The project uses Hatchling as the build backend, but no custom build script is defined.

## Coding Style & Naming Conventions
Follow standard Python conventions:

- Use 4-space indentation.
- Prefer type annotations for public functions.
- Keep conversion helpers pure and side-effect free.
- Name functions with `verb_noun` clarity, such as `meters_to_feet` or `convert_celsius_to_fahrenheit`.
- Use lowercase module names with underscores.

No formatter or linter is configured in `pyproject.toml`, so keep changes consistent with the surrounding code.

## Testing Guidelines
Tests use `pytest` with `unittest`-style test cases.

- Put new tests in `tests/` and name them `test_*.py`.
- Keep helper tests close to the behavior they verify.
- Prefer `assertAlmostEqual` for floating-point conversions.
- Add round-trip tests when a conversion has an inverse.

## Commit & Pull Request Guidelines
This workspace does not include Git history, so no repository-specific commit pattern can be inferred. Use short, imperative commit messages such as `Add mass conversion tests`.

Pull requests should include:

- A brief summary of the change and why it is needed.
- Notes on tests run, especially `python -m pytest`.
- Example inputs/outputs if a tool response changes.

## Agent Notes
When editing the MCP tools, keep JSON response keys stable unless you are intentionally making a breaking change.
