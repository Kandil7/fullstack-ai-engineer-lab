"""
Exercise 25: Application Events and Lifespan

Master startup/shutdown events, lifespan context managers, and background tasks.
Topics: startup events, shutdown events, lifespan, background tasks, health checks.

Prerequisites:
- FastAPI basics
- Async/await (exercise 21)
- Context managers

Estimated time: 45-60 minutes
"""

from fastapi import FastAPI, BackgroundTasks, Request
from pydantic import BaseModel
from typing import Optional
from contextlib import asynccontextmanager
from datetime import datetime
import asyncio
import time

# ============================================================
# Exercise 25.1: Startup and Shutdown Events
# ============================================================
"""
Problem:
    Implement proper application lifecycle management.

Requirements:
    1. Initialize resources on startup (DB connection, cache, etc.)
    2. Clean up resources on shutdown (close connections, flush buffers)
    3. Log lifecycle events with timestamps
    4. Track application state (ready, shutting down)
    5. Handle initialization failures gracefully

Startup/shutdown pattern (legacy):
    app = FastAPI()

    @app.on_event("startup")
    async def startup_event():
        print("Starting up...")
        app.state.db = await create_db_connection()
        app.state.cache = {}
        app.state.start_time = time.time()
        app.state.ready = True

    @app.on_event("shutdown")
    async def shutdown_event():
        print("Shutting down...")
        app.state.ready = False
        await app.state.db.close()
        print(f"Uptime: {time.time() - app.state.start_time:.1f}s")

Modern lifespan pattern (Python 3.10+):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup
        app.state.db = await create_db_connection()
        app.state.cache = {}
        app.state.start_time = time.time()
        app.state.ready = True
        print("Application started")
        yield
        # Shutdown
        app.state.ready = False
        await app.state.db.close()
        print(f"Uptime: {time.time() - app.state.start_time:.1f}s")

    app = FastAPI(lifespan=lifespan)

Endpoints:
    GET /health      - Health check with startup status
    GET /status      - Detailed application status
    GET /uptime      - Application uptime

Hints:
    - Use app.state to store application-level data
    - asynccontextmanager for the lifespan function
    - yield separates startup from shutdown code
    - app.state.ready flag prevents requests during shutdown
    - Handle exceptions in startup to prevent partial initialization

Test cases:
    # Health check
    GET /health
    -> 200 {"status": "healthy", "ready": true}

    # Application status
    GET /status
    -> 200 {
        "ready": true,
        "uptime_seconds": 125.3,
        "initialized": true
    }

    # During shutdown (simulate)
    GET /health
    -> 503 {"status": "shutting_down", "ready": false}
"""

# TODO: Write lifecycle management code below


# ============================================================
# Exercise 25.2: Background Tasks
# ============================================================
"""
Problem:
    Implement FastAPI BackgroundTasks for deferred processing.

Endpoints with background tasks:
    POST /orders          - Create order + send confirmation email in background
    POST /reports         - Generate report + send notification when done
    POST /analytics       - Track event + process analytics asynchronously

Background task patterns:

    1. Email sending (fire-and-forget):
        @app.post("/orders")
        async def create_order(order: OrderCreate, background_tasks: BackgroundTasks):
            # Create order (fast)
            db_order = create_order_in_db(order)
            # Send email in background (slow, but doesn't block response)
            background_tasks.add_task(
                send_confirmation_email,
                email=order.email,
                order_id=db_order.id
            )
            return db_order

    2. Report generation (with notification):
        @app.post("/reports")
        async def generate_report(
            report_request: ReportRequest,
            background_tasks: BackgroundTasks
        ):
            report_id = str(uuid.uuid4())
            reports[report_id] = {"status": "processing"}
            background_tasks.add_task(
                process_report, report_id, report_request
            )
            return {"report_id": report_id, "status": "processing"}

    3. Analytics tracking:
        @app.post("/analytics")
        async def track_event(
            event: AnalyticsEvent,
            background_tasks: BackgroundTasks
        ):
            background_tasks.add_task(
                process_analytics, event.dict()
            )
            return {"status": "tracked"}

Background functions:
    async def send_confirmation_email(email: str, order_id: int):
        await asyncio.sleep(1)  # Simulate email sending
        print(f"Email sent to {email} for order {order_id}")

    async def process_report(report_id: str, request: ReportRequest):
        # Simulate long-running report generation
        for i in range(10):
            await asyncio.sleep(1)
            reports[report_id]["progress"] = (i + 1) * 10
        reports[report_id]["status"] = "completed"
        reports[report_id]["url"] = f"/reports/{report_id}/download"

Hints:
    - BackgroundTasks is injected automatically by FastAPI
    - background_tasks.add_task(func, *args, **kwargs)
    - Tasks run after the response is sent
    - Tasks share the same database session (if using dependency injection)
    - For truly async tasks, use Celery, ARQ, or asyncio.create_task()

Test cases:
    # Create order (email sent in background)
    POST /orders {"item": "Widget", "email": "alice@example.com"}
    -> 201 {"id": 1, "item": "Widget"}
    (background: email sent to alice@example.com)

    # Generate report
    POST /reports {"type": "sales", "date_range": "2024-01"}
    -> 202 {"report_id": "abc-123", "status": "processing"}

    # Check report status
    GET /reports/abc-123
    -> 200 {"status": "completed", "progress": 100, "url": "/reports/abc-123/download"}
"""

