# Resilience Patterns — Glossary 47

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Backoff | Retry | Increasing delay between attempts |
| Bulkhead | Pattern | Per-dependency concurrency budget; failure isolation |
| Cascading failure | Failure | One dependency's outage spreading through retries |
| Circuit breaker | Pattern | Stop calling a failing dependency; probe later |
| CLOSED | Breaker | Normal state — calls flow |
| Fallback | Pattern | Degrading to a cheaper/cached path on failure |
| HALF-OPEN | Breaker | Probing state after cooldown — one test call |
| Jitter | Retry | Randomizing delays to prevent synchronized storms |
| OPEN | Breaker | Fast-fail state — calls rejected immediately |
| Retry | Pattern | Re-attempting transient failures with backoff |
| Timeout | Pattern | Bounding how long an outbound call may take |
| Transient | Failure | A failure that may succeed on retry (5xx, network) |

## Detailed Definitions

### Backoff
**Definition**: The increasing delay between retries (exponential: 20ms,
40ms, 80ms) — gives the downstream time to recover instead of hammering.
**Related**: Retry

### Bulkhead
**Definition**: Giving each dependency its own concurrency/thread budget —
a slow dependency exhausts its own slots, not the shared pool.
**Related**: Cascading failure

### Cascading failure
**Definition**: One dependency's outage spreading — provider blip → your
timeouts → retry storm → your SLO breach. Resilience patterns exist to
break this chain.
**Related**: Circuit breaker

### Circuit breaker
**Definition**: A state machine (closed/open/half-open) that stops calling
a failing dependency after a threshold and probes after a cooldown —
converting slow-motion outages into fast failures.
**Related**: OPEN

### CLOSED
**Definition**: The breaker's normal state — calls flow through; failures
count toward the trip threshold.
**Related**: OPEN

### Fallback
**Definition**: The degraded path when the primary fails — cached result,
cheaper model, smaller context — keeping the product usable.
**Related**: Retry

### HALF-OPEN
**Definition**: The breaker's probing state after cooldown — one test call
decides between recovery (closed) and another outage (open).
**Related**: Circuit breaker

### Jitter
**Definition**: Randomizing retry delays so thousands of clients do not
retry in lockstep — the fix for synchronized retry storms.
**Related**: Backoff

### OPEN
**Definition**: The breaker's fast-fail state — calls are rejected
immediately without touching the dependency.
**Related**: Circuit breaker

### Retry
**Definition**: Re-attempting a transient failure with backoff + jitter —
correct for 5xx/timeouts, wrong for 4xx and bad input.
**Related**: Backoff

### Timeout
**Definition**: The upper bound on an outbound call's duration — the
simplest resilience pattern; every external call needs one.
**Related**: Retry

### Transient
**Definition**: A failure likely to succeed on retry — network blips, 5xx,
timeouts — as opposed to permanent 4xx errors.
**Related**: Retry

## Key Concepts Summary

### The pattern stack
- Timeout every outbound call (bounds the damage).
- Retry transient failures (backoff + jitter, capped).
- Circuit breaker on failing dependencies (fast-fail, probe).
- Bulkheads per dependency (isolation).
- Fallbacks (degradation keeps the product usable).

### The enemy
- Cascading failure: one dependency's outage becomes your outage.
- Retry storms: synchronized retries multiply the load.

### The rules
- Retry 5xx/timeouts; never retry 4xx.
- Cap attempts; never retry forever.
- Break the circuit before the dependency's outage is yours.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Bounding how long a call may take — ___
2. Increasing delay between attempts — ___
3. Randomizing delays — ___
4. Stop calling after a failure threshold — ___
5. Fast-fail breaker state — ___
6. One test call after cooldown — ___
7. Per-dependency concurrency budget — ___
8. The degraded path on failure — ___

**Answers:** 1-timeout, 2-backoff, 3-jitter, 4-circuit breaker, 5-OPEN,
6-HALF-OPEN, 7-bulkhead, 8-fallback
