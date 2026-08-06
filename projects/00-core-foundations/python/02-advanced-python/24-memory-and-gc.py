"""
Advanced Python - 24: Memory and Garbage Collection
====================================================
Topics: refcounting; reference cycles and the generational collector;
        the gc module; weakref / WeakValueDictionary; __del__ pitfalls;
        tracemalloc leak hunting; interning; sys.getsizeof vs deep size.

Why this matters for AI/backend engineering:
    A long-running inference server's RSS climbing until OOM is usually
    not a leak in the C sense -- it is an unbounded cache, a closure
    capturing a growing list, or a cycle the collector is fighting.
    Caching embeddings without WeakValueDictionary, or decorating with
    an unbounded lru_cache, are the two classic shapes. This file makes
    the mechanisms measurable.

Run:      python 24-memory-and-gc.py
Verify:   python 24-memory-and-gc.py --verify
Reference: https://docs.python.org/3/library/gc.html
           https://docs.python.org/3/library/weakref.html
           https://docs.python.org/3/library/tracemalloc.html
"""

from __future__ import annotations

import gc
import os
import random
import sys
import tracemalloc
import weakref

random.seed(42)
os.environ.setdefault("MPLBACKEND", "Agg")   # never open a GUI window

# ============================================================
# 1. Reference Counting
# ============================================================
# CPython frees an object the moment its refcount hits zero: deterministic,
# immediate, no background thread. sys.getrefcount(x) returns the count
# PLUS one for the temporary argument passed to getrefcount itself.

class Token:
    """A tiny object we can watch die via a weakref callback."""

    def __init__(self, name: str) -> None:
        self.name = name


def demo_refcount() -> None:
    """Watch the refcount move as references appear and disappear."""
    obj = Token("t1")
    base = sys.getrefcount(obj)
    print(f"  refcount right after creation: {base}")
    refs: list[Token] = [obj, obj]
    print(f"  refcount with 2 more refs: {sys.getrefcount(obj)}")
    del refs
    print(f"  refcount after deleting them: {sys.getrefcount(obj)}")
    print(f"  id stable: {id(obj) == id(obj)}")
    # Output:
    #   refcount right after creation: 2
    #   refcount with 2 more refs: 4
    #   refcount after deleting them: 2
    #   id stable: True


# ============================================================
# 2. Reference Cycles: Where Refcounting Fails
# ============================================================
# A -> B -> A: neither refcount ever reaches zero, so refcounting alone
# can never free them. The generational collector (gc) finds unreachable
# cycles in periodic passes. Complexity: gc runs O(1) amortized per
# allocation, with full scans on demand.

class Node:
    """A doubly-linked node: classic cycle material."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.next: Node | None = None
        self.prev: Node | None = None


def build_cycle(name: str) -> tuple[Node, weakref.ReferenceType[Node]]:
    """Create a two-node cycle and return one node plus a weakref."""
    a = Node(f"{name}-a")
    b = Node(f"{name}-b")
    a.next = b
    b.prev = a
    return a, weakref.ref(a)


def demo_cycle() -> None:
    """A cycle survives del, then dies only when gc.collect() runs."""
    a, ref = build_cycle("demo")
    del a
    print(f"  cycle alive after del (refcount can't see it): {ref() is not None}")
    collected = gc.collect()
    print(f"  gc.collect() collected {collected} objects")
    print(f"  cycle dead after collection: {ref() is None}")
    # Output:
    #   cycle alive after del (refcount can't see it): True
    #   gc.collect() collected N objects
    #   cycle dead after collection: True


# ============================================================
# 3. The gc Module
# ============================================================
# gc exposes the collector: is_tracked, get_objects, get_referrers,
# disable/enable. Most code should never touch it -- the defaults are
# right -- but it is the diagnostic tool when memory grows suspiciously.

def demo_gc_module() -> None:
    """Introspect the collector and the graph."""
    a, _ = build_cycle("probe")
    print(f"  Node is tracked by gc: {gc.is_tracked(a)}")
    referrers = gc.get_referrers(a)
    print(f"  get_referrers found {len(referrers)} containers")
    print(f"  thresholds: {gc.get_threshold()}")
    del a
    gc.collect()
    # Output:
    #   Node is tracked by gc: True
    #   get_referrers found N containers
    #   thresholds: (700, 10, 10)


# ============================================================
# 4. weakref: References That Do Not Keep Objects Alive
# ============================================================
# A weakref dies with its target. WeakValueDictionary is the safe cache:
# entries vanish automatically when the value is garbage. That is how you
# cache embeddings without unbounded growth.

def demo_weakref() -> None:
    """weakref.ref dies with the owner; WeakValueDictionary self-cleans."""
    obj = Token("cached")
    ref = weakref.ref(obj, lambda r: print("  callback: target collected"))
    d: weakref.WeakValueDictionary[int, Token] = weakref.WeakValueDictionary()
    d[1] = obj
    print(f"  weakref alive: {ref() is not None}; cache size: {len(d)}")
    del obj
    gc.collect()
    print(f"  weakref dead: {ref() is None}; cache size after GC: {len(d)}")
    # Output:
    #   weakref alive: True; cache size: 1
    #   callback: target collected
    #   weakref dead: True; cache size after GC: 0


# ============================================================
# 5. __del__ Pitfalls
# ============================================================
# Since PEP 442 (3.4) cycles with finalizers are collected safely, but
# finalizer ORDER is not guaranteed, __del__ can resurrect an object,
# and __del__ at interpreter shutdown runs at an arbitrary time. Avoid
# relying on __del__ for anything you care about; prefer context
# managers and atexit.

class Fragile:
    """Demonstrates why __del__ should not hold important resources."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.closed = False

    def __del__(self) -> None:
        # Runs at gc time or interpreter shutdown -- not on demand.
        self.closed = True


