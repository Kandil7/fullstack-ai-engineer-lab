"""
01-core-python — 43: dataclasses & NamedTuples
==============================================
Topics: @dataclass, field(default_factory=...), frozen=True, order=True,
        slots=True (3.10+), __post_init__, NamedTuple, TypedDict,
        comparison table dict vs dataclass vs NamedTuple vs class

Why this matters for AI/backend engineering:
    Config objects, a RetrievedChunk(text, score, source) record,
    model hyperparameters. slots=True matters at a million records.

Run:      python 43-dataclasses-and-namedtuples.py
Verify:   python 43-dataclasses-and-namedtuples.py --verify
Reference: https://docs.python.org/3/library/dataclasses.html
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field, fields
from typing import NamedTuple, TypedDict
from collections import namedtuple

# ============================================================
# 1. Basic @dataclass
# ============================================================
# Complexity: O(1) construction, O(n) field access where n = fields

# Example 1: Minimal dataclass
@dataclass
class Config:
    model_name: str
    learning_rate: float
    batch_size: int = 32

cfg = Config("bert-base", 2e-5)
print(f"Config: {cfg}")
print(f"  model_name: {cfg.model_name}")
print(f"  lr: {cfg.learning_rate}")
print(f"  batch_size: {cfg.batch_size}")  # default used

# Example 2: field() with default_factory for mutable defaults
@dataclass
class ModelConfig:
    name: str
    tags: list[str] = field(default_factory=list)  # Each instance gets own list
    metadata: dict = field(default_factory=dict)

m1 = ModelConfig("bert")
m2 = ModelConfig("gpt")
m1.tags.append("nlp")
print(f"\nm1.tags: {m1.tags}")  # ["nlp"]
print(f"m2.tags: {m2.tags}")  # [] — separate list!

# ============================================================
# 2. Advanced dataclass Features
# ============================================================

# Example 3: frozen=True (immutable, hashable)
@dataclass(frozen=True)
class FrozenConfig:
    model: str
    version: int

fc = FrozenConfig("bert", 1)
print(f"\nFrozen: {fc}")
# fc.model = "gpt"  # Raises FrozenInstanceError

# Hashable — can use as dict key
config_registry = {fc: "registered"}
print(f"Used as dict key: {config_registry[fc]}")

# Example 4: order=True (auto-generates comparison methods)
@dataclass(order=True)
class PrioritizedTask:
    priority: int
    name: str = field(compare=False)  # Excluded from comparison

tasks = [
    PrioritizedTask(3, "low"),
    PrioritizedTask(1, "high"),
    PrioritizedTask(2, "medium"),
]
tasks.sort()
print(f"\nSorted by priority: {[t.name for t in tasks]}")  # high, medium, low

# Example 5: slots=True (Python 3.10+) — memory optimization
@dataclass(slots=True)
class SlottedConfig:
    model: str
    lr: float
    epochs: int

sc = SlottedConfig("bert", 2e-5, 10)
print(f"\nSlotted: {sc}")
print(f"Has __dict__: {hasattr(sc, '__dict__')}")  # False — saves memory!
# sc.new_attr = "x"  # Raises AttributeError

# ============================================================
# 3. __post_init__ for Computed Fields
# ============================================================

@dataclass
class TrainingConfig:
    model_name: str
    lr: float
    batch_size: int
    num_gpus: int
    effective_batch_size: int = field(init=False)  # Computed

    def __post_init__(self):
        self.effective_batch_size = self.batch_size * self.num_gpus

tc = TrainingConfig("bert", 2e-5, 32, 4)
print(f"\nEffective batch size: {tc.effective_batch_size}")  # 128

# ============================================================
# 4. NamedTuple — Lightweight Immutable Records
# ============================================================

class RetrievedChunk(NamedTuple):
    text: str
    score: float
    source: str
    doc_id: int

chunk = RetrievedChunk("The cat sat...", 0.95, "wiki", 42)
print(f"\nNamedTuple: {chunk}")
print(f"  text: {chunk.text}")
print(f"  score: {chunk.score}")
print(f"  Index access: {chunk[1]}")  # 0.95

# NamedTuple with defaults (Python 3.7+)
class ChunkWithDefaults(NamedTuple):
    text: str
    score: float = 0.0
    source: str = "unknown"

cwd = ChunkWithDefaults("hello")
print(f"With defaults: {cwd}")  # score=0.0, source="unknown"

# ============================================================
# 5. TypedDict — Structural Typing for Dicts
# ============================================================

class ModelHyperparams(TypedDict):
    lr: float
    batch_size: int
    epochs: int
    optimizer: str  # Required
    weight_decay: float  # Required

# Total=True (default) — all keys required
hp1: ModelHyperparams = {
    "lr": 2e-5,
    "batch_size": 32,
    "epochs": 10,
    "optimizer": "adamw",
    "weight_decay": 0.01,
}

# Partial TypedDict
class OptionalParams(TypedDict, total=False):
    lr: float
    scheduler: str

hp2: OptionalParams = {"scheduler": "cosine"}  # Valid

print(f"\nTypedDict: {hp1}")

# ============================================================
# 6. Comparison Table: Dict vs Dataclass vs NamedTuple vs Class
# ============================================================

print("\n" + "=" * 60)
print("COMPARISON: Dict vs Dataclass vs NamedTuple vs Class")
print("=" * 60)

print("""
| Feature              | dict      | @dataclass    | NamedTuple   | class       |
|----------------------|-----------|---------------|--------------|-------------|
| Syntax               | {}        | @dataclass    | class X(N...)| class X:    |
| Type hints           | Optional  | Required      | Required     | Optional    |
| Defaults             | .get()    | field()       | Class attr   | __init__    |
| Mutability           | Mutable   | Mutable*      | Immutable    | Mutable     |
| Hashable             | No        | frozen=True   | Yes          | Manual      |
| Memory (slots)       | High      | slots=True**  | Low          | Manual      |
| IDE support          | Weak      | Excellent     | Good         | Good        |
| Validation           | Manual    | __post_init__ | Manual       | __init__    |
| Pattern matching     | 3.10+     | 3.10+         | 3.10+        | 3.10+       |
| Performance (create) | Fast      | Fast**        | Fastest      | Fast        |
| Performance (access) | Dict lookup | Attr access | Attr/Index   | Attr access |

