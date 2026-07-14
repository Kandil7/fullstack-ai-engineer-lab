# Advanced Python Lecture 03: Context Managers

## Topic Overview

Context managers provide a clean, Pythonic way to manage resources — opening and closing files, acquiring and releasing locks, connecting and disconnecting from databases, and any scenario where setup and teardown logic must reliably execute. The `with` statement ensures cleanup happens even when exceptions occur, making code safer and more readable.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand the context manager protocol (`__enter__` and `__exit__`)
2. Create class-based context managers
3. Build function-based context managers using `contextlib.contextmanager`
4. Use `contextlib` utilities (`suppress`, `redirect_stdout`, `ExitStack`)
5. Handle exceptions within context managers
6. Create reusable context managers for common patterns
7. Implement nested and composed context managers
8. Apply context managers to AI engineering workflows
9. Debug context manager issues
10. Follow best practices for resource management

---

## 1. The Context Manager Protocol

### What is a Context Manager?

A **context manager** is an object that defines the runtime context to be established when entering a code block and the cleanup when exiting. It implements two methods:

- `__enter__()`: Sets up the context; returns a value bound to the `as` variable
- `__exit__(exc_type, exc_val, exc_tb)`: Cleans up the context; handles exceptions

```python
class FileManager:
    """Basic context manager for file operations."""
    
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        print(f"Opening {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Closing {self.filename}")
        if self.file:
            self.file.close()
        # Return False to propagate exceptions, True to suppress
        return False

# Usage
with FileManager("test.txt", "w") as f:
    f.write("Hello, World!")
# Output:
# Opening test.txt
# Closing test.txt
```

### The `__exit__` Method Parameters

```python
class ExceptionAwareManager:
    def __enter__(self):
        print("Entering context")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        exc_type:  Exception class (None if no exception)
        exc_val:   Exception instance (None if no exception)
        exc_tb:    Traceback object (None if no exception)
        """
        if exc_type is not None:
            print(f"Exception occurred: {exc_type.__name__}: {exc_val}")
            print(f"Traceback: {exc_tb}")
            return False  # Propagate the exception
        print("No exception occurred")
        return False

with ExceptionAwareManager():
    print("Doing work")
# Output:
# Entering context
# Doing work
# No exception occurred
```

---

## 2. Class-Based Context Managers

### Resource Management Pattern

```python
import time

class Timer:
    """Context manager that times code execution."""
    
    def __init__(self, label="Block"):
        self.label = label
        self.start = None
        self.elapsed = None
    
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        print(f"{self.label} took {self.elapsed:.4f}s")
        return False  # Don't suppress exceptions

# Usage
with Timer("Data processing"):
    total = sum(i ** 2 for i in range(1_000_000))
# "Data processing took 0.1234s"
```

### Database Connection Manager

```python
class DatabaseConnection:
    """Context manager for database connections."""
    
    def __init__(self, host, port, database):
        self.host = host
        self.port = port
        self.database = database
        self.connection = None
    
    def __enter__(self):
        print(f"Connecting to {self.host}:{self.port}/{self.database}")
        # Simulate connection
        self.connection = {
            "host": self.host,
            "port": self.port,
            "database": self.database,
            "connected": True
        }
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            print(f"Disconnecting from {self.database}")
            self.connection["connected"] = False
            self.connection = None
        
        if exc_type is not None:
            print(f"Error: {exc_val}")
            # Rollback on error
            return False  # Propagate exception
        return False

# Usage
with DatabaseConnection("localhost", 5432, "mydb") as conn:
    print(f"Connected: {conn['connected']}")
    # Perform database operations
    if some_error:
        raise ValueError("Query failed")  # Will trigger __exit__ with exception
```

### Thread Lock Manager

```python
import threading

class ManagedLock:
    """Context manager for thread locks."""
    
    def __init__(self, lock=None):
        self.lock = lock or threading.Lock()
        self.acquired = False
    
    def __enter__(self):
        self.lock.acquire()
        self.acquired = True
        return self.lock
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.acquired:
            self.lock.release()
            self.acquired = False
        return False

# Usage
lock = ManagedLock()
shared_data = []

def worker():
    with lock:
        # Critical section - thread safe
        shared_data.append(threading.current_thread().name)
```

