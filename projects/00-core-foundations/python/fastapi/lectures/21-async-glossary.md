# Glossary: Async Programming in FastAPI

## Quick Reference Table

| Term | Definition | Related Terms |
|------|------------|---------------|
| Await | Pause coroutine until result is ready | Async, Coroutine |
| Async | Keyword defining asynchronous function | Await, Coroutine |
| Coroutine | An async function that can be paused | Async, Await |
| Event Loop | Manages and runs async tasks | Asyncio, Task |
| Task | A scheduled coroutine | Coroutine, Event Loop |
| Gather | Run multiple coroutines concurrently | Task, Asyncio |
| Semaphore | Limits concurrent access | Concurrency, Task |
| AsyncClient | HTTP client for async requests | Httpx, Request |
| ASGI | Async Server Gateway Interface | Uvicorn, Starlette |
| Coroutine Function | Function defined with async def | Coroutine, Async |
| Awaiting | Suspending execution until ready | Await, Async |
| Concurrent | Multiple tasks executing simultaneously | Parallel, Async |
| Non-blocking | Operations that don't halt execution | Blocking, Async |
| Thread Pool | Pool of threads for sync operations | Executor, Sync |
| Streaming | Sending data in chunks | Generator, Async |

---

## Detailed Definitions

### Await

**Definition**: A keyword that pauses the execution of a coroutine until the awaited result is ready, allowing other tasks to run.

**Code Example**:
```python
import asyncio

async def fetch_data():
    # await pauses here, allowing other tasks to run
    await asyncio.sleep(2)
    return {"data": "value"}

async def main():
    # await waits for the coroutine to complete
    result = await fetch_data()
    print(result)  # {"data": "value"}

# Multiple awaits
async def process():
    data1 = await fetch_data()  # Pauses here
    data2 = await fetch_data()  # Pauses here
    return data1, data2

# Await with timeout
async def fetch_with_timeout():
    try:
        result = await asyncio.wait_for(
            fetch_data(),
            timeout=5.0
        )
    except asyncio.TimeoutError:
        print("Request timed out")
```

**Related Terms**: Async, Coroutine, Task

---

### Async

**Definition**: A keyword that defines an asynchronous function (coroutine) that can be paused and resumed.

**Code Example**:
```python
import asyncio

# Async function definition
async def my_function():
    await asyncio.sleep(1)
    return "done"

# Async with parameters
async def fetch_user(user_id: int) -> dict:
    await asyncio.sleep(0.5)
    return {"id": user_id, "name": "User"}

# Async class method
class DataFetcher:
    async def fetch(self, url: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.json()

# Async context manager
class AsyncDatabase:
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

# Async iterator
class AsyncRange:
    def __init__(self, stop):
        self.stop = stop
        self.current = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current >= self.stop:
            raise StopAsyncIteration
        self.current += 1
        await asyncio.sleep(0.1)
        return self.current - 1
```

**Related Terms**: Await, Coroutine, Asyncio

---

### Coroutine

**Definition**: An async function that can be paused and resumed, returning a coroutine object when called.

**Code Example**:
```python
import asyncio

# Define coroutine
async def greet(name: str) -> str:
    await asyncio.sleep(1)
    return f"Hello, {name}!"

# Create coroutine object
coro = greet("World")
print(coro)  # <coroutine object greet at 0x...>

# Run coroutine
async def main():
    # Method 1: await
    result = await greet("World")
    
    # Method 2: asyncio.run
    result = asyncio.run(greet("World"))
    
    # Method 3: create_task
    task = asyncio.create_task(greet("World"))
    result = await task

# Coroutine chain
async def step1():
    await asyncio.sleep(1)
    return "Step 1"

async def step2(data):
    await asyncio.sleep(1)
    return f"Step 2: {data}"

async def pipeline():
    data = await step1()
    return await step2(data)
```

**Related Terms**: Async, Await, Task

---

### Event Loop

**Definition**: The core component of asyncio that schedules and runs coroutines, handles I/O, and manages callbacks.

