# Glossary: FastAPI Background Tasks

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| BackgroundTasks | FastAPI's built-in task queue class | `BackgroundTasks()` |
| Task | A function executed after response | `send_email()` |
| Add Task | Method to queue background work | `background_tasks.add_task()` |
| Task Queue | FIFO queue for background tasks | Request processing queue |
| Async Task | Coroutine-based background task | `async def task()` |
| Sync Task | Synchronous background task | `def task()` |
| Task Chain | Sequential task execution | Multiple add_task calls |
| Task Dependency | External service needed by task | Database, email server |
| Retry | Re-executing failed tasks | Exponential backoff |
| Task ID | Unique identifier for task tracking | UUID string |
| Callback | Function called after task completion | Success/failure handlers |
| Dead Letter | Tasks that failed permanently | DLQ (Dead Letter Queue) |
| Worker | Process that executes tasks | Celery worker |
| Broker | Message queue for task distribution | Redis, RabbitMQ |
| Result Backend | Storage for task results | Redis, database |

---

## Terms - Alphabetical Order

### Add Task

**Definition:** Method on BackgroundTasks object that queues a function to run after the response is sent.

**Example:**
```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def send_email(email: str, subject: str):
    print(f"Sending {subject} to {email}")

@app.post("/register/")
async def register(background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, "user@test.com", "Welcome!")
    return {"message": "Registered"}
```

**Related Terms:** BackgroundTasks, Task, Queue

---

### Async Task

**Definition:** A background task defined as a coroutine using `async def`, allowing non-blocking I/O operations.

**Example:**
```python
import asyncio

async def fetch_data(url: str):
    """Async background task"""
    await asyncio.sleep(2)  # Simulate network call
    return {"status": "fetched"}

@app.post("/fetch/")
async def trigger_fetch(background_tasks: BackgroundTasks):
    background_tasks.add_task(fetch_data, "https://api.example.com")
    return {"message": "Fetch queued"}
```

**Related Terms:** Coroutine, Await, I/O Bound

---

### BackgroundTasks

**Definition:** FastAPI's dependency-injected class for managing background task execution after response is sent.

**Example:**
```python
from fastapi import BackgroundTasks

def process_data(data: dict):
    # Heavy processing here
    pass

@app.post("/process/")
async def process(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_data, {"key": "value"})
    return {"message": "Processing"}
```

**Related Terms:** Dependency Injection, Task Queue

---

### Broker

**Definition:** Message broker that receives and stores task messages for workers to process. Used with Celery/RQ, not FastAPI BackgroundTasks.

**Example:**
```python
# Celery configuration with Redis broker
from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def send_email(email: str):
    pass
```

**Related Terms:** Redis, RabbitMQ, Celery, Worker

---

### Callback

**Definition:** A function passed to background tasks that executes upon task completion or failure.

**Example:**
```python
def on_success(result):
    print(f"Task succeeded: {result}")

def on_failure(error):
    print(f"Task failed: {error}")

def long_running_task(callback_success, callback_error):
    try:
        result = do_work()
        callback_success(result)
    except Exception as e:
        callback_error(e)

@app.post("/task/")
async def run_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(
        long_running_task,
        on_success,
        on_failure
    )
    return {"message": "Task started"}
```

**Related Terms:** Completion Handler, Error Handler

---

### Chain

**Definition:** Executing multiple background tasks in sequence, where each task runs after the previous one completes.

**Example:**
```python
def step_one():
    print("Step 1: Validate")
    return True

def step_two():
    print("Step 2: Process")
    return True

def step_three():
    print("Step 3: Notify")

@app.post("/pipeline/")
async def run_pipeline(background_tasks: BackgroundTasks):
    # Tasks execute in order: step_one -> step_two -> step_three
    background_tasks.add_task(step_one)
    background_tasks.add_task(step_two)
    background_tasks.add_task(step_three)
    return {"message": "Pipeline started"}
```

**Related Terms:** Sequential Execution, Task Queue

---

### Celery

**Definition:** Distributed task queue framework for Python, providing reliability, monitoring, and scalability beyond FastAPI BackgroundTasks.

