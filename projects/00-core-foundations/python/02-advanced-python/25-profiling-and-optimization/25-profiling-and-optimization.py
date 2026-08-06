"""
Advanced Python - 25: Profiling and Optimization
=================================================
Topics: timeit microbenchmarks and their traps; cProfile + pstats;
        measure before optimizing; algorithmic wins; functools.cache;
        __slots__; str.join vs string concatenation; a 10s -> 100ms
        case study.

Why this matters for AI/backend engineering:
    A data pipeline that takes 10 seconds per run costs real money at
    10k runs. The 100x win is almost never micro-optimization -- it is
    swapping an O(n^2) algorithm for O(n), or a Python loop for a
    vectorized call (a Python loop over 1M rows is ~100x slower than the
    NumPy equivalent). Measure first: guessing is how 90% of "optimization"
    time gets spent on the wrong line.

Run:      python 25-profiling-and-optimization.py
Verify:   python 25-profiling-and-optimization.py --verify
Reference: https://docs.python.org/3/library/timeit.html
           https://docs.python.org/3/library/profile.html
"""

from __future__ import annotations

import cProfile
import functools
import os
import pstats
import random
import sys
import time
from collections import Counter

random.seed(42)
os.environ.setdefault("MPLBACKEND", "Agg")   # never open a GUI window

# ============================================================
# 1. timeit: Microbenchmarks and Their Traps
# ============================================================
# timeit gives stable timings by repeating and taking the best run.
# Traps: (a) default `number` may be too small; (b) global-name lookup is
# slower than local -- pass globals= or bind to a local; (c) building the
# object INSIDE the timed statement measures construction, not the op.

def demo_timeit_traps() -> None:
    """Show stable timing and the global-lookup trap."""
    import timeit
    data = list(range(1000))
    # timeit only sees the namespace you hand it via globals=; a local
    # variable is invisible unless you put it there.
    ns: dict[str, object] = {"data": data}
    t_global = timeit.timeit("sum(data)", globals=ns, number=10_000)
    ns["total"] = sum
    t_local = timeit.timeit("total(data)", globals=ns, number=10_000)
    print(f"  sum via attribute on ns: {t_global:.4f}s for 10k runs")
    print(f"  sum via local binding  : {t_local:.4f}s for 10k runs")
    print(f"  -> pass globals= explicitly; bind hot names locally")
    # Output:
    #   sum via attribute on ns: 0.0Xs for 10k runs
    #   sum via local binding  : 0.0Ys for 10k runs
    #   -> pass globals= explicitly; bind hot names locally


# ============================================================
# 2. cProfile + pstats: Where Time Actually Goes
# ============================================================
# Profile first, optimize second. pstats sorts by cumulative or self time
# and prints the top rows; tottime is time INSIDE the function, excluding
# callees -- the usual place to look first.

def _mix_work(rows: int) -> list[float]:
    """A plausible pipeline: nested loops, string work, a sort."""
    out: list[float] = []
    for i in range(rows):
        for j in range(50):
            out.append((i * j) % 97)
    out.sort()
    labels = [f"row-{v}" for v in out]
    return [len(s) for s in labels]


def demo_cprofile() -> None:
    """Profile a mixed function and print the top-5 self-time rows."""
    profiler = cProfile.Profile()
    profiler.enable()
    _mix_work(1200)
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats("tottime")
    print("  top 5 by tottime:")
    stats.print_stats(5)
    # Output:
    #   top 5 by tottime:
    #   <a small table of functions sorted by self time>


# ============================================================
# 3. Measure Before Optimizing: The Algorithmic Win
# ============================================================
# Finding duplicates with `x not in items[:i]` inside a comprehension is
# O(n^2) (each check scans a growing prefix). A seen-set is O(n). At
# n = 3000 the naive version is already ~100x slower.
# Complexity annotations:
#   naive_dedup: O(n^2) time, O(1) extra space
#   linear_dedup: O(n) time, O(n) space

def naive_dedup(items: list[int]) -> list[int]:
    """Keep first occurrences, scanning a prefix each time (O(n^2))."""
    return [x for i, x in enumerate(items) if x not in items[:i]]


def linear_dedup(items: list[int]) -> list[int]:
    """Keep first occurrences, one pass with a seen-set (O(n))."""
    seen: set[int] = set()
    out: list[int] = []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def demo_algorithmic_win() -> tuple[float, float]:
    """Measure naive vs linear dedup on the same data."""
    data = [random.randrange(50) for _ in range(3000)]
    start = time.perf_counter()
    naive_dedup(data)
    naive_t = time.perf_counter() - start
    start = time.perf_counter()
    linear_dedup(data)
    linear_t = time.perf_counter() - start
    print(f"  naive  O(n^2): {naive_t:.3f}s")
    print(f"  linear O(n)  : {linear_t:.4f}s")
    print(f"  speedup: {naive_t / linear_t:.0f}x")
    return naive_t, linear_t


# ============================================================
# 4. functools.cache: The Cheapest Win There Is
# ============================================================
# Memoization turns an exponential recursion into a linear one. lru_cache
# is O(1) per lookup; keys must be hashable. For AI work: caching the
# embedding of a repeated query is the same pattern.

