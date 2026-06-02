from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class FileInfo:
    path: str
    name: str
    size: int
    is_file: bool
    is_dir: bool
    modified_at: datetime
    created_at: datetime | None
    extension: str

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "name": self.name,
            "size": self.size,
            "is_file": self.is_file,
            "is_dir": self.is_dir,
            "modified_at": self.modified_at.isoformat(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "extension": self.extension,
        }


@dataclass(slots=True)
class DirectoryEntry:
    name: str
    path: str
    is_file: bool
    is_dir: bool
    size: int

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.path,
            "is_file": self.is_file,
            "is_dir": self.is_dir,
            "size": self.size,
        }


@dataclass(slots=True)
class SearchResult:
    line_number: int
    line: str
    match: str

    def to_dict(self) -> dict:
        return {
            "line_number": self.line_number,
            "line": self.line,
            "match": self.match,
        }


@dataclass(slots=True)
class WriteFileRequest:
    path: str
    content: str
    encoding: str = "utf-8"
    overwrite: bool = True


@dataclass(slots=True)
class AppendFileRequest:
    path: str
    content: str
    encoding: str = "utf-8"
