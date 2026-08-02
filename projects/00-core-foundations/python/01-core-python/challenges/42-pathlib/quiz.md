# 42: pathlib Quiz

## Topic Overview
Tests your understanding of `pathlib` for cross-platform path handling in Python.

## Instructions
- 20 questions, 4 options each
- Suggested time: 25 minutes
- 1 point per correct answer

## Questions

### Question 1
**What is the correct way to join path components using `pathlib`?**

A) `Path("data") + "train" + "images.jpg"`
B) `Path("data") / "train" / "images.jpg"`
C) `Path.join("data", "train", "images.jpg")`
D) `os.path.join(Path("data"), "train", "images.jpg")`

**Difficulty:** Easy

### Question 2
**What does `Path("data/train/../models").resolve()` return on a POSIX system where `data` is a symlink to `/mnt/data`?**

A) `/mnt/data/models`
B) `/home/user/project/data/../models`
C) `/home/user/project/models`
D) `/mnt/data/train/../models`

**Difficulty:** Medium

### Question 3
**Which method creates a directory and all necessary parent directories without raising an error if the directory already exists?**

A) `Path("a/b/c").mkdir()`
B) `Path("a/b/c").mkdir(parents=True)`
C) `Path("a/b/c").mkdir(parents=True, exist_ok=True)`
D) `Path("a/b/c").mkdir(exist_ok=True)`

**Difficulty:** Easy

### Question 4
**What is the difference between `Path.absolute()` and `Path.resolve()`?**

A) No difference — they are aliases
B) `resolve()` follows symlinks; `absolute()` does not
C) `absolute()` follows symlinks; `resolve()` does not
D) `resolve()` normalizes `..` components; `absolute()` does not

**Difficulty:** Medium

### Question 5
**What does `Path("archive.tar.gz").stem` return?**

A) `"archive"`
B) `"archive.tar"`
C) `"archive.tar.gz"`
D) `".gz"`

**Difficulty:** Easy

### Question 6
**What does `Path("archive.tar.gz").suffixes` return?**

A) `[".gz"]`
B) `[".tar", ".gz"]`
C) `[".tar.gz"]`
D) `[".archive", ".tar", ".gz"]`

**Difficulty:** Easy

### Question 7
**Which method efficiently iterates over all files matching a pattern recursively?**

A) `Path("data").glob("**/*.jpg")`
B) `Path("data").rglob("*.jpg")`
C) `Path("data").iterdir().filter("*.jpg")`
D) `Path("data").walk("*.jpg")`

**Difficulty:** Easy

### Question 8
**What does `Path("file.txt").write_text("hello")` do if the file already exists?**

A) Appends "hello" to the file
B) Raises `FileExistsError`
C) Overwrites the file with "hello"
D) Raises `PermissionError`

**Difficulty:** Easy

### Question 9
**Which method reads a file as bytes without decoding?**

A) `Path("model.bin").read_text()`
B) `Path("model.bin").read_bytes()`
C) `Path("model.bin").read()`
D) `Path("model.bin").read_binary()`

**Difficulty:** Easy

### Question 10
**What is the output of this code?**
```python
from pathlib import Path
p = Path("a/b/c")
print(p.parts)
```

A) `("a", "b", "c")`
B) `("a/b/c",)`
C) `("a", "b/c")`
D) `("a/", "b/", "c")`

**Difficulty:** Medium

### Question 11
**What does `Path("data").iterdir()` return?**

A) List of all files in `data/`
B) Generator of `Path` objects for direct children
C) List of all files recursively
D) Generator of strings

**Difficulty:** Easy

### Question 12
**Which code correctly finds the latest `.pt` checkpoint by modification time?**

A) `max(Path("ckpts").glob("*.pt"), key=lambda p: p.stat().st_size)`
B) `max(Path("ckpts").glob("*.pt"), key=lambda p: p.stat().st_mtime)`
C) `sorted(Path("ckpts").glob("*.pt"), key=lambda p: p.stat().st_mtime)[0]`
D) `Path("ckpts").glob("*.pt").latest()`

**Difficulty:** Medium

### Question 12
**What is the correct way to handle paths from user input for security?**

A) `Path(user_input).absolute()`
B) `Path(user_input).resolve(strict=True)`
C) `Path(user_input).resolve()`
D) `str(Path(user_input))`

**Difficulty:** Hard

### Question 13
**What does `Path("archive.tar.gz").stem` return?**

