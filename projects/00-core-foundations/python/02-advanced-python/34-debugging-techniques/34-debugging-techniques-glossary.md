# 34 — Debugging Techniques Glossary

## Quick Reference

| Term | Definition | Complexity |
|---|---|---|
| Traceback | The exception frame chain, printed outside-in | O(stack) |
| Innermost frame | The last (bottom) frame — where the exception was raised | O(1) to find |
| `traceback.format_exc` | Full stack as a string, for logs | O(stack) |
| `format_exception` | `(type, value, tb)` → formatted lines | O(stack) |
| Assertion-driven debugging | Asserting invariants at stage boundaries | O(1) per assert |
| Stage boundary | The edge between pipeline stages; where to log/assert | — |
| Leveled logging | INFO boundaries / DEBUG intermediates | O(1) per line |
| Seed freezing | Pinning `random`/numpy/torch for reproducible repros | O(1) |
| `PYTHONHASHSEED` | Env var controlling str/bytes hash randomization | O(1) |
| `faulthandler` | Dumps Python stacks on signals or on demand | O(stack) per dump |
| Hang | A process blocked forever, with no exception | — |
| `pdb` | The interactive debugger; `breakpoint()` enters it | O(1) per cmd |
| `cmdqueue` | Pdb's scripted command queue (deterministic sessions) | O(cmds) |
| Post-mortem debugging | Inspecting state after the crash | — |
| Bisection | Binary search over changes/configs; O(log n) runs | O(log n) |
| `git bisect` | Automated bisection over commits | O(log n) |
| Hypothesis-driven method | Reproduce → isolate → hypothesize → prove → fix | — |
| Probe | A tiny experiment that confirms/kills one hypothesis | O(stage) |
| Silent bug | Wrong output with no exception — the AI bug class | — |
| Regression test | A test that fails on the old behavior, proving the fix | O(1) |
| Await chain | The coroutine call path shown in async tracebacks | O(depth) |
| Child stderr | A subprocess's error output — capture it separately | O(output) |

## Detailed Definitions

### Traceback
**Definition:** The exception report listing every frame from the entry
point to the raise site. Printed **outside-in**: the last (bottom) frame
is where the exception was raised — always read from the bottom up.

```python
try:
    _outer()
except ValueError:
    tb = traceback.format_exc()
lines = tb.strip().splitlines()
print(lines[0])    # Traceback (most recent call last):
print(lines[-1])   # ValueError: chunk index out of range
```

**Related Terms:** Innermost frame, `traceback.format_exc`

### Innermost frame
**Definition:** The bottom frame of a traceback — the one where the
exception was actually raised. It names the exact function and line;
the frames above explain how execution arrived there.

**Related Terms:** Traceback

### `traceback.format_exc`
**Definition:** Returns the current exception's full traceback as a
string — the thing to log. `print(exc)` keeps only the message and
discards the frames that make the bug findable.

```python
import traceback
try:
    1 / 0
except ZeroDivisionError:
    log_text = traceback.format_exc()   # full stack for the log
```

**Related Terms:** Traceback, `format_exception`

### `format_exception`
**Definition:** `traceback.format_exception(type(exc), exc,
exc.__traceback__)` — formats an exception you *caught* (not the
current one) into lines, for custom logging.

**Related Terms:** `traceback.format_exc`

### Assertion-driven debugging
**Definition:** Using `assert` at stage boundaries to state invariants
("every chunk non-empty", "embeddings == chunks"). A crash says *where*;
an assertion says *what is wrong* — the difference between debugging
and guessing.

```python
assert len(embeddings) == len(chunks), "count mismatch at boundary"
```

**Related Terms:** Stage boundary, Silent bug

### Stage boundary
**Definition:** The edge between pipeline stages (chunking → embedding
→ retrieval → rerank). The canonical place to log counts/shapes and
assert invariants — silent corruption usually first appears at a
boundary.

**Related Terms:** Assertion-driven debugging, Leveled logging

### Leveled logging
**Definition:** Using logging levels as the debugging instrument: INFO
for stage boundaries (cheap, always on), DEBUG for intermediate values
(off in prod, on in the repro). Print-debugging has no levels and no
off switch.

**Related Terms:** Stage boundary

### Seed freezing
**Definition:** Pinning every random source (`random.seed(42)`, numpy,
torch, dataset shuffles) so the buggy run reproduces identically. A
bug that disappears when seeded was a randomness bug — that is the
diagnosis.

**Related Terms:** `PYTHONHASHSEED`, Silent bug

### `PYTHONHASHSEED`
**Definition:** Environment variable controlling hash randomization
for strings/bytes. `PYTHONHASHSEED=0 python repro.py` fixes set/dict
iteration order — the repro tool for "works on my machine" ordering
bugs.

**Related Terms:** Seed freezing

### `faulthandler`
**Definition:** `faulthandler.enable()` registers handlers that dump
Python stack traces on SIGSEGV/SIGABRT (crashes) and can be triggered
manually with `faulthandler.dump_traceback(file=...)`. The first tool
for hangs: dump the stack and see exactly where every thread blocks.

