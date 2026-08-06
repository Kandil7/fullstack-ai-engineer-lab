"""
01-core-python — 48: Comprehensions & Modern Syntax
====================================================
Topics: list/dict/set comprehensions, nested + conditional forms, generator
        expressions, walrus :=, f"{x=}", positional-only / and keyword-only *,
        zip(strict=True), itertools.pairwise, dict merge |, str.removeprefix

Why this matters for AI/backend engineering:
    `[transform(x) for x in batch]` is the daily idiom of data pipelines.
    Generator expressions stream a 10GB corpus without materializing it.
    zip(strict=True) catches silently misaligned train/label pairs — the kind
    of bug that quietly corrupts a model. Walrus lets you compute once, use twice.

Run:      python 48-comprehensions-and-modern-syntax.py
Verify:   python 48-comprehensions-and-modern-syntax.py --verify
Reference: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
"""

from __future__ import annotations

import itertools
import sys

# ============================================================
# 1. List Comprehensions
# ============================================================
# Comprehension = expression + for-clause (+ optional if-clause). Readable
# transformation in one line. If the body needs statements, use a plain loop.

# Example 1: basic transform and filter
tokens = ["the", "cat", "sat", "on", "the", "mat"]
upper = [t.upper() for t in tokens]
print(f"Uppercased: {upper}")

long_words = [t for t in tokens if len(t) >= 3]
print(f"Words >= 3 chars: {long_words}")

# Output:
# Uppercased: ['THE', 'CAT', 'SAT', 'ON', 'THE', 'MAT']
# Words >= 3 chars: ['the', 'cat', 'sat', 'the', 'mat']

# ============================================================
# 2. Dict and Set Comprehensions
# ============================================================
# Same shape, different braces. Dict: {key_expr: value_expr for ...}.
# Set: {expr for ...} — deduplicates automatically.

# Example 2: token -> id vocab built in one line
vocab = {w: i for i, w in enumerate(sorted(set(tokens)))}
print(f"Vocab: {vocab}")

unique_lengths = {len(t) for t in tokens}
print(f"Unique lengths: {unique_lengths}")

# Output:
# Vocab: {'cat': 0, 'mat': 1, 'on': 2, 'sat': 3, 'the': 4}
# Unique lengths: {2, 3}

# ============================================================
# 3. Generator Expressions — Lazy Streaming
# ============================================================
# Parentheses instead of brackets. No list is built — values are produced
# one at a time. O(1) memory instead of O(n). The tradeoff: single pass only.

# Example 3: memory-flat stream vs materialized list
import math

def squares_upto(n: int) -> list[int]:
    return [i * i for i in range(n)]          # materializes n ints


def squares_lazy(n: int) -> "generator":
    return (i * i for i in range(n))          # streams, O(1) memory


big_list = squares_upto(1_000_000)
gen = squares_lazy(1_000_000)
print(f"\nList size (sys.getsizeof): {sys.getsizeof(big_list)} bytes")
print(f"Generator size:           {sys.getsizeof(gen)} bytes")

# Output:
# List size (sys.getsizeof): 8448728 bytes
# Generator size:           112 bytes

# ============================================================
# 4. Nested & Conditional Comprehensions
# ============================================================
# The for-clauses nest left-to-right (outermost first) — same as loop order.

# Example 4: flattening a matrix of batches
batches = [[1, 2], [3, 4, 5], [6]]
flat = [x for batch in batches for x in batch]
print(f"\nFlattened batches: {flat}")

pairs = [(i, j) for i in range(2) for j in range(2) if i != j]
print(f"Off-diagonal pairs: {pairs}")

# Output:
# Flattened batches: [1, 2, 3, 4, 5, 6]
# Off-diagonal pairs: [(0, 1), (1, 0)]

# ============================================================
# 5. Walrus := — Compute Once, Use Twice
# ============================================================
# Assign-and-test in expressions. Best where it removes a double call or a
# pre-loop assignment. If it hurts readability, skip it — it is optional.

# Example 5: avoid re-parsing
def parse_float(s: str) -> float | None:
    try:
        return float(s)
    except ValueError:
        return None


values = ["3.14", "abc", "2.5", "xyz"]
valid = [v for v in values if (parsed := parse_float(v)) is not None]
print(f"\nValid floats: {valid}")

# Example 6: while-loop sentinel without duplication
# input_or_empty() is defined at module level below the section for clarity
def input_or_empty() -> str:
    """Return an empty string so the demo loop exits after one read."""
    return ""


chunk = ""
while (chunk := input_or_empty()) != "":
    print(f"  read chunk: {chunk!r}")
    break  # one iteration for the demo

# Output:
# Valid floats: ['3.14', '2.5']

# ============================================================
# 6. f"{x=}" Debugging + removeprefix
# ============================================================
# f"{x=}" prints name and value — the fastest way to trace a pipeline.

# Example 7: debug formatting
lr = 3e-4
epoch = 12
print(f"\n{lr=} {epoch=}")

# Example 8: removeprefix / removesuffix (3.9+)
filename = "model_checkpoint_v3.pt"
print(f"Stem: {filename.removesuffix('.pt')}")
path = "s3://bucket/key"
print(f"Bucket path: {path.removeprefix('s3://')}")

# Output:
# lr=0.0003 epoch=12
# Stem: model_checkpoint_v3
# Bucket path: bucket/key

# ============================================================
# 7. Positional-only / Keyword-only Parameters
# ============================================================
# `/` before it: positional-only (can't pass by name). `*` after it:
# keyword-only (must pass by name). Locking the call signature prevents
# silently wrong positional argument order in hot library code.

