# Phase 1 — Core Python (`01-core-python/`)

> **Current:** 41 exercises, 41 lectures, 41 glossaries. **40/40 runnable files pass.**
> This is the healthiest section in the module — the work here is *depth*, not repair.
>
> **Target:** 52 exercises (+11), all 52 self-verifying, all lectures carrying
> complexity and AI-relevance.

---

## 1. What Is Already Good

Do not rewrite these. The audit found genuine quality:

| Strength | Evidence |
|---|---|
| Every file runs | 40/40 pass (`33-user-input.py` needs stdin, expected) |
| Consistent teaching voice | `# Example N:` + `# =====` rules + inline expected output |
| Objectives everywhere | `Learning Objectives` in **41/41** lectures |
| Mistakes taught | `Common Mistakes` in **39/41** |
| Practice everywhere | `Practice Exercises` + `Best Practices` + `Summary` in **41/41** |
| Right instincts | `13-lists.py` teaches copy-vs-reference; `21-functions` warns on mutable defaults |
| Practice set with parity | `practice_all.py` 99 solutions ↔ `practice_no_solutions.py` 99 stubs |

---

## 2. Gaps Specific to Phase 1

| Gap | Measured |
|---|---|
No self-verification | **0 of 44** `.py` files contain `assert` |
No cost model | **2 of 41** lectures mention complexity |
Practice not gradeable | **146** `input()` calls across 99 problems |
Missing stdlib | 21 concepts at 0 occurrences (§4) |
Template drift | `Topic Overview` 28/41, `Quick Reference` 14/41, `Next Steps` 13/41 |
Glossary schemes | 3 competing (01–14, 15–33, 34–41) |
No forward links | **0 of 41** lectures link to Phase 2 |
Deprecated-first | `pathlib` in 1 file; `38-file-handling.py` teaches string paths |

---

## 3. Retrofit of the Existing 41 (Tier 1)

### 3.1 Add `_verify()` to all 41 files
Append the standard block from [01-content-standards.md](01-content-standards.md) §2.
Keep every existing `print()` — only add. Per-file assert targets:

| File | Assert targets |
|---|---|
`06-variables` | scoping, unpacking, swap, `is` vs `==` on small ints |
`07-data-types` | `type()` for all builtins, mutability matrix |
`08-numbers` | int/float/complex ops, `0.1+0.2 != 0.3`, `math.isclose` |
`09-casting` | round-trips, `int("3.7")` raises, `int(3.7)` truncates |
`10-strings` | slicing, methods, immutability raises `TypeError` |
`11-booleans` | truthiness of `0 "" [] {} None`, `bool` is `int` subclass |
`12-operators` | precedence, `//` vs `/`, `%` on negatives, chained comparison |
`13-lists` | mutation, slice assignment, copy-vs-reference, `deepcopy` |
`14-tuples` | immutability raises, single-element `(x,)`, unpacking |
`15-sets` | dedup, set algebra, `frozenset` hashable, unordered |
`16-dictionaries` | insertion order (3.7+), `get` default, `setdefault`, merge `\|` |
`17-if-else` | branch selection, ternary, truthiness pitfalls |
`18-match` | literal/sequence/mapping/class patterns, guards, wildcard |
`19-while` / `20-for` | `else` clause fires only without `break`; loop-var leak |
`21-functions` | `*args`/`**kwargs`, mutable-default trap, closure capture, LEGB |
`22-range` | half-open interval, negative step, `range` is lazy |
`23-arrays` | `array` typecodes vs `list`, `bytes` immutability |
`24-iterators` | protocol, `StopIteration`, exhaustion, generator laziness |
`25-modules` | import machinery, `__name__`, `sys.path`, circular-import failure |
`26-dates` | arithmetic, `strftime`/`strptime` round-trip, **naive vs aware** |
`27-math` | `isclose`, `inf`/`nan` semantics (`nan != nan`), domain errors |
`28-json` | round-trip, `default=`, non-str keys coerced, `NaN` non-standard |
`29-regex` | groups, greedy vs lazy, `findall` vs `finditer`, catastrophic backtracking |
`30-try-except` | ordering, `else`/`finally`, `finally` overriding return, custom types |
`31-string-formatting` | f-string vs `.format()` vs `%`, `f"{x=}"`, spec mini-language |
`32-none` | `is None` not `== None`, sentinel pattern, implicit return |
`33-user-input` | refactor to `parse_input(str)` so it becomes testable |
`34-classes` | attribute lookup, class-vs-instance state, `__str__`/`__repr__` |
`35-inheritance` | MRO order, `super()` chain, `__mro__`, diamond |
`36-polymorphism` | duck typing, operator overloading, `isinstance` vs duck |
`37-encapsulation` | name mangling `_Class__attr`, `@property` validation |
`38-file-handling` | read/write round-trip, `with` closes on exception, encoding |
`39-pip` / `40-virtualenv` | parse `requirements.txt`, compare versions (offline) |
`41-inner-classes` | nesting, closure over outer, when to prefer composition |

