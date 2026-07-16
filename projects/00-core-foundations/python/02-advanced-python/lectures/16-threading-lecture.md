# Lecture 16: Threading

## Topic Overview

Threading allows concurrent execution of code, making it ideal for I/O-bound tasks like file operations, network requests, and user interactions. Python's `threading` module provides tools for creating and managing threads, synchronization, and coordination.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Create and manage threads** using the threading module
2. **Understand the GIL** and its impact on threading
3. **Use synchronization primitives** (Lock, RLock, Semaphore)
4. **Implement thread-safe data structures**
5. **Build producer-consumer patterns** with Queue
6. **Use ThreadPoolExecutor** for simplified thread management
7. **Handle thread exceptions** and return values

---

## Key Concepts

### 1. Basic Thread

Threads are lightweight processes that share memory space.

#### Creating Threads

```python
import threading
import time

def worker(name, delay):
    print(f"[{name}] Starting")
    time.sleep(delay)
    print(f"[{name}] Finished")

# Create threads
t1 = threading.Thread(target=worker, args=("Thread-1", 0.3))
t2 = threading.Thread(target=worker, args=("Thread-2", 0.1))

# Start threads
t1.start()
t2.start()

# Wait for completion
t1.join()
t2.join()
print("Both threads completed")
```

#### Thread with Function and Arguments

```python
import threading
import time

def download_file(url, timeout=30):
    print(f"Downloading {url}...")
    time.sleep(0.5)  # Simulate download
    return f"Data from {url}"

# Create threads with different arguments
threads = []
for i in range(3):
    t = threading.Thread(
        target=download_file,
        args=(f"http://example.com/file{i}.txt",),
        kwargs={"timeout": 10}
    )
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("All downloads complete")
```

---

### 2. Thread with Return Value

Threads don't return values directly, but you can capture them using containers or callbacks.

#### Using a Container

```python
import threading

def compute_square(n, result_container):
    result_container[n] = n ** 2

results = {}
threads = []

for i in range(5):
    t = threading.Thread(target=compute_square, args=(i, results))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Results: {results}")
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

#### Using ThreadResult Helper

```python
import threading

class ThreadResult:
    def __init__(self):
        self._result = None
        self._exception = None
    
    @property
    def result(self):
        if self._exception:
            raise self._exception
        return self._result
    
    def set_result(self, result):
        self._result = result
    
    def set_exception(self, exception):
        self._exception = exception

def compute(n, result):
    try:
        time.sleep(0.1)
        result.set_result(n ** 2)
    except Exception as e:
        result.set_exception(e)

results = []
threads = []

for i in range(5):
    tr = ThreadResult()
    t = threading.Thread(target=compute, args=(i, tr))
    results.append(tr)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Results: {[r.result for r in results]}")
```

---

### 3. Lock and RLock

Locks ensure thread-safe access to shared resources.

#### Basic Lock

```python
import threading

class Counter:
    def __init__(self):
        self._count = 0
        self._lock = threading.Lock()
    
    def increment(self):
        with self._lock:
            self._count += 1
    
    @property
    def count(self):
        return self._count

counter = Counter()

def increment_many(n):
    for _ in range(n):
        counter.increment()

