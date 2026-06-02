from __future__ import annotations


class TodoError(ValueError):
    pass


class TodoNotFoundError(TodoError):
    def __init__(self, todo_id: str) -> None:
        super().__init__(f"Todo '{todo_id}' not found")
        self.todo_id = todo_id


class InvalidTodoFieldError(TodoError):
    def __init__(self, field: str, value: str, allowed: list[str]) -> None:
        super().__init__(f"Invalid {field} '{value}'. Allowed: {', '.join(allowed)}")
        self.field = field
        self.value = value
        self.allowed = allowed


class EmptyTitleError(TodoError):
    def __init__(self) -> None:
        super().__init__("Todo title cannot be empty")