**Note on 39/40:** these are shell-oriented. Rewrite the testable core as pure
functions (`parse_requirement("pkg>=1.2")`) and keep shell commands as comments.

### 3.2 Make the practice set gradeable
`practice_all.py` has **146** `input()` calls, so none of the 99 problems can be
auto-graded. Add (do not replace):

```
practice_testable.py       # 99 pure functions: solve_01(name: str) -> str
practice_stubs.py          # same signatures, NotImplementedError
tests/test_practice.py     # parametrized cases per problem
```
Originals stay for the interactive experience.

### 3.3 Retrofit lectures
For all 41: add `## Complexity and Cost` (where structures appear) and
`## AI Engineering Relevance` (all). Highest-value examples:

| Lecture | Complexity to state | AI-relevance hook |
|---|---|---|
`13-lists` | `insert(0)` O(n), `append` O(1) amortized, `x in list` O(n) | batching inference inputs; why `deque` for a sliding context window |
`15-sets` | membership O(1) vs list O(n) | dedup document IDs in a retrieval set |
`16-dictionaries` | O(1) average, O(n) worst; ordered since 3.7 | token→id vocab maps; feature dicts |
`24-iterators` | O(1) memory streaming | streaming a 10GB JSONL corpus that will not fit in RAM |
`29-regex` | backtracking can be exponential | cleaning scraped training text; ReDoS as a real DoS vector |
`30-try-except` | try is ~free, except is costly | retry/backoff around flaky LLM API calls |
`38-file-handling` | buffered vs unbuffered | reading shards, checkpointing |

### 3.4 Normalize headings
27 lectures (29–41 and others) and 27 glossaries need heading alignment to the
canonical templates. Mechanical, scriptable, low-risk. Expand the five thin
glossaries: `33-user-input` (159 lines), `39-pip` (178), `32-none` (187),
`36-polymorphism` (189), `40-virtualenv` (206) → ~300 each.

### 3.5 Add forward links
0 of 41 currently link to Phase 2. Add `Continues in:` to `## Next Steps`:

| From | To |
|---|---|
`21-functions` | `02-advanced-python/01-decorators`, `/09-functools` |
`24-iterators` | `02-advanced-python/02-generators`, `/10-itertools` |
`30-try-except` | new `47-exceptions-advanced` |
`34–37` (OOP) | `/06-dataclasses`, `/08-abc`, `/12-property`, `/15-descriptors` |
`38-file-handling` | new `42-pathlib`, `/03-context-managers` |
`13/15/16` | new `49-collections-toolkit`, `/11-collections` |

---

## 4. New Topics 42–52 (Tier 2)

Eleven topics closing the stdlib gap. Every one is measured at **0 occurrences**
in the current 41 files, and every one is used daily in AI/backend work.

### 42 — `42-pathlib.py`
**Why:** `pathlib` appears in exactly 1 file while `38-file-handling` teaches
string paths — the deprecated habit is taught first.
**Concepts:** `Path` construction, `/` operator, `.parent`/`.stem`/`.suffix`,
`glob`/`rglob`, `exists`/`is_file`, `mkdir(parents=True, exist_ok=True)`,
`read_text`/`write_text`, `os.path` → `pathlib` migration table, Windows vs POSIX
separators, `resolve()` vs `absolute()`.
**Asserts:** path composition, suffix replacement, glob counts on a temp tree,
round-trip `write_text`/`read_text`.
**AI relevance:** walking a dataset directory of 100k images; locating model
checkpoints; building output paths that work on Windows and Linux CI alike.

### 43 — `43-dataclasses-and-namedtuples.py`
**Why:** `dataclass` at 0 occurrences in Phase 1 despite 4 OOP lectures.
**Concepts:** `@dataclass`, `field(default_factory=...)`, `frozen=True` (hashable),
`order=True`, `slots=True` (3.10+), `__post_init__`, `NamedTuple`, `TypedDict`,
comparison table dict vs dataclass vs NamedTuple vs class.
**Asserts:** frozen raises `FrozenInstanceError`; `default_factory` gives distinct
lists; `order=True` sorts; `slots=True` blocks new attrs.
**AI relevance:** config objects, a `RetrievedChunk(text, score, source)` record,
model hyperparameters. `slots=True` matters at a million records.

