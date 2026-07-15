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

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import asyncio
import time
import httpx
from datetime import datetime

app = FastAPI(title="Async Programming Exercises")

# ============================================================
# Exercise 21.1: Sync vs Async Endpoints
# ============================================================
"""
Problem:
    Create both sync and async versions of the same endpoint
    and understand the differences.

Requirements:
    1. Create GET /sync/slow - synchronous endpoint that "blocks" for 2 seconds
    2. Create GET /async/slow - async endpoint that awaits for 2 seconds
    3. Create GET /sync/fast - synchronous endpoint that returns immediately
    4. Create GET /async/fast - async endpoint that returns immediately
    5. Create GET /compare - endpoint that calls all four and measures time

Sync blocking endpoint:
    @app.get("/sync/slow")
    def sync_slow():
        time.sleep(2)  # Blocks the thread!
        return {"type": "sync", "duration": 2}

Async non-blocking endpoint:
    @app.get("/async/slow")
    async def async_slow():
        await asyncio.sleep(2)  # Yields control, doesn't block
        return {"type": "async", "duration": 2}

Compare endpoint should show:
    {
        "sync_sequential": ~8.0,  # 4 endpoints x 2s each
        "async_concurrent": ~2.0,  # all run in parallel
        "sync_results": [...],
        "async_results": [...]
    }

Hints:
    - time.sleep() blocks the thread (bad for async)
    - asyncio.sleep() yields control (good for async)
    - Use asyncio.gather() to run async functions concurrently
    - Use time.time() to measure execution time
    - Test with: curl timing or pytest with multiple requests

Test cases:
    # Sync slow takes ~2 seconds
    GET /sync/slow
    -> 200 {"type": "sync", "duration": 2}  (takes ~2s)

    # Async slow also takes ~2 seconds but doesn't block other requests
    GET /async/slow
    -> 200 {"type": "async", "duration": 2}  (takes ~2s)

    # Compare shows sync is sequential, async is parallel
    GET /compare
    -> 200 {"sync_sequential": >6, "async_concurrent": <3}
"""

# TODO: Write your code below


# ============================================================
# Exercise 21.2: Async Dependencies
# ============================================================
"""
Problem:
    Create async dependencies that perform I/O operations.

Requirements:
    1. Create an async dependency that simulates fetching user from DB
    2. Create an async dependency that simulates checking permissions
    3. Create an async dependency that simulates rate limit checking
    4. Chain multiple async dependencies together

Async dependency pattern:
    async def get_current_user(user_id: int = Header(...)):
        await asyncio.sleep(0.1)  # Simulate DB lookup
        return {"id": user_id, "name": "Alice", "role": "admin"}

    async def check_permissions(user: dict = Depends(get_current_user)):
        await asyncio.sleep(0.05)  # Simulate permission check
        if user["role"] != "admin":
            raise HTTPException(status_code=403, detail="Forbidden")
        return user

Endpoints using dependencies:
    GET /admin/dashboard - requires admin user
    GET /admin/users - requires admin user with rate limit check

Hints:
    - Dependencies can be async: async def my_dep() -> dict:
    - Use Depends() to inject dependencies
    - Dependencies can depend on other dependencies
    - FastAPI resolves dependencies in dependency order
    - Async dependencies run concurrently when possible

Test cases:
    # Valid admin request
    GET /admin/dashboard
    Headers: X-User-Id: 1
    -> 200 {"user": "Alice", "dashboard": {...}}

    # Non-admin user
    GET /admin/dashboard
    Headers: X-User-Id: 2 (role=user)
    -> 403 {"detail": "Forbidden"}

    # Missing user header
    GET /admin/dashboard
    -> 422 Validation Error
"""

# TODO: Write your code below


# ============================================================
# Exercise 21.3: Concurrent HTTP Requests
# ============================================================
"""
Problem:
    Build endpoints that make concurrent external API calls.

Endpoints:
    GET /weather/{city}       - Fetch weather for a city
    GET /weather/batch        - Fetch weather for multiple cities concurrently
    GET /prices/{symbol}      - Fetch stock price
    GET /portfolio/{symbols}  - Fetch multiple stock prices concurrently

Simulated external APIs (use asyncio.sleep to simulate latency):
    async def fetch_weather(city: str) -> dict:
        await asyncio.sleep(0.5)  # Simulate API latency
        return {
            "city": city,
            "temp": 22.5,
            "condition": "sunny",
            "humidity": 65
        }

    async def fetch_stock_price(symbol: str) -> dict:
        await asyncio.sleep(0.3)  # Simulate API latency
        return {
            "symbol": symbol,
            "price": 150.25,
            "change": +2.3
        }

Batch endpoint should:
    1. Accept a list of cities in the request body
    2. Use asyncio.gather() to fetch all concurrently
    3. Return results as soon as all complete
    4. Handle individual failures gracefully

Request model:
    class BatchWeatherRequest(BaseModel):
        cities: list[str]

Hints:
    - Use httpx.AsyncClient for real HTTP calls
    - Use asyncio.gather(*tasks, return_exceptions=True)
    - Filter out exceptions from results
    - Use asyncio.create_task() for independent fetches
    - Consider using TaskGroup in Python 3.11+

Test cases:
    # Single city
    GET /weather/london
    -> 200 {"city": "london", "temp": 22.5, ...}

    # Batch (should complete in ~0.5s, not 2.5s)
    POST /weather/batch {"cities": ["london", "paris", "tokyo", "ny", "sydney"]}
    -> 200 {"results": [...5 cities...], "duration_ms": <600}

    # Portfolio (single request for multiple stocks)
    GET /portfolio/AAPL,GOOGL,MSFT
    -> 200 {"prices": [...], "duration_ms": <400}
"""

