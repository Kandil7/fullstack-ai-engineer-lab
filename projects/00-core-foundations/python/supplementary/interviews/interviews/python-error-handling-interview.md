# Python Error Handling Interview Practice

## Overview

Proper error handling is crucial for writing robust, production-ready code. This guide covers exception hierarchy, custom exceptions, context managers, try/except/else/finally, common exceptions, and best practices. Master these concepts to demonstrate professional coding practices.

---

## Interview Questions

### Q1: Explain the exception hierarchy in Python.

**Answer:**
Python exceptions form a tree structure rooted at `BaseException`.

```python
BaseException
├── SystemExit
├── KeyboardInterrupt
├── GeneratorExit
└── Exception
    ├── StopIteration
    ├── ArithmeticError
    │   ├── FloatingPointError
    │   ├── OverflowError
    │   └── ZeroDivisionError
    ├── AttributeError
    ├── EOFError
    ├── ImportError
    │   └── ModuleNotFoundError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── NameError
    │   └── UnboundLocalError
    ├── OSError
    │   ├── FileNotFoundError
    │   ├── FileExistsError
    │   └── PermissionError
    ├── RuntimeError
    │   ├── NotImplementedError
    │   └── RecursionError
    ├── SyntaxError
    │   └── IndentationError
    ├── TypeError
    └── ValueError
        └── UnicodeError

# Catching multiple exceptions
try:
    risky_operation()
except (ValueError, TypeError) as e:
    print(f"Caught: {e}")
```

---

### Q2: What are the differences between `except:`, `except Exception:`, and `except BaseException:`?

**Answer:**
Each catches different levels of exceptions.

```python
# Bad: catches everything including SystemExit, KeyboardInterrupt
try:
    process()
except:
    pass

# Better: catches most exceptions
try:
    process()
except Exception:
    pass

# Best: specific exceptions
try:
    process()
except ValueError as e:
    handle_value_error(e)
except TypeError as e:
    handle_type_error(e)

# Exception hierarchy matters
try:
    risky_operation()
except LookupError:  # Catches IndexError and KeyError
    pass

try:
    risky_operation()
except Exception as e:
    if isinstance(e, IndexError):
        handle_index_error()
    elif isinstance(e, KeyError):
        handle_key_error()
```

---

### Q3: Explain the complete try/except/else/finally block.

**Answer:**
Each block serves a specific purpose in exception handling.

```python
def process_file(filename):
    file = None
    try:
        file = open(filename, 'r')
        data = file.read()
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None
    except PermissionError:
        print(f"Permission denied: {filename}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
    else:
        # Runs if no exception occurred
        print(f"Successfully read {len(data)} characters")
        return data
    finally:
        # Always runs, even if exception occurred
        if file:
            file.close()
            print("File closed")

# Modern approach using context manager
def process_file_modern(filename):
    try:
        with open(filename, 'r') as file:
            data = file.read()
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None
    else:
        print(f"Successfully read {len(data)} characters")
        return data
```

---

### Q4: How do you create custom exceptions?

**Answer:**
Custom exceptions should inherit from `Exception` and provide meaningful context.

```python
# Basic custom exception
class ValidationError(Exception):
    def __init__(self, message, field, value):
        super().__init__(message)
        self.field = field
        self.value = value

# Using custom exception
def validate_age(age):
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")
    if age < 0 or age > 150:
        raise ValidationError(
            f"Invalid age: {age}",
            field="age",
            value=age
        )
    return True

try:
    validate_age(200)
except ValidationError as e:
    print(f"Error: {e}")
    print(f"Field: {e.field}")
    print(f"Value: {e.value}")

# Exception hierarchy for a library
class AppError(Exception):
    """Base exception for application"""
    pass

class DatabaseError(AppError):
    """Database-related errors"""
    pass

class ConnectionError(DatabaseError):
    """Database connection errors"""
    def __init__(self, host, port):
        super().__init__(f"Cannot connect to {host}:{port}")
        self.host = host
        self.port = port

class QueryError(DatabaseError):
    """Query execution errors"""
    def __init__(self, query, original_error):
        super().__init__(f"Query failed: {query}")
        self.query = query
        self.original_error = original_error
```

---

### Q5: Explain context managers and the `with` statement.

**Answer:**
Context managers handle setup and cleanup automatically using `__enter__` and `__exit__` methods.

