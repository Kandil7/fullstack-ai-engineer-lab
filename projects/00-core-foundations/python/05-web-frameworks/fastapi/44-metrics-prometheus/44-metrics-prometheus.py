"""
FastAPI — 44: Metrics with Prometheus
=======================================
Topics: the four golden signals; counters/gauges/histograms; RED and USE
        methods; cardinality explosions; /metrics; SLI/SLO definition

Why this matters for AI/backend engineering:
    Logs tell you WHAT happened; metrics tell you HOW the service is
    doing RIGHT NOW. The four golden signals (latency, traffic, errors,
    saturation) are the same four numbers that decide if an LLM service
    is healthy. The three metric types — counter (monotonic), gauge
    (level), histogram (distribution) — map to the signals. The two
    frameworks — RED (Rate/Errors/Duration per request) and USE
    (Utilization/Saturation/Errors per resource) — tell you what to
    instrument. This exercise implements all of it with the prometheus
    client, including a cardinality trap.

Run:      python 44-metrics-prometheus.py
Verify:   python 44-metrics-prometheus.py --verify
Reference: https://prometheus.io/docs/concepts/metric_types/
"""

from __future__ import annotations

import random
import sys
import time
from typing import Optional

from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram

# ============================================================
# 1. The three metric types
# ============================================================
# Counter  : monotonic increasing (requests, tokens, errors)
# Gauge    : a level that goes up and down (in-flight, queue depth, GPU util)
# Histogram: a distribution (latency buckets, token-count buckets)

reg = CollectorRegistry()
REQUESTS = Counter("http_requests_total", "Total requests", ["path", "status"], registry=reg)
IN_FLIGHT = Gauge("http_in_flight", "Requests currently executing", registry=reg)
LATENCY = Histogram("http_request_duration_seconds", "Latency",
                    buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0), registry=reg)
TOKENS = Histogram("llm_tokens_total", "Tokens generated", buckets=(16, 64, 256, 1024, 4096), registry=reg)


def simulate_request(path: str) -> float:
    """Simulate one request: record in-flight, latency, status, tokens."""
    IN_FLIGHT.inc()
    start = time.perf_counter()
    time.sleep(random.uniform(0.001, 0.01))       # simulated work
    latency = time.perf_counter() - start
    status = "200" if random.random() > 0.05 else "500"
    tokens = int(random.choice([16, 64, 128, 512, 2048]))
    REQUESTS.labels(path=path, status=status).inc()
    LATENCY.observe(latency)
    TOKENS.observe(tokens)
    IN_FLIGHT.dec()
    return latency


print("=== 1. Metric types ===")
for _ in range(200):
    simulate_request("/generate")
for _ in range(100):
    simulate_request("/embed")
total = REQUESTS.labels(path="/generate", status="200")._value.get()
print(f"counter /generate 200: {total}")
print(f"gauge in-flight after: {IN_FLIGHT._value.get()}")
print(f"histogram buckets    : {LATENCY._sum.get():.4f}s total over {LATENCY._count.get()} samples")
print()

# ============================================================
# 2. The four golden signals
# ============================================================
# Latency  : histogram of request duration (p50/p95/p99)
# Traffic  : request counter (rate per second)
# Errors   : counter of 5xx (rate)
# Saturation: gauge of in-flight / queue depth / utilization

def golden_signals(registry: CollectorRegistry) -> dict:
    """Compute the four signals from the metrics collected."""
    counts = {("generate", "200"): REQUESTS.labels(path="/generate", status="200")._value.get(),
              ("generate", "500"): REQUESTS.labels(path="/generate", status="500")._value.get(),
              ("embed", "200"): REQUESTS.labels(path="/embed", status="200")._value.get(),
              ("embed", "500"): REQUESTS.labels(path="/embed", status="500")._value.get()}
    latency = LATENCY._sum.get() / max(LATENCY._count.get(), 1)
    error_rate = (counts[("generate", "500")] + counts[("embed", "500")]) / \
                 max(counts[("generate", "200")] + counts[("embed", "200")] +
                     counts[("generate", "500")] + counts[("embed", "500")], 1)
    return {
        "latency_avg_s": round(latency, 4),
        "traffic_requests": int(REQUESTS._value.get()),
        "error_rate": round(error_rate, 4),
        "in_flight": int(IN_FLIGHT._value.get()),
    }


print("=== 2. Golden signals ===")
print(golden_signals(reg))
print()

# ============================================================
# 3. RED vs USE
# ============================================================
# RED : Rate, Errors, Duration — PER REQUEST (services)
# USE : Utilization, Saturation, Errors — PER RESOURCE (infra)
# An LLM service exposes both: RED on /generate, USE on GPU/queue.

RED_LABELS = ["rate_requests_per_s", "errors_per_s", "duration_p95_s"]
USE_LABELS = ["utilization", "saturation", "resource_errors"]

