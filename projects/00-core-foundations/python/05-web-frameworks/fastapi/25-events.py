"""
25 - Lifespan Events
=======================
Application startup and shutdown events.
Use for: initializing connections, warming caches, cleanup on exit.

Note: @app.on_event is deprecated. Use the lifespan context manager pattern.

Run: uvicorn 25-events:app --reload
"""

import time
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel


# ----- Lifespan context manager (modern pattern) -----
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager.
    Code BEFORE yield runs on startup.
    Code AFTER yield runs on shutdown.
    """
    # === STARTUP ===
    print("🚀 Application starting up...")
    start_time = time.perf_counter()

    # Initialize resources
    app.state.start_time = start_time
    app.state.request_count = 0
    app.state.version = "1.0.0"

    # Simulate initialization work
    print("   📡 Connecting to database...")
    time.sleep(0.5)  # Simulate DB connection
    print("   ✅ Database connected")

    print("   🔧 Loading configuration...")
    app.state.config = {
        "debug": True,
        "max_connections": 100,
        "cache_ttl": 300,
    }
    print("   ✅ Configuration loaded")

    print(f"   ✅ Startup complete ({(time.perf_counter() - start_time) * 1000:.0f}ms)")

    yield  # App is running

    # === SHUTDOWN ===
    print("\n🛑 Application shutting down...")
    shutdown_start = time.perf_counter()

    # Cleanup resources
    print("   🗑️  Clearing caches...")
    print("   📡 Closing database connections...")
    print("   📝 Flushing logs...")

    uptime = time.perf_counter() - app.state.start_time
    print(f"   📊 Stats: {app.state.request_count} requests served")
    print(f"   ⏱️  Uptime: {uptime:.1f}s")
    print(f"   ✅ Shutdown complete ({(time.perf_counter() - shutdown_start) * 1000:.0f}ms)")


# ----- App with lifespan -----
app = FastAPI(
    title="Lifespan Events Demo",
    version="1.0.0",
    lifespan=lifespan,
)


class StatusResponse(BaseModel):
    status: str
    version: str
    uptime: float
    request_count: int


@app.middleware("http")
async def count_requests(request, call_next):
    """Track request count using app state."""
    app.state.request_count += 1
    response = await call_next(request)
    return response


@app.get("/", response_model=StatusResponse)
def root():
    """Root endpoint showing app status."""
    uptime = time.perf_counter() - app.state.start_time
    return StatusResponse(
        status="running",
        version=app.state.version,
        uptime=round(uptime, 2),
        request_count=app.state.request_count,
    )


@app.get("/config")
def get_config():
    """Access initialized configuration."""
    return {"config": app.state.config}


@app.get("/health")
def health_check():
    """Health check using startup-initialized state."""
    uptime = time.perf_counter() - app.state.start_time
    return {
        "healthy": True,
        "uptime_seconds": round(uptime, 2),
        "requests_served": app.state.request_count,
        "timestamp": datetime.now().isoformat(),
    }


# ----- Simulated resource management -----
class DatabasePool:
    """Simulated connection pool."""
    def __init__(self):
        self.connections = []

    def connect(self):
        self.connections = [f"conn_{i}" for i in range(5)]
        print(f"   📡 Pool created: {len(self.connections)} connections")

    def close(self):
        count = len(self.connections)
        self.connections.clear()
        print(f"   📡 Pool closed: {count} connections released")

    def get_status(self):
        return {"active_connections": len(self.connections)}


db_pool = DatabasePool()


@asynccontextmanager
async def db_lifespan(app: FastAPI):
    """Separate lifespan for database pool."""
    db_pool.connect()
    yield
    db_pool.close()


# For combining multiple lifespans, you'd use:
# from contextlib import asynccontextmanager, ExitStack
# async def combined_lifespan(app):
#     async with ExitStack() as stack:
#         await stack.enter_async_context(db_lifespan(app))
#         await stack.enter_async_context(cache_lifespan(app))
#         yield


@app.get("/db/status")
def db_status():
    """Check database pool status."""
    return db_pool.get_status()


"""
Testing with curl:
    curl http://127.0.0.1:8000/
    # Check terminal for startup logs

    curl http://127.0.0.1:8000/config
    curl http://127.0.0.1:8000/health
    curl http://127.0.0.1:8000/db/status

    # Shutdown: press Ctrl+C in terminal to see shutdown logs

    Example output on startup:
    🚀 Application starting up...
       📡 Connecting to database...
       ✅ Database connected
       🔧 Loading configuration...
       ✅ Configuration loaded
       ✅ Startup complete (502ms)

    Example output on shutdown:
    🛑 Application shutting down...
       🗑️  Clearing caches...
       📡 Closing database connections...
       📝 Flushing logs...
       📊 Stats: 5 requests served
       ⏱️  Uptime: 30.2s
       ✅ Shutdown complete (12ms)
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
