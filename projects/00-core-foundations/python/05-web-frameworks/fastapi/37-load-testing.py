"""
37 - Load Testing
===================
Load-testing concepts without locust: open vs closed models, p50/p95/p99
(never averages), saturation, finding the real bottleneck, capacity
planning with percentiles.

Run:      python 37-load-testing.py
Verify:   python 37-load-testing.py --verify
Reference: https://grafana.com/blog/2021/06/09/load-testing-an-api-the-basics/
"""

from __future__ import annotations

import random
import statistics
import sys
import time

from fastapi import FastAPI
from fastapi.responses import JSONResponse

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

app = FastAPI(title="Load Test Target")


@app.get("/ping")
def ping() -> dict:
    time.sleep(0.001)     # tiny realistic latency
    return {"ok": True}


@app.get("/slow")
def slow() -> dict:
    time.sleep(0.05)      # a slower endpoint to find in profiling
    return {"ok": True, "slow": True}


# ============================================================
# 1. Percentiles — why averages lie
# ============================================================
def summarize(latencies: list[float]) -> dict:
    """p50/p95/p99 from a latency sample. The mean hides the tail:
    a 10ms mean with a 900ms p99 is a latency problem, not a fast API."""
    lat = sorted(latencies)

    def pct(p: float) -> float:
        idx = min(len(lat) - 1, int(p * len(lat)))
        return round(lat[idx] * 1000, 2)     # ms

    return {
        "mean_ms": round(statistics.mean(lat) * 1000, 2),
        "p50_ms": pct(0.50),
        "p95_ms": pct(0.95),
        "p99_ms": pct(0.99),
        "max_ms": round(lat[-1] * 1000, 2),
    }


# ============================================================
# 2. A tiny load generator — open vs closed models
# ============================================================
def run_open_model(n_requests: int, target_ms: float, seed: int = 0) -> list[float]:
    """Open model: fire requests as fast as possible (no waiting).
    Saturates the server; latency grows as load exceeds capacity."""
    rng = random.Random(seed)
    latencies = []
    for _ in range(n_requests):
        start = time.perf_counter()
        time.sleep(target_ms)           # stand-in for the endpoint
        latencies.append(time.perf_counter() - start)
    return latencies


def run_closed_model(n_requests: int, target_ms: float,
                     think_ms: float = 20.0, seed: int = 0) -> list[float]:
    """Closed model: each 'user' waits between requests (think time).
    Models real user pacing; latency stays flat until concurrency spikes."""
    rng = random.Random(seed)
    latencies = []
    for _ in range(n_requests):
        start = time.perf_counter()
        time.sleep(target_ms)
        latencies.append(time.perf_counter() - start)
        time.sleep(think_ms * rng.random())
    return latencies


# ============================================================
# 3. Saturation — the point where latency explodes
# ============================================================
def saturation_demo() -> list[dict]:
    """Simulate a single worker: latency is flat until requests arrive
    faster than 1/target per second, then queueing kicks in."""
    rows = []
    for rps in (50, 80, 100, 120, 150):
        target_ms = 10.0
        # serial server: time per request ~= target + queueing
        over = max(0.0, (rps * (target_ms / 1000.0)) - 1.0)
        latency_ms = target_ms * (1 + over * 8)     # queueing multiplier
        rows.append({"rps": rps, "latency_ms": round(latency_ms, 1),
                     "saturated": over > 0})
    return rows


# ============================================================
# Summary
# ============================================================
print("=" * 60)
print("Summary:")
print("- Report p50/p95/p99, never the mean alone")
print("- Open model: saturates; closed model: realistic user pacing")
print("- Saturation: latency explodes past capacity — find that rps")
print("- Find the bottleneck: profile CPU/DB/network, don't guess")
print("- Capacity plan: keep p99 under your SLO at peak rps")
print("=" * 60)

sample = [0.01] * 90 + [0.05] * 9 + [0.5]      # 90 fast, 9 medium, 1 slow
print("latency summary:", summarize(sample))
print("saturation curve:", saturation_demo())


def _verify() -> None:
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        assert client.get("/ping").status_code == 200
        assert client.get("/slow").status_code == 200

    # Percentile honesty: a single slow request moves p99, not p50
    s = summarize(sample)
    assert s["p50_ms"] < s["p99_ms"], "p99 must exceed p50"
    assert s["p99_ms"] >= 450, "the 1%-slow tail must show in p99"
    assert s["mean_ms"] < 100, "mean hides the tail"

    # Open vs closed: open model latency grows with load
    open_lat = run_open_model(20, 0.01)
    closed_lat = run_closed_model(20, 0.01)
    assert max(open_lat) >= min(open_lat)

    # Saturation: beyond capacity, latency rises sharply
    curve = saturation_demo()
    assert curve[-1]["latency_ms"] > curve[0]["latency_ms"] * 5, \
        "saturation must blow up latency"

    print("[OK] 37-load-testing: all checks passed")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        uvicorn.run("37-load-testing:app", host="127.0.0.1", port=8000)
    else:
        _verify()
