# Phase 2 — Advanced Python (`02-advanced-python/`)

> **Current:** 20 exercises, 20 lectures, 20 glossaries. **17/20 pass — 3 fail.**
> **Target:** 34 exercises (+14), all self-verifying, all carrying cost models.
>
> This section has the **best lecture quality in the module** (the decorators
> lecture is genuinely excellent) and the **worst cost coverage**: `0 of 20`
> lectures mention complexity, in the section that teaches `__slots__`,
> `functools`, and `itertools`.

---

## 1. Current State

| Topic | File | Health |
|---|---|---|
| 01 | `01-decorators.py` | ✅ pass — exemplary lecture, use as the reference |
| 02 | `02-generators.py` | ✅ pass |
| 03 | `03-context-managers.py` | ✅ pass |
| 04 | `04-async-await.py` | ✅ pass |
| 05 | `05-type-hints.py` | ✅ pass |
| 06 | `06-dataclasses.py` | ✅ pass |
| 07 | `07-enum.py` | ✅ pass |
| 08 | `08-abc.py` | ✅ pass |
| 09 | `09-functools.py` | ✅ pass |
| 10 | `10-itertools.py` | ✅ pass |
| 11 | `11-collections.py` | ✅ pass |
| 12 | `12-property.py` | ✅ pass |
| 13 | `13-slots.py` | ✅ pass |
| 14 | `14-metaclasses.py` | ✅ pass |
| 15 | `15-descriptors.py` | ❌ **R1.7** `TypeError: salary must be float, got int` |
| 16 | `16-threading.py` | ✅ pass |
| 17 | `17-multiprocessing.py` | ❌ **R1.5** closure not picklable on Windows spawn |
| 18 | `18-unit-testing.py` | ✅ pass |
| 19 | `19-logging.py` | ❌ **R1.6** `PermissionError` — handler holds temp file |
| 20 | `20-patterns.py` | ✅ pass |

Fix the three per [10-remediation-backlog.md](10-remediation-backlog.md) before extending.

---

## 2. Gaps Specific to Phase 2

| Gap | Measured | Consequence |
|---|---|---|
No cost model | **0 of 20** lectures mention complexity | `13-slots` teaches memory optimization without measuring memory; `10-itertools` never states laziness cost |
No self-verification | **0 of 21** `.py` files contain `assert` | Hid R1.5–R1.7 |
No AI framing | 0 lectures reference AI/ML | `04-async-await` is *the* concurrency primitive for LLM calls, taught abstractly |
Concurrency shallow | 3 files (`16`,`17`,`04`), no comparison | The "threads vs processes vs async" decision is the most common senior interview question and is never posed |
Missing modern typing | `Protocol` in 8 lectures but `TypeVar`/`ParamSpec`/`TypeAlias`/generics-syntax thin; `mypy` in 1 | Cannot write typed library code |
No packaging | Nothing on building/distributing a package | Cannot ship internal libraries |

---

## 3. Retrofit of the Existing 20 (Tier 1)

