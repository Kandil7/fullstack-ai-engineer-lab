# Glossary: Threading

## Quick Reference Table

| Term | Definition | Key Methods | Purpose |
|------|------------|-------------|---------|
| Thread | Lightweight process | `start()`, `join()`, `run()` | Concurrent execution |
| Lock | Mutual exclusion | `acquire()`, `release()` | Thread safety |
| RLock | Reentrant lock | `acquire()`, `release()` | Nested locking |
| Semaphore | Counting lock | `acquire()`, `release()` | Limit concurrency |
| Event | Signal mechanism | `set()`, `wait()`, `clear()` | Thread coordination |
| Condition | Wait for state | `wait()`, `notify()`, `notify_all()` | Producer-consumer |
| Queue | Thread-safe queue | `put()`, `get()`, `task_done()` | Data exchange |
| GIL | Global Interpreter Lock | N/A | Limits CPU parallelism |
| Daemon | Background thread | `daemon=True` | Auto-stop on exit |
| ThreadPool | Managed threads | `submit()`, `map()` | Simplified threading |

---

## Alphabetical Definitions

### Condition

**Definition**: A synchronization primitive that allows threads to wait until a particular condition is true, then be notified when it changes.

**Example**:
```python
import threading

condition = threading.Condition()
items = []

def producer():
    with condition:
        items.append("item")
        condition.notify()  # Wake up one waiting thread

def consumer():
    with condition:
        while not items:
            condition.wait()  # Wait for notification
        item = items.pop()
        print(f"Consumed: {item}")

t1 = threading.Thread(target=consumer)
t2 = threading.Thread(target=producer)
t1.start()
t2.start()
t1.join()
t2.join()
```

**Related Terms**: Event, Lock, producer-consumer

**Key Methods**:
- `wait()`: Wait for condition
- `notify()`: Wake up one waiting thread
- `notify_all()`: Wake up all waiting threads

---

### daemon

**Definition**: A thread that runs in the background and automatically stops when the main program exits. Daemon threads are useful for background tasks that shouldn't prevent program termination.

**Example**:
```python
import threading
import time

def background_task():
    while True:
        print("Background...")
        time.sleep(0.1)

# Daemon thread
daemon = threading.Thread(target=background_task, daemon=True)
daemon.start()

time.sleep(0.3)
print("Main exiting...")
# Daemon stops automatically
```

**Related Terms**: thread, background, lifecycle

---

### Event

**Definition**: A simple synchronization primitive used to signal between threads. One thread signals an event, and other threads wait for it.

**Example**:
```python
import threading
import time

event = threading.Event()

def waiter():
    print("Waiting for event...")
    event.wait()  # Blocks until event is set
    print("Event received!")

def setter():
    time.sleep(0.2)
    print("Setting event...")
    event.set()  # Signal waiting threads

t1 = threading.Thread(target=waiter)
t2 = threading.Thread(target=setter)
t1.start()
t2.start()
t1.join()
t2.join()
```

**Related Terms**: Condition, Lock, signaling

**Key Methods**:
- `set()`: Set the event, wake up waiters
- `clear()`: Reset the event
- `wait()`: Block until event is set
- `is_set()`: Check if event is set

---

### GIL (Global Interpreter Lock)

**Definition**: A mutex that protects access to Python objects, preventing multiple threads from executing Python bytecodes simultaneously. This limits CPU-bound parallelism but allows I/O-bound concurrency.

**Example**:
```python
import threading
import time

# CPU-bound task - GIL limits parallelism
def cpu_bound(n):
    return sum(i * i for i in range(n))

# With GIL, threads don't help CPU-bound tasks
start = time.time()
t1 = threading.Thread(target=cpu_bound, args=(10_000_000,))
t2 = threading.Thread(target=cpu_bound, args=(10_000_000,))
t1.start()
t2.start()
t1.join()
t2.join()
threaded_time = time.time() - start

# Sequential
start = time.time()
cpu_bound(10_000_000)
cpu_bound(10_000_000)
sequential_time = time.time() - start

print(f"Threaded: {threaded_time:.2f}s")
print(f"Sequential: {sequential_time:.2f}s")
# Threaded might be slower due to GIL overhead!
```

