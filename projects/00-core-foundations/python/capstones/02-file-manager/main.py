"""
File Manager — Mini Project
=============================
Combines: file handling, classes, pathlib, os module, CLI arguments

A CLI file manager with navigation, CRUD operations, and search.

Run: python projects/02-file-manager/main.py
"""

import os
import shutil
import fnmatch
import time
import sys
from pathlib import Path
from datetime import datetime


class FileManager:
    """Interactive CLI file manager with navigation and file operations."""

    def __init__(self, start_dir: str | None = None):
        self.current_dir = Path(start_dir or os.getcwd()).resolve()
        self.clipboard = None  # For cut/copy operations
        self.clipboard_mode = None  # 'copy' or 'cut'
        self.show_hidden = False

    # ── Navigation ────────────────────────────────────────────────────────

    def pwd(self) -> str:
        """Print working directory."""
        return str(self.current_dir)

    def cd(self, path: str) -> str:
        """Change directory."""
        target = Path(path)
        if not target.is_absolute():
            target = self.current_dir / target
        target = target.resolve()

        if not target.exists():
            raise FileNotFoundError(f"Directory not found: {target}")
        if not target.is_dir():
            raise NotADirectoryError(f"Not a directory: {target}")

        self.current_dir = target
        return str(target)

    def ls(self, pattern: str = "*") -> list[dict]:
        """List directory contents with metadata."""
        items = []
        for item in sorted(self.current_dir.iterdir()):
            name = item.name
            if name.startswith(".") and not self.show_hidden:
                continue
            if not fnmatch.fnmatch(name, pattern):
                continue

            stat = item.stat()
            items.append({
                "name": name,
                "type": "dir" if item.is_dir() else "file",
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime),
                "permissions": oct(stat.st_mode)[-3:],
            })
        return items

    def tree(self, max_depth: int = 2, indent: str = "") -> list[str]:
        """Display directory tree structure."""
        lines = []
        items = sorted(self.current_dir.iterdir())
        for i, item in enumerate(items):
            name = item.name
            if name.startswith(".") and not self.show_hidden:
                continue
            is_last = i == len(items) - 1
            prefix = "└── " if is_last else "├── "
            lines.append(f"{indent}{prefix}{name}")
            if item.is_dir() and max_depth > 0:
                sub_indent = indent + ("    " if is_last else "│   ")
                sub_lines = self._subtree(item, max_depth - 1, sub_indent)
                lines.extend(sub_lines)
        return lines

    def _subtree(self, path: Path, depth: int, indent: str) -> list[str]:
        """Recursive helper for tree display."""
        lines = []
        try:
            items = sorted(path.iterdir())
        except PermissionError:
            return [f"{indent}└── (permission denied)"]

        for i, item in enumerate(items):
            name = item.name
            if name.startswith(".") and not self.show_hidden:
                continue
            is_last = i == len(items) - 1
            prefix = "└── " if is_last else "├── "
            lines.append(f"{indent}{prefix}{name}")
            if item.is_dir() and depth > 0:
                sub_indent = indent + ("    " if is_last else "│   ")
                sub_lines = self._subtree(item, depth - 1, sub_indent)
                lines.extend(sub_lines)
        return lines

    # ── File Operations ───────────────────────────────────────────────────

    def read(self, filename: str) -> str:
        """Read and display a file's contents."""
        path = self._resolve(filename)
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {filename}")
        if path.stat().st_size > 1_000_000:
            raise ValueError("File too large to display (> 1MB)")

        return path.read_text(encoding="utf-8")

    def write(self, filename: str, content: str) -> int:
        """Write content to a file (overwrites)."""
        path = self._resolve(filename)
        path.write_text(content, encoding="utf-8")
        return len(content)

    def append(self, filename: str, content: str) -> int:
        """Append content to a file."""
        path = self._resolve(filename)
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
        return len(content)

    def mkfile(self, filename: str) -> str:
        """Create an empty file."""
        path = self._resolve(filename)
        if path.exists():
            raise FileExistsError(f"File already exists: {filename}")
        path.touch()
        return str(path)

    def mkdir(self, dirname: str) -> str:
        """Create a directory."""
        path = self._resolve(dirname)
        path.mkdir(parents=True, exist_ok=True)
        return str(path)

    def remove(self, target: str, recursive: bool = False) -> str:
        """Remove a file or directory."""
        path = self._resolve(target)
        if path.is_dir():
            if recursive:
                shutil.rmtree(path)
            else:
                path.rmdir()  # Only if empty
        else:
            path.unlink()
        return str(path)

    def rename(self, old: str, new: str) -> tuple[str, str]:
        """Rename a file or directory."""
        old_path = self._resolve(old)
        new_path = self._resolve(new)
        old_path.rename(new_path)
        return str(old_path), str(new_path)

    def copy(self, src: str, dst: str) -> tuple[str, str]:
        """Copy a file or directory."""
        src_path = self._resolve(src)
        dst_path = self._resolve(dst)

        if src_path.is_dir():
            shutil.copytree(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)
        return str(src_path), str(dst_path)

    def move(self, src: str, dst: str) -> tuple[str, str]:
        """Move a file or directory."""
        src_path = self._resolve(src)
        dst_path = self._resolve(dst)
        shutil.move(str(src_path), str(dst_path))
        return str(src_path), str(dst_path)

    # ── Search ────────────────────────────────────────────────────────────

    def find(self, pattern: str, max_results: int = 50) -> list[str]:
        """Find files matching a glob pattern recursively."""
        results = []
        for item in self.current_dir.rglob(pattern):
            if item.is_file():
                results.append(str(item.relative_to(self.current_dir)))
                if len(results) >= max_results:
                    break
        return results

    def find_text(self, search_term: str, pattern: str = "*",
                   max_results: int = 20) -> list[tuple[str, int, str]]:
        """Find files containing specific text."""
        results = []
        for item in self.current_dir.rglob(pattern):
            if not item.is_file():
                continue
            if item.stat().st_size > 500_000:  # Skip large files
                continue
            try:
                with open(item, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        if search_term.lower() in line.lower():
                            rel = str(item.relative_to(self.current_dir))
                            results.append((rel, i, line.strip()[:80]))
                            if len(results) >= max_results:
                                return results
            except (UnicodeDecodeError, PermissionError):
                continue
        return results

    # ── Utilities ─────────────────────────────────────────────────────────

    def info(self, target: str) -> dict:
        """Get detailed information about a file or directory."""
        path = self._resolve(target)
        if not path.exists():
            raise FileNotFoundError(f"Not found: {target}")

        stat = path.stat()
        return {
            "name": path.name,
            "type": "directory" if path.is_dir() else "file",
            "size": stat.st_size,
            "size_human": self._human_size(stat.st_size),
            "created": datetime.fromtimestamp(stat.st_ctime),
            "modified": datetime.fromtimestamp(stat.st_mtime),
            "accessed": datetime.fromtimestamp(stat.st_atime),
            "permissions": oct(stat.st_mode)[-3:],
            "absolute": str(path.resolve()),
        }

    def size(self, target: str = ".") -> int:
        """Calculate total size of a file or directory."""
        path = self._resolve(target)
        if path.is_file():
            return path.stat().st_size
        total = 0
        for item in path.rglob("*"):
            if item.is_file():
                total += item.stat().st_size
        return total

    @staticmethod
    def _human_size(size: int) -> str:
        """Convert bytes to human-readable format."""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} PB"

    def _resolve(self, name: str) -> Path:
        """Resolve a filename relative to current directory."""
        path = Path(name)
        if not path.is_absolute():
            path = self.current_dir / path
        return path.resolve()


