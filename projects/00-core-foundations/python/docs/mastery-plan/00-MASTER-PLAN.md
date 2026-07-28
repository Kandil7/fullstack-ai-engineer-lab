# Python Mastery Plan — Zero to Senior AI Engineer

> **Scope:** the `projects/00-core-foundations/python/` module.
> **Goal:** take this module from a syntax tutorial (W3Schools-derived) to a
> curriculum that produces a **senior AI/backend engineer** — someone who chooses
> constructs by cost and failure mode, not by familiarity.
>
> **Plan created:** 2026-07-29
> **Baseline measured:** 2026-07-29 (all numbers in this plan were measured, not estimated)

---

## Documents in This Plan

| # | Document | What it covers |
|---|----------|----------------|
| 00 | **00-MASTER-PLAN.md** (this file) | Baseline audit, gap analysis, philosophy, tiers, roadmap |
| 01 | [01-content-standards.md](01-content-standards.md) | The canonical templates every new file must follow |
| 02 | [02-phase-1-core-python.md](02-phase-1-core-python.md) | 11 new topics + retrofit of 41 existing |
| 03 | [03-phase-2-advanced-python.md](03-phase-2-advanced-python.md) | 14 new topics (concurrency, memory, protocols) |
| 04 | [04-phase-3-libraries.md](04-phase-3-libraries.md) | NumPy/Pandas/Matplotlib/SciPy + pandas dedup |
| 05 | [05-phase-4-databases.md](05-phase-4-databases.md) | Real SQL, SQLAlchemy, Postgres, Redis, vector DBs |
| 06 | [06-phase-5-backend.md](06-phase-5-backend.md) | Production FastAPI, auth, observability, deployment |
| 07 | [07-phase-6-dsa.md](07-phase-6-dsa.md) | DSA + interview patterns for AI engineers |
| 08 | [08-phase-7-9-ml-mlops-genai.md](08-phase-7-9-ml-mlops-genai.md) | ML depth, MLOps (new), GenAI/LLM (new) |
| 09 | [09-assessment-system.md](09-assessment-system.md) | Quizzes, code challenges, interviews, capstones |
| 10 | [10-remediation-backlog.md](10-remediation-backlog.md) | 34 measured failures with root causes and fixes |
| 11 | [11-execution-roadmap.md](11-execution-roadmap.md) | Sequenced 40-week build order, dependencies, DoD |

---

## 1. Measured Baseline

Every figure below came from running commands against the tree on 2026-07-29.

### 1.1 Inventory

| Asset | Count |
|---|---|
| Numbered exercise files (`NN-topic.py`) | **277** |
| Lecture files (`*-lecture.md`) | **256** |
| Glossary files (`*-glossary.md`) | **256** |
| Quizzes (`supplementary/quizzes/`) | **29** |
| Interview guides (`supplementary/interviews/`) | **15** |
| Capstone projects (`projects/`) | **5** (README only) |
| Unit test files (`tests/unit/`) | **7** |
| **Total files in module** | **1128** |

### 1.2 Per-section breakdown

| Section | Exercises | Lectures | Glossaries | Smoke-test result |
|---|---|---|---|---|
| `01-core-python` | 41 | 41 | 41 | **40/40 pass** (33 needs stdin) |
| `02-advanced-python` | 20 | 20 | 20 | 17/20 pass — **3 fail** |
| `03-libraries/numpy` | 28 | 28 | 28 | 24/28 pass — **4 fail** |
| `03-libraries/pandas` | **45** | 24 | 24 | 31/45 pass — **14 fail** |
| `03-libraries/matplotlib` | 20 | 20 | 20 | 20/20 pass |
| `03-libraries/scipy` | 12 | 12 | 12 | 12/12 pass |
| `04-databases/mysql` | 12 | 12 | 12 | 11/12 pass — **1 fail** |
| `04-databases/mongodb` | 11 | 11 | 11 | 9/11 pass — **2 fail** |
| `05-web-frameworks/fastapi` | 25 | 25 | 25 | not executed (needs server) |
| `05-web-frameworks/django` | 20 | 20 | 20 | **django not installed** |
| `06-data-structures-algorithms` | 20 | 20 | 20 | 16/20 pass — **4 fail** |
| `07-machine-learning` | 23 | 23 | 23 | 23/23 pass |

