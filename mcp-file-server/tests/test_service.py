from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.mcp_file.exceptions import (
    DirectoryDoesNotExistError,
    FileAlreadyExistsError,
    FileDoesNotExistError,
    FileHandleError,
    InvalidPathError,
)
from src.mcp_file.models import AppendFileRequest, WriteFileRequest
from src.mcp_file.service import FileService


def _make_service() -> FileService:
    return FileService()


class ReadFileTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.service = _make_service()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _write(self, name: str, content: str) -> str:
        p = self.root / name
        p.write_text(content, encoding="utf-8")
        return str(p)

    def test_reads_file_content(self) -> None:
        path = self._write("hello.txt", "Hello, World!")
        self.assertEqual(self.service.read_file(path), "Hello, World!")

    def test_raises_on_missing_file(self) -> None:
        with self.assertRaises(FileDoesNotExistError):
            self.service.read_file(str(self.root / "nonexistent.txt"))

    def test_raises_on_empty_path(self) -> None:
        with self.assertRaises(InvalidPathError):
            self.service.read_file("")

    def test_raises_on_unsupported_encoding(self) -> None:
        path = self._write("file.txt", "content")
        with self.assertRaises(FileHandleError):
            self.service.read_file(path, encoding="utf-32")


class WriteFileTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.service = _make_service()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_writes_new_file(self) -> None:
        path = str(self.root / "new.txt")
        self.service.write_file(WriteFileRequest(path=path, content="hello"))
        self.assertEqual(Path(path).read_text(), "hello")

    def test_overwrites_existing_file(self) -> None:
        path = str(self.root / "existing.txt")
        Path(path).write_text("old content")
        self.service.write_file(WriteFileRequest(path=path, content="new content", overwrite=True))
        self.assertEqual(Path(path).read_text(), "new content")

    def test_raises_when_overwrite_false_and_file_exists(self) -> None:
        path = str(self.root / "existing.txt")
        Path(path).write_text("old")
        with self.assertRaises(FileAlreadyExistsError):
            self.service.write_file(WriteFileRequest(path=path, content="new", overwrite=False))

    def test_raises_when_parent_dir_missing(self) -> None:
        path = str(self.root / "subdir" / "file.txt")
        with self.assertRaises(DirectoryDoesNotExistError):
            self.service.write_file(WriteFileRequest(path=path, content="x"))


class AppendFileTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.service = _make_service()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_appends_to_file(self) -> None:
        path = str(self.root / "log.txt")
        Path(path).write_text("line1\n")
        self.service.append_to_file(AppendFileRequest(path=path, content="line2\n"))
        self.assertEqual(Path(path).read_text(), "line1\nline2\n")

    def test_raises_when_file_does_not_exist(self) -> None:
        with self.assertRaises(FileDoesNotExistError):
            self.service.append_to_file(AppendFileRequest(path=str(self.root / "ghost.txt"), content="x"))


class DeleteFileTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.service = _make_service()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_deletes_file(self) -> None:
        path = str(self.root / "to_delete.txt")
        Path(path).write_text("bye")
        self.service.delete_file(path)
        self.assertFalse(Path(path).exists())

    def test_deletes_directory_tree(self) -> None:
        d = self.root / "mydir"
        d.mkdir()
        (d / "child.txt").write_text("x")
        self.service.delete_file(str(d))
        self.assertFalse(d.exists())

    def test_raises_when_file_does_not_exist(self) -> None:
        with self.assertRaises(FileDoesNotExistError):
            self.service.delete_file(str(self.root / "ghost.txt"))


class ListDirectoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.service = _make_service()
        (self.root / "a.txt").write_text("a")
        (self.root / "b.py").write_text("b")
        (self.root / "subdir").mkdir()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_lists_all_entries(self) -> None:
        entries = self.service.list_directory(str(self.root))
        names = {e.name for e in entries}
        self.assertIn("a.txt", names)
        self.assertIn("b.py", names)
        self.assertIn("subdir", names)

    def test_filters_by_glob_pattern(self) -> None:
        entries = self.service.list_directory(str(self.root), pattern="*.txt")
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].name, "a.txt")

    def test_dirs_sorted_before_files(self) -> None:
        entries = self.service.list_directory(str(self.root))
        self.assertTrue(entries[0].is_dir)

    def test_raises_on_missing_directory(self) -> None:
        with self.assertRaises(FileDoesNotExistError):
            self.service.list_directory(str(self.root / "nonexistent"))


class MoveFileTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.service = _make_service()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_moves_file(self) -> None:
        src = str(self.root / "src.txt")
        dst = str(self.root / "dst.txt")
        Path(src).write_text("hello")
        self.service.move_file(src, dst)
        self.assertFalse(Path(src).exists())
        self.assertEqual(Path(dst).read_text(), "hello")

    def test_raises_when_source_missing(self) -> None:
        with self.assertRaises(FileDoesNotExistError):
            self.service.move_file(str(self.root / "ghost.txt"), str(self.root / "out.txt"))


class CopyFileTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.service = _make_service()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_copies_file(self) -> None:
        src = str(self.root / "src.txt")
        dst = str(self.root / "dst.txt")
        Path(src).write_text("hello")
        self.service.copy_file(src, dst)
        self.assertTrue(Path(src).exists())
        self.assertEqual(Path(dst).read_text(), "hello")

    def test_raises_when_dst_exists_and_no_overwrite(self) -> None:
        src = str(self.root / "src.txt")
        dst = str(self.root / "dst.txt")
        Path(src).write_text("hello")
        Path(dst).write_text("existing")
        with self.assertRaises(FileAlreadyExistsError):
            self.service.copy_file(src, dst, overwrite=False)

    def test_overwrites_when_flag_set(self) -> None:
        src = str(self.root / "src.txt")
        dst = str(self.root / "dst.txt")
        Path(src).write_text("new")
        Path(dst).write_text("old")
        self.service.copy_file(src, dst, overwrite=True)
        self.assertEqual(Path(dst).read_text(), "new")


class GetFileInfoTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.service = _make_service()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_returns_file_metadata(self) -> None:
        path = str(self.root / "info.txt")
        Path(path).write_text("content")
        info = self.service.get_file_info(path)
        self.assertEqual(info.name, "info.txt")
        self.assertTrue(info.is_file)
        self.assertFalse(info.is_dir)
        self.assertEqual(info.extension, ".txt")
        self.assertGreater(info.size, 0)
        self.assertIsNotNone(info.modified_at)

    def test_returns_directory_metadata(self) -> None:
        info = self.service.get_file_info(str(self.root))
        self.assertTrue(info.is_dir)
        self.assertFalse(info.is_file)

    def test_raises_on_missing_path(self) -> None:
        with self.assertRaises(FileDoesNotExistError):
            self.service.get_file_info(str(self.root / "ghost.txt"))


class SearchInFileTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.service = _make_service()
        self.path = str(self.root / "search.txt")
        Path(self.path).write_text("Hello World\nfoo bar\nHELLO again\n")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_finds_matching_lines(self) -> None:
        results = self.service.search_in_file(self.path, "Hello")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].line_number, 1)

    def test_case_insensitive_search(self) -> None:
        results = self.service.search_in_file(self.path, "hello", case_sensitive=False)
        self.assertEqual(len(results), 2)

    def test_returns_empty_for_no_match(self) -> None:
        results = self.service.search_in_file(self.path, "zzznomatch")
        self.assertEqual(results, [])

    def test_raises_on_empty_query(self) -> None:
        with self.assertRaises(InvalidPathError):
            self.service.search_in_file(self.path, "")


class CreateDirectoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.service = _make_service()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_creates_directory(self) -> None:
        path = str(self.root / "new_dir")
        self.service.create_directory(path)
        self.assertTrue(Path(path).is_dir())

    def test_creates_nested_directories(self) -> None:
        path = str(self.root / "a" / "b" / "c")
        self.service.create_directory(path)
        self.assertTrue(Path(path).is_dir())

    def test_raises_when_already_exists(self) -> None:
        path = str(self.root / "existing")
        Path(path).mkdir()
        with self.assertRaises(FileAlreadyExistsError):
            self.service.create_directory(path)


if __name__ == "__main__":
    unittest.main()
