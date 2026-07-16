# Lecture 21: Asynchronous Programming in FastAPI

## Overview

FastAPI is built on top of ASGI (Asynchronous Server Gateway Interface), making it naturally suited for asynchronous programming. This lecture covers Python's async/await syntax, async patterns in FastAPI, and how to build high-performance applications that can handle thousands of concurrent connections.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand the fundamentals of asynchronous programming
2. Use async/await syntax correctly in FastAPI
3. Implement async database operations
4. Handle concurrent tasks with asyncio
5. Use async HTTP clients for external API calls
6. Implement WebSocket connections
7. Understand when to use sync vs async
8. Optimize performance with async patterns

---

## Key Concepts

### 1. Synchronous vs Asynchronous

#### Synchronous (Traditional)
```python
# Synchronous code - blocks execution
import time

def fetch_data():
    print("Start fetching")
    time.sleep(2)  # Blocks for 2 seconds
    print("Data fetched")
    return {"data": "value"}

def process_data():
    print("Start processing")
    time.sleep(1)  # Blocks for 1 second
    print("Processing done")

# Total time: 3 seconds (2 + 1)
fetch_data()
process_data()
```

#### Asynchronous
```python
# Asynchronous code - non-blocking
import asyncio

async def fetch_data():
    print("Start fetching")
    await asyncio.sleep(2)  # Yields control for 2 seconds
    print("Data fetched")
    return {"data": "value"}

async def process_data():
    print("Start processing")
    await asyncio.sleep(1)  # Yields control for 1 second
    print("Processing done")

# Total time: 2 seconds (max of 2, 1)
async def main():
    await asyncio.gather(
        fetch_data(),
        process_data()
    )

asyncio.run(main())
```

### 2. Understanding Event Loop

The event loop is the core of asyncio that handles async operations:

```python
import asyncio

# The event loop manages:
# 1. Running async functions
# 2. Handling I/O operations
# 3. Scheduling callbacks
# 4. Managing coroutines

async def main():
    print("Inside event loop")
    await asyncio.sleep(1)
    print("Event loop continues")

# asyncio.run() creates and runs the event loop
asyncio.run(main())

# Manual event loop management
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```

### 3. Coroutines and Tasks

```python
import asyncio

# Coroutine - an async function
async def my_coroutine():
    await asyncio.sleep(1)
    return "result"

# Task - a scheduled coroutine
async def main():
    # Create task (starts immediately)
    task1 = asyncio.create_task(my_coroutine())
    task2 = asyncio.create_task(my_coroutine())
    
    # Wait for both tasks
    result1 = await task1
    result2 = await task2
    
    print(f"Results: {result1}, {result2}")

# Gather - run multiple coroutines concurrently
async def main():
    results = await asyncio.gather(
        my_coroutine(),
        my_coroutine(),
        my_coroutine()
    )
    print(f"All results: {results}")
```

---

## Code Examples

### Example 1: Async FastAPI Endpoints

```python
from fastapi import FastAPI
import asyncio
import httpx

app = FastAPI()

# Async endpoint
@app.get("/async-endpoint")
async def async_endpoint():
    # This doesn't block the event loop
    await asyncio.sleep(1)
    return {"message": "Async response"}

# Sync endpoint (runs in thread pool)
@app.get("/sync-endpoint")
def sync_endpoint():
    # This blocks, but FastAPI runs it in a thread
    time.sleep(1)
    return {"message": "Sync response"}

# Async with external API
@app.get("/fetch-data")
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()

# Multiple concurrent requests
@app.get("/aggregate-data")
async def aggregate_data():
    async with httpx.AsyncClient() as client:
        # Run multiple requests concurrently
        responses = await asyncio.gather(
            client.get("https://api.example.com/users"),
            client.get("https://api.example.com/posts"),
            client.get("https://api.example.com/comments")
        )
        
        return {
            "users": responses[0].json(),
            "posts": responses[1].json(),
            "comments": responses[2].json()
        }
```

### Example 2: Async Database Operations

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from typing import List, Optional

# Async engine
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=20,
    max_overflow=10
)

# Async session factory
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Async dependency
async def get_async_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# Async CRUD operations
async def create_user(db: AsyncSession, user: UserCreate) -> User:
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()

