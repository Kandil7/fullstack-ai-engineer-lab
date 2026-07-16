"""
Context Managers - Advanced Python Exercises
============================================
Context managers ensure proper resource acquisition and release
using the 'with' statement.
"""

import os
import tempfile
from contextlib import contextmanager, suppress, redirect_stdout, ExitStack
from io import StringIO
from typing import Any, Optional


# =============================================================================
# 1. Class-Based Context Manager
# =============================================================================

class ManagedFile:
    """Context manager for file operations with auto-close."""

    def __init__(self, filename: str, mode: str = "r"):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        print(f"  Opening {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
            print(f"  Closed {self.filename}")
        if exc_type is not None:
            print(f"  Error occurred: {exc_val}")
        return False  # Don't suppress exceptions


class DatabaseConnection:
    """Simulated database connection context manager."""

    def __init__(self, host: str = "localhost", port: int = 5432):
        self.host = host
        self.port = port
        self.connection = None
        self.transaction_active = False

    def __enter__(self):
        self.connection = {"host": self.host, "port": self.port, "id": id(self)}
        self.transaction_active = True
        print(f"  Connected to {self.host}:{self.port}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"  Rolling back transaction: {exc_val}")
        else:
            print(f"  Committing transaction")
        self.transaction_active = False
        self.connection = None
        print(f"  Connection closed")
        return False

    def execute(self, query: str) -> dict:
        if not self.transaction_active:
            raise RuntimeError("No active transaction")
        return {"query": query, "status": "ok", "connection": self.connection["id"]}


# =============================================================================
# 2. Function-Based Context Manager (contextmanager)
# =============================================================================

@contextmanager
def managed_temp_dir(prefix: str = "temp_") -> str:
    """Create and clean up a temporary directory."""
    temp_dir = tempfile.mkdtemp(prefix=prefix)
    print(f"  Created temp dir: {temp_dir}")
    try:
        yield temp_dir
    finally:
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"  Cleaned up temp dir")


@contextmanager
def timer(label: str = "Operation"):
    """Time a block of code."""
    import time
    start = time.perf_counter()
    print(f"  [{label}] Starting...")
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"  [{label}] Completed in {elapsed:.4f}s")


@contextmanager
def captured_output():
    """Capture stdout output."""
    new_out = StringIO()
    old_out = __import__("sys").stdout
    __import__("sys").stdout = new_out
    try:
        yield new_out
    finally:
        __import__("sys").stdout = old_out


# =============================================================================
# 3. Advanced Patterns
# =============================================================================

class SuppressErrors:
    """Context manager to suppress specific exceptions."""

    def __init__(self, *exceptions):
        self.exceptions = exceptions

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and issubclass(exc_type, self.exceptions):
            print(f"  Suppressed: {exc_type.__name__}: {exc_val}")
            return True
        return False


class NestedResource:
    """Simulated nested resource manager."""

    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        print(f"  Acquiring {self.name}")
        return self

    def __exit__(self, *args):
        print(f"  Releasing {self.name}")


# =============================================================================
# 4. Contextlib Utilities
# =============================================================================

def demo_contextlib_utilities():
    """Demonstrate contextlib module features."""
    # suppress - silently ignore exceptions
    with suppress(FileNotFoundError):
        os.remove("nonexistent_file.txt")
    print("  FileNotFoundError was suppressed")

    # redirect_stdout
    with redirect_stdout(StringIO()) as output:
        print("  This goes to capture, not console")
    print(f"  Captured: {output.getvalue().strip()}")

    # ExitStack for dynamic context managers
    with ExitStack() as stack:
        files = []
        for i in range(3):
            f = stack.enter_context(
                ManagedFile(tempfile.mktemp(suffix=".txt"), "w")
            )
            f.write(f"File {i}\n")
            files.append(f)
        print(f"  Managed {len(files)} files dynamically")


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("CONTEXT MANAGERS DEMO")
    print("=" * 60)

    # 1. Class-based context manager
    print("\n--- Managed File ---")
    tmpfile = tempfile.mktemp(suffix=".txt")
    with ManagedFile(tmpfile, "w") as f:
        f.write("Hello, Context Managers!\n")
    with ManagedFile(tmpfile, "r") as f:
        print(f"  Content: {f.read().strip()}")
    os.remove(tmpfile)

    # 2. Database connection
    print("\n--- Database Connection ---")
    with DatabaseConnection("db.example.com", 5432) as db:
        result = db.execute("SELECT * FROM users")
        print(f"  Query result: {result}")

    # 3. Function-based context managers
    print("\n--- Temporary Directory ---")
    with managed_temp_dir("demo_") as temp_dir:
        print(f"  Working in: {temp_dir}")

    print("\n--- Timer ---")
    with timer("Fibonacci"):
        def fib(n):
            return n if n < 2 else fib(n-1) + fib(n-2)
        result = fib(25)
        print(f"  fib(25) = {result}")

    # 4. Suppress errors
    print("\n--- Suppress Errors ---")
    with SuppressErrors(ZeroDivisionError, ValueError):
        result = 1 / 0
    print("  Execution continued after error")

    # 5. Contextlib utilities
    print("\n--- Contextlib Utilities ---")
    demo_contextlib_utilities()

    print("\n" + "=" * 60)
    print("All context manager demos complete!")
    print("=" * 60)