### 44 — `44-logging.py`
**Why:** 0 occurrences. Nothing ships without logging; `print()` is not observability.
**Concepts:** five levels, logger hierarchy and propagation, handlers
(`Stream`/`File`/`Rotating`), formatters, `logging.config.dictConfig`,
`exc_info=True` vs `logger.exception`, lazy `%s` args vs f-strings, structured
JSON logging, `logging` vs `print`, per-module `getLogger(__name__)`.
**Asserts:** `caplog`-style capture, level filtering, propagation, formatter output shape.
**AI relevance:** tracing a RAG request end to end; logging token counts and
latency per call; correlation IDs across an async pipeline.
**Cross-ref:** deeper treatment in `02-advanced-python/19-logging.py` (fix R1.6 first).

### 45 — `45-testing-with-pytest.py`
**Why:** 0 occurrences of `pytest`/`unittest`/`assert` in all of Phase 1.
**Concepts:** test discovery, plain `assert`, `pytest.raises`,
`@pytest.mark.parametrize`, fixtures and scope, `tmp_path`, `monkeypatch`,
`unittest.mock` (`Mock`, `patch`, `side_effect`), coverage, AAA structure,
what not to test.
**Asserts:** the file's own tests, run in-process.
**AI relevance:** testing a chunking function's boundaries; mocking an LLM API so
tests are free and deterministic; golden-file tests for prompt templates.

### 46 — `46-cli-and-config.py`
**Why:** `argparse`, `sys.argv`, `os.environ` all at 0.
**Concepts:** `sys.argv`, `argparse` (positional, optional, flags, subcommands,
types, defaults, `--help`), `os.environ` + `.get` defaults, `.env` loading,
12-factor config, precedence CLI > env > file > default, exit codes, `sys.stderr`.
**Asserts:** parser on synthetic `argv`; precedence resolution; bad input exits non-zero.
**AI relevance:** every training script is a CLI (`train.py --epochs 10 --lr 3e-4`);
API keys come from env, never source.

### 47 — `47-exceptions-advanced.py`
**Why:** `raise from` 0, `ExceptionGroup` 0, custom hierarchies in 1 file.
**Concepts:** custom exception hierarchies with a package base, `raise ... from`
(chaining vs `__context__`), `ExceptionGroup` + `except*` (3.11+), EAFP vs LBYL,
`contextlib.suppress`, `finally` semantics and return-override, cleanup ordering,
retry with exponential backoff and jitter, when *not* to catch, narrow excepts,
`sys.exc_info`, traceback formatting.
**Asserts:** `__cause__` set by `from`; `suppress` swallows only the named type;
`finally` overriding a return; a `ValueError` subclass caught as `ValueError`.
**AI relevance:** distinguishing retryable (429/503) from fatal (400) LLM errors;
`ExceptionGroup` for a `gather()` of parallel embedding calls where three of
fifty fail.

### 48 — `48-comprehensions-and-modern-syntax.py`
**Why:** set comprehensions 0, walrus 0, `f"{x=}"` 0 — though the module targets 3.10+.
**Concepts:** list/dict/set comprehensions, nested and conditional, generator
expressions and when they beat lists, walrus `:=`, `f"{x=}"` debugging,
positional-only `/` and keyword-only `*`, structural pattern matching recap,
`zip(strict=True)` (3.10+), `itertools.pairwise`, dict merge `|`, `str.removeprefix`,
comprehension vs `map`/`filter` readability, when a loop is clearer.
**Asserts:** equivalence of comprehension and loop forms; generator is lazy and
one-shot; `zip(strict=True)` raises on length mismatch; walrus scoping.
**AI relevance:** the `[transform(x) for x in batch]` idiom everywhere; generator
expressions to stream a corpus without materializing it.

### 49 — `49-collections-toolkit.py`
**Why:** `deque` 0, `heapq` 0, `bisect` 0. These are the workhorses of retrieval.
**Concepts:** `deque` (O(1) both ends, `maxlen` ring buffer), `heapq`
(`heappush`/`heappop`/`nlargest`/`heapreplace`), `bisect`
(`bisect_left`/`insort`, sorted-list maintenance), `Counter` (`most_common`),
`defaultdict`, `ChainMap`, `OrderedDict` vs dict today. **Complexity table is the
centerpiece.**
**Asserts:** `deque(maxlen=3)` evicts oldest; heap yields sorted order;
`bisect_left` on duplicates; `Counter.most_common` ties.
**AI relevance:** `heapq.nlargest(k, ...)` **is** top-k retrieval;
`deque(maxlen=n)` is a sliding conversation window; `bisect` maintains a sorted
score list in O(log n); `Counter` for token frequency.
**Cost lesson:** top-k by `sorted(...)[:k]` is O(n log n); `heapq.nlargest` is
O(n log k). At n=10⁶, k=10 that is the difference that matters.