threads = []
for _ in range(10):
    t = threading.Thread(target=increment_many, args=(1000,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Expected: 10000, Actual: {counter.count}")
# Without lock: race condition, unpredictable result
# With lock: always 10000
```

#### Reentrant Lock (RLock)

```python
import threading

class BankAccount:
    def __init__(self, balance=0):
        self._balance = balance
        self._lock = threading.RLock()  # Reentrant lock
    
    def deposit(self, amount):
        with self._lock:
            self._balance += amount
    
    def withdraw(self, amount):
        with self._lock:
            if self._balance >= amount:
                self._balance -= amount
                return True
            return False
    
    def transfer(self, other, amount):
        with self._lock:
            if self._balance >= amount:
                self._balance -= amount
                other.deposit(amount)  # Can acquire lock again
                return True
            return False
    
    @property
    def balance(self):
        return self._balance

# RLock allows the same thread to acquire the lock multiple times
account1 = BankAccount(1000)
account2 = BankAccount(500)
account1.transfer(account2, 200)
print(f"Account1: ${account1.balance}")  # $800
print(f"Account2: ${account2.balance}")  # $700
```

---

### 4. Semaphore

Semaphores control access to a resource with a limited number of permits.

```python
import threading
import time

semaphore = threading.Semaphore(2)  # Max 2 concurrent

def limited_task(name):
    with semaphore:
        print(f"{name} started")
        time.sleep(0.1)
        print(f"{name} finished")

threads = []
for i in range(5):
    t = threading.Thread(target=limited_task, args=(f"Task-{i}",))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

#### BoundedSemaphore

```python
import threading

# BoundedSemaphore cannot be released more times than acquired
bounded = threading.BoundedSemaphore(2)

bounded.acquire()  # OK
bounded.acquire()  # OK
try:
    bounded.release()  # OK
    bounded.release()  # OK
    bounded.release()  # ValueError - released too many times
except ValueError as e:
    print(f"Error: {e}")
```

---

### 5. Producer-Consumer Pattern

Classic pattern for decoupling producers and consumers.

```python
import threading
import time
from queue import Queue

def producer(queue, count):
    for i in range(count):
        item = f"item-{i}"
        queue.put(item)
        print(f"Produced: {item}")
        time.sleep(0.01)
    queue.put(None)  # Sentinel to stop consumer

def consumer(queue):
    while True:
        item = queue.get()
        if item is None:
            break
        print(f"Consumed: {item}")
        time.sleep(0.02)
        queue.task_done()

queue = Queue(maxsize=5)

prod = threading.Thread(target=producer, args=(queue, 10))
cons = threading.Thread(target=consumer, args=(queue,))

prod.start()
cons.start()

prod.join()
cons.join()
print("Producer-Consumer complete")
```

---

### 6. Event and Condition

Synchronization primitives for thread coordination.

#### Event

```python
import threading
import time

event = threading.Event()

def waiter():
    print("Waiter: Waiting for event...")
    event.wait()
    print("Waiter: Event received!")

def setter():
    time.sleep(0.2)
    print("Setter: Setting event")
    event.set()

t1 = threading.Thread(target=waiter)
t2 = threading.Thread(target=setter)

t1.start()
t2.start()

t1.join()
t2.join()
```

#### Condition

```python
import threading
import time

condition = threading.Condition()
items = []

def producer():
    with condition:
        for i in range(5):
            items.append(i)
            print(f"Produced: {i}")
            condition.notify()
        condition.notify_all()

def consumer(name):
    with condition:
        while not items:
            print(f"{name}: Waiting...")
            condition.wait()
        item = items.pop(0)
        print(f"{name}: Consumed {item}")

# Start consumers first
consumers = []
for i in range(3):
    t = threading.Thread(target=consumer, args=(f"Consumer-{i}",))
    consumers.append(t)
    t.start()

time.sleep(0.1)

# Start producer
prod = threading.Thread(target=producer)
prod.start()

for t in consumers:
    t.join()
prod.join()
```

---

### 7. Thread Pool (concurrent.futures)

Simplified thread management using ThreadPoolExecutor.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def fetch_url(url):
    time.sleep(0.1)  # Simulate network request
    return f"Data from {url}"

urls = [f"http://example.com/page{i}" for i in range(5)]

# Method 1: map
with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(fetch_url, urls))
print(f"Map results: {len(results)} items")

# Method 2: submit with as_completed
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {executor.submit(fetch_url, url): url for url in urls}
    results = {}
    for future in as_completed(futures):
        url = futures[future]
        results[url] = future.result()

print(f"Submit results: {len(results)} items")
```

---

### 8. Daemon Threads

Daemon threads stop when the main program exits.

```python
import threading
import time

def background_task():
    while True:
        print("Background running...")
        time.sleep(0.1)

# Daemon process stops when main process exits
daemon = threading.Thread(target=background_task, daemon=True)
daemon.start()
time.sleep(0.3)
print("Main process exiting (daemon will stop)")
```

---

## Common Mistakes to Avoid

### 1. Race Conditions

```python
# WITHOUT LOCK - Race condition
counter = 0

def increment():
    global counter
    for _ in range(1000):
        counter += 1  # Not atomic!

threads = [threading.Thread(target=increment) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Expected: 10000, Actual: {counter}")  # Unpredictable!

# WITH LOCK - Thread safe
lock = threading.Lock()

def safe_increment():
    global counter
    for _ in range(1000):
        with lock:
            counter += 1
```

### 2. Not Joining Threads

```python
# WRONG - might exit before threads complete
t = threading.Thread(target=long_running_task)
t.start()
# Program might exit here!

# CORRECT - always join
t = threading.Thread(target=long_running_task)
t.start()
t.join()  # Wait for completion
```

### 3. Forgetting Sentinel Values

```python
# WRONG - consumer runs forever
def consumer(queue):
    while True:
        item = queue.get()
        process(item)

# CORRECT - use sentinel
def consumer(queue):
    while True:
        item = queue.get()
        if item is None:  # Sentinel
            break
        process(item)
```

---

## Best Practices

### 1. Use Context Managers

```python
import threading

lock = threading.Lock()

# GOOD
with lock:
    shared_resource += 1

# BAD
lock.acquire()
try:
    shared_resource += 1
finally:
    lock.release()
```

### 2. Minimize Shared State

```python
# BETTER - each thread has its own data
def worker(thread_id):
    local_data = []  # Thread-local
    for i in range(100):
        local_data.append(f"{thread_id}-{i}")
    return local_data
```

### 3. Use ThreadPoolExecutor for Most Cases

```python
from concurrent.futures import ThreadPoolExecutor

# Simpler than manual thread management
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_item, items))
```

---

## Practice Exercises

### Exercise 1: Thread-Safe Queue
```python
"""
Implement a thread-safe bounded queue with:
- put() and get() methods
- Maximum size limit
- Proper synchronization
"""
class BoundedQueue:
    # Your code here
    pass
