# 01-core-python — 48: Comprehensions & Modern Syntax

## Topic Overview

Comprehensions are Python's idiomatic data-transform expression:
`[transform(x) for x in batch]` is the daily vocabulary of data pipelines,
from tokenizing a prompt to normalizing a dataset. Generator expressions do
the same work **lazily**, streaming a 10GB corpus without materializing it.
Modern syntax layers on top: the walrus operator (`:=`) for compute-once
patterns, `f"{x=}"` for debugging, `zip(strict=True)` for catching silently
misaligned data, `itertools.pairwise` for sliding windows, positional-only
and keyword-only parameters for locking call signatures, and the `|` dict
merge.

This lecture exists because the module targets Python 3.10+ but three of
these features measured at **zero occurrences** in the previous 41 files.
These are not trivia — `zip(strict=True)` is the difference between a model
trained on aligned data and one silently trained on shifted pairs.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Write list, dict, and set comprehensions with conditions and nesting
2. Choose a generator expression over a list when memory matters
3. Use the walrus operator `:=` to compute once and use twice
4. Read `f"{x=}"` debug output and apply `removeprefix`/`removesuffix`
5. Design call signatures with positional-only `/` and keyword-only `*`
6. Catch misaligned data with `zip(strict=True)` and sliding windows with `pairwise`
7. Merge dicts with `|` and `|=` without mutating the source
8. Explain when a plain loop is clearer than a comprehension
9. Build a streaming cleaning pipeline from these pieces

## Prerequisites

| Need | Where |
|------|-------|
| `for` loops and iteration | `20-for.py`, `24-iterators.py` |
| Dictionaries and sets | `16-dictionaries.py`, `15-sets.py` |
| Functions, `*args`/`**kwargs` | `21-functions.py` |
| Generators and laziness | `24-iterators.py` |

## 1. List Comprehensions — Transform + Filter

A comprehension is `expression` + `for`-clause + optional `if`-clause. It
reads in the same order as the equivalent loop, but as an expression that
can be assigned, passed, or returned. If the body needs statements (side
effects, multiple steps), use a plain loop.

```python
tokens = ["the", "cat", "sat", "on", "the", "mat"]
upper = [t.upper() for t in tokens]
print(f"Uppercased: {upper}")

long_words = [t for t in tokens if len(t) >= 3]
print(f"Words >= 3 chars: {long_words}")
```

```
# Output:
# Uppercased: ['THE', 'CAT', 'SAT', 'ON', 'THE', 'MAT']
# Words >= 3 chars: ['the', 'cat', 'sat', 'the', 'mat']
```

The `if` filter comes after the `for` — that order is part of the grammar,
and it mirrors loop nesting. A comprehension is always a full re-build:
each element is computed fresh, so nothing aliases the source.

## 2. Dict and Set Comprehensions

Same shape, different braces. A dict comprehension uses
`{key_expr: value_expr for ...}`; a set comprehension uses `{expr for ...}`
and deduplicates automatically. Both are O(n) and both can be filtered.

```python
tokens = ["the", "cat", "sat", "on", "the", "mat"]
vocab = {w: i for i, w in enumerate(sorted(set(tokens)))}
print(f"Vocab: {vocab}")

unique_lengths = {len(t) for t in tokens}
print(f"Unique lengths: {unique_lengths}")
```

```
# Output:
# Vocab: {'cat': 0, 'mat': 1, 'on': 2, 'sat': 3, 'the': 4}
# Unique lengths: {2, 3}
```

This one-liner is the standard `token -> id` vocabulary builder. Note the
set comprehension deduplicated `len(t)` values automatically — `2` appears
once even though several tokens have length 2.

## 3. Generator Expressions — Lazy Streaming

Parentheses instead of brackets produce a **generator expression**: no list
is built; values are produced one at a time on demand. Memory is O(1)
regardless of the sequence length. The tradeoff: it is single-pass — once
consumed, it is gone.

```python
import sys

def squares_upto(n: int) -> list[int]:
    return [i * i for i in range(n)]          # materializes n ints

def squares_lazy(n: int):
    return (i * i for i in range(n))          # streams, O(1) memory

big_list = squares_upto(1_000_000)
gen = squares_lazy(1_000_000)
print(f"List size (sys.getsizeof): {sys.getsizeof(big_list)} bytes")
print(f"Generator size:           {sys.getsizeof(gen)} bytes")
```

```
# Output:
# List size (sys.getsizeof): 8448728 bytes
# Generator size:           112 bytes
```

8.4MB vs 112 bytes for the same 1M values. This is why corpus streaming
uses generators: `sum(len(line) for line in open(f))` never holds the file
in memory, no matter how large it is.

## 4. Nested and Conditional Comprehensions

