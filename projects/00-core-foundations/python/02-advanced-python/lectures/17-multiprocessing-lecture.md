# Lecture 17: Multiprocessing

## Topic Overview

Multiprocessing allows true parallelism by using multiple CPU cores, bypassing Python's Global Interpreter Lock (GIL). The `multiprocessing` module provides tools for creating and managing processes, sharing state, and coordinating inter-process communication.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Create and manage processes** using the multiprocessing module
2. **Understand when to use multiprocessing** vs threading
3. **Use Pool** for parallel execution of functions
4. **Share state** between processes using Value, Array, and Manager
5. **Implement inter-process communication** with Queue and Pipe
6. **Handle process synchronization** with Lock and Semaphore
7. **Use daemon processes** for background tasks

---

## Key Concepts

### 1. Basic Process

Each process has its own memory space and Python interpreter.

#### Creating Processes

```python
import multiprocessing
import time
import os

def worker(name):
    print(f"[{name}] PID: {os.getpid()}")
    time.sleep(0.1)
    print(f"[{name}] Done")

if __name__ == "__main__":
    processes = []
    for i in range(3):
        p = multiprocessing.Process(target=worker, args=(f"Process-{i}",))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print(f"Main process PID: {os.getpid()}")
```

#### Process with Arguments

```python
import multiprocessing

def compute_square(n):
    return n ** 2

if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    processes = []
    results = []
    
    for n in numbers:
        p = multiprocessing.Process(target=lambda: results.append(compute_square(n)))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print(f"Results: {results}")
```

---

### 2. Process Pool

Pool provides a convenient interface for parallel execution.

#### Basic Pool Usage

```python
import multiprocessing

def square(n):
    return n ** 2

if __name__ == "__main__":
    with multiprocessing.Pool(processes=4) as pool:
        numbers = [1, 2, 3, 4, 5, 6, 7, 8]
        
        # map - returns results in order
        results = pool.map(square, numbers)
        print(f"Squares: {results}")
        
        # map_async - asynchronous version
        async_result = pool.map_async(square, numbers)
        print(f"Async results: {async_result.get()}")
```

#### Pool with Multiple Arguments

```python
import multiprocessing

def power(base, exponent):
    return base ** exponent

if __name__ == "__main__":
    args = [(2, 3), (3, 4), (4, 2), (5, 3)]
    
    with multiprocessing.Pool(processes=2) as pool:
        # starmap - unpacks arguments
        results = pool.starmap(power, args)
        print(f"Power results: {results}")
```

#### Pool with Callbacks

```python
import multiprocessing

def process_item(item):
    return item * 2

def on_success(result):
    print(f"Success: {result}")

def on_error(error):
    print(f"Error: {error}")

if __name__ == "__main__":
    with multiprocessing.Pool(processes=2) as pool:
        # apply_async with callbacks
        result = pool.apply_async(
            process_item,
            (10,),
            callback=on_success,
            error_callback=on_error
        )
        result.get()  # Wait for completion
```

---

### 3. CPU-Bound Tasks

Multiprocessing excels at CPU-bound tasks.

```python
import multiprocessing
import time

def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

if __name__ == "__main__":
    numbers = [30, 32, 34, 35]
    
    # Sequential
    start = time.perf_counter()
    seq_results = [fibonacci(n) for n in numbers]
    seq_time = time.perf_counter() - start
    print(f"Sequential: {seq_time:.2f}s, results: {seq_results}")
    
    # Parallel
    start = time.perf_counter()
    with multiprocessing.Pool(processes=4) as pool:
        par_results = pool.map(fibonacci, numbers)
    par_time = time.perf_counter() - start
    print(f"Parallel: {par_time:.2f}s, results: {par_results}")
    print(f"Speedup: {seq_time/par_time:.2f}x")
```

---

### 4. Shared State

Processes can share state using specialized objects.

#### Shared Value

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

#### Shared Array

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

#### Manager

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

---

### 5. Queue Communication

Inter-process communication using Queue.

```python
import multiprocessing

def producer(q, count):
    for i in range(count):
        q.put(f"item-{i}")
    q.put(None)  # Sentinel

def consumer(q, results):
    while True:
        item = q.get()
        if item is None:
            break
        results.append(item.upper())

if __name__ == "__main__":
    q = multiprocessing.Queue()
    manager = multiprocessing.Manager()
    results = manager.list()
    
    prod = multiprocessing.Process(target=producer, args=(q, 5))
    cons = multiprocessing.Process(target=consumer, args=(q, results))
    
    prod.start()
    cons.start()
    
    prod.join()
    cons.join()
    
    print(f"Results: {list(results)}")
```

---

### 6. Process Lock

Ensure process-safe operations.