* frozen=True makes immutable
** Python 3.10+
""")

# ============================================================
# 7. Practical AI Example: Retrieval Result
# ============================================================

@dataclass(frozen=True, slots=True)
class RetrievalResult:
    """Immutable, memory-efficient retrieval result."""
    text: str
    score: float
    doc_id: int
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "score": self.score,
            "doc_id": self.doc_id,
            "metadata": self.metadata,
        }

results = [
    RetrievalResult("The cat sat...", 0.98, 1, {"source": "wiki"}),
    RetrievalResult("A dog ran...", 0.87, 2, {"source": "news"}),
]

print("\nRetrieval results:")
for r in results:
    print(f"  [{r.score:.2f}] {r.text[:20]}... (doc {r.doc_id})")

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: Mutable default without default_factory
#   @dataclass
#   class Bad:
#       tags: list = []  # SHARED across all instances!
# CORRECT:
#   @dataclass
#   class Good:
#       tags: list = field(default_factory=list)

# MISTAKE: Forgetting field() for defaults with mutable types
#   @dataclass
#   class Bad:
#       config: dict = {}  # Shared!
# CORRECT:
#   @dataclass
#   class Good:
#       config: dict = field(default_factory=dict)

# MISTAKE: Using class instead of dataclass for simple data
#   class Config:
#       def __init__(self, lr, batch):
#           self.lr = lr
#           self.batch = batch
# CORRECT (less boilerplate):
#   @dataclass
#   class Config:
#       lr: float
#       batch: int

# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    
    # Basic dataclass
    @dataclass
    class C:
        a: int
        b: str = "default"
    c = C(1)
    assert c.a == 1 and c.b == "default"
    
    # default_factory gives distinct objects
    @dataclass
    class D:
        items: list = field(default_factory=list)
    d1 = D()
    d2 = D()
    d1.items.append(1)
    assert d1.items == [1] and d2.items == []
    
    # frozen raises on mutation
    @dataclass(frozen=True)
    class F:
        x: int
    f = F(1)
    try:
        f.x = 2
        assert False, "Should have raised FrozenInstanceError"
    except Exception as e:
        assert "FrozenInstanceError" in type(e).__name__
    
    # frozen is hashable
    assert hash(f) == hash(F(1))
    
    # order=True enables comparison
    @dataclass(order=True)
    class O:
        priority: int
        name: str = field(compare=False)
    assert O(1, "a") < O(2, "b")
    
    # slots=True blocks __dict__ (3.10+)
    @dataclass(slots=True)
    class S:
        x: int
    s = S(1)
    assert not hasattr(s, '__dict__')
    try:
        s.y = 2
        assert False, "Should have raised AttributeError"
    except AttributeError:
        pass
    
    # __post_init__ runs after init
    @dataclass
    class P:
        x: int
        doubled: int = field(init=False)
        def __post_init__(self):
            self.doubled = self.x * 2
    p = P(5)
    assert p.doubled == 10
    
    # NamedTuple
    class NT(NamedTuple):
        a: int
        b: str
    nt = NT(1, "x")
    assert nt.a == 1 and nt[0] == 1 and nt.b == "x"
    
    # TypedDict
    class TD(TypedDict):
        x: int
    td: TD = {"x": 1}
    assert td["x"] == 1
    
    # slots blocks arbitrary attributes
    @dataclass(slots=True)
    class SL:
        x: int
    sl = SL(1)
    try:
        sl.new_attr = 5
        assert False
    except AttributeError:
        pass
    
    print("[OK] 43-dataclasses-and-namedtuples: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. @dataclass reduces boilerplate for data containers")
        print("2. field(default_factory=...) for mutable defaults")
        print("3. frozen=True for immutability + hashability")
        print("3. order=True for auto-comparison methods")
        print("4. slots=True (3.10+) for memory efficiency")
        print("5. __post_init__ for computed fields")
        print("6. NamedTuple for lightweight immutable records")
        print("7. TypedDict for structural dict typing")
        print("8. Use frozen + slots for high-volume immutable records")
        _verify()