async def get_users(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> List[User]:
    result = await db.execute(
        select(User).offset(skip).limit(limit)
    )
    return result.scalars().all()

# Async endpoint with database
@app.post("/users/", response_model=UserResponse)
async def create_user_endpoint(
    user: UserCreate,
    db: AsyncSession = Depends(get_async_db)
):
    return await create_user(db, user)

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user_endpoint(
    user_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    user = await get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Example 3: Async HTTP Client

```python
import httpx
from typing import List, Dict

# Basic async HTTP client
async def fetch_user_data(user_id: int) -> Dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.example.com/users/{user_id}",
            timeout=10.0
        )
        response.raise_for_status()
        return response.json()

# Multiple concurrent requests
async def fetch_multiple_users(user_ids: List[int]) -> List[Dict]:
    async with httpx.AsyncClient() as client:
        # Create tasks for all requests
        tasks = [
            client.get(f"https://api.example.com/users/{uid}")
            for uid in user_ids
        ]
        
        # Execute all requests concurrently
        responses = await asyncio.gather(*tasks)
        
        # Process responses
        return [
            response.json() 
            for response in responses 
            if response.status_code == 200
        ]

# With retry logic
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def fetch_with_retry(url: str) -> Dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

# Streaming response
async def stream_data():
    async with httpx.AsyncClient() as client:
        async with client.stream("GET", "https://api.example.com/stream") as response:
            async for chunk in response.aiter_text():
                yield chunk
```

### Example 4: Async Background Tasks

```python
from fastapi import BackgroundTasks
import asyncio

# Background task function
def send_email(email: str, subject: str, body: str):
    # This runs in thread pool (sync)
    import smtplib
    # ... send email logic

# Async background task
async def process_data_async(data: dict):
    # This runs in event loop
    await asyncio.sleep(10)  # Simulate long processing
    # ... process data

# Endpoint with background tasks
@app.post("/register/")
async def register_user(
    user: UserCreate,
    background_tasks: BackgroundTasks
):
    # Create user
    db_user = create_user(user)
    
    # Add background task (runs after response)
    background_tasks.add_task(
        send_email,
        email=user.email,
        subject="Welcome!",
        body="Thanks for registering!"
    )
    
    # Add async background task
    background_tasks.add_task(
        process_data_async,
        data={"user_id": db_user.id}
    )
    
    return {"message": "User created"}

# Custom background task manager
class BackgroundTaskManager:
    def __init__(self):
        self.tasks: List[asyncio.Task] = []
    
    async def add_task(self, coro):
        task = asyncio.create_task(coro)
        self.tasks.append(task)
        task.add_done_callback(self.tasks.remove)
        return task
    
    async def wait_all(self):
        if self.tasks:
            await asyncio.gather(*self.tasks)

task_manager = BackgroundTaskManager()

@app.post("/process/")
async def process_endpoint(data: dict):
    # Add task to manager
    await task_manager.add_task(process_data_async(data))
    return {"message": "Processing started"}
```

### Example 5: WebSocket with Async

```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            # Receive messages asynchronously
            data = await websocket.receive_text()
            
            # Process message
            response = f"Echo: {data}"
            
            # Send response
            await manager.send_personal_message(response, websocket)
            
            # Broadcast to all clients
            await manager.broadcast(f"Client #{client_id}: {data}")
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left")

# Async WebSocket with database
@app.websocket("/ws/messages")
async def websocket_messages(websocket: WebSocket):
    await websocket.accept()
    
    async with async_session() as db:
        try:
            while True:
                data = await websocket.receive_json()
                
                # Save to database
                message = Message(**data)
                db.add(message)
                await db.commit()
                
                # Send confirmation
                await websocket.send_json({
                    "status": "saved",
                    "message_id": message.id
                })
                
        except WebSocketDisconnect:
            pass
```

### Example 6: Async Generators and Streaming

```python
from fastapi.responses import StreamingResponse
import asyncio

# Async generator
async def generate_numbers():
    for i in range(10):
        await asyncio.sleep(0.5)  # Simulate async work
        yield f"Number: {i}\n"

# Streaming endpoint
@app.get("/stream")
async def stream_endpoint():
    return StreamingResponse(
        generate_numbers(),
        media_type="text/plain"
    )

# Streaming JSON
async def generate_json_stream():
    import json
    for i in range(100):
        await asyncio.sleep(0.1)
        data = {"id": i, "value": f"Item {i}"}
        yield json.dumps(data) + "\n"

@app.get("/stream-json")
async def stream_json():
    return StreamingResponse(
        generate_json_stream(),
        media_type="application/x-ndjson"
    )

# Async generator for database streaming
async def stream_users(db: AsyncSession):
    async with db.stream(select(User)) as result:
        async for row in result:
            yield UserResponse.from_rye(row)

@app.get("/users/stream")
async def stream_users_endpoint(db: AsyncSession = Depends(get_async_db)):
    return StreamingResponse(
        stream_users(db),
        media_type="application/json"
    )
```

---

## Common Mistakes to Avoid

### 1. Blocking the Event Loop

```python
# BAD: Blocking the event loop
@app.get("/blocking")
async def blocking_endpoint():
    time.sleep(5)  # Blocks the entire event loop!
    return {"message": "Done"}

# GOOD: Use async sleep or run in executor
@app.get("/non-blocking")
async def non_blocking_endpoint():
    await asyncio.sleep(5)  # Yields control
    return {"message": "Done"}

# GOOD: Run blocking code in executor
@app.get("/executor")
async def executor_endpoint():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, time.sleep, 5)
    return {"message": "Done"}
```

### 2. Creating Too Many Tasks

```python
# BAD: Creating thousands of tasks at once
async def bad_pattern():
    tasks = [fetch_data(i) for i in range(10000)]
    await asyncio.gather(*tasks)  # Memory issues!

# GOOD: Use semaphore to limit concurrency
async def good_pattern():
    semaphore = asyncio.Semaphore(100)  # Max 100 concurrent
    
    async def limited_fetch(i):
        async with semaphore:
            return await fetch_data(i)
    
    tasks = [limited_fetch(i) for i in range(10000)]
    await asyncio.gather(*tasks)
```

### 3. Not Handling Exceptions in Async

```python
# BAD: Exception might be lost
async def risky_operation():
    task = asyncio.create_task(might_fail())
    # If task fails, exception is lost!

# GOOD: Handle exceptions properly
async def safe_operation():
    task = asyncio.create_task(might_fail())
    try:
        result = await task
    except Exception as e:
        print(f"Task failed: {e}")
```

---

## Best Practices

1. **Use Async for I/O Operations**: Database queries, HTTP requests, file operations
2. **Use Sync for CPU-bound Work**: Heavy computations, data processing
3. **Limit Concurrency**: Use semaphores to prevent resource exhaustion
4. **Handle Exceptions**: Always handle exceptions in async tasks
5. **Use Connection Pools**: For database and HTTP connections
6. **Monitor Event Loop**: Detect blocking operations
7. **Use Async Generators**: For streaming data
8. **Test Async Code**: Use pytest-asyncio
9. **Profile Performance**: Identify bottlenecks
10. **Document Async Behavior**: Make it clear which functions are async

---

## When to Use Sync vs Async

| Use Case | Sync | Async | Reason |
|----------|------|-------|--------|
| Database queries | ❌ | ✅ | I/O bound |
| HTTP requests | ❌ | ✅ | I/O bound |
| File operations | ❌ | ✅ | I/O bound |
| CPU calculations | ✅ | ❌ | CPU bound |
| Data processing | ✅ | ❌ | CPU bound |
| Complex algorithms | ✅ | ❌ | CPU bound |
| WebSockets | ❌ | ✅ | I/O bound |
| Background tasks | ✅ | ✅ | Depends on task |

---

## Practice Exercises

### Exercise 1: Async API Client
Build an async API client that:
- Fetches data from multiple endpoints concurrently
- Implements retry logic
- Handles timeouts properly
- Streams large responses

### Exercise 2: WebSocket Chat
Create a WebSocket chat application:
- Multiple room support
- User authentication
- Message history
- Typing indicators

### Exercise 3: Async Task Queue
Implement a simple async task queue:
- Add tasks with priorities
- Execute tasks concurrently
- Track task status
- Handle failures

---

## Summary

- Async/await enables non-blocking operations
- FastAPI is built for async by default
- Use async for I/O-bound operations
- Use sync (in executor) for CPU-bound work
- Handle exceptions in async tasks
- Limit concurrency with semaphores
- Test async code with pytest-asyncio

**Next Lecture**: We'll explore CORS configuration and security in FastAPI.
