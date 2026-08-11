# Practice Authoring Spec

Every topic in this module gets one **challenge set** plus an entry in its module
**workbook**. This file is the contract: an authored set that violates it is a bug.

Reference implementation to copy from:
[`01-core-python/challenges/49-collections-toolkit/`](01-core-python/challenges/49-collections-toolkit/).

## 1. Layout

One `challenges/` directory per module (or per library / database / framework
inside a module), with one leaf per topic. The leaf name **must equal the topic
directory name** so the pairing is mechanical:

```
<module>/challenges/<NN-topic-name>/
├── README.md          # real-world problem + Bronze/Silver/Gold statements
├── starter.py         # signatures only, bodies raise NotImplementedError
├── solution.py        # reference implementation, each docstring says WHY
├── test_challenge.py  # pytest; runs against starter by default
└── quiz.md            # 8 recall questions + answer key
```

`<module>/challenges/README.md` indexes the module's sets. Do **not** also nest a
`challenges/` dir inside the topic dir — `02-advanced-python` currently has both
and they are byte-identical duplicates; new work uses the central path only.

## 2. The three tiers

| Tier | Time | Purpose |
|---|---|---|
| 🥉 Bronze | ~15 min | mechanics. Any correct approach passes. |
| 🥈 Silver | ~35 min | the *right* structure. A naive-but-correct solution must **fail** a measured guard. |
| 🥇 Gold | ~75 min | production constraint: scale, memory ceiling, failure, security, or cost. Ends with a **Follow-up** question ("what breaks first at 10^9?"). |

Silver and Gold are only meaningful if a wrong-complexity solution *fails*. If you
cannot write a guard that separates good from naive, the tier is under-specified —
redesign the task, don't weaken the test.

## 3. Verification rules (non-negotiable)

1. **Never assert on wall-clock time.** It is flaky across machines and under CI
   load. Measure the thing you actually care about:
   - **Comparisons / operations** — wrap values in a counting object
     (see `CountingFloat` in the reference set) and assert a budget like
     `counter[0] <= 10 * n`. This is how you prove O(n log k) beat O(n log n).
   - **Memory** — `tracemalloc.start()`, then assert `peak < N * 1024 * 1024`.
     This is how you prove a stream was never materialized.
   - **Call counts** — a fake/spy asserting how many times an API was hit
     (retries, caching, batching).
   - **Query counts** — count SQL statements to prove an N+1 was fixed.
2. **Deterministic data only.** Seed every RNG (`random.Random(42)`) or use a
   closed form (`(i * 7919) % 10**6` gives distinct, non-monotonic values).
   Never `Date.now()`-style or unseeded randomness.
3. **Default target is `starter.py`,** so a fresh clone's tests *fail loudly* with
   `NotImplementedError`. Validate the reference with an env var:
   ```python
   TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
   ```
   Load it via `importlib.util.spec_from_file_location` — never a package import,
   because these directories are not importable packages.
4. **Cover the edges explicitly:** empty input, `k == 0`, `k > n`, duplicates,
   negatives, ties (and assert the documented tie-break), single element.
5. **Adversarial case for the guard.** Include the input that is the *worst case*
   for the intended solution (e.g. strictly descending input for a top-k heap),
   so passing isn't luck.
6. **No network, no paid API calls, no service dependency** in tests. Fake the
   LLM/DB/HTTP boundary with a local double. A test must pass offline.
7. **Skip, don't fail, on a missing optional dependency:**
   `pytest.importorskip("torch")`.

## 4. Framing: every topic is an AI-engineering topic

Even `if-else` and `strings` are framed with a production AI scenario, because the
learner's goal is shipping AI systems. The scenario must be *real* — a problem
that actually occurs — not a cosmetic rename.

