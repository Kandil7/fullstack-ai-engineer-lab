# Phase 5 — Backend Engineering (`05-web-frameworks/`)

> **Current:** 45 exercises (FastAPI 25 + 25 paired exercises, Django 20),
> 45 lectures. FastAPI not smoke-tested (needs a server); **Django cannot run at
> all — the package is not installed.**
> **Target:** ~52 FastAPI topics covering production concerns; Django reduced to
> reference; new `system-design/` section.

---

## 1. Current State

| Framework | Exercises | `exercises/` | Lectures | Status |
|---|---|---|---|---|
| FastAPI | 25 | 25 | 25 | Well-structured; the only section with paired practice files |
| Django | 20 | — | 20 | **`ModuleNotFoundError: No module named 'django'`** |

### 1.1 FastAPI is the strongest section in the module

It is the only section with a dedicated `exercises/` directory — 25 practice files
with hints and TODO-driven structure. `pydantic` appears in 33 files. Coverage of
the framework surface (routing, DI, middleware, auth, WebSockets, ORM, testing) is
solid. **Do not restructure it. Extend it.**

### 1.2 Django decision (R7)

`requirements.txt` has `# django>=5.0.0` commented out; `pyproject.toml` lists
`django>=4.2` as a **core** dependency. The two contradict each other, and the
package is absent.

**Recommendation: make Django explicitly reference-only.**

| Rationale | |
|---|---|
| `README.md` already labels it "(reference)" while FastAPI is "(runnable)" | Formalize existing intent |
| Django is peripheral to AI engineering | FastAPI/async is the ecosystem standard for model serving |
| 20 non-running files in CI is worse than 20 honestly-labeled reference files | Keeps the gate green and truthful |

**Actions:** resolve the `pyproject.toml`/`requirements.txt` contradiction; exclude
`django/` from the smoke runner with a stated reason; add a `README.md` note
explaining what to read Django *for* (the ORM and admin are genuinely instructive);
keep the 20 lectures.

---

## 2. Gaps — Production Concerns Are Absent

Measured repo-wide `.py` occurrences:

| Concern | Files | Consequence |
|---|---|---|
| `Dockerfile` | **0** | Cannot deploy anything |
| `opentelemetry` | **0** | No tracing |
| `prometheus` | **0** | No metrics |
| `structlog` | **0** | No structured logs |
| `celery` | **0** | No durable background work |
| `alembic` | **0** | No schema evolution |
| `idempoten` | 1 | Retry safety untaught |
| `circuit.break` | 1 | Resilience untaught |

The existing 25 topics teach how to *write* an API. They do not teach how to
*operate* one — which is the entire distance between mid and senior.

---

## 3. FastAPI: New Topics 26–52

### 3.1 API Design and Correctness (26–31)

| # | Topic | Concepts |
|---|---|---|
| 26 | `26-pydantic-v2-deep.py` | `BaseModel` internals; validators (`field_validator`, `model_validator`); `Field` constraints; `computed_field`; serialization aliases; `model_config`; strict mode; custom types; **performance of v2 core**; `TypeAdapter` |
| 27 | `27-api-versioning.py` | URL path vs header vs media-type versioning; deprecation policy and `Sunset` headers; breaking vs additive changes; supporting two versions in one app |
| 28 | `28-pagination-and-filtering.py` | Offset vs **keyset/cursor** pagination (and why offset breaks at scale); sorting; filter DSLs; `Link` headers; total-count cost |
| 29 | `29-error-handling-rfc9457.py` | Problem Details (RFC 9457); consistent error envelopes; exception handlers; **never leaking internals**; validation error shaping; client-actionable messages |
| 30 | `30-idempotency-and-retries.py` ⭐ | Idempotency keys; safe vs unsafe methods; at-least-once delivery reality; dedup storage; `Retry-After`; exactly-once as a fiction |
| 31 | `31-openapi-and-clients.py` | Customizing the schema; tags and operation IDs; security schemes; examples; generating typed clients; contract testing; docs as the API surface |

### 3.2 Performance and Concurrency (32–37)

