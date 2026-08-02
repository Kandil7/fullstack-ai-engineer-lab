# 42: pathlib — Glossary

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| Path | Class | Object-oriented filesystem path representation |
| PurePath | Class | Path manipulation without I/O (no syscalls) |
| / operator | Operator | Joins path components cross-platform |
| resolve() | Method | Returns absolute path, follows symlinks |
| absolute() | Method | Returns absolute path, preserves symlinks |
| glob() | Method | Non-recursive pattern matching |
| rglob() | Method | Recursive pattern matching |
| iterdir() | Method | Iterator over direct children |
| mkdir() | Method | Creates directory |
| read_text() | Method | Reads file as UTF-8 string |
| write_text() | Method | Writes string to file |
| read_bytes() | Method | Reads file as bytes |
| write_bytes() | Method | Writes bytes to file |
| exists() | Method | True if path exists |
| is_file() | Method | True if regular file |
| is_dir() | Method | True if directory |
| stat() | Method | Returns os.stat_result |
| stem | Property | Filename without suffix |
| suffix | Property | File extension including dot |
| suffixes | Property | List of all suffixes |
| parent | Property | Parent directory Path |
| parents | Property | Immutable sequence of all ancestors |
| name | Property | Final path component |
| parts | Property | Tuple of normalized path components |

## Detailed Definitions

### Path
**Definition**: The main class in `pathlib` representing a filesystem path with I/O capabilities. Inherits from `PurePath` and adds methods that access the filesystem (`exists()`, `read_text()`, `mkdir()`, etc.).

**Example**:
```python
from pathlib import Path
p = Path("data") / "train.csv"
print(p.exists())      # True/False — syscall
print(p.read_text())   # File content — syscall
p.write_text("new")    # Syscall
```

**Complexity**: Construction O(1), I/O methods O(file size)

**Related**: PurePath, os.path

### PurePath
**Definition**: Base class providing path manipulation without filesystem access. No I/O methods. Useful for manipulating paths that don't exist yet or for testing.

**Example**:
```python
from pathlib import PurePath
p = PurePath("a") / "b" / "c"  # No syscall
print(p.name)  # "c" — pure computation
```

**Complexity**: All operations O(1) — no syscalls

**Related**: Path

### / operator
**Definition**: Overloaded division operator on `Path` and `PurePath` that joins path components using the platform-appropriate separator.

**Example**:
```python
Path("models") / "bert" / "checkpoint.pt"
# POSIX: "models/bert/checkpoint.pt"
# Windows: "models\\bert\\checkpoint.pt"
```

**Complexity**: O(1) — returns new Path object

**Related**: Path.joinpath()

### resolve()
**Definition**: Returns the absolute path, resolving all symlinks and normalizing `..` and `.` components. The canonical form of a path.

**Example**:
```python
# Assume /home/user/project/data -> /mnt/data (symlink)
Path("project/data/../models").resolve()
# Returns: /mnt/data/models (normalized + symlink followed)
```

**Complexity**: O(k) where k = path depth; makes syscalls per component

**Related**: absolute(), os.path.realpath()

### absolute()
**Definition**: Returns the absolute path without resolving symlinks or normalizing `..`. Faster than `resolve()` but not canonical.

**Example**:
```python
Path("../models").absolute()
# Returns: /home/user/project/../models (NOT normalized)
```

**Complexity**: O(1) — no symlink resolution

**Related**: resolve()

### glob()
**Definition**: Returns a generator of `Path` objects matching a pattern in the current directory only (non-recursive).

**Example**:
```python
for p in Path("data").glob("*.jpg"):
    print(p)
```

**Complexity**: O(n) where n = entries in directory

**Related**: rglob(), fnmatch

### rglob()
**Definition**: Returns a generator of `Path` objects matching a pattern recursively (current directory and all subdirectories).

**Example**:
```python
for p in Path("data").rglob("*.jpg"):
    print(p)  # Includes data/train/cat.jpg, data/val/dog.jpg, etc.
```

**Complexity**: O(n) where n = matching files; materializes full list if converted to list

**Related**: glob(), os.walk()

### iterdir()
**Definition**: Returns an iterator over direct children of a directory (files and subdirectories).

**Example**:
```python
for entry in Path("data").iterdir():
    if entry.is_dir():
        print(f"DIR: {entry.name}")
    else:
        print(f"FILE: {entry.name}")
```

**Complexity**: O(1) per iteration; lazy, memory-efficient

**Related**: os.scandir(), os.listdir()

### mkdir()
**Definition**: Creates a directory. Key parameters: `parents=True` creates intermediate directories; `exist_ok=True` suppresses error if directory exists.

**Example**:
```python
Path("experiments/run_001/checkpoints").mkdir(parents=True, exist_ok=True)
```

**Complexity**: O(d) where d = directory depth

**Related**: os.makedirs(), os.mkdir()

### read_text()
**Definition**: Reads entire file as UTF-8 string (configurable encoding). Loads entire file into memory.

**Example**:
```python
config = Path("config.json").read_text()
config = Path("data.txt").read_text(encoding="latin-1")
```

**Complexity**: O(file size) time and space

**Related**: write_text(), read_bytes(), open()

### write_text()
**Definition**: Writes string to file, overwriting existing content. Defaults to UTF-8.

**Example**:
```python
Path("output.txt").write_text("Hello\nWorld")
Path("config.json").write_text(json.dumps(config), encoding="utf-8")
```

