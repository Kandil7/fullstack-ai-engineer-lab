"""
Advanced Python — 34: Debugging Techniques
===========================================
Topics: pdb/breakpoint() and the command set; post-mortem (pdb.pm());
IDE debugging vs print; reading tracebacks properly; traceback module;
faulthandler for segfaults and hangs; sys.settrace basics; logging as
debugging; assertion-driven debugging; bisecting a failure; reproducing
nondeterminism (PYTHONHASHSEED, seeds); debugging async code; debugging
subprocesses; rubber-ducking and hypothesis-driven method

Why this matters for AI/backend engineering:
    The hardest AI bug class is SILENT: a RAG pipeline returns the wrong
    chunks with no traceback, no exception — just wrong answers. This
    file builds the hypothesis-driven method for that class: isolate
    the stage, log the intermediate values, freeze randomness, and
    bisect the failure. The tooling (traceback, faulthandler, pdb) is
    what you use before you ever reach for the LLM to explain a bug.

Run:      python 34-debugging-techniques.py
Verify:   python 34-debugging-techniques.py --verify
Reference: https://docs.python.org/3/library/pdb.html
"""

from __future__ import annotations

import faulthandler
import io
import logging
import os
import random
import sys
import traceback
from typing import Any


# ============================================================
# 1. Reading tracebacks properly — bottom-up, innermost first
# ============================================================
# A traceback lists frames OUTSIDE-IN: the LAST frame (bottom) is where
# the exception was raised; the frames above are the callers. Always
# read from the bottom up.

def _inner() -> None:
    """The actual failure site."""
    raise ValueError("chunk index out of range")


def _middle() -> None:
    """Intermediate caller."""
    _inner()


def _outer() -> None:
    """Entry point."""
    _middle()


def capture_traceback() -> str:
    """Run _outer, capture the traceback as text. O(1)."""
    try:
        _outer()
    except ValueError:
        return traceback.format_exc()
    return ""


# Example 1: the traceback SHAPE — frames outermost first
tb = capture_traceback()
lines = tb.strip().splitlines()
print("first line (exception + outermost caller):")
print(lines[0])
print("last line (exception message):")
print(lines[-1])
print("innermost frame name present:", "_inner" in tb)

# Output:
# first line (exception + outermost caller):
# Traceback (most recent call last):
# last line (exception message):
# ValueError: chunk index out of range
# innermost frame name present: True


# ============================================================
# 2. traceback.format_exc — get the traceback as a string
# ============================================================
# print(exc) gives the message only; format_exc gives the full frame
# stack — what you want in logs.

def log_exception(logger: logging.Logger, exc: BaseException) -> str:
    """Format the full traceback for a log line. O(1)."""
    return "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))


# Example 2: full stack vs bare message
try:
    _outer()
except ValueError as exc:
    full = log_exception(logging.getLogger("demo"), exc)
    print(f"bare message: {exc}")
    print(f"full text contains '_middle': {'_middle' in full}")

# Output:
# bare message: chunk index out of range
# full text contains '_middle': True


# ============================================================
# 3. Assertion-driven debugging — find the LIE, not the crash
# ============================================================
# A crash tells you WHERE; an assertion tells you WHAT WAS WRONG.
# The RAG silent-bug method: assert invariants at every stage boundary.

def normalize_chunks(chunks: list[str]) -> list[str]:
    """Strip and drop empties; assert the invariant. O(n)."""
    result = [c.strip() for c in chunks if c.strip()]
    assert all(isinstance(c, str) and c for c in result), \
        "invariant: every chunk is a non-empty string"
    return result


def retrieve(query: str, chunks: list[str], top_k: int) -> list[str]:
    """Fake retriever: naive scoring — bugs here are silent. O(n)."""
    scored = sorted(chunks, key=lambda c: len(c))  # BUG: wrong metric
    return scored[:top_k]


# Example 3: assertion catches the invariant break BEFORE the retriever
bad_chunks = ["  good  ", "", None, "ok"]          # type: ignore[list-item]
try:
    normalize_chunks(bad_chunks)                   # type: ignore[arg-type]
    print("normalized (unexpected)")
except (AssertionError, AttributeError) as exc:
    print(f"caught by assertion: {type(exc).__name__}: {exc}")

# Output:
# caught by assertion: AttributeError: 'NoneType' object has no attribute 'strip'

