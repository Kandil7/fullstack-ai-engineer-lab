"""
MLOps - 12: CI/CD for ML
========================
Topics: testing ML code, behavioral tests for models, training in CI,
model approval gates, deployment automation.

Why this matters for AI/backend engineering:
    A model is code plus data plus expectations. CI for ML must test all
    three: unit tests on the code, behavioral tests on the model (does it
    refuse OOD input? is it stable?), and gate checks before promotion.

Run:      python 12-ci-cd-for-ml.py
Verify:   python 12-ci-cd-for-ml.py --verify
Reference: https://scikit-learn.org/stable/modules/model_persistence.html
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Any, Callable


# ============================================================
# 1. Three Kinds of ML Tests
# ============================================================
# (a) code tests - does the pipeline run?
# (b) data tests - is the input sane?
# (c) behavioral tests - does the MODEL behave on known cases?

@dataclass
class TestResult:
    name: str
    passed: bool
    detail: str = ""


def run_test(name: str, fn: Callable[[], bool]) -> TestResult:
    try:
        return TestResult(name, bool(fn()))
    except Exception as e:  # noqa: BLE001
        return TestResult(name, False, str(e))


# Example 1: behavioral tests for a simple rule model
def rule_model_predict(age: int, income: float) -> str:
    """A toy 'loan approve' rule model."""
    if age < 18 or income < 0:
        return "REJECT"  # refuses invalid input
    if income > 50000 and age >= 25:
        return "APPROVE"
    return "REJECT"


behavioral_tests = [
    ("rejects negative income", lambda: rule_model_predict(30, -5.0) == "REJECT"),
    ("rejects minors", lambda: rule_model_predict(16, 100000.0) == "REJECT"),
    ("approves solid applicant", lambda: rule_model_predict(30, 60000.0) == "APPROVE"),
    ("rejects thin applicant", lambda: rule_model_predict(30, 30000.0) == "REJECT"),
]
print("Example 1: behavioral tests")
for name, fn in behavioral_tests:
    r = run_test(name, fn)
    print(f"  [{'PASS' if r.passed else 'FAIL'}] {name}")
assert all(run_test(n, f).passed for n, f in behavioral_tests)

# ============================================================
# 2. The CI Gate
# ============================================================
# CI runs: unit tests -> data tests -> behavioral tests -> training ->
# registry promotion. Each stage can fail the build.

@dataclass
class CIGate:
    stages: list[tuple[str, Callable[[], bool]]] = field(default_factory=list)

    def run(self) -> tuple[bool, list[TestResult]]:
        results = [run_test(name, fn) for name, fn in self.stages]
        return all(r.passed for r in results), results


# Example 2: a failing stage stops the ship
gate = CIGate([
    ("unit: import ok", lambda: True),
    ("data: no nulls", lambda: True),
    ("behavioral: approves", lambda: rule_model_predict(30, 60000.0) == "APPROVE"),
    ("behavioral: rejects minor", lambda: rule_model_predict(16, 1e9) == "REJECT"),
])
ok, results = gate.run()
print("\nExample 2: CI gate")
for r in results:
    print(f"  [{'PASS' if r.passed else 'FAIL'}] {r.name}")
assert ok, "all stages pass"

# A model that suddenly approves everyone fails the gate:
bad_model_test = lambda: rule_model_predict(16, 1e9) == "REJECT"  # noqa: E731
print(f"  gate with a regressed model: {run_test('minor', bad_model_test).passed}")

# ============================================================
# 3. Golden Data Tests
# ============================================================
# Lock in known input->output pairs. If a change breaks a golden case,
# the build fails - regressions are caught before merge.

GOLDEN_CASES = [
    ({"age": 30, "income": 60000.0}, "APPROVE"),
    ({"age": 30, "income": 30000.0}, "REJECT"),
    ({"age": 16, "income": 60000.0}, "REJECT"),
]

def golden_test() -> bool:
    return all(rule_model_predict(**case) == expected
               for case, expected in GOLDEN_CASES)


print("\nExample 3: golden data tests")
print(f"  {len(GOLDEN_CASES)} golden cases pass: {golden_test()}")
assert golden_test()

# ============================================================
# 4. Approval Gates
# ============================================================
# Even green CI is not deployment: a human (or a policy) approves the
# promotion to production. CI proves "safe"; approval proves "wanted".

@dataclass
class ApprovalFlow:
    requires_review: bool = True
    reviewer: str | None = None

    def promote(self, reviewer: str | None = None) -> tuple[bool, str]:
        if self.requires_review and reviewer is None:
            return False, "blocked: model needs reviewer approval"
        self.reviewer = reviewer
        return True, f"approved by {reviewer}"


# Example 4: approval gate
flow = ApprovalFlow()
blocked, msg = flow.promote()
print("\nExample 4: approval gate")
print(f"  {msg}")
assert not blocked
ok, msg = flow.promote("alice")
print(f"  {msg}")
assert ok

# ============================================================
# Production Pattern
# ============================================================
def ci_entrypoint(tests: list[tuple[str, Callable[[], bool]]],
                  reviewer: str | None = None) -> int:
    """The CI entrypoint: run tests, then require approval."""
    gate = CIGate(tests)
    ok, results = gate.run()
    for r in results:
        print(f"  [{'PASS' if r.passed else 'FAIL'}] {r.name}")
    if not ok:
        return 1
    flow = ApprovalFlow()
    approved, msg = flow.promote(reviewer)
    print(f"  {msg}")
    return 0 if approved else 1


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: CI tests code but never the MODEL behavior
# MISTAKE: no golden cases - subtle regressions ship silently
# MISTAKE: auto-deploy on green tests with no approval for risky changes


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    # rule model invariants
    assert rule_model_predict(16, 1e9) == "REJECT", "minor always rejected"
    assert rule_model_predict(30, -1) == "REJECT", "negative income rejected"
    assert rule_model_predict(40, 100000.0) == "APPROVE"

    assert golden_test(), "golden cases must pass"

    g = CIGate([("t1", lambda: True), ("t2", lambda: False)])
    ok, results = g.run()
    assert not ok and len(results) == 2, "failing stage fails the gate"

    flow = ApprovalFlow(requires_review=True)
    assert not flow.promote()[0], "no reviewer -> blocked"
    assert flow.promote("bob")[0], "reviewer -> approved"
    auto = ApprovalFlow(requires_review=False)
    assert auto.promote()[0], "no review needed -> auto-approve"

    rc = ci_entrypoint([("ok", lambda: True)], reviewer=None)
    assert rc == 1, "CI without approval returns failure"
    rc2 = ci_entrypoint([("ok", lambda: True)], reviewer="ci-bot")
    assert rc2 == 0, "CI with approval returns success"
    print("[OK] 12-ci-cd-for-ml: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Test code, data, AND model behavior.")
        print("2. Golden cases lock in known input->output pairs.")
        print("3. Green CI proves safe; approval proves wanted.")
        _verify()