### 50 — `50-datetime-and-timezones.py`
**Why:** `zoneinfo`/`timezone` at 0. Naive datetimes are a genuine bug source.
**Concepts:** naive vs aware (**the** core distinction), `zoneinfo.ZoneInfo`
(3.9+), UTC as the storage rule, `datetime.now(timezone.utc)` vs deprecated
`utcnow()`, DST transitions and non-existent/ambiguous local times, ISO 8601 and
`fromisoformat`, Unix timestamps, `timedelta` arithmetic, monotonic clocks for
measurement (`time.monotonic` not `time.time`), `date` vs `datetime`.
**Asserts:** naive−aware subtraction raises `TypeError`; DST gap behavior;
ISO round-trip; `monotonic` never decreases.
**AI relevance:** timestamping inference requests across regions; time-based
train/test splits where a timezone bug leaks the future into training; TTL on cached embeddings.

### 51 — `51-serialization-and-persistence.py`
**Why:** `pickle` 0, `sqlite3` 0 in Phase 1, `csv` in 2.
**Concepts:** `json` limits (no sets/tuples/datetime; `default=`/`object_hook`),
`csv` (`DictReader`/`DictWriter`, quoting, `newline=""` on Windows), `pickle`
(protocols, **security: never unpickle untrusted data**), `pickle` vs `json`
tradeoffs, `sqlite3` (connect, parameterized queries, **never** string
interpolation, transactions, context manager), `shelve`, JSONL for datasets,
binary vs text mode, `struct`, `base64`.
**Asserts:** JSON round-trip loses tuple→list; parameterized query resists
injection; CSV round-trip with embedded commas/newlines; pickle round-trip of a
custom class.
**AI relevance:** JSONL is the standard fine-tuning format; `sqlite3` backs local
vector-store metadata; pickled `.pkl` model artifacts and why that is a supply-chain risk.

### 52 — `52-memory-and-performance.py`
**Why:** `__slots__` 0, `timeit` 0, GIL 0, refcounting/interning/`gc` 0. This is
the most senior-flavored topic in Phase 1 and the strongest AI bridge.
**Concepts:** `sys.getsizeof` vs deep size, `__slots__` (measure the win),
small-int caching and string interning (`is` vs `==` surprises), refcounting +
`gc` for cycles, `timeit` for microbenchmarks, `cProfile` for hot spots,
`tracemalloc`, generators vs lists at scale, `memoryview`/zero-copy slicing,
string concat in a loop O(n²) vs `"".join` O(n), the GIL and why threads help
I/O not CPU, mutable-default and closure-capture leaks.
**Asserts:** `__slots__` instance is smaller; `"".join` beats `+=`; generator
memory is flat vs a list; small ints are interned, large are not.
**AI relevance:** holding 1M×768 float32 embeddings = ~3GB — the calculation
every AI engineer must be able to do on a whiteboard; why `float32` over
`float64` halves your bill; batch size vs OOM; the GIL as the reason inference
servers use processes or async, not threads.

---

## 5. Deliverables

| Item | Count |
|---|---|
New exercises `42`–`52` | 11 |
New lectures | 11 |
New glossaries | 11 |
`_verify()` retrofits | 41 |
Lecture retrofits (complexity + AI relevance) | 41 |
Heading normalizations | ~27 lectures + ~27 glossaries |
Glossary expansions | 5 |
`practice_testable.py` + stubs + tests | 3 |
Code challenges (`challenges/NN/`) | 52 dirs × 3 tiers |
Quizzes (→ 1 per topic) | 44 new |

---

## 6. Sequencing

| Step | Work | Depends on |
|---|---|---|
| 1 | `_verify()` in all 41 | Tier 0 green |
| 2 | `practice_testable.py` | step 1 |
| 3 | Heading normalization + 5 glossary expansions | — (parallel) |
| 4 | Complexity + AI-relevance retrofit | step 3 |
| 5 | New topics `42`–`52` | steps 1–2 (they follow the new standard) |
| 6 | Forward links | step 5 |
| 7 | Challenges + quizzes | step 5 |

Steps 3 and 5 can run in parallel with different agents; they touch disjoint files.

---

## 7. Exit Criteria

- [ ] 52 exercises, each ending in a passing `_verify()` with ≥5 asserts
- [ ] `python run_smoke_tests.py --phase 1 --verify` exits 0
- [ ] 52 lectures with all 12 canonical sections
- [ ] 52 glossaries, one scheme, ≥15 terms, ≥250 lines
- [ ] 99 practice problems gradeable via `pytest`
- [ ] Every lecture forward-links, including cross-phase
- [ ] Every collection/algorithm topic has a complexity table
- [ ] Zero W3Schools-only references — `docs.python.org` primary

---

*Phase 1 of [00-MASTER-PLAN.md](00-MASTER-PLAN.md). Templates: [01-content-standards.md](01-content-standards.md).*
