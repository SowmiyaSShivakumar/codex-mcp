from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from .exceptions import TodoError
from .models import CreateTodoRequest, UpdateTodoRequest
from .service import TodoService

mcp = FastMCP("todo-server")
_service = TodoService()


def _error(msg: str) -> str:
    return json.dumps({"error": msg})


def _ok(data: dict | list) -> str:
    return json.dumps(data, default=str)


@mcp.tool()
def create_todo(
    title: str,
    description: str = "",
    priority: str = "medium",
    due_date: str | None = None,
) -> str:
    """Create a new todo item.

    Args:
        title: Short title for the task (required).
        description: Optional detailed description.
        priority: One of 'low', 'medium', 'high'. Defaults to 'medium'.
        due_date: Optional ISO 8601 due date, e.g. '2026-12-31T23:59:59'.
    """
    try:
        todo = _service.create(
            CreateTodoRequest(
                title=title,
                description=description,
                priority=priority,
                due_date=due_date,
            )
        )
        return _ok(todo.to_dict())
    except TodoError as exc:
        return _error(str(exc))


@mcp.tool()
def get_todo(todo_id: str) -> str:
    """Retrieve a single todo by its ID.

    Args:
        todo_id: The UUID of the todo.
    """
    try:
        return _ok(_service.get(todo_id).to_dict())
    except TodoError as exc:
        return _error(str(exc))


@mcp.tool()
def list_todos(status: str | None = None, priority: str | None = None) -> str:
    """List all todos, optionally filtered.

    Args:
        status: Filter by status — 'pending', 'in_progress', or 'done'.
        priority: Filter by priority — 'low', 'medium', or 'high'.
    """
    try:
        todos = _service.list_all(status=status, priority=priority)
        return _ok([t.to_dict() for t in todos])
    except TodoError as exc:
        return _error(str(exc))


@mcp.tool()
def update_todo(
    todo_id: str,
    title: str | None = None,
    description: str | None = None,
    priority: str | None = None,
    status: str | None = None,
    due_date: str | None = None,
) -> str:
    """Update one or more fields of an existing todo.

    Args:
        todo_id: The UUID of the todo to update.
        title: New title (optional).
        description: New description (optional).
        priority: New priority — 'low', 'medium', or 'high' (optional).
        status: New status — 'pending', 'in_progress', or 'done' (optional).
        due_date: New ISO 8601 due date (optional).
    """
    try:
        todo = _service.update(
            UpdateTodoRequest(
                id=todo_id,
                title=title,
                description=description,
                priority=priority,
                status=status,
                due_date=due_date,
            )
        )
        return _ok(todo.to_dict())
    except TodoError as exc:
        return _error(str(exc))


@mcp.tool()
def delete_todo(todo_id: str) -> str:
    """Permanently delete a todo item.

    Args:
        todo_id: The UUID of the todo to delete.
    """
    try:
        _service.delete(todo_id)
        return _ok({"deleted": todo_id})
    except TodoError as exc:
        return _error(str(exc))


@mcp.tool()
def complete_todo(todo_id: str) -> str:
    """Mark a todo as done.

    Args:
        todo_id: The UUID of the todo to complete.
    """
    try:
        todo = _service.update(UpdateTodoRequest(id=todo_id, status="done"))
        return _ok(todo.to_dict())
    except TodoError as exc:
        return _error(str(exc))
