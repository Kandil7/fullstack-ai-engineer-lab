"""
32 - Async Endpoints Deep
===========================
def vs async def in FastAPI (the threadpool subtlety), never block the
event loop, run_in_threadpool, measuring both, when sync is correct.

Run:      python 32-async-endpoints-deep.py
Verify:   python 32-async-endpoints-deep.py --verify
Reference: https://fastapi.tiangolo.com/async/
"""

from __future__ import annotations

import asyncio
import sys
import time

from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

app = FastAPI(title="Async vs Sync Endpoints")

# A real blocking workload: CPU-bound or I/O via blocking libraries
def blocking_work(seconds: float) -> str:
    """Simulates a blocking call (requests, DB driver, CPU crunch)."""
    time.sleep(seconds)
    return f"blocking work done after {seconds}s"


async def async_work(seconds: float) -> str:
    """Simulates a genuinely async I/O call (aiohttp, asyncpg)."""
    await asyncio.sleep(seconds)
    return f"async work done after {seconds}s"


# ============================================================
# 1. async def endpoint — correct only if the body never blocks
# ============================================================
@app.get("/async/correct")
async def async_correct() -> dict:
    """await-based I/O: the event loop stays free for other requests."""
    result = await async_work(0.05)
    return {"kind": "async", "result": result}


# ============================================================
# 2. async def endpoint that BLOCKS — the classic footgun
# ============================================================
@app.get("/async/blocking")
async def async_blocking() -> dict:
    """time.sleep inside async def BLOCKS THE EVENT LOOP: while this runs,
    every other request on the process waits. This is the #1 FastAPI bug."""
    result = blocking_work(0.05)     # BAD: blocking call in the loop
    return {"kind": "async-but-blocking", "result": result}


# ============================================================
# 3. def endpoint — FastAPI runs it in a threadpool
# ============================================================
@app.get("/sync")
def sync_endpoint() -> dict:
    """Plain def: FastAPI runs the handler in a worker thread, so the
    event loop stays free. Correct home for blocking libraries."""
    result = blocking_work(0.05)
    return {"kind": "sync", "result": result}


# ============================================================
# 4. run_in_threadpool — escape to a thread inside async code
# ============================================================
@app.get("/async/threaded")
async def async_threaded() -> dict:
    """Keep the async signature but hand blocking work to a thread."""
    result = await run_in_threadpool(blocking_work, 0.05)
    return {"kind": "async+thread", "result": result}


# ============================================================
# 5. Measuring the cost of blocking the loop
# ============================================================
def demonstrate_blocking() -> None:
    """Two async handlers, one blocking: total wall time reveals the bug."""
    async def run_clean() -> float:
        start = time.perf_counter()
        await asyncio.gather(*[async_correct_body() for _ in range(4)])
        return time.perf_counter() - start

    async def async_correct_body() -> None:
        await asyncio.sleep(0.1)

    async def run_blocking() -> float:
        start = time.perf_counter()
        # four 'blocking' async calls, each sleeps 0.1s INSIDE the loop
        await asyncio.gather(*[blocked_body() for _ in range(4)])
        return time.perf_counter() - start

    async def blocked_body() -> None:
        time.sleep(0.1)     # blocks the loop

    clean = asyncio.run(run_clean())
    blocked = asyncio.run(run_blocking())
    print(f"  async (await sleep)  : {clean:.3f}s  (parallel, ~1x)")
    print(f"  async (time.sleep)   : {blocked:.3f}s  (serial, ~4x)")
    print("  -> blocking the loop serializes concurrent requests")


# ============================================================
# Summary
# ============================================================
print("=" * 60)
print("Summary:")
print("- async def: right for await-based I/O; WRONG if the body blocks")
print("- def      : FastAPI runs it in a threadpool; right for blocking libs")
print("- run_in_threadpool: escape to a thread inside async handlers")
print("- Rule: never put time.sleep / requests / CPU loops in async def")
print("=" * 60)
demonstrate_blocking()


def _verify() -> None:
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        for path in ("/async/correct", "/async/blocking", "/sync", "/async/threaded"):
            r = client.get(path)
            assert r.status_code == 200, f"{path} must return 200"
            assert "done after 0.05s" in r.json()["result"]

        # The three correct styles all behave; the point is the concurrency
        # behavior demonstrated in demonstrate_blocking(), not the status.
        r = client.get("/async/correct")
        assert r.json()["kind"] == "async"

    print("[OK] 32-async-endpoints-deep: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run("32-async-endpoints-deep:app", host="127.0.0.1", port=8000)
    else:
        _verify()
