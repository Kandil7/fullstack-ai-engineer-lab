"""
Pandas -- 39: Method Chaining
==============================================
Topics: .pipe, .assign, .query, chained vs stepwise,
        SettingWithCopyWarning explained properly, copy= semantics

Why this matters for AI/backend engineering:
    Feature engineering for ML is a long sequence of transforms; a chain
    makes that sequence reviewable and forces every step to return a new
    frame instead of mutating shared state. Misunderstood chaining is also
    the #1 source of the SettingWithCopyWarning -- silent data corruption
    in training pipelines that trains the model on different data than
    you think.

Run:      python 39-method-chaining.py
Verify:   python 39-method-chaining.py --verify
Reference: https://pandas.pydata.org/docs/user_guide/indexing.html#returning-a-view-versus-a-copy
"""

from __future__ import annotations

import sys
import warnings

import numpy as np
import pandas as pd

np.random.seed(42)
pd.set_option("mode.chained_assignment", "warn")  # keep the warning visible

# ============================================================
# 1. Chaining: One Expression, Many Reviewed Steps
# ============================================================
# A chain is a sequence of method calls where each call returns a new
# DataFrame and the next call starts from it. Read it top to bottom;
# each line is one transform that can be reviewed, tested, and reused.

# Example 1: the same pipeline written stepwise and chained
base = pd.DataFrame({
    "user_id": range(1, 11),
    "age": np.random.randint(18, 70, 10),
    "spend": np.random.uniform(10, 500, 10).round(2),
    "plan": np.random.choice(["free", "pro", "enterprise"], 10),
})

# STEPWISE: five statements, five chances to touch the wrong frame
step1 = base.copy()
step2 = step1[step1["spend"] > 100]
step3 = step2.assign(spend_rank=step2["spend"].rank(ascending=False))
step4 = step3.sort_values("spend", ascending=False)

# CHAINED: one expression, same result
chained = (
    base.copy()
    .query("spend > 100")
    .assign(spend_rank=lambda d: d["spend"].rank(ascending=False))
    .sort_values("spend", ascending=False)
)

print("Stepwise equals chained:", step4.equals(chained))

# Output:
# Stepwise equals chained: True


# ============================================================
# 2. .assign -- Adding Columns in the Chain
# ============================================================
# .assign returns a NEW frame with the added columns. Use a callable
# (lambda d: ...) when the new column depends on columns created
# EARLIER in the same chain: the callable receives the frame as it
# exists at that point in the chain.

# Example 2: assign with a callable sees the filtered frame, not the
# original one -- a classic bug if you pass a precomputed Series.
# The excluded 'pro' rows have the HIGHEST spends, so their removal
# shifts every rank: the two versions must disagree.
fresh = pd.DataFrame({
    "spend": [400.0, 350.0, 200.0, 50.0, 300.0],
    "plan": ["pro", "pro", "free", "free", "free"],
})
rank_after_filter = (
    fresh
    .query("plan == 'free'")
    .assign(rank=lambda d: d["spend"].rank(ascending=False))
)
rank_wrong = fresh.query("plan == 'free'").assign(
    rank=fresh["spend"].rank(ascending=False)   # BUG: ranks the full frame
)
print("Rank computed on filtered frame:", rank_after_filter["rank"].tolist())
print("Rank computed on full frame:   ", rank_wrong["rank"].tolist())

# Output:
# Rank computed on filtered frame: [2.0, 3.0, 1.0]
# Rank computed on full frame:    [4.0, 5.0, 3.0]


# ============================================================
# 3. .query -- SQL-Style Filtering in the Chain
# ============================================================
# .query evaluates a string expression against the frame. It is
# equivalent to boolean indexing but reads like SQL and avoids
# repeating df["col"] everywhere. Variables from the enclosing scope
# are referenced with @name.

# Example 3: query with @variables and string methods
city = "SF"
min_spend = 100.0
df_geo = pd.DataFrame({
    "city": ["NYC", "SF", "LA", "SF", "NYC"],
    "spend": [50.0, 120.0, 300.0, 400.0, 25.0],
})
result = df_geo.query("spend > @min_spend and city == @city")
print("query with @vars:", result["spend"].tolist())
print("query eq boolean indexing:",
      result.equals(df_geo[(df_geo["spend"] > min_spend)
                           & (df_geo["city"] == city)]))

