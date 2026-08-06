# 48: Comprehensions & Modern Syntax — Glossary

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| `f"{x=}"` | Syntax | Prints expression name, `=`, and value for debugging |
| `\|` merge | Operator | Non-mutating dict merge; right operand wins (3.9+) |
| `\|=` update | Operator | In-place dict merge |
| comprehension | Expression | `[expr for x in it if cond]` — build a collection inline |
| dict comprehension | Expression | `{k: v for x in it}` — build a dict inline |
| generator expression | Expression | `(expr for x in it)` — lazy, O(1) memory, single-pass |
| keyword-only | Parameter | After `*` — must be passed by name |
| `pairwise` | Function | `itertools.pairwise` — consecutive pairs (3.10+) |
| positional-only | Parameter | Before `/` — cannot be passed by name |
| `removeprefix` | Method | Removes a leading string, else returns unchanged (3.9+) |
| `removesuffix` | Method | Removes a trailing string, else returns unchanged (3.9+) |
| set comprehension | Expression | `{expr for x in it}` — builds a set, dedupes |
| `strict=True` | Parameter | `zip(strict=True)` raises on length mismatch (3.10+) |
| walrus `:=` | Operator | Assigns a name inside an expression |
| filter clause | Syntax | The trailing `if cond` of a comprehension |
| transform | Pattern | Mapping each element to a new value |

## Detailed Definitions

### comprehension
**Definition**: An expression that builds a list, dict, or set from an
iterable, combining a transform expression with `for`-clauses and optional
filters. It replaces the loop-and-append idiom with a single readable
expression.

**Example**:
```python
squares = [x * x for x in range(5)]
print(squares)  # [0, 1, 4, 9, 16]
```

**Complexity**: O(n) time, O(n) space for the result.

**Related**: dict comprehension, set comprehension, generator expression

### dict comprehension
**Definition**: A comprehension in `{key: value for ...}` form that builds a
dictionary. The classic use is building vocabularies: `{token: id for id,
token in enumerate(...)}`.

**Example**:
```python
words = ["cat", "dog", "cat"]
vocab = {w: i for i, w in enumerate(sorted(set(words)))}
print(vocab)  # {'cat': 0, 'dog': 1}
```

**Complexity**: O(n) time, O(n) space.

**Related**: comprehension, set comprehension

### `f"{x=}"`
**Definition**: An f-string specifier that prints `name=value` for the named
variable — `f"{lr=}"` produces `lr=0.0003`. The fastest debugging print for
a pipeline, since it writes the name for you.

**Example**:
```python
lr = 3e-4
print(f"{lr=}")  # lr=0.0003
```

**Complexity**: O(len(value)) to format.

**Related**: f-strings, `removeprefix`

### filter clause
**Definition**: The optional trailing `if cond` in a comprehension that
keeps only elements satisfying the condition. It binds to the nearest
`for`-clause.

**Example**:
```python
nums = [1, 2, 3, 4]
evens = [n for n in nums if n % 2 == 0]
print(evens)  # [2, 4]
```

**Complexity**: O(n).

**Related**: comprehension, transform

### generator expression
**Definition**: A comprehension written with parentheses instead of
brackets. It produces values lazily, one at a time, with O(1) memory — at
the cost of being single-pass and non-indexable.

**Example**:
```python
total = sum(x * x for x in range(10))
print(total)  # 285
```

**Complexity**: O(1) to create; O(n) total to iterate; O(1) working memory.

**Related**: comprehension, `pairwise`

### keyword-only
**Definition**: Parameters declared after a bare `*` in the signature. They
must be passed by name, which prevents positional-order mistakes in
calls like `train(model, 10, 1e-4)`.

**Example**:
```python
def train(model, *, epochs: int, lr: float) -> str:
    return f"{model} {epochs} {lr}"

print(train("bert", epochs=3, lr=1e-4))  # bert 3 0.0001
```

**Complexity**: O(1) at call time.

**Related**: positional-only

### `pairwise`
**Definition**: `itertools.pairwise(iterable)` yields consecutive pairs
`(x0, x1), (x1, x2), ...` in O(n) time with O(1) extra memory. The basis
for deltas, sliding windows of size 2, and transition counts.

**Example**:
```python
import itertools
print(list(itertools.pairwise([1, 3, 6])))  # [(1, 3), (3, 6)]
```

**Complexity**: O(n) time, O(1) extra space.

**Related**: generator expression, `strict=True`

### positional-only
**Definition**: Parameters declared before a bare `/` in the signature.
They cannot be passed by name, so the API owns the names and callers cannot
accidentally reorder keyword arguments.

**Example**:
```python
def mul(a, b, /):
    return a * b

print(mul(2, 3))      # 6
print(mul(a=2, b=3))  # TypeError: got some positional-only arguments
```

**Complexity**: O(1) at call time.

**Related**: keyword-only

### `removeprefix`
**Definition**: `str.removeprefix(prefix)` returns the string with the
prefix removed, or the string unchanged when the prefix does not match.
Safer than slice-by-length because it never mis-slices a non-matching
string.

**Example**:
```python
print("s3://bucket/k".removeprefix("s3://"))  # bucket/k
print("https://x".removeprefix("s3://"))      # https://x (unchanged)
```

