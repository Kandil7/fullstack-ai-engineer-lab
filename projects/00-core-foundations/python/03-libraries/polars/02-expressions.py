"""
Polars — 02: Expressions
=========================
Topics: the expression API; select / with_columns / filter; contexts;
composable expressions (alias, arithmetic, string ops).

Why this matters for AI/backend engineering:
    Feature engineering is expression composition. In pandas you mix
    column access, methods, and occasional apply() loops; in Polars every
    transform is an Expr object that only runs when a *context* consumes
    it. Expressions are lazily built, optimizer-visible, and identical in
    eager and lazy mode — the same `pl.col("x").mean()` works on a
    DataFrame and a 50GB LazyFrame. Mastering contexts is mastering the
    whole library.

Run:      python 02-expressions.py
Verify:   python 02-expressions.py --verify
Reference: https://docs.pola.rs/user-guide/concepts/expressions-and-contexts/
"""

from __future__ import annotations

import sys

try:
    import polars as pl
except ImportError:  # pragma: no cover - optional dependency
    print("[skip] polars not installed - install with: pip install polars")
    sys.exit(0)

# ============================================================
# 1. What an Expr is: a lazy recipe, not a value
# ============================================================
# pl.col("score") returns an Expr: a description of "the score column".
# It holds no data. Arithmetic and methods BUILD new Exprs:
#   pl.col("score") * 100          -> Expr (multiply)
#   pl.col("score").mean()         -> Expr (aggregate)
# An Expr evaluates only inside a context: select, with_columns, filter,
# or group_by.agg.

# Example 1: expressions are objects you can inspect and reuse
expr = (pl.col("score") * 100).alias("score_pct")
print(f"expr type: {type(expr).__name__}")

# Output:
# expr type: Expr

df = pl.DataFrame(
    {
        "user": ["a", "b", "c", "a"],
        "score": [0.9, 0.4, 0.7, 0.2],
        "spend": [10, 20, 30, 40],
    }
)

# Example 2: the same Expr object reused in two contexts
result1 = df.select(expr)
result2 = df.with_columns(expr)
print(result1.to_dict(as_series=False))
print(result2.columns)

# Output:
# {'score_pct': [90.0, 40.0, 70.0, 20.0]}
# ['user', 'score', 'spend', 'score_pct']


# ============================================================
# 2. select: the projection context (choose and compute columns)
# ============================================================
# select() returns a NEW frame with exactly the named columns, in order.
# It can also compute new columns on the fly. Think: "what columns do I
# want out of this table?"

def select_demo(frame: pl.DataFrame) -> pl.DataFrame:
    """Project existing and computed columns."""
    return frame.select(
        pl.col("user"),
        (pl.col("spend") / pl.col("score")).alias("cost_per_point"),
    )


# Example 3: select builds the output schema
sel = select_demo(df)
print(sel.to_dict(as_series=False))

# Output:
# {'user': ['a', 'b', 'c', 'a'], 'cost_per_point': [11.111..., 50.0, 42.857..., 200.0]}


# ============================================================
# 3. with_columns: the transform context (add or replace columns)
# ============================================================
# with_columns() keeps every existing column and adds/overwrites the
# named ones. This is the workhorse of feature engineering: one call,
# many derived features, all vectorized.

def with_columns_demo(frame: pl.DataFrame) -> pl.DataFrame:
    """Add three derived features in a single context."""
    return frame.with_columns(
        (pl.col("spend") / 100).alias("spend_norm"),
        pl.col("score").rank(descending=True).alias("score_rank"),
        pl.when(pl.col("score") >= 0.5)
        .then(pl.lit("high"))
        .otherwise(pl.lit("low"))
        .alias("band"),
    )


# Example 4: one call, three new columns
w = with_columns_demo(df)
print(w.columns)
print(w["band"].to_list())

# Output:
# ['user', 'score', 'spend', 'spend_norm', 'score_rank', 'band']
# ['high', 'low', 'high', 'low']


# ============================================================
# 4. filter: the row context (choose rows by predicate)
# ============================================================
# filter() keeps rows where the predicate Expr is True. Predicates are
# built from comparisons and combined with & | ~ (NOT and/or — Python's
# and/or do not work on Exprs).

def filter_demo(frame: pl.DataFrame) -> pl.DataFrame:
    """Keep high-scoring users who also spent at least 15."""
    return frame.filter(
        (pl.col("score") >= 0.5) & (pl.col("spend") >= 15)
    )


