# Glossary: Multiprocessing

## Quick Reference Table

| Term | Definition | Key Methods | Purpose |
|------|------------|-------------|---------|
| Process | Independent execution unit | `start()`, `join()`, `terminate()` | Parallel execution |
| Pool | Managed process pool | `map()`, `apply()`, `close()` | Simple parallelism |
| Queue | Process-safe queue | `put()`, `get()`, `empty()` | IPC (Inter-Process Communication) |
| Value | Shared memory (single) | `value`, `get_lock()` | Share simple values |
| Array | Shared memory (array) | `array`, `get_lock()` | Share arrays |
| Manager | Shared objects | `dict()`, `list()`, `Value()` | Complex shared state |
| Lock | Process synchronization | `acquire()`, `release()` | Process safety |
| Pipe | Bidirectional channel | `send()`, `recv()`, `close()` | Direct IPC |
| daemon | Background process | `daemon=True` | Auto-stop on exit |
| GIL | Global Interpreter Lock | N/A | Bypassed by multiprocessing |

---

## Alphabetical Definitions

### Array

**Definition**: A shared memory array that can be accessed by multiple processes. Provides a process-safe way to share numerical data.

**Example**:
```python
import multiprocessing

def fill_array(shared_arr, index, value):
    shared_arr[index] = value

if __name__ == "__main__":
    arr = multiprocessing.Array('i', [0, 0, 0, 0, 0])
    
    processes = []
    for i in range(5):
        p = multiprocessing.Process(target=fill_array, args=(arr, i, i * 10))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print(f"Array: {list(arr)}")  # [0, 10, 20, 30, 40]
```

**Related Terms**: Value, shared memory, Manager

**Type Codes**:
- `'i'`: signed int
- `'d'`: double
- `'f'`: float
- `'c'`: char

---

### daemon

**Definition**: A process that runs in the background and automatically terminates when the main process exits. Daemon processes are useful for background tasks.

**Example**:
```python
import multiprocessing
import time

def background_task():
    while True:
        print("Background...")
        time.sleep(0.1)

if __name__ == "__main__":
    daemon = multiprocessing.Process(target=background_task, daemon=True)
    daemon.start()
    time.sleep(0.3)
    print("Main exiting (daemon stops)")
```

**Related Terms**: Process, lifecycle, background

---

### GIL (Global Interpreter Lock)

**Definition**: A mutex that protects access to Python objects, preventing multiple threads from executing Python bytecodes simultaneously. Multiprocessing bypasses the GIL by using separate processes.

**Example**:
```python
import multiprocessing
import threading
import time

def cpu_bound(n):
    return sum(i * i for i in range(n))

# Threading - limited by GIL
start = time.time()
t1 = threading.Thread(target=cpu_bound, args=(10_000_000,))
t2 = threading.Thread(target=cpu_bound, args=(10_000_000,))
t1.start(); t2.start()
t1.join(); t2.join()
print(f"Threading: {time.time() - start:.2f}s")

# Multiprocessing - true parallelism
start = time.time()
p1 = multiprocessing.Process(target=cpu_bound, args=(10_000_000,))
p2 = multiprocessing.Process(target=cpu_bound, args=(10_000_000,))
p1.start(); p2.start()
p1.join(); p2.join()
print(f"Multiprocessing: {time.time() - start:.2f}s")
```

**Related Terms**: threading, CPU-bound, I/O-bound

---

### join

**Definition**: A method that blocks the calling process until the process whose `join()` was called completes.

**Example**:
```python
import multiprocessing
import time

def worker(name, delay):
    time.sleep(delay)
    print(f"{name} done")

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=worker, args=("P1", 0.2))
    p2 = multiprocessing.Process(target=worker, args=("P2", 0.1))
    
    p1.start()
    p2.start()
    
    p1.join()  # Wait for P1
    p2.join()  # Wait for P2
    
    print("All processes done")
```

**Related Terms**: start, lifecycle, synchronization

---

### Lock

**Definition**: A synchronization primitive that ensures only one process can access a shared resource at a time. Prevents race conditions.

**Example**:
```python
import multiprocessing

def increment(shared_val, n, lock):
    for _ in range(n):
        with lock:
            shared_val.value += 1

if __name__ == "__main__":
    counter = multiprocessing.Value('i', 0)
    lock = multiprocessing.Lock()
    
    processes = []
    for _ in range(4):
        p = multiprocessing.Process(target=increment, args=(counter, 1000, lock))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print(f"Counter: {counter.value}")  # 4000
```

