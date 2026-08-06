# 34 — Debugging Techniques Lecture

## 1. Topic Overview

Debugging is a *method*, not a talent. The best debuggers do the same
five steps every time: **reproduce, isolate, hypothesize, prove, fix** —
and they have tools for each step. This topic covers the Python toolset:

- **Reading tracebacks properly** (bottom-up, innermost frame first)
- **`traceback` module** — `format_exc` for logs
- **Assertion-driven debugging** — find the lie, not the crash
- **Logging as debugging** — level-driven visibility at stage boundaries
- **Reproducing nondeterminism** — freeze seeds, `PYTHONHASHSEED`
- **`faulthandler`** — dump the stack on hangs and crashes
- **`pdb`/`breakpoint()`** — interactive inspection
- **Bisecting failures** — binary search over changes/configs
- **Debugging async code and subprocesses**
- **The hypothesis-driven method**, with the RAG silent-bug case study

The hardest AI bug class is **silent**: a RAG pipeline returns the wrong
chunks — no traceback, no exception, just wrong answers. Everything in
this topic is in service of that case: the assertion that catches the
lie, the log that shows the stage, the fixed seed that reproduces it,
the bisect that narrows it.

## 2. Learning Objectives

By the end of this lecture you will be able to:

1. Read a traceback correctly: bottom-up, identifying the innermost
   frame where the exception was raised.
2. Capture full tracebacks as strings (`traceback.format_exc`,
   `format_exception`) for logs.
3. Apply assertion-driven debugging: assert invariants at stage
   boundaries to catch silent corruption.
4. Use leveled logging as a debugging instrument, not a firehose.
5. Reproduce nondeterministic failures by freezing seeds and hash
   order.
6. Use `faulthandler` to locate hangs and crashes.
7. Drive `pdb` non-interactively (and know the interactive command
   set).
8. Bisect a regression in O(log n) runs.
9. Apply the five-step hypothesis method to a silent RAG bug.

## 3. Prerequisites

- **`16-threading.py`** and **`22-asyncio-advanced.py`** — the async
  debugging section assumes you know what an await chain is.
- **`31-concurrency-patterns`** — hangs are usually concurrency bugs;
  faulthandler is how you find them.
- **`33-security-essentials`** — assertion-driven debugging pairs with
  input validation.
- Comfort with exceptions, logging, and random.

## 4. Key Concepts

### 4.1 Reading tracebacks bottom-up

A traceback prints frames **outside-in**: the first frame is the entry
point, the **last frame (bottom) is where the exception was raised**.
Read from the bottom up:

```python
def _inner():
    raise ValueError("chunk index out of range")

def _middle():
    _inner()

def _outer():
    _middle()

try:
    _outer()
except ValueError:
    tb = traceback.format_exc()

lines = tb.strip().splitlines()
print(lines[0])     # Traceback (most recent call last):
print(lines[-1])    # ValueError: chunk index out of range
print("_inner" in tb)
```

```text
# Output:
# Traceback (most recent call last):
# ValueError: chunk index out of range
# True
```

**The method:** the bottom frame tells you *what* broke; walk upward to
see *how you got there*. "Innermost frame first" is the answer to 80% of
"where do I start?"

### 4.2 `traceback.format_exc` — the string you log

`print(exc)` gives the message only — the frames are lost. Log the full
stack:

```python
def log_exception(logger, exc):
    return "".join(traceback.format_exception(
        type(exc), exc, exc.__traceback__))

try:
    _outer()
except ValueError as exc:
    print(f"bare: {exc}")
    print("_middle" in log_exception(logging.getLogger("d"), exc))
```

```text
# Output:
# bare: chunk index out of range
# True
```

**Rule:** in exception handlers that log, use `format_exc()` or
`format_exception` — never `str(exc)` alone.

### 4.3 Assertion-driven debugging — find the lie

A crash tells you *where*; an assertion tells you *what is wrong*. For
silent bugs (wrong data, no exception), assertions at **stage
boundaries** are the detector:

```python
def normalize_chunks(chunks):
    result = [c.strip() for c in chunks if c.strip()]
    assert all(isinstance(c, str) and c for c in result), \
        "invariant: every chunk is a non-empty string"
    return result

normalize_chunks(["  good  ", "", None, "ok"])   # None survives the filter
```

```text
# Output (AttributeError — or AssertionError with a proper filter):
# AttributeError: 'NoneType' object has no attribute 'strip'
```

The assertion (or the crash at the boundary) converts "the pipeline
silently produced garbage" into "stage 1 broke its contract". For the
RAG case, assert at every boundary: chunk non-empty, embeddings match
chunk count, retrieved chunk IDs exist in the corpus.

### 4.4 Logging as debugging

Debugging with print is debugging with a firehose. Logging gives you
**levels** — INFO for boundaries, DEBUG for intermediates — and they
cost nothing when disabled:

```python
def debug_pipeline(logger, n):
    logger.info("stage 1: load %d docs", n)
    processed = n * 2
    logger.debug("stage 2: processed=%d", processed)
    return processed
```

Set the level per environment: INFO in prod (cheap), DEBUG in the
repro (detailed). The log line at each stage boundary is the map you
need when the bug is silent.

### 4.5 Reproducing nondeterminism — freeze the seeds

"It works on my machine" = an unseeded random source or unstable
iteration order. Freeze everything:

```python
def shuffly_score(items):
    rng = random.Random(42)      # fixed seed -> fixed shuffle
    result = items[:]
    rng.shuffle(result)
    return result

print(shuffly_score(["a", "b", "c", "d"]))
print(shuffly_score(["a", "b", "c", "d"]))
print(list({"a", "b", "c"}))     # set order varies per process
```

```text
# Output:
# ['b', 'a', 'd', 'c']
# ['b', 'a', 'd', 'c']
# ['b', 'a', 'c']   (varies per run — PYTHONHASHSEED)
```

**Rules:** seed `random`, numpy, torch, and any shuffler; for dict/set
order bugs, reproduce with `PYTHONHASHSEED=0 python repro.py`; if the
bug disappears with a fixed seed, it was an ordering/randomness bug —
that *is* the diagnosis.

### 4.6 `faulthandler` — find the hang

A hang gives no traceback. `faulthandler` registers dump handlers for
signals and can dump manually:

```python
import faulthandler
faulthandler.enable()          # dumps on SIGSEGV/SIGABRT/Ctrl-C

# manual dump:
faulthandler.dump_traceback(file=sys.stderr)
```

On a hung job, send SIGTERM/SIGABRT (or Ctrl-C) and the stack shows
**exactly where every thread is blocked** — the R1.1 producer stuck in
`not_full.wait()` becomes visible in one line. This is the first tool
for any "it hangs" report.

### 4.7 `pdb` / `breakpoint()` — interactive inspection

`breakpoint()` drops into pdb. The essential command set:

| Command | Meaning |
|---|---|
| `n` (next) | Execute the current line |
| `s` (step) | Step INTO function calls |
| `p expr` | Print an expression in the current frame |
| `l` (list) | Show source around the current line |
| `w` (where) | Show the call stack |
| `u` / `d` | Move up/down the stack |
| `c` (continue) | Run until the next breakpoint |
| `q` (quit) | Exit |

For scripts and CI, pdb is scriptable — the exercise drives it
deterministically via `cmdqueue` and a `Pdb` subclass:

```python
cap = _CapturingPdb()          # records "p x" output
cap.cmdqueue = ["n", "p x", "n", "p y", "c"]
cap.run("x = 10\ny = 32\nresult = x + y\n")
```

```text
# Output:
# x = 10
# y = 32
```

**Rule:** `p expr` is the inspection tool; `n`/`s` are the navigation
tools; `w` answers "how did I get here?"

### 4.8 Bisecting a failure — binary search the change

For a regression across N commits/configs/inputs: test the midpoint,
keep the failing half, repeat — O(log n) runs:

```python
def bisect_bad(configs, bad_from):
    lo, hi = 0, len(configs) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if mid >= bad_from:
            hi = mid
        else:
            lo = mid + 1
    return lo

configs = [f"cfg-{i}" for i in range(100)]
print(configs[bisect_bad(configs, 42)])
```