### 3.1 `_verify()` in all 20
| File | Assert targets |
|---|---|
`01-decorators` | `functools.wraps` preserves `__name__`/`__doc__`/`__wrapped__`; stacking order bottom-to-top; factory arity; class decorator state |
`02-generators` | laziness (no work before first `next`); exhaustion; `send`/`throw`/`close`; `yield from` delegation |
`03-context-managers` | `__exit__` runs on exception; returning `True` suppresses; `ExitStack` LIFO order |
`04-async-await` | `gather` concurrency beats sequential; `TimeoutError` on `wait_for`; `Semaphore` caps in-flight; cancellation |
`05-type-hints` | `get_type_hints` output; `Protocol` structural match; `TypeVar` bound enforcement (via mypy in CI) |
`06-dataclasses` | `frozen` raises; `eq`/`order` generated; `slots=True` blocks new attrs |
`07-enum` | identity-based comparison; `auto()`; `Flag` bitwise ops; aliases via `@unique` |
`08-abc` | instantiating abstract raises `TypeError`; registration; `__subclasshook__` |
`09-functools` | `lru_cache` `cache_info` hits/misses; `partial` binding; `total_ordering` fills operators; `singledispatch` routing |
`10-itertools` | `islice` on infinite; `groupby` **requires pre-sorted input** (the classic trap); `tee` independence |
`11-collections` | `Counter` arithmetic; `defaultdict` factory; `deque` rotation; `ChainMap` precedence |
`12-property` | setter validation raises; `cached_property` computes once |
`13-slots` | **measure** `sys.getsizeof` reduction; `__dict__` absent; inheritance caveat |
`14-metaclasses` | registry populated at class creation; `__new__` vs `__init__` order |
`15-descriptors` | `__set_name__`; data vs non-data precedence; per-instance storage (**fix R1.7 here**) |
`16-threading` | `Lock` prevents the race (assert the unsynchronized version *does* corrupt); `Event`/`Condition`; pool results |
`17-multiprocessing` | pool map correctness; workers at module scope (**fix R1.5**); shared `Value` needs a lock |
`18-unit-testing` | mock call counts; `side_effect`; `patch` scope; fixture teardown |
`19-logging` | capture per level; propagation; handler cleanup (**fix R1.6**) |
`20-patterns` | singleton identity; factory dispatch; observer notification; strategy swap |

### 3.2 Add the missing cost models
`0 of 20` today. Highest-value additions:

| Lecture | Must state |
|---|---|
`13-slots` | Actual bytes saved per instance, measured. At 10⁶ objects this is hundreds of MB |
`09-functools` | `lru_cache` is O(1) lookup + unbounded memory when `maxsize=None`; keys must be hashable |
`10-itertools` | Lazy = O(1) memory; `tee` buffers and can be O(n); `product` is combinatorial |
`11-collections` | Full table: `deque` O(1) ends vs `list` O(n) front; `Counter.most_common` O(n log n) |
`02-generators` | O(1) memory vs O(n) for the list equivalent — with a measurement |
`16`/`17`/`04` | Thread ≈8MB stack; process ≈full interpreter; coroutine ≈KB. Drives the choice |
`14-metaclasses` | Class-creation cost paid at import, not per instance |

### 3.3 Add AI-engineering relevance
| Lecture | Hook |
|---|---|
`01-decorators` | `@retry` on 429s; `@cache` on embedding calls; `@timed` for latency SLOs |
`02-generators` | streaming a corpus too large for RAM; token-by-token LLM streaming |
`03-context-managers` | `torch.no_grad()`; DB sessions; temp dirs for model artifacts |
`04-async-await` | 200 concurrent LLM calls; `Semaphore` for rate limits; the single biggest throughput lever |
`05-type-hints` | typed tool schemas for function calling; Pydantic's foundation |
`06-dataclasses` | `RetrievedChunk`; training config objects |
`09-functools` | `lru_cache` on embeddings is the cheapest cost reduction available |
`13-slots` | 1M embedding records in RAM |
`16`/`17` | why inference servers use processes, not threads (the GIL) |
`20-patterns` | Strategy for swapping LLM providers; Factory for retriever backends |

---

## 4. New Topics 21–34 (Tier 2)

### 21 — `21-concurrency-comparison.py` ⭐ highest value
The synthesis the section is missing. Same workload — I/O-bound and CPU-bound —
implemented four ways: sequential, threaded, multiprocess, async. **Measured**
side by side.
**Concepts:** GIL mechanics; when threads help (I/O) and when they cannot (CPU);
process overhead and IPC cost; async as cooperative single-threaded concurrency;
`concurrent.futures` unified API (`ThreadPoolExecutor`/`ProcessPoolExecutor`);
a decision flowchart.
**Asserts:** threads beat sequential on I/O; threads do *not* beat sequential on
CPU; processes do; async has the lowest memory for 1000 tasks.
**AI relevance:** the actual decision behind every inference server. Embedding 10k
documents: async for API-based, processes for local models.