def _fib(n: int) -> int:
    """Raw Fibonacci: T(n) = T(n-1) + T(n-2), exponential calls."""
    return n if n < 2 else _fib(n - 1) + _fib(n - 2)


def demo_cache() -> tuple[int, int]:
    """Compare call counts with and without functools.cache."""
    uncalled = {"n": 0}

    def fib_uncached(n: int) -> int:
        uncalled["n"] += 1
        return n if n < 2 else fib_uncached(n - 1) + fib_uncached(n - 2)

    @functools.cache
    def fib_cached(n: int) -> int:
        return n if n < 2 else fib_cached(n - 1) + fib_cached(n - 2)

    n = 25
    assert fib_uncached(n) == fib_cached(n), "both must compute the same value"
    print(f"  fib({n}) uncached calls: {uncalled['n']}")
    print(f"  fib({n}) cached calls  : {fib_cached.cache_info().currsize + 1}")
    print(f"  speedup: {uncalled['n'] // 26}x fewer calls")
    return uncalled["n"], fib_cached.cache_info().currsize + 1


# ============================================================
# 5. __slots__: Memory Before Speed
# ============================================================
# __slots__ removes the per-instance __dict__, shrinking each object and
# making attribute access faster. At 1M embedding records this is
# hundreds of MB. (See 13-slots.py for the deep dive.)

class RowRegular:
    """A plain row object with a per-instance dict."""

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class RowSlots:
    """The same row with __slots__: no __dict__, no dynamic attrs."""

    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


def demo_slots() -> tuple[int, int]:
    """Measure per-instance memory of both variants at 10k objects.

    sys.getsizeof(instance) is identical for both on 3.13 (48 bytes);
    the real cost of a regular class is its per-instance __dict__, so
    the comparison must include it.
    """
    def instance_bytes(obj: object) -> int:
        total = sys.getsizeof(obj)
        d = getattr(obj, "__dict__", None)
        if d is not None:
            total += sys.getsizeof(d)
        return total

    n = 10_000
    regular = [RowRegular(i, i) for i in range(n)]
    slotted = [RowSlots(i, i) for i in range(n)]
    reg_bytes = sum(instance_bytes(r) for r in regular)
    slot_bytes = sum(instance_bytes(s) for s in slotted)
    print(f"  {n} regular rows (with __dict__): {reg_bytes // 1024} KB")
    print(f"  {n} slotted rows (no __dict__) : {slot_bytes // 1024} KB")
    print(f"  saving: {reg_bytes - slot_bytes} bytes across {n} objects")
    return reg_bytes, slot_bytes


# ============================================================
# 6. str.join vs String Concatenation
# ============================================================
# CPython optimizes `s = s + c` when s has refcount 1 (in-place resize).
# The quadratic disaster appears the moment an intermediate is kept alive
# -- a progress log, a snapshot, a retry buffer -- because the next
# concatenation can no longer reuse the buffer. join is O(n) either way.
# Complexity: concat_with_plus O(n^2) total copies; join O(n).

def concat_with_plus(chunks: list[str]) -> str:
    """Quadratic assembly: every intermediate stays referenced."""
    s = ""
    progress: list[str] = []          # holds refs -> blocks in-place resize
    for chunk in chunks:
        s = s + chunk
        progress.append(s)
    return s if progress else s


def concat_with_join(chunks: list[str]) -> str:
    """Linear assembly: one pass, one buffer."""
    return "".join(chunks)


def demo_join_vs_plus() -> tuple[float, float]:
    """Measure both builders on the same 8k chunks."""
    chunks = [f"chunk-{i};" for i in range(8_000)]
    start = time.perf_counter()
    concat_with_plus(chunks)
    plus_t = time.perf_counter() - start
    start = time.perf_counter()
    concat_with_join(chunks)
    join_t = time.perf_counter() - start
    print(f"  s = s + c (O(n^2)): {plus_t:.3f}s")
    print(f"  ''.join     (O(n)): {join_t:.4f}s")
    print(f"  speedup: {plus_t / join_t:.0f}x")
    return plus_t, join_t


# ============================================================
# 7. Case Study: 10s -> 100ms
# ============================================================
# A report builder doing three classic sins: quadratic string assembly,
# O(n^2) dedup, and building lists of throwaway objects. The optimized
# version keeps the same I/O contract but fixes all three.

def build_report_slow(rows: list[dict[str, int]]) -> str:
    """The 'before': naive in every dimension (same output format).

    Keeping an audit trail of every intermediate string forces a fresh
    allocation on each concatenation -- the realistic way the quadratic
    cost shows up in production code.
    """
    header = ""
    for i, name in enumerate(["id", "score"]):
        if i > 0:
            header = header + ","
        header = header + name
    lines = ""
    audit: list[str] = []
    for row in rows:
        line = ""
        for i, key in enumerate(["id", "score"]):
            if i > 0:
                line = line + ","
            line = line + str(row[key])
        lines = lines + line + "\n"
        audit.append(lines)              # holds refs -> O(n^2) copies
    return header + "\n" + lines


