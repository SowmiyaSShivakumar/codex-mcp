from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable

from .exceptions import EmptyTitleError, InvalidTodoFieldError, TodoNotFoundError
from .models import CreateTodoRequest, Priority, Status, Todo, UpdateTodoRequest
from .repository import InMemoryTodoRepository, TodoRepository, new_todo


class TodoService:
    def __init__(
        self,
        todos: TodoRepository | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._todos = todos or InMemoryTodoRepository()
        self._clock = clock

    def create(self, request: CreateTodoRequest) -> Todo:
        if not request.title.strip():
            raise EmptyTitleError()

        priority = self._parse_priority(request.priority)
        due_date = self._parse_date(request.due_date) if request.due_date else None

        todo = new_todo(
            title=request.title.strip(),
            description=request.description.strip(),
            priority=priority,
            due_date=due_date,
            clock=self._clock,
        )
        return self._todos.add(todo)

    def get(self, todo_id: str) -> Todo:
        return self._todos.get(todo_id)

    def list_all(self, status: str | None = None, priority: str | None = None) -> list[Todo]:
        parsed_status = self._parse_status(status) if status else None
        parsed_priority = self._parse_priority(priority) if priority else None
        return self._todos.list_all(status=parsed_status, priority=parsed_priority)

    def update(self, request: UpdateTodoRequest) -> Todo:
        todo = self._todos.get(request.id)

        title = todo.title
        description = todo.description
        priority = todo.priority
        status = todo.status
        due_date = todo.due_date

        if request.title is not None:
            if not request.title.strip():
                raise EmptyTitleError()
            title = request.title.strip()

        if request.description is not None:
            description = request.description.strip()

        if request.priority is not None:
            priority = self._parse_priority(request.priority)

        if request.status is not None:
            status = self._parse_status(request.status)

        if request.due_date is not None:
            due_date = self._parse_date(request.due_date)

        updated = Todo(
            id=todo.id,
            title=title,
            description=description,
            priority=priority,
            status=status,
            created_at=todo.created_at,
            updated_at=Todo.now(self._clock),
            due_date=due_date,
        )
        return self._todos.update(updated)

    def delete(self, todo_id: str) -> None:
        self._todos.delete(todo_id)

    def _parse_priority(self, value: str) -> Priority:
        allowed = [p.value for p in Priority]
        try:
            return Priority(value.lower())
        except ValueError:
            raise InvalidTodoFieldError("priority", value, allowed)

    def _parse_status(self, value: str) -> Status:
        allowed = [s.value for s in Status]
        try:
            return Status(value.lower())
        except ValueError:
            raise InvalidTodoFieldError("status", value, allowed)

    def _parse_date(self, value: str) -> datetime:
        try:
            dt = datetime.fromisoformat(value)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            raise InvalidTodoFieldError("due_date", value, ["ISO 8601 format, e.g. 2026-12-31T23:59:59"])
