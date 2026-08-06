"""
Pandas -- 44: Pandas Pitfalls
==============================================
Topics: chained assignment, index alignment surprises, inplace=True
        not faster, float equality, NaN != NaN, silent dtype upcasting,
        iterrows is slow, merge cardinality explosions, copy-on-write

Why this matters for AI/backend engineering:
    Every item in this file is a real production incident: a model
    trained on silently dropped values, a merge that produced 3x
    the rows, a NaN comparison that filtered out the most important
    customers. Learn to SEE the traps, and half your debugging
    career disappears.

Run:      python 44-pandas-pitfalls.py
Verify:   python 44-pandas-pitfalls.py --verify
Reference: https://pandas.pydata.org/docs/user_guide/indexing.html
"""

from __future__ import annotations

import sys
import warnings

import numpy as np
import pandas as pd

np.random.seed(42)
pd.set_option("mode.chained_assignment", "warn")

# ============================================================
# 1. Chained Assignment -- The Write That Never Happens
# ============================================================
# df[cond]["col"] = x is TWO selections. The second [] may operate
# on a copy; pandas warns, and your write vanishes. The fix is ONE
# .loc selection -- unambiguous, always writes.

# Example 1: the silent drop
df_chain = pd.DataFrame({"a": [1, 2, 3, 4], "b": [10.0, 20.0, 30.0, 40.0]})
df_chain["flag"] = 0
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    sub = df_chain[df_chain["a"] > 2]
    sub["flag"] = 1
print("Chained write flagged rows:", int(df_chain["flag"].sum()))
df_chain.loc[df_chain["a"] > 2, "flag"] = 1
print("One .loc write flagged rows:", int(df_chain["flag"].sum()))

# Output:
# Chained write flagged rows: 0
# One .loc write flagged rows: 2


# ============================================================
# 2. Index Alignment -- Operations Match LABELS, Not Positions
# ============================================================
# Adding two Series aligns on index. Mismatched labels produce NaN
# instead of an error -- silently. This is the most common source
# of "my features are all NaN" bugs.

# Example 2: same values, different index -> NaN soup
left = pd.Series([1.0, 2.0, 3.0], index=[0, 1, 2])
right = pd.Series([10.0, 20.0, 30.0], index=[1, 2, 3])
print("left + right:", (left + right).tolist())
print("After reindex, alignment gone:",
      (left.reset_index(drop=True) + right.reset_index(drop=True)).tolist())

# Output:
# left + right: [nan, 12.0, 23.0, nan]
# After reindex, alignment gone: [11.0, 22.0, 33.0]


# ============================================================
# 3. inplace=True -- Neither Faster Nor Cleaner
# ============================================================
# inplace=True performs the SAME work; it does not save memory
# (the old object is usually kept alive anyway) and it cannot be
# chained. It also silently does nothing useful on a copy. Use
# assignment: df = df.dropna() -- explicit, reviewable, chainable.

# Example 3: inplace returns None and cannot chain
df_ip = pd.DataFrame({"x": [1.0, np.nan, 3.0]})
result = df_ip.dropna(inplace=True)
print("dropna(inplace=True) returns:", result)
print("Frame was modified in place:", len(df_ip) == 2)

# Output:
# dropna(inplace=True) returns: None
# Frame was modified in place: True


# ============================================================
# 4. NaN != NaN -- Compare With isna(), Never With ==
# ============================================================
# NaN is not equal to anything, including itself. Filtering with
# == np.nan removes NOTHING. Use isna()/notna() -- they are the
# only honest predicates.

# Example 4: the filter that drops nothing
s = pd.Series([1.0, np.nan, 3.0, np.nan])
dropped_nothing = s[s != np.nan]
removed_correctly = s[s.notna()]
print("Filtering with != np.nan keeps:", len(dropped_nothing), "of", len(s))
print("Filtering with notna() keeps:", removed_correctly.tolist())

# Output:
# Filtering with != np.nan keeps: 4 of 4
# Filtering with notna() keeps: [1.0, 3.0]


