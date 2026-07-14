# Context Managers Glossary

## Quick Reference Table

| Term | One-Line Definition |
|------|-------------------|
| Context Manager | Object defining runtime context with `__enter__`/`__exit__` |
| `with` statement | Syntax for automatic resource management |
| `__enter__` | Method called when entering context |
| `__exit__` | Method called when exiting context |
| `contextmanager` | Decorator for function-based context managers |
| `ExitStack` | Manages multiple context managers dynamically |
| `suppress` | Context manager that ignores specified exceptions |
| `redirect_stdout` | Redirects stdout to another file object |
| `nullcontext` | No-op context manager for optional contexts |
| `asynccontextmanager` | Async version of `contextmanager` |
| Resource Management | Pattern for acquiring and releasing resources |
| Exception Suppression | Returning `True` from `__exit__` to hide exceptions |
| Cleanup Code | Code in `finally` or `__exit__` ensuring resource release |
| Context Nesting | Using multiple `with` statements together |
| Generator-Based | Using `yield` in `@contextmanager` decorated functions |

---

## Detailed Definitions

### `__enter__`

**Definition**: The special method called when entering a `with` block. It sets up the context and returns the value bound to the `as` variable.

**Example**:
```python
class Timer:
    def __init__(self):
        self.start = None
    
    def __enter__(self):
        import time
        self.start = time.perf_counter()
        return self  # Bound to 'as' variable
    
    def __exit__(self, *args):
        import time
        elapsed = time.perf_counter() - self.start
        print(f"Elapsed: {elapsed:.4f}s")

with Timer() as t:
    # t is the return value of __enter__
    sum(range(1000000))
```

**Related**: `__exit__`, Context Manager Protocol, `with` Statement

---

### `__exit__`

**Definition**: The special method called when exiting a `with` block (even if an exception occurs). Receives exception information and can suppress exceptions by returning `True`.

**Parameters**:
- `exc_type`: The exception class (or `None`)
- `exc_val`: The exception instance (or `None`)
- `exc_tb`: The traceback object (or `None`)

**Example**:
```python
class SafeFile:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        
        if exc_type is not None:
            print(f"Error: {exc_val}")
            return False  # Don't suppress exception
        
        return False

with SafeFile("test.txt", "w") as f:
    f.write("Hello")
```

**Related**: `__enter__`, Exception Handling, Exception Suppression

---

### `asynccontextmanager`

**Definition**: The async version of `contextmanager`, used for creating asynchronous context managers with `async with` syntax.

**Example**:
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def async_resource(name):
    print(f"Acquiring {name}")
    resource = await acquire_resource(name)
    try:
        yield resource
    finally:
        await resource.release()
        print(f"Released {name}")

async def main():
    async with async_resource("database") as conn:
        await conn.query("SELECT ...")
```

**Related**: `contextmanager`, Async/Await, Asynchronous Resource Management

---

### Cleanup Code

**Definition**: Code that releases resources, closes connections, or restores state when a context is exited. In `@contextmanager` functions, this goes in the `finally` block.

**Example**:
```python
from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    resource = acquire(name)
    try:
        yield resource
    finally:
        # This is cleanup code - always runs
        resource.close()
        print(f"Released {name}")

# Even if exception occurs, cleanup runs
with managed_resource("lock") as r:
    raise ValueError("Something went wrong")
# "Released lock" is printed, then ValueError propagates
```

**Related**: `finally`, Resource Management, `__exit__`

---

### Context Nesting

**Definition**: Using multiple `with` statements together, either on separate lines or combined in a single `with` statement.

**Example**:
```python
# Separate lines
with open("input.txt") as infile:
    with open("output.txt", "w") as outfile:
        outfile.write(infile.read())

# Single with (Python 3.1+)
with open("input.txt") as infile, open("output.txt", "w") as outfile:
    outfile.write(infile.read())