| Topic area | Real framing to use |
|---|---|
| strings / formatting | prompt templating, token-safe truncation, PII redaction |
| lists / tuples | batch construction for inference, embedding buffers |
| sets | dedup of retrieved chunks, stop-word filtering |
| dicts | vector-store metadata filters, per-tenant config |
| collections / heapq | **top-k retrieval** (the canonical one) |
| if-else / match | routing a request across model tiers, guardrail decisions |
| loops / iterators | streaming token consumption, chunked file ingest |
| generators | lazy corpus pipelines that can't fit in memory |
| decorators | retry with backoff, cost/latency instrumentation, caching |
| context managers | span tracing, connection and GPU-memory lifetime |
| async | fan-out over provider calls, rate-limit-aware concurrency |
| dataclasses / pydantic | structured LLM output, config validation |
| exceptions | provider 429/500 taxonomy, partial-batch failure |
| datetime | trace timestamps, UTC-vs-local drift in evals |
| pathlib / serialization | artifact and checkpoint layout, cache keys |
| numpy | embedding math, cosine similarity, broadcasting |
| pandas | eval result frames, leakage-free feature tables |
| SQL / ORM | metadata store, N+1 in a retrieval API |
| FastAPI | model-serving endpoint, streaming SSE, idempotency |
| DSA | ANN graph traversal, LRU cache, tokenizer trie |
| ML | leakage, calibration, threshold choice under class imbalance |

**Cost, latency, and failure are first-class.** A Gold tier should frequently force
a number: dollars per 1k requests, P95 budget, memory ceiling, retry amplification.

## 5. README.md structure

Open with 2–3 lines naming the production problem — no throat-clearing. Then per
tier: **Task**, **Signature** (fenced `python`), an **input/expected table**, and
**Constraints** stating the guard in plain terms ("tests count comparisons and
assert under `10 * n`; `sorted()[:k]` is ~17x over budget"). Close with a
`## Running` block and the `## Test File Structure` tree.

State the tie-break and ordering contract in the README. If the test asserts an
order the README didn't promise, that's a spec bug, not a learner error.

## 6. solution.py

Every function's docstring begins **"Why this approach:"** and names the
complexity against the alternative that loses — that comparison *is* the lesson:

```python
def top_k_scores(scores: Iterable[float], k: int) -> list[float]:
    """Return the k largest scores, descending.

    Why this approach: heapq.nlargest scans once, keeping a heap of size k —
    O(n log k) time, O(k) space. sorted()[:k] would be O(n log n); at
    n=10^6, k=10 that is ~20M comparisons vs ~1M.
    """
```

## 7. quiz.md

Exactly 8 single-line multiple-choice questions on the mechanics a learner
plausibly gets wrong, then `**Answers:** 1-B, 2-B, ...`. Test decisions and
consequences ("for top-k of a million scores the right tool is…"), not trivia.

## 8. Style

Python ≥ 3.10, `from __future__ import annotations`, builtin generics
(`list[str]`), type-hinted signatures, line length 100. **ASCII only** in `.py`
files — the Windows console is cp1252 and box-drawing characters crash it
(regression: commit 1d31fa4). Emoji are fine in Markdown. `starter.py` and
`solution.py` are excluded from lint in `pyproject.toml`; tests are not.

## 9. Module workbook

Each module gets `<module>/PRACTICE.md`: the section-level narrative that the
per-topic sets hang off, following
[`docs/curriculum/practice/README.md`](../../../docs/curriculum/practice/README.md) —
a **real-world problem per section** used as the lens, then per topic a
**Mastery =** line (observable: "you can build X, explain Y, debug Z"), the three
tiers linked to the challenge dir, and an exact **Verify** command.

## 10. Definition of done

```bash
# fails with NotImplementedError — proves tests target the starter
pytest <module>/challenges/<NN-topic>/test_challenge.py -q

# all green — proves the reference solution satisfies every guard
CHALLENGE_USE_SOLUTION=1 pytest <module>/challenges/<NN-topic>/test_challenge.py -q
```

Both must hold. Additionally: the naive solution you named in Constraints must
actually fail its guard — verify by writing it and watching it fail, not by
assuming.