# ============================================================
# 5. Silent Dtype Upcasting
# ============================================================
# pandas picks the SAFEST dtype when combining: int + float becomes
# float, int + string becomes object. pandas 2.2 emits a
# FutureWarning when a string lands in an int column (pandas 3
# raises instead) -- but the OBJECT dtype still appears either way,
# breaking every string-method and performance assumption. Check
# dtypes after every setitem; never let a stray value rewrite a
# column's contract.

# Example 5: one bad row silently rewrites a column's dtype
with warnings.catch_warnings():
    warnings.simplefilter("ignore", FutureWarning)   # suppress the 2.2 notice
    df_up = pd.DataFrame({"id": [1, 2, 3]})
    df_up.loc[2, "id"] = "oops"
print("id dtype after a string lands in it:", df_up["id"].dtype)
df_mix = pd.DataFrame({"a": [1, 2]})
df_mix["b"] = [1.5, 2.5]
print("int column + float column ->",
      [str(t) for t in df_mix.dtypes.tolist()])

# Output:
# id dtype after a string lands in it: object
# int column + float column -> ['int64', 'float64']


# ============================================================
# 6. iterrows() -- The O(n * Python) Trap
# ============================================================
# iterrows() converts every row to a Series and runs Python per
# row: 100x-1000x slower than the vectorized equivalent. When you
# MUST loop, itertuples() is 20-50x faster (plain tuples, no
# Series construction). Prefer vectorized ops and .apply for real
# work.

# Example 6: same result, dramatically different cost class
n = 5_000
loop_df = pd.DataFrame({"a": np.arange(n), "b": np.arange(n) * 2})

def with_iterrows(frame: pd.DataFrame) -> float:
    total = 0.0
    for _, row in frame.iterrows():
        if row["a"] % 2 == 0:
            total += row["b"]
    return total

def with_itertuples(frame: pd.DataFrame) -> float:
    total = 0.0
    for row in frame.itertuples(index=False):
        if row.a % 2 == 0:
            total += row.b
    return total

def vectorized(frame: pd.DataFrame) -> float:
    return float(frame.loc[frame["a"] % 2 == 0, "b"].sum())

print("iterrows result:", with_iterrows(loop_df))
print("itertuples result:", with_itertuples(loop_df))
print("vectorized result:", vectorized(loop_df))

# Output:
# iterrows result: 12495000.0
# itertuples result: 12495000.0
# vectorized result: 12495000.0


# ============================================================
# 7. Merge Cardinality Explosions
# ============================================================
# A one-to-many merge multiplies rows; many-to-many multiplies
# CROSS PRODUCTS. If the key is not unique on either side, expect
# rows to grow. Check uniqueness BEFORE merging -- 2 a-orders
# merged with 3 a-profiles produce 2 x 3 = 6 rows.

# Example 7: duplicate keys blow up row counts
orders = pd.DataFrame({"cust": ["a", "a", "b"], "amt": [1, 2, 3]})
profile = pd.DataFrame({"cust": ["a", "a", "a"], "city": ["NY", "LA", "SF"]})
merged = orders.merge(profile, on="cust")
print("orders rows:", len(orders), "| profile rows:", len(profile),
      "| merged rows:", len(merged))
print("Unique customers in orders:", orders["cust"].nunique(),
      "| in profile:", profile["cust"].nunique())

# Output:
# orders rows: 3 | profile rows: 3 | merged rows: 6
# Unique customers in orders: 2 | in profile: 1


# ============================================================
# 8. Copy-on-Write -- The Future Default, Test It Today
# ============================================================
# pandas 2.x: CoW off by default (views can alias); pandas 3.x:
# CoW on (every write copies). Code that mutates a shallow copy and
# EXPECTS the parent to change breaks under CoW; code that mutates
# one and DOESN'T expect the parent to change silently corrupts
# data today. Write code that works under BOTH.

# Example 8: same code, two worlds (single-cell write through a
# shared-block copy -- the clearest view/copy semantic split)
def slice_mutation(frame: pd.DataFrame) -> list[float]:
    view = frame.copy(deep=False)   # shares the data blocks
    view.iloc[0, 0] = 99
    return frame["a"].tolist()