# Example 9: both markers
def train(model, /, *, epochs: int, lr: float) -> str:
    return f"train {model} for {epochs} epochs at lr={lr}"


print(f"\n{train('bert', epochs=3, lr=1e-4)}")

# Output:
# train bert for 3 epochs at lr=0.0001

# ============================================================
# 8. zip(strict=True) and itertools.pairwise
# ============================================================
# zip(strict=True) raises ValueError on length mismatch — catching
# misaligned data instead of silently truncating.

# Example 10: strict zip catches drift
inputs = ["q1", "q2", "q3"]
labels = ["a1", "a2"]  # one short — a real-world data bug
try:
    list(zip(inputs, labels, strict=True))
except ValueError as e:
    print(f"\nstrict zip caught drift: {e}")

# Example 11: pairwise for sliding window deltas
scores = [0.1, 0.4, 0.9, 1.6]
deltas = [b - a for a, b in itertools.pairwise(scores)]
print(f"Score deltas: {deltas}")

# Output:
# strict zip caught drift: zip() argument 2 is shorter than argument 1
# Score deltas: [0.30000000000000004, 0.5, 0.7000000000000001]

# ============================================================
# 9. Dict Merge with |
# ============================================================
# The | operator merges dicts (3.9+) without mutating either operand.
# | updates in place; both keep the LAST value for duplicate keys.

# Example 12: merging config layers
defaults = {"lr": 1e-3, "batch": 32, "seed": 0}
overrides = {"lr": 1e-4, "epochs": 10}
merged = defaults | overrides
print(f"\nMerged config: {merged}")

# Output:
# Merged config: {'lr': 1e-04, 'batch': 32, 'seed': 0, 'epochs': 10}

# ============================================================
# 10. Production Pattern — Comprehension Pipeline
# ============================================================
# Chain comprehension + generator + strict zip into one readable pipeline.

def clean_batch(rows: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Return (question, answer) pairs, trimmed, deduped, non-empty."""
    cleaned = {
        (q.strip(), a.strip())
        for q, a in rows
        if q.strip() and a.strip()
    }
    return sorted(cleaned)


rows = [(" What is RAG? ", "Retrieval-augmented generation"), (" ", "x"), ("q", "")]
print(f"\nCleaned pairs: {clean_batch(rows)}")

# Output:
# Cleaned pairs: [('What is RAG?', 'Retrieval-augmented generation')]

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: comprehension with side effects (file writes, prints)
#   bad = [os.makedirs(d) for d in dirs]      # side effect hidden in an expr
# CORRECT:
#   good = [os.makedirs(d) for d in dirs] or [d for d in dirs if ...]

# MISTAKE: comprehension shadowing an outer variable
#   x = 0
#   bad = [x for x in range(3)]   # x is rebound to 2 afterwards
# CORRECT:
#   good = [_ for _ in range(3)]  # keeps the outer x untouched

# MISTAKE: zip without strict silently truncates aligned data
#   bad = list(zip(features, labels))         # silent misalignment
# CORRECT:
#   good = list(zip(features, labels, strict=True))

# MISTAKE: walrus overuse hurting readability
#   bad = (a := (b := compute())) and (c := a + b)
# CORRECT:
#   good = result = compute(); use result twice

# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    tokens2 = ["the", "cat", "sat", "on", "the", "mat"]

    # List comprehension equivalence to loop
    assert [t.upper() for t in tokens2] == [t.upper() for t in tokens2]
    long = [t for t in tokens2 if len(t) >= 3]
    assert all(len(t) >= 3 for t in long), "filter must keep only long words"

    # Dict + set comprehension
    vocab = {w: i for i, w in enumerate(sorted(set(tokens2)))}
    assert vocab["cat"] == 0 and vocab["the"] == 4, "vocab indices by sorted order"
    assert {len(t) for t in tokens2} == {2, 3}, "set comprehension dedupes"

    # Generator is lazy and single-use
    gen = (i for i in range(5))
    assert next(gen) == 0 and list(gen) == [1, 2, 3, 4], \
        "generator streams and exhausts"

    # Flatten order (outermost first)
    assert [x for batch in [[1, 2], [3]] for x in batch] == [1, 2, 3], \
        "nesting order is left-to-right"

    # Walrus filters without double parse
    assert valid == ["3.14", "2.5"], "walrus must filter invalid floats"

    # f"{x=}" produces name=value text
    lr, epoch = 3e-4, 12
    assert f"{lr=}" == "lr=0.0003", "f-string debug format"

    # removeprefix/removesuffix
    assert "model_v3.pt".removesuffix(".pt") == "model_v3"
    assert "s3://b/k".removeprefix("s3://") == "b/k"

    # zip strict raises on mismatch
    try:
        list(zip([1, 2, 3], [1], strict=True))
        assert False, "strict zip must raise on length mismatch"
    except ValueError:
        pass

    # pairwise
    assert list(itertools.pairwise([1, 2, 3])) == [(1, 2), (2, 3)]

    # dict merge
    assert {"a": 1} | {"b": 2} == {"a": 1, "b": 2}
    assert {"a": 1} | {"a": 9} == {"a": 9}, "right operand wins on dup keys"

    # Clean-batch pipeline
    assert clean_batch([(" q ", "a"), (" ", "x"), ("q", "")]) == [("q", "a")]

    print("[OK] 48-comprehensions-and-modern-syntax: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Comprehensions: expression + for + if, one-liner transforms")
        print("2. Generator expressions stream with O(1) memory")
        print("3. zip(strict=True) catches silent data misalignment")
        print("4. Walrus := computes once, uses twice")
        print("5. | merges dicts; removeprefix/removesuffix for strings")
        _verify()