**Related Terms**: multiprocessing, I/O-bound, CPU-bound

**Impact**:
- ✅ I/O-bound: Threading works well
- ❌ CPU-bound: Use multiprocessing instead

---

### join

**Definition**: A method that blocks the calling thread until the thread whose `join()` was called completes.

**Example**:
```python
import threading
import time

def worker(name, delay):
    time.sleep(delay)
    print(f"{name} done")

t1 = threading.Thread(target=worker, args=("T1", 0.2))
t2 = threading.Thread(target=worker, args=("T2", 0.1))

t1.start()
t2.start()

print("Waiting for threads...")
t1.join()  # Block until T1 completes
t2.join()  # Block until T2 completes
print("All threads done")
```

**Related Terms**: start, lifecycle, synchronization

**Parameters**:
- `timeout`: Maximum seconds to wait (optional)

---

### Lock

**Definition**: A synchronization primitive that ensures only one thread can access a shared resource at a time. Prevents race conditions.

**Example**:
```python
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(1000):
        with lock:  # Only one thread at a time
            counter += 1

threads = [threading.Thread(target=increment) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Counter: {counter}")  # Always 10000
```

**Related Terms**: RLock, race condition, thread safety

**Key Methods**:
- `acquire()`: Acquire the lock
- `release()`: Release the lock

---

### Queue

**Definition**: A thread-safe FIFO queue for exchanging data between threads. Automatically handles synchronization.

**Example**:
```python
from queue import Queue
import threading

def producer(queue):
    for i in range(5):
        queue.put(f"item-{i}")
    queue.put(None)  # Sentinel

def consumer(queue):
    while True:
        item = queue.get()
        if item is None:
            break
        print(f"Processed: {item}")
        queue.task_done()

queue = Queue()
t1 = threading.Thread(target=producer, args=(queue,))
t2 = threading.Thread(target=consumer, args=(queue,))

t1.start()
t2.start()
t1.join()
t2.join()
```

**Related Terms**: producer-consumer, synchronization

**Key Methods**:
- `put()`: Add item to queue
- `get()`: Remove and return item
- `task_done()`: Signal item processed
- `join()`: Wait for all items to be processed

---

### race condition

**Definition**: A bug that occurs when multiple threads access and modify shared data concurrently, leading to unpredictable results.

**Example**:
```python
import threading

# WITHOUT LOCK - Race condition
counter = 0

def unsafe_increment():
    global counter
    for _ in range(1000):
        counter += 1  # Not atomic!

threads = [threading.Thread(target=unsafe_increment) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Expected: 10000, Actual: {counter}")  # Unpredictable!

# WITH LOCK - Safe
lock = threading.Lock()

def safe_increment():
    global counter
    for _ in range(1000):
        with lock:
            counter += 1
```

**Related Terms**: Lock, thread safety, synchronization

---

### RLock (Reentrant Lock)

**Definition**: A lock that can be acquired multiple times by the same thread without blocking. Useful for nested locking.

**Example**:
```python
import threading

class BankAccount:
    def __init__(self, balance):
        self._balance = balance
        self._lock = threading.RLock()
    
    def deposit(self, amount):
        with self._lock:
            self._balance += amount
    
    def transfer(self, other, amount):
        with self._lock:  # Acquire lock
            self._balance -= amount
            other.deposit(amount)  # Can acquire same lock again

# Regular Lock would deadlock here!
```

**Related Terms**: Lock, deadlock, nested locking

---

### Semaphore

**Definition**: A synchronization primitive that limits the number of threads that can access a resource simultaneously.

