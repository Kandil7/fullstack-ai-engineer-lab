# Execution Roadmap

> Sequenced build order for the whole plan, with dependencies, parallelization,
> and definition of done per block.
>
> **40 weeks** at a sustained pace. The ordering is by *leverage*, not by section
> number — and the first two weeks are repair, not authoring.

---

## 1. Principles

| # | Principle | Why |
|---|---|---|
| 1 | **Green before growth** | Tier 0 first. 34 broken files means new content lands on sand and regressions hide. |
| 2 | **Retrofit before extend** | `_verify()` across 277 existing files buys more than 50 new files. Cheap, high leverage. |
| 3 | **Follow the critical path to the goal** | NumPy → transformers → GenAI foundations → vector stores → RAG is the chain that makes this AI-engineer training. |
| 4 | **Never author a challenge before its exercise** | The challenge must test what was actually taught. |
| 5 | **One topic = five artifacts** | Exercise, lecture, glossary, challenge, quiz coverage. Partial topics accumulate as debt. |
| 6 | **CI gates every block** | A block is not done until `run_smoke_tests.py --all --verify` is green on Linux + Windows. |

---

## 2. Timeline

### Block 0 — Repair (Weeks 1–2)

| Week | Work | Doc |
|---|---|---|
| 1 | R1.1 hang (`04-queues`), R1.2 syntax (`20-performance`), R1.3–R1.7 logic bugs | [10](10-remediation-backlog.md) |
| 1 | R3 encoding (4 files), R4 deps (`openpyxl`, `seaborn`) | R3, R4 |
| 2 | R2 API drift (11 pandas/numpy files) | R2 |
| 2 | R5 SQL dialect, R6 Mongo simulator, R7 **Django decision** | R5–R7 |
| 2 | R8 pandas renumbering (38 renames) | R8 |
| 2 | R9 doc corrections, R10 CI gate + Windows matrix | R9, R10 |

**DoD:** `run_smoke_tests.py --all` exits 0 on Ubuntu + Windows, Python 3.10 + 3.12.
Zero failing files. Every documented count matches reality.

> **Do not skip R10.** Without the gate, every subsequent block re-accumulates the
> same 34-file debt. All four encoding bugs are Windows-only — the matrix is what
> catches them.

---

### Block 1 — Rigor Retrofit (Weeks 3–10)

The highest-leverage block in the plan. Touches only existing content.

| Week | Work | Files |
|---|---|---|
| 3–4 | `_verify()` in Phase 1 (41) + Phase 2 (20) | 61 |
| 5 | `_verify()` in Phase 3 (~105) | 105 |
| 6 | `_verify()` in Phases 4, 6, 7 (23 + 20 + 23) | 66 |
| 6 | `TestClient` `_verify()` in FastAPI (25) | 25 |
| 7 | `practice_testable.py` + stubs + tests (99 problems off `input()`) | 3 |
| 8 | Heading normalization (~27 lectures, ~27 glossaries); expand 5 thin glossaries | 59 |
| 9–10 | `## Complexity and Cost` + `## AI Engineering Relevance` across all lectures | ~256 |

**Parallelizable:** weeks 3–6 split cleanly by section; weeks 8 and 9–10 touch
markdown only and can run alongside.

**DoD:** all 277 exercises self-verify; 99 practice problems gradeable via pytest;
every lecture carries a cost model and an AI-relevance section; one heading scheme.

---

### Block 2 — Foundation Gaps (Weeks 11–22)

| Week | Work | Doc |
|---|---|---|
| 11–14 | **Phase 1 topics 42–52** (pathlib, dataclasses, logging, pytest, CLI, exceptions, comprehensions, collections, datetime, serialization, memory) | [02](02-phase-1-core-python.md) |
| 15–16 | **Phase 2 topics 21–22, 31** (concurrency comparison, asyncio advanced, concurrency patterns) | [03](03-phase-2-advanced-python.md) |
| 17–18 | Phase 2 topics 23–30 (typing, memory/GC, profiling, patterns, packaging, tooling, functional, protocols) | [03](03-phase-2-advanced-python.md) |
| 19 | Phase 2 topics 32–34 (metaprogramming, security, debugging) | [03](03-phase-2-advanced-python.md) |
| 19–20 | **NumPy 29–34** (broadcasting, vectorization, strides, dtypes, linalg, advanced indexing) | [04](04-phase-3-libraries.md) |
| 20–21 | 17 orphaned pandas lecture+glossary pairs; pandas 39–44 | [04](04-phase-3-libraries.md) |
| 21 | SciPy 13–16 (stats tests, optimization, **sparse**, **distance**) | [04](04-phase-3-libraries.md) |
| 22 | Matplotlib 21–24; DSA 21–26 (heaps, tries, union-find, LRU, Bloom, segment trees) | [04](04-phase-3-libraries.md), [07](07-phase-6-dsa.md) |

**Sequencing notes**
- `21-concurrency-comparison` before the other Phase 2 concurrency topics — it
  reframes the existing `04`/`16`/`17`.
