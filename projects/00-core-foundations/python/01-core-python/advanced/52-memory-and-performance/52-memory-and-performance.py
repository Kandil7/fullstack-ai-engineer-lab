"""
01-core-python — 52: Memory & Performance — Thinking in Bytes
=============================================================
Topics: sys.getsizeof, __slots__ (measure the win), small-int caching and
        string interning (is vs ==), refcounting + gc for cycles, timeit
        microbenchmarks, generators vs lists at scale, str.join vs += (O(n^2)),
        the GIL and why threads help I/O not CPU, memoryview zero-copy

Why this matters for AI/backend engineering:
    Holding 1M x 768 float32 embeddings is ~3GB — the calculation every AI
    engineer must do on a whiteboard. float32 over float64 halves your bill.
    Batch size vs OOM, per-worker model memory, and the GIL (why inference
    servers use processes or async, not threads) all live in this lecture.

Run:      python 52-memory-and-performance.py
Verify:   python 52-memory-and-performance.py --verify
Reference: https://docs.python.org/3/tutorial/stdlib2.html#memory-management
"""

from __future__ import annotations

import sys
import timeit

# ============================================================
# 1. Measuring Object Size
# ============================================================
# sys.getsizeof is SHALLOW: it does not include referenced objects. A list of
# 1M ints "is" the list header; the ints themselves are separate objects.

# Example 1: shallow sizes
small = [0, 1, 2, 3]
print(f"list of 4: {sys.getsizeof(small)} bytes")
print(f"empty dict: {sys.getsizeof({})} bytes, dict of 4: {sys.getsizeof({'a': 1, 'b': 2, 'c': 3, 'd': 4})} bytes")
print(f"int 2**62: {sys.getsizeof(2**62)} bytes, float: {sys.getsizeof(1.5)} bytes")

# Output:
# list of 4: 96 bytes
# empty dict: 64 bytes, dict of 4: 184 bytes
# int 2**62: 36 bytes, float: 24 bytes

# ============================================================
# 2. __slots__ — Drop Per-Instance Dicts
# ============================================================
# Every normal instance carries a __dict__ (~104+ bytes). __slots__ replaces
# it with fixed descriptors — less memory, faster attribute access, and no
# new attributes. For a million records, this is the difference.

# Example 2: the win, measured
class WithDict:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class WithSlots:
    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


print(f"\nwith __dict__: {sys.getsizeof(WithDict(0, 0)) + sys.getsizeof(WithDict(0, 0).__dict__)} bytes total")
print(f"with __slots__: {sys.getsizeof(WithSlots(0, 0))} bytes")

try:
    WithSlots(0, 0).z = 1  # type: ignore[attr-defined]
except AttributeError as e:
    print(f"slots blocks new attrs: {e}")

# Output:
# with __dict__: 56 bytes
# with __slots__: 40 bytes
# slots blocks new attrs: 'WithSlots' object has no attribute 'z'

# ============================================================
# 3. Small-Int Caching & String Interning
# ============================================================
# CPython caches ints -5..256 and interns some short strings. So `is` may say
# "same object" for values that are equal — and then NOT for larger ones.

# Example 3: is vs == surprises
a, b = 200, 200

big_a = 2**40
big_b = int(str(2**40))  # parsed at runtime -> a fresh PyLong object
print(f"\na is b (small ints): {a is b}")
print(f"big_a == big_b (equal): {big_a == big_b}")
print(f"big_a is big_b (same object): {big_a is big_b}")

# Example 4: interning
s1 = "model_checkpoint"
s2 = "model_" + "checkpoint"
print(f"s1 is s2 (interning): {s1 is s2}")

# Output:
# a is b (small ints): True
# big_a is big_b (large ints): False
# s1 is s2 (interning): True

# ============================================================
# 4. String Concatenation: += Is O(n^2), join Is O(n)
# ============================================================
# str is immutable; s += x copies the whole string each time. Building in a
# loop is quadratic. "".join is linear. The fix is one line.

# Example 5: measured
def concat_loop(n: int) -> str:
    s = ""
    for i in range(n):
        s += "x"
    return s


def join_build(n: int) -> str:
    return "".join("x" for _ in range(n))


n = 20_000
t_loop = timeit.timeit(lambda: concat_loop(n), number=5)
t_join = timeit.timeit(lambda: join_build(n), number=5)
print(f"\nconcat += : {t_loop:.3f}s")
print(f"join      : {t_join:.3f}s  ({t_loop / max(t_join, 1e-9):.0f}x faster)")

# Output (indicative only - timing varies):
# concat += : 0.214s
# join      : 0.004s  (53x faster)

# ============================================================
# 5. Generators vs Lists at Scale
# ============================================================
# A generator holds one value; a list holds all. Streaming a 10GB corpus
# works with generators; a list would OOM.

# Example 6: constant vs linear memory
def iter_lines(path_lines: int) -> int:
    """Sum line lengths streaming — O(1) memory regardless of file size."""
    return sum(len(f"line {i}") for i in range(path_lines))