**Example:**
```python
from celery import Celery

app_celery = Celery("worker", broker="redis://localhost")

@app_celery.task(bind=True, max_retries=3)
def process_payment(self, payment_id: int):
    try:
        # Process payment
        pass
    except Exception as exc:
        self.retry(exc=exc, countdown=60)

# In FastAPI
@app.post("/pay/")
async def pay(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_payment.delay, 123)
    return {"message": "Payment processing"}
```

**Related Terms:** Worker, Broker, Retry, Monitoring

---

### Coroutine

**Definition:** An async function that can be paused and resumed, used for non-blocking background tasks.

**Example:**
```python
async def fetch_user_data(user_id: int):
    """This is a coroutine"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api/users/{user_id}")
        return response.json()

@app.post("/enrich/")
async def enrich_user(
    user_id: int,
    background_tasks: BackgroundTasks
):
    # Pass coroutine to background task
    background_tasks.add_task(fetch_user_data, user_id)
    return {"message": "Enrichment queued"}
```

**Related Terms:** Async/Await, Non-blocking, I/O

---

### Dead Letter Queue (DLQ)

**Definition:** Queue that holds tasks that failed repeatedly and cannot be processed. Used with message brokers like RabbitMQ.

**Example:**
```python
# Celery configuration with DLQ
celery_app.conf.update(
    task_routes={
        "tasks.email.*": {"queue": "email"},
    },
    task_default_queue="default",
    task_default_dlqueue="dead_letter",
)
```

**Related Terms:** Failed Tasks, Retry, Queue

---

### Dependency Injection

**Definition:** FastAPI feature that provides BackgroundTasks instance to your endpoint function automatically.

**Example:**
```python
from fastapi import BackgroundTasks

# BackgroundTasks is automatically injected
@app.post("/task/")
async def run_task(background_tasks: BackgroundTasks):
    # Use injected background_tasks
    background_tasks.add_task(my_function)
    return {"status": "ok"}

# Can also use in sub-dependencies
def get_task_runner(background_tasks: BackgroundTasks):
    return background_tasks

@app.post("/subtask/")
async def subtask(runner: BackgroundTasks = Depends(get_task_runner)):
    runner.add_task(my_function)
```

**Related Terms:** Inject, FastAPI, Request Scope

---

### Execution Order

**Definition:** The sequence in which background tasks run - FIFO (First In, First Out) by default.

**Example:**
```python
@app.post("/order/")
async def demo_order(background_tasks: BackgroundTasks):
    # These execute in this exact order:
    background_tasks.add_task(task_a)  # Runs first
    background_tasks.add_task(task_b)  # Runs second
    background_tasks.add_task(task_c)  # Runs third
    return {"message": "Tasks queued"}
```

**Related Terms:** FIFO, Sequential, Queue

---

### Exponential Backoff

**Definition:** Retry strategy where wait time increases exponentially between attempts (1s, 2s, 4s, 8s, etc.).

**Example:**
```python
import asyncio
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    delay = base_delay * (2 ** attempt)
                    await asyncio.sleep(delay)
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
async def unreliable_api_call():
    # Will retry with delays: 1s, 2s, 4s
    pass
```

**Related Terms:** Retry, Backoff, Delay

---

### FIFO (First In, First Out)

**Definition:** Queue ordering where the first task added is the first task executed.

**Example:**
```python
@app.post("/fifo/")
async def fifo_demo(background_tasks: BackgroundTasks):
    # Tasks processed in order added
    background_tasks.add_task(first)   # Executes 1st
    background_tasks.add_task(second)  # Executes 2nd
    background_tasks.add_task(third)   # Executes 3rd
    return {"message": "FIFO order"}
```

**Related Terms:** Queue, Execution Order

---

### I/O Bound

**Definition:** Tasks that spend most time waiting for external systems (network, disk, database) - ideal for async background tasks.

**Example:**
```python
async def fetch_external_data(url: str):
    """I/O bound - waits for network"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

async def read_file(path: str):
    """I/O bound - waits for disk"""
    async with aiofiles.open(path) as f:
        return await f.read()

@app.post("/io/")
async def io_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(fetch_external_data, "https://api.example.com")
    return {"message": "I/O task queued"}
```

