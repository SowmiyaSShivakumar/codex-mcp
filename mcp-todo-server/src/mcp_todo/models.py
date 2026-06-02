from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Callable


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Status(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class Todo:
    id: str
    title: str
    description: str
    priority: Priority
    status: Status
    created_at: datetime
    updated_at: datetime
    due_date: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "due_date": self.due_date.isoformat() if self.due_date else None,
        }

    @staticmethod
    def now(clock: Callable[[], datetime] | None = None) -> datetime:
        return clock() if clock else _utcnow()


@dataclass(slots=True)
class CreateTodoRequest:
    title: str
    description: str = ""
    priority: str = Priority.MEDIUM.value
    due_date: str | None = None


@dataclass(slots=True)
class UpdateTodoRequest:
    id: str
    title: str | None = None
    description: str | None = None
    priority: str | None = None
    status: str | None = None
    due_date: str | None = None