---

## 3. Function-Based Context Managers with `contextmanager`

The `contextlib.contextmanager` decorator allows you to create context managers using generator functions:

```python
from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    """Function-based context manager using yield."""
    print(f"Acquiring {name}")
    resource = {"name": name, "active": True}
    
    try:
        yield resource  # Value bound to 'as' variable
    except Exception as e:
        print(f"Error with {name}: {e}")
        resource["active"] = False
        raise  # Re-raise after cleanup
    finally:
        print(f"Releasing {name}")
        resource["active"] = False

# Usage
with managed_resource("database") as res:
    print(f"Using {res['name']}")
    # Do work
# Output:
# Acquiring database
# Using database
# Releasing database
```

### Exception Handling in `contextmanager`

```python
from contextlib import contextmanager

@contextmanager
def suppress_and_log(*exceptions):
    """Suppress specified exceptions and log them."""
    try:
        yield
    except exceptions as e:
        print(f"Suppressed: {type(e).__name__}: {e}")

# Usage
with suppress_and_log(ZeroDivisionError, ValueError):
    result = 1 / 0  # Prints "Suppressed: ZeroDivisionError: division by zero"
    print(result)

print("Continues normally")
```

### `contextmanager` with Parameters

```python
from contextlib import contextmanager
import time

@contextmanager
def retry_context(max_attempts=3, delay=1):
    """Context manager that retries the block on failure."""
    attempt = 0
    last_exception = None
    
    while attempt < max_attempts:
        try:
            yield attempt
            return  # Success
        except Exception as e:
            last_exception = e
            attempt += 1
            print(f"Attempt {attempt} failed: {e}")
            if attempt < max_attempts:
                time.sleep(delay)
    
    raise last_exception

# Usage
with retry_context(max_attempts=3, delay=0.5) as attempt:
    print(f"Attempt {attempt + 1}")
    if attempt < 2:
        raise ConnectionError("Network error")
```

---

## 4. `contextlib` Utilities

### `contextlib.suppress`

```python
from contextlib import suppress

# Suppress specific exceptions
with suppress(FileNotFoundError):
    os.remove("nonexistent_file.txt")  # No error raised

# Multiple exceptions
with suppress(ValueError, TypeError, KeyError):
    result = int("not_a_number")
```

### `contextlib.redirect_stdout` and `redirect_stderr`

```python
from contextlib import redirect_stdout, redirect_stderr
import io

# Capture stdout
f = io.StringIO()
with redirect_stdout(f):
    print("This goes to the buffer")
    print("So does this")

output = f.getvalue()
print(f"Captured: {output!r}")

# Capture stderr
import sys
f = io.StringIO()
with redirect_stderr(f):
    print("Error message", file=sys.stderr)

error_output = f.getvalue()
```

### `contextlib.ExitStack`

```python
from contextlib import ExitStack

def process_files(filenames):
    """Manage multiple context managers dynamically."""
    with ExitStack() as stack:
        # Dynamically enter contexts
        files = [
            stack.enter_context(open(fn, "r"))
            for fn in filenames
        ]
        
        # All files are open here
        for f in files:
            print(f.read()[:100])
        
        # All files closed automatically when exiting ExitStack

# Usage
process_files(["file1.txt", "file2.txt", "file3.txt"])
```

### `contextlib.nullcontext`

```python
from contextlib import nullcontext

def process_data(data, use_lock=False, lock=None):
    """Optionally use a context manager."""
    cm = lock if use_lock else nullcontext()
    
    with cm:
        # Same code regardless of whether lock is used
        process(data)

# In testing, nullcontext replaces real context managers
with nullcontext():
    pass  # Does nothing
```

