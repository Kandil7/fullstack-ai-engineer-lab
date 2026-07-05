# Advanced Python Lecture 04: Async/Await

## Topic Overview

Asynchronous programming enables writing concurrent code that can handle many I/O-bound operations efficiently without threads or processes. Python's `async`/`await` syntax (introduced in Python 3.5) provides a clean, readable way to write asynchronous code using coroutines, event loops, and asynchronous libraries. This is critical for building responsive applications, handling concurrent network requests, and building AI systems that need to process multiple requests simultaneously.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand the difference between concurrency, parallelism, and asynchrony
2. Define and use coroutines with `async def` and `await`
3. Work with the `asyncio` event loop
4. Run concurrent tasks with `asyncio.gather()` and `asyncio.create_task()`
5. Handle timeouts and cancellation
6. Use asynchronous context managers and iterators
7. Implement producer-consumer patterns with async queues
8. Build async generators for streaming data
9. Apply async patterns to AI engineering workflows
10. Debug async code effectively

---

## 1. Foundations of Asynchrony

### Concurrency vs Parallelism

```python
# Concurrency: Interleaving tasks (one CPU, switching between tasks)
# Parallelism: Simultaneous execution (multiple CPUs)

# Asynchronous programming achieves concurrency through:
# - Non-blocking I/O
# - Event loop that switches tasks during waits
# - Coroutines that yield control back to the loop
```

### Why Async/Await?

```python
# Synchronous: Blocks during I/O
def fetch_data_sync(urls):
    results = []
    for url in urls:
        response = requests.get(url)  # Blocks here!
        results.append(response.json())
    return results
# Total time: sum of all request times

# Asynchronous: Overlaps I/O operations
async def fetch_data_async(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks)
# Total time: ~max of all request times
```

---

## 2. Coroutines

### Basic Coroutine

```python
import asyncio

async def greet(name):
    """A basic coroutine."""
    print(f"Hello, {name}!")
    await asyncio.sleep(1)  # Simulates async I/O
    return f"Goodbye, {name}!"

# Must run in an event loop
result = asyncio.run(greet("Alice"))
print(result)
```

### Coroutine vs Generator

```python
# Generator (uses yield)
def gen():
    yield 1
    yield 2

# Coroutine (uses await)
async def coro():
    await asyncio.sleep(1)
    return 42

# Key difference: coroutines are scheduled on event loop
```

### Awaitable Objects

```python
# Things you can await:
# 1. Coroutines (async def functions)
# 2. Tasks (created with asyncio.create_task)
# 3. Futures (low-level)
# 4. Objects with __await__ method

async def example():
    # Await a coroutine
    result = await some_coroutine()
    
    # Await a task
    task = asyncio.create_task(another_coroutine())
    result = await task
    
    # Await multiple tasks
    results = await asyncio.gather(
        task1(),
        task2(),
        task3()
    )
```

---

## 3. The Event Loop

### Running the Event Loop

```python
import asyncio

async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

# Method 1: asyncio.run (Python 3.7+) - preferred
asyncio.run(main())

# Method 2: Get and manage the loop manually
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

# Method 3: In Jupyter notebooks
# await main()  (already in async context)
```

### Creating and Managing Tasks

```python
import asyncio

async def fetch_data(url, delay):
    print(f"Fetching {url}")
    await asyncio.sleep(delay)
    return f"Data from {url}"

async def main():
    # Create tasks (schedules them to run concurrently)
    task1 = asyncio.create_task(fetch_data("api1.com", 2))
    task2 = asyncio.create_task(fetch_data("api2.com", 1))
    task3 = asyncio.create_task(fetch_data("api3.com", 3))
    
    # All three run concurrently
    result1 = await task1
    result2 = await task2
    result3 = await task3
    
    print(f"Results: {result1}, {result2}, {result3}")

asyncio.run(main())
# Total time: ~3 seconds (not 6!)
```

### `asyncio.gather()`

```python
import asyncio

async def process(item):
    await asyncio.sleep(1)
    return item * 2

async def main():
    # Run multiple coroutines concurrently
    results = await asyncio.gather(
        process(1),
        process(2),
        process(3),
        process(4),
    )
    print(results)  # [2, 4, 6, 8]

asyncio.run(main())
```

---

## 4. Error Handling in Async Code

```python
import asyncio

async def risky_operation():
    await asyncio.sleep(0.5)
    raise ValueError("Something went wrong!")

async def safe_operation():
    await asyncio.sleep(1)
    return "Success"

async def main():
    # gather with return_exceptions=True
    results = await asyncio.gather(
        risky_operation(),
        safe_operation(),
        return_exceptions=True  # Exceptions returned as values
    )
    
    for result in results:
        if isinstance(result, Exception):
            print(f"Error: {result}")
        else:
            print(f"Result: {result}")

asyncio.run(main())
```

### Exception Groups (Python 3.11+)

