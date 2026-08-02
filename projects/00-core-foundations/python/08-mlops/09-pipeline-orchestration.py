"""
MLOps - 09: Pipeline Orchestration
==================================
Topics: DAGs, retries, scheduling, backfills, idempotent tasks, failure
handling. A minimal, dependency-respecting scheduler - the same shape as
Prefect/Airflow DAGs - so the concepts transfer.

Why this matters for AI/backend engineering:
    Training pipelines are not a script; they are a graph of steps with
    dependencies, retries, and failure semantics. Idempotency is what makes
    retries and backfills safe - without it, a re-run duplicates work or
    corrupts state.

Run:      python 09-pipeline-orchestration.py
Verify:   python 09-pipeline-orchestration.py --verify
Reference: https://docs.prefect.io/
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Callable, Optional


# ============================================================
# 1. A DAG Is a Dependency Graph
# ============================================================
# Task C depends on outputs of A and B. A scheduler must run A and B
# before C, in any order, and skip nothing.

@dataclass
class Task:
    name: str
    fn: Callable[[dict], object]
    depends_on: list[str] = field(default_factory=list)
    max_retries: int = 0

    def run(self, results: dict) -> object:
        return self.fn(results)


# Example 1: define a small pipeline
def _ingest(results: dict) -> int:
    return 100


def _clean(results: dict) -> int:
    return results["ingest"] - 10


def _train(results: dict) -> float:
    return 0.90


tasks = {
    "ingest": Task("ingest", _ingest),
    "clean": Task("clean", _clean, depends_on=["ingest"]),
    "train": Task("train", _train, depends_on=["clean"]),
}


# ============================================================
# 2. Topological Execution
# ============================================================
def run_dag(tasks: dict[str, Task]) -> dict[str, object]:
    """Execute tasks in dependency order (simple Kahn's algorithm)."""
    results: dict[str, object] = {}
    pending = set(tasks)
    while pending:
        progressed = False
        for name in list(pending):
            task = tasks[name]
            if all(dep in results for dep in task.depends_on):
                results[name] = task.run(results)
                pending.discard(name)
                progressed = True
        if not progressed:
            raise RuntimeError("cycle detected in DAG")
    return results


# Example 2: run the pipeline
print("Example 2: topological execution")
out = run_dag(tasks)
print(f"  ingest={out['ingest']} clean={out['clean']} train={out['train']}")
assert out["clean"] == 90, "clean ran after ingest"

# ============================================================
# 3. Retries with Backoff
# ============================================================
# Transient failures (network, quota) deserve retry; retries need
# backoff and a cap so they do not hammer a dying service.

import time as _time


def run_with_retries(task: Task, results: dict,
                     backoff_s: float = 0.01) -> object:
    attempt = 0
    while True:
        try:
            return task.run(results)
        except Exception:
            attempt += 1
            if attempt > task.max_retries:
                raise
            _time.sleep(backoff_s * (2 ** (attempt - 1)))


# Example 3: retry a flaky task
flaky_calls = {"n": 0}


def _flaky(results: dict) -> str:
    flaky_calls["n"] += 1
    if flaky_calls["n"] < 3:
        raise ConnectionError("transient")
    return "ok"


flaky = Task("flaky", _flaky, max_retries=3)
result = run_with_retries(flaky, {})
print("\nExample 3: retries")
print(f"  result={result} after {flaky_calls['n']} attempts")
assert result == "ok" and flaky_calls["n"] == 3

# ============================================================
# 4. Idempotency
# ============================================================
# A task is idempotent if running it twice equals running it once.
# That is what makes retries and backfills safe.

def make_idempotent_counter() -> Callable[[dict], int]:
    state = {"seen": False}
    def _run(results: dict) -> int:
        if state["seen"]:
            return 42  # already done - return same result, no side effect
        state["seen"] = True
        return 42
    return _run


# Example 4: idempotent task behaves the same on re-run
idem = make_idempotent_counter()
first = run_with_retries(Task("idem", idem), {})
second = run_with_retries(Task("idem", idem), {})
print("\nExample 4: idempotency")
print(f"  first={first} second={second} (equal: {first == second})")
assert first == second

# ============================================================
# Production Pattern
# ============================================================
# The production DAG runner: order, retries, and a failure that
# stops the pipeline loudly instead of silently producing bad data.

def orchestrate(tasks: dict[str, Task]) -> dict[str, object]:
    """Run a DAG with per-task retries; fail loudly on real errors."""
    results: dict[str, object] = {}
    pending = set(tasks)
    while pending:
        progressed = False
        for name in list(pending):
            task = tasks[name]
            if all(dep in results for dep in task.depends_on):
                results[name] = run_with_retries(task, results)
                pending.discard(name)
                progressed = True
        if not progressed:
            raise RuntimeError(f"cycle or unsatisfied deps: {sorted(pending)}")
    return results


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: retrying non-transient errors (a bug will never succeed)
# MISTAKE: no backoff - retries become a DDoS on the failing service
# MISTAKE: non-idempotent tasks + retries = double-written outputs
# MISTAKE: swallowing exceptions and continuing with partial data


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    # topological order
    tasks2 = {
        "a": Task("a", lambda r: 1),
        "b": Task("b", lambda r: r["a"] + 1, depends_on=["a"]),
        "c": Task("c", lambda r: r["b"] * 2, depends_on=["b"]),
    }
    res = run_dag(tasks2)
    assert res == {"a": 1, "b": 2, "c": 4}, "deps respected"

    # cycle detection
    cyclic = {
        "x": Task("x", lambda r: 1, depends_on=["y"]),
        "y": Task("y", lambda r: 1, depends_on=["x"]),
    }
    try:
        run_dag(cyclic)
        raised = False
    except RuntimeError:
        raised = True
    assert raised, "cycle must raise"

    # retry exhaustion
    def _always_fail(results: dict) -> object:
        raise ValueError("permanent")
    t = Task("f", _always_fail, max_retries=2)
    try:
        run_with_retries(t, {}, backoff_s=0.0)
        raised = False
    except ValueError:
        raised = True
    assert raised, "retries exhausted -> raise"

    # idempotency
    counter = {"n": 0}
    def _inc(results: dict) -> int:
        counter["n"] += 1
        return counter["n"]
    twice = [run_with_retries(Task("i", _inc), {}, backoff_s=0.0) for _ in range(2)]
    assert twice == [1, 2], "non-idempotent task differs on re-run"
    print("[OK] 09-pipeline-orchestration: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Pipelines are DAGs - dependencies define order.")
        print("2. Retry transient errors with backoff and a cap.")
        print("3. Make tasks idempotent so retries and backfills are safe.")
        _verify()
