from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from .exceptions import FileHandleError
from .models import AppendFileRequest, WriteFileRequest
from .service import FileService

mcp = FastMCP("file-server")
_service = FileService()


def _error(msg: str) -> str:
    return json.dumps({"error": msg})


def _ok(data: dict | list | str) -> str:
    if isinstance(data, str):
        return json.dumps({"content": data})
    return json.dumps(data, default=str)


@mcp.tool()
def read_file(path: str, encoding: str = "utf-8") -> str:
    """Read the full text content of a file.

    Args:
        path: Absolute or relative path to the file.
        encoding: File encoding. Defaults to 'utf-8'. Supported: utf-8, utf-16, ascii, latin-1, utf-8-sig.
    """
    try:
        content = _service.read_file(path, encoding)
        return _ok(content)
    except FileHandleError as exc:
        return _error(str(exc))


@mcp.tool()
def write_file(
    path: str,
    content: str,
    encoding: str = "utf-8",
    overwrite: bool = True,
) -> str:
    """Write text content to a file, creating it if it does not exist.

    Args:
        path: Absolute or relative path to the file.
        content: Text content to write.
        encoding: File encoding. Defaults to 'utf-8'.
        overwrite: If False, raises an error when the file already exists. Defaults to True.
    """
    try:
        _service.write_file(WriteFileRequest(path=path, content=content, encoding=encoding, overwrite=overwrite))
        return _ok({"written": path})
    except FileHandleError as exc:
        return _error(str(exc))


@mcp.tool()
def append_to_file(path: str, content: str, encoding: str = "utf-8") -> str:
    """Append text content to an existing file.

    Args:
        path: Absolute or relative path to the file.
        content: Text to append.
        encoding: File encoding. Defaults to 'utf-8'.
    """
    try:
        _service.append_to_file(AppendFileRequest(path=path, content=content, encoding=encoding))
        return _ok({"appended_to": path})
    except FileHandleError as exc:
        return _error(str(exc))


@mcp.tool()
def delete_file(path: str) -> str:
    """Delete a file or an entire directory tree.

    Args:
        path: Absolute or relative path to the file or directory to delete.
    """
    try:
        _service.delete_file(path)
        return _ok({"deleted": path})
    except FileHandleError as exc:
        return _error(str(exc))


@mcp.tool()
def list_directory(path: str, pattern: str | None = None) -> str:
    """List files and directories inside a directory.

    Args:
        path: Absolute or relative path to the directory.
        pattern: Optional glob pattern to filter entries, e.g. '*.py' or '**/*.txt'.
    """
    try:
        entries = _service.list_directory(path, pattern)
        return _ok([e.to_dict() for e in entries])
    except FileHandleError as exc:
        return _error(str(exc))


@mcp.tool()
def move_file(src: str, dst: str) -> str:
    """Move or rename a file or directory.

    Args:
        src: Source path of the file or directory.
        dst: Destination path (new location or new name).
    """
    try:
        _service.move_file(src, dst)
        return _ok({"moved": {"from": src, "to": dst}})
    except FileHandleError as exc:
        return _error(str(exc))


@mcp.tool()
def copy_file(src: str, dst: str, overwrite: bool = False) -> str:
    """Copy a file or directory to a new location.

    Args:
        src: Source path of the file or directory.
        dst: Destination path.
        overwrite: If True, overwrites the destination if it already exists. Defaults to False.
    """
    try:
        _service.copy_file(src, dst, overwrite)
        return _ok({"copied": {"from": src, "to": dst}})
    except FileHandleError as exc:
        return _error(str(exc))


@mcp.tool()
def get_file_info(path: str) -> str:
    """Retrieve metadata for a file or directory (size, timestamps, type, extension).

    Args:
        path: Absolute or relative path to the file or directory.
    """
    try:
        info = _service.get_file_info(path)
        return _ok(info.to_dict())
    except FileHandleError as exc:
        return _error(str(exc))


@mcp.tool()
def search_in_file(path: str, query: str, case_sensitive: bool = True) -> str:
    """Search for a text substring inside a file and return all matching lines.

    Args:
        path: Absolute or relative path to the file.
        query: Text substring to search for.
        case_sensitive: If False, performs a case-insensitive search. Defaults to True.
    """
    try:
        results = _service.search_in_file(path, query, case_sensitive)
        return _ok([r.to_dict() for r in results])
    except FileHandleError as exc:
        return _error(str(exc))


@mcp.tool()
def create_directory(path: str) -> str:
    """Create a directory and all necessary parent directories.

    Args:
        path: Absolute or relative path to the directory to create.
    """
    try:
        _service.create_directory(path)
        return _ok({"created": path})
    except FileHandleError as exc:
        return _error(str(exc))
