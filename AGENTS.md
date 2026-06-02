# AGENTS.md

> Auto-generated — do not edit manually.
> Source of truth: each `mcp-*/AGENTS.md`.

---

## mcp-file-server

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

---

## mcp-todo-server

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

## Versioning
This server follows semantic versioning. Bump the patch version in `pyproject.toml` for bug fixes, minor for new tools, major for breaking protocol changes.


# Add a blank line to mcp-todo-server/AGENTS.md

---

## mcp-unit-converter

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

---

