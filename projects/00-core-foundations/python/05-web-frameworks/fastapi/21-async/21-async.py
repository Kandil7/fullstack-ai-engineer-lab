"""
21 - Async/Await
==================
Async support in FastAPI for non-blocking I/O operations.
FastAPI supports both sync and async functions.

Run: uvicorn 21-async:app --reload
"""

import sys
import asyncio
import time
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks
import httpx

app = FastAPI(title="Async/Await in FastAPI")


# ----- Sync vs Async endpoints -----
@app.get("/sync")
def sync_endpoint():
    """
    Synchronous endpoint.
    FastAPI runs it in a thread pool automatically.
    Good for CPU-bound or traditional I/O tasks.
    """
    time.sleep(1)  # Simulates blocking I/O
    return {"type": "sync", "message": "Handled in thread pool"}


@app.get("/async")
async def async_endpoint():
    """
    Asynchronous endpoint.
    Runs directly on the event loop.
    Better for I/O-bound tasks (DB, HTTP calls, file I/O).
    """
    await asyncio.sleep(1)  # Non-blocking sleep
    return {"type": "async", "message": "Handled on event loop"}


# ----- Concurrent operations -----
@app.get("/concurrent")
async def concurrent_operations():
    """
    Run multiple I/O operations concurrently.
    asyncio.gather runs them in parallel — much faster than sequential.
    """
    start = time.perf_counter()

    # These run concurrently (not sequentially!)
    results = await asyncio.gather(
        simulate_db_query("users"),
        simulate_db_query("orders"),
        simulate_db_query("products"),
    )

    elapsed = (time.perf_counter() - start) * 1000
    return {
        "results": results,
        "elapsed_ms": round(elapsed, 2),
        "note": "All 3 queries ran concurrently (~1s, not ~3s)",
    }


@app.get("/sequential")
async def sequential_operations():
    """
    Sequential I/O — slower than concurrent.
    Each await blocks until the previous one completes.
    """
    start = time.perf_counter()

    r1 = await simulate_db_query("users")
    r2 = await simulate_db_query("orders")
    r3 = await simulate_db_query("products")

    elapsed = (time.perf_counter() - start) * 1000
    return {
        "results": [r1, r2, r3],
        "elapsed_ms": round(elapsed, 2),
        "note": "Sequential — ~3s total",
    }


async def simulate_db_query(table: str) -> dict:
    """Simulate an async database query."""
    await asyncio.sleep(1)  # Simulate network/DB latency
    return {
        "table": table,
        "rows": 42,
        "timestamp": datetime.now().isoformat(),
    }


# ----- Async HTTP client -----
@app.get("/fetch/")
async def fetch_url(url: str = "https://httpbin.org/get"):
    """
    Make an async HTTP request.
    Uses httpx for async HTTP (like requests but async).
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10.0)
        return {
            "status": response.status_code,
            "url": url,
            "headers": dict(response.headers),
        }


@app.get("/fetch/multiple")
async def fetch_multiple():
    """
    Fetch multiple URLs concurrently.
    All requests run in parallel — much faster than sequential.
    """
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/ip",
        "https://httpbin.org/user-agent",
    ]

    async with httpx.AsyncClient() as client:
        tasks = [client.get(url, timeout=10.0) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

    results = []
    for url, resp in zip(urls, responses):
        if isinstance(resp, Exception):
            results.append({"url": url, "error": str(resp)})
        else:
            results.append({"url": url, "status": resp.status_code})

    return {"results": results}


# ----- Async background tasks -----
@app.post("/process-async/")
async def process_async(data: str, background_tasks: BackgroundTasks):
    """
    Combine async endpoint with background tasks.
    The response is sent immediately; heavy processing runs in background.
    """
    background_tasks.add_task(heavy_processing, data)
    return {"status": "processing", "data": data}


async def heavy_processing(data: str):
    """Simulate heavy async processing."""
    await asyncio.sleep(2)
    print(f"✅ Processed: {data}")


# ----- Async generator for streaming -----
@app.get("/stream/")
async def stream_data():
    """
    Async generator for streaming responses.
    Data is sent chunk by chunk.
    """
    from fastapi.responses import StreamingResponse

    async def generate():
        for i in range(10):
            yield f"Chunk {i}: {datetime.now().isoformat()}\n"
            await asyncio.sleep(0.5)

    return StreamingResponse(generate(), media_type="text/plain")


# ----- Semaphore for rate limiting -----
semaphore = asyncio.Semaphore(5)  # Max 5 concurrent requests


@app.get("/rate-limited/")
async def rate_limited_endpoint():
    """
    Async semaphore for limiting concurrent operations.
    Useful for API rate limiting or DB connection pools.
    """
    async with semaphore:
        await asyncio.sleep(1)
        return {"message": "Processed within concurrency limit", "timestamp": datetime.now().isoformat()}


"""
Testing with curl:
    curl http://127.0.0.1:8000/sync         # ~1s
    curl http://127.0.0.1:8000/async        # ~1s

    time curl http://127.0.0.1:8000/concurrent   # ~1s (3 queries in parallel)
    time curl http://127.0.0.1:8000/sequential    # ~3s (3 queries sequentially)

    curl http://127.0.0.1:8000/fetch/
    curl http://127.0.0.1:8000/fetch/multiple

    curl -X POST "http://127.0.0.1:8000/process-async/?data=test"
    curl http://127.0.0.1:8000/stream/  (or open in browser)

    # Load test concurrency:
    for i in $(seq 1 10); do curl http://127.0.0.1:8000/rate-limited/ & done; wait
"""

def _verify():
    """Smoke-test the app in-process with TestClient (no real server).

    Only endpoints with simulated (deterministic) delays are exercised.
    /fetch* need real network so they are intentionally NOT called here;
    /sequential, /stream/ and /rate-limited/ are skipped to stay fast.
    """
    try:
        from fastapi.testclient import TestClient
    except ImportError:
        print("[skip] fastapi not installed")
        return

    client = TestClient(app)

    r = client.get("/sync")  # ~1s (thread pool)
    assert r.status_code == 200
    assert r.json()["type"] == "sync"

    r = client.get("/async")  # ~1s (event loop)
    assert r.status_code == 200
    assert r.json()["type"] == "async"

    r = client.get("/concurrent")  # ~1s (3 queries gathered in parallel)
    assert r.status_code == 200
    assert len(r.json()["results"]) == 3

    print("[OK] 21-async: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        _verify()