**Code Example**:
```python
import asyncio

# Get current event loop
loop = asyncio.get_event_loop()

# Run coroutine
async def main():
    print("Running in event loop")
    await asyncio.sleep(1)
    return "done"

# Method 1: asyncio.run (recommended)
result = asyncio.run(main())

# Method 2: Manual loop management
loop = asyncio.get_event_loop()
try:
    result = loop.run_until_complete(main())
finally:
    loop.close()

# Check if running
async def check_loop():
    loop = asyncio.get_running_loop()
    print(f"Loop running: {loop.is_running()}")

# Schedule callback
def callback(future):
    print(f"Callback result: {future.result()}")

async def schedule_callback():
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    
    # Schedule callback
    loop.call_soon(callback, future)
    
    # Set result
    future.set_result("Callback data")
```

**Related Terms**: Asyncio, Task, Coroutine

---

### Task

**Definition**: A wrapper for a coroutine that schedules it to run on the event loop.

**Code Example**:
```python
import asyncio

async def slow_operation():
    await asyncio.sleep(5)
    return "result"

async def main():
    # Create task (starts immediately)
    task = asyncio.create_task(slow_operation())
    
    # Do other work while task runs
    print("Doing other work...")
    
    # Get result (waits if needed)
    result = await task
    print(f"Result: {result}")

# Multiple tasks
async def process_all():
    tasks = [
        asyncio.create_task(slow_operation()),
        asyncio.create_task(slow_operation()),
        asyncio.create_task(slow_operation())
    ]
    
    # Wait for all tasks
    results = await asyncio.gather(*tasks)
    return results

# Task with callback
def task_done_callback(task):
    print(f"Task completed: {task.result()}")

async def main():
    task = asyncio.create_task(slow_operation())
    task.add_done_callback(task_done_callback)
    await task

# Cancel task
async def cancellable():
    try:
        await asyncio.sleep(100)
    except asyncio.CancelledError:
        print("Task cancelled")
        raise

async def main():
    task = asyncio.create_task(cancellable())
    await asyncio.sleep(1)
    task.cancel()
```

**Related Terms**: Coroutine, Event Loop, Gather

---

### Gather

**Definition**: Run multiple coroutines concurrently and collect their results.

**Code Example**:
```python
import asyncio

async def fetch_user(user_id: int):
    await asyncio.sleep(1)
    return {"id": user_id, "name": f"User {user_id}"}

async def main():
    # Basic gather
    results = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3)
    )
    print(results)  # [{"id": 1, ...}, {"id": 2, ...}, {"id": 3, ...}]

# Gather with return exceptions
async def might_fail():
    await asyncio.sleep(1)
    raise ValueError("Error!")

async def safe_gather():
    results = await asyncio.gather(
        fetch_user(1),
        might_fail(),
        fetch_user(2),
        return_exceptions=True  # Don't raise, return exception
    )
    # results = [{"id": 1}, ValueError("Error!"), {"id": 2}]

# Gather with timeout
async def gather_with_timeout():
    results = await asyncio.wait_for(
        asyncio.gather(
            fetch_user(1),
            fetch_user(2)
        ),
        timeout=5.0
    )
    return results
```

**Related Terms**: Task, Coroutine, Concurrent

---

### Semaphore

**Definition**: A synchronization primitive that limits the number of concurrent tasks accessing a resource.

**Code Example**:
```python
import asyncio

# Create semaphore with limit
semaphore = asyncio.Semaphore(5)  # Max 5 concurrent

async def limited_operation(task_id: int):
    async with semaphore:
        print(f"Task {task_id} started")
        await asyncio.sleep(2)
        print(f"Task {task_id} completed")

async def main():
    # Only 5 tasks run at a time
    tasks = [limited_operation(i) for i in range(20)]
    await asyncio.gather(*tasks)

# Semaphore for HTTP requests
class RateLimiter:
    def __init__(self, max_requests: int):
        self.semaphore = asyncio.Semaphore(max_requests)
    
    async def fetch(self, url: str):
        async with self.semaphore:
            async with httpx.AsyncClient() as client:
                return await client.get(url)

async def main():
    limiter = RateLimiter(max_requests=10)
    tasks = [limiter.fetch(f"https://api.example.com/{i}") for i in range(100)]
    results = await asyncio.gather(*tasks)
```

**Related Terms**: Concurrency, Task, Limit

---

### AsyncClient

**Definition**: An asynchronous HTTP client for making non-blocking HTTP requests.

