# Glossary: Application Events and Lifespan in FastAPI

## Quick Reference Table

| Term | Definition | Related Terms |
|------|------------|---------------|
| Lifespan | Modern pattern for app lifecycle management | Context Manager, Startup |
| Startup | Phase when application initializes | Lifespan, Initialize |
| Shutdown | Phase when application cleans up | Lifespan, Cleanup |
| Context Manager | Python pattern for resource management | asynccontextmanager |
| App State | Storage for application-wide data | Request State |
| Resource | External connection or object to manage | Database, Redis |
| Cleanup | Releasing resources on shutdown | Shutdown, Dispose |
| Initialization | Setting up resources on startup | Startup, Connect |
| Yield | Keyword marking application run phase | Lifespan, Context |
| Graceful Shutdown | Clean termination without data loss | Shutdown, Cleanup |
| Background Task | Long-running process managed by app | Task, Asyncio |
| Event | Occurrence in application lifecycle | Startup, Shutdown |
| Middleware | Processing layer for requests | Request, Response |
| Dependency Injection | Providing resources to endpoints | Depends, Provider |
| Connection Pool | Cached database connections | Database, Engine |

---

## Detailed Definitions

### Lifespan

**Definition**: The modern FastAPI pattern for managing application startup and shutdown using an async context manager.

**Code Example**:
```python
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ============ STARTUP ============
    print("Application starting...")
    
    # Initialize resources
    app.state.db = await create_database()
    app.state.cache = await create_cache()
    
    print("Application ready!")
    
    yield  # Application runs here
    
    # ============ SHUTDOWN ============
    print("Application shutting down...")
    
    # Cleanup resources
    await app.state.db.close()
    await app.state.cache.close()
    
    print("Cleanup complete!")

# Use lifespan
app = FastAPI(
    title="My API",
    lifespan=lifespan
)

# Access resources in endpoints
@app.get("/data/")
async def get_data(request: Request):
    db = request.app.state.db
    cache = request.app.state.cache
    return {"data": "value"}
```

**Related Terms**: Context Manager, Startup, Shutdown

---

### Startup

**Definition**: The phase when a FastAPI application initializes resources and prepares to handle requests.

**Code Example**:
```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ============ STARTUP PHASE ============
    
    # 1. Initialize database
    app.state.db_engine = create_async_engine(DATABASE_URL)
    print("✓ Database engine created")
    
    # 2. Create tables
    async with app.state.db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Database tables created")
    
    # 3. Initialize cache
    app.state.redis = redis.Redis(host="localhost", port=6379)
    print("✓ Redis connected")
    
    # 4. Load configuration
    app.state.config = load_config()
    print("✓ Configuration loaded")
    
    # 5. Warm up caches
    await warm_up_caches(app.state.redis)
    print("✓ Caches warmed up")
    
    print("🚀 Startup complete!")
    
    yield  # Application runs
    
    # ============ SHUTDOWN PHASE ============
    # Cleanup code here
```

**Related Terms**: Lifespan, Initialize, Connect

---

### Shutdown

**Definition**: The phase when a FastAPI application releases resources and terminates gracefully.

**Code Example**:
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.resources = await initialize_resources()
    yield
    # ============ SHUTDOWN PHASE ============
    
    # 1. Flush pending writes
    await app.state.db.flush()
    print("✓ Pending writes flushed")
    
    # 2. Close database connections
    await app.state.db_engine.dispose()
    print("✓ Database connections closed")
    
    # 3. Close cache connections
    await app.state.redis.close()
    print("✓ Redis connection closed")
    
    # 4. Cancel background tasks
    for task in app.state.background_tasks:
        task.cancel()
    await asyncio.gather(*app.state.background_tasks, return_exceptions=True)
    print("✓ Background tasks stopped")
    
    # 5. Save application state
    await save_application_state(app.state)
    print("✓ Application state saved")
    
    print("🛑 Shutdown complete!")
```

**Related Terms**: Lifespan, Cleanup, Dispose

---

### Context Manager

**Definition**: Python pattern using async with for automatic resource management.

**Code Example**:
```python
from contextlib import asynccontextmanager

# Basic context manager
@asynccontextmanager
async def database_connection():
    conn = await create_connection()
    try:
        yield conn  # Resource is available here
    finally:
        await conn.close()  # Always cleanup

# Usage
async with database_connection() as conn:
    result = await conn.execute(query)

