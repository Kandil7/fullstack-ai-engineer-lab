# 01-core-python — 42: pathlib — Modern Path Handling

## Topic Overview

The `pathlib` module, introduced in Python 3.4 and significantly improved in 3.6+, provides an **object-oriented interface for filesystem paths**. It replaces the error-prone string manipulation of `os.path` with a clean, cross-platform `Path` class. For AI and backend engineers, `pathlib` is essential: training pipelines walk dataset directories of 100k+ images, inference services locate model checkpoints across runs, and CI/CD systems build output paths that must work identically on Windows, Linux, and macOS.

Every major ML framework (PyTorch, TensorFlow, Hugging Face) now accepts `Path` objects natively. The standard library itself uses `pathlib` internally. If you're still concatenating strings with `os.path.join` or f-strings, you're writing legacy code.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Construct `Path` objects using the `/` operator and factory methods
2. Extract path components (name, stem, suffix, parent, parents)
3. Resolve paths absolutely and follow symlinks with `resolve()`
4. Check existence and type with `exists()`, `is_file()`, `is_dir()`
4. Traverse directories with `glob()`, `rglob()`, and `iterdir()`
5. Read/write text and binary files with `read_text()`, `write_text()`, `read_bytes()`, `write_bytes()`
6. Create directories safely with `mkdir(parents=True, exist_ok=True)`
7. Manipulate paths for ML workflows: checkpoint naming, latest model discovery, cross-platform compatibility
8. Avoid the three most common `pathlib` mistakes

## Prerequisites

| Need | Where |
|------|-------|
| Basic file I/O concepts | `38-file-handling.py` |
| String manipulation | `10-strings.py` |
| Context managers | `02-advanced-python/03-context-managers.py` |

## 1. Path Construction

### The `/` Operator

The single most important feature of `pathlib` is the overloaded `/` operator. It joins path components intelligently, handling separators automatically:

```python
from pathlib import Path

# Instead of os.path.join("data", "raw", "images")
p = Path("data") / "raw" / "images"
print(p)  # data/raw/images (POSIX) or data\raw\images (Windows)

# Works with absolute and relative paths
Path("/home/user") / "projects" / "model.pt"
Path.home() / "models" / "checkpoint.pt"
Path.cwd() / "outputs" / "run_001"
```

**Why this matters:** String concatenation (`"data/" + "train"`) breaks on Windows. The `/` operator never does.

### Factory Methods

```python
Path("relative/path")           # From string
Path.cwd()                      # Current working directory
Path.home()                     # User's home directory
Path(__file__)                  # This script's path
Path("/absolute/path")          # Absolute path
```

## 2. Path Properties

Every `Path` object exposes components as read-only properties:

```python
p = Path("/home/user/data/train.csv")

p.name        # "train.csv"      — final component
p.stem        # "train"          — name without suffix
p.suffix      # ".csv"           — last suffix
p.suffixes    # [".csv"]         — all suffixes (e.g. [".tar", ".gz"])
p.parent      # "/home/user/data" — parent directory
p.parents     # ["/home/user/data", "/home/user", "/home", "/"] — immutable sequence
p.root        # "/"              — root prefix
p.drive       # "" (POSIX) or "C:" (Windows) — drive letter
```

**Key distinction:** `parent` returns a single `Path`; `parents` is an iterable of all ancestors from immediate parent to root.

## 3. Resolution & Existence

### `absolute()` vs `resolve()`

| Method | Symlinks | Use Case |
|--------|----------|----------|
| `absolute()` | Preserved | Fast path normalization |
| `resolve()` | **Followed** | Canonical location, security checks |

```python
p = Path("data/../models/model.pt")

p.absolute()  # /home/user/project/data/../models/model.pt
p.resolve()   # /home/user/project/models/model.pt  (normalized + symlinks followed)
```

**Security note:** `resolve()` is critical when accepting user-supplied paths — it prevents directory traversal attacks by resolving `../../../etc/passwd` to its actual location.

### Existence Checks