### `contextlib.asynccontextmanager`

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def async_database_connection(url):
    """Async context manager for database connections."""
    conn = await create_connection(url)
    try:
        yield conn
    finally:
        await conn.close()

# Usage
async def main():
    async with async_database_connection("postgresql://...") as conn:
        result = await conn.execute("SELECT * FROM users")
```

---

## 5. Advanced Patterns

### Context Manager as a Decorator

```python
from contextlib import contextmanager

@contextmanager
def timer(label="Timer"):
    """Can be used as both context manager and decorator."""
    import time
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label}: {elapsed:.4f}s")

# As context manager
with timer("Sum"):
    total = sum(range(1_000_000))

# As decorator
@timer("Fibonacci")
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

### Nested Context Managers

```python
from contextlib import contextmanager

@contextmanager
def database_connection(url):
    conn = connect(url)
    try:
        yield conn
    finally:
        conn.close()

@contextmanager
def transaction(conn):
    try:
        yield conn
        conn.commit()
    except:
        conn.rollback()
        raise

# Nested usage
with database_connection("postgresql://...") as conn:
    with transaction(conn) as tx:
        tx.execute("INSERT INTO users ...")

# Or using multiple with
with database_connection("postgresql://...") as conn, \
     transaction(conn) as tx:
    tx.execute("INSERT INTO users ...")
```

### Chained Context Managers

```python
from contextlib import contextmanager

@contextmanager
def step1():
    print("Step 1: Setup")
    yield "resource1"
    print("Step 1: Cleanup")

@contextmanager
def step2(resource1):
    print(f"Step 2: Setup with {resource1}")
    yield "resource2"
    print("Step 2: Cleanup")

@contextmanager
def combined():
    with step1() as r1:
        with step2(r1) as r2:
            yield r1, r2

with combined() as (r1, r2):
    print(f"Working with {r1} and {r2}")
```

---

## 6. Context Managers in AI Engineering

### Model Loading and Cleanup

```python
from contextlib import contextmanager
import torch

@contextmanager
def load_model(model_path, device="cuda"):
    """Load a model and ensure cleanup."""
    model = None
    try:
        print(f"Loading model from {model_path}")
        model = torch.load(model_path)
        model.to(device)
        model.eval()
        yield model
    finally:
        if model is not None:
            del model
            torch.cuda.empty_cache()
            print("Model unloaded and GPU memory freed")

# Usage
with load_model("model.pt") as model:
    output = model(input_tensor)
```

### Temporary Directory for Processing

```python
import tempfile
import shutil
from pathlib import Path

@contextmanager
def temporary_workspace(prefix="workspace_"):
    """Create a temporary directory for processing."""
    tmp_dir = tempfile.mkdtemp(prefix=prefix)
    try:
        yield Path(tmp_dir)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

# Usage
with temporary_workspace() as workspace:
    # Process files in workspace
    (workspace / "output.txt").write_text("Results")
    # Directory cleaned up automatically
```

### Experiment Tracking

```python
from contextlib import contextmanager
import json
import time

@contextmanager
def experiment_tracking(experiment_name, config):
    """Track experiment execution with metrics."""
    experiment = {
        "name": experiment_name,
        "config": config,
        "start_time": time.time(),
        "metrics": {},
        "status": "running"
    }
    
    try:
        yield experiment
        experiment["status"] = "completed"
    except Exception as e:
        experiment["status"] = "failed"
        experiment["error"] = str(e)
        raise
    finally:
        experiment["end_time"] = time.time()
        experiment["duration"] = experiment["end_time"] - experiment["start_time"]
        
        # Save experiment data
        with open(f"experiments/{experiment_name}.json", "w") as f:
            json.dump(experiment, f, indent=2)
        
        print(f"Experiment {experiment_name}: {experiment['status']} "
              f"({experiment['duration']:.2f}s)")

# Usage
with experiment_tracking("resnet50_v2", {"lr": 0.001, "epochs": 10}) as exp:
    # Training loop
    exp["metrics"]["accuracy"] = 0.95
    exp["metrics"]["loss"] = 0.05
```