# FastAPI lifespan is a context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup
    resource = await acquire_resource()
    app.state.resource = resource
    
    yield  # App runs
    
    # Teardown
    await resource.release()

# Multiple resources
@asynccontextmanager
async def lifespan(app: FastAPI):
    db = await create_db()
    cache = await create_cache()
    
    try:
        app.state.db = db
        app.state.cache = cache
        yield
    finally:
        await cache.close()
        await db.close()
```

**Related Terms**: async, with, yield, try/finally

---

### App State

**Definition**: A namespace for storing application-wide data accessible across requests.

**Code Example**:
```python
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Store data in app.state
    app.state.database = await create_database()
    app.state.cache = Redis()
    app.state.settings = load_settings()
    app.state.start_time = datetime.now()
    
    yield
    
    # Cleanup
    await app.state.database.close()

app = FastAPI(lifespan=lifespan)

# Access in endpoints
@app.get("/status/")
async def status(request: Request):
    return {
        "database": request.app.state.database.is_connected(),
        "uptime": (datetime.now() - request.app.state.start_time).seconds
    }

# Access in middleware
@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    request.app.state.process_time = process_time
    return response
```

**Related Terms**: Request, Global, Storage

---

### Resource

**Definition**: An external connection or object that needs initialization and cleanup.

**Code Example**:
```python
# Resource types and their lifecycle
class DatabaseResource:
    def __init__(self, url: str):
        self.url = url
        self.engine = None
    
    async def connect(self):
        self.engine = create_async_engine(self.url)
        print(f"✓ Database connected")
    
    async def disconnect(self):
        if self.engine:
            await self.engine.dispose()
            print("✓ Database disconnected")

class CacheResource:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.client = None
    
    async def connect(self):
        self.client = redis.Redis(host=self.host, port=self.port)
        print("✓ Cache connected")
    
    async def disconnect(self):
        if self.client:
            await self.client.close()
            print("✓ Cache disconnected")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize resources
    db = DatabaseResource(DATABASE_URL)
    await db.connect()
    
    cache = CacheResource("localhost", 6379)
    await cache.connect()
    
    app.state.db = db
    app.state.cache = cache
    
    yield
    
    # Cleanup in reverse order
    await cache.disconnect()
    await db.disconnect()
```

**Related Terms**: Connection, Initialize, Cleanup

---

### Cleanup

**Definition**: The process of releasing resources and finalizing operations during shutdown.

**Code Example**:
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    resources = []
    
    # Startup - collect resources
    db = await create_database()
    resources.append(("database", db))
    
    cache = await create_cache()
    resources.append(("cache", cache))
    
    app.state.db = db
    app.state.cache = cache
    
    yield
    
    # Shutdown - cleanup in reverse order
    for name, resource in reversed(resources):
        try:
            await resource.close()
            print(f"✓ {name} cleaned up")
        except Exception as e:
            print(f"✗ Error cleaning up {name}: {e}")

# With try/finally
@asynccontextmanager
async def lifespan(app: FastAPI):
    db = await create_database()
    try:
        yield
    finally:
        try:
            await db.close()
        except Exception as e:
            logger.error(f"Database cleanup error: {e}")
```

**Related Terms**: Shutdown, Dispose, Close

---

### Yield

**Definition**: Keyword in lifespan that marks where the application runs between startup and shutdown.

**Code Example**:
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code BEFORE yield = startup
    print("Starting up...")
    app.state.db = await create_database()
    
    # Yield marks the boundary
    yield
    
    # Code AFTER yield = shutdown
    print("Shutting down...")
    await app.state.db.close()

# Multiple yields (not recommended, but possible)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Phase 1: Startup")
    yield  # App runs
    
    print("Phase 2: Intermediate")
    yield  # App runs again (unusual)
    
    print("Phase 3: Shutdown")

# Correct pattern - single yield
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup")
    yield  # Single yield point
    print("Shutdown")
```

**Related Terms**: Context Manager, async, Generator

---

### Graceful Shutdown

**Definition**: Terminating an application while completing pending operations and releasing resources properly.

**Code Example**:
```python
import signal
from contextlib import asynccontextmanager

