"""
Pandas -- 42: GroupBy Internals
==============================================
Topics: split-apply-combine mechanics, agg vs transform vs filter vs
        apply, named aggregation, multiple functions, performance
        ordering (apply is the slow path)

Why this matters for AI/backend engineering:
    groupby is the workhorse of feature engineering and reporting.
    The difference between a correct and a broken groupby is rarely
    syntax -- it is knowing WHICH verb does WHICH job: agg shrinks,
    transform preserves, filter selects groups, apply is the
    escape hatch you pay for. Get this wrong and your "user
    lifetime value" features silently double-count.

Run:      python 42-groupby-internals.py
Verify:   python 42-groupby-internals.py --verify
Reference: https://pandas.pydata.org/docs/user_guide/groupby.html
"""

from __future__ import annotations

import sys

import numpy as np
import pandas as pd

np.random.seed(42)

# ============================================================
# 1. Split-Apply-Combine, Step by Step
# ============================================================
# groupby(key)[col].op() is three phases: SPLIT the frame into
# sub-frames by key, APPLY the operation to each sub-frame, COMBINE
# the results back into one object.

# Example 1: manual split-apply-combine reproduces groupby exactly
df = pd.DataFrame({
    "team": ["a", "b", "a", "c", "b", "a"],
    "score": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0],
})

# Manual: split by key, apply mean, combine into a Series
manual = {}
for key, sub in df.groupby("team"):
    manual[key] = sub["score"].mean()
manual_result = pd.Series(manual).sort_index()

native = df.groupby("team")["score"].mean()
print("Manual split-apply-combine:")
print(manual_result.round(2).tolist(), "| native:", native.round(2).tolist())
print("Identical:", manual_result.equals(native))

# Output:
# Manual split-apply-combine:
# [33.33, 35.0, 40.0] | native: [33.33, 35.0, 40.0]
# Identical: True


# ============================================================
# 2. agg -- Many Functions, One Pass
# ============================================================
# agg() applies one or more functions per column and returns a
# SMALLER frame: one row per group. Mix built-in names ("mean",
# "sum"), callables (np.median), and per-column dictionaries.

# Example 2: multiple aggregations, list and dict forms
stats = df.groupby("team").agg(["mean", "max"])
print("Multi-func agg columns:", stats.columns.tolist())

by_col = df.groupby("team").agg(avg=("score", "mean"),
                                peak=("score", "max"),
                                count=("score", "count"))
print("Named agg:")
print(by_col.round(2).to_dict("index"))

# Output:
# Multi-func agg columns: [('score', 'mean'), ('score', 'max')]
# Named agg:
# {'a': {'avg': 33.33, 'peak': 60.0, 'count': 3}, 'b': {'avg': 35.0, 'peak': 50.0, 'count': 2}, 'c': {'avg': 40.0, 'peak': 40.0, 'count': 1}}


# ============================================================
# 3. transform -- Same Shape, Group-Wise Values
# ============================================================
# transform() returns a frame with the SAME number of rows: each row
# gets its group's statistic. It is how you compute "score minus the
# team average" or "share of team total" -- both classic features.

# Example 3: transform keeps the index and length
df["team_mean"] = df.groupby("team")["score"].transform("mean")
df["score_delta"] = df["score"] - df["team_mean"]
df["team_share"] = df["score"] / df.groupby("team")["score"].transform("sum")
print(df.round(3).to_string(index=False))

# Output:
# team  score  team_mean  score_delta  team_share
#    a   10.0      33.333      -23.333        0.100
#    b   20.0      35.000      -15.000        0.286
#    a   30.0      33.333       -3.333        0.300
#    c   40.0      40.000        0.000        1.000
#    b   50.0      35.000       15.000        0.714
#    a   60.0      33.333       26.667        0.600