**Related Terms:** Async, Network, Disk, CPU Bound

---

### Monitor

**Definition:** Tracking background task execution, including success rates, failure rates, and performance metrics.

**Example:**
```python
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def monitored_task(task_id: str):
    start_time = datetime.now()
    try:
        logger.info(f"Task {task_id} started")
        do_work()
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Task {task_id} completed in {duration}s")
    except Exception as e:
        logger.error(f"Task {task_id} failed: {e}")
        # Could also send to monitoring service
```

**Related Terms:** Logging, Metrics, Observability

---

### Non-blocking

**Definition:** Operation that doesn't halt execution while waiting for completion, allowing other tasks to proceed.

**Example:**
```python
import asyncio

async def non_blocking_task():
    """This is non-blocking"""
    await asyncio.sleep(10)  # Other tasks can run during this
    print("Done")

async def blocking_task():
    """This blocks the event loop"""
    time.sleep(10)  # Nothing else can run!
    print("Done")

# Use non-blocking in background tasks
@app.post("/async/")
async def async_endpoint(background_tasks: BackgroundTasks):
    background_tasks.add_task(non_blocking_task)  # ✅ Good
    # background_tasks.add_task(blocking_task)  # ❌ Bad
    return {"message": "Queued"}
```

**Related Terms:** Async, Await, Event Loop

---

### Queue

**Definition:** Data structure holding background tasks waiting to be executed, processed in FIFO order.

**Example:**
```python
@app.post("/queue/")
async def add_to_queue(background_tasks: BackgroundTasks):
    # Tasks are added to internal queue
    background_tasks.add_task(task1)
    background_tasks.add_task(task2)
    background_tasks.add_task(task3)
    # Queue: [task1, task2, task3]
    # Executes: task1 → task2 → task3
    return {"message": "Tasks queued"}
```

**Related Terms:** FIFO, Execution Order, BackgroundTasks

---

### Retry

**Definition:** Automatically re-executing a failed task, typically with increasing delays between attempts.

**Example:**
```python
import asyncio

async def send_webhook(url: str, data: dict, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data)
                response.raise_for_status()
                return {"success": True}
        except Exception as e:
            if attempt < max_retries - 1:
                delay = 2 ** attempt  # Exponential backoff
                await asyncio.sleep(delay)
            else:
                raise

@app.post("/webhook/")
async def trigger_webhook(background_tasks: BackgroundTasks):
    background_tasks.add_task(
        send_webhook,
        "https://hooks.example.com",
        {"event": "user.created"}
    )
    return {"message": "Webhook queued"}
```

**Related Terms:** Exponential Backoff, Failure, Error Handling

---

### Result Backend

**Definition:** Storage system (Redis, database, etc.) where Celery stores task results for later retrieval.

**Example:**
```python
from celery import Celery

# Redis as result backend
celery_app = Celery(
    "tasks",
    broker="redis://localhost",
    backend="redis://localhost"  # Result backend
)

@celery_app.task
def compute(x, y):
    return x + y

# In FastAPI
@app.get("/compute/")
async def compute_endpoint(background_tasks: BackgroundTasks):
    result = compute.delay(4, 4)
    # Get result later
    return {"task_id": result.id}
```

**Related Terms:** Celery, Redis, Task ID

---

### Task Chain

**Definition:** Linking multiple tasks where each receives the result of the previous one.

**Example:**
```python
def validate(data: dict) -> dict:
    return {"valid": True, "data": data}

def process(validated: dict) -> dict:
    return {"processed": True, "id": 123}

def notify(result: dict):
    print(f"Notifying about result: {result}")

@app.post("/chain/")
async def run_chain(background_tasks: BackgroundTasks):
    background_tasks.add_task(validate, {"raw": "data"})
    background_tasks.add_task(process, {"valid": True})
    background_tasks.add_task(notify, {"processed": True})
    return {"message": "Chain started"}
```

**Related Terms:** Sequential, Pipeline, Tasks

---

### Task ID

**Definition:** Unique identifier for tracking background task execution and status.

