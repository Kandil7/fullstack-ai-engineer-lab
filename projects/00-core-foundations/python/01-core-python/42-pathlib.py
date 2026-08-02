"""
01-core-python — 42: pathlib — Modern Path Handling
===================================================
Topics: Path construction, / operator, glob/rglob, read_text/write_text,
        mkdir(parents=True), resolve() vs absolute(), Windows vs POSIX

Why this matters for AI/backend engineering:
    Walking a dataset directory of 100k images; locating model checkpoints
    across runs; building output paths that work on Windows and Linux CI alike.
    pathlib is the standard — string paths are legacy.

Run:      python 42-pathlib.py
Verify:   python 42-pathlib.py --verify
Reference: https://docs.python.org/3/library/pathlib.html
"""

from __future__ import annotations

import sys
import tempfile
import shutil
from pathlib import Path

# ============================================================
# 1. Path Construction & Basic Operations
# ============================================================
# Complexity: O(1) for construction, O(k) for resolution where k = path depth

# Example 1: Creating Path objects
p1 = Path("data") / "raw" / "images" / "train"
print(f"Path via / operator: {p1}")

p2 = Path.home() / "projects" / "model.pt"
print(f"Path with home(): {p2}")

# Example 2: Path properties
path = Path("/home/user/data/train.csv")
print(f"\nPath: {path}")
print(f"  name:      {path.name}")        # train.csv
print(f"  stem:      {path.stem}")        # train
print(f"  suffix:    {path.suffix}")      # .csv
print(f"  suffixes:  {path.suffixes}")    # ['.csv']
print(f"  parent:    {path.parent}")      # /home/user/data
print(f"  parents:   {list(path.parents)}")

# ============================================================
# 2. Path Resolution & Existence
# ============================================================

# Example 3: exists, is_file, is_dir
test_file = Path(__file__)
print(f"\nThis file exists: {test_file.exists()}")
print(f"Is file: {test_file.is_file()}")
print(f"Is dir:  {test_file.is_dir()}")

# Example 4: absolute() vs resolve()
relative = Path(".")
print(f"\nRelative: {relative}")
print(f"  absolute(): {relative.absolute()}")
print(f"  resolve():  {relative.resolve()}")  # resolves symlinks

# Symlink demonstration
with tempfile.TemporaryDirectory() as tmp:
    tmp_path = Path(tmp)
    real = tmp_path / "real_file.txt"
    real.write_text("content")
    link = tmp_path / "link.txt"
    link.symlink_to(real)
    print(f"\nSymlink demo:")
    print(f"  link.absolute(): {link.absolute()}")
    print(f"  link.resolve():  {link.resolve()}")

# ============================================================
# 3. Directory Traversal with glob/rglob
# ============================================================

# Example 5: glob patterns
with tempfile.TemporaryDirectory() as tmp:
    tmp_path = Path(tmp)
    (tmp_path / "train").mkdir()
    (tmp_path / "val").mkdir()
    (tmp_path / "train" / "cat.jpg").write_text("fake")
    (tmp_path / "train" / "dog.jpg").write_text("fake")
    (tmp_path / "val" / "cat.jpg").write_text("fake")
    (tmp_path / "test.png").write_text("fake")

    print(f"\nDirectory structure:")
    for p in tmp_path.rglob("*"):
        print(f"  {p.relative_to(tmp_path)}")

    print(f"\nAll .jpg files (rglob):")
    for p in tmp_path.rglob("*.jpg"):
        print(f"  {p.relative_to(tmp_path)}")

    print(f"\nDirect children only (glob):")
    for p in tmp_path.glob("*"):
        print(f"  {p.relative_to(tmp_path)}")

# ============================================================
# 4. Reading & Writing Files
# ============================================================

# Example 6: read_text, write_text, read_bytes, write_bytes
with tempfile.TemporaryDirectory() as tmp:
    tmp_path = Path(tmp)
    file = tmp_path / "config.json"
    
    # Write
    file.write_text('{"model": "bert", "epochs": 10}')
    print(f"\nWrote: {file.read_text()}")
    
    # Append
    file.write_text(file.read_text() + '\n', encoding='utf-8')
    
    # Binary
    bin_file = tmp_path / "model.bin"
    bin_file.write_bytes(b"\x00\x01\x02\x03")
    print(f"Binary read: {bin_file.read_bytes()}")

# ============================================================
# 5. Directory Creation & Manipulation
# ============================================================

# Example 7: mkdir with parents and exist_ok
with tempfile.TemporaryDirectory() as tmp:
    tmp_path = Path(tmp)
    deep = tmp_path / "experiments" / "run_001" / "checkpoints"
    deep.mkdir(parents=True, exist_ok=True)
    print(f"\nCreated deep path: {deep.exists()}")
    
    # Safe re-creation
    deep.mkdir(parents=True, exist_ok=True)  # No error