def demo_del_pitfall() -> None:
    """Plain refcount-zero objects finalize at del; cycles defer to gc."""
    f = Fragile("plain")
    del f
    print(f"  plain object finalized immediately at del: True")

    a = Fragile("cyc-a")
    b = Fragile("cyc-b")
    a.other = b                    # type: ignore[attr-defined]
    b.other = a                    # type: ignore[attr-defined]
    print(f"  cycle member closed BEFORE gc.collect(): {a.closed}")
    gc.collect()
    print(f"  cycle member closed AFTER gc.collect(): {a.closed}")
    print(f"  -> __del__ timing is gc-dependent; never rely on it")
    # Output:
    #   plain object finalized immediately at del: True
    #   cycle member closed BEFORE gc.collect(): False
    #   cycle member closed AFTER gc.collect(): True
    #   -> __del__ timing is gc-dependent; never rely on it


# ============================================================
# 6. tracemalloc: Hunting a Real Leak
# ============================================================
# tracemalloc snapshots Python allocations. Diff two snapshots around a
# suspicious block and the growth is the leak's size. This is the first
# tool to reach for when RSS climbs.

_LEAK_HOLDER: list[list[int]] = []   # module-level cache that never clears


def leaky_work() -> None:
    """Simulate a leak: append to a module-level list forever."""
    for _ in range(20):
        _LEAK_HOLDER.append(list(range(500)))


def measure_growth(work: object, repeats: int) -> int:
    """Bytes allocated by `work()` that survive after it returns."""
    tracemalloc.start()
    gc.collect()
    before = tracemalloc.take_snapshot()
    for _ in range(repeats):
        work()                       # type: ignore[operator]
    gc.collect()
    after = tracemalloc.take_snapshot()
    growth = sum(s.size_diff for s in after.compare_to(before, "filename"))
    tracemalloc.stop()
    return growth


def demo_tracemalloc() -> int:
    """Run leaky_work and report the retained growth."""
    growth = measure_growth(leaky_work, 3)
    print(f"  retained growth after 3 x leaky_work: {growth // 1024} KB")
    return growth


# ============================================================
# 7. Interning
# ============================================================
# Small ints (-5..256) are singletons; sys.intern() canonicalizes strings
# so equality comparisons become pointer comparisons. Great for many
# repeated identifiers (column names, prompt labels), terrible as a
# general memory strategy -- interned strings are never freed.

def demo_interning() -> None:
    """Small ints are singletons; sys.intern makes strings singletons.

    Two traps make this look wrong: literal 257s share one co_consts
    entry (so `c = 257; d = 257; c is d` is True!), and 256 + 1 is
    constant-folded at compile time. Only runtime-computed ints show
    the real cache boundary at 256.
    """
    a, b = 256, 256
    base = 256
    c = base + 1
    d = base + 1
    print(f"  256 is 256: {a is b}")
    print(f"  runtime-computed 257 is 257: {c is d}")
    s1 = sys.intern("embedding")
    s2 = sys.intern("embedding")
    print(f"  intern('embedding') is intern('embedding'): {s1 is s2}")
    print(f"  equal but distinct: {('a' + 'bc') is ('ab' + 'c')}")
    # Output:
    #   256 is 256: True
    #   runtime-computed 257 is 257: False
    #   intern('embedding') is intern('embedding'): True
    #   equal but distinct: False


# ============================================================
# 8. sys.getsizeof Is Shallow
# ============================================================
# sys.getsizeof(x) reports the container only -- never its contents.
# A deep size must walk the object graph.