- NumPy `29`–`34` is on the critical path: it gates Phase 7 deep learning.
- SciPy `15`/`16` (sparse, distance) are RAG prerequisites.

**DoD:** Phase 1 at 52 topics; Phase 2 at 34; every pandas file has a lecture;
NumPy covers the performance surface.

---

### Block 3 — Data and Backend Production (Weeks 23–26)

| Week | Work | Doc |
|---|---|---|
| 23 | `sql-fundamentals/` 14 topics (sqlite3, no Docker needed) | [05](05-phase-4-databases.md) |
| 23 | Docker wiring + skip-if-absent helper | [05](05-phase-4-databases.md) |
| 24 | `postgres/` 01–07, 10–12; `redis/` 8 topics | [05](05-phase-4-databases.md) |
| 24 | `sqlalchemy/` 10 topics (**06-eager-loading / N+1**) | [05](05-phase-4-databases.md) |
| 25 | `postgres/08–09` (pgvector, hybrid); `vector-stores/` 8 topics; Mongo port | [05](05-phase-4-databases.md) |
| 25–26 | FastAPI 26–37 (API design, performance, **32-async-deep**, **36-streaming**) | [06](06-phase-5-backend.md) |
| 26 | FastAPI 38–52 (security, observability, deployment, **52-serving-ml-models**) | [06](06-phase-5-backend.md) |
| 26 | `system-design/` 10 topics | [06](06-phase-5-backend.md) |

**DoD:** real Postgres/Redis/Mongo/Qdrant exercised via Docker with clean skips;
N+1 demonstrated by query count; pgvector + hybrid search working; FastAPI at 52
topics with observability and deployment.

---

### Block 4 — ML Depth and MLOps (Weeks 27–30)

| Week | Work | Doc |
|---|---|---|
| 27 | **Phase 7: 24-pipelines, 25-data-leakage**, 26–29 (validation, metrics, calibration, imbalance) | [08](08-phase-7-9-ml-mlops-genai.md) |
| 28 | Phase 7: 30–35 (GBDT, features, selection, tuning, ensembling, explainability) | [08](08-phase-7-9-ml-mlops-genai.md) |
| 29 | Phase 7: 36–40 (PyTorch → **40-transformers-from-scratch**) | [08](08-phase-7-9-ml-mlops-genai.md) |
| 30 | `08-mlops/` 01–16 | [08](08-phase-7-9-ml-mlops-genai.md) |

`24`/`25` first: pipelines and leakage are what make everything after them
trustworthy. `40-transformers` closes Phase 7 and opens Phase 9.

**DoD:** Phase 7 at 40 topics; leakage taught with a worked before/after; PyTorch
used (from 0 files); attention implemented from scratch; MLOps train→serve→monitor
loop complete.

---

### Block 5 — GenAI (Weeks 31–34)

| Week | Work | Doc |
|---|---|---|
| 31 | `09-genai/` 01–05 (LLM fundamentals, clients, structured output, prompting, prompt eval) | [08](08-phase-7-9-ml-mlops-genai.md) |
| 32 | 06–12 (embeddings, **chunking**, doc processing, baseline RAG, **retrieval quality**, advanced retrieval, reranking) | [08](08-phase-7-9-ml-mlops-genai.md) |
| 33 | 13–16 (tool calling, agent patterns, multi-agent, memory) | [08](08-phase-7-9-ml-mlops-genai.md) |
| 34 | 17–22 (observability, caching/cost, guardrails, eval, fine-tuning, local models); 23–25 case studies | [08](08-phase-7-9-ml-mlops-genai.md) |

Order within week 32 matters: build the baseline (`09`) and learn to *measure* it
(`10`) before adding techniques (`11`, `12`). Optimizing before measuring is the
most common RAG mistake.

**DoD:** 25 topics; complete RAG service with citations; retrieval quality measured;
structured output validated; injection defenses covered; all pure logic tested offline.

---

### Block 6 — Assessment and Capstones (Weeks 35–40)

| Week | Work | Doc |
|---|---|---|
| 35 | Challenge scaffolding + CI both-directions check; challenges for Phases 1–2 | [09](09-assessment-system.md) |
| 36 | Challenges for Phases 3–6 | [09](09-assessment-system.md) |
| 37 | Challenges for Phases 7–9; quizzes (**Advanced Python first — 0 of 20 today**) | [09](09-assessment-system.md) |
| 38 | Remaining quizzes + 9 checkpoint quizzes; progress-tracking docs | [09](09-assessment-system.md) |
| 39 | 30 interview guides | [09](09-assessment-system.md) |
| 40 | Build capstones 01–05; scaffold 06–12 | [09](09-assessment-system.md) |

Capstones 06–12 are full projects and realistically extend past week 40 — treat
them as ongoing portfolio work rather than a sprint.

**DoD:** every topic has a quiz and a 3-tier challenge; tests verified to fail on
`starter.py` and pass on `solution.py`; 45 interview guides; capstones 01–05 running.

---

## 3. Critical Path