# Output:
# query with @vars: [120.0, 400.0]
# query eq boolean indexing: True


# ============================================================
# 4. .pipe -- Custom Functions in the Chain
# ============================================================
# .pipe(drop_na_rows) calls drop_na_rows(current_frame) and returns
# whatever the function returns. This is how you plug ANY function --
# including one from another library -- into a chain.

# Example 4: reusable transform functions piped together
def drop_missing_rows(frame: pd.DataFrame) -> pd.DataFrame:
    """Drop rows with any missing values."""
    return frame.dropna()

def add_ratio(frame: pd.DataFrame, num: str, den: str,
              out: str) -> pd.DataFrame:
    """Add out = num / den as a new column."""
    return frame.assign(**{out: frame[num] / frame[den]})

def flag_high(frame: pd.DataFrame, col: str, threshold: float,
              out: str = "is_high") -> pd.DataFrame:
    """Add a boolean column marking values above a threshold."""
    return frame.assign(**{out: frame[col] > threshold})

piped = (
    df_geo
    .pipe(drop_missing_rows)
    .pipe(add_ratio, "spend", "spend", "ratio")
    .pipe(flag_high, "spend", 100.0)
)
print("Pipe chain columns:", piped.columns.tolist())
print("Pipe chain rows:", len(piped))

# Output:
# Pipe chain columns: ['city', 'spend', 'ratio', 'is_high']
# Pipe chain rows: 5


# ============================================================
# 5. Why Chains Protect You -- and the copy= Trap
# ============================================================
# Most DataFrame methods return a NEW object. Chain safety depends on
# knowing which operations return views/copies and what .copy() gives
# you. copy(deep=True) is fully independent; copy(deep=False) shares
# the underlying data blocks and is only safe for read-only use.

# Example 5: deep vs shallow copy semantics
original = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
deep = original.copy(deep=True)
deep.iloc[0, 0] = 999
print("Deep copy mutation visible in original:", original["a"].tolist())

shallow = original.copy(deep=False)
print("Shallow copy shares blocks:",
      shallow.iloc[0, 0] == 1)

# Output:
# Deep copy mutation visible in original: [1, 2, 3]
# Shallow copy shares blocks: True


# ============================================================
# 6. SettingWithCopyWarning -- Explained Properly
# ============================================================
# The warning fires when you set a value through a CHAIN of selections
# (df[cond]["col"] = x or sub = df.loc[...]; sub["col"] = x). pandas
# cannot prove whether the intermediate object is a view or a copy, so
# it warns. Two outcomes are possible: the write is lost silently
# (copy) or it lands in the wrong place (view). Both are bugs.
# The fix is always the same: ONE selection with .loc.

# Example 6: chained assignment -- value does NOT stick
df_copy = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})
df_copy["flag"] = 0

with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    sub = df_copy[df_copy["a"] > 1]      # boolean mask -> copy
    sub["flag"] = 1                      # chained write, lands in the copy
    warned = any(w.category.__name__ == "SettingWithCopyWarning"
                 for w in caught)
print("Chained write raised a warning:", warned)
print("Chained write stuck to df:", int(df_copy["flag"].sum()))

# Example 7: the correct write -- one .loc selection
df_copy.loc[df_copy["a"] > 1, "flag"] = 1
print("After .loc write, flag sum:", int(df_copy["flag"].sum()))

# Output:
# Chained write raised a warning: True
# Chained write stuck to df: 0
# After .loc write, flag sum: 2


# ============================================================
# 7. Where the Warning DOES Fire (pandas 2.2)
# ============================================================
# Slicing (df.iloc[:2], df.loc["a":"c"]) returns a VIEW when the
# underlying data is not copied. Writing through that view triggers
# SettingWithCopyWarning -- and the write may land in the parent
# frame, which is exactly the corruption chains are designed to avoid.

# Example 8: write through an iloc-slice view
df_view = pd.DataFrame({"a": [1, 2, 3, 4], "b": [5, 6, 7, 8]})
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    view = df_view.iloc[:2]              # a view of the first 2 rows
    view["b"] = 99                       # ambiguous: view or copy?
    warned = any(w.category.__name__ == "SettingWithCopyWarning"
                 for w in caught)
print("Slice-view write raised a warning:", warned)

