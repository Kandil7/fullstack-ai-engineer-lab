"""
MLOps - 10: Data Validation
===========================
Topics: schema contracts, distribution checks, and "fail the pipeline,
not the model". A lightweight validator teaches the same contracts as
Pandera/Great Expectations.

Why this matters for AI/backend engineering:
    Garbage in, garbage out - but the garbage usually arrives as a
    schema change or a distribution shift that nobody noticed. Validating
    data BEFORE training (fail the pipeline) beats discovering it after
    the model shipped.

Run:      python 10-data-validation.py
Verify:   python 10-data-validation.py --verify
Reference: https://pandera.readthedocs.io/
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Any, Callable


# ============================================================
# 1. Schema Contracts
# ============================================================
# A contract states what a column MUST be: type, non-null, range.
# Violations are caught at the boundary, not 20 steps downstream.

@dataclass
class ColumnRule:
    name: str
    dtype: type = float
    nullable: bool = False
    min_value: float | None = None
    max_value: float | None = None

    def validate(self, values: list[Any]) -> list[str]:
        errors: list[str] = []
        for i, v in enumerate(values):
            if v is None:
                if not self.nullable:
                    errors.append(f"{self.name}[{i}] is null but not nullable")
                continue
            if not isinstance(v, self.dtype):
                # allow int for float columns
                if not (self.dtype is float and isinstance(v, (int, float))):
                    errors.append(f"{self.name}[{i}] has type {type(v).__name__}, "
                                  f"expected {self.dtype.__name__}")
            if isinstance(v, (int, float)):
                if self.min_value is not None and v < self.min_value:
                    errors.append(f"{self.name}[{i}]={v} < min {self.min_value}")
                if self.max_value is not None and v > self.max_value:
                    errors.append(f"{self.name}[{i}]={v} > max {self.max_value}")
        return errors


# Example 1: validate a column
age_rule = ColumnRule("age", dtype=int, min_value=0, max_value=120)
errors = age_rule.validate([25, None, -5, 200])
print("Example 1: column rule violations")
for e in errors:
    print(f"  {e}")
assert any("-5 < min 0" in e for e in errors), "negative age flagged"
assert any("> max 120" in e for e in errors), "200 age flagged"

# ============================================================
# 2. Whole-DataFrame Validation
# ============================================================

@dataclass
class DataContract:
    rules: list[ColumnRule] = field(default_factory=list)

    def validate(self, data: dict[str, list[Any]]) -> list[str]:
        errors: list[str] = []
        for rule in self.rules:
            if rule.name not in data:
                errors.append(f"missing column: {rule.name}")
                continue
            errors.extend(rule.validate(data[rule.name]))
        return errors

    def is_valid(self, data: dict[str, list[Any]]) -> bool:
        return not self.validate(data)


# Example 2: full contract
contract = DataContract([
    ColumnRule("age", dtype=int, min_value=0, max_value=120),
    ColumnRule("income", dtype=float, min_value=0.0),
])
valid_data = {"age": [30, 41, 22], "income": [50000.0, 80000.0, 30000.0]}
bad_data = {"age": [30, -1, 22], "income": [50000.0, None, -5.0]}
print("\nExample 2: contract validation")
print(f"  valid: {contract.is_valid(valid_data)}")
print(f"  bad:   {contract.is_valid(bad_data)}")
assert contract.is_valid(valid_data)
assert not contract.is_valid(bad_data)

# ============================================================
# 3. Distribution Checks
# ============================================================
# Schema catches types; distribution checks catch shifts. A sudden jump
# in the mean or null-rate is the first warning a source broke.

@dataclass
class DistributionBaseline:
    mean: float
    std: float
    null_rate: float
    tolerance_std: float = 3.0

    def check(self, values: list[Any]) -> list[str]:
        numeric = [v for v in values if isinstance(v, (int, float))]
        nulls = sum(1 for v in values if v is None)
        errors = []
        if numeric:
            mean = sum(numeric) / len(numeric)
            if abs(mean - self.mean) > self.tolerance_std * self.std:
                errors.append(f"mean {mean:.2f} drifted > "
                              f"{self.tolerance_std} std from {self.mean:.2f}")
        null_rate = nulls / len(values) if values else 0.0
        if null_rate > self.null_rate * 2 + 0.01:
            errors.append(f"null rate {null_rate:.2%} exceeds baseline")
        return errors


# Example 3: detect drift
baseline = DistributionBaseline(mean=50.0, std=5.0, null_rate=0.01)
stable = [49.0, 52.0, 48.0, 51.0, 50.0]
drifted = [80.0, 85.0, 78.0, 82.0, 79.0]
print("\nExample 3: distribution drift")
print(f"  stable data errors: {baseline.check(stable)}")
print(f"  drifted data errors: {baseline.check(drifted)}")
assert not baseline.check(stable), "stable data passes"
assert baseline.check(drifted), "drifted mean flagged"

# ============================================================
# Production Pattern
# ============================================================
# Validate at the pipeline boundary and FAIL FAST with a clear message.

def validate_or_fail(contract: DataContract, data: dict[str, list[Any]]) -> None:
    errors = contract.validate(data)
    if errors:
        raise ValueError(
            f"Data validation failed ({len(errors)} errors). "
            f"First 5: {errors[:5]}"
        )


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: validating on train only - the serving path needs the same gate
# MISTAKE: dropping invalid rows silently instead of failing loudly
# MISTAKE: thresholds too tight -> constant false alarms (alert fatigue)


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    r = ColumnRule("x", dtype=int, min_value=0, max_value=10)
    assert not r.validate([1, 2, 3]), "clean column"
    assert r.validate([-1]) and r.validate([11]), "range enforced"
    assert any("null" in e for e in r.validate([None])), "null checked"

    c = DataContract([ColumnRule("a", dtype=int), ColumnRule("b", dtype=float)])
    assert c.is_valid({"a": [1], "b": [2.0]})
    assert not c.is_valid({"a": [1]}), "missing column flagged"
    assert not c.is_valid({"a": ["x"], "b": [1.0]}), "wrong type flagged"

    base = DistributionBaseline(10.0, 1.0, 0.0)
    assert not base.check([10.0, 10.5, 9.5]), "within tolerance"
    assert base.check([100.0]), "massive drift flagged"

    try:
        validate_or_fail(c, {"a": ["x"], "b": [1.0]})
        raised = False
    except ValueError:
        raised = True
    assert raised, "validate_or_fail must raise on violation"
    print("[OK] 10-data-validation: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Contracts catch type/range/null violations at the boundary.")
        print("2. Distribution checks catch shifts schema checks cannot.")
        print("3. Fail the pipeline early - never train on bad data.")
        _verify()