```python
# Class-based context manager
class FileManager:
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
        # Return True to suppress exception, False to propagate
        if exc_type is not None:
            print(f"Error occurred: {exc_val}")
        return False

with FileManager("test.txt", "w") as f:
    f.write("Hello, World!")

# Function-based using contextlib
from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    print(f"Acquiring {name}")
    resource = {"name": name, "active": True}
    try:
        yield resource
    except Exception as e:
        print(f"Error: {e}")
        resource["active"] = False
    finally:
        print(f"Releasing {name}")

with managed_resource("database") as res:
    print(f"Using {res['name']}")
```

---

### Q6: What are the best practices for exception handling?

**Answer:**
Follow these guidelines for clean, maintainable error handling.

```python
# 1. Be specific
try:
    value = my_dict[key]
except KeyError:
    value = default

# 2. Don't catch exceptions you can't handle
try:
    result = complex_operation()
except SpecificError:
    handle_specifically()
except Exception:
    log_error()
    raise  # Re-raise if you can't handle it

# 3. Don't use exceptions for flow control
# Bad
try:
    value = my_list[index]
except IndexError:
    value = None

# Good
if index < len(my_list):
    value = my_list[index]
else:
    value = None

# 4. Log exceptions properly
import logging

logger = logging.getLogger(__name__)

try:
    risky_operation()
except ValueError as e:
    logger.error("Operation failed", exc_info=True)
    raise

# 5. Clean up resources
# Use context managers or try/finally
with open("file.txt") as f:
    process(f)
```

---

### Q7: How do you handle exceptions in async code?

**Answer:**
Async functions use try/except, but exceptions propagate differently.

```python
import asyncio

async def risky_operation():
    await asyncio.sleep(1)
    raise ValueError("Something went wrong")

async def main():
    try:
        await risky_operation()
    except ValueError as e:
        print(f"Caught: {e}")
    
    # Handling multiple awaitables
    tasks = [
        asyncio.create_task(task1()),
        asyncio.create_task(task2()),
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Task {i} failed: {result}")
        else:
            print(f"Task {i} succeeded: {result}")

# Exception groups (Python 3.11+)
async def handle_exception_groups():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(task1())
            tg.create_task(task2())
    except* ValueError as eg:
        print(f"ValueErrors: {eg.exceptions}")
    except* TypeError as eg:
        print(f"TypeErrors: {eg.exceptions}")
```

---

### Q8: Explain exception chaining and the `raise from` syntax.

**Answer:**
Exception chaining preserves the original exception while adding context.

```python
# Implicit chaining
try:
    open("nonexistent.txt")
except FileNotFoundError as e:
    raise RuntimeError("Failed to process") from e

# Explicit chaining with raise from
class DatabaseError(Exception):
    pass

def connect_db():
    try:
        # Some connection attempt
        raise ConnectionError("Connection refused")
    except ConnectionError as e:
        raise DatabaseError("Database unavailable") from e

# Suppressing chaining
try:
    risky_operation()
except ValueError:
    raise TypeError("Type error") from None  # No chain

# Accessing chained exceptions
try:
    connect_db()
except DatabaseError as e:
    print(f"Error: {e}")
    print(f"Original: {e.__cause__}")
```

---

### Q9: What are the EAFP and LBYL approaches?

**Answer:**
Easier to Ask Forgiveness than Permission (EAFP) vs Look Before You Leap (LBYL).

```python
# LBYL - Look Before You Leap
def get_value_lbyl(dictionary, key):
    if key in dictionary:
        return dictionary[key]
    return None

# EAFP - Easier to Ask Forgiveness than Permission
def get_value_eafp(dictionary, key):
    try:
        return dictionary[key]
    except KeyError:
        return None

# Python prefers EAFP
# - More Pythonic
# - Handles race conditions better
# - Often faster when operation usually succeeds

# Example: Thread-safe access
import threading

shared_dict = {}
lock = threading.Lock()

# LBYL - race condition possible
if key in shared_dict:
    value = shared_dict[key]  # Another thread might remove it

# EAFP - safer
try:
    value = shared_dict[key]
except KeyError:
    value = default

# Or use lock
with lock:
    value = shared_dict.get(key, default)
```

---

### Q10: How do you test exception handling?

**Answer:**
Use `pytest.raises` for testing that exceptions are properly raised and handled.