```python
p = Path("model.pt")

p.exists()    # True if file or dir exists
p.is_file()   # True only if regular file
p.is_dir()    # True only if directory
p.is_symlink() # True if symlink
```

**Performance:** These are syscalls. In hot loops, cache the result or use `try/except` with `open()` (EAFP style).

## 4. Directory Traversal

### `glob()` — Non-recursive

```python
# Files matching pattern in this directory only
for img in Path("data").glob("*.jpg"):
    print(img)
```

### `rglob()` — Recursive

```python
# All .jpg files anywhere under data/
for img in Path("data").rglob("*.jpg"):
    print(img)
```

**Pattern syntax:** Uses `fnmatch` — `*` matches anything except `/`, `?` matches single char, `[abc]` matches character class.

### `iterdir()` — Direct children only

```python
for entry in Path("data").iterdir():
    if entry.is_dir():
        print(f"DIR:  {entry.name}")
    else:
        print(f"FILE: {entry.name}")
```

**Performance tip:** `iterdir()` is faster than `glob("*")` when you need all entries.

## 5. Reading & Writing Files

`Path` provides convenient high-level I/O methods:

```python
p = Path("config.json")

# Text (defaults to UTF-8)
p.write_text('{"lr": 1e-4}')
content = p.read_text()
content = p.read_text(encoding="utf-8")  # Explicit

# Binary
p.write_bytes(b"\x00\x01\x02")
data = p.read_bytes()

# Append (write_text overwrites by default)
p.write_text(content + "\nnew line", encoding="utf-8")
```

**Warning:** `write_text`/`write_bytes` overwrite silently. For atomic writes, use a temp file + `replace()`.

## 6. Directory Creation

```python
# Safe: creates parents, ignores existing
Path("experiments/run_001/checkpoints").mkdir(parents=True, exist_ok=True)

# Strict: raises if parents missing (legacy behavior)
Path("a/b/c").mkdir()  # FileNotFoundError if a/b doesn't exist
```

**Always use `parents=True, exist_ok=True`** in production code. The strict mode exists only for backward compatibility.

## 7. ML Workflow Patterns

### Checkpoint Naming Convention

```python
def checkpoint_path(base: Path, model: str, epoch: int, metric: float) -> Path:
    """Generate sortable, informative checkpoint paths."""
    return base / model / f"epoch_{epoch:04d}_val_acc_{metric:.4f}.pt"

# Produces: models/bert/epoch_0001_val_acc_0.9234.pt
# Lexicographic sort = chronological sort
```

### Finding Latest Checkpoint

```python
def latest_checkpoint(ckpt_dir: Path) -> Path | None:
    """Return most recently modified .pt file, or None."""
    checkpoints = list(ckpt_dir.glob("*.pt"))
    if not checkpoints:
        return None
    return max(checkpoints, key=lambda p: p.stat().st_mtime)
```

### Walking Dataset Directories

```python
def count_images(data_root: Path) -> dict[str, int]:
    """Count images per class (subdirectory)."""
    counts = {}
    for class_dir in data_root.iterdir():
        if class_dir.is_dir():
            counts[class_dir.name] = len(list(class_dir.rglob("*.jpg")))
    return counts
```

### Cross-Platform Path Building

```python
# WRONG - breaks on Windows
path = "models/" + model_name + "/checkpoint.pt"

# CORRECT - works everywhere
path = Path("models") / model_name / "checkpoint.pt"

# Path.parts gives normalized components
Path("a/b/c").parts    # ("a", "b", "c")
Path("a//b/./c").parts # ("a", "b", "c") — normalized
```

## 8. Common Mistakes

### Mistake 1: String Concatenation

```python
# WRONG
path = "data/" + "train" + "/images.jpg"   # Hardcoded separator
path = os.path.join("data", "train")       # Legacy, verbose

# CORRECT
path = Path("data") / "train" / "images.jpg"
```

### Mistake 2: Forgetting `parents=True`

```python
# WRONG — raises FileNotFoundError if parent missing
Path("experiments/run_01/checkpoints").mkdir()

# CORRECT
Path("experiments/run_01/checkpoints").mkdir(parents=True, exist_ok=True)
```

