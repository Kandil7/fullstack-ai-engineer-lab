"""
FastAPI — 46: Health & Readiness
==================================
Topics: liveness vs readiness vs startup; dependency checks; graceful
        shutdown and in-flight draining; SIGTERM; deployment interaction

Why this matters for AI/backend engineering:
    Orchestrators (K8s, ECS, Nomad) decide your service's fate from its
    health endpoints. Three DIFFERENT endpoints with three different
    jobs: liveness ("is the process alive?" — crash -> restart),
    readiness ("can it serve traffic?" — no -> stop routing), and
    startup ("is it still warming up?" — yes -> delay probes). The
    distinction is life-or-death: a readiness check that fails when the
    DB blips makes the orchestrator restart a perfectly healthy process.
    Graceful shutdown drains in-flight requests so a deploy doesn't kill
    a generation mid-stream.

Run:      python 46-health-and-readiness.py
Verify:   python 46-health-and-readiness.py --verify
Reference: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
"""

from __future__ import annotations

import json
import signal
import sys
import threading
import time
from typing import Optional

# ============================================================
# 1. The three probes — different questions, different endpoints
# ============================================================
# Liveness : "is the process alive?"   -> crash => restart container
# Readiness: "can it serve traffic?"   -> no => stop routing, keep process
# Startup  : "is it still warming up?" -> yes => delay other probes

class HealthState:
    def __init__(self) -> None:
        self.alive = True
        self.ready = False
        self.startup_complete = False
        self.deps: dict[str, bool] = {"db": True, "cache": True, "model": False}

    def liveness(self) -> tuple[int, dict]:
        # 200 if the process can do ANYTHING (even erroring is 'alive')
        if not self.alive:
            return 500, {"status": "dead"}
        return 200, {"status": "alive"}

    def readiness(self) -> tuple[int, dict]:
        # 200 only when every critical dependency is reachable
        if not all(self.deps.values()):
            failed = [k for k, v in self.deps.items() if not v]
            return 503, {"status": "not ready", "failed_deps": failed}
        return 200, {"status": "ready"}

    def startup(self) -> tuple[int, dict]:
        if not self.startup_complete:
            return 503, {"status": "starting"}
        return 200, {"status": "started"}


hs = HealthState()
print("=== 1. Three probes, three questions ===")
print(f"liveness before startup: {hs.liveness()[1]['status']}  (process is up)")
print(f"startup before done    : {hs.startup()[1]['status']}   (still warming)")
print(f"readiness before model : {hs.readiness()[1]}  (no traffic yet)")
print()

# ============================================================
# 2. Dependency checks — readiness fails on DB blip
# ============================================================
# Readiness polls dependencies. When the DB blips, readiness returns
# 503, the orchestrator stops sending traffic — and does NOT kill the
# process (that is liveness's job). Wrong probe on the wrong endpoint
# = crash loop.

print("=== 2. Dependency checks ===")
hs.deps["db"] = False
print(f"db down -> readiness: {hs.readiness()[1]}")
hs.deps["db"] = True
hs.deps["model"] = True
hs.startup_complete = True
print(f"all up  -> readiness: {hs.readiness()[1]}")
print()

# ============================================================
# 3. Graceful shutdown + in-flight draining
# ============================================================
# On SIGTERM the service should: stop accepting new work, wait for
# in-flight requests to finish (drain), THEN exit. Killing mid-request
# drops generations; draining lets them complete within a timeout.