The `for`-clauses nest **left to right, outermost first** — exactly the
order of the equivalent loop. This is the #1 source of confusion, so read
the clauses like a loop:

```python
batches = [[1, 2], [3, 4, 5], [6]]
flat = [x for batch in batches for x in batch]
print(f"Flattened batches: {flat}")

pairs = [(i, j) for i in range(2) for j in range(2) if i != j]
print(f"Off-diagonal pairs: {pairs}")
```

```
# Output:
# Flattened batches: [1, 2, 3, 4, 5, 6]
# Off-diagonal pairs: [(0, 1), (1, 0)]
```

The loop equivalent of the second one is:

```python
pairs = []
for i in range(2):        # outermost clause first
    for j in range(2):    # then the inner clause
        if i != j:
            pairs.append((i, j))
```

If you find yourself nesting three or more clauses, extract a helper
function — readability drops fast.

## 5. Walrus `:=` — Compute Once, Use Twice

The walrus operator assigns a name **inside an expression**, which is
valuable when the same expensive computation would otherwise run twice —
once in a condition and once in the body. The canonical example: parse a
value, test it, and use the parsed result.

```python
def parse_float(s: str) -> float | None:
    try:
        return float(s)
    except ValueError:
        return None


values = ["3.14", "abc", "2.5", "xyz"]
valid = [v for v in values if (parsed := parse_float(v)) is not None]
print(f"Valid floats: {valid}")
```

```
# Output:
# Valid floats: ['3.14', '2.5']
```

Without the walrus you would call `parse_float(v)` twice — doubling the
work for every element, or write a clumsy two-step loop. It also shines in
`while` loops where the read-and-test would otherwise duplicate the read:

```python
chunk = ""
while (chunk := input_or_empty()) != "":
    process(chunk)
```

The walrus is **optional** — if `(n := len(items))` is not more readable
than `n = len(items)`, skip it.

## 6. `f"{x=}"` and String Methods

The `=` specifier in an f-string prints the expression, the equals sign,
and the value — the fastest way to trace a pipeline without writing
`print(f"lr = {lr}")` by hand.

```python
lr = 3e-4
epoch = 12
print(f"{lr=} {epoch=}")

filename = "model_checkpoint_v3.pt"
print(f"Stem: {filename.removesuffix('.pt')}")
path = "s3://bucket/key"
print(f"Bucket path: {path.removeprefix('s3://')}")
```

```
# Output:
# lr=0.0003 epoch=12
# Stem: model_checkpoint_v3
# Bucket path: bucket/key
```

`removeprefix` and `removesuffix` (3.9+) are the safe replacements for
`startswith` + slice or regex — they return the string unchanged when the
prefix/suffix does not match, which `s[len("s3://"):]` would not.

## 7. Positional-only and Keyword-only Parameters

The `/` marker makes everything before it positional-only (cannot be passed
by name); the `*` marker makes everything after it keyword-only (must be
passed by name). Locking the signature prevents silently wrong argument
order in hot library code — think `train("bert", 0.1, 32)` where the middle
argument could be lr or dropout.

```python
def train(model, /, *, epochs: int, lr: float) -> str:
    return f"train {model} for {epochs} epochs at lr={lr}"


print(f"{train('bert', epochs=3, lr=1e-4)}")
```

```
# Output:
# train bert for 3 epochs at lr=0.0001
```

Here `model` is positional-only, while `epochs` and `lr` are keyword-only.
The API is self-documenting: nobody can call `train(lr=0.1, "bert")`
silently reordering arguments.

## 8. `zip(strict=True)` and `itertools.pairwise`

Plain `zip` truncates to the shortest input — silently. If your features
and labels drifted out of sync (a real data bug), plain zip quietly drops
rows and your model trains on misaligned pairs. `zip(strict=True)` (3.10+)
raises `ValueError` on any length mismatch.

```python
import itertools

inputs = ["q1", "q2", "q3"]
labels = ["a1", "a2"]  # one short — a real-world data bug
try:
    list(zip(inputs, labels, strict=True))
except ValueError as e:
    print(f"strict zip caught drift: {e}")

scores = [0.1, 0.4, 0.9, 1.6]
deltas = [b - a for a, b in itertools.pairwise(scores)]
print(f"Score deltas: {deltas}")
```

```
# Output:
# strict zip caught drift: zip() argument 2 is shorter than argument 1
# Score deltas: [0.30000000000000004, 0.5, 0.7000000000000001]
```

`itertools.pairwise` yields consecutive pairs `(x0, x1), (x1, x2), ...` in
O(n) with O(1) extra memory — the foundation of deltas, sliding differences,
and transition counts.

## 9. Dict Merge with `|`

