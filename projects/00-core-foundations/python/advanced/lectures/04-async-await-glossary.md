# Async/Await Glossary

## Quick Reference Table

| Term | One-Line Definition |
|------|-------------------|
| `async def` | Defines a coroutine function |
| `await` | Pauses coroutine until awaited object completes |
| Coroutine | An async function that can be suspended and resumed |
| Event Loop | Core async scheduler that runs coroutines |
| Task | A wrapped coroutine scheduled on the event loop |
| `asyncio.run()` | Entry point that runs an async program |
| `asyncio.gather()` | Run multiple coroutines concurrently |
| `asyncio.create_task()` | Schedule a coroutine as a concurrent task |
| `asyncio.wait()` | Wait for multiple tasks with conditions |
| `asyncio.wait_for()` | Run coroutine with timeout |
| `async with` | Async context manager syntax |
| `async for` | Async iterator/generator loop |
| `__aenter__` | Async context manager enter method |
| `__aexit__` | Async context manager exit method |
| `__aiter__` | Async iterator protocol method |
| `__anext__` | Async iterator next value method |
| `StopAsyncIteration` | Signals end of async iteration |
| `asyncio.Queue` | Thread-safe async queue |
| `asyncio.Semaphore` | Limits concurrent operations |
| `CancelledError` | Exception when task is cancelled |
| `asyncio.TimeoutError` | Exception when timeout exceeded |
| `asyncio.to_thread()` | Run sync function in thread pool |
| Awaitable | Object that can be used with `await` |
| Concurrency | Interleaving multiple tasks |
| Parallelism | Simultaneous execution on multiple cores |
| Non-Blocking | Operations that don't halt the event loop |
| Event Loop Policy | Strategy for managing event loops |
| `asynccontextmanager` | Decorator for async context managers |
| `aiohttp` | Async HTTP client/server library |
| `asyncio.gather` | Run coroutines concurrently, return results |

---

## Detailed Definitions

### `__aenter__`

**Definition**: The async special method called when entering an `async with` block. Sets up the async context and returns a value bound to `as`.

**Example**:
```python
class AsyncDatabase:
    async def __aenter__(self):
        self.connection = await create_connection()
        return self.connection
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.connection.close()
        return False

async def main():
    async with AsyncDatabase() as conn:
        await conn.execute("SELECT ...")
```

**Related**: `__aexit__`, Async Context Manager, `async with`

---

### `__aexit__`

**Definition**: The async special method called when exiting an `async with` block. Performs cleanup and can suppress exceptions by returning `True`.

**Parameters**: Same as `__exit__` — `exc_type`, `exc_val`, `exc_tb`.

**Example**:
```python
class AsyncLock:
    async def __aenter__(self):
        await self.acquire()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.release()
        return False  # Don't suppress exceptions
```

**Related**: `__aenter__`, Async Context Manager, Exception Handling

---

### `__aiter__`

**Definition**: The async special method that returns the async iterator object. Must return `self` for objects that implement both `__aiter__` and `__anext__`.

**Example**:
```python
class AsyncCounter:
    def __init__(self, stop):
        self.current = 0
        self.stop = stop
    
    def __aiter__(self):
        return self  # Returns self as the async iterator
    
    async def __anext__(self):
        if self.current >= self.stop:
            raise StopAsyncIteration
        self.current += 1
        return self.current - 1

async def main():
    async for num in AsyncCounter(5):
        print(num)  # 0, 1, 2, 3, 4
```

**Related**: `__anext__`, Async Iterator, `async for`

---

### `__anext__`

**Definition**: The async special method that returns the next value from an async iterator. Must raise `StopAsyncIteration` when exhausted.

**Example**:
```python
class AsyncFileReader:
    def __init__(self, filename):
        self.filename = filename
        self.file = None
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.file is None:
            self.file = await aio_open(self.filename, "r")
        
        line = await self.file.readline()
        if not line:
            await self.file.close()
            raise StopAsyncIteration
        return line.rstrip("\n")
```

**Related**: `__aiter__`, `StopAsyncIteration`, Async Generator

---

### Awaitable

**Definition**: Any object that can be used with the `await` expression. Includes coroutines, Tasks, Futures, and objects implementing `__await__`.