def red_vs_use() -> dict:
    return {
        "RED (/generate)": {"rate": 120.0, "errors": 6.0, "duration_p95": 1.8},
        "USE (gpu:0)": {"utilization": 0.87, "saturation": 0.42, "errors": 0.0},
    }


print("=== 3. RED vs USE ===")
for k, v in red_vs_use().items():
    print(f"  {k}: {v}")
print()

# ============================================================
# 4. Cardinality explosion — the metric killer
# ============================================================
# Every unique label value creates a NEW time series. A 'prompt' or
# 'user_id' label means a new series per user per prompt — the
# database dies while the app looks fine. Labels must be bounded
# sets: path, status, model, tenant. NEVER free-form text.

def label_cardinality_bad() -> int:
    """BROKEN: user_id in labels -> unbounded series."""
    return 0  # (would be: 1 series per user)

def label_cardinality_good() -> int:
    """Correct: bounded labels. Models/tenants are small closed sets."""
    models = {"gpt-4o", "gpt-4o-mini", "claude-3.5", "llama-3-70b"}
    tenants = {"acme", "globex"}
    return len(models) * len(tenants)   # 8 series, bounded


print("=== 4. Cardinality ===")
print(f"bounded labels -> {label_cardinality_good()} series (models × tenants)")
print(f"user_id label  -> unbounded (1 series per user — never)")
print()

# ============================================================
# 5. SLI / SLO
# ============================================================
# SLI: the measured indicator (e.g. p95 latency <= 2s for 99% of
# requests). SLO: the target — "99% of /generate requests complete
# under 2s over 30 days". The error budget is the allowed misses.

def sli_passes(error_rate: float, p95: float, target: tuple) -> bool:
    """Check an SLI against its SLO target."""
    rate_target, latency_target = target
    return error_rate <= rate_target and p95 <= latency_target


print("=== 5. SLI / SLO ===")
slo = (0.01, 2.0)   # 1% errors, p95 < 2s
print(f"current p95=1.8, errors=1.5% -> within SLO: {sli_passes(0.015, 1.8, slo)}")
print(f"current p95=3.1, errors=0.5% -> within SLO: {sli_passes(0.005, 3.1, slo)}")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: labeling with unbounded values (user_id, prompt hash, ip)
#   -> cardinality explosion; the TSDB dies silently
# CORRECT: bounded label sets only; put free-form text in log lines
#
# MISTAKE: averaging latency — p50 hides the tail that kills users
# CORRECT: histograms; alert on p95/p99
#
# MISTAKE: no error counter per endpoint — errors invisible until paging
# CORRECT: counter with path+status labels
#
# MISTAKE: forgetting saturation — the service is 'fast' while the GPU
#   queue grows; USE covers resources, RED covers requests
# CORRECT: both perspectives

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""

    r = CollectorRegistry()
    c = Counter("c_total", "count", ["kind"], registry=r)
    g = Gauge("g", "gauge", registry=r)
    h = Histogram("h", "hist", buckets=(0.1, 0.5, 1.0), registry=r)

    # 1. Counter increments monotonically
    c.labels(kind="a").inc()
    c.labels(kind="a").inc(3)
    assert c.labels(kind="a")._value.get() == 4, "counter accumulates"
    assert c.labels(kind="b")._value.get() == 0, "labels are separate series"

    # 2. Gauge reflects a level
    g.inc(); g.inc(); g.dec()
    assert g._value.get() == 1, "gauge goes up and down"

    # 3. Histogram records sum + count (latency math works)
    h.observe(0.2); h.observe(0.6); h.observe(1.5)
    assert h._count.get() == 3
    assert abs(h._sum.get() - 2.3) < 1e-9
    assert h._buckets[0]._value.get() == 0, "nothing under 0.1"
    assert h._buckets[1]._value.get() == 1, "0.2 lands in <=0.5"

    # 4. Bounded label sets keep cardinality small
    assert label_cardinality_good() == 8, "models × tenants = 8 bounded series"

    # 5. SLO math
    assert sli_passes(0.005, 1.5, (0.01, 2.0))
    assert not sli_passes(0.02, 1.5, (0.01, 2.0)), "error rate above target"
    assert not sli_passes(0.005, 2.5, (0.01, 2.0)), "latency above target"

    # 6. Golden signals computed from real registry
    gs = golden_signals(reg)
    assert gs["traffic_requests"] == 300, "counter totals match the simulation"
    assert 0 <= gs["error_rate"] <= 0.1, "error rate in a sane band"
    assert gs["in_flight"] == 0, "no request left in-flight"

    print("[OK] 44-metrics-prometheus: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Counter/Gauge/Histogram map to the golden signals")
        print("2. RED (requests) + USE (resources) = both perspectives")
        print("3. Cardinality: bounded labels or the TSDB dies")
        print("4. SLI measured, SLO targeted, budget spent deliberately")
        _verify()          # always runs, so plain execution is also a test