**Related Terms**: race condition, synchronization, Value

---

### Manager

**Definition**: A server process that allows other processes to manipulate Python objects (dicts, lists, etc.) through shared proxies.

**Example**:
```python
import multiprocessing

def update_dict(shared_dict, key, value):
    shared_dict[key] = value

if __name__ == "__main__":
    manager = multiprocessing.Manager()
    shared_dict = manager.dict()
    
    processes = []
    for i in range(5):
        p = multiprocessing.Process(
            target=update_dict,
            args=(shared_dict, f"key{i}", i * 10)
        )
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print(f"Dict: {dict(shared_dict)}")
```

**Related Terms**: Value, Array, shared state

**Supported Types**:
- `dict()` / `dict({...})`
- `list()` / `list([...])`
- `Value()`
- `Namespace()`
- `Queue()`
- `Lock()` / `RLock()` / `Semaphore()`

---

### Pool

**Definition**: A managed group of worker processes that can execute functions in parallel. Provides convenient methods like `map()`, `apply()`, and `starmap()`.

**Example**:
```python
import multiprocessing

def square(n):
    return n ** 2

if __name__ == "__main__":
    with multiprocessing.Pool(processes=4) as pool:
        numbers = [1, 2, 3, 4, 5]
        
        # map - returns results in order
        results = pool.map(square, numbers)
        print(f"Squares: {results}")
        
        # starmap - unpacks arguments
        def power(base, exp):
            return base ** exp
        results = pool.starmap(power, [(2, 3), (3, 4)])
        print(f"Powers: {results}")
```

**Related Terms**: Process, map, parallel

**Key Methods**:
- `map(func, iterable)`: Map function to items
- `map_async(func, iterable)`: Async version
- `starmap(func, iterable)`: Unpack arguments
- `apply(func, args)`: Apply function
- `apply_async(func, args)`: Async version
- `close()`: Prevent more tasks
- `terminate()`: Stop workers
- `join()`: Wait for completion

---

### Pipe

**Definition**: A bidirectional communication channel between two processes. More efficient than Queue for simple two-process communication.

**Example**:
```python
import multiprocessing

def sender(conn):
    conn.send({"message": "Hello"})
    conn.send(None)  # Sentinel
    conn.close()

def receiver(conn):
    while True:
        msg = conn.recv()
        if msg is None:
            break
        print(f"Received: {msg}")

if __name__ == "__main__":
    parent_conn, child_conn = multiprocessing.Pipe()
    
    p1 = multiprocessing.Process(target=sender, args=(parent_conn,))
    p2 = multiprocessing.Process(target=receiver, args=(child_conn,))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
```

**Related Terms**: Queue, IPC, communication

**Methods**:
- `send()`: Send object
- `recv()`: Receive object
- `poll()`: Check for data
- `close()`: Close pipe

---

### Process

**Definition**: An independent execution unit with its own memory space and Python interpreter. Processes are heavier than threads but bypass the GIL.

**Example**:
```python
import multiprocessing
import os

def worker(name):
    print(f"[{name}] PID: {os.getpid()}")

if __name__ == "__main__":
    processes = []
    for i in range(3):
        p = multiprocessing.Process(target=worker, args=(f"P-{i}",))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
```

**Related Terms**: Pool, thread, GIL

**Key Methods**:
- `start()`: Start process
- `join()`: Wait for completion
- `terminate()`: Stop process
- `is_alive()`: Check if running
- `pid`: Process ID

---

### Queue

**Definition**: A process-safe FIFO queue for exchanging data between processes. Automatically handles synchronization.

**Example**:
```python
import multiprocessing

def producer(q, count):
    for i in range(count):
        q.put(f"item-{i}")
    q.put(None)  # Sentinel

def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break
        print(f"Processed: {item}")

if __name__ == "__main__":
    q = multiprocessing.Queue()
    
    prod = multiprocessing.Process(target=producer, args=(q, 5))
    cons = multiprocessing.Process(target=consumer, args=(q,))
    
    prod.start()
    cons.start()
    
    prod.join()
    cons.join()
```

**Related Terms**: Pipe, IPC, producer-consumer