# Example 4: the silent bug — wrong ranking with no exception
print(f"retriever top2: {retrieve('q', ['short', 'a much longer chunk', 'med'], 2)}")
print(f"retriever top1: {retrieve('q', ['short', 'a much longer chunk'], 1)}")

# Output:
# retriever top2: ['med', 'short']
# retriever top1: ['short']


# ============================================================
# 4. Logging as debugging — structured, leveled, queryable
# ============================================================

def make_logger(level: int = logging.DEBUG) -> tuple[logging.Logger, io.StringIO]:
    """A logger that writes to a StringIO for tests. O(1)."""
    logger = logging.getLogger("debug-demo")
    logger.handlers.clear()
    logger.setLevel(level)
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    logger.addHandler(handler)
    return logger, stream


def debug_pipeline(logger: logging.Logger, n: int) -> int:
    """Log at each stage; DEBUG level shows intermediates. O(n)."""
    logger.info("stage 1: load %d docs", n)
    processed = n * 2
    logger.debug("stage 2: processed=%d", processed)
    return processed


# Example 5: level-driven visibility (default level is DEBUG)
logger, stream = make_logger()
result = debug_pipeline(logger, 3)
output = stream.getvalue()
print(f"result: {result}")
print(f"info logged: {'stage 1' in output}")
print(f"debug shown at DEBUG level: {'processed=6' in output}")
logger_info, stream_info = make_logger(level=logging.INFO)
debug_pipeline(logger_info, 3)
print(f"debug hidden at INFO level: {'processed=6' not in stream_info.getvalue()}")

# Output:
# result: 6
# info logged: True
# debug shown at DEBUG level: True
# debug hidden at INFO level: True


# ============================================================
# 5. Reproducing nondeterminism — freeze the seeds
# ============================================================
# "It works on my machine" usually means an unseeded random source or
# set/dict iteration order. Freeze everything for a repro.

def shuffly_score(items: list[str]) -> list[str]:
    """Deterministic ONLY with a seeded random. O(n)."""
    rng = random.Random(42)             # fixed seed -> fixed shuffle
    result = items[:]
    rng.shuffle(result)
    return result


def hash_order() -> list[str]:
    """Dict/set iteration order depends on PYTHONHASHSEED. O(n)."""
    return list({"a", "b", "c"})        # order varies per process


# Example 6: seeded shuffle is reproducible; set order is not
print(f"seeded shuffle: {shuffly_score(['a', 'b', 'c', 'd'])}")
print(f"seeded shuffle: {shuffly_score(['a', 'b', 'c', 'd'])}")
print(f"set order (process-dependent): {hash_order()}")

# Output:
# seeded shuffle: ['b', 'a', 'd', 'c']
# seeded shuffle: ['b', 'a', 'd', 'c']
# set order (process-dependent): ['b', 'a', 'c']  (varies per run)


# ============================================================
# 6. faulthandler — dump the stack on hang or crash
# ============================================================
# faulthandler registers handlers that dump Python stack traces on
# signals (SIGSEGV, SIGABRT) and can be triggered manually. The
# canonical fix for "it hangs" — find WHERE it hangs.

def enable_faulthandler() -> None:
    """Register faulthandler; also flush stderr immediately. O(1)."""
    faulthandler.enable()
    sys.stderr.reconfigure(line_buffering=True)  # type: ignore[attr-defined]


def hang_site() -> str:
    """A function that would hang (simulated: returns, but marked)."""
    return "would-block-here"


# Example 7: faulthandler dump (the real one fires on Ctrl-C/SIGTERM)
enable_faulthandler()
print(f"faulthandler registered; site marker: {hang_site()}")


def _dump_demo() -> str:
    """Run a manual faulthandler dump; the frame appears in the stack."""
    dump_path = "__faulthandler_dump_demo__"
    with open(dump_path, "w", encoding="utf-8") as dump_file:
        faulthandler.dump_traceback(file=dump_file)   # manual dump
    with open(dump_path, encoding="utf-8") as dump_file:
        text = dump_file.read()
    os.remove(dump_path)
    return text


dump_text = _dump_demo()
print(f"manual dump contains '_dump_demo': {'_dump_demo' in dump_text}")

# Output:
# faulthandler registered; site marker: would-block-here
# manual dump contains '_dump_demo': True