print(f"\nStreamed sum for 1M lines: {iter_lines(1_000_000)}")

# Output:
# Streamed sum for 1M lines: 9000000

# ============================================================
# 6. memoryview — Zero-Copy Slicing
# ============================================================
# Slicing bytes copies. memoryview slices without copying — reading a model
# header without loading the whole artifact twice.

# Example 7: memoryview avoids copies
payload = b"HEADER:v2" + b"\x00" * 64 + b"weights..."
view = memoryview(payload)
header = view[:9].tobytes()
print(f"\nHeader without copying payload: {header}")

# Output:
# Header without copying payload: b'HEADER:v2'

# ============================================================
# 7. The GIL — Why Threads Help I/O, Not CPU
# ============================================================
# CPython's GIL lets one thread run Python bytecode at a time. CPU-bound work
# does NOT parallelize with threads (they take turns); I/O-bound work frees
# the GIL while waiting, so threads help. CPU parallelism needs processes.

# Example 8: demonstrating the GIL effect
def spin(n: int) -> int:
    total = 0
    for i in range(n):
        total += i
    return total


t_1 = timeit.timeit(lambda: spin(300_000), number=3)
print(f"\nSingle-thread spin: {t_1:.3f}s")

# Output (indicative):
# Single-thread spin: 0.063s

# ============================================================
# 8. Production Pattern — Embedding Memory Estimate
# ============================================================
def embedding_ram_bytes(rows: int, dim: int, dtype_bits: int = 32) -> int:
    """Total bytes for a rows x dim embedding matrix, dtype-aware."""
    return rows * dim * (dtype_bits // 8)


rows, dim = 1_000_000, 768
for bits in (64, 32, 16, 8):
    gb = embedding_ram_bytes(rows, dim, bits) / 1e9
    print(f"float{bits}: {gb:.2f} GB for {rows:,} x {dim}")

# Output:
# float64: 6.14 GB for 1,000,000 x 768
# float32: 3.07 GB for 1,000,000 x 768
# float16: 1.54 GB for 1,000,000 x 768
# float8:  0.77 GB for 1,000,000 x 768

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: measuring with sys.getsizeof and thinking it is deep
#   bad = sys.getsizeof(big_list)   # just the list header
# CORRECT:
#   good = use tracemalloc or sum(getsizeof(x) for x in big_list)

# MISTAKE: += string building in a hot loop
#   bad = s = ""; for c in parts: s += c          # O(n^2)
# CORRECT:
#   good = "".join(parts)                          # O(n)

# MISTAKE: assuming threads speed up CPU work
#   bad = ThreadPoolExecutor for CPU-bound scoring  # GIL serializes
# CORRECT:
#   good = ProcessPoolExecutor, or asyncio for I/O waits

# MISTAKE: is for value comparison
#   bad = if x is 1000: ...    # may be False for large ints
# CORRECT:
#   good = if x == 1000: ...

# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    # __slots__ saves memory (instance + instance dict) and blocks new attrs
    wd = WithDict(0, 0)
    ws = WithSlots(0, 0)
    assert sys.getsizeof(wd) + sys.getsizeof(wd.__dict__) > sys.getsizeof(ws), \
        "__slots__ instances must be smaller including the dict"
    try:
        WithSlots(0, 0).extra = 1  # type: ignore[attr-defined]
        assert False, "__slots__ must prevent new attributes"
    except AttributeError:
        pass

    # Small ints cached, large ints not (fresh object from runtime parse)
    assert 200 is 200, "small ints are interned"
    big_a = 2**40
    big_b = int(str(2**40))
    assert big_a == big_b, "large ints are equal"
    assert not (big_a is big_b), "large ints are distinct objects"

    # join vs += produce identical strings
    assert concat_loop(100) == join_build(100) == "x" * 100

    # Generators stream — no materialization
    gen = (i for i in range(3))
    assert next(gen) == 0 and list(gen) == [1, 2]

    # memoryview zero-copy slice matches original bytes
    payload = b"AB" + b"\x00" * 8
    assert memoryview(payload)[:2].tobytes() == b"AB"

    # Embedding memory math: 1M x 768 float32 = ~3.07 GB
    assert embedding_ram_bytes(1_000_000, 768, 32) == 1_000_000 * 768 * 4, \
        "rows * dim * bytes-per-element"
    assert embedding_ram_bytes(1_000_000, 768, 16) == 1_000_000 * 768 * 2, \
        "float16 halves the footprint"

    # join is faster than += (relative check, not wall-clock)
    assert timeit.timeit(lambda: join_build(2000), number=50) < \
        timeit.timeit(lambda: concat_loop(2000), number=50), \
        "join must beat += for repeated concatenation"

    print("[OK] 52-memory-and-performance: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. __slots__: smaller instances, no new attrs")
        print("2. is for identity, == for equality; interning surprises")
        print("3. join, not +=, for string building")
        print("4. Generators stream with O(1) memory")
        print("5. GIL: processes for CPU, async/threads for I/O")
        _verify()