# Parenthesized (Python 3.10+)
with (
    open("input.txt") as infile,
    open("output.txt", "w") as outfile,
):
    outfile.write(infile.read())
```

**Related**: `with` Statement, Multiple Context Managers

---

### `contextmanager`

**Definition**: A decorator from `contextlib` that converts a generator function into a context manager. The generator should `yield` the value to be bound to `as`, with setup before `yield` and cleanup in `finally`.

**Example**:
```python
from contextlib import contextmanager

@contextmanager
def temporary_directory():
    import tempfile
    import shutil
    
    path = tempfile.mkdtemp()
    try:
        yield path  # Bound to 'as' variable
    finally:
        shutil.rmtree(path)  # Cleanup in finally

with temporary_directory() as tmpdir:
    # Use tmpdir for temporary files
    pass
# tmpdir is automatically cleaned up
```

**Related**: `@contextmanager`, Generator-Based Context Manager, `yield`

---

### `ExitStack`

**Definition**: A context manager from `contextlib` that manages a dynamic number of other context managers, useful when the number of contexts isn't known at compile time.

**Example**:
```python
from contextlib import ExitStack

def process_many_files(filenames):
    with ExitStack() as stack:
        # Dynamically enter contexts
        files = [
            stack.enter_context(open(fn, "r"))
            for fn in filenames
        ]
        
        # All files are open
        for f in files:
            print(f.read()[:100])
        
        # All files closed when ExitStack exits

# Or use callback for custom cleanup
with ExitStack() as stack:
    conn = stack.enter_context(get_connection())
    lock = stack.enter_context(acquire_lock())
    stack.callback(release_resource, resource)
```

**Related**: Dynamic Context Management, `enter_context`, `callback`

---

### Exception Suppression

**Definition**: The act of preventing an exception from propagating by returning `True` from `__exit__`. Should be used sparingly and only for expected exceptions.

**Example**:
```python
class ExpectedExceptionSuppressor:
    def __init__(self, *exceptions):
        self.exceptions = exceptions
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and issubclass(exc_type, self.exceptions):
            print(f"Suppressing: {exc_type.__name__}")
            return True  # Suppress the exception
        return False  # Propagate all others

# Usage
with ExpectedExceptionSuppressor(ZeroDivisionError):
    x = 1 / 0  # ZeroDivisionError is suppressed

print("Continues here")  # This runs
```

**Related**: `__exit__` Return Value, Exception Handling, `contextlib.suppress`

---

### `nullcontext`

**Definition**: A no-op context manager from `contextlib` that does nothing. Useful as a default or placeholder when a context manager is optional.

**Example**:
```python
from contextlib import nullcontext

def process_data(data, lock=None):
    cm = lock if lock is not None else nullcontext()
    
    with cm:
        # Code runs the same regardless
        process(data)

# In testing
with nullcontext() as ctx:
    pass  # Does nothing, ctx is None
```

**Related**: Optional Context Manager, Testing Patterns

---

### `redirect_stderr`

**Definition**: A context manager from `contextlib` that redirects stderr to a specified file object.

**Example**:
```python
import sys
from contextlib import redirect_stderr
import io

f = io.StringIO()
with redirect_stderr(f):
    print("Error message", file=sys.stderr)
    # No error appears on console

error_text = f.getvalue()
print(f"Captured: {error_text!r}")
```

**Related**: `redirect_stdout`, Output Capture, Testing

---

### `redirect_stdout`

**Definition**: A context manager from `contextlib` that redirects stdout to a specified file object, capturing all print output.

**Example**:
```python
from contextlib import redirect_stdout
import io

f = io.StringIO()
with redirect_stdout(f):
    print("Hello, World!")
    print("This is captured")

output = f.getvalue()
print(f"Captured output:\n{output}")
```

**Related**: `redirect_stderr`, Output Capture, Testing

---

### `suppress`

**Definition**: A context manager from `contextlib` that suppresses specified exceptions, allowing code to continue executing.

**Example**:
```python
from contextlib import suppress

