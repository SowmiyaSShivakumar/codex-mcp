---
name: math-server
description: Work on the math-server MCP project, including arithmetic helpers, MCP tool wiring, tests, and local server setup. Use when adding or changing add, subtract, multiply, divide behavior, updating server registration, or validating the package with pytest.
---

# Math Server

## Use This Repo Structure
- Keep runtime code in `src/math_server/`.
- Put arithmetic logic in `src/math_server/operations.py`.
- Keep MCP tool registration and response wiring in `src/math_server/server.py`.
- Keep tests in `tests/`, especially `tests/test_operations.py`.

## Make Changes Carefully
- Keep arithmetic helpers pure and small.
- Preserve MCP JSON response keys unless a protocol change is intended.
- Update `mcp_config.json` only when local launch settings need to change.

## Validate
- Install dev dependencies with `python -m pip install -e .[dev]`.
- Run the test suite with `python -m pytest`.
- Start the server locally with `python -m math_server`.
