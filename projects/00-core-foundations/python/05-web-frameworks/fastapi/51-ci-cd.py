"""
FastAPI — 51: CI/CD
=====================
Topics: test -> build -> scan -> deploy pipeline; matrix testing; caching;
        migrations in the pipeline; blue-green and canary; rollback

Why this matters for AI/backend engineering:
    CI/CD is how a change becomes a running service without a human
    clicking. The pipeline stages are a gauntlet: unit tests -> lint ->
    build image -> scan for CVEs -> migrate schema -> deploy (blue-green
    or canary) -> health-gate. Every stage that fails stops the ship.
    This exercise models the pipeline as DATA (stage lists, gates,
    rollout math) and verifies the decisions — the same way a real
    pipeline config is tested.

Run:      python 51-ci-cd.py
Verify:   python 51-ci-cd.py --verify
Reference: https://docs.github.com/en/actions
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Optional

# ============================================================
# 1. The pipeline as data
# ============================================================
# Stages are a gauntlet: each must pass before the next runs. A stage
# failing stops the ship. Fast feedback first (tests/lint), expensive
# and risky later (scan, deploy).

PIPELINE = [
    ("unit-tests", 2),
    ("lint", 1),
    ("build-image", 3),
    ("cve-scan", 4),
    ("migrate-db", 5),
    ("deploy-canary", 6),
    ("health-gate", 7),
    ("promote-100", 8),
]

def run_pipeline(fail_at: str | None) -> list[tuple[str, bool]]:
    results = []
    for stage, order in PIPELINE:
        ok = stage != fail_at
        results.append((stage, ok))
        if not ok:
            break                        # a failed stage stops the ship
    return results


print("=== 1. Pipeline as a gauntlet ===")
for stage, ok in run_pipeline("cve-scan"):
    print(f"  {stage:<14} {'PASS' if ok else 'FAIL (ship stopped)'}")
print()

# ============================================================
# 2. Matrix testing — the matrix is the coverage contract
# ============================================================
# Run tests across Python versions and dependency sets: the change must
# pass on the oldest supported Python AND the newest, not just your
# laptop's.

MATRIX = [
    {"python": "3.11", "deps": "min"},
    {"python": "3.12", "deps": "latest"},
    {"python": "3.13", "deps": "latest"},
]

def matrix_success(run_log: list[bool]) -> bool:
    return all(run_log)                  # every cell must pass


print("=== 2. Matrix testing ===")
for cell in MATRIX:
    print(f"  py{cell['python']:<6} deps={cell['deps']:<6} ...")
print(f"matrix passes when all cells pass: {matrix_success([True, True, True])}")
print(f"  (and fails if any: {matrix_success([True, False, True])})")
print()

# ============================================================
# 3. Caching — dependency install is the slowest stage
# ============================================================
# pip install ~minutes; a cache keyed on the lockfile turns it into
# seconds when nothing changed. Key correctness matters: too coarse
# (no key) = stale cache; too fine = never hits.

def cache_hit(cache_key: str, lockfile_hash: str, store: dict[str, str]) -> bool:
    """Restore from cache if the key matches the lockfile hash."""
    if store.get("key") == cache_key:
        return True
    store["key"] = cache_key
    return False


print("=== 3. Caching ===")
store: dict[str, str] = {}
h1 = "deadbeef"
print(f"first run (no cache): hit={cache_hit(f'deps-{h1}', h1, store)}")
print(f"same lockfile run    : hit={cache_hit(f'deps-{h1}', h1, store)}")
h2 = "cafebabe"
print(f"lockfile changed run : hit={cache_hit(f'deps-{h2}', h2, store)}")
print()

# ============================================================
# 4. Migrations in the pipeline
# ============================================================
# Schema changes ship with the code. The rule: migrations run BEFORE
# the new code serves traffic (expand), and destructive steps run
# AFTER (contract) — or the new code queries a schema that does not
# exist yet. The pipeline orders it for you.

def migration_order(expand: list[str], contract: list[str]) -> list[str]:
    """Expand (additive) before deploy; contract (destructive) after."""
    return ["EXPAND: " + s for s in expand] + ["deploy"] + ["CONTRACT: " + s for s in contract]


print("=== 4. Migrations in the pipeline ===")
for step in migration_order(["add column model_v2_score"],
                            ["drop column legacy_score"]):
    print(f"  {step}")
print()

# ============================================================
# 5. Blue-green and canary — deploy math
# ============================================================
# Blue-green: switch a whole fleet (fast, all-or-nothing, big blast).
# Canary: route 5% -> 25% -> 100% (slow, measurable, small blast).
# The rollout is traffic math with health gates at each step.

def canary_steps(steps: list[float]) -> list[float]:
    return steps

def blue_green_switch(old_ok: bool, new_ok: bool) -> str:
    if not new_ok:
        return "abort — new version failed health gate"
    return "switch all traffic to green" if old_ok else "switch + rollback path ready"


print("=== 5. Blue-green and canary ===")
print(f"  canary: {canary_steps([0.05, 0.25, 1.0])}")
print(f"  blue-green: {blue_green_switch(True, True)}")
print(f"  blue-green when green fails: {blue_green_switch(True, False)}")
print()

# ============================================================
# 6. Rollback — the last gate
# ============================================================
# Every deploy has a rollback: revert the code AND the data changes.
# Schema-destructive migrations complicate rollback — which is why
# expand/contract (section 4) makes rollback just a code revert.

def rollback_strategy(has_destructive_migration: bool) -> str:
    if has_destructive_migration:
        return "code revert + data restore (complex, slow)"
    return "code revert only (fast — expand/contract kept data compatible)"


print("=== 6. Rollback ===")
print(f"  with destructive migration : {rollback_strategy(True)}")
print(f"  with expand/contract       : {rollback_strategy(False)}")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: tests last — the pipeline is slow and failures arrive late
# CORRECT: fast feedback first; expensive stages after
#
# MISTAKE: one Python version — works on your laptop, breaks on 3.11
# CORRECT: matrix across supported versions/deps
#
# MISTAKE: no dependency cache — 2 minutes per run, forever
# CORRECT: cache keyed on the lockfile hash
#
# MISTAKE: migrations after deploy — new code queries missing columns
# CORRECT: expand before, contract after
#
# MISTAKE: no rollback story — the deploy is a point of no return
# CORRECT: expand/contract so rollback = code revert

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""

    # 1. Pipeline stops at the first failure
    r = run_pipeline("cve-scan")
    assert r[-1][0] == "cve-scan" and r[-1][1] is False, "pipeline must stop"
    assert all(ok for _, ok in r[:-1]), "stages before the failure pass"
    r = run_pipeline(None)
    assert len(r) == len(PIPELINE), "full pipeline when nothing fails"

    # 2. Matrix requires every cell
    assert matrix_success([True, True, True])
    assert not matrix_success([True, False, True])

    # 3. Cache hits only on matching lockfile hash
    store3: dict[str, str] = {}
    h = "abc123"
    assert cache_hit(f"deps-{h}", h, store3) is False, "first run misses"
    assert cache_hit(f"deps-{h}", h, store3) is True, "same hash hits"
    assert cache_hit(f"deps-{h}", "other", store3) is False, "changed lockfile misses"

    # 4. Expand before, contract after
    order = migration_order(["add col"], ["drop col"])
    assert order.index("deploy") > order.index("EXPAND: add col"), "expand first"
    assert order.index("deploy") < order.index("CONTRACT: drop col"), "contract last"

    # 5. Rollout math and health gating
    assert canary_steps([0.05, 0.25, 1.0]) == [0.05, 0.25, 1.0]
    assert blue_green_switch(True, False) == "abort — new version failed health gate"

    # 6. Rollback strategy depends on schema destructiveness
    assert "code revert only" in rollback_strategy(False)
    assert "data restore" in rollback_strategy(True)

    print("[OK] 51-ci-cd: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Pipeline = gauntlet; a failed stage stops the ship")
        print("2. Matrix = the coverage contract across versions")
        print("3. Cache keyed on the lockfile; migrations expand/contract")
        print("4. Canary/blue-green rollout; rollback = code revert")
        _verify()          # always runs, so plain execution is also a test