| # | Topic | Concepts |
|---|---|---|
| 32 | `32-async-endpoints-deep.py` ⭐ | `def` vs `async def` in FastAPI (**the threadpool subtlety most people get wrong**); never block the loop; `run_in_threadpool`; measuring both; when sync is correct |
| 33 | `33-database-async.py` | Async SQLAlchemy in requests; session-per-request DI; pool sizing vs worker count; transaction scope; avoiding pool exhaustion |
| 34 | `34-caching-strategies.py` | Response caching; `ETag`/`If-None-Match`; `Cache-Control`; Redis-backed caching; **cache-key design**; invalidation; per-user vs shared |
| 35 | `35-background-jobs.py` | `BackgroundTasks` limits (**lost on restart**); Celery/RQ/ARQ; job durability; retries and DLQs; progress reporting; when to use which |
| 36 | `36-streaming-and-sse.py` ⭐ | `StreamingResponse`; Server-Sent Events; chunked transfer; **streaming LLM tokens**; client disconnect handling; backpressure |
| 37 | `37-load-testing.py` | `locust`/`k6`; open vs closed models; p50/p95/p99 (**never averages**); saturation; finding the real bottleneck; capacity planning |

### 3.3 Security (38–42)

| # | Topic | Concepts |
|---|---|---|
| 38 | `38-auth-deep.py` | Session vs token; JWT structure, signing, and **what JWTs are bad at**; refresh rotation; revocation lists; `argon2`/`bcrypt`; timing-safe compare |
| 39 | `39-oauth2-oidc.py` | Authorization Code + PKCE; scopes vs claims; ID vs access tokens; JWKS and key rotation; third-party providers |
| 40 | `40-authorization.py` | RBAC vs ABAC; resource-level checks; **multi-tenant isolation**; policy as data; DI-enforced permissions; the confused-deputy problem |
| 41 | `41-api-security.py` | Rate limiting per identity; CORS **correctly** (not `*`); CSRF for cookie auth; security headers; request size limits; input validation; SSRF; secrets handling |
| 42 | `42-security-testing.py` | Auth bypass tests; fuzzing inputs; `bandit`; `pip-audit`; dependency CVEs; threat modeling an endpoint |

### 3.4 Observability and Operations (43–47)

| # | Topic | Concepts |
|---|---|---|
| 43 | `43-structured-logging.py` | `structlog`; JSON logs; **correlation/request IDs through async context**; log levels in production; sampling; PII redaction; cost of logging |
| 44 | `44-metrics-prometheus.py` | The four golden signals; counters/gauges/histograms; RED and USE methods; cardinality explosions; `/metrics`; **SLI/SLO definition** |
| 45 | `45-tracing-opentelemetry.py` | Spans and context propagation; auto vs manual instrumentation; sampling; tracing across services; **tracing an async RAG pipeline end to end** |
| 46 | `46-health-and-readiness.py` | Liveness vs readiness vs startup (**they are different**); dependency checks; graceful shutdown and in-flight draining; `SIGTERM`; deployment interaction |
| 47 | `47-resilience-patterns.py` | Timeouts (**always set one**); retries with jitter; circuit breakers; bulkheads; fallbacks and degradation; `tenacity`; cascading-failure prevention |

### 3.5 Deployment (48–52)

| # | Topic | Concepts |
|---|---|---|
| 48 | `48-docker-fastapi.py` | Multi-stage builds; layer caching; slim vs alpine (**and why alpine hurts Python**); non-root user; `.dockerignore`; image size; reproducible builds |
| 49 | `49-uvicorn-gunicorn.py` | ASGI servers; worker counts vs cores; `uvloop`; keep-alive; timeouts; when threads vs processes; **why not `--reload` in production** |
| 50 | `50-configuration.py` | `pydantic-settings`; env precedence; secret managers; per-environment config; validation at startup (**fail fast**); feature flags |
| 51 | `51-ci-cd.py` | Test → build → scan → deploy; matrix testing; caching; migrations in the pipeline; blue-green and canary; rollback |
| 52 | `52-serving-ml-models.py` ⭐ | Model loading at startup (not per request); warmup; batching for throughput; GPU vs CPU; `/predict` contracts; versioning; async inference; **memory per worker with a loaded model** |

Topics `32`, `36`, and `52` are the three that most directly serve the AI-engineer
target: how async actually behaves in FastAPI, how to stream tokens, and how to
serve a model without exhausting memory.

---

## 4. New: `05-web-frameworks/system-design/` (10 topics)

Senior interviews and senior work are both design-heavy. No exercises here — these
are lecture + worked-artifact topics.

