# FastAPI — 47: Resilience Patterns

## Topic Overview

Dependencies fail — the LLM provider 5xxs, the vector DB slows, the
upstream times out. Resilience is the set of patterns that keeps one
dependency's failure from becoming *your* outage. **Timeouts** bound the
wait; **retries with backoff and jitter** survive transient blips without
causing storms; **circuit breakers** stop hammering a dying dependency;
**bulkheads** isolate failure per dependency; **fallbacks** keep the
product usable while degraded. The enemy is **cascading failure**: the
provider blip that becomes your timeout, your retry storm, your SLO
breach. `tenacity` provides battle-tested retry/circuit machinery; this
exercise builds the semantics from scratch so the tradeoffs are visible.

The mental model: your service is only as available as its weakest
dependency — resilience is the blast wall between them and you.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Set explicit timeouts on every outbound call.
2. Retry transient failures with backoff + jitter, capped.
3. Implement a circuit breaker and explain its three states.
4. Use bulkheads to isolate dependencies.
5. Design fallbacks and know when to degrade.

## Prerequisites

| Need | Where |
|---|---|
| Async FastAPI | `32-async-endpoints-deep-lecture.md` |
| Health checks | `46-health-and-readiness-lecture.md` |
| Observability | `43`, `44` lectures |

---

## 1. Timeouts — always set one

An un-timed external call can hang forever, wedging a worker thread and
backing up the queue. A timeout bounds the damage: fail fast, free the
worker, return the fallback. Every outbound call gets an explicit timeout
— HTTP clients take it natively (`httpx.Timeout`), async code uses
`asyncio.wait_for`. No exceptions.

## 2. Retries with backoff and jitter

Retry *transient* failures (5xx, network, timeouts) — never 4xx or bad
input. Two rules keep retries from becoming the problem:

- **Backoff**: exponential delays (20ms → 40ms → 80ms) give the
  downstream time to recover.
- **Jitter**: randomize the delay. Without jitter, 1000 clients retry in
  lockstep — the retry storm that converts a blip into an outage.

Cap attempts (3–5); retrying forever turns a transient blip into a
permanent failure.

## 3. Circuit breaker

A state machine around the failing dependency:

- **CLOSED**: normal; failures count toward the trip threshold.
- **OPEN**: after the threshold — calls fail fast without touching the
  dependency, saving it from your retries.
- **HALF-OPEN**: after the cooldown, one test call decides — success
  closes, failure reopens.

The breaker converts a slow-motion outage into fast failures. Without it,
a dying dependency is hammered by every request, and its outage becomes
yours.

## 4. Bulkheads

One slow dependency should not exhaust the shared pool. A bulkhead gives
each dependency its own concurrency budget — the retrieval bulkhead
filling up does not starve the LLM call bulkhead. Named after ship
compartmentalization: a breach floods one compartment, not the whole hull.

## 5. Fallbacks and degradation

When the premium path fails, degrade gracefully: a cached completion, a
cheaper model, a smaller context window, a stale-but-present answer. The
product stays usable; the SLO breach becomes a quality dip. Degradation
is a product decision — define what "good enough while degraded" means
before the incident.

## Common Mistakes to Avoid

### Mistake 1: No timeouts
```python
# WRONG - one hung provider wedges workers forever
# CORRECT - explicit timeout on every outbound call
```

### Mistake 2: Retry storms
```python
# WRONG - fixed 100ms retries, no jitter, 1000 clients
# CORRECT - exponential backoff + jitter, capped attempts
```

### Mistake 3: Retrying everything
```python
# WRONG - retrying 4xx "because it failed"
# CORRECT - retry 5xx/timeouts only; fail fast on 4xx
```

### Mistake 4: No circuit breaker
```python
# WRONG - hammering a dying dependency until its outage is yours
# CORRECT - breaker trips on threshold, probes after cooldown
```

### Mistake 5: Shared pool for all dependencies
```python
# WRONG - one slow dependency exhausts every other's budget
# CORRECT - bulkheads per dependency
```

## Best Practices

1. Timeout every outbound call; set it where the call is made.
2. Retry transient failures: backoff + jitter, capped, idempotent only.
3. Circuit-break any dependency with a failure history.
4. Bulkhead by dependency class (LLM, DB, vector store, cache).
5. Define fallbacks per endpoint before the incident.
6. Log every degraded path; track breaker state as a metric.
7. Test the failure modes: timeouts, trips, fallbacks — in CI.

## Complexity and Cost

| Concern | Cost | Cheaper alternative |
|---|---|---|
| Timeout | free | — |
| Retry | extra latency per attempt | fewer attempts |
| Circuit breaker | O(1) per call | — |
| Bulkhead | pool sizing decision | — |
| Fallback | design work | — |

Resilience costs latency and design, not compute. The expensive version
is the cascading failure it prevents.

## AI Engineering Relevance

**Where this shows up:** LLM provider calls (the flakiest dependency in
the stack), vector-store queries, model serving behind a gateway, and
agent loops that call tools.

| Concept here | Used for |
|---|---|
| timeouts | bounding LLM generation waits |
| retries | provider 5xx blips with jitter |
| circuit breaker | stopping a dying provider from cascading |
| bulkheads | separate budgets for embed/LLM/rerank |
| fallbacks | cheaper model when premium is down |

**Scale note:** at 10k rps, one provider blip without a breaker is a retry
storm that multiplies load 3–5x — with a breaker, it is 10 seconds of
fast-fail and cached fallbacks.

## Practice Exercises

### Exercise 1: Timeout  (Difficulty: Easy)
Wrap a slow call; assert the timeout fires fast.

### Exercise 2: Retry semantics  (Difficulty: Easy)
Two transient failures then success; assert attempts and outcome.

### Exercise 3: Backoff + jitter  (Difficulty: Medium)
Instrument delays; assert they grow and vary (not lockstep).

### Exercise 4: Circuit breaker  (Difficulty: Medium)
Trip on threshold, fast-fail while open, probe and recover. Assert all
states.

### Exercise 5: Bulkhead  (Difficulty: Medium)
Acquire beyond slots; assert rejection and release.

### Exercise 6: Failure cascade simulation  (Difficulty: Hard)
Model 100 clients × a failing provider with and without breaker +
jitter; assert the breaker version survives while the naive one storms.

## Summary

| Concept | Description |
|---|---|
| timeout | bounds the wait — every call |
| retry | transient only; backoff + jitter |
| circuit breaker | fast-fail, probe, recover |
| bulkhead | per-dependency budgets |
| fallback | degrade, stay usable |
| cascading failure | the thing all of it prevents |

Resilience is the blast wall between your dependencies and your users.
Timeouts, retries done right, breakers, bulkheads, fallbacks — each one
cheap, each one preventing a known failure class.

## Quick Reference

| Task | Idiom |
|---|---|
| Timeout | `httpx.Timeout(5)` / `asyncio.wait_for(coro, 5)` |
| Retry | `tenacity.retry(stop=stop_after_attempt(3), wait=wait_exponential()+wait_random())` |
| Breaker | custom states closed/open/half-open |
| Bulkhead | per-dependency semaphore/slots |
| Fallback | try/except → degraded path |

## Next Steps

Next: **[48 — Docker & FastAPI](48-docker-fastapi-lecture.md)** — packaging
the resilient service for deployment.

Continues in: **[49 — Uvicorn & Gunicorn](49-uvicorn-gunicorn-lecture.md)** —
running it in production with the right worker model.

Official docs:
- tenacity: https://tenacity.readthedocs.io/
- Failure modes (AWS): https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
