# Assessment System — Quizzes, Challenges, Interviews, Capstones

> **Current:** 29 quizzes, 15 interview guides, **0 code challenges**, 5 capstone
> projects that are README-only.
> **Target:** ~120 quizzes, ~200 code challenges, ~45 interview guides, 12 built
> capstones.
>
> The module can currently teach and (after Tier 1) verify. It cannot **assess**.
> Reading a lecture and running a script proves nothing about capability.

---

## 1. The Four-Layer Model

Each layer tests something the others cannot.

| Layer | Tests | Feedback | Time |
|---|---|---|---|
| **Quiz** | Recall and conceptual precision | Immediate, answer key | 20 min |
| **Code challenge** | Can you build it under constraints | Automated, hidden tests | 15–75 min |
| **Interview drill** | Can you *explain* it | Self-assessed against a model answer | 30 min |
| **Capstone** | Can you integrate it into a system | Rubric + working software | 1–2 weeks |

The missing middle layer — code challenges — is the largest gap. There is nothing
between "read the lecture" and "build a project," which is where most learners stall.

---

## 2. Quizzes: 29 → ~120

### 2.1 Current coverage is thin and uneven

| Area | Quizzes | Topics | Coverage |
|---|---|---|---|
| Core Python | 8 | 41 | **20%** |
| Advanced Python | 0 | 20 | **0%** |
| NumPy | 2 | 28 | 7% |
| pandas | 2 | 38 | 5% |
| Matplotlib | 1 | 20 | 5% |
| SciPy | 1 | 12 | 8% |
| Databases | 0 | 64 | **0%** |
| FastAPI | 2 | 52 | 4% |
| Django | 1 | 20 | 5% |
| DSA | 7 | 40 | 18% |
| ML | 5 | 40 | 13% |
| MLOps | 0 | 16 | **0%** |
| GenAI | 0 | 25 | **0%** |

**Advanced Python has 20 topics and zero quizzes** — the section with the best
lectures has no assessment at all.

### 2.2 Keep the existing format

The current quizzes are genuinely good: 20 questions, difficulty tags, and an
answer key that *explains* rather than just states. Preserve that exactly; only
add coverage. Requirements per quiz:

- 20 questions; roughly 6 Easy / 9 Medium / 5 Hard
- **≥8 must be "what does this code output?"** with a real snippet — these test
  understanding, not memorization
- Answer key explains why the key is right **and why each distractor is wrong**
- Distractors encode actual misconceptions (e.g. that `list.insert(0,x)` is O(1),
  that `is` compares values, that `inplace=True` is faster)

### 2.3 Target distribution

| Area | Target |
|---|---|
| Core Python (per-topic) | 44 |
| Advanced Python | 17 |
| NumPy / pandas / Matplotlib / SciPy / Polars | 20 |
| Databases (SQL, Postgres, SQLAlchemy, Redis, Mongo, vector) | 12 |
| Backend (FastAPI, system design) | 12 |
| DSA | 13 |
| ML | 12 |
| MLOps | 6 |
| GenAI | 8 |
| **Total** | **~144** |

Also add **cumulative checkpoint quizzes** (40 questions, mixed topics) at the end
of each phase — spaced retrieval across a whole phase, which per-topic quizzes miss.

---

## 3. Code Challenges: 0 → ~200

The critical new artifact. One `challenges/NN-topic/` directory per topic, three
tiers each, graded by hidden tests.

### 3.1 Why three tiers

| Tier | Purpose | Constraint design |
|---|---|---|
| 🥉 **Bronze** | Confirm you understood the lecture | Small n; any correct approach passes |
| 🥈 **Silver** | Force the right data structure | n ≤ 10⁶ — **O(n²) times out** |
| 🥇 **Gold** | Force real engineering | Streaming 10⁷, memory ≤ 50MB — single pass required |

The constraint is the teacher. A learner who passes Bronze with nested loops
*cannot* pass Silver that way, and discovers why the complexity table mattered.

### 3.2 Directory contract

```python
challenges/49-collections-toolkit/
├── README.md            # three briefs with I/O tables and constraints
├── starter.py           # signatures only; bodies raise NotImplementedError
├── solution.py          # reference impl + why-this-approach commentary
└── test_challenge.py    # hidden tests: correctness, edges, performance
```

**Invariants**
- Tests **fail** against `starter.py` and **pass** against `solution.py` — verify
  both directions in CI, or the tests are not actually testing anything
- Edge cases always: empty, single element, all duplicates, negatives, boundary values
- Silver/Gold include a performance or memory guard
- No solution text in `README.md` or `starter.py`

### 3.3 Performance guards that are CI-stable

Never assert wall-clock. Assert **operation counts** or **memory**, which are
deterministic:

```python
def test_silver_is_subquadratic():
    """A nested-loop solution must fail this."""
    n = 200_000
    data = list(range(n))
    counter = CallCounter()
    result = starter.solve(data, _probe=counter)
    assert result == expected
    # O(n) allows ~n operations; O(n^2) would need 4e10
    assert counter.count < 10 * n, (
        f"used {counter.count} ops for n={n} — needs a hash map or heap, not nested loops"
    )

def test_gold_memory_bounded():
    import tracemalloc
    tracemalloc.start()
    starter.solve_streaming(generate(10_000_000))
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert peak < 50 * 1024 * 1024, f"peak {peak/1e6:.1f}MB exceeds 50MB — must stream"
```

`tracemalloc` and operation counters are reproducible across machines; timing is not.

### 3.4 High-value challenge examples

| Topic | Gold challenge |
|---|---|
| `49-collections-toolkit` | Top-k from a 10⁷ stream in bounded memory (**heap, not sort**) |
| `52-memory-performance` | Process a 5GB file with a 50MB ceiling |
| `21-heaps` | Streaming median with two heaps |
| `24-lru-cache` | O(1) LRU from scratch — no `OrderedDict` |
| `25-bloom-filters` | Dedup 10⁸ IDs within a memory budget |
| `31-dynamic-programming` | Edit distance with O(min(m,n)) space |
| `sql/10-indexes` | Rewrite a query to use an index; assert the `EXPLAIN` plan changes |
| `sqlalchemy/06-eager-loading` | Eliminate N+1; assert query count drops from 101 to 2 |
| `fastapi/30-idempotency` | Idempotent endpoint surviving duplicate concurrent requests |
| `genai/07-chunking` | Chunker that never splits mid-sentence and preserves overlap |
| `genai/10-retrieval-quality` | Raise recall@5 above a threshold on a fixed corpus |
| `ml/25-data-leakage` | Find and fix the leak in a provided pipeline; score must *drop* |

That last one is the most valuable pattern in the entire assessment system: a
challenge where **success means the metric gets worse**, because the original
number was a lie.

---

## 4. Interview Guides: 15 → ~45

### 4.1 Current

15 guides covering DSA (7), Python basics/OOP/functions/data-structures/errors (5),
libraries (1), FastAPI (1), ML (1). Format is good — Q, model answer, code. Keep it.

### 4.2 Additions

| Area | New guides |
|---|---|
| Advanced Python | decorators/generators, concurrency (**threads vs processes vs async**), typing, memory/GC, metaprogramming |
| Databases | SQL query writing, schema design, indexing/optimization, transactions/isolation, Redis/caching, vector search |
| Backend | API design, auth/security, observability, scaling/reliability, FastAPI internals |
| System design | LLM API design, RAG system design, inference platform, multi-tenancy |
| ML | feature engineering, validation/leakage, metrics selection, deep learning, explainability |
| MLOps | deployment, monitoring/drift, experiment tracking, cost |
| GenAI | prompt engineering, RAG architecture, agents, fine-tuning vs prompting, LLM eval, safety/injection |
| Behavioral | project walkthrough, debugging war stories, tradeoff articulation |

### 4.3 Add what the current guides lack

Each new guide includes:
- **Follow-up ladder** — interviewers escalate; model 3 levels of depth per question
- **Red flags** — answers that sound right but reveal a gap
- **"I don't know" scripts** — how to reason aloud from first principles instead of bluffing
- **Whiteboard-ready diagrams** for design questions

---

## 5. Capstone Projects: 5 stubs → 12 built

All five existing projects contain only a `README.md`. Nothing is implemented.

### 5.1 Existing five — build them

| # | Project | Phases | Deliverable |
|---|---|---|---|
| 01 | Calculator | 1 | CLI + parser, full test suite, error handling |
| 02 | File Manager | 1, 2 | `pathlib`-based, atomic ops, progress, logging |
| 03 | API Server | 5 | FastAPI CRUD, auth, DB, tests, Docker |
| 04 | Data Analyzer | 3 | pandas EDA, charts, report generation |
| 05 | ML Pipeline | 7 | Leak-free pipeline, tracked experiments, model artifact |

### 5.2 Seven new, AI-engineer targeted

| # | Project | Phases | Core challenge |
|---|---|---|---|
| 06 | **RAG Knowledge Base** ⭐ | 1–5, 9 | Hybrid retrieval, citations, **measured recall@k**, eval suite, cost tracking |
| 07 | ML Training Platform | 3, 7, 8 | Validation → train → register → serve → monitor, with drift detection |
| 08 | LLM Gateway Service ⭐ | 2, 5, 9 | Multi-provider routing, semantic caching, rate limits, token accounting, tracing |
| 09 | Document Intelligence | 3, 5, 9 | PDF/table extraction, structured output with validation, high volume |
| 10 | Agent Platform | 2, 5, 9 | Tool registry, budget caps, state persistence, human-in-loop |
| 11 | Vector Search Service | 4, 9 | Ingestion pipeline, incremental indexing, filtered search, reindex without downtime |
| 12 | Observability Dashboard | 3, 4, 5, 8 | Metrics collection, drift charts, alerting, retraining triggers |

