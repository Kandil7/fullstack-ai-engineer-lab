# File Handling Glossary

## Topic 38: Quick Reference Guide

---

## Glossary Terms

### C

#### Close
**Definition:** Release file resources after operations.
```python
file = open("data.txt", "r")
content = file.read()
file.close()  # Release resources
```
**Related:** Context manager, `with` statement

#### Context Manager
**Definition:** Object that manages file lifecycle (auto-close).
```python
with open("data.txt") as f:
    content = f.read()
# File automatically closed
```
**Related:** `with` statement, `__enter__`, `__exit__`

#### CSV (Comma-Separated Values)
**Definition:** Plain text format for tabular data.
```python
import csv
with open("data.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
```
**Related:** `csv` module, `csv.reader`, `csv.writer`

---

### D

#### Directory
**Definition:** Folder containing files and subdirectories.
```python
from pathlib import Path
Path("my_dir").mkdir(exist_ok=True)
```
**Related:** Folder, path, `mkdir()`

---

### E

#### Encoding
**Definition:** Character encoding for text files (e.g., UTF-8).
```python
with open("data.txt", encoding="utf-8") as f:
    content = f.read()
```
**Related:** UTF-8, ASCII, character set

---

### F

#### File Mode
**Definition:** Permission/type when opening a file ('r', 'w', 'a', etc.).
```python
open("file.txt", "r")   # Read mode
open("file.txt", "w")   # Write mode
open("file.txt", "a")   # Append mode
open("file.txt", "x")   # Create mode
```
**Related:** Read, write, append, binary

---

### J

#### JSON (JavaScript Object Notation)
**Definition:** Lightweight data interchange format.
```python
import json
data = {"name": "Alice"}
with open("data.json", "w") as f:
    json.dump(data, f)
```
**Related:** `json` module, `json.load()`, `json.dump()`

---

### P

#### Path
**Definition:** Location of file/directory in filesystem.
```python
from pathlib import Path
p = Path("/home/user/file.txt")
```
**Related:** Absolute path, relative path, `pathlib`

#### pathlib
**Definition:** Modern Python module for path operations.
```python
from pathlib import Path
p = Path("folder/file.txt")
print(p.exists())
```
**Related:** Path, os.path, modern path handling

---

### R

#### Read
**Definition:** Get content from a file.
```python
with open("data.txt") as f:
    content = f.read()      # Entire file
    line = f.readline()     # One line
    lines = f.readlines()   # List of lines
```
**Related:** Read modes, file reading

---

### W

#### Write
**Definition:** Put content into a file.
```python
with open("output.txt", "w") as f:
    f.write("Hello\n")
    f.writelines(["Line 1\n", "Line 2\n"])
```
**Related:** Write modes, file writing

---

## Quick Reference Table

| Term | Syntax/Function | Description |
|------|-----------------|-------------|
| **open()** | `open(file, mode)` | Open a file |
| **with** | `with open(...) as f:` | Context manager |
| **read()** | `f.read()` | Read entire file |
| **readline()** | `f.readline()` | Read one line |
| **readlines()** | `f.readlines()` | Read all lines |
| **write()** | `f.write(text)` | Write text |
| **writelines()** | `f.writelines(list)` | Write list of strings |
| **close()** | `f.close()` | Close file |
| **Path** | `Path("path")` | Modern path object |
| **exists()** | `p.exists()` | Check existence |
| **glob()** | `p.glob("*.txt")` | Pattern matching |
| **iterdir()** | `p.iterdir()` | List directory contents |
| **csv.reader** | `csv.reader(f)` | Read CSV |
| **csv.writer** | `csv.writer(f)` | Write CSV |
| **json.load** | `json.load(f)` | Parse JSON |
| **json.dump** | `json.dump(obj, f)` | Write JSON |

---

## File Modes

| Mode | Name | Description |
|------|------|-------------|
| `'r'` | Read | Read only (default) |
| `'w'` | Write | Write only (truncates) |
| `'a'` | Append | Write to end |
| `'x'` | Create | Create new (fails if exists) |
| `'r+'` | Read+Write | Read and write |
| `'w+'` | Write+Read | Write and read (truncates) |
| `'rb'` | Read Binary | Binary read |
| `'wb'` | Write Binary | Binary write |

---

## Path Operations

### Create
```python
from pathlib import Path
Path("dir").mkdir(exist_ok=True)
Path("file.txt").touch()
```

### Delete
```python
Path("file.txt").unlink()
Path("dir").rmdir()
```

### Move/Copy
```python
import shutil
shutil.move("src", "dst")
shutil.copy("src", "dst")
```

### Info
```python
p = Path("file.txt")
p.exists()    # True/False
p.is_file()   # True/False
p.is_dir()    # True/False
p.stat()      # File stats
p.name        # Filename
p.stem        # Name without extension
p.suffix      # Extension
p.parent      # Parent directory
```