```python
import multiprocessing

lock = multiprocessing.Lock()

def safe_print(msg, lock_obj):
    with lock_obj:
        print(f"  {msg}")

if __name__ == "__main__":
    processes = []
    for i in range(5):
        p = multiprocessing.Process(
            target=safe_print,
            args=(f"Message from process {i}", lock)
        )
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
```

---

### 7. Daemon Processes

Daemon processes stop when the main process exits.

```python
import multiprocessing
import time

def background_task():
    while True:
        time.sleep(0.1)
        print("Background running...")

if __name__ == "__main__":
    daemon = multiprocessing.Process(target=background_task, daemon=True)
    daemon.start()
    time.sleep(0.3)
    print("Main process exiting (daemon will stop)")
```

---

### 8. Process with Return Value

Get return values from processes using Pool.

```python
import multiprocessing

def process_data(data):
    return {"input": data, "output": data * 2, "pid": multiprocessing.current_process().pid}

if __name__ == "__main__":
    data = [1, 2, 3, 4, 5]
    
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(process_data, data)
    
    for r in results:
        print(f"PID {r['pid']}: {r['input']} -> {r['output']}")
```

---

## Common Mistakes to Avoid

### 1. Forgetting `if __name__ == "__main__"`

```python
import multiprocessing

def worker():
    print("Working")

# WRONG - will cause issues on Windows
p = multiprocessing.Process(target=worker)
p.start()

# CORRECT
if __name__ == "__main__":
    p = multiprocessing.Process(target=worker)
    p.start()
    p.join()
```

### 2. Pickling Errors

```python
import multiprocessing

# WRONG - lambda functions can't be pickled
def bad_example():
    with multiprocessing.Pool() as pool:
        pool.map(lambda x: x * 2, [1, 2, 3])  # PicklingError

# CORRECT - use regular functions
def square(x):
    return x * 2

if __name__ == "__main__":
    with multiprocessing.Pool() as pool:
        pool.map(square, [1, 2, 3])
```

### 3. Not Joining Processes

```python
import multiprocessing

def worker():
    print("Working")

# WRONG - might exit before process completes
p = multiprocessing.Process(target=worker)
p.start()
# Program might exit here!

# CORRECT
p = multiprocessing.Process(target=worker)
p.start()
p.join()  # Wait for completion
```

---

## Best Practices

### 1. Use Pool for Simple Parallelism

```python
import multiprocessing

def process(item):
    return item * 2

if __name__ == "__main__":
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(process, items)
```

### 2. Use Manager for Complex Shared State

```python
import multiprocessing

if __name__ == "__main__":
    manager = multiprocessing.Manager()
    shared_dict = manager.dict()
    shared_list = manager.list()
```

### 3. Use Queue for Communication

```python
import multiprocessing

def producer(q):
    q.put("data")

def consumer(q):
    data = q.get()
    process(data)
```

---

## Practice Exercises

### Exercise 1: Parallel Download
```python
"""
Create a parallel downloader that:
- Downloads multiple URLs concurrently
- Returns results in order
- Handles errors gracefully
"""
# Your code here
```

### Exercise 2: MapReduce
```python
"""
Implement a simple MapReduce:
- Map: process each item
- Reduce: combine results
"""
# Your code here
```

### Exercise 3: Parallel Calculator
```python
"""
Create a parallel calculator that:
- Takes a list of expressions
- Evaluates them in parallel
- Returns results
"""
# Your code here
```

---

## Summary

### Multiprocessing Components

| Component | Purpose | Use Case |
|-----------|---------|----------|
| `Process` | Individual process | Complex tasks |
| `Pool` | Process pool | Simple parallelism |
| `Queue` | Communication | Data exchange |
| `Value/Array` | Shared memory | Small shared data |
| `Manager` | Shared objects | Complex shared state |
| `Lock` | Synchronization | Process safety |

### When to Use Multiprocessing

| Use Case | Recommendation |
|----------|----------------|
| CPU-bound tasks | ✅ Use multiprocessing |
| I/O-bound tasks | ⚠️ Consider threading |
| Memory-intensive | ⚠️ Consider memory limits |
| Simple parallelism | ✅ Use Pool |

### Key Takeaways

1. **Multiprocessing bypasses GIL** for true parallelism
2. **Use Pool** for simple map/reduce operations
3. **Use Queue** for inter-process communication
4. **Use Manager** for complex shared state
5. **Always join processes** before exiting
6. **Use `if __name__ == "__main__"`** on Windows

---

## Further Reading

- [Python multiprocessing documentation](https://docs.python.org/3/library/multiprocessing.html)
- [multiprocessing API reference](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing)
- [When to use multiprocessing vs threading](https://docs.python.org/3/library/multiprocessing.html#when-to-use-processes-vs-threads)