```

### Exercise 2: Web Scraper
```python
"""
Create a thread pool web scraper that:
- Downloads multiple URLs concurrently
- Handles errors gracefully
- Returns results in order
"""
# Your code here
```

### Exercise 3: Thread Pool Calculator
```python
"""
Implement a thread pool that:
- Processes a list of numbers concurrently
- Calculates squares, cubes, and factorials
- Returns results as a dictionary
"""
# Your code here
```

---

## Summary

### Synchronization Primitives

| Primitive | Purpose | Use Case |
|-----------|---------|----------|
| `Lock` | Mutual exclusion | Protect shared resources |
| `RLock` | Reentrant lock | Nested locking |
| `Semaphore` | Limit concurrency | Connection pools |
| `Event` | Signal between threads | Coordination |
| `Condition` | Wait for condition | Producer-consumer |

### When to Use Threading

| Use Case | Recommendation |
|----------|----------------|
| I/O-bound tasks | ✅ Use threading |
| CPU-bound tasks | ❌ Use multiprocessing |
| Simple concurrency | ✅ Use ThreadPoolExecutor |
| Complex coordination | ⚠️ Consider asyncio |

### Key Takeaways

1. **Threads share memory** - use locks for thread safety
2. **GIL limits CPU parallelism** - use multiprocessing for CPU-bound
3. **Use ThreadPoolExecutor** for simpler thread management
4. **Always join threads** before exiting
5. **Use daemon threads** for background tasks
6. **Minimize shared state** to reduce synchronization needs

---

## Further Reading

- [Python threading documentation](https://docs.python.org/3/library/threading.html)
- [concurrent.futures documentation](https://docs.python.org/3/library/concurrent.futures.html)
- [GIL documentation](https://docs.python.org/3/glossary.html#term-global-interpreter-lock)