# Example 8: Iterating directory contents
with tempfile.TemporaryDirectory() as tmp:
    tmp_path = Path(tmp)
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "b.txt").write_text("b")
    (tmp_path / "subdir").mkdir()
    
    print(f"\nIterating with iterdir():")
    for item in tmp_path.iterdir():
        print(f"  {item.name} {'(dir)' if item.is_dir() else '(file)'}")

# ============================================================
# 6. Path Manipulation for ML Workflows
# ============================================================

# Example 9: Building checkpoint paths
def checkpoint_path(base: Path, model_name: str, epoch: int, metric: float) -> Path:
    """Generate standardized checkpoint path."""
    return base / model_name / f"epoch_{epoch:04d}_metric_{metric:.4f}.pt"

base = Path("/models")
print(f"\nCheckpoint paths:")
for epoch, metric in [(1, 0.9234), (10, 0.9567), (50, 0.9721)]:
    print(f"  {checkpoint_path(base, 'bert-base', epoch, metric)}")

# Example 10: Finding latest checkpoint
with tempfile.TemporaryDirectory() as tmp:
    tmp_path = Path(tmp)
    ckpt_dir = tmp_path / "checkpoints"
    ckpt_dir.mkdir()
    (ckpt_dir / "model_epoch_0001.pt").write_text("1")
    (ckpt_dir / "model_epoch_0010.pt").write_text("10")
    (ckpt_dir / "model_epoch_0050.pt").write_text("50")
    
    latest = max(ckpt_dir.glob("*.pt"), key=lambda p: p.stat().st_mtime)
    print(f"\nLatest checkpoint: {latest.name}")

# Example 11: Cross-platform path handling
windows_style = Path(r"C:\Users\Name\project\data")
posix_style = Path("/home/user/project/data")
print(f"\nWindows path parts: {windows_style.parts}")
print(f"POSIX path parts:   {posix_style.parts}")

# Using / operator works on both
cross = Path("data") / "train" / "images"
print(f"Cross-platform: {cross}")

# ============================================================
# 7. Common Mistakes
# ============================================================
# MISTAKE: String concatenation for paths
#   bad = "data/" + "train" + "/images"  # Breaks on Windows
# CORRECT:
#   good = Path("data") / "train" / "images"

# MISTAKE: Not using parents=True
#   bad = Path("a/b/c").mkdir()  # FileNotFoundError if a/b missing
# CORRECT:
#   good = Path("a/b/c").mkdir(parents=True, exist_ok=True)

# MISTAKE: resolve() on non-existent path
#   bad = Path("nonexistent").resolve()  # Returns absolute but doesn't check existence
# CORRECT:
#   good = Path("file.txt").resolve(strict=True)  # Raises if missing (3.6+)

# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    import tempfile
    
    # Path construction
    p = Path("a") / "b" / "c"
    assert str(p) == "a/b/c" or str(p) == "a\\b\\c", "Path construction failed"
    
    # Properties
    assert Path("/home/user/file.txt").name == "file.txt"
    assert Path("/home/user/file.txt").stem == "file"
    assert Path("/home/user/file.txt").suffix == ".txt"
    assert Path("/home/user/file.txt").parent == Path("/home/user")
    
    # Resolution
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        real = tmp_path / "real.txt"
        real.write_text("x")
        link = tmp_path / "link.txt"
        link.symlink_to(real)
        assert link.resolve() == real.resolve(), "resolve() should follow symlinks"
        
        # glob/rglob
        (tmp_path / "sub").mkdir()
        (tmp_path / "sub" / "test.txt").write_text("x")
        files = list(tmp_path.rglob("*.txt"))
        assert len(files) == 1, "rglob should find nested files"
        assert files[0].name == "test.txt"
        
        # read/write
        f = tmp_path / "data.json"
        f.write_text('{"key": "value"}')
        assert f.read_text() == '{"key": "value"}'
        
        # mkdir parents
        deep = tmp_path / "a" / "b" / "c"
        deep.mkdir(parents=True, exist_ok=True)
        assert deep.is_dir()
        
        # cross-platform path building
        cross = Path("models") / "bert" / "checkpoint.pt"
        assert "models" in str(cross) and "bert" in str(cross) and "checkpoint.pt" in str(cross)
    
    print("[OK] 42-pathlib: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Use Path and / operator for cross-platform paths")
        print("2. glob/rglob for directory traversal")
        print("3. read_text/write_text for simple I/O")
        print("4. mkdir(parents=True, exist_ok=True) for safe dir creation")
        print("5. resolve() for absolute paths with symlink resolution")
        _verify()