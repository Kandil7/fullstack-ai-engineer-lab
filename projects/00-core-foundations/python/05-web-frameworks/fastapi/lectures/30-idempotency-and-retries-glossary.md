# Idempotency and Retries — Glossary 30

Companion lecture: `30-idempotency-and-retries-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| At-least-once | Delivery | Retries may deliver an operation more than once |
| Dedup store | Mechanism | key -> original result; replays return it |
| Deduplicated | Response | Flag marking a returned replay of an earlier result |
| Exactly-once | Delivery | The unachievable ideal; approximated by at-least-once + dedup |
| Idempotency-Key | Header | Client-supplied unique key per logical operation |
| Idempotent | Property | Repeating the operation yields the same result |
| Retry | Delivery | Client resending a request whose outcome it doesn't know |
| Retry-After | Header | Server tells the client when to retry |
| Safe method | HTTP | GET/HEAD/OPTIONS/TRACE — no side effects, retry freely |
| Side effect | Failure | A state change (charge, job, email) that duplicates on retry |
| Unsafe method | HTTP | POST/DELETE — may create side effects |
| Atomic check | Correctness | Lookup+insert that cannot race |
| Backoff | Delivery | Waiting between retries, often exponential with jitter |
| Replay | Request | A duplicate request with an already-seen key |
| SET NX | Mechanism | Redis atomic set-if-not-exists used for dedup |
| Unique constraint | Mechanism | Database guarantee that a key appears once |
| TTL | Mechanism | Expiry on stored keys bounding store growth |

## Detailed Definitions

### At-least-once
**Definition**: The delivery reality: a request or message may be delivered
more than once. The design assumption; safety comes from deduplication.
**Related**: Exactly-once

### Dedup store
**Definition**: A keyed store mapping Idempotency-Key to the original result,
so replays return the stored response.
**Example**:
```python
store[key] = {"charge_id": cid, "status": "succeeded"}
```
**Related**: Idempotency-Key

### Deduplicated
**Definition**: A response flag telling the client this reply is a replay of
an earlier result, not a new operation.
**Related**: Replay

### Exactly-once
**Definition**: The ideal delivery guarantee — not achievable across a network
because an ack can always be lost. Approximated by at-least-once + idempotency.
**Related**: At-least-once

### Idempotency-Key
**Definition**: A client-supplied header value, unique per logical operation,
sent on every retry of that operation so the server can deduplicate.
**Example**:
```python
key: str | None = Header(default=None, alias="Idempotency-Key")
```
**Related**: Dedup store

### Idempotent
**Definition**: The property that repeating an operation with the same input
produces the same result. PUT is idempotent; POST is not by default.
**Related**: Safe method

### Retry
**Definition**: A client resending a request because the previous attempt's
outcome is unknown (timeout, drop). Requires idempotency to be safe.
**Related**: At-least-once

### Retry-After
**Definition**: A response header on 429/503 telling the client how long to
wait before retrying.
**Example**:
```python
raise HTTPException(429, headers={"Retry-After": "2"})
```
**Related**: Backoff

### Safe method
**Definition**: An HTTP method defined as having no side effects
(GET, HEAD, OPTIONS, TRACE) — retries are free by contract.
**Related**: Unsafe method

### Side effect
**Definition**: A state change (charge, job, email, write) that, if executed
twice, corrupts the system's meaning — the thing retries must not duplicate.
**Related**: Unsafe method

### Unsafe method
**Definition**: An HTTP method (POST, DELETE) that may create side effects;
retries need an idempotency key.
**Related**: Safe method

### Atomic check
**Definition**: A lookup-and-insert that cannot interleave — implemented with
a lock, unique constraint, or SET NX — so concurrent retries deduplicate
correctly.
**Related**: Unique constraint

### Backoff
**Definition**: The strategy of waiting between retries (fixed, exponential,
with jitter) to avoid retry storms; often driven by Retry-After.
**Related**: Retry-After

### Replay
**Definition**: A duplicate request carrying an already-seen idempotency key;
the server returns the stored original result.
**Related**: Deduplicated

### SET NX
**Definition**: Redis's atomic set-if-not-exists command, used as a distributed
dedup primitive across multiple server instances.
**Related**: Atomic check

### Unique constraint
**Definition**: A database guarantee that a column value appears once —
the production-grade way to make the idempotency check atomic.
**Related**: Atomic check

### TTL
**Definition**: Time-to-live on stored idempotency entries (e.g. 24h), bounding
store growth so old keys expire.
**Related**: Dedup store

## Key Concepts Summary

### The problem
- Retries of unsafe methods duplicate side effects.
- The client cannot distinguish "never happened" from "happened, ack lost".

### The fix
- Idempotency-Key per logical operation + dedup store returning original results.
- Atomic check (lock / unique constraint / SET NX) against races.
- Safe methods retry freely; unsafe need a key.

### The delivery truth
- Exactly-once is a fiction; design at-least-once + dedup.
- Retry-After drives server-controlled backoff.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Client-supplied unique key per logical operation — ___
2. The unachievable ideal delivery guarantee — ___
3. key -> original result store — ___
4. Server tells the client when to retry — ___
5. GET/HEAD/OPTIONS/TRACE — ___
6. Lookup+insert that cannot race — ___
7. A duplicate request with a seen key — ___
8. Redis atomic set-if-not-exists — ___

**Answers:** 1-Idempotency-Key, 2-exactly-once, 3-dedup store, 4-Retry-After,
5-safe method, 6-atomic check, 7-replay, 8-SET NX
