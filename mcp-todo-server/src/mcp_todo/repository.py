from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Callable

from .exceptions import TodoNotFoundError
from .models import Priority, Status, Todo


class TodoRepository(ABC):
    @abstractmethod
    def add(self, todo: Todo) -> Todo: ...

    @abstractmethod
    def get(self, todo_id: str) -> Todo: ...

    @abstractmethod
    def list_all(self, status: Status | None = None, priority: Priority | None = None) -> list[Todo]: ...

    @abstractmethod
    def update(self, todo: Todo) -> Todo: ...

    @abstractmethod
    def delete(self, todo_id: str) -> None: ...


class InMemoryTodoRepository(TodoRepository):
    def __init__(self) -> None:
        self._store: dict[str, Todo] = {}

    def add(self, todo: Todo) -> Todo:
        self._store[todo.id] = todo
        return todo

    def get(self, todo_id: str) -> Todo:
        if todo_id not in self._store:
            raise TodoNotFoundError(todo_id)
        return self._store[todo_id]

    def list_all(self, status: Status | None = None, priority: Priority | None = None) -> list[Todo]:
        todos = list(self._store.values())
        if status:
            todos = [t for t in todos if t.status == status]
        if priority:
            todos = [t for t in todos if t.priority == priority]
        return sorted(todos, key=lambda t: t.created_at)

    def update(self, todo: Todo) -> Todo:
        if todo.id not in self._store:
            raise TodoNotFoundError(todo.id)
        self._store[todo.id] = todo
        return todo

    def delete(self, todo_id: str) -> None:
        if todo_id not in self._store:
            raise TodoNotFoundError(todo_id)
        del self._store[todo_id]


def new_todo(
    title: str,
    description: str = "",
    priority: Priority = Priority.MEDIUM,
    due_date: datetime | None = None,
    clock: Callable[[], datetime] | None = None,
) -> Todo:
    now = Todo.now(clock)
    return Todo(
        id=str(uuid.uuid4()),
        title=title,
        description=description,
        priority=priority,
        status=Status.PENDING,
        created_at=now,
        updated_at=now,
        due_date=due_date,
    )