**Code Example**:
```python
import httpx
import asyncio

# Basic usage
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()

# With timeout
async def fetch_with_timeout():
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get("https://api.example.com/data")
        return response.json()

# POST request
async def create_resource(data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.example.com/resources",
            json=data,
            headers={"Authorization": "Bearer token123"}
        )
        return response.json()

# Multiple concurrent requests
async def fetch_multiple(urls: list):
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]

# Streaming
async def stream_data():
    async with httpx.AsyncClient() as client:
        async with client.stream("GET", "https://api.example.com/stream") as response:
            async for chunk in response.aiter_text():
                yield chunk
```

**Related Terms**: HTTP, Request, Async

---

### ASGI

**Definition**: Asynchronous Server Gateway Interface - the standard for async Python web applications.

**Code Example**:
```python
# ASGI application structure
# app = AsyncApp()

# Uvicorn runs ASGI applications
# uvicorn app.main:app --reload

# Custom ASGI middleware
class TimingMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            start_time = time.time()
            
            async def send_wrapper(message):
                if message["type"] == "http.response.start":
                    process_time = time.time() - start_time
                    headers = list(message.get("headers", []))
                    headers.append([
                        b"x-process-time",
                        str(process_time).encode()
                    ])
                    message["headers"] = headers
                await send(message)
            
            await self.app(scope, receive, send_wrapper)
        else:
            await self.app(scope, receive, send)

# FastAPI uses ASGI under the hood
from fastapi import FastAPI
app = FastAPI()  # This is an ASGI application
```

**Related Terms**: Uvicorn, Starlette, Async

---

### Concurrent

**Definition**: Multiple tasks executing during the same time period, potentially interleaving their execution.

**Code Example**:
```python
import asyncio

# Concurrent execution
async def task1():
    print("Task 1 start")
    await asyncio.sleep(2)
    print("Task 1 end")
    return 1

async def task2():
    print("Task 2 start")
    await asyncio.sleep(1)
    print("Task 2 end")
    return 2

async def main():
    # These run concurrently
    await asyncio.gather(task1(), task2())
    # Output:
    # Task 1 start
    # Task 2 start
    # Task 2 end (after 1 second)
    # Task 1 end (after 2 seconds)

# Concurrent with asyncio.as_completed
async def main():
    tasks = [task1(), task2()]
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"Got result: {result}")
```

**Related Terms**: Parallel, Async, Task

---

### Non-blocking

**Definition**: Operations that don't halt execution, allowing other tasks to proceed.

**Code Example**:
```python
import asyncio

# Blocking (BAD for async)
def blocking_operation():
    time.sleep(5)  # Blocks everything

# Non-blocking (GOOD for async)
async def non_blocking_operation():
    await asyncio.sleep(5)  # Yields control

# Non-blocking I/O
async def read_file():
    import aiofiles
    async with aiofiles.open('file.txt', 'r') as f:
        content = await f.read()
    return content

# Non-blocking network
async def fetch_url():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://example.com")
        return response.text
```

**Related Terms**: Blocking, Async, Await

---

### Thread Pool

**Definition**: A pool of worker threads for executing synchronous blocking operations without blocking the event loop.

**Code Example**:
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Default executor
async def run_blocking():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, blocking_function)
    return result

# Custom thread pool
executor = ThreadPoolExecutor(max_workers=10)

async def run_in_custom_pool():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, blocking_function)
    return result

# CPU-bound work
def cpu_intensive():
    # Heavy computation
    return sum(i * i for i in range(1000000))

async def main():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, cpu_intensive)
    return result
```

**Related Terms**: Executor, Thread, Sync

---

### Streaming

**Definition**: Sending or receiving data in chunks rather than all at once.

**Code Example**:
```python
from fastapi.responses import StreamingResponse
import asyncio

# Async generator for streaming
async def data_stream():
    for i in range(100):
        await asyncio.sleep(0.1)
        yield f"Chunk {i}\n"

# Streaming endpoint
@app.get("/stream")
async def stream_endpoint():
    return StreamingResponse(
        data_stream(),
        media_type="text/plain"
    )

# Streaming JSON
async def json_stream():
    import json
    for i in range(100):
        data = {"id": i, "value": f"Item {i}"}
        yield json.dumps(data) + "\n"
        await asyncio.sleep(0.1)

@app.get("/stream-json")
async def stream_json():
    return StreamingResponse(
        json_stream(),
        media_type="application/x-ndjson"
    )