class GracefulServer:
    def __init__(self) -> None:
        self.in_flight = 0
        self.draining = False
        self._lock = threading.Lock()

    def start_request(self) -> bool:
        with self._lock:
            if self.draining:
                return False            # new work refused during drain
            self.in_flight += 1
            return True

    def finish_request(self) -> None:
        with self._lock:
            self.in_flight -= 1

    def begin_shutdown(self) -> int:
        """Stop accepting work; return how many requests must drain."""
        with self._lock:
            self.draining = True
            return self.in_flight

    def drain(self, timeout: float) -> bool:
        """Wait (up to timeout) for in-flight requests to finish."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            with self._lock:
                if self.in_flight == 0:
                    return True
            time.sleep(0.005)
        return False                    # timeout: force-exit remaining


server = GracefulServer()
print("=== 3. Graceful shutdown ===")
assert server.start_request()           # request A in flight
assert server.start_request()           # request B in flight
pending = server.begin_shutdown()
print(f"SIGTERM received; {pending} in-flight request(s) must drain")
print(f"new work during drain accepted: {server.start_request()} (refused)")
server.finish_request()
server.finish_request()
print(f"drained within timeout: {server.drain(0.5)}")
print()

# ============================================================
# 4. SIGTERM handler wiring (simulated)
# ============================================================
# Production: signal handler flips draining; the event loop keeps
# serving in-flight work until empty or the grace period expires.

def install_shutdown_handler(server: GracefulServer) -> None:
    def _on_sigterm(signum, frame):
        pending = server.begin_shutdown()
        print(f"[signal] SIGTERM: draining {pending} in-flight requests")
    signal.signal(signal.SIGTERM, _on_sigterm)


print("=== 4. SIGTERM wiring ===")
install_shutdown_handler(server)
print("handler installed: SIGTERM -> begin_shutdown (drain) -> exit")
print()

# ============================================================
# 5. Deployment interaction
# ============================================================
# Startup probe delays traffic until the model is loaded (cold start).
# Readiness routes traffic only to warmed pods. Liveness restarts
# crashed processes. Graceful shutdown makes deploys zero-loss.

def deploy_sequence(hs: HealthState) -> list[str]:
    events = []
    events.append("pod scheduled")
    events.append(f"startup probe -> {hs.startup()[0]} (503: loading)")
    hs.deps["model"] = True
    hs.startup_complete = True
    events.append(f"startup probe -> {hs.startup()[0]} (200: loaded)")
    events.append(f"readiness probe -> {hs.readiness()[0]} (200: routing)")
    events.append("traffic flows")
    return events


print("=== 5. Deployment interaction ===")
for e in deploy_sequence(HealthState()):
    print(f"  {e}")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: one /health endpoint for everything — a DB blip kills the
#   process via liveness, or a model reload stops all probes
# CORRECT: /health/live (alive), /health/ready (deps), /health/startup
#
# MISTAKE: readiness checks external services on every poll with
#   timeouts — slow deps make readiness flaky
# CORRECT: short, cached dependency checks (few seconds TTL)
#
# MISTAKE: no drain — SIGTERM kills in-flight generations mid-stream
# CORRECT: stop accepting, drain within grace, then exit
#
# MISTAKE: startup probe missing — orchestrator routes traffic into a
#   pod that is still loading a 2GB model
# CORRECT: startup probe gates traffic until warm

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""

    # 1. The three probes answer three different questions
    hs0 = HealthState()
    assert hs0.liveness()[0] == 200, "liveness is about the process"
    assert hs0.startup()[0] == 503, "startup gated until warm"
    assert hs0.readiness()[0] == 503, "readiness gated on deps"

    # 2. A dependency failure makes readiness 503 but liveness 200
    hs0.deps["cache"] = False
    assert hs0.readiness()[0] == 503 and "cache" in hs0.readiness()[1]["failed_deps"]
    assert hs0.liveness()[0] == 200, "process stays alive during a blip"

    # 3. After startup + deps, everything is green
    hs0.deps["cache"] = True
    hs0.deps["model"] = True
    hs0.startup_complete = True
    assert hs0.readiness()[0] == 200 and hs0.startup()[0] == 200

    # 4. Graceful shutdown: refuse new work, drain the rest
    s = GracefulServer()
    assert s.start_request() and s.start_request()
    assert s.begin_shutdown() == 2, "two requests must drain"
    assert s.start_request() is False, "new work refused while draining"
    s.finish_request(); s.finish_request()
    assert s.drain(0.5) is True, "drain completes when empty"

    # 5. Drain times out gracefully if requests hang
    s2 = GracefulServer()
    s2.start_request()
    s2.begin_shutdown()
    assert s2.drain(0.02) is False, "drain must fail on timeout (force exit)"

    print("[OK] 46-health-and-readiness: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Liveness = alive; readiness = can serve; startup = warmed")
        print("2. Dependency checks gate readiness, never liveness")
        print("3. SIGTERM -> stop accepting -> drain -> exit")
        print("4. Probes wire the deploy: startup delays, readiness routes")
        _verify()          # always runs, so plain execution is also a test