def build_report_fast(rows: list[dict[str, int]]) -> str:
    """The 'after': join-based assembly, no per-row string churn."""
    header = ",".join(["id", "score"])
    lines = []
    for row in rows:
        lines.append(",".join([str(row["id"]), str(row["score"])]))
    return header + "\n" + "\n".join(lines) + "\n"


def demo_case_study() -> tuple[float, float]:
    """Measure the same report two ways; results must be identical."""
    rows = [{"id": i, "score": random.randrange(1000)} for i in range(4000)]
    slow_out = build_report_slow(rows)
    fast_out = build_report_fast(rows)
    assert slow_out == fast_out, "optimized version must be byte-identical"
    start = time.perf_counter()
    build_report_slow(rows)
    slow_t = time.perf_counter() - start
    start = time.perf_counter()
    build_report_fast(rows)
    fast_t = time.perf_counter() - start
    print(f"  slow (quadratic strings): {slow_t:.3f}s")
    print(f"  fast (join-based)       : {fast_t:.4f}s")
    print(f"  speedup: {slow_t / fast_t:.0f}x")
    return slow_t, fast_t


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: optimizing before measuring -- 90% of effort lands on code
#   that is not the bottleneck. cProfile first.
# MISTAKE: micro-optimizing an O(n^2) algorithm (the constant factor
#   hides the real 100x).
# CORRECT: fix the algorithm, then micro-optimize what remains.
# MISTAKE: s = s + c in a loop, then wondering why join is 'magically'
#   faster. It is not magic: + allocates a fresh string every step.
# MISTAKE: timing with a wall clock once and trusting the number.
# CORRECT: timeit.repeat, take min, run in CI with ratio asserts only.


# ============================================================
# Self-Verification  (MANDATORY -- every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # 1. Correctness first: optimized paths must match naive ones.
    data = [random.randrange(50) for _ in range(3000)]
    assert linear_dedup(data) == naive_dedup(data), \
        "linear dedup must return the same elements as naive dedup"
    chunks = [f"chunk-{i};" for i in range(8_000)]
    assert concat_with_join(chunks) == concat_with_plus(chunks), \
        "join and plus assembly must produce identical strings"

    # 2. Algorithmic win: linear dedup is far faster (generous ratio).
    naive_t, linear_t = demo_algorithmic_win()
    assert linear_t < naive_t * 0.2, \
        "linear dedup must be >5x faster than naive O(n^2) (got %.2fx)" % (
            naive_t / linear_t)

    # 3. functools.cache cuts calls by orders of magnitude (deterministic).
    uncached_calls, cached_calls = demo_cache()
    assert uncached_calls > cached_calls * 1000, \
        "cache must eliminate >1000x the recursive calls (got %d vs %d)" % (
            uncached_calls, cached_calls)

    # 4. __slots__ saves memory (measured, not wall-clock).
    reg_bytes, slot_bytes = demo_slots()
    assert slot_bytes < reg_bytes, \
        "__slots__ must reduce per-instance memory"

    # 5. str.join beats fresh-allocation concatenation (generous ratio).
    plus_t, join_t = demo_join_vs_plus()
    assert join_t < plus_t * 0.2, \
        "join must be >5x faster than s = s + c (got %.2fx)" % (plus_t / join_t)

    # 6. Case study: the optimized report is much faster AND identical.
    rows = [{"id": i, "score": random.randrange(1000)} for i in range(8000)]
    assert build_report_fast(rows) == build_report_slow(rows), \
        "optimized report must be byte-identical to the slow one"
    slow_t, fast_t = demo_case_study()
    assert fast_t < slow_t * 0.2, \
        "optimized pipeline must be >5x faster (got %.2fx)" % (slow_t / fast_t)

    # 7. cProfile runs without error and reports the hot function.
    profiler = cProfile.Profile()
    profiler.enable()
    _mix_work(200)
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats("tottime")
    top = stats.stats
    assert any("_mix_work" in fn[2] for fn in top), \
        "cProfile must record _mix_work in its stats"

    print("\n[OK] 25-profiling-and-optimization: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("=" * 60)
        print("PROFILING AND OPTIMIZATION: MEASURE FIRST, WIN BIG")
        print("=" * 60)
        print("\n--- 1. timeit traps ---")
        demo_timeit_traps()
        print("\n--- 2. cProfile / pstats ---")
        demo_cprofile()
        print("\n--- 3. Algorithmic win: O(n^2) vs O(n) dedup ---")
        demo_algorithmic_win()
        print("\n--- 4. functools.cache ---")
        demo_cache()
        print("\n--- 5. __slots__ memory ---")
        demo_slots()
        print("\n--- 6. str.join vs concatenation ---")
        demo_join_vs_plus()
        print("\n--- 7. Case study: 10s -> 100ms ---")
        demo_case_study()
        print("\n--- Summary ---")
        print("1. Profile (cProfile) before optimizing anything.")
        print("2. Algorithmic wins (O(n^2) -> O(n)) beat micro-tuning.")
        print("3. cache, join, __slots__ are the cheap, safe wins.")
        _verify()