# ============================================================
# 4. filter -- Keep Whole Groups
# ============================================================
# filter(predicate) keeps entire groups whose predicate is True.
# Rows are dropped only in whole-group chunks -- you never partially
# filter inside a group with this verb.

# Example 4: keep teams with at least 2 observations
big_teams = df.groupby("team").filter(lambda g: len(g) >= 2)
print("Teams with >= 2 rows:", sorted(big_teams["team"].unique().tolist()))
print("Rows kept:", len(big_teams))

# Output:
# Teams with >= 2 rows: ['a', 'b']
# Rows kept: 5


# ============================================================
# 5. apply -- The Flexible Slow Path
# ============================================================
# apply(func) passes each group's DataFrame to func. It is the most
# flexible and the SLOWEST: pandas cannot vectorize arbitrary Python
# functions, so apply pays per-group Python overhead. Rule of thumb:
# prefer agg/transform; use apply only when the result shape cannot
# be expressed otherwise.

# Example 5: apply returning a scalar per group
first_last = df.groupby("team")["score"].apply(
    lambda g: g.iloc[0] - g.iloc[-1])
print("First - last per team:", first_last.round(2).tolist())

# Output:
# First - last per team: [-50.0, -30.0, 0.0]


# ============================================================
# 6. The Performance Ordering
# ============================================================
# For the same task, the fast path is built-in agg > transform >
# filter > apply. The numbers below are order-of-magnitude guidance,
# not a benchmark: the lesson is that apply on 100k groups means
# 100k Python calls.

# Example 6: same computation, three spellings -- verify equal results
n = 20_000
big = pd.DataFrame({
    "key": np.random.randint(0, 1000, n),
    "val": np.random.randn(n),
})

agg_mean = big.groupby("key")["val"].mean()
apply_mean = big.groupby("key")["val"].apply(lambda g: g.mean())

# transform returns one value PER ROW: take the first row of each key
# so every spelling ends up keyed the same way.
transform_first = (
    big
    .assign(m=big.groupby("key")["val"].transform("mean"))
    .drop_duplicates("key")[["key", "m"]]
    .set_index("key")["m"]
    .sort_index()
)
agg_sorted = agg_mean.sort_index()
apply_sorted = apply_mean.sort_index().reset_index(drop=True)

print("agg == transform:", np.allclose(agg_sorted.values, transform_first.values))
print("agg == apply:", np.allclose(agg_sorted.values, apply_sorted.values))

# Output:
# agg == transform: True
# agg == apply: True


# ============================================================
# 7. Grouping by Multiple Keys
# ============================================================
# Pass a LIST to groupby to form composite keys; the result has a
# MultiIndex. Unstack (or pivot_table) turns one grouping level into
# columns -- the classic "cohort x month" matrix.

# Example 7: two-key grouping and reshaping
sales = pd.DataFrame({
    "month": np.repeat(["Jan", "Feb", "Mar"], 4),
    "city": np.tile(["NY", "SF", "NY", "SF"], 3),
    "amount": np.random.uniform(10, 100, 12).round(1),
})
cohort = sales.groupby(["month", "city"])["amount"].sum()
print("Multi-key index:", cohort.index.names)
matrix = cohort.unstack()
print("Cohort matrix:")
print(matrix.round(1).to_string())

# Output:
# Multi-key index: ['month', 'city']
# Cohort matrix:
# city      NY    SF
# month
# Feb     95.2  98.3
# Jan    166.0  96.8
# Mar     98.9  49.9


# ============================================================
# 8. Production Pattern: Feature Table from Group Statistics
# ============================================================
# The senior pattern: ONE groupby pass producing all group-level
# features via named agg, then merge back onto the base frame with
# transform-style alignment -- but explicit, reviewable, and fast.

