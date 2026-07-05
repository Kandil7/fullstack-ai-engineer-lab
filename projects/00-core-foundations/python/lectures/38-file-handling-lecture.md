# File Handling in Python

## Topic 38: Working with Files and Directories

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Open, read, write, and close files
2. Use context managers (`with` statement)
3. Work with different file modes
4. Handle CSV, JSON, and text files
5. Perform file operations (copy, move, delete)
6. Work with paths using `pathlib`

---

## 1. Opening Files

### Basic Syntax

```python
# open(filename, mode)
file = open("example.txt", "r")
content = file.read()
file.close()  # Always close when done!
```

### File Modes

| Mode | Description |
|------|-------------|
| `'r'` | Read (default) |
| `'w'` | Write (creates/overwrites) |
| `'a'` | Append (creates/adds to end) |
| `'x'` | Create (fails if exists) |
| `'rb'` | Read binary |
| `'wb'` | Write binary |
| `'r+'` | Read and write |
| `'w+'` | Write and read (truncates) |

---

## 2. Context Managers (`with` Statement)

**Always use `with`** - it automatically closes the file.

```python
# GOOD - auto-closes file
with open("example.txt", "r") as file:
    content = file.read()

# File is now closed automatically
```

### Multiple Files

```python
with open("input.txt", "r") as infile, open("output.txt", "w") as outfile:
    content = infile.read()
    outfile.write(content.upper())
```

---

## 3. Reading Files

### Reading Entire File

```python
with open("example.txt", "r") as file:
    content = file.read()  # Returns string
    print(content)
```

### Reading Line by Line

```python
# Method 1: iter() - memory efficient
with open("large.txt", "r") as file:
    for line in file:
        print(line.strip())  # strip() removes newline

# Method 2: readlines() - returns list
with open("example.txt", "r") as file:
    lines = file.readlines()  # List of strings
    for line in lines:
        print(line.strip())
```

### Reading Specific Amount

```python
with open("example.txt", "r") as file:
    chunk = file.read(100)  # Read first 100 characters
    print(chunk)
```

---

## 4. Writing Files

### Writing Text

```python
# 'w' mode - overwrites existing file
with open("output.txt", "w") as file:
    file.write("Hello, World!\n")
    file.write("Second line\n")

# 'a' mode - appends to existing file
with open("log.txt", "a") as file:
    file.write("New log entry\n")

# writelines() - write list of strings
lines = ["Line 1\n", "Line 2\n", "Line 3\n"]
with open("output.txt", "w") as file:
    file.writelines(lines)
```

### Using print()

```python
with open("output.txt", "w") as file:
    print("Hello", file=file)
    print("World", file=file)
```

---

## 5. Working with CSV Files

### Reading CSV

```python
import csv

# Method 1: csv.reader
with open("data.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)  # ['name', 'age', 'city']

# Method 2: csv.DictReader
with open("data.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row['name'], row['age'])
```

### Writing CSV

```python
import csv

data = [
    ['name', 'age', 'city'],
    ['Alice', 30, 'New York'],
    ['Bob', 25, 'Boston']
]

with open("output.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)
```

---

## 6. Working with JSON Files

### Reading JSON

```python
import json

with open("data.json", "r") as file:
    data = json.load(file)  # Parse JSON to dict
    print(data['name'])
```

### Writing JSON

```python
import json

data = {
    "name": "Alice",
    "age": 30,
    "hobbies": ["reading", "coding"]
}

with open("output.json", "w") as file:
    json.dump(data, file, indent=4)  # Write with formatting
```

---

## 7. File Operations

### Checking File Existence

```python
import os
import pathlib

# os.path
if os.path.exists("file.txt"):
    print("File exists")

# pathlib (modern approach)
from pathlib import Path
path = Path("file.txt")
if path.exists():
    print("File exists")
```

### Getting File Info

```python
import os

# File size
size = os.path.getsize("file.txt")
print(f"Size: {size} bytes")

# File modification time
mtime = os.path.getmtime("file.txt")

# Using pathlib
from pathlib import Path
path = Path("file.txt")
print(f"Size: {path.stat().st_size}")
print(f"Exists: {path.exists()}")
```

### Copying Files

```python
import shutil

# Copy file
shutil.copy("source.txt", "destination.txt")

# Copy with metadata
shutil.copy2("source.txt", "destination.txt")
```

### Moving Files