| # | Topic | Concepts |
|---|---|---|
| 01 | `01-fundamentals.md` | Latency vs throughput; back-of-envelope math; **latency numbers every engineer should know**; CAP honestly; consistency models |
| 02 | `02-scaling-patterns.md` | Vertical vs horizontal; stateless services; load balancing; sharding; read replicas; caching layers |
| 03 | `03-api-gateway-and-bff.md` | Gateway responsibilities; BFF; service mesh; when a monolith is correct |
| 04 | `04-queues-and-events.md` | Queues vs streams; Kafka vs SQS vs Redis Streams; ordering; delivery semantics; outbox pattern; event-driven tradeoffs |
| 05 | `05-data-consistency.md` | Transactions across services; sagas; eventual consistency; idempotency; distributed-transaction avoidance |
| 06 | `06-multi-tenancy.md` | Shared vs isolated schema vs isolated DB; noisy neighbors; per-tenant limits; data isolation guarantees |
| 07 | `07-designing-an-llm-api.md` ⭐ | Streaming; token accounting and quotas; provider fallback; caching semantics; cost per request; abuse prevention; timeout budgets |
| 08 | `08-designing-a-rag-system.md` ⭐ | Ingestion vs query paths; chunking strategy; index freshness; hybrid retrieval; reranking budget; eval loop; cost model |
| 09 | `09-designing-an-inference-platform.md` | Model registry; autoscaling on GPU; batching; cold starts; canary for models; A/B on model versions |
| 10 | `10-design-review-checklist.md` | A reusable checklist: scale, failure modes, data, security, cost, observability, rollout, and the questions to ask |

---

## 5. Retrofit FastAPI's Existing 25

### 5.1 Make them testable
FastAPI files cannot smoke-test by running a server. Use `TestClient` instead —
this is the correct pattern and doubles as the testing lesson:

```python
def _verify() -> None:
    from fastapi.testclient import TestClient
    client = TestClient(app)

    r = client.get("/items")
    assert r.status_code == 200, f"expected 200, got {r.status_code}"
    assert "items" in r.json()

    r = client.post("/items", json={"name": "x"})
    assert r.status_code == 201, "POST must return 201 Created"

    r = client.get("/items/99999")
    assert r.status_code == 404, "missing resource must 404"

    r = client.post("/items", json={})           # validation
    assert r.status_code == 422, "invalid body must 422"
    print("[OK] all endpoint checks passed")
```

This makes all 25 FastAPI files CI-verifiable **without** running `uvicorn` —
resolving the "not smoke-tested" gap in the baseline.

### 5.2 Add to all 25 lectures
`## Complexity and Cost` (per-request cost, N+1 risk, connection usage) and
`## AI Engineering Relevance` (each endpoint pattern mapped to a model-serving or
RAG scenario).

---

## 6. Deliverables

| Item | Count |
|---|---|
| Django R7 resolution | docs + CI exclusion |
| FastAPI new topics `26`–`52` | 27 |
| FastAPI new lecture+glossary pairs | 54 |
| FastAPI new paired `exercises/` files | 27 |
| `TestClient` `_verify()` retrofits | 25 |
| Lecture retrofits | 25 |
| `system-design/` topics | 10 |
| Challenges | 52 dirs |
| Quizzes | ~12 |

---

## 7. Sequencing

| Step | Work | Depends on |
|---|---|---|
| 1 | R7 Django decision + CI exclusion | Tier 0 |
| 2 | `TestClient` `_verify()` in 25 files | — |
| 3 | `32-async-endpoints-deep` | Phase 2 `21`/`22` (concurrency) |
| 4 | `26`–`31` (API design) | step 2 |
| 5 | `33`–`37` (performance) | Phase 4 SQLAlchemy |
| 6 | `38`–`42` (security) | Phase 2 `33-security-essentials` |
| 7 | `43`–`47` (observability) | step 2 |
| 8 | `48`–`52` (deployment) | steps 4–7 |
| 9 | `system-design/` | after `48`–`52` |
| 10 | Challenges + quizzes | after exercises |

Step 2 is the highest-leverage item: it converts 25 untested files into 25 gated ones.

---

## 8. Exit Criteria

- [ ] All 25 existing FastAPI files verified via `TestClient` in CI
- [ ] 52 FastAPI topics, each with lecture, glossary, and paired exercise
- [ ] Django status unambiguous; `pyproject.toml`/`requirements.txt` reconciled
- [ ] A learner can containerize and deploy a service from this content alone
- [ ] Observability covered: structured logs, metrics, traces, health checks
- [ ] Security covered: authn, authz, rate limits, CORS, headers, dependency scanning
- [ ] Streaming/SSE working — token streaming demonstrated
- [ ] `52-serving-ml-models` shows a real model behind an endpoint with memory measured
- [ ] `system-design/` includes the LLM API and RAG system designs

---

*Phase 5 of [00-MASTER-PLAN.md](00-MASTER-PLAN.md). Django decision: [10-remediation-backlog.md](10-remediation-backlog.md) R7.*