def group_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Per-user summary features, one row per user."""
    return (
        frame
        .groupby("user_id")
        .agg(
            total_spend=("amount", "sum"),
            avg_spend=("amount", "mean"),
            order_count=("amount", "count"),
            max_spend=("amount", "max"),
        )
        .reset_index()
    )

# Example 8: users with orders, then join features back
orders = pd.DataFrame({
    "user_id": np.repeat([1, 2, 3], [3, 2, 1]),
    "amount": [50.0, 30.0, 20.0, 90.0, 10.0, 15.0],
    "status": ["paid", "paid", "refunded", "paid", "paid", "paid"],
})
features = group_features(orders)
print("User features:")
print(features.round(2).to_string(index=False))

# Output:
# User features:
#    user_id  total_spend  avg_spend  order_count  max_spend
#          1        100.0       33.33            3       50.0
#          2        100.0       50.00            2       90.0
#          3         15.0       15.00            1       15.0


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: using apply() when agg() suffices
#   df.groupby("k")["v"].apply(lambda g: g.mean())   # slow path
# CORRECT:
#   df.groupby("k")["v"].mean()                      # C-optimized
#
# MISTAKE: transform when you meant agg (or vice versa)
#   gb.transform("mean")  # same length as input -- if you wanted
#                         # one row per group, this is a shape bug
# CORRECT: decide by OUTPUT SHAPE: agg shrinks, transform preserves.
#
# MISTAKE: assuming groupby sorts the keys
#   df.groupby("k").mean()      # sorted keys by default
#   df.groupby("k", sort=False) # preserves first-appearance order
# CORRECT: if order matters, pass sort=False explicitly.
#
# MISTAKE: forgetting NaN handling
#   .sum() skips NaN but .count() counts non-NaN -- "missing order"
#   rows can silently vanish from aggregations.


# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # Manual split-apply-combine equals the native groupby.
    assert manual_result.equals(native), \
        "manual split-apply-combine must match groupby"

    # Named agg produces the expected columns and values.
    assert by_col.columns.tolist() == ["avg", "peak", "count"], \
        "named agg must produce the requested column names"
    assert by_col.loc["a", "avg"] == 33.333333333333336, \
        "team a mean must be (10+30+60)/3"
    assert by_col.loc["a", "count"] == 3, "team a has 3 rows"
    assert by_col.loc["b", "peak"] == 50.0, "team b max must be 50"

    # transform preserves the input length and computes group means.
    assert len(df) == 6, "transform must not change row count"
    assert df["team_mean"].tolist()[0] == 33.333333333333336, \
        "team_mean must be the group mean"
    assert np.isclose(df["team_share"].sum(), 3.0), \
        "each team's shares must sum to 1.0 (three teams -> 3.0)"

    # filter keeps whole groups only.
    assert sorted(big_teams["team"].unique().tolist()) == ["a", "b"], \
        "filter must drop team c entirely"

    # apply produces the per-group first-minus-last.
    assert first_last.sort_index().tolist() == [-50.0, -30.0, 0.0], \
        "apply must compute first - last per group"

    # agg, transform, and apply agree on the same computation.
    assert np.allclose(agg_sorted.values, transform_first.values), \
        "agg and transform must agree"
    assert np.allclose(agg_sorted.values, apply_sorted.values), \
        "agg and apply must agree"

    # Multi-key grouping produces a valid cohort matrix.
    assert cohort.index.names == ["month", "city"], \
        "two-key groupby must produce a MultiIndex"
    assert matrix.shape == (3, 2), "cohort matrix must be 3 months x 2 cities"

    # Production pattern: one row per user, correct totals.
    assert features["total_spend"].tolist() == [100.0, 100.0, 15.0], \
        "user totals must be [100, 100, 15]"
    assert features["order_count"].tolist() == [3, 2, 1], \
        "order counts must be [3, 2, 1]"

    print("[OK] 42-groupby-internals: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. agg shrinks, transform preserves, filter drops groups.")
        print("2. apply is the flexible slow path -- last resort.")
        print("3. Named agg makes group features reviewable.")
        _verify()          # always runs, so plain execution is also a test
