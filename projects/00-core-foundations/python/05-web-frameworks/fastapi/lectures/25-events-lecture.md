# Lecture 25: Application Events and Lifespan in FastAPI

## Overview

Application events and lifespan management are crucial for initializing resources, setting up connections, and cleaning up when your FastAPI application shuts down. This lecture covers startup/shutdown events, the new lifespan pattern, and best practices for managing application lifecycle.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand application lifecycle in FastAPI
2. Use startup and shutdown events
3. Implement the modern lifespan pattern
4. Manage database connections lifecycle
5. Initialize and cleanup resources properly
6. Handle graceful shutdowns
7. Use context managers for resource management
8. Debug lifecycle issues

---

## Key Concepts

### 1. Application Lifecycle

FastAPI applications have a lifecycle with distinct phases:

```
Application Start
    │
    ├─→ Startup Events
    │   ├─ Initialize database
    │   ├─ Load configuration
    │   ├─ Connect to services
    │   └─ Warm up caches
    │
    ├─→ Running (Handling Requests)
    │   ├─ Process requests
    │   ├─ Execute middleware
    │   └─ Return responses
    │
    └─→ Shutdown Events
        ├─ Close database connections
        ├─ Flush pending operations
        ├─ Release resources
        └─ Log shutdown
```

### 2. Two Approaches to Lifecycle

#### Legacy: @app.on_event (Deprecated)
```python
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("Starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")
```

#### Modern: lifespan (Recommended)
```python
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)
```

---

## Code Examples

### Example 1: Basic Lifespan Pattern

```python
# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ============ STARTUP ============
    print("🚀 Application starting up...")
    
    # Initialize resources
    app.state.start_time = asyncio.get_event_loop().time()
    print(f"✓ App initialized at {app.state.start_time}")
    
    yield  # Application runs here
    
    # ============ SHUTDOWN ============
    print("🛑 Application shutting down...")
    
    # Cleanup resources
    elapsed = asyncio.get_event_loop().time() - app.state.start_time
    print(f"✓ App ran for {elapsed:.2f} seconds")

app = FastAPI(
    title="My API",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### Example 2: Database Lifecycle Management

```python
# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from contextlib import asynccontextmanager
from typing import AsyncGenerator

class Base(DeclarativeBase):
    pass

# Database configuration
DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/db"

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    echo=True
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# Lifespan for database
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Verify database connection
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Database connected and tables created")
    
    yield
    
    # Shutdown: Close database connection
    await engine.dispose()
    print("✓ Database connection closed")

# main.py
from fastapi import FastAPI

app = FastAPI(
    title="Database API",
    lifespan=lifespan
)

@app.get("/users/")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()
```

### Example 3: Multiple Resource Management

```python
# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
import aiohttp
import redis.asyncio as redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ============ STARTUP ============
    
    # 1. Initialize Redis
    app.state.redis = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )
    print("✓ Redis connected")
    
    # 2. Initialize HTTP client
    app.state.http_client = aiohttp.ClientSession()
    print("✓ HTTP client initialized")
    
    # 3. Load configuration
    app.state.config = load_config()
    print("✓ Configuration loaded")
    
    # 4. Warm up cache
    await warm_up_cache(app.state.redis)
    print("✓ Cache warmed up")
    
    # Application runs
    yield
    
    # ============ SHUTDOWN ============
    
    # 1. Close HTTP client
    await app.state.http_client.close()
    print("✓ HTTP client closed")
    
    # 2. Close Redis
    await app.state.redis.close()
    print("✓ Redis connection closed")
    
    # 3. Save any pending data
    await save_pending_data()
    print("✓ Pending data saved")
    
    print("✓ All resources cleaned up")

app = FastAPI(
    title="Multi-Resource API",
    lifespan=lifespan
)

@app.get("/data/")
async def get_data(request: Request):
    # Access resources from app.state
    redis_client = request.app.state.redis
    http_client = request.app.state.http_client
    
    # Use Redis
    cached = await redis_client.get("data")
    if cached:
        return {"source": "cache", "data": cached}
    
    # Use HTTP client
    async with http_client.get("https://api.example.com/data") as resp:
        data = await resp.json()
        await redis_client.set("data", data, ex=300)
        return {"source": "api", "data": data}
```

### Example 4: Database with Session Lifecycle

```python
# database.py
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Database:
    def __init__(self, url: str):
        self.url = url
        self.engine = None
        self.session_factory = None
    
    async def connect(self):
        """Initialize database connection"""
        self.engine = create_async_engine(
            self.url,
            pool_size=20,
            max_overflow=10
        )
        self.session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        # Verify connection
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        print(f"✓ Database connected: {self.url}")
    
    async def disconnect(self):
        """Close database connection"""
        if self.engine:
            await self.engine.dispose()
            print("✓ Database disconnected")
    
    def get_session(self) -> AsyncSession:
        """Get a new session"""
        return self.session_factory()

# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

database = Database("postgresql+asyncpg://user:pass@localhost/db")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await database.connect()
    app.state.database = database
    
    yield
    
    # Shutdown
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/users/")
async def list_users():
    async with database.get_session() as session:
        result = await session.execute(select(User))
        return result.scalars().all()
```

### Example 5: Background Tasks with Lifecycle

```python
# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
from typing import Optional