```text
# Output:
# cfg-42
```

`git bisect` automates this over commits; the same pattern works over
config values and inputs. 100 possibilities → 7 runs.

### 4.9 The hypothesis-driven method — the silent RAG bug

The five steps, applied to "RAG returns wrong chunks, no traceback":

1. **Reproduce** — freeze seeds, pin the exact query and documents.
   A bug you cannot reproduce on demand is a bug you cannot fix.
2. **Isolate** — which stage? chunking, embedding, retrieval, or
   reranking? Log at each boundary; compare counts and IDs.
3. **Hypothesize** — *one* candidate cause (e.g. "retriever ranks by
   chunk length, not similarity").
4. **Prove** — a small probe that confirms or kills the hypothesis:

```python
def retrieve(query, chunks, top_k):
    scored = sorted(chunks, key=len)   # wrong metric
    return scored[:top_k]

print(retrieve("q", ["short", "a much longer chunk"], 1))
```

```text
# Output:
# ['short']     <- proof: it ranks by length, not relevance
```

5. **Fix + regression test** — fix the metric, and add a test that
   would fail on the old behavior. Never fix blind.

Stage isolation with boundary probes:

```python
def isolate_stage(chunks):
    stage1 = [c.strip() for c in chunks]
    if any(not c for c in stage1):
        return "stage-1: empty after strip"
    stage2 = sorted(stage1, key=len)
    if len(stage2) != len(set(stage2)):
        return "stage-2: duplicates introduced"
    return "ok"

print(isolate_stage([" ok ", ""]))
print(isolate_stage(["b", "a", "a"]))
```

```text
# Output:
# stage-1: empty after strip
# stage-2: duplicates introduced
```

### 4.10 Debugging async code and subprocesses

**Async:** failures surface at `await` points; enable
`asyncio.run(main(), debug=True)` for slow-callback and unawaited-task
warnings; wrap coroutines at task boundaries. Python 3.11+ tracebacks
show the exact await chain — read it like the call stack.

**Subprocesses:** the child's traceback is *not* your traceback.
Always capture child stderr separately, set a timeout, and check
`returncode`. A failing child that prints to stderr you never read is a
bug that looks like your code's fault.

## 5. Common Mistakes

1. **Reading the traceback top-down** — the bottom frame is where it
   broke; start there.
2. **`print(exc)` in logs** — frames are lost; use `format_exc`.
3. **Fixing the crash, not the invariant** — the crash is a symptom;
   the assertion is the diagnosis.
4. **Unseeded randomness in the repro** — the bug "disappears"; freeze
   every seed.
5. **Debugging a hang without faulthandler** — you are guessing where
   it blocks; dump the stack.
6. **Fixing blind instead of hypothesizing** — change three things,
   fix none; one hypothesis at a time.
7. **INFO-only logging** — the DEBUG intermediates are the map; add
   them at boundaries.

## 6. Best Practices

- **Log at stage boundaries** (counts, IDs, shapes) — that is the map
  for silent bugs.
- **Assert invariants** (non-empty chunks, count matches, ID
  containment) — cheap insurance at every boundary.
- **Reproduce first** — fixed seeds, pinned inputs, captured config;
  "reproduce on demand" is step one of every fix.
- **One hypothesis at a time** — change one thing, measure, repeat.
- **Dump stacks on hang** — faulthandler enabled in CI/debug runs.
- **Bisect changes** — O(log n) runs over O(n) candidates; `git
  bisect` over commits.
- **Turn every fix into a regression test** — the test is the proof
  the fix worked.

## 7. Complexity and Cost

| Tool | Cost | Failure cost when skipped |
|---|---|---|
| `traceback.format_exc` | O(stack) | Logs without the frames that matter |
| Assertions | O(1) per boundary | Silent corruption ships |
| Leveled logging | O(1) per line | Firehose or blindness |
| Fixed seeds | O(1) | Irreproducible "works on my machine" |
| `faulthandler` | O(stack) on dump | Hours guessing where it hangs |
| `pdb` inspection | O(1) per command | Blind fixes |
| Bisection | O(log n) runs | O(n) manual reverts |
| Hypothesis probes | O(stage) | Three changes, no diagnosis |

**Scale notes:** logging and assertions are O(1) per boundary — the
cost is negligible at 10k chunks and priceless at 10M. `faulthandler`
dumps are the difference between a 10-minute hang diagnosis and a
2-day mystery. Bisection is the only technique whose cost grows
logarithmically — always reach for it first with large candidate sets.

## 8. AI Engineering Relevance

- **Silent correctness failures are the AI bug class.** No traceback,
  just wrong chunks/scores/answers. The assertion + boundary-log +
  fixed-seed method is the standard toolkit.
- **RAG pipelines**: assert embedding count == chunk count, retrieved
  IDs ⊆ corpus, scores in [0, 1]. Each is a stage-boundary invariant.
- **Randomness is everywhere**: sampling, shuffles, augmentation,
  dropout — freeze every seed for a repro; a disappearing bug was a
  randomness bug.
- **Model output is data**: when a model returns malformed JSON, the
  parse failure is at a boundary — log the raw output (redacted).
- **Hangs in batch jobs** (embedding a corpus, provider calls) are
  concurrency bugs: faulthandler shows the blocked `put()`/`get()`.
- **Prompt changes are configs**: bisect prompt revisions like
  commits — the midpoint test is the same O(log n) pattern.

## 9. Practice Exercises

1. **Traceback shape:** build a 3-frame failure; assert
   `format_exc()` starts with the header, contains all frames
   innermost-last, and ends with the message.
2. **Boundary asserts:** add invariants to a fake RAG pipeline
   (non-empty chunks, count preservation); feed it a corrupting stage
   and assert the invariant catches it before the retriever.
3. **Seed freezing:** write a function with an unseeded shuffle;
   show two runs differ; fix with `random.Random(42)`; assert
   reproducibility.
4. **faulthandler on a fake hang:** in a thread stuck on
   `queue.get()`, dump with faulthandler and assert the dump names the
   blocking call.
5. **Bisect:** over 100 configs with the break at index 42, assert
   `bisect_bad` returns 42 in ≤ 8 probe runs (count the probes).
6. **Silent bug drill:** given a `retrieve()` that ranks by length,
   write a hypothesis probe that proves the metric is wrong, then fix
   it and add a regression test.

## 10. Summary

- Read tracebacks **bottom-up**; log **`format_exc`**, never bare
  messages.
- Assert invariants at boundaries — the detector for silent bugs.
- Log at boundaries; freeze seeds; dump stacks; bisect changes.
- `pdb` for live inspection; `faulthandler` for hangs.
- The method: **reproduce → isolate → hypothesize → prove → fix +
  regression test**. One hypothesis at a time.

## 11. Quick Reference

| Need | Tool |
|---|---|
| Where did it break? | Read the traceback's last frame first |
| Log the full stack | `traceback.format_exc()` / `format_exception` |
| Catch silent corruption | Assertions at stage boundaries |
| See what each stage did | Leveled logging (INFO/DEBUG) |
| Reproduce the flaky bug | Seed `random`/numpy/torch; `PYTHONHASHSEED=0` |
| Where is it hanging? | `faulthandler.enable()` + dump on signal |
| Inspect live state | `breakpoint()`: `n`, `s`, `p`, `w`, `c`, `q` |
| Which change broke it? | `git bisect` / midpoint testing |
| Which stage corrupts data? | Boundary probes (`isolate_stage`) |
| Async failures | `asyncio.run(debug=True)`; read the await chain |
| Child process failing | Capture child stderr; check `returncode` |

## 12. Next Steps

- **`33-security-essentials`** — assertion-driven debugging is also the
  validation layer: the same invariants that catch bugs catch attacks.
- **`31-concurrency-patterns`** — the R1.1 hang is the canonical
  faulthandler case: a producer blocked on a full queue.
- **`08-mlops`** — observability: structured logs, eval harnesses, and
  regression tests are this topic's production form.
- Practice on a real silent bug: break a RAG pipeline deliberately
  (wrong metric, dropped chunks, bad seed) and run the five-step
  method end-to-end — that drill is the interview question and the
  daily job, in one.
