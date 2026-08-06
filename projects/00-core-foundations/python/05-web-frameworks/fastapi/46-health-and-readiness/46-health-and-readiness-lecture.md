# FastAPI — 46: Health & Readiness

## Topic Overview

Orchestrators decide your service's fate from its health endpoints — so
getting the probes right is operational survival. Three DIFFERENT probes
with three different jobs: **liveness** ("is the process alive?" → crash
= restart), **readiness** ("can it serve traffic?" → no = stop routing,
keep the process), **startup** ("is it still warming up?" → yes = delay
the other probes). The classic incident is the wrong probe on the wrong
endpoint: a readiness check that 500s on a DB blip makes the orchestrator
restart a perfectly healthy process — a self-inflicted crash loop. And
**graceful shutdown** (stop accepting → drain in-flight → exit) is what
keeps deploys from killing generations mid-stream.

The mental model: liveness is about the process, readiness about
*dependencies*, startup about *time*. Conflating them is how healthy
services get restarted.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain liveness vs readiness vs startup and when each fires.
2. Build dependency-checked readiness that fails soft.
3. Implement graceful shutdown with in-flight draining.
4. Wire SIGTERM handling to the drain sequence.
5. Predict how probes behave across a deploy.

## Prerequisites

| Need | Where |
|---|---|
| FastAPI app lifecycle | `25-events.py` |
| Observability | `43`, `44`, `45` lectures |
| Process signals | Python `signal` module |

---

## 1. Three probes, three questions

| Probe | Question | Answer | Orchestrator action |
|---|---|---|---|
| liveness | is the process alive? | 500 | restart container |
| readiness | can it serve traffic? | 503 | stop routing (keep process) |
| startup | is it still warming up? | 503 | delay other probes |

Liveness must NEVER depend on external services — a DB blip is not a dead
process. Readiness SHOULD check dependencies (with short, cached checks).
Startup gates traffic until the pod is actually warm (e.g. a loaded model).

## 2. Dependency-checked readiness

```python
@app.get("/health/ready")
def ready():
    if not all(check_deps()):          # short, cached checks
        return JSONResponse({"failed": [...]}, status_code=503)
    return {"status": "ready"}
```

Readiness polls critical dependencies — DB, cache, model — with short
timeouts and a few-seconds cache so a slow dependency cannot make probes
flaky. Fail = orchestrator stops routing; the process lives to recover.

## 3. Graceful shutdown and draining

On SIGTERM (deploy, scale-down, node drain):

1. **Stop accepting** new work (flag checked at request start).
2. **Drain**: let in-flight requests finish within a grace period.
3. **Exit**: force-exit if the grace period expires.

Killing mid-request drops a generation; draining lets it complete. The
grace period is the contract: orchestrators wait `terminationGracePeriod`
before SIGKILL — a service that drains slowly gets killed anyway.

## 4. Deployment interaction

- **Cold start**: startup probe holds traffic while the model loads —
  without it, requests hit an unready pod and 5xx.
- **Rolling deploy**: readiness gates each new pod; traffic shifts only
  to warm pods; old pods drain on SIGTERM.
- **DB blip**: readiness 503s, traffic stops, liveness stays 200, the
  pod survives.

## Common Mistakes to Avoid

### Mistake 1: One /health for everything
```python
# WRONG - a DB blip 500s liveness and the pod is restarted
# CORRECT - /health/live (process), /health/ready (deps), /health/startup
```

### Mistake 2: Slow readiness checks
```python
# WRONG - each probe polls the DB with a 10s timeout; probes pile up
# CORRECT - short timeouts + a few-seconds cache
```

### Mistake 3: No drain
```python
# WRONG - SIGTERM exits immediately, dropping in-flight generations
# CORRECT - refuse new work, drain within grace, then exit
```

### Mistake 4: No startup probe
```python
# WRONG - orchestrator routes traffic into a pod loading a 2GB model
# CORRECT - startup probe gates traffic until warm
```

### Mistake 5: Restarting on dependency failure
```python
# WRONG - crash-looping a process whose DB simply blipped
# CORRECT - liveness ignores deps; readiness handles them
```

## Best Practices

1. Three endpoints: live, ready, startup — never one.
2. Liveness: process only. Readiness: cached, short dependency checks.
3. Startup probe gates traffic until warm.
4. SIGTERM → stop accepting → drain within grace → exit.
5. Set the grace period to your real drain time.
6. Log probe results; track readiness flaps as a metric.

## Complexity and Cost

| Concern | Cost | Cheaper alternative |
|---|---|---|
| Probe endpoints | O(1) per poll | — |
| Dependency checks | cached seconds | — |
| Drain wait | up to grace period | shorter grace |
| Wrong-probe restart | whole pod | correct probe semantics |

The cost of health endpoints is trivial; the cost of conflating them is
crash loops and dropped traffic.

## AI Engineering Relevance

**Where this shows up:** model-serving pods (2GB models = long cold
starts), GPU workers (readiness = model loaded + GPU healthy), and every
LLM endpoint behind a rolling deploy.

| Concept here | Used for |
|---|---|
| startup probe | gating traffic until the model is loaded |
| readiness | routing only to warm, dep-healthy pods |
| liveness | restarting truly dead workers only |
| graceful drain | deploys without dropping generations |
| SIGTERM wiring | coordinated shutdown on scale-down |

**Scale note:** with 1GB+ models, cold start is minutes — the startup
probe is what makes rolling deploys possible at all.

## Practice Exercises

### Exercise 1: Probe semantics  (Difficulty: Easy)
Assert liveness ignores deps; readiness gates on them; startup gates on
warmth.

### Exercise 2: Dependency failure  (Difficulty: Easy)
Flip a dependency; assert readiness 503s while liveness stays 200.

### Exercise 3: Drain  (Difficulty: Medium)
Two in-flight requests; assert new work is refused and drain completes.

### Exercise 4: Drain timeout  (Difficulty: Medium)
A hanging request; assert drain fails on timeout (force-exit path).

### Exercise 5: Deploy sequence  (Difficulty: Hard)
Model the full sequence — startup gated, readiness green, traffic flows;
assert ordering.

### Exercise 6: Probe wiring in FastAPI  (Difficulty: Hard)
Three real endpoints + a SIGTERM handler in a TestClient-friendly app;
assert the statuses at each lifecycle stage.

## Summary

| Concept | Description |
|---|---|
| liveness | the process is alive |
| readiness | the dependencies can serve |
| startup | the pod is warmed |
| drain | in-flight work finishes before exit |
| SIGTERM | stop accepting, drain, exit |

Health endpoints are a contract with the orchestrator. Give it three
honest answers — alive, ready, started — and drain gracefully, and the
platform will treat your service the way it deserves.

## Quick Reference

| Task | Idiom |
|---|---|
| Liveness | process-only 200/500 |
| Readiness | deps checked with cache; 503 lists failures |
| Startup | 503 until warm; gates traffic |
| Shutdown | `signal.SIGTERM` → drain flag → finish → exit |
| Grace | match `terminationGracePeriod` |

## Next Steps

Next: **[47 — Resilience Patterns](47-resilience-patterns-lecture.md)** —
timeouts, retries with jitter, circuit breakers, and bulkheads.

Continues in: **[48 — Docker & FastAPI](48-docker-fastapi-lecture.md)** —
packaging the service the orchestrator will run.

Official docs:
- K8s probes: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
- K8s termination: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination
