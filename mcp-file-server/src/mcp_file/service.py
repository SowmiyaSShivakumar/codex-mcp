from __future__ import annotations

from .exceptions import FileHandleError, InvalidPathError
from .models import (
    AppendFileRequest,
    DirectoryEntry,
    FileInfo,
    SearchResult,
    WriteFileRequest,
)
from .repository import FileRepository, LocalFileRepository

_SUPPORTED_ENCODINGS = {"utf-8", "utf-16", "ascii", "latin-1", "utf-8-sig"}


class FileService:
    def __init__(self, repo: FileRepository | None = None) -> None:
        self._repo = repo or LocalFileRepository()

    def read_file(self, path: str, encoding: str = "utf-8") -> str:
        self._validate_path(path)
        self._validate_encoding(encoding)
        return self._repo.read(path, encoding)

    def write_file(self, request: WriteFileRequest) -> None:
        self._validate_path(request.path)
        self._validate_encoding(request.encoding)
        self._repo.write(request.path, request.content, request.encoding, request.overwrite)

    def append_to_file(self, request: AppendFileRequest) -> None:
        self._validate_path(request.path)
        self._validate_encoding(request.encoding)
        self._repo.append(request.path, request.content, request.encoding)

    def delete_file(self, path: str) -> None:
        self._validate_path(path)
        self._repo.delete(path)

    def list_directory(self, path: str, pattern: str | None = None) -> list[DirectoryEntry]:
        self._validate_path(path)
        return self._repo.list_dir(path, pattern)

    def move_file(self, src: str, dst: str) -> None:
        self._validate_path(src)
        self._validate_path(dst)
        self._repo.move(src, dst)

    def copy_file(self, src: str, dst: str, overwrite: bool = False) -> None:
        self._validate_path(src)
        self._validate_path(dst)
        self._repo.copy(src, dst, overwrite)

    def get_file_info(self, path: str) -> FileInfo:
        self._validate_path(path)
        return self._repo.stat(path)

    def search_in_file(self, path: str, query: str, case_sensitive: bool = True) -> list[SearchResult]:
        self._validate_path(path)
        if not query:
            raise InvalidPathError(path, "search query cannot be empty")
        return self._repo.search(path, query, case_sensitive)

    def create_directory(self, path: str) -> None:
        self._validate_path(path)
        self._repo.create_dir(path)

    def _validate_path(self, path: str) -> None:
        if not path or not path.strip():
            raise InvalidPathError(path or "", "path cannot be empty")

    def _validate_encoding(self, encoding: str) -> None:
        if encoding.lower() not in _SUPPORTED_ENCODINGS:
            raise FileHandleError(
                f"Unsupported encoding '{encoding}'. Supported: {', '.join(sorted(_SUPPORTED_ENCODINGS))}"
            )