### 22 — `22-asyncio-advanced.py`
**Concepts:** `TaskGroup` (3.11+) vs `gather`; cancellation and shielding;
`asyncio.timeout`; async context managers and iterators; `async for`/`async with`;
queues for producer-consumer; `Semaphore` rate limiting; `run_in_executor` to
bridge sync code; event-loop debugging; **never block the loop**; `anyio`/`trio` note.
**Asserts:** `TaskGroup` cancels siblings on failure; `Semaphore` caps concurrency
observably; a blocking `time.sleep` stalls the loop while `asyncio.sleep` does not.
**AI relevance:** streaming responses from multiple models; bounded-concurrency
embedding pipelines; graceful cancellation when a client disconnects mid-generation.

### 23 — `23-typing-advanced.py`
**Concepts:** `TypeVar` + bounds/constraints, generic classes, `ParamSpec` and
`Concatenate` (typing decorators correctly), `Protocol` + `runtime_checkable`,
`overload`, `Literal`, `Final`, `Annotated`, `TypeAlias` / 3.12 `type`,
`Self`, `NewType`, variance, `TYPE_CHECKING` for cycles, gradual typing strategy,
`mypy --strict` in CI, `cast` and `reveal_type`.
**Asserts:** run `mypy` in-process on inline snippets; assert expected errors are
raised. **Protocol structural checks at runtime.**
**AI relevance:** typing a `Retriever` protocol so Qdrant/Chroma/pgvector are
interchangeable; typed tool signatures for LLM function calling.

### 24 — `24-memory-and-gc.py`
**Concepts:** refcounting; reference cycles and the generational collector; `gc`
module and `gc.get_referrers`; `weakref` and `WeakValueDictionary` for caches;
`__del__` pitfalls; `tracemalloc` leak hunting; interning; `sys.getsizeof` vs deep
size; copy-on-write and `fork` memory sharing; common leak shapes (module-level
caches, closures, unbounded `lru_cache`).
**Asserts:** a cycle survives refcount but not `gc.collect()`; `weakref` clears;
`tracemalloc` reports growth from a known leak.
**AI relevance:** why a long-running inference server's RSS climbs; caching
embeddings without unbounded growth; why `fork` workers share model weights and
`spawn` workers do not.

### 25 — `25-profiling-and-optimization.py`
**Concepts:** `timeit` microbenchmarks and their traps; `cProfile` + `pstats`;
line-level profiling; `tracemalloc`; **measure before optimizing**; algorithmic
wins vs micro-optimization; vectorization as the real answer; `functools.cache`;
`__slots__`; local-variable lookup speed; `str.join`; interpreter overhead and
when to reach for C/Rust/Cython; a case study taking one function from 10s to 100ms.
**Asserts:** the optimized version is faster (with generous margins so CI is
stable — timing printed, ratios asserted loosely).
**AI relevance:** finding the bottleneck in a data pipeline; why a Python loop
over 1M rows is 100× slower than the NumPy equivalent.

### 26 — `26-design-patterns-advanced.py`
Extends `20-patterns.py`.
**Concepts:** Dependency Injection and testability; Repository; Unit of Work;
Strategy vs `singledispatch`; Adapter for provider swaps; Chain of Responsibility
for middleware; Command with undo; Builder for complex configs; Registry/plugin
via `__init_subclass__` or entry points; composition over inheritance;
when a pattern is over-engineering.
**Asserts:** DI enables a fake in tests; registry auto-discovers subclasses;
adapter makes two incompatible APIs interchangeable.
**AI relevance:** a `VectorStore` interface with Qdrant/Chroma/FAISS adapters; a
plugin registry for agent tools; DI so tests never call a real LLM.