```python
import faulthandler
faulthandler.enable()          # dump on crash signals
faulthandler.dump_traceback()  # manual dump: "where am I?"
```

**Related Terms:** Hang

### Hang
**Definition:** A process blocked forever with no exception — typically
a concurrency bug (the R1.1 producer waiting on a full queue). No
traceback exists for a hang; faulthandler creates one on demand.

**Related Terms:** `faulthandler`

### `pdb`
**Definition:** Python's interactive debugger; `breakpoint()` enters it.
Key commands: `n` next, `s` step, `p expr` print, `l` list, `w` where,
`u`/`d` up/down the stack, `c` continue, `q` quit.

**Related Terms:** `cmdqueue`, Post-mortem debugging

### `cmdqueue`
**Definition:** Pdb's attribute holding queued commands, consumed
without stdin — how scripts and CI run deterministic pdb sessions
(`cap.cmdqueue = ["n", "p x", "c"]`).

**Related Terms:** `pdb`

### Post-mortem debugging
**Definition:** Inspecting program state after a crash: `pdb.pm()`
opens pdb at the last exception's frame. Faster than re-running when
the failure is expensive to reproduce.

**Related Terms:** `pdb`

### Bisection
**Definition:** Binary search over changes, configs, or inputs: test
the midpoint, keep the failing half, repeat — O(log n) runs for n
candidates. 100 candidates → 7 runs.

**Related Terms:** `git bisect`

### `git bisect`
**Definition:** Git's automated bisection over commits: mark a commit
good/bad, and it binary-searches the first failing commit for you.

**Related Terms:** Bisection

### Hypothesis-driven method
**Definition:** The debugging loop: **reproduce → isolate → hypothesize
→ prove → fix + regression test**. One hypothesis at a time; never fix
blind. The method behind every "hard" bug.

**Related Terms:** Probe, Silent bug

### Probe
**Definition:** A tiny experiment designed to confirm or kill one
hypothesis — e.g. printing `retrieve()`'s ranking order to prove the
metric is length, not similarity.

**Related Terms:** Hypothesis-driven method

### Silent bug
**Definition:** Wrong output with no exception — the AI bug class (RAG
returns wrong chunks, scores inverted, dropped items). Only detectable
by invariants, boundary logs, and probes.

**Related Terms:** Assertion-driven debugging, Hypothesis-driven method

### Regression test
**Definition:** A test asserting the *fixed* behavior — it must fail
on the old code. The proof the fix worked, and the guard against
recurrence.

**Related Terms:** Hypothesis-driven method

### Await chain
**Definition:** The coroutine call path shown in Python 3.11+ async
tracebacks — the async equivalent of the call stack. Failures surface
at `await` points; read the chain like a traceback.

**Related Terms:** Silent bug

### Child stderr
**Definition:** A subprocess's error output. Your traceback is not the
child's — capture `stderr` separately, set a timeout, check
`returncode`. An unread child stderr is a bug that looks like your
code's fault.

**Related Terms:** Silent bug

## Key Concepts Summary

1. **Read tracebacks bottom-up.** The innermost frame is the raise
   site; the frames above are the journey. This one habit solves most
   "where do I start" paralysis.
2. **Assertions catch what crashes cannot.** Silent corruption is
   caught by invariant assertions at stage boundaries — the AI bug
   class's only detector.
3. **Reproduce or die.** Freeze every seed and pin inputs; a bug you
   cannot reproduce on demand cannot be fixed, and a bug that
   disappears when seeded was a randomness bug.
4. **Log at boundaries, dump on hangs.** INFO/DEBUG at stage edges is
   the map; faulthandler is the flashlight for hangs.
5. **One hypothesis at a time.** Reproduce → isolate → hypothesize →
   prove → fix + regression test. Change one thing, measure, repeat.

## Practice Terms

1. **Why read a traceback from the bottom?**
   *Answer:* The last (bottom) frame is where the exception was
   raised — the innermost scope. Frames above are callers; starting at
   the raise site tells you *what* broke before *how you got there*.
2. **Why is `print(exc)` insufficient in logs?**
   *Answer:* It keeps only the message; the frame chain — the path to
   the failure — is discarded. `traceback.format_exc()` logs the full
   stack, so the log itself is debuggable.
3. **What makes a bug "silent", and how do you catch it?**
   *Answer:* Wrong output with no exception (RAG wrong chunks). Catch
   it with invariants asserted at stage boundaries (counts, IDs,
   shapes), boundary logs, and hypothesis probes that inspect
   intermediates.
4. **How do you reproduce an intermittent failure?**
   *Answer:* Freeze every random source (`random.Random(42)`, numpy,
   torch), pin inputs and config, and fix hash order with
   `PYTHONHASHSEED=0`. If it stops failing when seeded, the diagnosis
   is randomness/ordering.
5. **What is the first tool for a hang?**
   *Answer:* `faulthandler` — enable it (or dump on signal) to get a
   stack trace showing exactly where every thread is blocked. The R1.1
   producer stuck in a queue `put()` becomes visible in one line.