### 5.3 Every capstone must ship

```text
projects/NN-name/
├── README.md              # architecture, decisions, setup, screenshots
├── src/                   # implementation
├── tests/                 # unit + integration, meaningful coverage
├── docker-compose.yml     # one-command local run
├── Dockerfile
├── .github/workflows/     # CI: lint, type-check, test
├── docs/
│   ├── architecture.md    # diagram + component responsibilities
│   ├── decisions.md       # ADRs — what was rejected and why
│   └── evaluation.md      # how quality is measured (mandatory for 06-11)
└── Makefile               # make setup / test / run / clean
```

### 5.4 Rubric (100 points)

| Dimension | Pts | Senior-level bar |
|---|---|---|
| Functionality | 20 | Works, handles errors, no happy-path-only |
| Code quality | 15 | Readable, typed, lint/type clean, no dead code |
| Testing | 15 | Meaningful coverage of logic and edges, not just smoke |
| Architecture | 15 | Clear boundaries, DI, swappable components |
| Observability | 10 | Structured logs, metrics, traceable requests |
| Documentation | 10 | Another engineer can run and extend it |
| Performance | 10 | Measured; bottleneck identified; cost stated |
| Reliability | 5 | Timeouts, retries, graceful degradation |

**Bar: ≥80 to consider a capstone portfolio-ready.** Below 80, the gap is the
next learning objective.

---

## 6. Progress Tracking

Add `supplementary/progress/`:

| File | Purpose |
|---|---|
| `SKILLS-MATRIX.md` | Every topic × 4 levels (Aware / Can use / Can teach / Can design) — self-assessed, dated |
| `CHECKPOINTS.md` | Per-phase gate: quiz score, challenges passed, capstone rubric |
| `SPACED-REVIEW.md` | Review schedule — topics resurface at 1d / 7d / 30d / 90d |
| `INTERVIEW-READINESS.md` | Checklist against a senior AI-engineer job description |

### 6.1 Phase gates

Do not advance until:

| Gate | Requirement |
|---|---|
| Quiz | ≥80% on every topic quiz **and** the phase checkpoint quiz |
| Challenges | 100% Bronze, ≥80% Silver, ≥50% Gold |
| Verification | All `_verify()` in the phase pass on a clean clone |
| Articulation | Can explain any phase topic aloud for 5 minutes without notes |
| Capstone | ≥80 on the rubric where the phase has one |

The articulation gate matters most and is easiest to skip. Recall ≠ understanding;
if you cannot explain the threads-vs-async decision aloud, you do not own it.

---

## 7. Deliverables

| Item | Count |
|---|---|
| New quizzes | ~115 |
| Phase checkpoint quizzes | 9 |
| Challenge directories (×4 files) | ~200 |
| New interview guides | ~30 |
| Capstones built | 12 (5 existing + 7 new) |
| Progress-tracking docs | 4 |

---

## 8. Sequencing

| Step | Work | Notes |
|---|---|---|
| 1 | Challenge scaffolding tool + CI both-directions check | Enables everything else |
| 2 | Challenges for existing topics as `_verify()` retrofits land | Follows Tier 1 |
| 3 | Quizzes for uncovered areas — **Advanced Python first** (0 of 20) | Biggest hole |
| 4 | Progress-tracking docs | Cheap, immediately useful |
| 5 | Interview guides per phase | After phase content lands |
| 6 | Build capstones 01–05 | After Phases 1–7 |
| 7 | Build capstones 06–12 | After Phases 8–9 |

**Never** author a challenge before its topic exercise exists — the challenge must
test what the lecture actually taught.

---

## 9. Exit Criteria

- [ ] Every topic has ≥1 quiz; every phase has a checkpoint quiz
- [ ] Every topic has a 3-tier challenge with hidden tests
- [ ] All challenge tests verified to fail on `starter.py` and pass on `solution.py`
- [ ] Silver/Gold constraints proven to reject naive solutions
- [ ] 45 interview guides with follow-up ladders and red flags
- [ ] 12 capstones running via `docker compose up`, each ≥80 on the rubric
- [ ] Capstones 06–11 include `docs/evaluation.md` with measured quality numbers
- [ ] Progress tracking in place with phase gates defined

---

*Assessment layer for [00-MASTER-PLAN.md](00-MASTER-PLAN.md). Templates: [01-content-standards.md](01-content-standards.md) §5–6.*
