from __future__ import annotations


class FileHandleError(ValueError):
    pass


class FileDoesNotExistError(FileHandleError):
    def __init__(self, path: str) -> None:
        super().__init__(f"File or directory not found: '{path}'")
        self.path = path


class FileAlreadyExistsError(FileHandleError):
    def __init__(self, path: str) -> None:
        super().__init__(f"File already exists: '{path}'")
        self.path = path


class DirectoryDoesNotExistError(FileHandleError):
    def __init__(self, path: str) -> None:
        super().__init__(f"Directory not found: '{path}'")
        self.path = path


class FileAccessError(FileHandleError):
    def __init__(self, path: str, reason: str = "") -> None:
        msg = f"Permission denied: '{path}'"
        if reason:
            msg += f" — {reason}"
        super().__init__(msg)
        self.path = path


class InvalidPathError(FileHandleError):
    def __init__(self, path: str, reason: str = "") -> None:
        msg = f"Invalid path: '{path}'"
        if reason:
            msg += f" — {reason}"
        super().__init__(msg)
        self.path = path