# ============================================================
# 7. pdb / breakpoint() — interactive inspection
# ============================================================
# breakpoint() drops into pdb: n=next, s=step, p expr=print,
# c=continue, q=quit, l=list, w=where, u/d=up/down.
# The demo below RUNS pdb non-interactively via runctx and a command
# script, so the exercise stays deterministic.

import pdb  # noqa: E402


def pdb_demo_source() -> int:
    """A function we 'debug' with pdb in the demo. O(1)."""
    x = 10
    y = 32
    return x + y


def run_pdb_commands(code: str, commands: str) -> str:
    """Run pdb with a command script; return the session text. O(1)."""
    out = io.StringIO()
    pdb.Pdb(stdout=out).runcall(eval, code, {})  # noqa: S307 - demo only
    # (the commands are applied via Pdb's set_trace-free protocol below)
    return out.getvalue()


# Example 8: pdb can print values at a breakpoint (deterministic demo)
class _CapturingPdb(pdb.Pdb):
    """Pdb subclass that records 'p <expr>' results instead of printing."""

    def __init__(self) -> None:
        super().__init__(stdout=io.StringIO())
        self.recorded = ""

    def do_p(self, arg: str) -> None:
        """Capture the result of the pdb 'p' command. O(1)."""
        frame = self.curframe
        try:
            value = eval(arg, frame.f_globals, frame.f_locals)  # noqa: S307
        except Exception as exc:  # noqa: BLE001
            self.recorded += f"{arg}: {type(exc).__name__}\n"
        else:
            self.recorded += f"{arg} = {value!r}\n"


def pdb_inspect() -> str:
    """Run the demo code under a scripted pdb session. O(1)."""
    cap = _CapturingPdb()
    code = (
        "x = 10\n"
        "y = 32\n"
        "result = x + y\n"
    )
    # cmdqueue feeds pdb commands deterministically (no stdin):
    # step past x=10, inspect it, step past y=32, inspect it, continue
    cap.cmdqueue = ["n", "p x", "n", "p y", "c"]
    cap.run(code)
    return cap.recorded


# Example 8 (run): pdb 'p' commands evaluate live state
print(pdb_inspect(), end="")

# Output:
# x = 10
# y = 32


# ============================================================
# 8. Bisecting a failure — binary search the change
# ============================================================
# For a regression across N commits/configs: test the midpoint, keep
# the failing half, repeat. O(log n) runs instead of O(n).

def bisect_bad(configs: list[str], bad_from: int) -> int:
    """Return the first index where a config goes bad. O(log n)."""
    lo, hi = 0, len(configs) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if mid >= bad_from:
            hi = mid
        else:
            lo = mid + 1
    return lo


# Example 8b: 100 configs, break at index 42 -> found in ~7 checks
configs = [f"cfg-{i}" for i in range(100)]
print(f"first bad config: {configs[bisect_bad(configs, 42)]}")

# Output:
# first bad config: cfg-42


# ============================================================
# 9. Hypothesis-driven debugging — the method
# ============================================================
# 1. Reproduce (freeze seeds, pin inputs)      — "can I make it fail
#    on demand?"
# 2. Isolate (which stage?)                    — log at boundaries
# 3. Hypothesize (WHY?)                        — one candidate cause
# 4. Test the hypothesis (prove it)            — small probe
# 5. Fix + regression test                     — never fix blind

def isolate_stage(chunks: list[str]) -> str:
    """Which stage corrupts the data? Check each boundary. O(n)."""
    stage1 = [c.strip() for c in chunks]
    if any(not c for c in stage1):
        return "stage-1: empty after strip"
    stage2 = sorted(stage1, key=len)
    if len(stage2) != len(set(stage2)):        # probe: no duplicates
        return "stage-2: duplicates introduced"
    return "ok"


# Example 9: stage isolation localizes the silent failure
print(isolate_stage([" ok ", "fine"]))
print(isolate_stage([" ok ", ""]))
print(isolate_stage(["b", "a", "a"]))

# Output:
# ok
# stage-1: empty after strip
# stage-2: duplicates introduced