### 27 — `27-packaging-and-distribution.py`
**Concepts:** `pyproject.toml` anatomy; src-layout vs flat; editable installs;
`__init__.py` and public API design; `__all__`; semantic versioning; extras;
dependency pinning vs ranges; lockfiles; building sdist/wheel; `uv`/`poetry`/`pdm`
landscape; entry-point console scripts; namespace packages; publishing basics.
**Asserts:** parse and validate a `pyproject.toml`; version comparison ordering;
`__all__` controls `import *`.
**AI relevance:** packaging a shared `rag_utils` library used by three services;
reproducible builds so training runs are reproducible.

### 28 — `28-code-quality-tooling.py`
**Concepts:** `ruff` (lint + format, replacing flake8/isort/black), `black`
philosophy, `mypy` strictness levels, `pre-commit` hooks, complexity metrics,
`bandit` security lint, `pip-audit` for CVEs, `docformatter`/docstring conventions,
CI gating, `# noqa` discipline, editorconfig.
**Asserts:** run `ruff check` on inline bad code and assert the expected rule
fires; assert clean code passes.
**AI relevance:** keeping a fast-moving ML codebase reviewable; catching the
mutable-default and bare-except bugs that plague notebook-derived code.

### 29 — `29-functional-python.py`
**Concepts:** pure functions and referential transparency; immutability and
`frozen` dataclasses; `map`/`filter`/`reduce` and when comprehensions read better;
`operator` module; currying with `partial`; composition; `itertools` as functional
toolkit; recursion and Python's limit; tail-call absence; `functools.reduce`
tradeoffs; side-effect isolation; a functional-core/imperative-shell architecture.
**Asserts:** composition associativity; pure functions are memoizable and
reordering-safe; immutable structures are hashable.
**AI relevance:** pure transforms make data pipelines testable and cacheable;
functional core keeps ML preprocessing reproducible.

### 30 — `30-iterators-protocols-deep.py`
**Concepts:** the full data model — `__iter__`/`__next__`, `__len__`,
`__getitem__` fallback, `__contains__`, `__reversed__`, `__enter__`/`__exit__`,
`__call__`, `__hash__`/`__eq__` contract, `__lt__` + `total_ordering`,
`__getattr__` vs `__getattribute__`, `__set_name__`, `__init_subclass__`,
`__class_getitem__`, `collections.abc` hierarchy, Sequence/Mapping/Set implementation.
**Asserts:** custom Sequence works with `len`/`in`/slicing/`reversed`; breaking the
`__hash__`/`__eq__` contract corrupts dict behavior (demonstrated).
**AI relevance:** a `Dataset` class that works with `len()` and indexing — the
PyTorch `Dataset` protocol; custom containers for batched inference.

### 31 — `31-concurrency-patterns.py`
**Concepts:** producer-consumer with bounded queues and backpressure; worker
pools; fan-out/fan-in; rate limiting (token bucket, sliding window); circuit
breaker; bulkhead isolation; retry with jitter; graceful shutdown and signal
handling; idempotency; deadlock, livelock, starvation; race detection; thread-safe
lazy init.
**Asserts:** backpressure blocks the producer when the queue is full (bounded,
with timeout — **this is the correct version of the R1.1 bug**); circuit breaker
opens after N failures; token bucket enforces the rate.
**AI relevance:** the architecture of a batch embedding job; respecting provider
rate limits without dropping work; circuit-breaking a degraded model endpoint.
**Note:** explicitly reference the `04-queues.py` deadlock (R1.1) as a worked
example of what goes wrong.

### 32 — `32-metaprogramming.py`
**Concepts:** `__init_subclass__` (usually better than a metaclass);
`__set_name__`; class decorators vs metaclasses; `type()` dynamic creation;
`inspect` (signatures, source, stack); `ast` for code analysis; `importlib`
dynamic import and plugin loading; `setattr`/`getattr` patterns; `exec`/`eval`
and why to avoid them; monkey-patching and its costs; descriptors recap;
**when metaprogramming is the wrong answer**.
**Asserts:** `__init_subclass__` registers subclasses; `inspect.signature`
matches; dynamic import loads a module by name.
**AI relevance:** auto-registering agent tools; building JSON schemas from
function signatures for LLM function calling — the exact mechanism behind
`@tool` decorators in agent frameworks.

