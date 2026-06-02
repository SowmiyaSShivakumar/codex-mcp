from __future__ import annotations

import unittest
from datetime import datetime, timezone

from src.mcp_todo.exceptions import EmptyTitleError, InvalidTodoFieldError, TodoNotFoundError
from src.mcp_todo.models import CreateTodoRequest, Priority, Status, UpdateTodoRequest
from src.mcp_todo.repository import InMemoryTodoRepository
from src.mcp_todo.service import TodoService

_FIXED_NOW = datetime(2026, 6, 1, 12, 0, 0, tzinfo=timezone.utc)


def _make_service() -> TodoService:
    return TodoService(
        todos=InMemoryTodoRepository(),
        clock=lambda: _FIXED_NOW,
    )


class CreateTodoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = _make_service()

    def test_creates_todo_with_defaults(self) -> None:
        todo = self.service.create(CreateTodoRequest(title="Buy milk"))

        self.assertEqual(todo.title, "Buy milk")
        self.assertEqual(todo.priority, Priority.MEDIUM)
        self.assertEqual(todo.status, Status.PENDING)
        self.assertEqual(todo.created_at, _FIXED_NOW)
        self.assertIsNone(todo.due_date)

    def test_creates_todo_with_all_fields(self) -> None:
        todo = self.service.create(
            CreateTodoRequest(
                title="Write report",
                description="Q2 summary",
                priority="high",
                due_date="2026-12-31T23:59:59",
            )
        )

        self.assertEqual(todo.priority, Priority.HIGH)
        self.assertEqual(todo.description, "Q2 summary")
        self.assertIsNotNone(todo.due_date)

    def test_strips_whitespace_from_title(self) -> None:
        todo = self.service.create(CreateTodoRequest(title="  Buy milk  "))
        self.assertEqual(todo.title, "Buy milk")

    def test_raises_on_empty_title(self) -> None:
        with self.assertRaises(EmptyTitleError):
            self.service.create(CreateTodoRequest(title="   "))

    def test_raises_on_invalid_priority(self) -> None:
        with self.assertRaises(InvalidTodoFieldError) as ctx:
            self.service.create(CreateTodoRequest(title="Task", priority="urgent"))
        self.assertEqual(ctx.exception.field, "priority")

    def test_raises_on_invalid_due_date(self) -> None:
        with self.assertRaises(InvalidTodoFieldError) as ctx:
            self.service.create(CreateTodoRequest(title="Task", due_date="not-a-date"))
        self.assertEqual(ctx.exception.field, "due_date")

    def test_each_todo_gets_unique_id(self) -> None:
        t1 = self.service.create(CreateTodoRequest(title="First"))
        t2 = self.service.create(CreateTodoRequest(title="Second"))
        self.assertNotEqual(t1.id, t2.id)


class GetTodoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = _make_service()

    def test_returns_created_todo(self) -> None:
        created = self.service.create(CreateTodoRequest(title="Task"))
        fetched = self.service.get(created.id)
        self.assertEqual(fetched.id, created.id)

    def test_raises_for_unknown_id(self) -> None:
        with self.assertRaises(TodoNotFoundError) as ctx:
            self.service.get("nonexistent-id")
        self.assertEqual(ctx.exception.todo_id, "nonexistent-id")


class ListTodosTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = _make_service()
        self.service.create(CreateTodoRequest(title="Low task", priority="low"))
        self.service.create(CreateTodoRequest(title="High task", priority="high"))
        self.service.create(CreateTodoRequest(title="Medium task", priority="medium"))

    def test_returns_all_todos(self) -> None:
        self.assertEqual(len(self.service.list_all()), 3)

    def test_filters_by_priority(self) -> None:
        result = self.service.list_all(priority="high")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "High task")

    def test_filters_by_status(self) -> None:
        todos = self.service.list_all()
        self.service.update(UpdateTodoRequest(id=todos[0].id, status="done"))

        pending = self.service.list_all(status="pending")
        done = self.service.list_all(status="done")

        self.assertEqual(len(done), 1)
        self.assertEqual(len(pending), 2)

    def test_raises_on_invalid_status_filter(self) -> None:
        with self.assertRaises(InvalidTodoFieldError):
            self.service.list_all(status="archived")


class UpdateTodoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = _make_service()
        self.todo = self.service.create(CreateTodoRequest(title="Original"))

    def test_updates_title(self) -> None:
        updated = self.service.update(UpdateTodoRequest(id=self.todo.id, title="Updated"))
        self.assertEqual(updated.title, "Updated")

    def test_updates_status(self) -> None:
        updated = self.service.update(UpdateTodoRequest(id=self.todo.id, status="in_progress"))
        self.assertEqual(updated.status, Status.IN_PROGRESS)

    def test_partial_update_preserves_other_fields(self) -> None:
        updated = self.service.update(UpdateTodoRequest(id=self.todo.id, title="New Title"))
        self.assertEqual(updated.status, Status.PENDING)
        self.assertEqual(updated.priority, Priority.MEDIUM)

    def test_raises_on_empty_title_update(self) -> None:
        with self.assertRaises(EmptyTitleError):
            self.service.update(UpdateTodoRequest(id=self.todo.id, title=""))

    def test_raises_on_unknown_todo(self) -> None:
        with self.assertRaises(TodoNotFoundError):
            self.service.update(UpdateTodoRequest(id="ghost-id", title="X"))


class DeleteTodoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = _make_service()
        self.todo = self.service.create(CreateTodoRequest(title="To delete"))

    def test_deletes_todo(self) -> None:
        self.service.delete(self.todo.id)
        with self.assertRaises(TodoNotFoundError):
            self.service.get(self.todo.id)

    def test_raises_on_unknown_todo(self) -> None:
        with self.assertRaises(TodoNotFoundError):
            self.service.delete("ghost-id")


if __name__ == "__main__":
    unittest.main()