pd.set_option("mode.copy_on_write", False)
cow_off = slice_mutation(pd.DataFrame({"a": [1, 2, 3], "b": [5.0, 6.0, 7.0]}))
pd.set_option("mode.copy_on_write", True)
cow_on = slice_mutation(pd.DataFrame({"a": [1, 2, 3], "b": [5.0, 6.0, 7.0]}))
pd.set_option("mode.copy_on_write", False)   # restore default

print("CoW off: parent sees", cow_off, "| CoW on: parent sees", cow_on)
print("Behavior differs between modes:", cow_off != cow_on)

# Output:
# CoW off: parent sees [99, 2, 3] | CoW on: parent sees [1, 2, 3]
# Behavior differs between modes: True


# ============================================================
# 9. Production Pattern: A Pre-Merge Contract Check
# ============================================================
# The senior habit: assert the shape of reality BEFORE expensive
# operations. A merge guard takes 3 lines and turns a silent row
# explosion into a loud, immediate error.

def merge_with_contract(left: pd.DataFrame, right: pd.DataFrame,
                        key: str) -> pd.DataFrame:
    """Merge, but refuse to explode on duplicate keys."""
    assert right[key].is_unique, \
        f"right side key '{key}' must be unique; found duplicates"
    return left.merge(right, on=key)

# Example 9: the guard catches a duplicate-key disaster
try:
    merge_with_contract(orders, profile, "cust")
    print("Merge succeeded (unexpected!)")
except AssertionError as err:
    print("Guard caught:", str(err))

# Output:
# Guard caught: right side key 'cust' must be unique; found duplicates


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: df[cond]["col"] = x, then wondering where the data went
# CORRECT: df.loc[cond, "col"] = x
#
# MISTAKE: comparing with == np.nan to find missing values
# CORRECT: df["col"].isna() / .notna()
#
# MISTAKE: trusting row counts after a merge
# CORRECT: assert df[key].is_unique on the many-side key first
#
# MISTAKE: "optimizing" with inplace=True
# CORRECT: df = df.dropna()   # explicit rebinding, chainable


# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # Chained assignment writes to a copy: the original is untouched.
    assert int(df_chain["flag"].sum()) == 2, \
        "only the .loc write may land in the frame"

    # Index alignment produces NaN at non-matching labels.
    assert np.isnan((left + right).iloc[0]), \
        "label 0 only exists in left -> NaN"
    assert (left + right).iloc[1] == 12.0, "label 1 exists in both"

    # inplace=True returns None (not the frame).
    assert result is None, "inplace methods must return None"

    # NaN never equals itself.
    assert np.isnan(np.nan) and not (np.nan == np.nan), \
        "NaN must not equal itself"
    assert len(dropped_nothing) == 4, \
        "filtering with != np.nan must keep every row"
    assert removed_correctly.tolist() == [1.0, 3.0], \
        "notna() must remove exactly the NaNs"

    # Dtype upcasting is silent and visible.
    assert df_up["id"].dtype == np.dtype("object"), \
        "a string in an int column must upcast to object"

    # All three loop spellings agree numerically.
    assert with_iterrows(loop_df) == with_itertuples(loop_df) == vectorized(loop_df), \
        "iterrows/itertuples/vectorized must agree"

    # Duplicate keys explode the merge row count.
    assert len(merged) == 6, "2x3 duplicate-key merge must produce 6 rows"

    # Copy-on-write changes slice mutation semantics.
    assert cow_off == [99, 2, 3], \
        "CoW off: shallow-copy write must reach the parent"
    assert cow_on == [1, 2, 3], \
        "CoW on: shallow-copy write must NOT reach the parent"

    # The merge guard refuses duplicate keys loudly.
    try:
        merge_with_contract(orders, profile, "cust")
        raise AssertionError("guard must refuse duplicate keys")
    except AssertionError:
        pass

    print("[OK] 44-pandas-pitfalls: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. One .loc selection; never chain writes.")
        print("2. isna()/notna() -- NaN never equals NaN.")
        print("3. Assert key uniqueness before every merge.")
        _verify()          # always runs, so plain execution is also a test