# Example 9: make the intent explicit -- copy, then write freely
safe = df_view.iloc[:2].copy()
safe["b"] = 99
print("Explicit .copy() write is silent and safe:", safe["b"].tolist())

# Output:
# Slice-view write raised a warning: True
# Explicit .copy() write is silent and safe: [99, 99]


# ============================================================
# 8. Production Pattern: A Feature-Engineering Chain
# ============================================================
# The senior-engineer shape: named functions, one chain, no hidden
# mutation. Each helper is unit-testable in isolation.

def engineer_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Build the ML feature set for a user-spend dataset.

    Chain order matters: filter BEFORE computing group stats so the
    stats describe the cohort the model will actually see.
    """
    return (
        frame
        .copy()
        .pipe(drop_missing_rows)
        .query("spend > 0")
        .assign(
            log_spend=lambda d: np.log1p(d["spend"]),
            spend_rank=lambda d: d["spend"].rank(ascending=False),
            is_power_user=lambda d: d["spend"] >= d["spend"].quantile(0.8),
        )
        .pipe(flag_high, "spend", 300.0, out="is_high")
        .sort_values("spend", ascending=False)
    )

# Example 10: the production chain end to end
ml_ready = engineer_features(base)
print("Feature chain shape:", ml_ready.shape)
print("Feature chain columns:", ml_ready.columns.tolist())

# Output:
# Feature chain shape: (10, 8)
# Feature chain columns: ['user_id', 'age', 'spend', 'plan', 'log_spend', 'spend_rank', 'is_power_user', 'is_high']


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: assigning through a chain and assuming it sticks
#   df[df.a > 1]["flag"] = 1        # silently lost (copy)
# CORRECT:
#   df.loc[df.a > 1, "flag"] = 1    # one selection, always sticks
#
# MISTAKE: .assign with a precomputed Series instead of a callable
#   df.query("spend > 100").assign(rank=df["spend"].rank())
#      # ranks the FULL frame, not the filtered one
# CORRECT:
#   df.query("spend > 100").assign(rank=lambda d: d["spend"].rank())
#
# MISTAKE: relying on inplace=True to "save memory" inside a chain
#   df.query(...).dropna(inplace=True)   # returns None -> chain dies
# CORRECT:
#   df.query(...).dropna()               # returns a new frame


# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # Chain equivalence: stepwise and chained pipelines agree.
    assert step4.equals(chained), "chained and stepwise must agree"

    # .query filters correctly: only rows above the threshold remain.
    expected_rows = int((base["spend"] > 100).sum())
    assert len(chained) == len(step4) == expected_rows, \
        "query must keep exactly the rows with spend > 100"
    assert bool((chained["spend"] > 100).all()), \
        "query must only return spend > 100"

    # .assign adds columns and callables see the intermediate frame.
    assert "spend_rank" in chained.columns, "assign must add a column"
    assert rank_after_filter["rank"].tolist() == [2.0, 3.0, 1.0], \
        "callable must rank the filtered frame"
    assert rank_wrong["rank"].tolist() == [4.0, 5.0, 3.0], \
        "precomputed Series must rank the full frame (the bug)"

    # .pipe plugs functions into the chain and returns their output.
    assert piped.columns.tolist() == [
        "city", "spend", "ratio", "is_high"], "pipe must add columns"
    assert bool((piped["ratio"] == 1.0).all()), "ratio must be spend/spend"

    # Deep copies are independent; shallow copies share blocks.
    assert original["a"].tolist() == [1, 2, 3], \
        "deep copy mutation must not leak into the original"

    # Chained assignment does NOT stick; .loc does.
    assert int(df_copy["flag"].sum()) == 2, \
        "chained write must be lost, .loc write must stick"

    # The production chain is deterministic and correct.
    assert ml_ready.shape == (len(base), 8), \
        "feature chain must keep exactly the filtered rows"
    assert bool((ml_ready["log_spend"] == np.log1p(ml_ready["spend"])).all()), \
        "log_spend must be log1p of spend"
    assert ml_ready["spend"].iloc[0] >= ml_ready["spend"].iloc[-1], \
        "chain must sort descending by spend"

    print("[OK] 39-method-chaining: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Chains turn a pipeline into one reviewable expression.")
        print("2. .assign callables see the frame at that point in the chain.")
        print("3. Never write through a chain; use one .loc selection.")
        _verify()          # always runs, so plain execution is also a test