```python
import pytest

# Basic exception testing
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)
    assert str(exc_info.value) == "Cannot divide by zero"

# Testing exception type hierarchy
def test_divide_by_zero_hierarchy():
    with pytest.raises(ArithmeticError):
        divide(10, 0)  # ValueError is subclass of ArithmeticError

# Testing no exception
def test_divide_normal():
    result = divide(10, 2)
    assert result == 5.0

# Parametrized exception testing
@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5.0),
    (10, 0, None),
])
def test_divide(a, b, expected):
    if b == 0:
        with pytest.raises(ValueError):
            divide(a, b)
    else:
        assert divide(a, b) == expected

# Custom exception context
class AppError(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code

def test_custom_exception():
    with pytest.raises(AppError) as exc_info:
        raise AppError("Bad request", 400)
    assert exc_info.value.code == 400
```

---

### Q11: What are contextlib utilities?

**Answer:**
`contextlib` provides utilities for working with context managers.

```python
from contextlib import (
    contextmanager,
    suppress,
    redirect_stdout,
    redirect_stderr,
    ExitStack,
    closing
)
from io import StringIO

# suppress - ignore specific exceptions
with suppress(FileNotFoundError):
    os.remove("nonexistent.txt")

# redirect_stdout - capture stdout
f = StringIO()
with redirect_stdout(f):
    print("Hello, World!")
output = f.getvalue()

# ExitStack - dynamic context management
with ExitStack() as stack:
    files = [stack.enter_context(open(f)) for f in file_list]
    # All files will be closed when exiting

# closing - wrap objects with close() method
class Database:
    def __init__(self):
        self.connected = True
    
    def close(self):
        self.connected = False

with closing(Database()) as db:
    # Use db
    pass
# db.close() called automatically

# contextmanager with exception handling
@contextmanager
def managed_resource(name):
    print(f"Acquiring {name}")
    try:
        yield name
    except Exception as e:
        print(f"Error with {name}: {e}")
        raise
    finally:
        print(f"Releasing {name}")
```

---

### Q12: How do you handle exceptions in generators?

**Answer:**
Generators can raise and handle exceptions using try/except and `throw()`.

```python
# Generator with exception handling
def generator_with_errors():
    try:
        yield 1
        yield 2
        yield 3
    except ValueError:
        print("Caught ValueError in generator")
    finally:
        print("Generator cleanup")

gen = generator_with_errors()
print(next(gen))  # 1
print(next(gen))  # 2
gen.throw(ValueError, "Forced error")

# Generator that receives exceptions
def controlled_generator():
    value = 0
    while True:
        try:
            response = yield value
            if response == "error":
                raise ValueError("Error requested")
            value = response if response is not None else value + 1
        except Exception as e:
            print(f"Generator received: {e}")
            yield -1

gen = controlled_generator()
print(next(gen))      # 0
print(gen.send(5))    # 5
print(gen.throw(ValueError, "test"))  # -1 (after handling)

# Context manager using generator
@contextmanager
def managed_file(filename, mode):
    try:
        f = open(filename, mode)
    except Exception as e:
        print(f"Failed to open: {e}")
        raise
    try:
        yield f
    finally:
        f.close()
```

---

### Q13: Explain exception safety and RAII in Python.

**Answer:**
RAII (Resource Acquisition Is Initialization) ensures resources are cleaned up. Python uses context managers for this.

```python
# RAII pattern with context manager
class DatabaseConnection:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None
    
    def __enter__(self):
        self.connection = self._connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
        return False
    
    def _connect(self):
        print(f"Connecting to {self.connection_string}")
        return {"connected": True}
    
    def execute(self, query):
        print(f"Executing: {query}")

# Usage - connection guaranteed to close
with DatabaseConnection("postgres://localhost/mydb") as db:
    db.execute("SELECT * FROM users")
# Connection closed here, even if exception occurred

# Multiple resources
class Transaction:
    def __init__(self, db):
        self.db = db
    
    def __enter__(self):
        self.db.execute("BEGIN")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.db.execute("COMMIT")
        else:
            self.db.execute("ROLLBACK")
        return False
```

---

### Q14: What are the common pitfalls in exception handling?

**Answer:**
Avoid these common mistakes in production code.