**Example**:
```python
import threading

semaphore = threading.Semaphore(3)  # Max 3 concurrent

def limited_task(name):
    with semaphore:
        print(f"{name} started")
        # Only 3 tasks run at a time
        import time
        time.sleep(0.1)
        print(f"{name} finished")

threads = [threading.Thread(target=limited_task, args=(f"T-{i}",)) 
           for i in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

**Related Terms**: Lock, concurrency, connection pool

---

### start

**Definition**: A method that begins the thread's execution by calling the `run()` method in a new thread of control.

**Example**:
```python
import threading

def worker():
    print("Working in thread")

t = threading.Thread(target=worker)
t.start()  # Begins execution
t.join()   # Wait for completion
```

**Related Terms**: join, run, lifecycle

---

### Thread

**Definition**: A separate sequence of execution within a program. Threads share memory space but have their own stack and instruction pointer.

**Example**:
```python
import threading

class MyThread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
    
    def run(self):
        print(f"{self.name} running")

t = MyThread("Worker")
t.start()
t.join()
```

**Related Terms**: daemon, GIL, synchronization

---

### ThreadPoolExecutor

**Definition**: A high-level interface for managing a pool of threads, simplifying thread creation and management.

**Example**:
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def process(item):
    return item * 2

items = [1, 2, 3, 4, 5]

with ThreadPoolExecutor(max_workers=3) as executor:
    # Method 1: map
    results = list(executor.map(process, items))
    
    # Method 2: submit
    futures = [executor.submit(process, item) for item in items]
    results = [f.result() for f in futures]

print(f"Results: {results}")
```

**Related Terms**: thread, concurrent.futures, pool

---

### thread safety

**Definition**: Code that functions correctly during simultaneous execution by multiple threads, using synchronization to prevent race conditions.

**Example**:
```python
import threading

class ThreadSafeCounter:
    def __init__(self):
        self._count = 0
        self._lock = threading.Lock()
    
    def increment(self):
        with self._lock:
            self._count += 1
    
    @property
    def count(self):
        with self._lock:
            return self._count
```

**Related Terms**: Lock, race condition, synchronization

---

## Concept Relationships

```
Threading
├── Thread Management
│   ├── Thread class
│   ├── start(), join(), daemon
│   └── ThreadPoolExecutor
│
├── Synchronization
│   ├── Lock / RLock (mutual exclusion)
│   ├── Semaphore (limited concurrency)
│   ├── Event (signaling)
│   └── Condition (wait/notify)
│
├── Data Exchange
│   ├── Queue (thread-safe)
│   └── Shared variables (with locks)
│
├── Challenges
│   ├── GIL (limits CPU parallelism)
│   ├── Race conditions
│   └── Deadlocks
│
└── Use Cases
    ├── I/O-bound tasks
    ├── GUI responsiveness
    └── Background tasks
```

---

## When to Use Threading

| Use Case | Recommendation |
|----------|----------------|
| I/O-bound (network, file) | ✅ Use threading |
| CPU-bound (computations) | ❌ Use multiprocessing |
| GUI responsiveness | ✅ Use threading |
| Simple concurrency | ✅ Use ThreadPoolExecutor |
| Complex coordination | ⚠️ Consider asyncio |

---

## Common Patterns

### 1. Worker Pool Pattern
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_item, items))
```

### 2. Producer-Consumer Pattern
```python
from queue import Queue

queue = Queue()

def producer():
    for item in items:
        queue.put(item)
    queue.put(None)

def consumer():
    while True:
        item = queue.get()
        if item is None:
            break
        process(item)
```

### 3. Thread-Safe Counter
```python
class SafeCounter:
    def __init__(self):
        self._count = 0
        self._lock = threading.Lock()
    
    def increment(self):
        with self._lock:
            self._count += 1
```

### 4. Event Coordination
```python
event = threading.Event()

def waiter():
    event.wait()
    print("Event received")

def setter():
    event.set()

# Start setter after waiter
```
