"""
Exercise 21: Async Programming in FastAPI

Master async/await patterns in FastAPI applications.
Topics: async endpoints, async dependencies, async HTTP, concurrency.

Prerequisites:
- Python async/await basics
- asyncio event loop fundamentals
- FastAPI routing basics

Estimated time: 60-80 minutes
"""

from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from typing import List
import asyncio
import time
import uuid
from datetime import datetime

app = FastAPI(title="Async Programming Exercises")


# ============================================================
# Exercise 21.1: Sync vs Async Endpoints
# ============================================================

@app.get("/sync/slow")
def sync_slow():
    """Synchronous endpoint that blocks the thread for 2 seconds."""
    time.sleep(2)
    return {"type": "sync", "duration": 2, "message": "I blocked the thread!"}


@app.get("/async/slow")
async def async_slow():
    """Async endpoint that yields control for 2 seconds (non-blocking)."""
    await asyncio.sleep(2)
    return {"type": "async", "duration": 2, "message": "I didn't block the thread!"}


@app.get("/sync/fast")
def sync_fast():
    """Synchronous endpoint returning immediately."""
    return {"type": "sync", "duration": 0, "message": "Fast and synchronous"}


@app.get("/async/fast")
async def async_fast():
    """Async endpoint returning immediately."""
    return {"type": "async", "duration": 0, "message": "Fast and async"}


@app.get("/compare")
async def compare():
    """Compare sync sequential vs async concurrent execution."""
    # Sync sequential (calling async functions directly)
    start_sync = time.time()
    # Run sync endpoints sequentially
    sync_results = []
    sync_results.append(await async_slow())
    sync_results.append(await async_slow())
    sync_results.append(await async_slow())
    sync_results.append(await async_slow())
    sync_duration = time.time() - start_sync

    # Async concurrent using asyncio.gather
    start_async = time.time()
    tasks = [async_slow() for _ in range(4)]
    async_results = await asyncio.gather(*tasks)
    async_duration = time.time() - start_async

    return {
        "sync_sequential": round(sync_duration, 2),
        "async_concurrent": round(async_duration, 2),
        "sync_results": sync_results,
        "async_results": async_results
    }


# ============================================================
# Exercise 21.2: Async Dependencies
# ============================================================

MOCK_USERS = {
    1: {"id": 1, "name": "Alice", "role": "admin"},
    2: {"id": 2, "name": "Bob", "role": "user"},
    3: {"id": 3, "name": "Charlie", "role": "user"},
}


async def get_current_user(user_id: int = Header(alias="X-User-Id")):
    """Async dependency that simulates fetching user from DB."""
    await asyncio.sleep(0.1)  # Simulate DB lookup
    user = MOCK_USERS.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_admin_user(user: dict = Depends(get_current_user)):
    """Async dependency that checks for admin role."""
    await asyncio.sleep(0.05)  # Simulate permission check
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden: admin access required")
    return user


async def check_rate_limit(user: dict = Depends(get_current_user)):
    """Async dependency that simulates rate limit checking."""
    await asyncio.sleep(0.02)  # Simulate rate limit check
    # Always allow in this demo
    return user


@app.get("/admin/dashboard")
async def admin_dashboard(user: dict = Depends(get_admin_user)):
    """Admin-only dashboard endpoint."""
    return {
        "user": user["name"],
        "dashboard": {
            "total_users": len(MOCK_USERS),
            "active_sessions": 42,
            "system_health": "good"
        }
    }


@app.get("/admin/users")
async def admin_list_users(
    user: dict = Depends(get_admin_user),
    rate_ok: dict = Depends(check_rate_limit)
):
    """Admin-only users list with rate limiting."""
    return {
        "admin": user["name"],
        "users": [
            {"id": uid, "name": u["name"], "role": u["role"]}
            for uid, u in MOCK_USERS.items()
        ]
    }


@app.get("/profile")
async def get_profile(user: dict = Depends(get_current_user)):
    """Get current user's profile (any authenticated user)."""
    return {"user": user}


# ============================================================
# Exercise 21.3: Concurrent HTTP Requests
# ============================================================

# Simulated external API functions
async def fetch_weather(city: str) -> dict:
    """Simulate fetching weather data for a city."""
    await asyncio.sleep(0.5)  # Simulate API latency
    conditions = {
        "london": {"temp": 15.2, "condition": "cloudy", "humidity": 72},
        "paris": {"temp": 22.5, "condition": "sunny", "humidity": 55},
        "tokyo": {"temp": 28.0, "condition": "clear", "humidity": 60},
        "ny": {"temp": 18.3, "condition": "rainy", "humidity": 85},
        "sydney": {"temp": 30.1, "condition": "sunny", "humidity": 45},
    }
    data = conditions.get(city.lower(), {"temp": 20.0, "condition": "unknown", "humidity": 50})
    return {"city": city, **data}