```python
# Pitfall 1: Bare except
try:
    process()
except:  # BAD - catches everything
    pass

# Pitfall 2: Swallowing exceptions
try:
    risky_operation()
except Exception:
    pass  # BAD - silent failure

# Pitfall 3: Too broad exception handling
try:
    process()
except Exception:  # BAD - catches too much
    log_error()

# Pitfall 4: Mutable default in exception
def bad_function(errors=[]):  # BAD - shared state
    errors.append("error")
    return errors

# Pitfall 5: Exception in finally block
def risky_finally():
    try:
        raise ValueError("Original")
    finally:
        raise TypeError("Finally")  # Original exception lost!

# Pitfall 6: Infinite recursion in except
def infinite_loop():
    try:
        raise ValueError()
    except ValueError:
        infinite_loop()  # BAD - RecursionError

# Good practices
def good_exception_handling():
    try:
        risky_operation()
    except SpecificError as e:
        logger.error("Specific error", exc_info=True)
        raise  # Re-raise if needed
    except Exception as e:
        logger.critical("Unexpected error", exc_info=True)
        raise
    else:
        logger.info("Operation succeeded")
    finally:
        cleanup()
```

---

### Q15: Explain exception handling in concurrent code.

**Answer:**
Concurrent code requires special consideration for exception propagation.

```python
import asyncio
import concurrent.futures

# Threading
def thread_worker():
    raise ValueError("Thread error")

with concurrent.futures.ThreadPoolExecutor() as executor:
    future = executor.submit(thread_worker)
    try:
        result = future.result()
    except ValueError as e:
        print(f"Thread error: {e}")

# Multiprocessing
def process_worker():
    raise ValueError("Process error")

with concurrent.futures.ProcessPoolExecutor() as executor:
    future = executor.submit(process_worker)
    try:
        result = future.result()
    except ValueError as e:
        print(f"Process error: {e}")

# Async
async def async_worker():
    raise ValueError("Async error")

async def main():
    try:
        await async_worker()
    except ValueError as e:
        print(f"Async error: {e}")
    
    # Exception in tasks
    tasks = [
        asyncio.create_task(task1()),
        asyncio.create_task(task2()),
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for result in results:
        if isinstance(result, Exception):
            print(f"Task failed: {result}")

asyncio.run(main())
```

---

## Coding Challenges

### Challenge 1: Implement a Retry Decorator

**Problem:** Create a decorator that retries function calls on specific exceptions.

**Solution:**
```python
import functools
import time

def retry(exceptions=Exception, max_attempts=3, delay=1, backoff=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise
                    print(f"Attempt {attempts} failed: {e}")
                    print(f"Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            return None
        return wrapper
    return decorator

# Usage
@retry(exceptions=(ConnectionError, TimeoutError), max_attempts=3, delay=1)
def fetch_data(url):
    import random
    if random.random() < 0.7:
        raise ConnectionError("Connection failed")
    return "Success"

# Test
try:
    result = fetch_data("https://api.example.com")
    print(result)
except ConnectionError as e:
    print(f"Failed after retries: {e}")
```

---

### Challenge 2: Implement a Context Manager with Exception Handling

**Problem:** Create a context manager that logs exceptions and provides cleanup.

**Solution:**
```python
from contextlib import contextmanager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@contextmanager
def managed_operation(operation_name):
    logger.info(f"Starting: {operation_name}")
    start_time = __import__('time').time()
    
    try:
        yield operation_name
    except Exception as e:
        duration = __import__('time').time() - start_time
        logger.error(f"Failed: {operation_name} after {duration:.2f}s")
        logger.error(f"Exception: {type(e).__name__}: {e}")
        raise
    else:
        duration = __import__('time').time() - start_time
        logger.info(f"Completed: {operation_name} in {duration:.2f}s")

# Usage
with managed_operation("data processing"):
    # Do work
    data = [1, 2, 3]
    result = [x * 2 for x in data]

# With exception
try:
    with managed_operation("risky operation"):
        raise ValueError("Something went wrong")
except ValueError:
    logger.info("Exception was logged and re-raised")
```

---

### Challenge 3: Implement a Validation Framework

**Problem:** Create a validation framework that collects multiple errors.