# Suppress FileNotFoundError
with suppress(FileNotFoundError):
    os.remove("nonexistent.txt")

# Suppress multiple exceptions
with suppress(ValueError, TypeError, KeyError):
    result = int("not_a_number")

# More explicit than try/except pass
with suppress(StopIteration):
    value = next(iter([]))
```

**Related**: Exception Suppression, `contextlib`, Clean Code

---

### `with` Statement

**Definition**: A Python statement that wraps a block of code with a context manager, automatically calling `__enter__` at the start and `__exit__` at the end.

**Example**:
```python
# Basic usage
with open("file.txt") as f:
    content = f.read()
# File is automatically closed

# Multiple context managers
with open("in.txt") as fin, open("out.txt", "w") as fout:
    fout.write(fin.read())

# Exception handling - __exit__ still called
with managed_resource() as r:
    raise ValueError("Error")
# Cleanup still happens despite exception
```

**Related**: Context Manager, `__enter__`, `__exit__`, Resource Management

---

### Resource Management

**Definition**: The practice of acquiring resources (files, connections, locks) when needed and releasing them when done, ensuring no leaks occur even if exceptions happen.

**Example**:
```python
# Manual (error-prone)
resource = acquire()
try:
    use(resource)
finally:
    release(resource)

# With context manager (safe)
with managed_resource() as resource:
    use(resource)
# Automatic cleanup
```

**Related**: Context Manager, `with` Statement, Cleanup Code

---

### `@contextmanager` Decorator

**Definition**: See `contextmanager`. The decorator that transforms a generator function into a context manager, where `yield` separates setup from cleanup.

**Example**:
```python
from contextlib import contextmanager

@contextmanager
def timer(label="Timer"):
    import time
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label}: {elapsed:.4f}s")

# Can also be used as a decorator!
@timer("Function")
def slow_function():
    import time
    time.sleep(0.1)
```

**Related**: Context Manager, Generator, `yield`, Cleanup Code

---

### `enter_context`

**Definition**: A method on `ExitStack` that enters a context manager and registers its `__exit__` method for cleanup when the `ExitStack` exits.

**Example**:
```python
from contextlib import ExitStack

with ExitStack() as stack:
    # Enter multiple contexts dynamically
    db = stack.enter_context(get_database_connection())
    cache = stack.enter_context(get_cache_connection())
    
    # Both cleaned up when ExitStack exits
    db.query("SELECT ...")
    cache.get("key")
```

**Related**: `ExitStack`, Dynamic Context Management

---

### Generator-Based Context Manager

**Definition**: A context manager created using a generator function decorated with `@contextmanager`, where setup code is before `yield` and cleanup code is in the `finally` block after `yield`.

**Example**:
```python
from contextlib import contextmanager

@contextmanager
def managed_connection(url):
    # Setup (before yield)
    conn = connect(url)
    print(f"Connected to {url}")
    
    try:
        yield conn  # Value for 'as' variable
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        raise
    finally:
        # Cleanup (after yield, in finally)
        conn.close()
        print("Disconnected")
```

**Related**: `@contextmanager`, Generator, `yield`, Cleanup Code

---

### `callback`

**Definition**: A method on `ExitStack` that registers a callable to be called when the `ExitStack` exits, useful for custom cleanup logic.

**Example**:
```python
from contextlib import ExitStack

def cleanup_temp_file(path):
    import os
    if os.path.exists(path):
        os.remove(path)
        print(f"Removed {path}")

with ExitStack() as stack:
    # Register cleanup callback
    stack.callback(cleanup_temp_file, "/tmp/data.txt")
    
    # Do work
    with open("/tmp/data.txt", "w") as f:
        f.write("temporary data")
    
    # cleanup_temp_file called when ExitStack exits
```

**Related**: `ExitStack`, Cleanup Code, Destructor Pattern

---