### Mistake 3: `resolve()` on Non-Existent Paths

```python
# WRONG — returns absolute path but doesn't verify existence
Path("maybe_missing.txt").resolve()

# CORRECT (Python 3.6+) — raises FileNotFoundError if missing
Path("maybe_missing.txt").resolve(strict=True)

# Or check first
p = Path("maybe_missing.txt")
if p.exists():
    canonical = p.resolve()
```

### Mistake 4: Mixing `Path` and Strings

```python
# WRONG — loses pathlib benefits
path = Path("data") / "train"
open(str(path))  # Unnecessary conversion

# CORRECT — Path works directly with open()
with open(path) as f:  # Python 3.6+
    data = f.read()
```

## Complexity and Cost

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| `Path()` construction | O(1) | O(k) | k = path length |
| `/` operator | O(1) | O(k) | Returns new Path |
| `resolve()` | O(k) | O(k) | Syscalls per component |
| `glob()` / `rglob()` | O(n) | O(n) | n = matching files |
| `iterdir()` | O(n) | O(1) | Generator, lazy |
| `mkdir(parents=True)` | O(d) | O(1) | d = depth |
| `read_text()` | O(file) | O(file) | Loads entire file |

**At scale:** Walking 1M files with `rglob()` materializes a list — use `iterdir()` + manual recursion for streaming.

## AI Engineering Relevance

**Where this shows up:**

| Concept | AI/Backend Use Case |
|---------|---------------------|
| `Path / Path` | Building checkpoint paths: `Path("models") / name / f"epoch_{epoch}.pt"` |
| `rglob("*.jpg")` | Walking 100k-image dataset for training |
| `mkdir(parents=True)` | Creating experiment directories: `runs/exp_001/checkpoints/` |
| `resolve()` | Canonicalizing user upload paths for security |
| `read_text()` | Loading JSON/YAML configs for model hyperparameters |
| `stat().st_mtime` | Finding latest checkpoint for resume |

**Scale note:** At 1M files, `rglob("*")` materializes a 1M-element list (~50 MB). For streaming, use `os.scandir()` or manual `iterdir()` recursion. At 100M files, even that struggles — use a database or manifest file.

## Practice Exercises

### Exercise 1: Path Construction (Easy)
**Task:** Given `base = Path("/models")`, `model = "bert"`, `epoch = 42`, construct the path `/models/bert/checkpoint_epoch_0042.pt` using only `/` operator and f-strings.

**Signature:** `def checkpoint_path(base: Path, model: str, epoch: int) -> Path:`

**Expected:** `checkpoint_path(Path("/models"), "bert", 42)` → `Path("/models/bert/checkpoint_epoch_0042.pt")`

### Exercise 2: Find Latest Checkpoint (Medium)
**Task:** Implement `latest_checkpoint(dir: Path) -> Path | None` that returns the most recently modified `.pt` file in a directory, or `None` if empty.

**Constraints:** Must handle empty directory, non-existent directory, and permission errors gracefully.

### Exercise 3: Dataset Statistics (Hard)
**Task:** Write `dataset_stats(root: Path) -> dict[str, int]` that returns `{class_name: image_count}` for a directory structured as `root/class_name/*.jpg`. Must handle 100k+ files efficiently (stream, don't materialize full list).

## Summary

| Concept | Key Takeaway |
|---------|--------------|
| `Path` + `/` | Cross-platform path building, never string concat |
| `resolve()` | Canonical path, follows symlinks, security critical |
| `glob()` / `rglob()` | Pattern matching, recursive or not |
| `mkdir(parents=True, exist_ok=True)` | Safe directory creation, always use this |
| `read_text()` / `write_text()` | Convenience I/O, UTF-8 default |
| `stat().st_mtime` | Finding latest file by modification time |

**Next:** `43-dataclasses-and-namedtuples.py` — structured data for configs and records.

---

Official docs: https://docs.python.org/3/library/pathlib.html