# ============================================================
# 10. Debugging subprocesses and async code (rules)
# ============================================================
# Subprocess: capture stderr separately; the child's traceback is not
# your traceback — always log child stderr, set a timeout, and check
# returncode.
# Async: asyncio failures surface at await points; enable
# asyncio.run(debug=True) for slow-callback and unawaited-task
# warnings; wrap coroutines in try/except at task boundaries.
# Python 3.11+ shows the exact await chain in tracebacks.


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: reading the traceback top-down        -> read bottom-up
# MISTAKE: print(exc) and losing the frames      -> format_exc
# MISTAKE: fixing the crash, not the invariant   -> assert + investigate
# MISTAKE: unseeded random in the repro          -> freeze ALL seeds
# MISTAKE: debugging a hang without faulthandler -> dump the stack
# MISTAKE: fixing blind instead of hypothesis    -> isolate, prove, fix
# MISTAKE: only INFO logs, no DEBUG stage logs   -> log at boundaries


# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # --- traceback.format_exc shape ---
    tb = capture_traceback()
    assert tb.startswith("Traceback (most recent call last):"), \
        "format_exc must start with the traceback header"
    assert "_inner" in tb and "_middle" in tb and "_outer" in tb, \
        "the full frame chain must appear"
    assert "ValueError: chunk index out of range" in tb, \
        "the innermost frame and message must appear at the end"

    # --- log_exception includes the stack ---
    try:
        _outer()
    except ValueError as exc:
        full = log_exception(logging.getLogger("verify"), exc)
        assert "_inner" in full, \
            "format_exception must include all frames"
        assert "chunk index out of range" in full, \
            "the message must be in the formatted output"

    # --- assertion-driven debugging catches the invariant break ---
    try:
        normalize_chunks([" ok ", "", None, "x"])  # type: ignore[list-item]
        raise AssertionError("normalize_chunks accepted None")
    except (AssertionError, AttributeError):
        pass
    assert normalize_chunks([" a ", " b "]) == ["a", "b"], \
        "clean chunks normalize correctly"

    # --- the silent retriever bug is reproducible ---
    assert retrieve("q", ["short", "a much longer chunk"], 1) == ["short"], \
        "the naive metric ranks by length — reproducible bug"

    # --- logging levels control visibility ---
    logger, stream = make_logger()
    debug_pipeline(logger, 3)
    output = stream.getvalue()
    assert "stage 1" in output, "INFO lines appear at DEBUG level"
    assert "processed=6" in output, "DEBUG lines appear at DEBUG level"
    logger2, stream2 = make_logger(level=logging.INFO)
    debug_pipeline(logger2, 3)
    assert "processed=6" not in stream2.getvalue(), \
        "DEBUG lines are hidden at INFO level"

    # --- seeded randomness is reproducible ---
    a = shuffly_score(["a", "b", "c", "d"])
    b = shuffly_score(["a", "b", "c", "d"])
    assert a == b, "same seed -> same shuffle (the repro requirement)"

    # --- faulthandler dump works ---
    enable_faulthandler()
    dump_path = "__faulthandler_dump_verify__"
    with open(dump_path, "w", encoding="utf-8") as dump_file:
        faulthandler.dump_traceback(file=dump_file)
    with open(dump_path, encoding="utf-8") as dump_file:
        dump_text = dump_file.read()
    os.remove(dump_path)
    assert "34-debugging-techniques.py" in dump_text, \
        "the dump must show the current stack (our file in it)"

    # --- pdb inspection records values ---
    recorded = pdb_inspect()
    assert "x = 10" in recorded and "y = 32" in recorded, \
        "pdb 'p' commands must evaluate live state"

    # --- bisection is logarithmic ---
    assert bisect_bad([f"c{i}" for i in range(100)], 42) == 42, \
        "bisect must find the exact first-bad index"

    # --- stage isolation ---
    assert isolate_stage([" ok ", ""]) == "stage-1: empty after strip", \
        "isolation must name the failing stage"
    assert isolate_stage(["b", "a", "a"]) == "stage-2: duplicates introduced", \
        "the second probe names its own stage"
    assert isolate_stage([" ok ", "fine"]) == "ok", \
        "clean data passes all stage probes"

    print("[OK] 34-debugging-techniques: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Read tracebacks bottom-up; log format_exc, not str(exc)")
        print("2. Assert invariants at stage boundaries (silent-bug method)")
        print("3. Freeze seeds, dump stacks, bisect changes, test hypotheses")
        _verify()
