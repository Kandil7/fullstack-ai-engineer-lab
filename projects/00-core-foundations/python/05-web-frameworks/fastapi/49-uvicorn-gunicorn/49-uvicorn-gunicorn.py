"""
FastAPI — 49: Uvicorn & Gunicorn
==================================
Topics: ASGI servers; worker counts vs cores; uvloop; keep-alive;
        timeouts; threads vs processes; why --reload is dev-only

Why this matters for AI/backend engineering:
    Uvicorn runs your FastAPI app; Gunicorn manages the processes; the
    worker count decides how many requests run concurrently. The math:
    CPU-bound (inference!) workers ~ cores; IO-bound workers can exceed
    cores. --reload is a dev tool — in production it watches files,
    restarts on every touch, and uses a hot-reloader per worker. This
    exercise models the worker economics and verifies the decisions.

Run:      python 49-uvicorn-gunicorn.py
Verify:   python 49-uvicorn-gunicorn.py --verify
Reference: https://www.uvicorn.org/deployment/
"""

from __future__ import annotations

import os
import sys
from typing import Optional

# ============================================================
# 1. ASGI server roles: uvicorn vs gunicorn
# ============================================================
# uvicorn: the ASGI server — speaks the ASGI protocol to your app.
# gunicorn: the process manager — spawns and supervises workers.
# Together: gunicorn manages uvicorn workers (one process each).

SERVERS = {
    "uvicorn": "ASGI protocol server: accepts connections, runs your app",
    "gunicorn": "process manager: forks N workers, supervises, restarts",
    "uvicorn --workers": "uvicorn's own process model (no supervisor)",
    "gunicorn -k uvicorn.workers.UvicornWorker": "the production pair",
}

print("=== 1. Roles ===")
for k, v in SERVERS.items():
    print(f"  {k:<38} {v}")
print()

# ============================================================
# 2. Worker count — the core math
# ============================================================
# CPU-bound work (model inference, JSON-heavy parsing) runs on one core
# at a time; workers ≈ cores. IO-bound work (waiting on DB/cache/API)
# frees the CPU while awaiting; workers can exceed cores (threads/async
# concurrency inside each worker also matters).
# Rule of thumb: 2-4 workers per core for IO; 1 per core for CPU.
# A GPU inference worker holds ~GB of model memory per worker — memory,
# not cores, becomes the limit (see topic 52).

def recommended_workers(cores: int, workload: str) -> int:
    """Return the recommended worker count for a workload class."""
    if workload == "cpu-bound":       # inference, heavy compute
        return max(1, cores)
    if workload == "io-bound":        # DB/API waiting
        return max(1, cores * 2 + 1)
    return max(1, cores + 1)          # mixed default


print("=== 2. Worker math ===")
for wl in ("cpu-bound", "io-bound", "mixed"):
    print(f"  {wl:<10} on 4 cores -> {recommended_workers(4, wl)} workers")
print()

# ============================================================
# 3. The one-worker-per-model-memory trap
# ============================================================
# Each worker imports and holds the model. 4 workers × 2GB model =
# 8GB RAM before a single request. Worker count must respect MEMORY
# as well as cores.