**Solution:**
```python
class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors
        super().__init__(f"Validation failed: {len(errors)} errors")

class Validator:
    def __init__(self):
        self.errors = []
    
    def check(self, condition, message):
        if not condition:
            self.errors.append(message)
        return self
    
    def is_valid(self):
        return len(self.errors) == 0
    
    def validate(self):
        if not self.is_valid():
            raise ValidationError(self.errors)

def validate_user(data):
    validator = Validator()
    
    validator.check(
        "name" in data and len(data["name"]) > 0,
        "Name is required"
    ).check(
        "email" in data and "@" in data.get("email", ""),
        "Valid email is required"
    ).check(
        "age" in data and 0 <= data.get("age", -1) <= 150,
        "Age must be between 0 and 150"
    )
    
    validator.validate()

# Usage
try:
    validate_user({"name": "", "email": "invalid"})
except ValidationError as e:
    print("Validation errors:")
    for error in e.errors:
        print(f"  - {error}")
```

---

### Challenge 4: Implement Error Handling Pipeline

**Problem:** Create a pipeline that processes data with error handling at each step.

**Solution:**
```python
from typing import Any, Callable, List

class PipelineError(Exception):
    def __init__(self, step, original_error):
        self.step = step
        self.original_error = original_error
        super().__init__(f"Error in step '{step}': {original_error}")

class Pipeline:
    def __init__(self):
        self.steps = []
    
    def add_step(self, name: str, func: Callable):
        self.steps.append((name, func))
        return self
    
    def execute(self, data: Any, stop_on_error: bool = False) -> Any:
        result = data
        errors = []
        
        for name, func in self.steps:
            try:
                result = func(result)
            except Exception as e:
                errors.append((name, e))
                if stop_on_error:
                    raise PipelineError(name, e)
        
        if errors:
            print(f"Pipeline completed with {len(errors)} errors:")
            for step, error in errors:
                print(f"  - {step}: {error}")
        
        return result

# Usage
def validate(data):
    if not isinstance(data, list):
        raise TypeError("Input must be a list")
    return data

def clean(data):
    return [x.strip() if isinstance(x, str) else x for x in data]

def transform(data):
    return [x.upper() if isinstance(x, str) else x for x in data]

pipeline = Pipeline()
pipeline.add_step("validate", validate)
pipeline.add_step("clean", clean)
pipeline.add_step("transform", transform)

result = pipeline.execute(["  hello  ", " world  "])
print(result)  # ['HELLO', 'WORLD']
```

---

### Challenge 5: Implement Circuit Breaker Pattern

**Problem:** Create a circuit breaker to prevent cascading failures.

**Solution:**
```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = None
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self.state = CircuitState.HALF_OPEN
                else:
                    raise Exception("Circuit breaker is OPEN")
            
            try:
                result = func(*args, **kwargs)
                self._on_success()
                return result
            except Exception as e:
                self._on_failure()
                raise
        return wrapper
    
    def _on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
    
    def _should_attempt_reset(self):
        return time.time() - self.last_failure_time >= self.recovery_timeout

# Usage
@CircuitBreaker(failure_threshold=3, recovery_timeout=5)
def call_external_service():
    import random
    if random.random() < 0.5:
        raise ConnectionError("Service unavailable")
    return "Success"

# Test
for i in range(10):
    try:
        result = call_external_service()
        print(f"Attempt {i+1}: {result}")
    except Exception as e:
        print(f"Attempt {i+1}: {e}")
    time.sleep(1)
```

---

### Challenge 6: Implement Error Collector

**Problem:** Create a class that collects multiple errors during processing.

**Solution:**
```python
class ErrorCollector:
    def __init__(self):
        self.errors = []
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.errors.append({
                "type": exc_type.__name__,
                "message": str(exc_val),
                "traceback": exc_tb
            })
        return True  # Suppress exception
    
    def add_error(self, error_type, message):
        self.errors.append({
            "type": error_type,
            "message": message
        })
    
    def has_errors(self):
        return len(self.errors) > 0
    
    def clear(self):
        self.errors = []
    
    def raise_if_errors(self):
        if self.has_errors():
            error_messages = "\n".join(
                f"  - {e['type']}: {e['message']}"
                for e in self.errors
            )
            raise Exception(f"Collected errors:\n{error_messages}")

# Usage
with ErrorCollector() as collector:
    try:
        risky_operation_1()
    except Exception as e:
        collector.add_error("Operation1Error", str(e))
    
    try:
        risky_operation_2()
    except Exception as e:
        collector.add_error("Operation2Error", str(e))

if collector.has_errors():
    print(f"Found {len(collector.errors)} errors")
    collector.raise_if_errors()
```

---

### Challenge 7: Implement Error Recovery Decorator

**Problem:** Create a decorator that attempts recovery strategies on failure.