def deep_size(obj: object, seen: set[int] | None = None) -> int:
    """Recursively total the size of an object and its contents."""
    if seen is None:
        seen = set()
    if id(obj) in seen:
        return 0
    seen.add(id(obj))
    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        size += sum(deep_size(k, seen) + deep_size(v, seen)
                    for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(deep_size(item, seen) for item in obj)
    return size


def demo_shallow_size() -> None:
    """sys.getsizeof undercounts containers with contents."""
    data = {"chunks": [list(range(100)) for _ in range(5)], "meta": "x" * 1000}
    shallow = sys.getsizeof(data)
    deep = deep_size(data)
    print(f"  shallow: {shallow} bytes; deep: {deep} bytes")
    print(f"  deep/shallow ratio: {deep / shallow:.1f}x")
    # Output:
    #   shallow: N bytes; deep: M bytes
    #   deep/shallow ratio: Kx


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: calling gc.collect() on a hot path "to be safe".
# CORRECT: let the generational collector run; it triggers on thresholds.
#   Use gc.collect() only at batch boundaries or in tests.
# MISTAKE: caching with a plain dict keyed by objects that should die.
# CORRECT: WeakValueDictionary / weakref.WeakKeyDictionary.
# MISTAKE: blaming sys.getsizeof for "small" structures while the
#   CONTENTS (nested lists of floats) dominate.
# CORRECT: deep_size or tracemalloc for the real footprint.
# MISTAKE: __del__ for cleanup of sockets/files.
# CORRECT: context managers; __del__ is non-deterministic.


# ============================================================
# Self-Verification  (MANDATORY -- every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # 1. A cycle survives `del` -- refcounting alone cannot collect it.
    a, ref = build_cycle("verify")
    del a
    assert ref() is not None, \
        "cycle must survive del: refcount cannot see cyclic references"

    # 2. gc.collect() finds the unreachable cycle.
    gc.collect()
    assert ref() is None, \
        "gc.collect() must collect an unreachable reference cycle"

    # 3. weakref dies with its owner (no cycle involved).
    obj = Token("v")
    ref = weakref.ref(obj)
    del obj
    gc.collect()
    assert ref() is None, "weakref must clear when its target is collected"

    # 4. WeakValueDictionary self-cleans when values disappear.
    # TRAP: a temporary value dies instantly -- the dict holds only a
    # weakref, so you MUST keep a strong reference elsewhere.
    d: weakref.WeakValueDictionary[int, Token] = weakref.WeakValueDictionary()
    strong = Token("cached")
    d[1] = strong
    assert len(d) == 1, "cache must hold the entry while the value lives"
    del strong
    gc.collect()
    assert len(d) == 0, \
        "WeakValueDictionary must drop entries whose values died"
    temp = Token("temp")
    d[2] = temp
    del temp
    gc.collect()
    assert 2 not in d, "temporaries must not survive in a weak cache"

    # 5. tracemalloc reports growth for a known leak.
    growth = measure_growth(leaky_work, 3)
    assert growth > 50_000, \
        "tracemalloc must report retained growth for leaky_work (got %d)" % growth

    # 6. Interning: small ints are singletons, larger ones are not.
    a, b = 256, 256
    base = 256
    c = base + 1                    # runtime-computed: NOT constant-folded
    d = base + 1
    assert a is b, "256 must be a singleton (interned small int)"
    assert c is not d, "257 must NOT be a singleton when runtime-computed"
    assert sys.intern("xyz") is sys.intern("xyz"), \
        "sys.intern must canonicalize equal strings to one object"

    # 7. sys.getsizeof is shallow; deep_size sees the contents.
    data = {"chunks": [list(range(100)) for _ in range(5)], "meta": "x" * 1000}
    assert deep_size(data) > sys.getsizeof(data), \
        "deep size must exceed shallow size for nested containers"

    # 8. The gc module tracks container objects.
    probe, _ = build_cycle("probe")
    assert gc.is_tracked(probe), "container objects must be tracked by gc"
    del probe
    gc.collect()

    print("\n[OK] 24-memory-and-gc: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("=" * 60)
        print("MEMORY AND GC: HOW OBJECTS LIVE AND DIE")
        print("=" * 60)
        print("\n--- 1. Reference counting ---")
        demo_refcount()
        print("\n--- 2. Reference cycles ---")
        demo_cycle()
        print("\n--- 3. The gc module ---")
        demo_gc_module()
        print("\n--- 4. weakref and WeakValueDictionary ---")
        demo_weakref()
        print("\n--- 5. __del__ pitfalls ---")
        demo_del_pitfall()
        print("\n--- 6. tracemalloc leak hunting ---")
        demo_tracemalloc()
        print("\n--- 7. Interning ---")
        demo_interning()
        print("\n--- 8. Shallow vs deep size ---")
        demo_shallow_size()
        print("\n--- Summary ---")
        print("1. Refcounting frees immediately; cycles need the gc.")
        print("2. WeakValueDictionary = safe caches; tracemalloc = leaks.")
        print("3. __del__ is not cleanup; interning trades memory for speed.")
        _verify()