**Complexity**: O(len(s)).

**Related**: `removesuffix`, `f"{x=}"`

### `removesuffix`
**Definition**: `str.removesuffix(suffix)` returns the string with the
trailing suffix removed, or unchanged when it does not match. The standard
way to strip a file extension you know is present.

**Example**:
```python
print("model_v3.pt".removesuffix(".pt"))  # model_v3
print("model_v3".removesuffix(".pt"))     # model_v3 (unchanged)
```

**Complexity**: O(len(s)).

**Related**: `removeprefix`

### set comprehension
**Definition**: A comprehension in `{expr for ...}` form that builds a set,
automatically deduplicating values. Useful for unique vocabularies, tag
sets, and distinct-value extraction.

**Example**:
```python
texts = ["cat", "dog", "cat"]
print({t[0] for t in texts})  # {'d', 'c'}
```

**Complexity**: O(n) time, O(n) space.

**Related**: comprehension, dict comprehension

### `strict=True`
**Definition**: The `zip(strict=True)` flag (3.10+) that raises `ValueError`
when the iterables have different lengths, instead of silently truncating
to the shortest. The guard for paired training data.

**Example**:
```python
inputs = [1, 2, 3]
labels = [1, 2]
try:
    list(zip(inputs, labels, strict=True))
except ValueError as e:
    print("drift caught")
```

**Complexity**: O(n) time, O(n) space for the list.

**Related**: `pairwise`, transform

### transform
**Definition**: The mapping part of a comprehension — the expression
evaluated for every element, e.g. `t.upper()` in `[t.upper() for t in ...]`.
Transforms may reuse the loop variable or ignore it entirely.

**Example**:
```python
tokens = ["a", "b"]
print([t.upper() for t in tokens])  # ['A', 'B']
```

**Complexity**: O(n * cost(transform)).

**Related**: comprehension, filter clause

### walrus `:=`
**Definition**: The assignment expression operator: assigns a name inside
an enclosing expression. Used to compute once and use twice — typically a
parse or lookup in a condition that the body then reuses.

**Example**:
```python
values = ["3.14", "x", "2.5"]
valid = [v for v in values if (parsed := float(v)) is not None]
print(valid)  # ['3.14', '2.5']
```

**Complexity**: O(1) per assignment; saves a duplicated O(cost) call.

**Related**: comprehension, filter clause

### `|` merge
**Definition**: `a | b` returns a new dict containing both, with `b`
winning on duplicate keys; neither operand is mutated. The readable
replacement for `{**a, **b}`.

**Example**:
```python
defaults = {"lr": 1e-3, "seed": 0}
overrides = {"lr": 1e-4}
print(defaults | overrides)  # {'lr': 1e-04, 'seed': 0}
```

**Complexity**: O(len(a) + len(b)) time and space.

**Related**: `|=` update

### `|=` update
**Definition**: In-place dict merge: `a |= b` updates `a` with `b`'s keys,
mutating `a` instead of copying. Choose it when the base dict is disposable.

**Example**:
```python
cfg = {"lr": 1e-3, "seed": 0}
cfg |= {"lr": 1e-4, "epochs": 10}
print(cfg)  # {'lr': 1e-04, 'seed': 0, 'epochs': 10}
```

**Complexity**: O(len(b)) time, O(1) extra space (reuses `a`).

**Related**: `|` merge

## Key Concepts Summary

### Read the Comprehension Like a Loop
- Clauses run left to right: `[x for a in A for b in B if cond]` equals the
  nested-loop form with the same order.
- The `if` filter binds to the nearest `for`-clause.
- Keep it to one or two clauses; beyond that, extract a function.

### List vs Generator
- **List**: materialized, indexable, reusable — O(n) memory.
- **Generator**: lazy, single-pass, O(1) memory — stream when you can.

### Modern-Syntax Guardrails
- `zip(strict=True)` turns silent misalignment into a loud error.
- `/` and `*` lock argument order in public APIs.
- `removeprefix`/`removesuffix` replace error-prone slicing.
- `\|` and `\|=` replace `{**a, **b}` and `a.update(b)`.

### Walrus Rule
Use `:=` when it removes a doubled computation (parse-then-test, read-then-
test). Skip it when a plain assignment is just as clear.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. generator expression — ___
2. walrus `:=` — ___
3. `zip(strict=True)` — ___
4. positional-only — ___
5. `pairwise` — ___
6. `f"{x=}"` — ___
7. set comprehension — ___
8. `removeprefix` — ___
9. `\|` merge — ___
10. filter clause — ___

A. Parameters before `/` — cannot be passed by name
B. Lazy comprehension with O(1) memory, single-pass
C. Assigns a name inside an expression
D. Trailing `if cond` in a comprehension
E. Raises on length mismatch instead of truncating
F. Consecutive pairs from an iterable
G. Builds a deduplicated collection
H. Prints name=value for debugging
I. Non-mutating dict merge, right operand wins
J. Removes a leading string or returns unchanged

**Answers:** 1-B, 2-C, 3-E, 4-A, 5-F, 6-H, 7-G, 8-J, 9-I, 10-D