# TODO: Write your code below


# ============================================================
# Exercise 21.4: Async Background Tasks
# ============================================================
"""
Problem:
    Implement async background task processing.

Endpoints:
    POST /process           - Start async processing, return job ID
    GET /process/{job_id}   - Check job status
    POST /process/{job_id}/cancel - Cancel a running job

Job states: pending -> running -> completed/failed/cancelled

Requirements:
    1. Jobs run in the background using asyncio.create_task()
    2. Job status is tracked in memory (dict)
    3. Jobs can be cancelled mid-execution
    4. Failed jobs include error messages

Async job pattern:
    jobs: dict[str, dict] = {}

    async def process_job(job_id: str, data: dict):
        try:
            jobs[job_id]["status"] = "running"
            for i in range(10):
                if jobs[job_id].get("cancelled"):
                    jobs[job_id]["status"] = "cancelled"
                    return
                await asyncio.sleep(1)  # Simulate work
                jobs[job_id]["progress"] = (i + 1) * 10
            jobs[job_id]["status"] = "completed"
            jobs[job_id]["result"] = {"processed": True}
        except Exception as e:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["error"] = str(e)

    @app.post("/process")
    async def start_processing(data: dict):
        job_id = str(uuid.uuid4())
        jobs[job_id] = {"status": "pending", "progress": 0}
        asyncio.create_task(process_job(job_id, data))
        return {"job_id": job_id, "status": "pending"}

Hints:
    - Use asyncio.create_task() for fire-and-forget background work
    - Use a dict to store job status (in production, use Redis/DB)
    - Check for cancellation flag in your processing loop
    - Return job ID immediately, let client poll for status
    - Consider using FastAPI BackgroundTasks for simpler cases

Test cases:
    # Start processing
    POST /process {"data": "process this"}
    -> 202 {"job_id": "abc-123", "status": "pending"}

    # Check status (initially pending/running)
    GET /process/abc-123
    -> 200 {"status": "running", "progress": 30}

    # Cancel job
    POST /process/abc-123/cancel
    -> 200 {"status": "cancelled"}

    # Check cancelled job
    GET /process/abc-123
    -> 200 {"status": "cancelled"}
"""

# TODO: Write your code below


# ============================================================
# Exercise 21.5: Async Rate Limiter (Advanced)
# ============================================================
"""
Problem:
    Build an async rate limiter using a sliding window algorithm.

Requirements:
    1. Track request counts per API key
    2. Use sliding window (last 60 seconds)
    3. Allow 100 requests per minute per API key
    4. Return 429 Too Many Requests with retry-after header
    5. Rate limiter must be async-safe (concurrent requests)

Sliding window implementation:
    - Store timestamps of recent requests per key
    - On each request, remove timestamps older than 60s
    - Count remaining timestamps
    - If count >= limit, reject with 429

    class AsyncRateLimiter:
        def __init__(self, limit: int = 100, window: int = 60):
            self.limit = limit
            self.window = window
            self.requests: dict[str, list[float]] = {}

        async def check(self, key: str) -> tuple[bool, int]:
            """Returns (allowed, remaining)"""
            now = time.time()
            if key not in self.requests:
                self.requests[key] = []
            # Remove old timestamps
            self.requests[key] = [
                t for t in self.requests[key]
                if now - t < self.window
            ]
            remaining = self.limit - len(self.requests[key])
            if remaining <= 0:
                oldest = self.requests[key][0]
                retry_after = int(self.window - (now - oldest)) + 1
                return False, retry_after
            self.requests[key].append(now)
            return True, remaining - 1

Endpoints:
    GET /rate-limited/data - Rate limited data endpoint

Response headers:
    X-RateLimit-Limit: 100
    X-RateLimit-Remaining: 95
    X-RateLimit-Reset: 1693000060
    Retry-After: 30  (only on 429)

Hints:
    - Use asyncio.Lock() to prevent race conditions
    - Use time.time() for timestamps
    - Add rate limit headers to every response
    - Consider using a sorted list for efficient sliding window
    - In production, use Redis for distributed rate limiting

Test cases:
    # Normal request
    GET /rate-limited/data
    Headers: X-Api-Key: test-key
    -> 200 {"data": "..."}
    Headers: X-RateLimit-Remaining: 99

    # After many requests
    (make 100 requests)
    GET /rate-limited/data
    -> 429 {"detail": "Rate limit exceeded"}
    Headers: Retry-After: 30
"""

# TODO: Write your code below