A) `"archive"`
B) `"archive.tar"`
C) `"archive.tar.gz"`
D) `".gz"`

**Difficulty:** Easy

### Question 14
**What does `Path("a/b/c").parents` return?**

A) `Path("a/b")`
B) `[Path("a/b"), Path("a"), Path(".")]`
C) `["a/b", "a", "."]`
D) Generator of parent paths

**Difficulty:** Medium

### Question 15
**Which pattern correctly builds a cross-platform model checkpoint path?**

A) `"models/" + name + "/epoch_" + str(epoch) + ".pt"`
B) `Path("models") / name / f"epoch_{epoch:04d}.pt"`
C) `os.path.join("models", name, f"epoch_{epoch:04d}.pt")`
D) `f"models/{name}/epoch_{epoch:04d}.pt"`

**Difficulty:** Easy

### Question 16
**What happens when `Path("missing.txt").resolve(strict=True)` is called on Python 3.6+ if the file doesn't exist?**

A) Returns absolute path anyway
B) Returns `None`
C) Raises `FileNotFoundError`
D) Returns empty Path

**Difficulty:** Medium

### Question 17
**What is the time complexity of `Path("data").rglob("*.jpg")` converted to a list?**

A) O(1)
B) O(n) where n = matching files
C) O(n log n) where n = total files
D) O(d) where d = directory depth

**Difficulty:** Medium

### Question 18
**Which method efficiently streams directory contents without materializing the full list?**

A) `list(Path("data").glob("*"))`
B) `Path("data").iterdir()`
C) `Path("data").rglob("*")`
D) `os.listdir("data")`

**Difficulty:** Easy

### Question 19
**What is the correct way to read a JSON config file with pathlib?**

A) `json.loads(Path("config.json").read_text())`
B) `Path("config.json").read_json()`
C) `json.load(open(Path("config.json")))`
D) Both A and C are correct

**Difficulty:** Easy

### Question 20
**What breaks first when scaling `rglob("*")` to 10⁹ files?**

A) Python memory for the list
B) Filesystem inode limits
C) Single directory entry limits
D) stat() syscall overhead
E) All of the above

**Difficulty:** Hard

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Expert — you own pathlib
- 15-17: Proficient — minor gaps
- 12-14: Competent — review weak areas
- Below 12: Needs study — re-read lecture and glossary

---

## Answer Key

1. **B** — The `/` operator is the pathlib idiom for joining paths.
2. **A** — `resolve()` follows symlinks and normalizes; `/mnt/data/models` is canonical.
3. **C** — `parents=True` creates intermediate dirs; `exist_ok=True` suppresses error on existing.
4. **B** — `resolve()` follows symlinks; `absolute()` does not. Both normalize `.` but only `resolve()` normalizes `..`.
5. **B** — `stem` removes only the final suffix; `archive.tar.gz` → `archive.tar`.
6. **B** — `suffixes` returns all suffixes: `[".tar", ".gz"]`.
7. **B** — `rglob()` is the recursive glob method.
8. **C** — `write_text` overwrites by default (like `open(..., 'w')`).
9. **B** — `read_bytes()` returns `bytes`; `read_text()` decodes to `str`.
10. **A** — `parts` returns normalized components as tuple.
11. **B** — `iterdir()` yields `Path` objects for direct children only.
12. **B** — `st_mtime` is modification time; `max` with this key finds latest.
12. **C** — `resolve()` without strict=True returns absolute path; with `strict=True` it validates existence (Python 3.6+). `resolve()` canonicalizes user input.
13. **B** — `stem` removes only last suffix: `archive.tar.gz` → `archive.tar`.
14. **D** — `parents` is an immutable sequence (generator-like) of all ancestors.
15. **B** — Uses `/` operator and f-string; cross-platform and clean.
16. **C** — `strict=True` makes `resolve()` raise `FileNotFoundError` if path doesn't exist (3.6+).
17. **B** — Must visit each matching file once to collect into list.
18. **B** — `iterdir()` is a lazy iterator; others materialize lists.
19. **D** — Both work; A uses pathlib convenience, C uses stdlib with pathlib object.
20. **E** — At 10⁹: inode exhaustion, directory entry limits, stat() syscall storm all hit.

---

*Quiz for [02-pathlib-lecture.md](02-pathlib-lecture.md) · Glossary: [02-pathlib-glossary.md](02-pathlib-glossary.md)*