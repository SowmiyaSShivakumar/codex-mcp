from __future__ import annotations

import shutil
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path

from .exceptions import (
    DirectoryDoesNotExistError,
    FileAccessError,
    FileAlreadyExistsError,
    FileDoesNotExistError,
)
from .models import DirectoryEntry, FileInfo, SearchResult


class FileRepository(ABC):
    @abstractmethod
    def read(self, path: str, encoding: str) -> str: ...

    @abstractmethod
    def write(self, path: str, content: str, encoding: str, overwrite: bool) -> None: ...

    @abstractmethod
    def append(self, path: str, content: str, encoding: str) -> None: ...

    @abstractmethod
    def delete(self, path: str) -> None: ...

    @abstractmethod
    def list_dir(self, path: str, pattern: str | None) -> list[DirectoryEntry]: ...

    @abstractmethod
    def move(self, src: str, dst: str) -> None: ...

    @abstractmethod
    def copy(self, src: str, dst: str, overwrite: bool) -> None: ...

    @abstractmethod
    def stat(self, path: str) -> FileInfo: ...

    @abstractmethod
    def create_dir(self, path: str) -> None: ...

    @abstractmethod
    def search(self, path: str, query: str, case_sensitive: bool) -> list[SearchResult]: ...


class LocalFileRepository(FileRepository):
    def read(self, path: str, encoding: str) -> str:
        p = Path(path)
        if not p.exists():
            raise FileDoesNotExistError(path)
        try:
            return p.read_text(encoding=encoding)
        except PermissionError:
            raise FileAccessError(path)

    def write(self, path: str, content: str, encoding: str, overwrite: bool) -> None:
        p = Path(path)
        if p.exists() and not overwrite:
            raise FileAlreadyExistsError(path)
        parent = p.parent
        if not parent.exists():
            raise DirectoryDoesNotExistError(str(parent))
        try:
            p.write_text(content, encoding=encoding)
        except PermissionError:
            raise FileAccessError(path)

    def append(self, path: str, content: str, encoding: str) -> None:
        p = Path(path)
        if not p.exists():
            raise FileDoesNotExistError(path)
        try:
            with p.open("a", encoding=encoding) as f:
                f.write(content)
        except PermissionError:
            raise FileAccessError(path)

    def delete(self, path: str) -> None:
        p = Path(path)
        if not p.exists():
            raise FileDoesNotExistError(path)
        try:
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
        except PermissionError:
            raise FileAccessError(path)

    def list_dir(self, path: str, pattern: str | None) -> list[DirectoryEntry]:
        p = Path(path)
        if not p.exists():
            raise FileDoesNotExistError(path)
        if not p.is_dir():
            raise DirectoryDoesNotExistError(path)
        try:
            entries = list(p.glob(pattern) if pattern else p.iterdir())
        except PermissionError:
            raise FileAccessError(path)
        return sorted(
            [
                DirectoryEntry(
                    name=e.name,
                    path=str(e),
                    is_file=e.is_file(),
                    is_dir=e.is_dir(),
                    size=e.stat().st_size if e.is_file() else 0,
                )
                for e in entries
            ],
            key=lambda e: (not e.is_dir, e.name.lower()),
        )

    def move(self, src: str, dst: str) -> None:
        s = Path(src)
        if not s.exists():
            raise FileDoesNotExistError(src)
        try:
            shutil.move(str(s), dst)
        except PermissionError:
            raise FileAccessError(src)

    def copy(self, src: str, dst: str, overwrite: bool) -> None:
        s = Path(src)
        d = Path(dst)
        if not s.exists():
            raise FileDoesNotExistError(src)
        if d.exists() and not overwrite:
            raise FileAlreadyExistsError(dst)
        try:
            if s.is_dir():
                shutil.copytree(str(s), str(d), dirs_exist_ok=overwrite)
            else:
                shutil.copy2(str(s), str(d))
        except PermissionError:
            raise FileAccessError(src)

    def stat(self, path: str) -> FileInfo:
        p = Path(path)
        if not p.exists():
            raise FileDoesNotExistError(path)
        try:
            st = p.stat()
        except PermissionError:
            raise FileAccessError(path)
        return FileInfo(
            path=str(p.resolve()),
            name=p.name,
            size=st.st_size,
            is_file=p.is_file(),
            is_dir=p.is_dir(),
            modified_at=datetime.fromtimestamp(st.st_mtime, tz=timezone.utc),
            created_at=datetime.fromtimestamp(st.st_ctime, tz=timezone.utc),
            extension=p.suffix,
        )

    def create_dir(self, path: str) -> None:
        p = Path(path)
        if p.exists():
            raise FileAlreadyExistsError(path)
        try:
            p.mkdir(parents=True, exist_ok=False)
        except PermissionError:
            raise FileAccessError(path)

    def search(self, path: str, query: str, case_sensitive: bool) -> list[SearchResult]:
        p = Path(path)
        if not p.exists():
            raise FileDoesNotExistError(path)
        if not p.is_file():
            raise FileDoesNotExistError(path)
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except PermissionError:
            raise FileAccessError(path)

        compare_query = query if case_sensitive else query.lower()
        results = []
        for i, line in enumerate(text.splitlines(), 1):
            compare_line = line if case_sensitive else line.lower()
            if compare_query in compare_line:
                results.append(SearchResult(line_number=i, line=line.rstrip(), match=query))
        return results