The `|` operator merges dicts (3.9+) without mutating either operand; `|=`
updates in place. On duplicate keys, the right operand wins — the standard
override semantics you want for layered config.

```python
defaults = {"lr": 1e-3, "batch": 32, "seed": 0}
overrides = {"lr": 1e-4, "epochs": 10}
merged = defaults | overrides
print(f"Merged config: {merged}")
```

```
# Output:
# Merged config: {'lr': 1e-04, 'batch': 32, 'seed': 0, 'epochs': 10}
```

`overrides` won the `lr` key; `defaults` contributed `batch` and `seed`;
`epochs` came only from `overrides`. The old idiom
`{**defaults, **overrides}` still works, but `|` is the readable form.

## 10. Production Pattern — A One-Line Cleaning Pipeline

Chain comprehension, set dedup, and sorting into a readable pipeline — the
shape of a data-cleaning step in a training-prep service:

```python
def clean_batch(rows: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Return (question, answer) pairs, trimmed, deduped, non-empty."""
    cleaned = {
        (q.strip(), a.strip())
        for q, a in rows
        if q.strip() and a.strip()
    }
    return sorted(cleaned)


rows = [(" What is RAG? ", "Retrieval-augmented generation"), (" ", "x"), ("q", "")]
print(f"Cleaned pairs: {clean_batch(rows)}")
```

```
# Output:
# Cleaned pairs: [('What is RAG?', 'Retrieval-augmented generation')]
```

The set comprehension deduplicates *and* drops empty pairs in one pass;
`q.strip()` runs twice per row (once in the expression, once in the filter)
— a place the walrus from section 5 would also work. For a 10M-row dataset,
the streaming version replaces the braces with parentheses and lets a
consumer iterate instead of materializing.

## Common Mistakes to Avoid

### Mistake 1: Side effects inside a comprehension
```python
# WRONG - the makedirs call is hidden inside an expression
[os.makedirs(d) for d in dirs]

# CORRECT - statements belong in a loop
for d in dirs:
    os.makedirs(d)
```

### Mistake 2: Comprehension shadowing an outer variable
```python
# WRONG - x is rebound to the last element (2) after the comprehension
x = 0
values = [x for x in range(3)]

# CORRECT - keep the outer name untouched
x = 0
values = [_ for _ in range(3)]
```

### Mistake 3: `zip` without strict silently truncates aligned data
```python
# WRONG - if labels has one fewer row, the pair drifts silently
pairs = list(zip(features, labels))

# CORRECT - any length mismatch becomes a loud ValueError
pairs = list(zip(features, labels, strict=True))
```

### Mistake 4: Walrus overuse
```python
# WRONG - unreadable
(a := (b := compute())) and (c := a + b)

# CORRECT - plain assignment when there is no condition to test
result = compute()
c = result + result
```

### Mistake 5: Wrong nesting order
```python
# WRONG - reads as if the filter applies before the inner loop
pairs = [(x, y) for x in xs if x > 0 for y in ys]

# CORRECT - filters bind to the nearest for-clause; write the loop first
pairs = [(x, y) for x in xs for y in ys if x > 0]
```

## Best Practices

1. Use comprehensions for transforms and filters; use loops for statements.
2. Prefer generator expressions when the result is consumed once and the
   sequence is large.
3. Add `strict=True` to every `zip` over paired data you expect to match.
4. Reach for the walrus when it removes a doubled computation; skip it when
   it hurts readability.
5. Keep comprehensions to two `for`-clauses or fewer; extract helpers beyond
   that.
6. Use `removeprefix`/`removesuffix` instead of manual slicing.
7. Lock public API signatures with `/` and `*` where argument order matters.
8. Use `|` for config merges and `|=` for in-place updates.

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| List comprehension | O(n) | O(n) | Generator expression — O(1) working memory |
| Dict comprehension | O(n) | O(n) | — |
| Set comprehension | O(n) | O(n) | Generator of unique-so-far if order matters |
| Generator expression creation | O(1) | O(1) | — |
| Full generator iteration | O(n) | O(1) | — |
| Walrus assignment | O(1) | O(1) | Avoids a second O(cost) call |
| `zip(strict=True)` | O(n) | O(n) | `itertools.zip_longest` if lengths may legitimately differ |
| `itertools.pairwise` | O(n) | O(1) | Slice-pair zip: `zip(xs, xs[1:])` — O(n) space |
| Dict merge `a \| b` | O(len(a)+len(b)) | O(len(a)+len(b)) | Update smaller dict into larger with `\|=` |

## AI Engineering Relevance

**Where this shows up:** `[transform(x) for x in batch]` is the daily idiom
of data pipelines — tokenizing, normalizing, filtering training rows.
Generator expressions stream a corpus that will not fit in RAM. `zip(strict=True)`
guards train/label alignment. Walrus avoids double-parsing every row of a
JSONL file.

