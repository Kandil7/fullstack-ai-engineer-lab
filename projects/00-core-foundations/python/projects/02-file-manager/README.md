# 📁 Project 02: CLI File Manager

A full-featured command-line file manager with navigation, CRUD operations, search, and more.

## What This Project Practices

| Skill | Phase | Details |
|-------|-------|---------|
| File Handling | Phase 1 | Read/write/delete files |
| `os` Module | Phase 1 | Path operations, stat |
| `pathlib` | Phase 1 | Modern path handling |
| `shutil` | Phase 1 | Copy, move, rmtree |
| `fnmatch` | Phase 1 | Pattern matching |
| Classes & OOP | Phase 1 | `FileManager` class |
| Error Handling | Phase 1 | Specific exception types |
| CLI Arguments | Phase 1 | Command parsing |
| Recursion | Phase 1 | `tree()` and `find_text()` |
| String Formatting | Phase 1 | Column-aligned output |
| Type Hints | Phase 2 | Function annotations |
| Generators | Phase 2 | `rglob()` for iteration |
| Context Managers | Phase 2 | `with open()` pattern |

## How to Run

```bash
python projects/02-file-manager/main.py
```

## Features

- **Navigation**: `pwd`, `cd`, `ls`, `tree`
- **File CRUD**: `read`, `write`, `append`, `mkfile`, `rm`
- **Directory Ops**: `mkdir`, `rmdir`, `rm -r`
- **Manipulation**: `cp`, `mv`, `rename`
- **Search**: `find` (glob), `grep` (text search)
- **Info**: `info` (detailed metadata), `size`
- **Display**: `hidden` (toggle hidden files)

## Example Session

```
📁 python> ls
  📄 01-introduction.py       2.1 KB  2026-07-15 10:00
  📄 02-get-started.py        1.8 KB  2026-07-15 10:00
  📁 01-core-python/          4.0 KB  2026-07-15 11:00

  3 item(s)

📁 python> info run_smoke_tests.py
  name: run_smoke_tests.py
  type: file
  size: 6278
  size_human: 6.1 KB
  modified: 2026-07-15 11:30:00
```