# Streaming response from external API
async def stream_external():
    async with httpx.AsyncClient() as client:
        async with client.stream("GET", "https://api.example.com/stream") as response:
            async for chunk in response.aiter_text():
                yield chunk
```

**Related Terms**: Generator, Async, Response

---

### Executor

**Definition**: An interface for running synchronous functions in a separate thread or process pool.

**Code Example**:
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Thread executor
thread_executor = ThreadPoolExecutor(max_workers=5)

async def use_thread_executor():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        thread_executor,
        blocking_io_operation
    )
    return result

# Process executor for CPU-bound work
process_executor = ProcessPoolExecutor(max_workers=4)

async def use_process_executor():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        process_executor,
        cpu_intensive_operation
    )
    return result

# Custom executor
from concurrent.futures import Executor

class CustomExecutor(Executor):
    def submit(self, fn, *args, **kwargs):
        # Custom implementation
        return super().submit(fn, *args, **kwargs)
```

**Related Terms**: Thread Pool, Process, Sync

---

### Timeout

**Definition**: A limit on how long an async operation can run before being cancelled.

**Code Example**:
```python
import asyncio

# Simple timeout
async def fetch_with_timeout():
    try:
        result = await asyncio.wait_for(
            slow_operation(),
            timeout=5.0
        )
        return result
    except asyncio.TimeoutError:
        print("Operation timed out")
        return None

# Timeout with shield (prevent cancellation)
async def protected_operation():
    try:
        result = await asyncio.wait_for(
            asyncio.shield(important_operation()),
            timeout=5.0
        )
    except asyncio.TimeoutError:
        print("Timed out, but operation continues")
        # important_operation() still runs

# Multiple timeouts
async def multiple_timeouts():
    tasks = [
        asyncio.wait_for(task1(), timeout=5.0),
        asyncio.wait_for(task2(), timeout=3.0),
        asyncio.wait_for(task3(), timeout=10.0)
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

**Related Terms**: Wait For, Cancel, Error

---

## Async Patterns

### Fan-out/Fan-in
```python
async def fan_out_fan_in():
    # Fan-out: distribute work
    tasks = [process_item(item) for item in items]
    
    # Fan-in: collect results
    results = await asyncio.gather(*tasks)
    return results
```

### Producer-Consumer
```python
async def producer_consumer():
    queue = asyncio.Queue()
    
    async def producer():
        for i in range(10):
            await queue.put(i)
        await queue.put(None)  # Sentinel
    
    async def consumer():
        while True:
            item = await queue.get()
            if item is None:
                break
            await process(item)
    
    await asyncio.gather(producer(), consumer())
```

### Pipeline
```python
async def pipeline():
    async def stage1(input_queue, output_queue):
        while True:
            item = await input_queue.get()
            if item is None:
                await output_queue.put(None)
                break
            result = await transform1(item)
            await output_queue.put(result)
    
    async def stage2(input_queue, output_queue):
        while True:
            item = await input_queue.get()
            if item is None:
                await output_queue.put(None)
                break
            result = await transform2(item)
            await output_queue.put(result)
    
    q1, q2, q3 = asyncio.Queue(), asyncio.Queue(), asyncio.Queue()
    await asyncio.gather(
        producer(q1),
        stage1(q1, q2),
        stage2(q2, q3),
        consumer(q3)
    )
```

---

## Performance Considerations

| Operation | Sync | Async | Recommendation |
|-----------|------|-------|----------------|
| HTTP requests | Blocking | Non-blocking | Use async |
| Database queries | Blocking | Non-blocking | Use async |
| File I/O | Blocking | Non-blocking | Use async |
| CPU computation | Uses thread | Same | Use sync in executor |
| Sleep | Blocking | Non-blocking | Use async |
| WebSocket | Blocking | Non-blocking | Use async |

---

## Summary

Understanding async programming is essential for building high-performance FastAPI applications. Key takeaways:

1. **Async/Await**: Use for non-blocking operations
2. **Event Loop**: Manages concurrent tasks
3. **Tasks**: Schedule coroutines for execution
4. **Gather**: Run multiple tasks concurrently
5. **Semaphores**: Limit concurrency
6. **AsyncClient**: Non-blocking HTTP requests
7. **Thread Pool**: Run blocking code safely
8. **Streaming**: Send data in chunks

**Next**: Move to the CORS lecture to learn about cross-origin resource sharing.