```python
import shutil

shutil.move("old_location.txt", "new_location.txt")
```

### Deleting Files

```python
import os
from pathlib import Path

# os.remove()
os.remove("file.txt")

# pathlib
Path("file.txt").unlink()

# Delete directory
os.rmdir("empty_dir")
shutil.rmtree("directory_with_contents")
```

---

## 8. Working with Paths (pathlib)

### Creating Paths

```python
from pathlib import Path

# Different ways to create paths
path = Path("folder/file.txt")
path = Path("folder") / "file.txt"  # / operator joins paths

# Get current directory
cwd = Path.cwd()

# Get home directory
home = Path.home()
```

### Path Properties

```python
from pathlib import Path

path = Path("/home/user/documents/file.txt")

print(path.name)      # file.txt
print(path.stem)      # file
print(path.suffix)    # .txt
print(path.parent)    # /home/user/documents
print(path.is_file()) # True
print(path.is_dir())  # False
```

### Iterating Directory

```python
from pathlib import Path

# List all files in directory
path = Path("my_folder")
for item in path.iterdir():
    print(item.name)

# Glob pattern
txt_files = path.glob("*.txt")  # All .txt files
py_files = path.rglob("*.py")   # Recursive search
```

---

## 9. Common Mistakes to Avoid

### 1. Forgetting to Close Files

```python
# BAD - file might not close
file = open("data.txt", "r")
content = file.read()

# GOOD - use context manager
with open("data.txt", "r") as file:
    content = file.read()
```

### 2. Not Handling Encoding

```python
# BAD - encoding might cause issues
with open("data.txt", "r") as file:
    content = file.read()

# GOOD - specify encoding
with open("data.txt", "r", encoding="utf-8") as file:
    content = file.read()
```

### 3. Not Handling Newlines

```python
# BAD - extra newlines on Windows
with open("output.txt", "w") as file:
    file.write("line\n")

# GOOD - use newline parameter
with open("output.txt", "w", newline='') as file:
    file.write("line\n")
```

---

## 10. Best Practices

1. **Always use `with`** statement for file handling
2. **Specify encoding** (`encoding="utf-8"`)
3. **Handle exceptions** for file operations
4. **Use `pathlib`** for modern path handling
5. **Use appropriate modes** (don't use `'w'` when you mean `'a'`)
6. **Close binary files** explicitly if not using `with`
7. **Test for existence** before operations

---

## 11. Practice Exercises

### Exercise 1: Log File Analyzer

```python
from collections import Counter
from pathlib import Path

def analyze_log(log_file):
    """Analyze a log file and return statistics."""
    error_count = 0
    warning_count = 0
    level_counter = Counter()
    
    with open(log_file, "r") as file:
        for line in file:
            if "ERROR" in line:
                error_count += 1
                level_counter["ERROR"] += 1
            elif "WARNING" in line:
                warning_count += 1
                level_counter["WARNING"] += 1
    
    return {
        "total_errors": error_count,
        "total_warnings": warning_count,
        "levels": dict(level_counter)
    }

# Test
# stats = analyze_log("app.log")
# print(stats)
```

### Exercise 2: File Organizer

```python
from pathlib import Path
import shutil

def organize_files(source_dir, dest_dir):
    """Organize files by extension."""
    source = Path(source_dir)
    dest = Path(dest_dir)
    
    for file in source.iterdir():
        if file.is_file():
            ext = file.suffix[1:] or "no_extension"
            target_dir = dest / ext
            target_dir.mkdir(exist_ok=True)
            shutil.move(str(file), str(target_dir / file.name))

# organize_files("./downloads", "./organized")
```

---

## 12. Summary

| Operation | Function/Method |
|-----------|-----------------|
| **Open file** | `open()`, `Path()` |
| **Read** | `read()`, `readline()`, `readlines()` |
| **Write** | `write()`, `writelines()` |
| **Close** | `close()` (use `with` instead) |
| **Check exists** | `os.path.exists()`, `Path.exists()` |
| **Copy** | `shutil.copy()` |
| **Move** | `shutil.move()` |
| **Delete** | `os.remove()`, `Path.unlink()` |
| **CSV** | `csv.reader()`, `csv.writer()` |
| **JSON** | `json.load()`, `json.dump()` |

---

## Next Steps

- Learn about memory-mapped files
- Study async file operations
- Explore database file handling