The dependency chain that must not slip, because it is what produces the target skill:

```text
Block 0 (green CI)
   └─> Block 1 (_verify retrofit)
          └─> NumPy 29-34  [Week 19-20]
                 └─> Phase 7: 36-40 PyTorch + transformers  [Week 29]
                        └─> GenAI 01-05 foundations  [Week 31]
                               └─> GenAI 06-12 RAG  [Week 32]
                                      ^
   Phase 4 vector-stores  [Week 25] ──┘
   Phase 5 observability  [Week 26] ──> GenAI 17-22 production  [Week 34]
```

Everything else — Matplotlib, Polars, Django, DSA patterns, system design — is
valuable but off the critical path and can absorb slippage.

---

## 4. Parallelization

Independent tracks that different agents or sessions can run concurrently:

| Track | Blocks | Touches | Conflicts with |
|---|---|---|---|
| **A. Code retrofit** | 1 | `.py` files | none (append-only `_verify()`) |
| **B. Markdown retrofit** | 1 | lectures/glossaries | none |
| **C. New Python topics** | 2–5 | new files | none |
| **D. Databases** | 3 | `04-databases/` | none |
| **E. Assessment** | 6 | `challenges/`, quizzes | must trail C by ≥1 topic |

**Serial-only work:** R8 pandas renumbering (git mv across 38 files) and R10 CI
setup. Both must complete before parallel tracks start touching those areas.

---

## 5. Effort Distribution

| Block | Weeks | New files | Retrofit files | Character |
|---|---|---|---|---|
| 0 — Repair | 2 | ~5 | ~60 | Debugging |
| 1 — Rigor | 8 | ~20 | ~530 | Mechanical, high leverage |
| 2 — Foundations | 12 | ~200 | — | Authoring |
| 3 — Data/Backend | 4 | ~230 | ~25 | Authoring + infra |
| 4 — ML/MLOps | 4 | ~130 | ~23 | Authoring |
| 5 — GenAI | 4 | ~100 | — | Authoring |
| 6 — Assessment | 6 | ~250 | — | Authoring + tooling |

Block 1 is only 8 weeks for ~530 file touches because the work is mechanical and
scriptable — and it is where the module's credibility is won.

---

## 6. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| **Scope fatigue** — 900 files is a lot | High | Blocks 0–1 alone deliver a verified, correct 277-file curriculum. That is a legitimate stopping point. |
| **Library drift again** | High | R10 CI + pinned minimums + scheduled dependency job. This already happened once (11 files). |
| **LLM API cost during Block 5** | Medium | All pure logic tested offline; live calls opt-in via env var. |
| **Docker friction in Block 3** | Medium | Skip-if-absent pattern; `sql-fundamentals/` needs no Docker at all. |
| **Capstones under-built** | Medium | Rubric with an explicit ≥80 bar; scaffold early, build continuously. |
| **Quality drift across ~900 files** | Medium | [01-content-standards.md](01-content-standards.md) is enforceable; add a `_dev/validate_structure.py` check for the 12 required lecture headings. |
| **Windows-only breakage recurring** | Medium | Windows in the CI matrix permanently, not as an afterthought. |

---

## 7. Milestones

| Milestone | Week | Meaning |
|---|---|---|
| **M1 — Green baseline** | 2 | Zero failures; CI gates the module |
| **M2 — Verified curriculum** | 10 | All 277 exercises self-verify; every lecture has cost + AI framing |
| **M3 — Complete Python foundation** | 22 | Phases 1–3 and 6 cover the professional stdlib and performance surface |
| **M4 — Production backend** | 26 | Real databases, deployable observable services |
| **M5 — ML engineer** | 30 | Leak-free ML, PyTorch, transformers, MLOps loop |
| **M6 — AI engineer** | 34 | RAG with measured quality, agents, LLM production concerns |
| **M7 — Assessed and portfolio-ready** | 40 | Challenges, quizzes, interview prep, built capstones |

**M1 and M2 are the ones that matter most.** They convert an existing 1128-file
tutorial into a trustworthy, verified curriculum — before a single new topic is
written. If effort has to stop somewhere, stop after M2, not mid-Block 2.

---

## 8. Getting Started

The first three actions, in order:

1. **Fix `06-data-structures-algorithms/04-queues.py`** — it hangs forever
   (exit 124) and blocks any CI run over that directory. [R1.1](10-remediation-backlog.md)
2. **Fix `03-libraries/pandas/20-performance.py`** — `SyntaxError`; the file has
   never executed. [R1.2](10-remediation-backlog.md)
3. **Extend `run_smoke_tests.py`** with `--all --verify`, a 30s per-file timeout,
   and a documented skip list; wire it into CI with a Windows job. [R10](10-remediation-backlog.md)

With those three done, the module is measurable — and everything after becomes
verifiable rather than hopeful.

---

*Roadmap for [00-MASTER-PLAN.md](00-MASTER-PLAN.md). Per-phase detail in documents 02–09; fixes in [10-remediation-backlog.md](10-remediation-backlog.md).*