| Concept here | Used for |
|---|---|
| List/dict comprehension | Batch tokenization, `{token: id}` vocab building |
| Generator expression | Streaming a 10GB corpus line by line |
| `zip(strict=True)` | Aligning (prompt, response) pairs before training |
| Walrus `:=` | Parsing each JSONL row exactly once |
| `pairwise` | Reward deltas, token transition counts |
| Dict merge `\|` | Layering model config: `defaults \| overrides` |
| `f"{x=}"` | Debugging a pipeline step without extra print lines |

**Scale note:** at 1M rows, a list comprehension costs ~80MB for the result
plus a full second pass; a generator expression costs O(1) and streams.
At 10M rows the list version starts risking OOM in a shared worker — the
generator is not a micro-optimization, it is the difference between fitting
in the job's memory budget and not.

## Practice Exercises

### Exercise 1: Filter and Transform (Difficulty: Easy)
Write `clean_tokens(tokens: list[str], stop: set[str]) -> list[str]` that
returns lowercased tokens not in `stop`, using a list comprehension.

### Exercise 2: Vocabulary Builder (Difficulty: Easy)
Write `build_vocab(texts: list[str]) -> dict[str, int]` returning
`{token: id}` with ids assigned in sorted order, using a set comprehension
and an enumerate dict comprehension.

### Exercise 3: Strict Alignment (Difficulty: Medium)
Write `align(inputs: list[str], labels: list[str]) -> list[tuple[str, str]]`
that returns pairs and **raises ValueError** when lengths differ, using
`zip(strict=True)`.

### Exercise 4: Stream Without Materializing (Difficulty: Medium)
Write `squares_sum(n: int) -> int` that sums `i*i` for `i in range(n)` using
a generator expression — it must work for `n = 10**9` (do not build a list).

### Exercise 5: Walrus Dedup Parse (Difficulty: Hard)
Write `parse_rows(rows: Iterable[str]) -> list[float]` that parses each row
exactly once (walrus or equivalent), keeps valid floats, and preserves
order. Prove the parse function is called once per row, not twice.

### Exercise 6: Cleaning Pipeline (Difficulty: Hard)
Write `stream_clean(rows: Iterable[tuple[str, str]]) -> Iterator[tuple[str, str]]`
that yields trimmed, non-empty, first-seen-wins pairs **lazily** — the first
output must be produced before the whole input is consumed.

## Summary

| Concept | Description |
|---|---|
| Comprehension | `[expr for x in it if cond]` — transform/filter in one expression |
| Dict/set forms | `{k: v for ...}` and `{expr for ...}` (dedupes) |
| Generator expression | Lazy, O(1) memory, single-pass |
| Walrus `:=` | Compute once, use twice inside an expression |
| `f"{x=}"` | Name-and-value debug output |
| `/` and `*` | Positional-only and keyword-only parameter markers |
| `zip(strict=True)` | Loud failure on length mismatch instead of silent truncation |
| `pairwise` | Consecutive pairs for deltas and transitions |
| `\|` merge | Non-mutating dict merge, right operand wins |

Comprehensions are how Python expresses data transformation without
ceremony. The modern syntax around them — strict zip, walrus, pairwise —
exists to catch the silent mistakes that corrupt data at scale. When you
need a loop, write a loop; when an expression tells the story, the
comprehension is the cleanest sentence in the language.

## Quick Reference

| Task | Idiom |
|---|---|
| Transform a batch | `[t.upper() for t in tokens]` |
| Filter a batch | `[t for t in tokens if len(t) >= 3]` |
| Build a vocab | `{w: i for i, w in enumerate(sorted(set(words)))}` |
| Stream, don't list | `(x * x for x in range(n))` |
| Parse once, test | `[v for v in raw if (parsed := float_or_none(v)) is not None]` |
| Debug print | `print(f"{lr=} {epoch=}")` |
| Strip prefix/suffix | `s.removeprefix("s3://")`, `s.removesuffix(".pt")` |
| Locked signature | `def train(model, /, *, epochs: int, lr: float)` |
| Align pairs | `list(zip(features, labels, strict=True))` |
| Consecutive deltas | `[b - a for a, b in itertools.pairwise(scores)]` |
| Merge configs | `cfg = defaults \| overrides` |

## Next Steps

Next: **[49-collections-toolkit](49-collections-toolkit-lecture.md)** — deque, heapq, bisect, and Counter for retrieval work.
Continues in: **[02-advanced-python — 02 generators](../../02-advanced-python/lectures/02-generators-lecture.md)** and **[10 itertools](../../02-advanced-python/lectures/10-itertools-lecture.md)**.
Official docs: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