**Example**:
```python
import asyncio

# Coroutines are awaitable
async def my_coro():
    return 42

# Tasks are awaitable
task = asyncio.create_task(my_coro())

# Custom awaitable
class AsyncResult:
    def __init__(self, value):
        self.value = value
    
    def __await__(self):
        yield  # Suspends once
        return self.value

async def main():
    result = await AsyncResult(100)
    print(result)  # 100
```

**Related**: Coroutine, Task, Future, `__await__`

---

### Cancellation

**Definition**: The act of requesting a task to stop before completion. Cancellation raises `CancelledError` inside the coroutine, which should be caught for cleanup.

**Example**:
```python
import asyncio

async def long_task():
    try:
        for i in range(100):
            print(f"Step {i}")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Task cancelled, cleaning up...")
        raise  # Re-raise to properly mark as cancelled

async def main():
    task = asyncio.create_task(long_task())
    await asyncio.sleep(3)
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        print("Task was cancelled successfully")

asyncio.run(main())
```

**Related**: `CancelledError`, `asyncio.Task.cancel()`, Graceful Shutdown

---

### `CancelledError`

**Definition**: An exception raised inside a coroutine when its task is cancelled. It's a subclass of `BaseException` (not `Exception`), so bare `except Exception` won't catch it.

**Example**:
```python
import asyncio

async def worker():
    try:
        while True:
            await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        print("Cleaning up before exit")
        raise  # Always re-raise to mark task as cancelled

async def main():
    task = asyncio.create_task(worker())
    await asyncio.sleep(2)
    task.cancel()
    
    await task  # Raises CancelledError if not caught in worker
```

**Related**: Cancellation, `BaseException`, Task Lifecycle

---

### Concurrency

**Definition**: The ability to handle multiple tasks by interleaving their execution, switching between them during wait times (I/O operations). Different from parallelism.

**Example**:
```python
import asyncio

async def io_task(name, duration):
    print(f"{name} started")
    await asyncio.sleep(duration)  # I/O wait
    print(f"{name} finished")
    return f"{name}: {duration}s"

async def main():
    # Concurrent execution - tasks interleave during sleeps
    results = await asyncio.gather(
        io_task("Task1", 2),
        io_task("Task2", 1),
        io_task("Task3", 3),
    )
    # Total time: ~3s (not 6s) due to concurrency
    print(results)
```

**Related**: Parallelism, Event Loop, Non-Blocking I/O

---

### `asynccontextmanager`

**Definition**: A decorator from `contextlib` that creates an async context manager from an async generator function. The generator yields the value for `as` and handles cleanup in `finally`.

**Example**:
```python
from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def async_database(url):
    conn = await create_connection(url)
    try:
        yield conn
    finally:
        await conn.close()

async def main():
    async with async_database("postgresql://...") as conn:
        result = await conn.fetch("SELECT * FROM users")
```

**Related**: `@contextmanager`, Async Context Manager, `async with`

---

### `async for`

**Definition**: A loop syntax for iterating over async iterables and async generators, automatically calling `__aiter__` and `__anext__`.

**Example**:
```python
import asyncio

async def async_range(n):
    for i in range(n):
        await asyncio.sleep(0.1)
        yield i

async def main():
    async for num in async_range(5):
        print(num)  # 0, 1, 2, 3, 4
```

**Related**: `__aiter__`, `__anext__`, Async Generator, Async Iterator

---

### `asyncio.create_task()`

**Definition**: Schedules a coroutine to run concurrently on the event loop, wrapping it in a Task object. Returns the Task immediately without blocking.

**Example**:
```python
import asyncio

async def background_work():
    await asyncio.sleep(5)
    return "Background complete"

async def main():
    # Task starts running immediately
    task = asyncio.create_task(background_work())
    
    # Do other work while task runs
    print("Foreground work...")
    await asyncio.sleep(1)
    
    # Get result when needed
    result = await task
    print(result)  # "Background complete"

asyncio.run(main())
```

**Related**: Task, Event Loop, `asyncio.gather()`

---

### `asyncio.gather()`

**Definition**: Runs multiple awaitables concurrently and returns their results in order. If any fail, the exception propagates (unless `return_exceptions=True`).