**34 files fail or cannot run.** Full root-cause table in [10-remediation-backlog.md](10-remediation-backlog.md).

### 1.3 Structural defect: pandas has two merged series

`03-libraries/pandas` holds **45** exercise files but only **24** lectures, because
two independently-authored series were dropped into one folder. Every prefix
`02`–`13` is duplicated:

```
02-getting-started.py   +  02-inspecting-data.py
03-series.py            +  03-indexing-selection.py
04-dataframes.py        +  04-filtering.py
...                        (through 13-)
```

The W3Schools-style series (`*-series`, `*-dataframes`, `*-data-loc`) has lectures;
the EXPANSION_PLAN series (`*-inspecting-data`, `*-filtering`, `*-window-functions`)
has **21 files with no lecture and no glossary**. This must be resolved before
either series is extended.

---

## 2. Gap Analysis

### 2.1 The root cause

**All 41 core files and most of the library files derive from W3Schools**
(verified: every `01-core-python` file carries a `w3schools.com` reference URL).
That origin sets a hard ceiling. W3Schools teaches *syntax*. Senior engineering is
*judgment*: which construct, at what asymptotic cost, failing how, observable by what.

### 2.2 Five measured gaps

#### Gap A — Nothing is self-verifying

| Section | Files containing `assert` | Total `.py` |
|---|---|---|
| `01-core-python` | **0** | 44 |
| `02-advanced-python` | **0** | 21 |
| `03-libraries` | 2 | 111 |
| `04-databases` | **0** | 27 |
| `05-web-frameworks` | 2 | 73 |
| `06-data-structures-algorithms` | **0** | 21 |
| `07-machine-learning` | **0** | 24 |

Every file is a `print()` walkthrough. A learner who edits a file cannot tell
whether they broke it. There is no feedback loop — the single biggest pedagogical
weakness in the module.

Worse, this hides real bugs: `06-data-structures-algorithms/09-binary-search-trees.py`
reaches a `BSTNode` object with `.val` when the class defines `.data`, and the file
still "looked fine" because nothing asserted anything until Python raised
`AttributeError` at the very end.

#### Gap B — No cost model

| Section | Lectures mentioning Big-O / complexity |
|---|---|
| `01-core-python` | 2 of 41 |
| `02-advanced-python` | **0 of 20** |
| `06-data-structures-algorithms` | 29 (good) |

`13-lists.py` teaches `list.insert(0, x)` with no note that it is O(n) while
`deque.appendleft` is O(1). `02-advanced-python` — the section that covers
`__slots__`, `functools`, and `itertools` — never once discusses cost. This is
precisely the judgment that distinguishes engineering levels.

#### Gap C — Missing stdlib that backend/AI work uses daily

Absent from all 41 `01-core-python` exercises (measured, `0` occurrences):

| Missing | Needed for |
|---|---|
`logging`, `pytest`, `assert` | Nothing ships without these |
`argparse`, `sys.argv`, `os.environ` | Every CLI, every 12-factor service |
`dataclasses`, `functools`, `contextlib` | Modern Python baseline |
`heapq`, `bisect`, `deque` | Top-k retrieval, ranked results, sliding windows |
`pickle`, `sqlite3`, `shutil`, `subprocess` | Persistence, model artifacts, orchestration |
`__slots__`, `__hash__`, `__lt__`, `total_ordering` | Memory limits, sortable domain objects |
`zoneinfo` / `timezone` | Real correctness bugs |
walrus `:=`, `f"{x=}"`, `TypeAlias`, `TypedDict` | Idiomatic ≥3.10 (module targets 3.10+) |
`ExceptionGroup`, `raise ... from` | Structured error handling |
`gc`, refcounting, interning, GIL | Reasoning about memory and concurrency |

`pathlib` appears in only **1** exercise while `38-file-handling.py` teaches
string paths — the deprecated habit is taught first.

#### Gap D — No AI-engineering or production bridge

Repo-wide `.py` occurrences:

| Topic | Files |
|---|---|
`torch` | **0** |
`openai` / `anthropic` | **0** / **0** |
`mlflow`, `drift`, `feature store`, `onnx`, `quantiz` | **0** each |
`opentelemetry`, `prometheus`, `structlog` | **0** each |
`Dockerfile`, `celery`, `alembic`, `qdrant` | **0** each |
`redis` | 1 |
`embedding` | 1 |

Meanwhile `torch` **is installed** in the environment and unused. The words
"AI Engineer" appear in **0 of 41** core lectures. There are two entire phases
(MLOps, GenAI) planned in `EXPANSION_PLAN.md` that do not exist.

#### Gap E — Template drift breaks navigability

`01-core-python/lectures/README.md` promises a "consistent format." Measured:

| Section heading | Present in |
|---|---|
`Learning Objectives` | **41/41** ✅ |
`Best Practices` | **41/41** ✅ |
`Practice Exercises` | **41/41** ✅ |
`Summary` | **41/41** ✅ |
`Common Mistakes` | 39/41 |
`Topic Overview` | **28/41** — files 29–41 use `## Topic NN:` instead |
`Quick Reference` | **14/41** |
`Next Steps` | **13/41** |

Glossaries use **three** different schemes: files 01–14 `## Detailed Definitions`,
15–33 `## Definitions`, 34–41 `## Glossary Terms` with A/B/C letter grouping.
The content exists — the headings diverge, so the promise is false past file 14.

Also: **0 of 41** core lectures link forward to Phase 2, even where the topic
demands it (`21-functions` teaches closures and decorators with no pointer to
`02-advanced-python/01-decorators.py`).

---

## 3. Design Philosophy

Five principles govern every new file in this plan.

### P1 — Every file is executable and self-verifying
Teaching flow stays `print()`-driven, but each file **ends** with a
`_verify()` block of `assert`s that pass silently and fail loudly. A learner who
breaks something learns immediately. Enables CI over the whole module.

### P2 — Every construct carries its cost
Any lecture introducing a data structure or algorithm states time **and** space
complexity, and names the cheaper alternative. `list.insert(0,x)` is never taught
without `deque.appendleft`.

### P3 — Every topic answers "why does a senior care?"
Each lecture gains an **AI Engineering Relevance** section making the bridge
concrete: `bisect` → top-k reranking; `__slots__` → a million embeddings in RAM;
`asyncio` → 200 concurrent LLM calls; `Decimal` → billing, never loss curves.

### P4 — Progression is Read → Run → Break → Build → Prove
Five artifacts per topic: lecture (read), exercise (run), quiz (recall),
code challenge (build under hidden tests), interview drill (articulate).

### P5 — Reuse the existing voice
The current format is good: `# Example N:` headers, `# ============` rules,
inline expected output, `--- Summary ---` footer. New files match it exactly.
This is an **extension**, not a rewrite.

---

## 4. Target State

| Metric | Now | Target | Δ |
|---|---|---|---|
| Sections (phases) | 7 | **9** | +2 (MLOps, GenAI) |
| Exercise files | 277 | **~470** | +193 |
| Lectures | 256 | **~450** | +194 |
| Glossaries | 256 | **~450** | +194 |
| Quizzes | 29 | **~120** | +91 |
| Code challenges | 0 | **~200** | +200 |
| Interview guides | 15 | **~45** | +30 |
| Capstone projects | 5 stubs | **12 built** | +7 |
| Files with `assert` self-check | 4 | **~470** | +466 |
| Lectures with complexity notes | ~31 | **~450** | — |
| Failing files | **34** | **0** | −34 |

Roughly **+900 new files**. No working content is rewritten.

---

## 5. Tiered Priorities

Work is ordered by *leverage per hour*, not by section number.

### Tier 0 — Stop the bleeding (Week 1–2)
Fix the 34 broken files; resolve the pandas double-series; make `run_smoke_tests.py`
gate the module in CI. **Nothing new is written until the baseline is green** —
building on a broken foundation multiplies the debt.
→ [10-remediation-backlog.md](10-remediation-backlog.md)