class BackgroundTaskManager:
    def __init__(self):
        self.tasks: list[asyncio.Task] = []
        self.running = False
    
    async def start(self):
        """Start background tasks"""
        self.running = True
        print("✓ Background tasks started")
    
    async def stop(self):
        """Stop all background tasks"""
        self.running = False
        for task in self.tasks:
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)
        print("✓ Background tasks stopped")
    
    async def add_task(self, coro):
        """Add a background task"""
        if self.running:
            task = asyncio.create_task(coro)
            self.tasks.append(task)
            task.add_done_callback(self.tasks.remove)
            return task
        return None

task_manager = BackgroundTaskManager()

async def periodic_cleanup():
    """Periodic cleanup task"""
    while True:
        await asyncio.sleep(3600)  # Every hour
        print("Running cleanup...")
        # Cleanup logic here

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await task_manager.start()
    await task_manager.add_task(periodic_cleanup())
    
    yield
    
    # Shutdown
    await task_manager.stop()

app = FastAPI(
    title="Background Tasks API",
    lifespan=lifespan
)

@app.post("/tasks/")
async def create_task(data: dict):
    async def process_task(task_data):
        await asyncio.sleep(10)
        print(f"Task completed: {task_data}")
    
    await task_manager.add_task(process_task(data))
    return {"status": "task_started"}
```

### Example 6: Testing with Lifespan

```python
# test_main.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app, lifespan

@pytest.fixture
async def client():
    """Test client with lifespan"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

@pytest.mark.asyncio
async def test_startup(client):
    """Test that startup events ran"""
    response = await client.get("/health")
    assert response.status_code == 200

# Custom test lifespan
@pytest.fixture
async def test_lifespan():
    """Test-specific lifespan"""
    @asynccontextmanager
    async def test_lifespan(app: FastAPI):
        # Test startup
        app.state.test_mode = True
        yield
        # Test shutdown
    
    return test_lifespan

@pytest.mark.asyncio
async def test_with_mock_database(client, test_lifespan):
    """Test with mock database"""
    # Override dependencies for testing
    app.dependency_overrides[get_db] = mock_get_db
    
    response = await client.get("/users/")
    assert response.status_code == 200
```

### Example 7: Error Handling in Lifecycle

```python
# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    resources = []
    
    try:
        # Startup - with error handling
        try:
            db = await create_database()
            resources.append(("database", db))
            app.state.db = db
            logger.info("Database connected")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
        
        try:
            redis = await create_redis()
            resources.append(("redis", redis))
            app.state.redis = redis
            logger.info("Redis connected")
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {e}")
            # Redis is optional, continue without it
            app.state.redis = None
        
        yield
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise
    
    finally:
        # Shutdown - always cleanup
        for name, resource in reversed(resources):
            try:
                await resource.close()
                logger.info(f"{name} closed")
            except Exception as e:
                logger.error(f"Error closing {name}: {e}")

app = FastAPI(lifespan=lifespan)

@app.get("/data/")
async def get_data(request: Request):
    # Check if Redis is available
    if request.app.state.redis:
        # Use Redis
        pass
    else:
        # Fallback
        pass
```

---

## Common Mistakes to Avoid

### 1. Not Yielding in Lifespan

```python
# BAD: No yield means no application running
@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize()
    # Missing yield!
    await cleanup()

# GOOD: Always yield
@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize()
    yield  # Application runs here
    await cleanup()
```

### 2. Not Handling Cleanup Errors

```python
# BAD: Exception in cleanup might leave resources
@asynccontextmanager
async def lifespan(app: FastAPI):
    resource = await create_resource()
    yield
    await resource.close()  # If this fails, no cleanup

# GOOD: Use try/finally
@asynccontextmanager
async def lifespan(app: FastAPI):
    resource = await create_resource()
    try:
        yield
    finally:
        try:
            await resource.close()
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
```

### 3. Using Deprecated on_event

```python
# BAD: Deprecated pattern
@app.on_event("startup")
async def startup():
    await initialize()

@app.on_event("shutdown")
async def shutdown():
    await cleanup()

# GOOD: Use lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize()
    yield
    await cleanup()

app = FastAPI(lifespan=lifespan)
```

---

## Best Practices

1. **Use lifespan**: Modern pattern for lifecycle management
2. **Always yield**: Ensure application runs between startup/shutdown
3. **Handle errors gracefully**: Don't let cleanup failures crash the app
4. **Use try/finally**: Ensure cleanup always runs
5. **Log lifecycle events**: Help with debugging
6. **Test lifecycle**: Verify startup/shutdown behavior
7. **Order matters**: Cleanup in reverse order of initialization
8. **Make resources optional**: Don't fail if non-critical resources unavailable

---

## Practice Exercises

### Exercise 1: Complete Lifecycle
Implement a full lifecycle with:
- Database connection
- Redis cache
- HTTP client
- Background tasks

### Exercise 2: Error Recovery
Create a lifespan that:
- Handles initialization failures
- Continues with partial resources
- Logs all errors

### Exercise 3: Testing Lifecycle
Write tests for:
- Startup events
- Shutdown events
- Error scenarios
- Resource cleanup

---

## Summary

- Lifespan manages application lifecycle
- Use @asynccontextmanager pattern
- Always yield in lifespan function
- Handle errors in both startup and shutdown
- Clean up resources in reverse order
- Test lifecycle behavior
- Log all lifecycle events

**Congratulations!** You've completed the FastAPI fundamentals course. Continue building projects to solidify your knowledge!
