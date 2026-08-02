"""Unit tests for devmate.ingest.repo_reader."""

import textwrap
from pathlib import Path

import pytest

from devmate.ingest.repo_reader import RepoAnalyzer, analyze_repository


SAMPLE_PY = textwrap.dedent(
    """\
    # module docstring
    import os


    def helper(value: int) -> int:
        \"\"\"Docstring line.\"\"\"
        return value * 2


    async def fetch(url: str) -> str:
        return url


    class Greeter:
        def __init__(self, name: str) -> None:
            self.name = name

        def hello(self) -> str:
            return f"hi {self.name}"


    GREETING = Greeter("world").hello()
    """
)


def _write_tree(tmp_path: Path) -> Path:
    """Create a small fixture repository and return its root."""
    (tmp_path / "app").mkdir()
    (tmp_path / "app" / "main.py").write_text(SAMPLE_PY, encoding="utf-8")
    (tmp_path / "README.md").write_text("# hello\n\nsome docs\n", encoding="utf-8")
    # Excluded directory must be ignored.
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "dep.js").write_text("module.exports = 1;\n", encoding="utf-8")
    return tmp_path


def test_analyze_counts_files_and_languages(tmp_path: Path) -> None:
    root = _write_tree(tmp_path)
    stats = analyze_repository(root)

    assert stats.total_files == 2  # main.py + README.md (node_modules excluded)
    assert stats.languages["python"] == 1
    assert stats.languages["markdown"] == 1
    assert stats.file_types[".py"] == 1


def test_analyze_counts_python_functions_and_classes(tmp_path: Path) -> None:
    root = _write_tree(tmp_path)
    stats = analyze_repository(root)

    # helper, fetch (and 2 methods on Greeter) -> 4 functions; 1 class.
    assert stats.total_functions == 4
    assert stats.total_classes == 1


def test_analyze_counts_lines(tmp_path: Path) -> None:
    root = _write_tree(tmp_path)
    stats = analyze_repository(root)

    py_stats = next(f for f in stats.files if f.path.endswith("main.py"))
    assert py_stats.total_lines == len(SAMPLE_PY.splitlines())
    assert py_stats.code_lines > 0
    assert py_stats.comment_lines >= 1  # module docstring first line + decorator context
    assert py_stats.blank_lines >= 1


def test_analyze_skips_unreadable_and_unsupported(tmp_path: Path) -> None:
    root = _write_tree(tmp_path)
    (root / "app" / "data.bin").write_bytes(b"\x00\x01\x02\xff")
    (root / "app" / "notes.unknown_ext").write_text("nope\n", encoding="utf-8")

    stats = RepoAnalyzer().analyze(root)
    assert stats.total_files == 2  # binary and unknown extension are skipped


def test_exclude_dirs_are_respected(tmp_path: Path) -> None:
    root = _write_tree(tmp_path)
    (root / ".git").mkdir()
    (root / ".git" / "config").write_text("x\n", encoding="utf-8")

    stats = RepoAnalyzer().analyze(root)
    assert ".git" not in stats.languages


def test_analyze_file_returns_none_for_missing_file(tmp_path: Path) -> None:
    analyzer = RepoAnalyzer()
    assert analyzer.analyze_file(tmp_path / "does-not-exist.py") is None


def test_to_dict_roundtrip(tmp_path: Path) -> None:
    root = _write_tree(tmp_path)
    data = analyze_repository(root).to_dict()
    assert data["total_files"] == 2
    assert data["languages"]["python"] == 1
    assert len(data["files"]) == 2
