# Python AI Engineer Checklist

> Self-audit for **production-ready** Python capability, not notebook familiarity. Derived from
> the same source material as the rest of `docs/reference/`; relocated here 2026-08-02.

## How to use this

Mark each item **Done** · **Needs practice** · **Not started**.

The hiring signal is never the checkbox — it is the **visible artifact**: code, tests,
benchmarks, deployment notes, architecture docs. An item is only Done when you can point at a
file path. Re-audit at each monthly review.

Many Foundations items are already covered by
[`projects/00-core-foundations/python/`](../../projects/00-core-foundations/python/) (354
files across core, advanced, libraries, and FastAPI). The gaps concentrate in **Backend →
Production safeguards** and everything under **Deployment** — which is precisely what the
[active track](../roadmap/active-track-10-week.md) builds.

---

## Foundations

### Core language

- [ ] Confident with lists, dicts, sets, tuples, and comprehensions
- [ ] Understands functions, scope, argument passing, return semantics
- [ ] Uses classes to model services, configs, and domain objects
- [ ] Understands inheritance and magic methods — `__init__`, `__call__`, `__repr__`
- [ ] Uses decorators, generators, and `yield` in real code, not toy examples
- [ ] Handles exceptions with `try/except/finally`; defines custom exceptions where useful
- [ ] Uses `with` blocks; understands context-manager protocol for resource safety
- [ ] Uses `async/await`; knows when async helps I/O-heavy or API workloads
- [ ] Reads and writes type hints using `typing` and modern annotation style

*Repo evidence:* `python/01-core-python/`, `python/02-advanced-python/`

### Clean code

- [ ] Follows PEP8 naming and formatting consistently
- [ ] Writes Pythonic code — `enumerate`, `zip`, unpacking, `dict.get`, truthiness
- [ ] Avoids mutable default arguments and weak naming
- [ ] Uses f-strings, clear names, short single-purpose functions
- [ ] Writes docstrings and coherent module structure for non-trivial paths

*Reference:* [`python-clean-code-checklist.md`](python-clean-code-checklist.md)

### Data handling

- [ ] Comfortable with file I/O, JSON, CSV, and chunked streaming of large inputs
- [ ] Knows NumPy arrays, vectorization, broadcasting at a practical level
- [ ] Knows Pandas for cleaning, merging, grouping, basic analysis
- [ ] **Can write SQL: joins, filtering, aggregation, schema-aware work** ← known gap; week 4

*Repo evidence:* `python/03-libraries/`

---

## Backend

### API engineering

- [ ] FastAPI app with clear routing, request models, response models
- [ ] Pydantic validation; structured schemas instead of raw dicts on important endpoints
- [ ] **Loads models and heavy resources once at startup**, never per request
- [ ] Health endpoints and meaningful HTTP error handling
- [ ] Chooses sync vs. async endpoints deliberately

*Repo evidence:* `python/05-web-frameworks/fastapi/` (25 topics + exercises)

### Project structure

- [ ] Code organized into routes, services, schemas, config, utilities
- [ ] Environment variables and configuration handled cleanly — no secrets in code
- [ ] English README, setup instructions, architecture notes maintained from the start
- [ ] Git confidence: branching, conflict resolution, rebase

### Production safeguards

- [ ] Input validation and guardrails on user-facing AI endpoints
- [ ] Rate limiting, retry strategy, timeout handling for external API calls
- [ ] Logging useful for debugging and operations — not print statements
- [ ] Can explain failure modes for model serving, retrieval, and upstream outages

*Active track:* week 7 · *Artifact:* `devmate/docs/failure-modes.md`

---

## ML tooling

### Experimentation and training

*Largely deferred — see [`ml-fundamentals-map.md`](ml-fundamentals-map.md), week 11+.*

- [ ] Uses notebooks for exploration; moves stable logic into reusable modules
- [ ] scikit-learn preprocessing, pipelines, train/test split, evaluation
- [ ] Overfitting, regularization, task-appropriate metrics (F1, ROC-AUC)
- [ ] Basic PyTorch training loops; `Dataset` and `DataLoader` used properly
- [ ] Tensor operations, autograd, inference contexts like `torch.no_grad()`

### LLM and RAG stack

- [ ] Hugging Face `transformers`, `datasets`, tokenization workflows
- [ ] Embeddings, chunking, retrieval, re-ranking **at implementation level**
- [ ] Can build a minimal RAG pipeline and explain chunk-size trade-offs with numbers
- [ ] Knows the difference between prompt-only, RAG, and fine-tuned systems — and when each applies
- [ ] Evaluates retrieval and answer quality with explicit metrics and a documented harness

*Active track:* weeks 2–3 · *Artifact:* `evaluations/rag/reports/`

### Quality engineering

- [ ] pytest unit tests for core logic and API behaviour
- [ ] Experiments separated from production code paths
- [ ] Experiment or model-behaviour tracking (MLflow, W&B, or equivalent)
- [ ] Assumptions, limitations, and benchmark setup documented per serious artifact

---

## Deployment

### Packaging and runtime

- [ ] Virtual environments or Poetry used correctly
- [ ] Docker images built for API/inference services
- [ ] Can deploy an AI service to Railway, Render, or similar
- [ ] Knows how to expose a public demo **safely** — keys, quotas, abuse limits

*Active track:* week 4

### Reliability and observability

- [ ] Caching where it meaningfully cuts cost or latency (Redis; semantic, not exact-match)
- [ ] Monitoring and tracing (Langfuse or equivalent) on production workflows
- [ ] **Measures latency, cost, and quality** rather than describing them qualitatively
- [ ] Documentation for deployment, environment variables, and rollback

*Active track:* weeks 1 and 7

---

## Proof artifacts

Converting checkboxes into hiring evidence:

| Area | Minimal proof | Strong proof |
| --- | --- | --- |
| Python foundations | utility scripts with clean structure | refactored service module with tests and type hints |
| FastAPI | a working inference endpoint | public AI API with Pydantic schemas, health checks, error handling |
| RAG | local retrieval demo | evaluated RAG service with chunking comparison and documented metrics |
| Deployment | Dockerfile and run steps | live demo with monitoring, cache notes, architecture doc |
| Engineering quality | a linting config | CI-green repo with tests, docs, production notes |

The right-hand column is what the active track produces. The left-hand column is what most
candidates bring.

---

## Priority order

**Python cleanliness → FastAPI serving → RAG evaluation → deployment → observability and
guardrails.**

This matches the active track's progression from local implementation to production delivery,
and it front-loads the artifacts a recruiter can inspect in five minutes.

---

## Related

- [`../roadmap/active-track-10-week.md`](../roadmap/active-track-10-week.md) — the schedule that closes these gaps
- [`python-clean-code-checklist.md`](python-clean-code-checklist.md) — the code-level rules
- [`llm-production-architecture.md`](llm-production-architecture.md) — the production layers
- [`../roadmap/skills-matrix.md`](../roadmap/skills-matrix.md) — numeric skill tracking

*Relocated to `docs/reference/` 2026-08-02; source citations resolved to repo paths.*