---

## 7. Common Mistakes to Avoid

### Mistake 1: Not Returning from `__exit__`

```python
# BAD: Always returns True, suppressing ALL exceptions
class BadManager:
    def __exit__(self, *args):
        return True  # This suppresses all exceptions!

# GOOD: Only suppress specific exceptions when intentional
class GoodManager:
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == ExpectedException:
            return True  # Suppress only expected exceptions
        return False  # Propagate all others
```

### Mistake 2: Forgetting `finally` in `contextmanager`

```python
# BAD: Cleanup only happens if no exception
@contextmanager
def bad_manager():
    resource = acquire()
    yield resource
    resource.release()  # Skipped if exception occurs!

# GOOD: Use try/finally
@contextmanager
def good_manager():
    resource = acquire()
    try:
        yield resource
    finally:
        resource.release()  # Always executes
```

### Mistake 3: Returning a Value from `__exit__` Unexpectedly

```python
# BAD: Accidentally suppressing exceptions
class SuspiciousManager:
    def __exit__(self, *args):
        cleanup()
        return True  # Oops! Suppresses exception after cleanup

# BETTER: Explicit exception handling
class ExplicitManager:
    def __exit__(self, exc_type, exc_val, exc_tb):
        cleanup()
        if exc_type is SomeSpecificException:
            return True
        return False
```

---

## 8. Best Practices

1. **Always use `try/finally`** in `contextmanager` generators for cleanup
2. **Return `False` from `__exit__`** unless you intentionally suppress exceptions
3. **Document what exceptions are suppressed** in docstrings
4. **Keep context managers focused** — one resource, one concern
5. **Use `contextlib` utilities** (`suppress`, `ExitStack`) for common patterns
6. **Test cleanup logic** by raising exceptions inside `with` blocks
7. **Use `nullcontext`** for optional context managers in parameterized code
8. **Prefer function-based** `@contextmanager` for simple cases
9. **Use class-based** for complex state management or reuse
10. **Consider `atexit`** for process-level cleanup

---

## 9. Practice Exercises

### Exercise 1: File Backup Manager
Create a context manager that backs up a file before modifying it and restores from backup on failure:

```python
with safe_write("config.json") as f:
    json.dump(new_config, f)
    # If this fails, original file is restored
```

### Exercise 2: Rate Limiter Context Manager
Build a context manager that limits API calls to N per second:

```python
with RateLimiter(max_calls=10, period=1.0):
    response = api.call(endpoint)
```

### Exercise 3: Database Transaction
Create a context manager that handles database transactions with automatic commit/rollback:

```python
with database.transaction() as tx:
    tx.execute("INSERT INTO users ...")
    tx.execute("UPDATE accounts ...")
    # Auto-commits if no exception, rollback otherwise
```

### Exercise 4: Temporary Environment Variable
Build a context manager that temporarily sets an environment variable:

```python
with env_variable("API_KEY", "new_key"):
    # API_KEY is "new_key" here
    make_api_call()
# API_KEY restored to original value
```

---

## 10. Summary

| Concept | Description |
|---------|-------------|
| **Context Manager Protocol** | `__enter__` + `__exit__` methods |
| **`with` statement** | Syntax for using context managers |
| **`contextlib.contextmanager`** | Decorator for function-based managers |
| **`contextlib.suppress`** | Suppress specific exceptions |
| **`contextlib.redirect_stdout`** | Redirect stdout/stderr |
| **`contextlib.ExitStack`** | Dynamic context manager management |
| **`contextlib.nullcontext`** | No-op context manager |
| **Exception handling** | `__exit__` receives exception info |
| **Cleanup guarantee** | `finally` ensures cleanup even on errors |

Context managers are essential for writing safe, clean Python code. They ensure resources are properly managed, exceptions are handled gracefully, and cleanup code always runs — critical for production AI systems where resource leaks can cause cascading failures.

---

## Next Steps

In the next lecture, we'll explore **Async/Await**, which extends context managers into asynchronous programming patterns.