```python
import asyncio

async def fail1():
    raise ValueError("Error 1")

async def fail2():
    raise TypeError("Error 2")

async def main():
    try:
        await asyncio.gather(fail1(), fail2())
    except* ValueError as eg:
        print(f"ValueErrors: {eg.exceptions}")
    except* TypeError as eg:
        print(f"TypeErrors: {eg.exceptions}")

asyncio.run(main())
```

---

## 5. Timeouts and Cancellation

### Timeouts

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

### Cancellation

```python
import asyncio

async def long_running():
    try:
        while True:
            print("Working...")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Task was cancelled!")
        raise  # Re-raise to properly clean up

async def main():
    task = asyncio.create_task(long_running())
    await asyncio.sleep(3)
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        print("Task cancelled successfully")

asyncio.run(main())
```

### `asyncio.wait()`

```python
import asyncio

async def worker(name, delay):
    await asyncio.sleep(delay)
    return f"{name} done"

async def main():
    tasks = [
        asyncio.create_task(worker("A", 2)),
        asyncio.create_task(worker("B", 1)),
        asyncio.create_task(worker("C", 3)),
    ]
    
    # Wait for first completed
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_COMPLETED
    )
    
    for task in done:
        print(f"Completed: {task.result()}")
    
    # Cancel remaining
    for task in pending:
        task.cancel()

asyncio.run(main())
```

---

## 6. Async Context Managers and Iterators

### Async Context Managers

```python
import asyncio

class AsyncDatabase:
    async def __aenter__(self):
        print("Connecting...")
        await asyncio.sleep(0.5)
        self.connection = "connected"
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Disconnecting...")
        await asyncio.sleep(0.5)
        self.connection = None
        return False
    
    async def query(self, sql):
        await asyncio.sleep(0.1)
        return f"Results for: {sql}"

async def main():
    async with AsyncDatabase() as db:
        result = await db.query("SELECT * FROM users")
        print(result)

asyncio.run(main())
```

### Using `contextlib.asynccontextmanager`

```python
import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def managed_resource(name):
    print(f"Acquiring {name}")
    await asyncio.sleep(0.5)
    resource = {"name": name, "active": True}
    
    try:
        yield resource
    finally:
        print(f"Releasing {name}")
        resource["active"] = False

async def main():
    async with managed_resource("cache") as cache:
        print(f"Using {cache['name']}")

asyncio.run(main())
```

### Async Iterators

```python
import asyncio

class AsyncCounter:
    def __init__(self, stop):
        self.current = 0
        self.stop = stop
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current >= self.stop:
            raise StopAsyncIteration
        await asyncio.sleep(0.1)
        self.current += 1
        return self.current - 1

async def main():
    async for num in AsyncCounter(5):
        print(num)  # 0, 1, 2, 3, 4

asyncio.run(main())
```

### Async Generators

```python
import asyncio

async def async_range(start, stop):
    """Async generator using async yield."""
    current = start
    while current < stop:
        await asyncio.sleep(0.1)
        yield current
        current += 1

async def main():
    async for num in async_range(0, 5):
        print(num)

asyncio.run(main())
```

---

## 7. Async Queues

```python
import asyncio
import random

async def producer(queue, name):
    for i in range(5):
        item = f"{name}-{i}"
        await queue.put(item)
        print(f"Produced: {item}")
        await asyncio.sleep(random.uniform(0.1, 0.5))

async def consumer(queue, name):
    while True:
        item = await queue.get()
        print(f"{name} consumed: {item}")
        await asyncio.sleep(random.uniform(0.1, 0.3))
        queue.task_done()

async def main():
    queue = asyncio.Queue(maxsize=10)
    
    # Start producers and consumers
    producers = [
        asyncio.create_task(producer(queue, f"P{i}"))
        for i in range(2)
    ]
    consumers = [
        asyncio.create_task(consumer(queue, f"C{i}"))
        for i in range(3)
    ]
    
    # Wait for all producers to finish
    await asyncio.gather(*producers)
    
    # Wait for queue to be empty
    await queue.join()
    
    # Cancel consumers
    for c in consumers:
        c.cancel()

asyncio.run(main())
```

---

## 8. Async Patterns for AI Engineering

### Concurrent API Calls

```python
import asyncio
import aiohttp

async def fetch_model_response(session, prompt, model):
    url = f"https://api.example.com/v1/chat"
    async with session.post(url, json={"prompt": prompt, "model": model}) as resp:
        return await resp.json()

async def process_batch(prompts, model="gpt-4"):
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_model_response(session, prompt, model)
            for prompt in prompts
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if not isinstance(r, Exception)]

async def main():
    prompts = ["What is AI?", "Explain ML", "What is RAG?"]
    results = await process_batch(prompts)
    print(results)
```

### Async Data Pipeline