**Example**:
```python
import asyncio

async def fetch(url):
    await asyncio.sleep(1)
    return f"Data from {url}"

async def main():
    # Run concurrently
    results = await asyncio.gather(
        fetch("api1.com"),
        fetch("api2.com"),
        fetch("api3.com"),
    )
    print(results)  # ["Data from api1.com", "Data from api2.com", "Data from api3.com"]

    # With error handling
    results = await asyncio.gather(
        fetch("api1.com"),
        failing_fetch(),
        return_exceptions=True  # Exceptions returned as values
    )
```

**Related**: `asyncio.create_task()`, Concurrent Execution, Error Handling

---

### `asyncio.Queue`

**Definition**: An async-safe queue for producer-consumer patterns. Supports `put()`, `get()`, and `task_done()` for synchronization.

**Example**:
```python
import asyncio

async def producer(queue):
    for i in range(5):
        await queue.put(f"item-{i}")
        print(f"Produced: item-{i}")
        await asyncio.sleep(0.1)
    await queue.put(None)  # Sentinel

async def consumer(queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"Consumed: {item}")
        await asyncio.sleep(0.2)
        queue.task_done()

async def main():
    queue = asyncio.Queue()
    await asyncio.gather(producer(queue), consumer(queue))

asyncio.run(main())
```

**Related**: Producer-Consumer Pattern, Thread Safety, `task_done()`

---

### `asyncio.Semaphore`

**Definition**: A synchronization primitive that limits the number of concurrent accesses to a resource. Useful for rate limiting or limiting concurrent connections.

**Example**:
```python
import asyncio

async def fetch(url, sem):
    async with sem:  # Acquires semaphore (blocks if at limit)
        print(f"Fetching {url}")
        await asyncio.sleep(1)
        return f"Data from {url}"

async def main():
    sem = asyncio.Semaphore(3)  # Max 3 concurrent
    
    urls = [f"api.com/{i}" for i in range(10)]
    tasks = [fetch(url, sem) for url in urls]
    results = await asyncio.gather(*tasks)
    print(f"Fetched {len(results)} URLs")

asyncio.run(main())
```

**Related**: Rate Limiting, Concurrency Control, Resource Management

---

### `asyncio.to_thread()`

**Definition**: Runs a synchronous function in a separate thread, preventing it from blocking the event loop. Bridge between sync and async code.

**Example**:
```python
import asyncio
import time

def cpu_intensive():
    time.sleep(2)  # Blocking sync function
    return "Result from CPU work"

async def main():
    # This would block the event loop:
    # result = cpu_intensive()
    
    # Use to_thread instead:
    result = await asyncio.to_thread(cpu_intensive)
    print(result)

asyncio.run(main())
```

**Related**: Blocking I/O, Thread Pool, Sync/Async Bridge

---

### `asyncio.wait_for()`

**Definition**: Runs a coroutine with a timeout. Raises `asyncio.TimeoutError` if the coroutine doesn't complete in time.

**Example**:
```python
import asyncio

async def slow_operation():
    await asyncio.sleep(10)
    return "Done"

async def main():
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=2.0)
    except asyncio.TimeoutError:
        print("Operation timed out!")

asyncio.run(main())
```

**Related**: Timeout, Cancellation, `asyncio.wait()`

---

### `asyncio.wait()`

**Definition**: Waits for multiple awaitables with conditions like `FIRST_COMPLETED`, `FIRST_EXCEPTION`, or `ALL_COMPLETED`. Returns sets of done and pending tasks.

**Example**:
```python
import asyncio

async def worker(name, delay):
    await asyncio.sleep(delay)
    return f"{name} done"

async def main():
    tasks = [
        asyncio.create_task(worker("A", 3)),
        asyncio.create_task(worker("B", 1)),
        asyncio.create_task(worker("C", 2)),
    ]
    
    # Wait for first completed
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_COMPLETED
    )
    
    print(f"First done: {done.pop().result()}")
    print(f"Still pending: {len(pending)}")
    
    # Wait for all
    done, _ = await asyncio.wait(pending)
```

**Related**: `asyncio.gather()`, Task Management, Completion Conditions

---

### Async Generator

**Definition**: A function defined with `async def` that contains `yield` expressions. Supports both `async for` iteration and `async with` context management.