**Example:**
```python
import uuid

# In-memory task storage
task_storage = {}

@app.post("/task/")
async def create_task(background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    task_storage[task_id] = {"status": "queued"}
    
    def run_task(tid: str):
        task_storage[tid] = {"status": "running"}
        # Do work...
        task_storage[tid] = {"status": "completed"}
    
    background_tasks.add_task(run_task, task_id)
    return {"task_id": task_id}

@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    return task_storage.get(task_id, {"status": "unknown"})
```

**Related Terms:** UUID, Status, Tracking

---

### Worker

**Definition:** Process that pulls tasks from a queue and executes them. Used with Celery/RQ, not FastAPI BackgroundTasks.

**Example:**
```bash
# Start Celery worker
celery -A tasks worker --loglevel=info

# With multiple concurrency
celery -A tasks worker --concurrency=4

# Specific queue
celery -A tasks worker -Q email,processing
```

```python
# In FastAPI
@app.post("/celery-task/")
async def celery_task(background_tasks: BackgroundTasks):
    # .delay() sends task to Celery worker
    result = my_celery_task.delay(arg1, arg2)
    return {"task_id": result.id}
```

**Related Terms:** Celery, Broker, Concurrency

---

## Code Examples Collection

### Complete Background Task Setup

```python
from fastapi import FastAPI, BackgroundTasks
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

def process_order(order_id: int):
    """Background task with logging and error handling"""
    start_time = datetime.now()
    try:
        logger.info(f"Processing order {order_id}")
        # Simulate processing
        import time
        time.sleep(2)
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Order {order_id} processed in {duration}s")
    except Exception as e:
        logger.error(f"Order {order_id} failed: {e}")

@app.post("/orders/")
async def create_order(background_tasks: BackgroundTasks):
    order_id = 12345
    
    background_tasks.add_task(process_order, order_id)
    
    return {
        "message": "Order received",
        "order_id": order_id,
        "status": "processing"
    }
```

### Error Handling Pattern

```python
from fastapi import BackgroundTasks
import logging

logger = logging.getLogger(__name__)

def safe_background_task(func):
    """Decorator for safe background task execution"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Background task {func.__name__} failed: {e}")
            # Could store error, send alert, etc.
    return wrapper

@safe_background_task
async def risky_operation(data: dict):
    # Task that might fail
    pass

@app.post("/safe/")
async def safe_endpoint(background_tasks: BackgroundTasks):
    background_tasks.add_task(risky_operation, {"key": "value"})
    return {"message": "Safe task queued"}
```

### Task with External Service

```python
import httpx
from fastapi import BackgroundTasks

async def send_webhook(url: str, payload: dict):
    """Send webhook in background"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            logger.info(f"Webhook sent to {url}")
        except httpx.HTTPError as e:
            logger.error(f"Webhook failed: {e}")

@app.post("/event/")
async def trigger_event(background_tasks: BackgroundTasks):
    event = {"type": "user.created", "user_id": 123}
    
    background_tasks.add_task(
        send_webhook,
        "https://hooks.slack.com/xxx",
        event
    )
    
    return {"message": "Event triggered"}
```

---

## Quick Reference Card

### FastAPI BackgroundTasks API

```python
from fastapi import BackgroundTasks

# Inject into endpoint
async def endpoint(background_tasks: BackgroundTasks):
    # Add synchronous task
    background_tasks.add_task(sync_func, arg1, arg2)
    
    # Add async task
    background_tasks.add_task(async_func, arg1, arg2)
    
    # Add method
    background_tasks.add_task(service.method, arg1)
```

### Celery Integration

```python
from celery import Celery

celery = Celery("tasks", broker="redis://localhost")

@celery.task
def my_task(arg):
    pass

# In FastAPI
async def endpoint(background_tasks: BackgroundTasks):
    background_tasks.add_task(my_task.delay, arg)
```

### Common Patterns

```python
# 1. Simple fire-and-forget
background_tasks.add_task(send_email, email)

# 2. With error handling
def safe_task():
    try:
        do_work()
    except Exception as e:
        logger.error(e)

background_tasks.add_task(safe_task)

# 3. Async with httpx
async def fetch_data(url: str):
    async with httpx.AsyncClient() as client:
        return await client.get(url)

background_tasks.add_task(fetch_data, "https://api.example.com")
```