**Solution:**
```python
import functools
from typing import Callable, Any, List

def with_recovery(
    strategies: List[Callable],
    fallback: Any = None,
    max_retries: int = 1
):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    print(f"Attempt {attempt + 1} failed: {e}")
                    
                    for strategy in strategies:
                        try:
                            result = strategy(e)
                            if result is not None:
                                return result
                        except Exception as strategy_error:
                            print(f"Recovery strategy failed: {strategy_error}")
            
            if fallback is not None:
                print("Using fallback value")
                return fallback
            
            raise last_error
        return wrapper
    return decorator

# Recovery strategies
def cache_recovery(error):
    print("Attempting cache recovery")
    return {"source": "cache", "data": "cached_value"}

def default_recovery(error):
    print("Using default value")
    return {"source": "default", "data": "default_value"}

# Usage
@with_recovery(
    strategies=[cache_recovery, default_recovery],
    fallback={"source": "fallback", "data": None}
)
def fetch_data(url):
    raise ConnectionError("Service unavailable")

result = fetch_data("https://api.example.com")
print(result)
```

---

### Challenge 8: Implement Structured Error Logging

**Problem:** Create a system for structured error logging with context.

**Solution:**
```python
import logging
import json
from datetime import datetime
from typing import Any, Dict
from contextlib import contextmanager

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
    
    def log_error(
        self,
        error: Exception,
        context: Dict[str, Any] = None,
        level: str = "ERROR"
    ):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "error_type": type(error).__name__,
            "message": str(error),
            "context": context or {}
        }
        
        self.logger.log(
            getattr(logging, level),
            json.dumps(log_entry, indent=2)
        )
    
    @contextmanager
    def error_context(self, **context):
        try:
            yield
        except Exception as e:
            self.log_error(e, context)
            raise

# Usage
logger = StructuredLogger("myapp")

# Manual logging
try:
    risky_operation()
except Exception as e:
    logger.log_error(
        e,
        context={
            "user_id": 123,
            "operation": "fetch_data",
            "url": "https://api.example.com"
        }
    )

# Context manager
with logger.error_context(user_id=123, operation="process"):
    risky_operation()
```

---

## Common Follow-up Questions

1. **"When should you catch exceptions vs let them propagate?"**
   - Catch when you can handle or recover
   - Let propagate if caller needs to know
   - Always log before re-raising

2. **"How do you handle exceptions in production?"**
   - Log with context (user, request, stack trace)
   - Alert on critical errors
   - Use circuit breakers for external services
   - Implement graceful degradation

3. **"What's the difference between error and exception?"**
   - Error: serious problems (SystemError, MemoryError)
   - Exception: conditions that can be caught and handled
   - Both inherit from BaseException

4. **"How do you debug production exceptions?"**
   - Structured logging with context
   - Stack traces
   - Correlation IDs
   - Error tracking services (Sentry, etc.)

5. **"When is it appropriate to create custom exceptions?"**
   - When standard exceptions don't convey enough info
   - For library/framework boundaries
   - To group related errors
   - For domain-specific error handling

---

## Tips for Answering

1. **Be specific** - Don't just say "catch exceptions"; show you know which ones
2. **Discuss trade-offs** - EAFP vs LBYL, broad vs narrow catching
3. **Mention production concerns** - Logging, monitoring, recovery
4. **Show awareness of pitfalls** - Mutable defaults, swallowed exceptions
5. **Know the built-in exceptions** - ValueError, TypeError, KeyError, etc.
6. **Practice context managers** - Both class-based and function-based
7. **Understand exception chaining** - `raise from` syntax
8. **Be familiar with testing** - pytest.raises, exception assertions
9. **Consider async implications** - Exception handling differs in async code
10. **Think about resource cleanup** - try/finally, context managers

---

## Key Concepts to Review

| Concept | Key Points |
|---------|-----------|
| Exception Hierarchy | BaseException -> Exception -> specific types |
| try/except/else/finally | Each block serves specific purpose |
| Custom Exceptions | Inherit from Exception, provide context |
| Context Managers | `__enter__`/`__exit__`, with statement |
| EAFP | Python prefers asking forgiveness |
| Exception Chaining | `raise from` preserves original |
| Best Practices | Be specific, log, clean up resources |
| Testing | pytest.raises, exception assertions |

---

*Proper error handling distinguishes professional code from amateur code. Master these patterns to write robust, maintainable applications!*