**Example**:
```python
import asyncio

async def async_fetch_pages(url, max_pages=10):
    """Async generator fetching paginated data."""
    page = 1
    while page <= max_pages:
        await asyncio.sleep(0.5)  # Simulate network I/O
        data = f"Page {page} data"
        yield data
        page += 1

async def main():
    async for page_data in async_fetch_pages("api.com/data"):
        print(page_data)
```

**Related**: `yield`, Async Iterator, `async for`

---

### Async Iterator

**Definition**: An object implementing `__aiter__` and `__anext__` methods, allowing iteration with `async for`. Each step can perform async operations.

**Example**:
```python
import asyncio

class AsyncLineReader:
    def __init__(self, lines):
        self.lines = iter(lines)
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        try:
            line = next(self.lines)
            await asyncio.sleep(0.1)  # Simulate I/O
            return line
        except StopIteration:
            raise StopAsyncIteration

async def main():
    reader = AsyncLineReader(["line1", "line2", "line3"])
    async for line in reader:
        print(line)
```

**Related**: `__aiter__`, `__anext__`, `async for`

---

### Coroutine

**Definition**: An async function defined with `async def` that can be suspended and resumed. Coroutines are the building blocks of async Python.

**Example**:
```python
import asyncio

async def greet(name):
    """This is a coroutine function."""
    print(f"Hello, {name}!")
    await asyncio.sleep(1)
    return f"Goodbye, {name}!"

# Calling returns a coroutine object (doesn't run yet)
coro = greet("Alice")

# Must be scheduled on event loop
result = asyncio.run(coro)
```

**Related**: `async def`, `await`, Event Loop, Awaitable

---

### Event Loop

**Definition**: The core asyncio mechanism that schedules and runs coroutines, manages callbacks, and handles I/O events. One loop per thread.

**Example**:
```python
import asyncio

async def main():
    print("Running on event loop")
    await asyncio.sleep(1)
    print("Done")

# Method 1: asyncio.run (creates and closes loop)
asyncio.run(main())

# Method 2: Manual loop management
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.close()

# Method 3: Get running loop (inside async context)
async def check_loop():
    loop = asyncio.get_running_loop()
    print(f"Current loop: {loop}")
```

**Related**: Coroutine, Task, Scheduling, `asyncio.run()`

---

### Non-Blocking

**Definition**: An operation that returns control to the caller immediately without waiting for completion, allowing other tasks to run. Async I/O operations are non-blocking.

**Example**:
```python
import asyncio
import time

async def non_blocking_example():
    print("Start")
    # Non-blocking: yields control to event loop
    await asyncio.sleep(1)
    print("End")

# This would be blocking (bad):
# time.sleep(1)  # Blocks entire event loop!

async def main():
    # Multiple non-blocking operations overlap
    await asyncio.gather(
        asyncio.sleep(2),  # All run concurrently
        asyncio.sleep(1),
        asyncio.sleep(3),
    )
    print("All done in ~3 seconds")
```

**Related**: Blocking I/O, Event Loop, Concurrency

---

### `StopAsyncIteration`

**Definition**: An exception raised by `__anext__` to signal the end of an async iteration, analogous to `StopIteration` for sync iterators.

**Example**：
```python
class AsyncCountdown:
    def __init__(self, start):
        self.current = start
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current <= 0:
            raise StopAsyncIteration
        await asyncio.sleep(0.1)
        self.current -= 1
        return self.current + 1

async def main():
    async for num in AsyncCountdown(3):
        print(num)  # 3, 2, 1
```

**Related**: `__anext__`, Async Iterator, `async for` Termination

---

### Task

**Definition**: A wrapper around a coroutine scheduled to run on the event loop. Created by `asyncio.create_task()`. Supports `cancel()`, `result()`, `done()`, and `exception()`.

**Example**:
```python
import asyncio

async def background():
    await asyncio.sleep(2)
    return "Background result"

async def main():
    # Create task (starts immediately)
    task = asyncio.create_task(background())
    
    # Check status
    print(task.done())  # False
    
    # Get result (waits if needed)
    result = await task
    print(result)  # "Background result"
    print(task.done())  # True
```

**Related**: Coroutine, Event Loop, `create_task()`, Cancellation

---