### 33 — `33-security-essentials.py`
**Concepts:** `secrets` vs `random` for tokens; password hashing (bcrypt/argon2,
never MD5/SHA1); `hmac.compare_digest` for timing-safe comparison; input
validation and injection classes (SQL, command, path traversal); `pickle`
deserialization as RCE; YAML `safe_load`; dependency CVEs; secret management and
never logging credentials; TLS verification; ReDoS; `subprocess` without
`shell=True`; least privilege.
**Asserts:** `compare_digest` used correctly; parameterized SQL resists injection;
path traversal blocked by `Path.resolve().is_relative_to()`; a bad YAML payload is
refused by `safe_load`.
**AI relevance:** prompt injection as the new injection class; untrusted model
output driving tool calls; `.pkl` model files as a supply-chain vector; never
logging API keys.

### 34 — `34-debugging-techniques.py`
**Concepts:** `pdb`/`breakpoint()` and the command set; post-mortem
(`pdb.pm()`); IDE debugging vs print; reading tracebacks properly; `traceback`
module; `faulthandler` for segfaults and hangs; `sys.settrace` basics; logging as
debugging; assertion-driven debugging; bisecting a failure; reproducing
nondeterminism (`PYTHONHASHSEED`, seeds); debugging async code; debugging
subprocesses; rubber-ducking and hypothesis-driven method.
**Asserts:** `traceback.format_exc` shape; `faulthandler` dumps on signal;
deterministic repro under a fixed seed.
**AI relevance:** debugging a RAG pipeline that returns wrong chunks — a silent
correctness failure with no traceback, the hardest and most common AI bug class.

---

## 5. Deliverables

| Item | Count |
|---|---|
Bug fixes (R1.5, R1.6, R1.7) | 3 |
New exercises `21`–`34` | 14 |
New lectures + glossaries | 28 |
`_verify()` retrofits | 20 |
Cost-model retrofits | 20 |
AI-relevance retrofits | 20 |
Challenges | 34 dirs × 3 tiers |
Quizzes | 34 |

---

## 6. Sequencing

| Step | Work | Notes |
|---|---|---|
| 1 | Fix R1.5/R1.6/R1.7 | Tier 0; blocks the rest |
| 2 | `_verify()` in 20 | Locks in behavior before edits |
| 3 | Cost + AI retrofits | Parallelizable per file |
| 4 | **`21-concurrency-comparison`** | Do first among new — highest value, reframes 04/16/17 |
| 5 | `22`, `31` (async, patterns) | Depend on 21 |
| 6 | `23`, `30` (typing, protocols) | Independent |
| 7 | `24`, `25` (memory, profiling) | Pair well; share tooling |
| 8 | `26`–`29`, `32`–`34` | Independent |
| 9 | Challenges + quizzes | After exercises land |

---

## 7. Exit Criteria

- [ ] 34 exercises pass, each with `_verify()` ≥5 asserts
- [ ] Zero failures on Windows and Linux, 3.10 and 3.12
- [ ] Every lecture has a cost model (from 0/20 to 34/34)
- [ ] Every lecture has AI-engineering relevance
- [ ] `mypy --strict` clean on all new files
- [ ] The threads/processes/async decision is answerable with measured evidence
- [ ] Concurrency lectures reference the R1.1 deadlock as a worked example

---

*Phase 2 of [00-MASTER-PLAN.md](00-MASTER-PLAN.md). Templates: [01-content-standards.md](01-content-standards.md). Fixes: [10-remediation-backlog.md](10-remediation-backlog.md).*