# TODO: Write background tasks code below


# ============================================================
# Exercise 25.3: Application State Management
# ============================================================
"""
Problem:
    Build a robust application state management system.

State categories:
    1. Configuration (immutable after startup)
    2. Runtime state (changes during operation)
    3. Metrics (accumulated statistics)
    4. Cache (temporary data)

State manager:
    class AppState:
        def __init__(self):
            # Configuration (set on startup)
            self.config: dict = {}
            # Runtime state
            self.status: str = "initializing"
            self.start_time: float = 0
            # Metrics
            self.metrics = {
                "requests_total": 0,
                "errors_total": 0,
                "active_connections": 0
            }
            # Cache
            self.cache: dict = {}
            self.cache_ttl: dict = {}

        def increment_requests(self):
            self.metrics["requests_total"] += 1

        def increment_errors(self):
            self.metrics["errors_total"] += 1

        def cache_set(self, key: str, value: Any, ttl: int = 300):
            self.cache[key] = value
            self.cache_ttl[key] = time.time() + ttl

        def cache_get(self, key: str):
            if key in self.cache:
                if time.time() < self.cache_ttl.get(key, 0):
                    return self.cache[key]
                del self.cache[key]
            return None

Endpoints:
    GET  /state/config    - Get application configuration
    GET  /state/metrics   - Get current metrics
    POST /state/config    - Update configuration (admin only)
    GET  /state/cache/{key} - Get cached value
    POST /state/cache/{key} - Set cached value

Hints:
    - Store AppState instance in app.state
    - Middleware can update metrics on each request
    - Use atomic operations for concurrent metric updates
    - Consider using dataclasses or Pydantic for state validation
    - Thread-safe state for multi-worker deployments

Test cases:
    # Get configuration
    GET /state/config
    -> 200 {"app_name": "MyApp", "version": "1.0", "debug": false}

    # Get metrics
    GET /state/metrics
    -> 200 {"requests_total": 42, "errors_total": 3, "active_connections": 5}

    # Cache operations
    POST /state/cache/user:1 {"value": {"name": "Alice"}, "ttl": 60}
    -> 200 {"cached": true, "expires_in": 60}

    GET /state/cache/user:1
    -> 200 {"value": {"name": "Alice"}}
"""

# TODO: Write application state management below