async def fetch_stock_price(symbol: str) -> dict:
    """Simulate fetching stock price."""
    await asyncio.sleep(0.3)
    prices = {
        "AAPL": {"price": 150.25, "change": 2.3},
        "GOOGL": {"price": 2750.50, "change": -1.2},
        "MSFT": {"price": 338.10, "change": 0.8},
        "AMZN": {"price": 3450.00, "change": 1.5},
    }
    data = prices.get(symbol.upper(), {"price": 100.0, "change": 0.0})
    return {"symbol": symbol.upper(), **data}


@app.get("/weather/{city}")
async def get_weather(city: str):
    """Get weather for a single city."""
    result = await fetch_weather(city)
    return result


class BatchWeatherRequest(BaseModel):
    cities: List[str]


@app.post("/weather/batch")
async def batch_weather(req: BatchWeatherRequest):
    """Fetch weather for multiple cities concurrently."""
    start = time.time()
    tasks = [fetch_weather(city) for city in req.cities]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out any exceptions
    valid_results = [r for r in results if not isinstance(r, Exception)]
    duration_ms = round((time.time() - start) * 1000)

    return {"results": valid_results, "duration_ms": duration_ms}


@app.get("/portfolio/{symbols}")
async def get_portfolio(symbols: str):
    """Fetch stock prices for multiple symbols concurrently."""
    symbol_list = [s.strip() for s in symbols.split(",")]
    start = time.time()
    tasks = [fetch_stock_price(sym) for sym in symbol_list]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    valid_results = [r for r in results if not isinstance(r, Exception)]
    duration_ms = round((time.time() - start) * 1000)
    return {"prices": valid_results, "duration_ms": duration_ms}


# ============================================================
# Exercise 21.4: Async Background Tasks
# ============================================================

jobs: dict[str, dict] = {}


async def process_job(job_id: str, data: dict):
    """Background job processing function."""
    try:
        jobs[job_id]["status"] = "running"
        total_steps = 10
        for i in range(total_steps):
            # Check if cancelled
            if jobs[job_id].get("cancelled"):
                jobs[job_id]["status"] = "cancelled"
                jobs[job_id]["progress"] = 100
                return
            await asyncio.sleep(0.5)  # Simulate work
            jobs[job_id]["progress"] = ((i + 1) / total_steps) * 100
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["result"] = {"processed": True, "input": data}
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)


@app.post("/process", status_code=202)
async def start_processing(data: dict):
    """Start async processing and return job ID."""
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "pending",
        "progress": 0,
        "created_at": datetime.utcnow().isoformat()
    }
    asyncio.create_task(process_job(job_id, data))
    return {"job_id": job_id, "status": "pending"}


@app.get("/process/{job_id}")
async def get_job_status(job_id: str):
    """Check job status."""
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "job_id": job_id,
        "status": job["status"],
        "progress": job.get("progress", 0),
        "result": job.get("result"),
        "error": job.get("error")
    }


@app.post("/process/{job_id}/cancel")
async def cancel_job(job_id: str):
    """Cancel a running job."""
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job["status"] == "completed":
        return {"status": "already_completed"}
    job["cancelled"] = True
    job["status"] = "cancelled"
    return {"status": "cancelled"}


# ============================================================
# Exercise 21.5: Async Rate Limiter (Advanced)
# ============================================================

class AsyncRateLimiter:
    """Sliding window rate limiter using asyncio.Lock for thread safety."""

    def __init__(self, limit: int = 10, window: int = 60):
        self.limit = limit
        self.window = window
        self.requests: dict[str, list[float]] = {}
        self._lock = asyncio.Lock()

    async def check(self, key: str) -> tuple[bool, int]:
        """
        Check if request is allowed.
        Returns (allowed: bool, remaining_or_retry_after: int).
        """
        async with self._lock:
            now = time.time()
            if key not in self.requests:
                self.requests[key] = []

            # Remove old timestamps outside the window
            self.requests[key] = [
                t for t in self.requests[key]
                if now - t < self.window
            ]

            remaining = self.limit - len(self.requests[key])
            if remaining <= 0:
                # Calculate retry-after (seconds until oldest request expires)
                oldest = self.requests[key][0]
                retry_after = int(self.window - (now - oldest)) + 1
                return False, retry_after

            self.requests[key].append(now)
            return True, remaining - 1


rate_limiter = AsyncRateLimiter(limit=10, window=60)


@app.get("/rate-limited/data")
async def rate_limited_data(x_api_key: str = Header(default="default")):
    """Rate-limited data endpoint."""
    allowed, info = await rate_limiter.check(x_api_key)

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(info)}
        )

    return {
        "data": "This is rate-limited content",
        "rate_limit": {
            "limit": rate_limiter.limit,
            "remaining": info,
            "window_seconds": rate_limiter.window
        }
    }