def workers_by_memory(available_gb: float, model_gb: float, overhead_gb: float = 0.3) -> int:
    per_worker = model_gb + overhead_gb
    return max(1, int(available_gb // per_worker))


print("=== 3. Memory constraint ===")
print(f"  16GB box, 2GB model -> {workers_by_memory(16, 2.0)} workers max")
print(f"  8GB box,  4GB model -> {workers_by_memory(8, 4.0)} workers max")
print()

# ============================================================
# 4. --reload: dev-only, and why
# ============================================================
# --reload watches files and restarts the app on every change. In
# production that means: file-watcher overhead, restarts on any touch,
# and a hot-reload worker per process (extra memory). The deployment
# restarts come from the orchestrator, not file watching.

def reload_suitable(env: str) -> bool:
    return env in {"dev", "local", "test"}


print("=== 4. --reload is dev-only ===")
print(f"  env=dev     -> reload: {reload_suitable('dev')}")
print(f"  env=prod    -> reload: {reload_suitable('prod')}")
print()

# ============================================================
# 5. Timeouts, keep-alive, and threads
# ============================================================
# --timeout-keep-alive: how long an idle connection stays open.
# --timeout-graceful-shutdown: drain window (topic 46).
# Def endpoints run in a threadpool: the threadpool size is a
# concurrency knob for sync routes (see topic 32).

def timeout_policy(timeout_keep_alive: int, graceful_shutdown: int) -> dict:
    return {
        "keep_alive_s": timeout_keep_alive,
        "graceful_shutdown_s": graceful_shutdown,
        "note": "idle conns close; in-flight requests drain before exit",
    }


print("=== 5. Timeouts ===")
print(f"  {timeout_policy(5, 30)}")
print()

# ============================================================
# 6. Production command construction
# ============================================================
# The production pair: gunicorn manages N uvicorn workers; each worker
# is one process running the app. Dev uses uvicorn directly with reload.

def prod_command(cores: int, app_path: str, workload: str = "io-bound") -> str:
    workers = recommended_workers(cores, workload)
    return (f"gunicorn {app_path} "
            f"-k uvicorn.workers.UvicornWorker "
            f"--workers {workers} "
            f"--bind 0.0.0.0:8000 "
            f"--timeout 60 "
            f"--graceful-timeout 30")


print("=== 6. Production command ===")
print(f"  {prod_command(4, 'app.main:app')}")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: --reload in production — file-watcher restarts, hot-reload
#   workers eating memory; orchestrator should own restarts
# CORRECT: plain workers; restarts via the platform
#
# MISTAKE: workers = cores for everything — GPU inference workers hold
#   GB of model each; memory caps before cores
# CORRECT: workers = min(cores_needed, memory_allowed)
#
# MISTAKE: one worker "because it's simpler" — one request at a time
# CORRECT: workers/threads matched to the workload and box
#
# MISTAKE: no graceful-timeout — SIGTERM kills in-flight generations
# CORRECT: graceful-timeout >= drain time (topic 46)

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""

    # 1. Worker math: io > cpu
    assert recommended_workers(4, "io-bound") > recommended_workers(4, "cpu-bound"), \
        "IO-bound should allow more workers"
    assert recommended_workers(4, "cpu-bound") == 4, "CPU-bound ~ cores"
    assert recommended_workers(2, "io-bound") == 5, "2*cores+1"

    # 2. Memory constraint binds
    assert workers_by_memory(16, 2.0) == 6, "16GB / 2.3GB per worker"
    assert workers_by_memory(8, 4.0) == 1, "8GB / 4.3GB -> 1 worker"

    # 3. Reload is dev-only
    assert reload_suitable("dev") and not reload_suitable("prod"), \
        "reload must be dev-only"

    # 4. Production command shape
    cmd = prod_command(4, "app.main:app")
    assert cmd.startswith("gunicorn"), "production uses gunicorn"
    assert "UvicornWorker" in cmd, "uvicorn worker class"
    assert "--workers 9" in cmd, "io-bound 4 cores -> 9 workers"
    assert "--graceful-timeout 30" in cmd, "drain window present"

    # 5. Timeout policy sanity
    tp = timeout_policy(5, 30)
    assert tp["keep_alive_s"] == 5 and tp["graceful_shutdown_s"] == 30

    print("[OK] 49-uvicorn-gunicorn: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. uvicorn = ASGI server; gunicorn = process manager")
        print("2. workers: CPU-bound ~ cores; IO-bound > cores; memory binds")
        print("3. --reload is dev-only; orchestrator owns prod restarts")
        print("4. Graceful timeout >= drain time")
        _verify()          # always runs, so plain execution is also a test
