---
name: mcp-file-standards
description: Define and apply repository standards for file-system behavior in this MCP file server. Use when writing, reviewing, or normalizing code, tests, or prompts that touch file paths, directory operations, naming, or filesystem safety.
---

# MCP File Standards

Use this provided skill to keep file-related changes consistent, safe, and easy to review.

## Path Rules

- Treat paths as explicit inputs. Validate empty or blank values before use.
- Prefer temporary directories in tests, for example `tempfile.TemporaryDirectory()`.
- Keep path handling platform-aware and avoid assumptions about separators or current working directory.

## Operation Rules

- Make file actions idempotent when practical, or fail clearly when a precondition is missing.
- For destructive operations, confirm the target exists and is the intended file or directory tree.
- For copy and move behavior, define overwrite handling explicitly and test both allowed and denied cases.

## Naming And Tests

- Use clear, descriptive names for files, classes, methods, and test cases.
- Keep test files under `tests/` and name them `test_*.py`.
- Prefer one focused assertion group per test method, especially for filesystem edge cases.

## Review Checklist

- Confirm error handling maps to the correct exception type.
- Confirm directory and file behavior are tested separately.
- Confirm changes do not rely on local machine state or hidden files.