```python
import asyncio

async def read_chunks(source):
    """Async generator yielding data chunks."""
    for chunk in source:
        await asyncio.sleep(0.01)  # Simulate I/O
        yield chunk

async def process_chunk(chunk):
    """Process a single chunk."""
    await asyncio.sleep(0.05)  # Simulate processing
    return chunk.upper()

async def pipeline(source):
    """Async pipeline processing."""
    results = []
    async for chunk in read_chunks(source):
        result = await process_chunk(chunk)
        results.append(result)
    return results

async def main():
    data = ["hello", "world", "async", "python"]
    results = await pipeline(data)
    print(results)

asyncio.run(main())
```

### Rate-Limited API Access

```python
import asyncio
import time

class AsyncRateLimiter:
    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
    
    async def acquire(self):
        now = time.time()
        # Remove old calls
        self.calls = [t for t in self.calls if now - t < self.period]
        
        if len(self.calls) >= self.max_calls:
            # Wait until oldest call expires
            sleep_time = self.period - (now - self.calls[0])
            await asyncio.sleep(sleep_time)
        
        self.calls.append(time.time())
    
    async def __aenter__(self):
        await self.acquire()
        return self
    
    async def __aexit__(self, *args):
        pass

async def call_api(endpoint, limiter):
    async with limiter:
        print(f"Calling {endpoint}")
        await asyncio.sleep(0.1)  # Actual API call
        return f"Response from {endpoint}"

async def main():
    limiter = AsyncRateLimiter(max_calls=5, period=1.0)
    endpoints = [f"api/endpoint/{i}" for i in range(20)]
    
    tasks = [call_api(ep, limiter) for ep in endpoints]
    results = await asyncio.gather(*tasks)
    print(f"Completed {len(results)} calls")

asyncio.run(main())
```

---

## 9. Common Mistakes to Avoid

### Mistake 1: Blocking in Async Code

```python
# BAD: Blocking the event loop
async def bad_example():
    import time
    time.sleep(5)  # Blocks entire event loop!
    return "done"

# GOOD: Use async sleep
async def good_example():
    await asyncio.sleep(5)  # Yields control to event loop
    return "done"
```

### Mistake 2: Forgetting to `await`

```python
# BAD: Coroutine never runs
async def example():
    fetch_data()  # Missing await! Coroutine created but not awaited

# GOOD: Actually await the coroutine
async def example():
    result = await fetch_data()
```

### Mistake 3: Creating Tasks Without Tracking

```python
# BAD: Tasks can be garbage collected
async def bad_example():
    asyncio.create_task(long_running())  # Task might be GC'd!

# GOOD: Keep references to tasks
async def good_example():
    task = asyncio.create_task(long_running())
    await task  # Or keep in a set
```

---

## 10. Best Practices

1. **Use `asyncio.run()`** as the entry point for async programs
2. **Never mix sync and async** without proper handling (`asyncio.to_thread()`)
3. **Use `asyncio.gather()`** for concurrent task execution
4. **Set timeouts** to prevent hanging operations
5. **Use `return_exceptions=True`** in gather for fault tolerance
6. **Keep references to tasks** to prevent garbage collection
7. **Use async context managers** for resource management
8. **Use async generators** for streaming data
9. **Profile async code** — async doesn't always mean faster
10. **Use `asyncio.Semaphore`** to limit concurrency

---

## 11. Practice Exercises

### Exercise 1: Async Web Scraper
Build an async scraper that fetches multiple URLs concurrently:

```python
async def scrape_urls(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)
```

### Exercise 2: Async Producer-Consumer
Implement an async producer-consumer system with rate limiting:

```python
async def producer_consumer():
    queue = asyncio.Queue(maxsize=100)
    # Producers add items, consumers process them
    # Limit to 10 concurrent consumers
```

### Exercise 3: Async Retry Decorator
Create an async retry decorator with exponential backoff:

```python
@async_retry(max_attempts=3, backoff=2.0)
async def unreliable_api_call():
    # May fail intermittently
    pass
```

### Exercise 4: Async Pipeline
Build an async data pipeline with stages:

```python
async def pipeline():
    async for data in read_source():
        processed = await validate(data)
        transformed = await transform(processed)
        await store(transformed)
```

---

## 12. Summary

| Concept | Description |
|---------|-------------|
| **Coroutine** | Function defined with `async def` |
| **`await`** | Pauses coroutine until awaited object completes |
| **Event Loop** | Manages and schedules coroutine execution |
| **`asyncio.run()`** | Entry point for async programs |
| **`asyncio.gather()`** | Run multiple coroutines concurrently |
| **`asyncio.create_task()`** | Schedule a coroutine as a task |
| **`async with`** | Async context manager usage |
| **`async for`** | Async iterator/generator iteration |
| **`asyncio.Queue`** | Async-safe queue for producer-consumer |
| **`asyncio.Semaphore`** | Limit concurrent operations |

Async/await is essential for building responsive, scalable Python applications. In AI engineering, it enables concurrent API calls, real-time data streaming, and efficient resource utilization — all critical for production systems handling multiple simultaneous requests.

---

## Next Steps

In the next lecture, we'll explore **Type Hints**, which work beautifully with async code to provide better IDE support and catch errors early.