**Key Methods**:
- `put()`: Add item
- `get()`: Remove item
- `empty()`: Check if empty
- `qsize()`: Get size

---

### race condition

**Definition**: A bug that occurs when multiple processes access and modify shared data concurrently, leading to unpredictable results.

**Example**:
```python
import multiprocessing

# WITHOUT LOCK - Race condition
def unsafe_increment(shared_val, n):
    for _ in range(n):
        shared_val.value += 1  # Not atomic!

# WITH LOCK - Safe
def safe_increment(shared_val, n, lock):
    for _ in range(n):
        with lock:
            shared_val.value += 1

if __name__ == "__main__":
    counter = multiprocessing.Value('i', 0)
    lock = multiprocessing.Lock()
    
    processes = []
    for _ in range(4):
        p = multiprocessing.Process(target=safe_increment, args=(counter, 1000, lock))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print(f"Counter: {counter.value}")  # 4000
```

**Related Terms**: Lock, synchronization, shared state

---

### start

**Definition**: A method that begins the process's execution by creating a new process and calling the `run()` method.

**Example**:
```python
import multiprocessing

def worker():
    print("Working in process")

if __name__ == "__main__":
    p = multiprocessing.Process(target=worker)
    p.start()  # Begins execution
    p.join()   # Wait for completion
```

**Related Terms**: join, lifecycle, run

---

### Value

**Definition**: A shared memory object that can hold a single value, accessible by multiple processes.

**Example**:
```python
import multiprocessing

def increment(shared_val, n):
    for _ in range(n):
        with shared_val.get_lock():
            shared_val.value += 1

if __name__ == "__main__":
    counter = multiprocessing.Value('i', 0)  # 'i' = int
    
    processes = []
    for _ in range(4):
        p = multiprocessing.Process(target=increment, args=(counter, 1000))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print(f"Counter: {counter.value}")  # 4000
```

**Related Terms**: Array, shared memory, Manager

**Type Codes**:
- `'i'`: signed int
- `'d'`: double
- `'f'`: float
- `'c'`: char

---

## Concept Relationships

```
Multiprocessing
├── Process Management
│   ├── Process (individual)
│   ├── Pool (managed group)
│   └── daemon (background)
│
├── Communication
│   ├── Queue (FIFO, multi-process)
│   ├── Pipe (bidirectional, two-process)
│   └── Manager (shared objects)
│
├── Shared State
│   ├── Value (single value)
│   ├── Array (numerical array)
│   └── Manager (complex objects)
│
├── Synchronization
│   ├── Lock (mutual exclusion)
│   ├── RLock (reentrant)
│   └── Semaphore (counting)
│
└── Use Cases
    ├── CPU-bound tasks
    ├── Parallel computation
    └── Data processing
```

---

## When to Use Multiprocessing

| Use Case | Recommendation |
|----------|----------------|
| CPU-bound tasks | ✅ Use multiprocessing |
| I/O-bound tasks | ⚠️ Consider threading |
| Memory-intensive | ⚠️ Consider memory limits |
| Simple parallelism | ✅ Use Pool |
| Complex shared state | ✅ Use Manager |

---

## Multiprocessing vs Threading

| Aspect | Multiprocessing | Threading |
|--------|-----------------|-----------|
| GIL | Bypassed | Limited by GIL |
| Memory | Separate spaces | Shared space |
| Overhead | Higher | Lower |
| Best for | CPU-bound | I/O-bound |
| Communication | Queue/Pipe | Shared variables |

---

## Common Patterns

### 1. Pool Map Pattern
```python
import multiprocessing

def process(item):
    return item * 2

if __name__ == "__main__":
    with multiprocessing.Pool(4) as pool:
        results = pool.map(process, items)
```

### 2. Producer-Consumer Pattern
```python
import multiprocessing

def producer(q):
    for item in items:
        q.put(item)
    q.put(None)

def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break
        process(item)
```

### 3. Shared Counter Pattern
```python
import multiprocessing

def safe_increment(counter, lock, n):
    for _ in range(n):
        with lock:
            counter.value += 1
```

### 4. MapReduce Pattern
```python
import multiprocessing

def map_function(item):
    return (item, 1)

def reduce_function(results):
    from collections import Counter
    return Counter(dict(results))

if __name__ == "__main__":
    with multiprocessing.Pool(4) as pool:
        mapped = pool.map(map_function, items)
    reduced = reduce_function(mapped)
```
