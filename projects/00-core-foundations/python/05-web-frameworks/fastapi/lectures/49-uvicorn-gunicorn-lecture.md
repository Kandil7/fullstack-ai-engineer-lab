# FastAPI — 49: Uvicorn & Gunicorn

## Topic Overview

Uvicorn is the **ASGI server** — it speaks the ASGI protocol and runs
your FastAPI app. Gunicorn is the **process manager** — it forks N
workers and supervises them. The production pair is
`gunicorn app.main:app -k uvicorn.workers.UvicornWorker --workers N`.
The load-bearing decision is **N**: CPU-bound workloads (inference!)
get ~1 worker per core; IO-bound workloads can oversubscribe; and in
model-serving, **memory binds before cores** — every worker holds the
model in RAM. Two rules complete the picture: `--reload` is dev-only
(production restarts belong to the orchestrator), and the graceful
timeout must cover your drain window so deploys don't kill in-flight
requests.

The mental model: workers are the concurrency unit; the count is
`min(cores_needed, memory_allowed, stability_margin)`.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain uvicorn vs gunicorn roles and the production pair.
2. Compute worker counts for CPU-, IO-, and memory-bound cases.
3. Explain why --reload is dev-only.
4. Set keep-alive and graceful-shutdown timeouts coherently.
5. Build the production command for a service.

## Prerequisites

| Need | Where |
|---|---|
| FastAPI app | `01-introduction.py` |
| Docker packaging | `48-docker-fastapi-lecture.md` |
| Shutdown/drain | `46-health-and-readiness-lecture.md` |

---

## 1. Two roles, one command

- **uvicorn**: the ASGI server — accepts connections, parses the ASGI
  protocol, runs your app.
- **gunicorn**: the process manager — forks workers, supervises them,
  restarts crashed ones.

Uvicorn alone (`uvicorn app.main:app`) runs a single process. The
production shape uses gunicorn to run N uvicorn workers, each a separate
process: `gunicorn -k uvicorn.workers.UvicornWorker --workers N`.

## 2. The worker math

| Workload | Rule | 4 cores |
|---|---|---|
| CPU-bound (inference, heavy parse) | ~1 per core | 4 |
| IO-bound (DB/API waiting) | 2–4 per core | 9–17 |
| Mixed | cores + 1 | 5 |

CPU-bound work uses one core at a time — more workers than cores means
context-switching without throughput. IO-bound work frees the CPU while
awaiting — workers can oversubscribe. Inside each worker, async handles
concurrency for `async def` endpoints; sync endpoints use the threadpool.

## 3. Memory binds before cores

In model serving each worker imports the model: 4 workers × 2GB model =
8GB before one request. The real constraint is:

```
workers = floor(available_memory / (model_memory + overhead))
```

A 16GB box with a 2GB model fits ~6 workers; an 8GB box with a 4GB model
fits 1. Check memory before you check cores — OOM restarts are the
symptom of getting this backwards.

## 4. --reload is dev-only

`--reload` watches files and restarts on change. In production: extra
file-watcher overhead, restarts on any stray touch, and a hot-reload
worker per process (more memory). Restarts in production belong to the
orchestrator (readiness + liveness from topic 46), not to a file watcher.

## 5. Timeouts

- `--timeout-keep-alive`: idle connection lifetime — short values (5s)
  close idle browser/agent keep-alives; too short hurts connection reuse.
- `--graceful-timeout`: the drain window after SIGTERM — must cover your
  real in-flight duration (a generation can take 30s+), or the orchestrator
  SIGKILLs mid-request.

## Common Mistakes to Avoid

### Mistake 1: `--reload` in production
```python
# WRONG - file-watcher restarts + hot-reload worker memory
# CORRECT - orchestrator owns restarts; no reload in prod
```

### Mistake 2: Workers = cores, ignoring memory
```python
# WRONG - 8 workers × 2GB model on a 16GB box = OOM
# CORRECT - workers = min(cores, floor(mem / per_worker))
```

### Mistake 3: One worker "for simplicity"
```python
# WRONG - one process, one request at a time, no redundancy
# CORRECT - matched to workload and box; >= 2 for availability
```

### Mistake 4: No graceful timeout
```python
# WRONG - SIGTERM kills 30s generations mid-stream
# CORRECT - --graceful-timeout >= drain time
```

## Best Practices

1. gunicorn + UvicornWorker in production; uvicorn alone in dev.
2. Compute workers from workload AND memory.
3. Model-serving: memory first, then cores.
4. --reload only in dev; orchestrator owns prod restarts.
5. Graceful timeout >= longest in-flight request.
6. Keep-alive ~5s unless profiling says otherwise.
7. Monitor per-worker memory to validate the math.

## Complexity and Cost

| Concern | Cost | Cheaper alternative |
|---|---|---|
| Extra worker | +RAM, +process | async concurrency inside workers |
| Oversubscribed CPU workers | context switching | workers = cores |
| Model per worker | GB × workers | one big worker + batching (52) |
| No graceful timeout | dropped requests | timeout >= drain |

Workers cost memory; concurrency inside a worker costs nothing. The
production answer usually mixes: a few workers + async/threads inside.

## AI Engineering Relevance

**Where this shows up:** model-serving endpoints, LLM gateways, and any
service where per-worker memory is measured in GB.

| Concept here | Used for |
|---|---|
| workers = cores | CPU-heavy preprocessing |
| memory-bounded workers | GPU/CPU model serving |
| keep-alive | agent/browser connection reuse |
| graceful timeout | letting generations finish on deploy |

**Scale note:** a serving box with 4 workers × 2GB models serves 4
concurrent generations; a single worker with async + batching can serve
more with the same memory — which is exactly what topic 52 builds.

## Practice Exercises

### Exercise 1: Worker math  (Difficulty: Easy)
Assert io > cpu worker counts for the same cores.

### Exercise 2: Memory constraint  (Difficulty: Easy)
Compute workers by memory; assert the OOM trap case returns 1.

### Exercise 3: Reload policy  (Difficulty: Easy)
Assert reload is dev-only.

### Exercise 4: Command construction  (Difficulty: Medium)
Build the production command; assert the flags and worker count.

### Exercise 5: Timeout coherence  (Difficulty: Medium)
Given a 45s p95 generation, choose a graceful timeout; assert the policy.

### Exercise 6: Capacity model  (Difficulty: Hard)
Model a box (cores, RAM, model size, workload) into a worker count and
concurrency estimate; assert the memory constraint binds.

## Summary

| Concept | Description |
|---|---|
| uvicorn | the ASGI protocol server |
| gunicorn | the process manager/supervisor |
| worker count | min(cores, memory) |
| --reload | dev-only |
| graceful timeout | the drain window |

The production server is a handful of decisions: pair the ASGI server
with a supervisor, count workers from both cores and memory, keep reload
out of prod, and let the graceful timeout cover your longest request.

## Quick Reference

| Task | Idiom |
|---|---|
| Dev | `uvicorn app.main:app --reload` |
| Prod | `gunicorn app.main:app -k uvicorn.workers.UvicornWorker --workers N` |
| Workers CPU | `cores` |
| Workers IO | `2*cores + 1` |
| Workers mem | `floor(mem / (model + overhead))` |
| Drain | `--graceful-timeout >= p95 latency` |

## Next Steps

Next: **[50 — Configuration](50-configuration-lecture.md)** — the env vars
the running service needs.

Continues in: **[51 — CI/CD](51-ci-cd-lecture.md)** — building, scanning,
and shipping the image.

Official docs:
- Uvicorn deployment: https://www.uvicorn.org/deployment/
- Gunicorn: https://docs.gunicorn.org/
