"""
Repository statistics via AST — counts functions, classes, LOC, and file types.

This is the Week 0 deliverable behind ``devmate stats <repo>``. It walks a repository
tree and produces language-aware statistics:

- file types and line counts (total / code / blank / comment)
- function and class counts for Python files, parsed with the ``ast`` module

The reader is intentionally dependency-free (stdlib only) so the stats command stays
fast and testable without network or services.
"""

from __future__ import annotations

import ast
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

# Directories that are never analyzed (mirrors DocumentLoader.exclude_patterns).
DEFAULT_EXCLUDE_DIRS: Set[str] = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".mimocode",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    ".next",
    ".cache",
    "target",
    "coverage",
}

# Extension -> language label for the file-types / languages tables.
EXTENSION_LANGUAGES: Dict[str, str] = {
    ".py": "python",
    ".pyi": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".hpp": "cpp",
    ".cs": "csharp",
    ".rb": "ruby",
    ".php": "php",
    ".swift": "swift",
    ".kt": "kotlin",
    ".md": "markdown",
    ".rst": "rst",
    ".txt": "text",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".ini": "ini",
    ".cfg": "ini",
    ".html": "html",
    ".css": "css",
    ".scss": "scss",
    ".sql": "sql",
    ".sh": "shell",
    ".bash": "shell",
    ".ps1": "powershell",
    ".dockerfile": "dockerfile",
    ".xml": "xml",
    ".csv": "csv",
}


@dataclass
class FileStats:
    """Statistics for a single file."""

    path: str
    language: str
    extension: str
    total_lines: int = 0
    code_lines: int = 0
    blank_lines: int = 0
    comment_lines: int = 0
    functions: int = 0
    classes: int = 0

    def to_dict(self) -> Dict[str, object]:
        return {
            "path": self.path,
            "language": self.language,
            "extension": self.extension,
            "total_lines": self.total_lines,
            "code_lines": self.code_lines,
            "blank_lines": self.blank_lines,
            "comment_lines": self.comment_lines,
            "functions": self.functions,
            "classes": self.classes,
        }


@dataclass
class RepoStats:
    """Aggregated statistics for a repository."""

    root: str = ""
    total_files: int = 0
    total_lines: int = 0
    total_code_lines: int = 0
    total_functions: int = 0
    total_classes: int = 0
    file_types: Counter = field(default_factory=Counter)
    languages: Counter = field(default_factory=Counter)
    files: List[FileStats] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        return {
            "root": self.root,
            "total_files": self.total_files,
            "total_lines": self.total_lines,
            "total_code_lines": self.total_code_lines,
            "total_functions": self.total_functions,
            "total_classes": self.total_classes,
            "file_types": dict(self.file_types),
            "languages": dict(self.languages),
            "files": [f.to_dict() for f in self.files],
        }


class RepoAnalyzer:
    """Walk a repository and compute statistics."""

    def __init__(self, exclude_dirs: Optional[Set[str]] = None):
        self.exclude_dirs = exclude_dirs or set(DEFAULT_EXCLUDE_DIRS)

    # ------------------------------------------------------------------ public

    def analyze(self, root: Path) -> RepoStats:
        """Analyze every supported file under *root* (recursively)."""
        root = root.resolve()
        stats = RepoStats(root=str(root))

        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            if self._is_excluded(path, root):
                continue

            file_stats = self.analyze_file(path)
            if file_stats is None:
                continue

            stats.files.append(file_stats)
            stats.total_files += 1
            stats.total_lines += file_stats.total_lines
            stats.total_code_lines += file_stats.code_lines
            stats.total_functions += file_stats.functions
            stats.total_classes += file_stats.classes
            stats.file_types[file_stats.extension or "unknown"] += 1
            stats.languages[file_stats.language] += 1

        return stats

    def analyze_file(self, path: Path) -> Optional[FileStats]:
        """Analyze a single file. Returns None for unsupported or unreadable files."""
        ext = path.suffix.lower()
        language = EXTENSION_LANGUAGES.get(ext)
        if language is None and path.name.lower() != "dockerfile":
            return None
        if language is None:
            language = "dockerfile"
            ext = ".dockerfile"

        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            return None

        lines = content.splitlines()
        file_stats = FileStats(
            path=str(path),
            language=language,
            extension=ext,
            total_lines=len(lines),
        )

        if language == "python":
            functions, classes = self._count_python_ast(content)
            file_stats.functions = functions
            file_stats.classes = classes
            code, blank, comment = self._count_lines_python(lines)
        else:
            code, blank, comment = self._count_lines_generic(lines)

        file_stats.code_lines = code
        file_stats.blank_lines = blank
        file_stats.comment_lines = comment
        return file_stats

    # --------------------------------------------------------------- internals

    def _is_excluded(self, path: Path, root: Path) -> bool:
        """True if *path* sits under an excluded directory."""
        try:
            rel = path.relative_to(root)
        except ValueError:
            return True
        parts = set(rel.parts[:-1])  # drop the filename itself
        return bool(parts & self.exclude_dirs)

    @staticmethod
    def _count_python_ast(content: str) -> tuple[int, int]:
        """Return (functions, classes) parsed from the module."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return 0, 0

        functions = sum(
            1
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        )
        classes = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
        return functions, classes

    @staticmethod
    def _count_lines_python(lines: List[str]) -> tuple[int, int, int]:
        """Split lines into (code, blank, comment) for Python."""
        code = 0
        blank = 0
        comment = 0
        for line in lines:
            stripped = line.strip()
            if not stripped:
                blank += 1
            elif stripped.startswith("#"):
                comment += 1
            else:
                code += 1
        return code, blank, comment

    @staticmethod
    def _count_lines_generic(lines: List[str]) -> tuple[int, int, int]:
        """Split lines into (code, blank, comment) using # / // comment heuristics."""
        code = 0
        blank = 0
        comment = 0
        for line in lines:
            stripped = line.strip()
            if not stripped:
                blank += 1
            elif stripped.startswith(("#", "//", "/*", "*", "--")):
                comment += 1
            else:
                code += 1
        return code, blank, comment


def analyze_repository(root: Path, exclude_dirs: Optional[Set[str]] = None) -> RepoStats:
    """Convenience wrapper around :class:`RepoAnalyzer`."""
    return RepoAnalyzer(exclude_dirs=exclude_dirs).analyze(root)