### Tier 1 — The rigor layer (Week 3–10)
Highest leverage in the plan. Applies to content that already exists.
1. `assert`-based `_verify()` block appended to all 277 exercises
2. `practice_testable.py` — refactor the 99 practice problems off `input()`
   (measured: **146** `input()` calls make them un-gradeable)
3. Complexity notes + **AI Engineering Relevance** into all lectures
4. Heading normalization across the drifted 27 lectures / 27 glossaries

### Tier 2 — Fill the stdlib and depth gaps (Week 11–22)
New topics in Phases 1–3 and 6: the `logging`/`pytest`/`argparse`/`pathlib`/
`dataclasses`/`heapq` set; concurrency and memory depth; NumPy/Pandas performance.

### Tier 3 — The two missing phases (Week 23–34)
`08-mlops/` and `09-genai/` — the phases that make the title "AI Engineer" true.
Also production backend: auth, observability, Docker, Postgres, Redis, vector DBs.

### Tier 4 — Assessment and capstones (Week 35–40)
~200 code challenges, quiz coverage to every topic, 30 interview guides,
7 portfolio-grade capstones.

---

## 6. Roadmap at a Glance

| Weeks | Tier | Deliverable |
|---|---|---|
| 1–2 | 0 | 34 fixes; pandas dedup; green CI |
| 3–6 | 1 | `_verify()` in 277 files; testable practice set |
| 7–10 | 1 | Complexity + AI-relevance retrofit; heading normalization |
| 11–14 | 2 | Phase 1: 11 new topics (42–52) |
| 15–18 | 2 | Phase 2: 14 new topics (21–34) |
| 19–22 | 2 | Phase 3: pandas restructure, NumPy perf, Polars/PyArrow |
| 23–26 | 3 | Phase 4+5: Postgres, SQLAlchemy, Redis, vector DBs, prod FastAPI |
| 27–30 | 3 | Phase 8 `08-mlops/` (16 topics) |
| 31–34 | 3 | Phase 9 `09-genai/` (20 topics) |
| 35–37 | 4 | 200 code challenges + 91 quizzes |
| 38–40 | 4 | 30 interview guides + 7 capstones |

Detailed sequencing, parallelization, and definition-of-done per week:
[11-execution-roadmap.md](11-execution-roadmap.md)

---

## 7. How to Use This Plan

**If you are executing it yourself:** work Tier 0 → 1 → 2 → 3 → 4. Do not skip
Tier 1 to get to the exciting GenAI content — Tier 1 is what converts the
existing 277 files from demos into a verified curriculum, and it is cheap.

**If you are directing an agent:** each phase document contains per-file topic
tables with the concepts, the `assert` targets, and the AI-relevance hook. A file
can be generated from one table row plus
[01-content-standards.md](01-content-standards.md).

**Definition of done for any new topic** — five artifacts, all present:
```
NN-topic.py                      exercise, runs clean, ends with _verify()
lectures/NN-topic-lecture.md     canonical 12-section template
lectures/NN-topic-glossary.md    canonical 4-section template
challenges/NN-topic/             bronze/silver/gold + hidden tests
quizzes/<topic>-quiz.md          20 Q, difficulty-tagged, explained key
```

---

## 8. Known Corrections Needed in Existing Docs

Found during the audit; fold into Tier 0.

| File | Claim | Reality |
|---|---|---|
`python/README.md` | "405+ files"; `01-core-python` = 43 | 1128 files; 41 numbered + 2 practice |
`python/README.md` | `pandas/ (24 files)` | 45 files (double series) |
`EXPANSION_PLAN.md` | pandas `0 files ❌ MISSING` | 45 files exist |
`EXPANSION_PLAN.md` | matplotlib `0 files ❌ MISSING` | 20 files exist |
`EXPANSION_PLAN.md` | "Plan created: July 2024" | inconsistent with July 2026 content |
`01-core-python/README.md` | "43 exercise files" | 41 numbered + 2 practice |
`01-core-python/lectures/README.md` | "consistent format" | drifts after file 14 (Gap E) |
`learning_path.md` | lectures at `supplementary/lectures/01-core-python/` | actually `01-core-python/lectures/` |

---

*Plan generated 2026-07-29 against commit `c4a4eec`. All baseline numbers measured, not estimated.*