def format_listing(items: list[dict], human_readable: bool = True) -> str:
    """Format directory listing for display."""
    if not items:
        return "  (empty)"

    # Calculate column widths
    max_name = max(len(item["name"]) for item in items)
    max_name = min(max_name, 50)

    lines = []
    for item in items:
        icon = "📁" if item["type"] == "dir" else "📄"
        size = item["size"]
        size_str = FileManager._human_size(size) if human_readable else str(size)
        modified = item["modified"].strftime("%Y-%m-%d %H:%M")
        lines.append(f"  {icon} {item['name']:<{max_name + 2}} {size_str:>8}  {modified}")
    return "\n".join(lines)


def print_header(text: str, width: int = 60):
    print()
    print("=" * width)
    print(f"  {text}")
    print("=" * width)


def main():
    fm = FileManager()

    print("=" * 50)
    print("  📁 File Manager")
    print("=" * 50)
    print("  Type 'help' for commands, 'quit' to exit.")
    print(f"  Current: {fm.pwd()}")
    print()

    while True:
        try:
            cmd = input(f"📁 {fm.current_dir.name}> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not cmd:
            continue

        if cmd.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        if cmd.lower() == "help":
            print("""
  Navigation:
    pwd                          Show current directory
    cd <path>                    Change directory
    ls [pattern]                 List contents
    tree [depth]                 Show directory tree

  File Operations:
    read <file>                  Display file contents
    write <file> <content>       Write to file
    append <file> <content>      Append to file
    mkfile <name>                Create empty file
    mkdir <name>                 Create directory
    rm <name>                    Remove file
    rmdir <name>                 Remove empty directory
    rm -r <name>                 Remove recursively
    rename <old> <new>           Rename file or directory
    cp <src> <dst>               Copy
    mv <src> <dst>               Move

  Search:
    find <pattern>               Find files
    grep <text> [pattern]        Find text in files

  Info:
    info <name>                  File/directory details
    size [name]                  Calculate size
    hidden                       Toggle hidden files display
    help                         Show this help
    quit                         Exit
            """)
            continue

        parts = cmd.split(maxsplit=2)
        command = parts[0].lower()

        try:
            if command == "pwd":
                print(f"  {fm.pwd()}")

            elif command == "cd":
                target = parts[1] if len(parts) > 1 else "."
                result = fm.cd(target)
                print(f"  → {result}")

            elif command == "ls":
                pattern = parts[1] if len(parts) > 1 else "*"
                items = fm.ls(pattern)
                print(format_listing(items))
                print(f"\n  {len(items)} item(s)")

            elif command == "tree":
                depth = int(parts[1]) if len(parts) > 1 else 2
                lines = fm.tree(depth)
                for line in lines:
                    print(f"  {line}")

            elif command == "read":
                content = fm.read(parts[1])
                print(f"\n{content}")

            elif command == "write":
                content = parts[2] if len(parts) > 2 else ""
                n = fm.write(parts[1], content)
                print(f"  Wrote {n} bytes")

            elif command == "append":
                content = parts[2] if len(parts) > 2 else ""
                n = fm.append(parts[1], content + "\n")
                print(f"  Appended {n} bytes")

            elif command == "mkfile":
                result = fm.mkfile(parts[1])
                print(f"  Created: {result}")

            elif command == "mkdir":
                result = fm.mkdir(parts[1])
                print(f"  Created: {result}")

            elif command == "rm":
                recursive = False
                target = parts[1]
                if target == "-r" and len(parts) > 2:
                    recursive = True
                    target = parts[2]
                fm.remove(target, recursive=recursive)
                print(f"  Removed: {target}")

            elif command == "rmdir":
                fm.remove(parts[1])
                print(f"  Removed: {parts[1]}")

            elif command == "rename":
                if len(parts) < 3:
                    print("  Usage: rename <old> <new>")
                    continue
                old, new = fm.rename(parts[1], parts[2])
                print(f"  {old} → {new}")

            elif command == "cp":
                if len(parts) < 3:
                    print("  Usage: cp <source> <destination>")
                    continue
                src, dst = fm.copy(parts[1], parts[2])
                print(f"  Copied: {src} → {dst}")

            elif command == "mv":
                if len(parts) < 3:
                    print("  Usage: mv <source> <destination>")
                    continue
                src, dst = fm.move(parts[1], parts[2])
                print(f"  Moved: {src} → {dst}")

            elif command == "find":
                pattern = parts[1] if len(parts) > 1 else "*"
                results = fm.find(pattern)
                if results:
                    for r in results:
                        print(f"  {r}")
                    print(f"\n  {len(results)} result(s)")
                else:
                    print("  No results")

            elif command == "grep":
                search = parts[1] if len(parts) > 1 else ""
                pattern = parts[2] if len(parts) > 2 else "*"
                results = fm.find_text(search, pattern)
                if results:
                    for fpath, lineno, line in results:
                        print(f"  {fpath}:{lineno}: {line}")
                    print(f"\n  {len(results)} match(es)")
                else:
                    print("  No matches")

            elif command == "info":
                target = parts[1] if len(parts) > 1 else "."
                info = fm.info(target)
                for key, val in info.items():
                    print(f"  {key}: {val}")

            elif command == "size":
                target = parts[1] if len(parts) > 1 else "."
                total = fm.size(target)
                print(f"  {FileManager._human_size(total)}")

            elif command == "hidden":
                fm.show_hidden = not fm.show_hidden
                print(f"  Hidden files: {'shown' if fm.show_hidden else 'hidden'}")

            else:
                print(f"  Unknown command: {command}. Type 'help' for commands.")

        except (FileNotFoundError, NotADirectoryError, FileExistsError,
                PermissionError, ValueError, IsADirectoryError) as e:
            print(f"  ⚠️  {e}")


if __name__ == "__main__":
    main()