**Complexity**: O(string length) time

**Related**: read_text(), write_bytes()

### read_bytes() / write_bytes()
**Definition**: Binary I/O equivalents of read_text/write_text. No encoding/decoding.

**Example**:
```python
data = Path("model.bin").read_bytes()
Path("output.bin").write_bytes(b"\x00\x01\x02")
```

**Complexity**: O(file size)

**Related**: read_text(), write_text()

### exists() / is_file() / is_dir()
**Definition**: Existence and type checks. Each is a separate syscall.

**Example**:
```python
p = Path("model.pt")
if p.exists() and p.is_file():
    print("Model file exists")
```

**Complexity**: O(1) syscall each

**Related**: os.path.exists(), os.stat()

### stat()
**Definition**: Returns `os.stat_result` with file metadata: size, modification time, permissions, etc.

**Example**:
```python
st = Path("model.pt").stat()
print(st.st_size)      # File size in bytes
print(st.st_mtime)     # Modification timestamp (float)
print(st.st_mode)      # Permissions
```

**Complexity**: O(1) syscall

**Related**: os.stat(), lstat()

### stem
**Definition**: Filename without the final suffix. For `archive.tar.gz`, stem is `archive.tar`.

**Example**:
```python
Path("model_final.pt").stem      # "model_final"
Path("archive.tar.gz").stem      # "archive.tar" (only last suffix removed)
```

**Complexity**: O(1)

**Related**: suffix, suffixes, name

### suffix
**Definition**: Final file extension including the dot. For `archive.tar.gz`, suffix is `.gz`.

**Example**:
```python
Path("model.pt").suffix      # ".pt"
Path("data.csv").suffix      # ".csv"
Path("README").suffix        # "" (empty)
```

**Complexity**: O(1)

**Related**: suffixes, stem

### suffixes
**Definition**: List of all suffixes. For `archive.tar.gz`, returns `[".tar", ".gz"]`.

**Example**:
```python
Path("model.pt").suffixes       # [".pt"]
Path("archive.tar.gz").suffixes # [".tar", ".gz"]
```

**Complexity**: O(1)

**Related**: suffix, stem

### parent
**Definition**: The logical parent directory of the path.

**Example**:
```python
Path("/home/user/file.txt").parent  # Path("/home/user")
Path("file.txt").parent             # Path(".")
```

**Complexity**: O(1)

**Related**: parents

### parents
**Definition**: Immutable sequence of all ancestor directories from immediate parent to root.

**Example**:
```python
p = Path("/home/user/project/file.txt")
list(p.parents)  # [/home/user/project, /home/user, /home, /]
```

**Complexity**: O(d) where d = depth

**Related**: parent

### name
**Definition**: Final component of the path (filename or directory name).

**Example**:
```python
Path("/home/user/file.txt").name   # "file.txt"
Path("/home/user/").name           # "user"
```

**Complexity**: O(1)

**Related**: stem, suffix

### parts
**Definition**: Tuple of normalized path components. Separators and `.` components are removed.

**Example**:
```python
Path("a/b/c").parts           # ("a", "b", "c")
Path("/a/b/c").parts          # ("/", "a", "b", "c")
Path("a//b/./c").parts        # ("a", "b", "c") — normalized
```

**Complexity**: O(k) where k = components

**Related**: parent, name

## Key Concepts Summary

### Path vs String Operations

| Operation | String (Legacy) | pathlib (Modern) |
|-----------|-----------------|------------------|
| Join | `os.path.join(a, b)` | `Path(a) / b` |
| Dirname | `os.path.dirname(p)` | `Path(p).parent` |
| Basename | `os.path.basename(p)` | `Path(p).name` |
| Extension | `os.path.splitext(p)[1]` | `Path(p).suffix` |
| Exists | `os.path.exists(p)` | `Path(p).exists()` |
| Is file | `os.path.isfile(p)` | `Path(p).is_file()` |
| Read all | `open(p).read()` | `Path(p).read_text()` |
| Write all | `open(p, 'w').write(s)` | `Path(p).write_text(s)` |
| Make dirs | `os.makedirs(p, exist_ok=True)` | `Path(p).mkdir(parents=True, exist_ok=True)` |

### Safe Patterns Checklist

- [ ] Always use `/` operator, never string concatenation
- [ ] Always `mkdir(parents=True, exist_ok=True)`
- [ ] Use `resolve()` for canonical paths, especially from user input
- [ ] Use `resolve(strict=True)` (3.6+) when path must exist
- [ ] Prefer `iterdir()` over `glob("*")` for full directory listing
- [ ] `Path` works directly with `open()` — no `str()` needed (3.6+)

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Path          — ___
2. resolve()     — ___
3. rglob()       — ___
4. stem          — ___
5. suffixes      — ___
6. parents       — ___
6. iterdir()     — ___
7. write_text()  — ___
8. PurePath      — ___
9. resolve(strict=True) — ___

A. Filename without final suffix
B. Returns absolute path, follows symlinks
C. Main pathlib class with I/O methods
D. Path manipulation without I/O
E. Recursive pattern matching
F. Raises if path doesn't exist (3.6+)
G. All suffixes as list
H. Writes string to file (UTF-8 default)
I. Immutable sequence of ancestor directories
J. Iterator over direct children

**Answers:** 1-C, 2-B, 3-E, 4-A, 5-G, 6-I, 7-J, 8-H, 9-D, 10-F