# ============================================================
# Exercise 25.4: Health Check System
# ============================================================
"""
Problem:
    Build a comprehensive health check system.

Health check types:
    1. Basic liveness check (is the app running?)
    2. Readiness check (can the app serve traffic?)
    3. Detailed dependency checks (DB, cache, external APIs)
    4. Kubernetes-compatible probes

Endpoints:
    GET /health              - Basic liveness (returns 200 if running)
    GET /health/ready       - Readiness (returns 200 if ready to serve)
    GET /health/live        - Kubernetes liveness probe
    GET /health/detailed    - Full health report with dependencies

Health response:
    {
        "status": "healthy",
        "timestamp": "2024-01-15T10:30:00Z",
        "uptime_seconds": 125.3,
        "checks": {
            "database": {"status": "healthy", "latency_ms": 2.3},
            "cache": {"status": "healthy", "latency_ms": 0.5},
            "external_api": {"status": "degraded", "latency_ms": 1500.0},
            "disk_space": {"status": "healthy", "free_gb": 45.2}
        },
        "version": "1.2.3",
        "environment": "production"
    }

Health check implementation:
    async def check_database() -> dict:
        try:
            start = time.time()
            # Simulate DB ping
            await asyncio.sleep(0.002)
            latency = (time.time() - start) * 1000
            return {"status": "healthy", "latency_ms": round(latency, 1)}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    async def check_cache() -> dict:
        try:
            start = time.time()
            # Simulate cache ping
            await asyncio.sleep(0.0005)
            latency = (time.time() - start) * 1000
            return {"status": "healthy", "latency_ms": round(latency, 1)}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

Kubernetes probe endpoints:
    GET /health/live   -> 200 (app is alive)
    GET /health/ready  -> 200 (app is ready)
                       -> 503 (app is not ready)

Hints:
    - Liveness: just check if app is running (minimal check)
    - Readiness: check all critical dependencies
    - Use asyncio.gather() for parallel health checks
    - Cache health check results for 5 seconds
    - Return 503 for unhealthy, 200 for healthy
    - Consider adding version info for rolling deployments

Test cases:
    # Liveness probe
    GET /health/live
    -> 200 {"status": "alive"}

    # Readiness probe
    GET /health/ready
    -> 200 {"status": "ready"}

    # Detailed health
    GET /health/detailed
    -> 200 {
        "status": "healthy",
        "checks": {
            "database": {"status": "healthy", "latency_ms": 2.3},
            "cache": {"status": "healthy", "latency_ms": 0.5}
        }
    }

    # Unhealthy (simulate DB failure)
    GET /health/detailed
    -> 503 {
        "status": "unhealthy",
        "checks": {
            "database": {"status": "unhealthy", "error": "Connection refused"}
        }
    }
"""

# TODO: Write health check system below


# ============================================================
# Exercise 25.5: Event-Driven Architecture (Advanced)
# ============================================================
"""
Problem:
    Build a simple in-process event system for decoupled components.

Requirements:
    1. Create an EventBus class for publish/subscribe pattern
    2. Events are processed asynchronously
    3. Support multiple subscribers per event
    4. Include error handling and retry logic
    5. Events are logged for debugging

EventBus:
    class EventBus:
        def __init__(self):
            self.subscribers: dict[str, list[Callable]] = {}
            self.event_log: list[dict] = []

        def subscribe(self, event_type: str, handler: Callable):
            if event_type not in self.subscribers:
                self.subscribers[event_type] = []
            self.subscribers[event_type].append(handler)

        async def publish(self, event_type: str, data: dict):
            # Log the event
            self.event_log.append({
                "event": event_type,
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            })
            # Notify all subscribers
            if event_type in self.subscribers:
                for handler in self.subscribers[event_type]:
                    try:
                        await handler(data)
                    except Exception as e:
                        print(f"Handler error: {e}")

Usage:
    event_bus = EventBus()

    # Subscribe to events
    async def send_welcome_email(data: dict):
        print(f"Sending welcome email to {data['email']}")

    async def create_default_workspace(data: dict):
        print(f"Creating workspace for user {data['user_id']}")

    event_bus.subscribe("user.created", send_welcome_email)
    event_bus.subscribe("user.created", create_default_workspace)

    # Publish event (both handlers run)
    await event_bus.publish("user.created", {
        "user_id": 1,
        "email": "alice@example.com"
    })

Endpoints:
    POST /events            - Publish an event
    GET  /events            - List recent events
    POST /events/subscribe  - Subscribe to events (for demo)

Events to support:
    - user.created    -> Send welcome email, create workspace
    - order.placed    -> Update inventory, send notification
    - payment.received -> Update order status, generate invoice
    - report.ready    -> Send download link

Hints:
    - Use Callable type for handlers
    - Use asyncio.create_task() for fire-and-forget publishing
    - Store event log for debugging and replay
    - Consider using Redis Pub/Sub for distributed events
    - Add event IDs for tracking and deduplication

Test cases:
    # Publish event
    POST /events {"type": "user.created", "data": {"email": "alice@test.com"}}
    -> 202 {"event_id": "evt-123", "type": "user.created"}

    # List events
    GET /events
    -> 200 {"events": [{"event_id": "evt-123", "type": "user.created", ...}]}

    # Subscribe and receive events
    POST /events/subscribe {"event_type": "order.placed"}
    -> 200 {"subscriber_id": "sub-1"}
"""

# TODO: Write event-driven architecture code below


# ============================================================
# Running the Application
# ============================================================
"""
To run any exercise file:
    cd projects/00-core-foundations/python/fastapi/exercises
    uvicorn 25-events:app --reload --port 8000

Test with curl:
    curl http://localhost:8000/health
    curl http://localhost:8000/status

View API docs:
    http://localhost:8000/docs
    http://localhost:8000/redoc
"""
