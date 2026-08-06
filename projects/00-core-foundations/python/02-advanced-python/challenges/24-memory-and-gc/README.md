# Challenge 24: Memory Management and GC

Make memory visible: collect cycles, size instances honestly (dict
included), and prove the weak-cache trap with a tracer.

## 🥉 Bronze — Cycle Collection (~15 min)

**Task:** Implement `collect_cycle(n)`: build `n` `Node` objects wired
into a cycle (`node[i].peer = node[i + 1]`, last wraps to first), drop
all references, force `gc.collect()`, and return the number of objects
the collector freed.

**Signature:**
```python
def collect_cycle(n: int) -> int:
```

| Input | Expected |
|---|---|
| `2` | `2` |
| `5` | `5` |
| `1` | `1` (self-cycle also counts) |

**Constraints:** refcounts alone cannot free a cycle — the answer must
be exactly `n`. Count before/after with `gc.get_objects()` filtered by
`Node` type (or a `__del__`-style counter); `del` the roots first.

---

## 🥈 Silver — Honest Instance Sizing (~35 min)

**Task:** Implement `slots_ratio(n)`: build `n` instances of a plain
class and `n` of a slotted class with the same two fields; measure each
list **including `__dict__` sizes** (`sys.getsizeof(inst)` +
`sys.getsizeof(inst.__dict__)` where it exists); return
`plain_total / slotted_total`.

**Signature:**
```python
def slots_ratio(n: int) -> float:
```

| Input | Expected |
|---|---|
| `10_000` | `>= 1.5` (measured ~2.8 on CPython) |

**Constraints:** on Python 3.13 `sys.getsizeof(instance)` is **48 bytes
for both classes** — measuring without `__dict__` returns ~1.0 and
fails. Include the dict, and the ratio proves `__slots__` at scale.

---

## 🥇 Gold — Weak Cache Trap + Leak Tracer (~75 min)

**Task:** implement three functions.

1. `weak_cache_trap()` — a `WeakValueDictionary`: insert a temporary
   `Entry` (trap: evicted instantly), insert an `Entry` held by a
   strong reference, then delete the strong reference. Return
   `(trap_len, alive_len, after_del_len)` — expected `(0, 1, 0)`.
2. `sum_materialized(n)` — `(total, peak)` where peak is the
   `tracemalloc` peak for building `[i for i in range(n)]` and summing.
3. `sum_streamed(n)` — `(total, peak)` for the same sum computed with a
   generator / `range` directly (no materialized list).

**Signatures:**
```python
def weak_cache_trap() -> tuple[int, int, int]
def sum_materialized(n: int) -> tuple[int, int]
def sum_streamed(n: int) -> tuple[int, int]
```

| Call | Expected |
|---|---|
| `weak_cache_trap()` | `(0, 1, 0)` |
| `sum_materialized(100_000)[0]` | `sum_streamed(100_000)[0]` (equal) |
| `sum_materialized(100_000)[1]` | `>= sum_streamed(100_000)[1] * 10` |

**Constraints:** the tracer must run **inside** each function
(`tracemalloc.start()` … `stop()`, returning `get_traced_memory()[1]`
as peak). The naive "cache without an owner" returns a non-zero first
value; materializing instead of streaming blows the peak ratio.

---

## Running

```bash
pytest challenges/24-memory-and-gc/test_challenge.py -v
```

Tests default to **starter.py** (must fail). To verify the reference
implementation:

```bash
# PowerShell
$env:CHALLENGE_MODULE = "solution"
pytest challenges/24-memory-and-gc/test_challenge.py -v
```

## Test File Structure

```
challenges/24-memory-and-gc/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
