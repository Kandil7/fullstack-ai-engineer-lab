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

from fastapi import FastAPI, BackgroundTasks, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Any, Callable
from contextlib import asynccontextmanager
from datetime import datetime
import asyncio
import time
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("events")


# ============================================================
# Exercise 25.1: Startup and Shutdown Events
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Modern lifespan context manager for startup/shutdown."""
    # Startup
    app.state.db = {"connected": True, "pool_size": 10}
    app.state.cache = {}
    app.state.start_time = time.time()
    app.state.ready = True
    app.state.request_count = 0
    logger.info(f"Application started at {datetime.utcnow().isoformat()}")

    yield

    # Shutdown
    app.state.ready = False
    app.state.db = {"connected": False}
    uptime = time.time() - app.state.start_time
    logger.info(f"Application shutting down. Uptime: {uptime:.1f}s, Requests handled: {app.state.request_count}")


app = FastAPI(title="Events & Lifespan Exercises", lifespan=lifespan)


@app.get("/health")
async def health_check(request: Request):
    """Basic health check with startup status."""
    ready = request.app.state.ready
    if not ready:
        raise HTTPException(status_code=503, detail="Service is shutting down")
    return {"status": "healthy", "ready": ready, "timestamp": datetime.utcnow().isoformat()}


@app.get("/status")
async def application_status(request: Request):
    """Detailed application status."""
    uptime = time.time() - request.app.state.start_time
    return {
        "ready": request.app.state.ready,
        "uptime_seconds": round(uptime, 1),
        "database": "connected" if request.app.state.db.get("connected") else "disconnected",
        "cache_items": len(request.app.state.cache),
        "requests_handled": request.app.state.request_count,
    }


@app.get("/uptime")
async def get_uptime(request: Request):
    """Application uptime."""
    uptime = time.time() - request.app.state.start_time
    return {"uptime_seconds": round(uptime, 1), "started_at": datetime.fromtimestamp(request.app.state.start_time).isoformat()}


# ============================================================
# Exercise 25.2: Background Tasks
# ============================================================

orders_for_background: List[dict] = []
reports_store: dict = {}


async def send_confirmation_email(email: str, order_id: int, item: str):
    """Simulate sending a confirmation email in the background."""
    await asyncio.sleep(1)  # Simulate email sending
    logger.info(f"Email sent to {email} for order #{order_id}: {item}")


class OrderCreate(BaseModel):
    item: str
    email: str


@app.post("/orders", status_code=201)
async def create_order(order: OrderCreate, background_tasks: BackgroundTasks):
    """Create an order and send confirmation email in background."""
    order_id = len(orders_for_background) + 1
    orders_for_background.append({"id": order_id, **order.model_dump()})

    background_tasks.add_task(
        send_confirmation_email,
        email=order.email,
        order_id=order_id,
        item=order.item
    )

    return {"id": order_id, "item": order.item, "status": "created"}


class ReportRequest(BaseModel):
    type: str
    date_range: str


async def process_report(report_id: str, request_data: ReportRequest):
    """Generate a report in the background with progress updates."""
    reports_store[report_id] = {"status": "processing", "progress": 0}

    total_steps = 10
    for i in range(total_steps):
        await asyncio.sleep(0.3)
        reports_store[report_id]["progress"] = ((i + 1) / total_steps) * 100

    reports_store[report_id]["status"] = "completed"
    reports_store[report_id]["progress"] = 100
    reports_store[report_id]["url"] = f"/reports/{report_id}/download"
    logger.info(f"Report {report_id} completed")


@app.post("/reports", status_code=202)
async def generate_report(report_request: ReportRequest, background_tasks: BackgroundTasks):
    """Generate a report asynchronously."""
    report_id = str(uuid.uuid4())[:8]
    background_tasks.add_task(process_report, report_id, report_request)
    return {"report_id": report_id, "status": "processing"}


@app.get("/reports/{report_id}")
async def get_report_status(report_id: str):
    """Check report generation status."""
    report = reports_store.get(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"report_id": report_id, **report}


class AnalyticsEvent(BaseModel):
    event_type: str
    user_id: str
    properties: dict = {}


async def process_analytics(event: dict):
    """Process analytics event in background."""
    await asyncio.sleep(0.2)
    logger.info(f"Analytics processed: {event['event_type']} for user {event['user_id']}")


@app.post("/analytics")
async def track_event(event: AnalyticsEvent, background_tasks: BackgroundTasks):
    """Track analytics event asynchronously."""
    background_tasks.add_task(process_analytics, event.model_dump())
    return {"status": "tracked", "event_type": event.event_type}


# ============================================================
# Exercise 25.3: Application State Management
# ============================================================

class AppState:
    """Robust application state management system."""

    def __init__(self):
        # Configuration (immutable after startup)
        self.config: dict = {
            "app_name": "FastAPI Events Demo",
            "version": "1.0.0",
            "debug": False,
            "max_requests_per_minute": 100,
        }
        # Runtime state
        self.status: str = "initializing"
        self.start_time: float = time.time()
        # Metrics
        self.metrics = {
            "requests_total": 0,
            "errors_total": 0,
            "active_connections": 0,
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

    def cache_get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            if time.time() < self.cache_ttl.get(key, 0):
                return self.cache[key]
            del self.cache[key]
            del self.cache_ttl[key]
        return None


app_state = AppState()


@app.on_event("startup")
async def start_state():
    app_state.status = "running"


@app.get("/state/config")
async def get_config():
    """Get application configuration."""
    return app_state.config


@app.get("/state/metrics")
async def get_metrics():
    """Get current metrics."""
    return {
        **app_state.metrics,
        "uptime_seconds": round(time.time() - app_state.start_time, 1),
        "cache_size": len(app_state.cache),
    }


@app.post("/state/config")
async def update_config(config: dict):
    """Update configuration (admin only)."""
    app_state.config.update(config)
    return {"updated": True, "config": app_state.config}


@app.get("/state/cache/{key}")
async def get_cached_value(key: str):
    """Get cached value by key."""
    value = app_state.cache_get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Cache miss")
    return {"key": key, "value": value, "source": "cache"}


class CacheSetRequest(BaseModel):
    value: Any
    ttl: int = 60


@app.post("/state/cache/{key}")
async def set_cached_value(key: str, req: CacheSetRequest):
    """Set a cached value with TTL."""
    app_state.cache_set(key, req.value, req.ttl)
    return {"cached": True, "key": key, "expires_in": req.ttl}


# Middleware to track metrics
@app.middleware("http")
async def track_metrics(request: Request, call_next):
    """Middleware that tracks request metrics."""
    app_state.increment_requests()
    request.app.state.request_count += 1
    response = await call_next(request)
    if response.status_code >= 400:
        app_state.increment_errors()
    return response


# ============================================================
# Exercise 25.4: Health Check System
# ============================================================

async def check_database() -> dict:
    """Check database connectivity."""
    try:
        start = time.time()
        await asyncio.sleep(0.002)  # Simulate DB ping
        latency = (time.time() - start) * 1000
        return {"status": "healthy", "latency_ms": round(latency, 1)}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


async def check_cache() -> dict:
    """Check cache connectivity."""
    try:
        start = time.time()
        await asyncio.sleep(0.0005)  # Simulate cache ping
        latency = (time.time() - start) * 1000
        return {"status": "healthy", "latency_ms": round(latency, 1)}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


async def check_disk_space() -> dict:
    """Check available disk space."""
    import shutil
    try:
        total, used, free = shutil.disk_usage(".")
        free_gb = free / (1024 ** 3)
        status = "healthy" if free_gb > 1.0 else "degraded" if free_gb > 0.1 else "unhealthy"
        return {"status": status, "free_gb": round(free_gb, 1)}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@app.get("/health/live")
async def liveness_probe():
    """Kubernetes liveness probe - checks if app is running."""
    return {"status": "alive"}


@app.get("/health/ready")
async def readiness_probe(request: Request):
    """Kubernetes readiness probe - checks if app is ready to serve traffic."""
    if not request.app.state.ready:
        raise HTTPException(status_code=503, detail="Service not ready")
    return {"status": "ready"}


@app.get("/health/detailed")
async def detailed_health():
    """Full health report with dependency checks."""
    checks = await asyncio.gather(
        check_database(),
        check_cache(),
        check_disk_space(),
    )

    health_data = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": round(time.time() - app_state.start_time, 1),
        "checks": {
            "database": checks[0],
            "cache": checks[1],
            "disk_space": checks[2],
        },
        "version": app_state.config.get("version", "unknown"),
        "environment": "development",
    }

    # Determine overall status
    statuses = [c["status"] for c in checks]
    if "unhealthy" in statuses:
        health_data["status"] = "unhealthy"
    elif "degraded" in statuses:
        health_data["status"] = "degraded"

    if health_data["status"] != "healthy":
        return JSONResponse(status_code=503, content=health_data)

    return health_data


# ============================================================
# Exercise 25.5: Event-Driven Architecture (Advanced)
# ============================================================

class EventBus:
    """Simple in-process publish/subscribe event system."""

    def __init__(self):
        self.subscribers: dict[str, list[Callable]] = {}
        self.event_log: list[dict] = []
        self._event_counter = 0

    def subscribe(self, event_type: str, handler: Callable):
        """Register a handler for an event type."""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
        logger.info(f"Subscribed handler '{handler.__name__}' to event '{event_type}'")

    async def publish(self, event_type: str, data: dict) -> str:
        """Publish an event and notify all subscribers."""
        self._event_counter += 1
        event_id = f"evt-{self._event_counter}"

        # Log the event
        event_entry = {
            "event_id": event_id,
            "type": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.event_log.append(event_entry)

        # Notify all subscribers
        if event_type in self.subscribers:
            for handler in self.subscribers[event_type]:
                try:
                    await handler(data)
                except Exception as e:
                    logger.error(f"Handler '{handler.__name__}' failed for event '{event_type}': {e}")

        return event_id


event_bus = EventBus()


# Define some event handlers
async def send_welcome_email(data: dict):
    """Handler: Send welcome email on user.created."""
    await asyncio.sleep(0.1)
    logger.info(f"Welcome email sent to {data.get('email', 'unknown')}")


async def create_default_workspace(data: dict):
    """Handler: Create default workspace on user.created."""
    await asyncio.sleep(0.2)
    logger.info(f"Default workspace created for user {data.get('user_id', 'unknown')}")


async def update_inventory(data: dict):
    """Handler: Update inventory on order.placed."""
    await asyncio.sleep(0.15)
    logger.info(f"Inventory updated for order {data.get('order_id', 'unknown')}")


async def send_order_notification(data: dict):
    """Handler: Send order notification on order.placed."""
    await asyncio.sleep(0.1)
    logger.info(f"Order notification sent for order {data.get('order_id', 'unknown')}")


# Subscribe handlers to events
event_bus.subscribe("user.created", send_welcome_email)
event_bus.subscribe("user.created", create_default_workspace)
event_bus.subscribe("order.placed", update_inventory)
event_bus.subscribe("order.placed", send_order_notification)


class PublishEventRequest(BaseModel):
    type: str
    data: dict = {}


@app.post("/events", status_code=202)
async def publish_event(event: PublishEventRequest):
    """Publish an event to the event bus."""
    event_id = await event_bus.publish(event.type, event.data)
    return {"event_id": event_id, "type": event.type}


@app.get("/events")
async def list_events(limit: int = 10):
    """List recent events from the event log."""
    recent = event_bus.event_log[-limit:]
    return {"events": recent, "total": len(event_bus.event_log)}


class SubscribeRequest(BaseModel):
    event_type: str


subscribers_db: dict = {}


@app.post("/events/subscribe")
async def subscribe_to_event(req: SubscribeRequest):
    """Register a dynamic subscriber for demo purposes."""
    sub_id = f"sub-{len(subscribers_db) + 1}"
    subscribers_db[sub_id] = req.event_type

    async def dynamic_handler(data: dict):
        logger.info(f"[Dynamic subscriber {sub_id}] Event '{req.event_type}': {data}")

    event_bus.subscribe(req.event_type, dynamic_handler)
    return {"subscriber_id": sub_id, "event_type": req.event_type}
