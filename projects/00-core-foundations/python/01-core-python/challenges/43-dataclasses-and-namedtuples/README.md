# Challenge 43: Dataclasses & NamedTuples

## 🥉 Bronze — Frozen Point (~15 min)

**Task:** Implement a frozen dataclass `Point(x: float, y: float)` whose
`__post_init__` rejects non-finite values (NaN or infinity).

**Signature:**
```python
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Point:
    x: float
    y: float
    def __post_init__(self) -> None:
        ...
```

| Input | Expected |
|-------|----------|
| `Point(1.0, 2.0)` | constructs fine |
| `Point(float("nan"), 0.0)` | raises `ValueError` |
| `Point(1.0, float("inf"))` | raises `ValueError` |
| `Point(1, 2).x = 5` | raises `FrozenInstanceError` |

**Constraints:** n ≤ 10^3. Any correct approach passes.

---

## 🥈 Silver — Ranked Hits (~35 min)

**Task:** Implement `rank_hits(hits: list[tuple[str, float]]) -> list[str]`
using a dataclass with `order=True` so ties break by doc id ascending, then
score descending.

**Signature:**
```python
@dataclass(order=True)
class Hit:
    score: float
    doc: str

def rank_hits(hits: list[tuple[str, float]]) -> list[str]: ...
```

| Input | Expected |
|-------|----------|
| `[("b", 0.5), ("a", 0.9), ("c", 0.5)]` | `["a", "b", "c"]` |

**Constraints:** n ≤ 10^5. An O(n²) comparison loop will time out — use the
dataclass ordering.

---

## 🥇 Gold — Slots Record Store (~75 min)

**Task:** Implement a memory-conscious record store: `RecordStore` backed by a
list of `@dataclass(slots=True)` records with `frozen=True` and
`__post_init__` validation. Records are `Embedding(id: str, vector: tuple[float, ...])`
with `len(vector) == dim` enforced. Add `top_k(k: int) -> list[Embedding]` via
`heapq.nlargest`.

**Signature:**
```python
class RecordStore:
    def __init__(self, dim: int) -> None: ...
    def add(self, id: str, vector: tuple[float, ...]) -> None: ...
    def top_k(self, k: int) -> list["Embedding"]: ...
```

**Constraints:** 10^6 records, memory ≤ 80 MB total. Must be single-pass and
use slots. (A plain-class version with `__dict__` will exceed the budget.)

**Follow-up:** what breaks first at 10^9 records? (Answer: RAM; the store must
move to disk/a vector DB.)

---

## Running

```bash
pytest challenges/43-dataclasses-and-namedtuples/test_challenge.py -v
```