shutdown_event = asyncio.Event()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Handle shutdown signals
    def handle_signal():
        shutdown_event.set()
    
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, handle_signal)
    
    # Startup
    app.state.db = await create_database()
    app.state.tasks = []
    
    yield
    
    # Graceful shutdown
    print("Starting graceful shutdown...")
    
    # 1. Stop accepting new requests
    shutdown_event.set()
    
    # 2. Complete pending tasks
    for task in app.state.tasks:
        if not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
    
    # 3. Flush database
    await app.state.db.flush()
    
    # 4. Close connections
    await app.state.db.close()
    
    print("Graceful shutdown complete!")
```

**Related Terms**: Shutdown, Signal, Cleanup

---

### Background Task

**Definition**: A long-running process managed by the application lifecycle.

**Code Example**:
```python
import asyncio
from contextlib import asynccontextmanager

class BackgroundTaskManager:
    def __init__(self):
        self.tasks: list[asyncio.Task] = []
        self._running = False
    
    async def start(self):
        self._running = True
    
    async def stop(self):
        self._running = False
        for task in self.tasks:
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)
    
    async def add(self, coro):
        if self._running:
            task = asyncio.create_task(coro)
            self.tasks.append(task)
            task.add_done_callback(self.tasks.remove)
            return task
        return None

task_manager = BackgroundTaskManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start background tasks
    await task_manager.start()
    
    # Add periodic tasks
    async def periodic_cleanup():
        while True:
            await asyncio.sleep(3600)
            await cleanup_old_data()
    
    await task_manager.add(periodic_cleanup())
    
    yield
    
    # Stop all background tasks
    await task_manager.stop()

@app.post("/process/")
async def process_data(data: dict):
    async def background_process(d):
        await asyncio.sleep(10)
        print(f"Processed: {d}")
    
    await task_manager.add(background_process(data))
    return {"status": "processing"}
```

**Related Terms**: Async, Task, Lifecycle

---

## Lifecycle Event Order

```
Application Start
    │
    ├─→ 1. Import modules
    ├─→ 2. Create FastAPI app
    ├─→ 3. Add middleware
    ├─→ 4. Add routes
    │
    └─→ Lifespan STARTUP
        ├─→ Initialize database
        ├─→ Connect to cache
        ├─→ Load configuration
        └─→ Warm up resources
            │
            ▼
    ┌───────────────────┐
    │  APPLICATION RUNS │
    │  (Handling        │
    │   Requests)       │
    └───────────────────┘
            │
            ▼
        Lifespan SHUTDOWN
        ├─→ Stop accepting requests
        ├─→ Complete pending tasks
        ├─→ Flush database
        ├─→ Close connections
        └─→ Release resources
            │
            ▼
    Application Stop
```

---

## Common Patterns

### Pattern: Resource Registry
```python
class ResourceRegistry:
    def __init__(self):
        self.resources = {}
    
    async def register(self, name: str, resource):
        self.resources[name] = resource
    
    async def cleanup_all(self):
        for name in reversed(list(self.resources.keys())):
            await self.resources[name].close()

registry = ResourceRegistry()

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = await create_db()
    await registry.register("db", db)
    
    cache = await create_cache()
    await registry.register("cache", cache)
    
    yield
    
    await registry.cleanup_all()
```

### Pattern: Conditional Resources
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Required resource
    db = await create_database()
    app.state.db = db
    
    # Optional resource
    try:
        cache = await create_cache()
        app.state.cache = cache
    except Exception as e:
        logger.warning(f"Cache unavailable: {e}")
        app.state.cache = None
    
    yield
    
    # Cleanup
    if app.state.cache:
        await app.state.cache.close()
    await db.close()
```

### Pattern: Health Check
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.health = {"status": "starting"}
    
    try:
        app.state.db = await create_database()
        app.state.health["database"] = "connected"
        
        yield
        
    except Exception as e:
        app.state.health["status"] = "error"
        app.state.health["error"] = str(e)
        raise
    
    finally:
        app.state.health["status"] = "shutdown"
        if hasattr(app.state, 'db'):
            await app.state.db.close()

@app.get("/health/")
async def health_check(request: Request):
    return request.app.state.health
```

---

## Summary

Understanding application lifecycle is essential for building robust FastAPI applications. Key takeaways:

1. **Lifespan**: Modern pattern for lifecycle management
2. **Yield**: Marks where application runs
3. **App State**: Store application-wide data
4. **Resources**: Manage connections and objects
5. **Cleanup**: Always release resources
6. **Graceful Shutdown**: Handle signals properly
7. **Background Tasks**: Manage long-running processes
8. **Error Handling**: Don't let failures crash the app

**Congratulations!** You've completed the FastAPI fundamentals course!