# Example 5: compound predicate with & and parentheses
f = filter_demo(df)
print(f.rows())

# Output:
# [('c', 0.7, 30)]


# ============================================================
# 5. group_by + agg: the aggregation context
# ============================================================
# group_by splits the frame, applies an aggregate Expr per group, and
# combines. Any expression that reduces many rows to one value (mean,
# sum, count, first) can appear in .agg(). This is split-apply-combine
# without apply().

def groupby_demo(frame: pl.DataFrame) -> pl.DataFrame:
    """Per-user aggregates in one context."""
    return frame.group_by("user").agg(
        pl.col("score").mean().alias("avg_score"),
        pl.col("spend").sum().alias("total_spend"),
        pl.len().alias("n_events"),
    )


# Example 6: one group_by, three aggregates
g = groupby_demo(df).sort("user")
print(g.rows())

# Output:
# [('a', 0.55, 50, 2), ('b', 0.4, 20, 1), ('c', 0.7, 30, 1)]


# ============================================================
# 6. Composing contexts: a feature pipeline in one expression
# ============================================================
# Contexts nest: filter inside a select, aggregates inside with_columns
# (window-style). The whole chain stays one lazy graph, so the optimizer
# sees everything before anything runs.

def pipeline_demo(frame: pl.DataFrame) -> pl.DataFrame:
    """Filter, rank within group, and normalize in one chain."""
    return (
        frame.filter(pl.col("spend") > 0)
        .with_columns(pl.col("spend").rank().over("user").alias("spend_rank_in_user"))
        .select(pl.col("user"), pl.col("score"), pl.col("spend_rank_in_user"))
    )


# Example 7: rank over a group inside with_columns
p = pipeline_demo(df)
print(p.rows())

# Output:
# [('a', 0.9, 1.0), ('b', 0.4, 1.0), ('c', 0.7, 1.0), ('a', 0.2, 2.0)]


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: .alias() binding to the wrong operand (Python precedence!)
#   pl.col("spend") / pl.col("score").alias("x")  # alias binds to score only
# CORRECT:
#   (pl.col("spend") / pl.col("score")).alias("x")  # alias the WHOLE expression
#
# MISTAKE: Python and/or on expressions
#   df.filter(pl.col("a") > 1 and pl.col("b") < 2)  # ValueError
# CORRECT:
#   df.filter((pl.col("a") > 1) & (pl.col("b") < 2))
#
# MISTAKE: putting a Python function call inside an expression
#   df.select(pl.col("x").apply(my_py_fn))   # slow, and now discouraged
# CORRECT: use a native expression or pl.map_batches for real functions
#
# MISTAKE: forgetting select() returns only the named columns
#   df.select(pl.col("a"))  # frame with ONLY column a - intended
# CORRECT: with_columns() when you want to KEEP the other columns


# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    assert isinstance(expr, pl.Expr), "pl.col() must produce an Expr, not data"
    assert expr.meta.output_name() == "score_pct", \
        ".alias() must set the output name"

    sel = select_demo(df)
    assert sel.columns == ["user", "cost_per_point"], \
        "select() must return exactly the projected columns"
    assert abs(sel["cost_per_point"][0] - 10.0 / 0.9) < 1e-9, \
        "computed column must be spend / score"

    w = with_columns_demo(df)
    assert w.shape == (4, 6), "with_columns must keep all rows and add 3 cols"
    assert w["band"].to_list() == ["high", "low", "high", "low"], \
        "when/then/otherwise must map thresholds to bands"
    assert w["score_rank"].to_list() == [1.0, 3.0, 2.0, 4.0], \
        "rank(descending=True) must put the highest score at rank 1"

    f = filter_demo(df)
    assert f.rows() == [("c", 0.7, 30)], \
        "compound & predicate must keep only high AND spent rows"

    g = groupby_demo(df).sort("user")
    assert g.rows() == [("a", 0.55, 50, 2), ("b", 0.4, 20, 1), ("c", 0.7, 30, 1)], \
        "group_by agg must compute per-group mean/sum/count"
    assert "n_events" in g.columns, "pl.len() must count rows per group"

    p = pipeline_demo(df)
    assert p.rows()[3] == ("a", 0.2, 2.0), \
        "rank().over('user') must rank within each group"

    print("[OK] 02-expressions: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Expr objects are recipes; contexts (select/with_columns/filter) run them")
        print("2. select projects, with_columns transforms, filter selects rows")
        print("3. group_by().agg() is split-apply-combine without apply()")
        _verify()   # always runs, so plain execution is also a test
