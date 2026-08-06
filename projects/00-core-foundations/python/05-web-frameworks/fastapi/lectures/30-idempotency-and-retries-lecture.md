# FastAPI — 30: Idempotency and Retries

Companion exercise: `30-idempotency-and-retries.py`

---

## Topic Overview

Networks drop, time out, and duplicate. Clients retry — and every retry of a
non-idempotent request can duplicate a side effect: two charges, two emails,
two jobs. This topic covers the discipline that makes retries safe:
**idempotency keys** (the client sends a unique key; the server deduplicates),
the safe-vs-unsafe method distinction, `Retry-After` for server-driven backoff,
and the uncomfortable truth that **exactly-once is a fiction** — the honest
design is at-least-once delivery plus deduplication.

The core mental model: a retry must be indistinguishable from the original
request. The Idempotency-Key header is how a server makes that true.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the retry problem with a concrete side-effect example.
2. Implement an Idempotency-Key header and dedup store.
3. Return the original response on a replay, flagged as deduplicated.
4. Distinguish safe methods (retry freely) from unsafe (need a key).
5. Use Retry-After to drive client backoff.
6. Explain why exactly-once is unachievable and what to design instead.
7. Protect the dedup check with locking against concurrent retries.
8. Test idempotency with duplicate and concurrent requests.

## Prerequisites

| Need | Where |
|---|---|
| Request headers | `04-query-parameters.py` |
| Request bodies | `05-request-body.py` |
| Error handling | `29-error-handling-rfc9457.py` |

## 1. The Problem: Retries Duplicate Side Effects

```python
@app.post("/naive/charges")
def naive_charge(body: ChargeRequest):
    charge_id = str(uuid.uuid4())
    _CHARGES.append(charge_id)
    return {"charge_id": charge_id}
```

Output:
```
# First POST  -> charge A
# Client retry (timeout, no response) -> charge B  <-- double charge!
```

The client timed out waiting for a response — it does not know whether the
charge happened. It retries, and the server charges twice. The failure is not
the network; it is the server treating two identical requests as two distinct
operations.

## 2. The Fix: Idempotency-Key + Dedup Store

```python
@app.post("/charges")
def charge(body: ChargeRequest,
           idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")):
    existing = _IDEMPOTENCY.get(idempotency_key)
    if existing is not None:
        existing["attempts"] += 1
        return ChargeResponse(charge_id=existing["charge_id"], deduplicated=True, ...)

    charge_id = str(uuid.uuid4())
    _CHARGES.append(charge_id)
    _IDEMPOTENCY[idempotency_key] = {...}
    return ChargeResponse(charge_id=charge_id, ...)
```

Output:
```
# POST /charges  Idempotency-Key: order-123 -> charge X
# POST /charges  Idempotency-Key: order-123 -> charge X, deduplicated: true
```

The client generates a UUID per logical operation and sends it on every retry
of that operation. The server keeps a store of key -> original result. A replay
returns the **original** response, so the client sees the same charge ID and
knows nothing new happened. Stripe, PayPal, and most payment APIs work exactly
this way.

## 3. Safe vs Unsafe Methods — The Retry Rule

```python
SAFE_METHODS = {"GET", "HEAD", "OPTIONS", "TRACE"}

def can_retry(method, has_idempotency_key):
    if method in SAFE_METHODS:
        return True, "safe method: retry freely"
    if has_idempotency_key:
        return True, "unsafe with key: safe to retry"
    return False, "unsafe without key: retrying may duplicate"
```

Output:
```
# GET    -> retry freely (no side effect by contract)
# POST   + key -> retry safely
# DELETE without key -> retry may duplicate or fail unexpectedly
```

HTTP semantics: GET/HEAD/OPTIONS/TRACE are defined as safe (no side effects),
so retries are free. PUT is idempotent by definition (same body, same result).
POST and DELETE need an explicit key to be retried safely.

## 4. Retry-After — Server-Driven Backoff

```python
raise HTTPException(429, detail="Rate limit exceeded",
                    headers={"Retry-After": "2"})
```

Output:
```
# 429 + Retry-After: 2  -> client waits 2s before retrying
```

When the server is overloaded or rate-limited, it should tell the client *when*
to retry instead of letting clients hammer it. `Retry-After` carries seconds
(or an HTTP-date) and is the standard signal on 429 and 503.

## 5. Exactly-Once Is a Fiction — Design for At-Least-Once + Dedup

Exactly-once delivery is not achievable across a network: a message can always
be lost after the side effect commits but before the acknowledgment arrives.
The honest design:

1. Assume at-least-once delivery (retries happen).
2. Make each operation idempotent (same key -> same result).
3. Deduplicate at the side-effect boundary (the store, the lock).
4. Idempotency keys make at-least-once **equivalent to** exactly-once from
   the client's perspective.

## 6. Concurrency — The Check Must Be Atomic

Two racing retries with the same key can both miss the dedup store and both
perform the side effect. The lookup-and-insert must be atomic: a database
unique constraint, a Redis `SET NX`, or an in-process lock around the check.

```python
with _LOCK:                       # or a DB unique constraint on the key
    existing = _IDEMPOTENCY.get(key)
    if existing is None:
        # side effect happens exactly once
        _IDEMPOTENCY[key] = entry
```

Output:
```
# two concurrent retries, same key -> one charge, one stored entry
```

## 7. Common Mistakes to Avoid

### Mistake 1: No idempotency on money/effect endpoints
```python
# WRONG — POST /charges with no key and no dedup
# CORRECT — require Idempotency-Key on any unsafe, effectful POST
```

### Mistake 2: Returning a fresh result on replay
```python
# WRONG — replay returns a NEW id, client believes it's a second operation
# CORRECT — return the stored ORIGINAL response, marked deduplicated
```

### Mistake 3: Non-atomic dedup check
```python
# WRONG — check, then insert, with a gap between them (race)
# CORRECT — lock / unique constraint / SET NX around the side effect
```

### Mistake 4: Letting clients invent keys lazily
```python
# WRONG — client sends a key only sometimes
# CORRECT — require the key for unsafe methods; reject without it
```

### Mistake 5: Hammering retries with no backoff
```python
# WRONG — instant retry storm on 429
# CORRECT — honor Retry-After; exponential backoff with jitter
```

## 8. Best Practices

1. Require Idempotency-Key on every unsafe, effectful endpoint.
2. Store the key with the original response and return it on replay.
3. Make the dedup check atomic (lock, unique constraint, SET NX).
4. Set a key TTL (e.g. 24h) so the store doesn't grow forever.
5. Send Retry-After on 429/503.
6. Document the retry contract: which methods are safe, which need keys.
7. Flag replays (`deduplicated: true`) so clients can log them.
8. Use the same key across retries of one logical operation — never per-attempt.
9. Test with concurrent duplicate requests.
10. Treat exactly-once as a goal achieved via at-least-once + dedup.

## 9. Complexity and Cost

| Operation | Time | Space | Notes |
|---|---|---|---|
| Idempotency lookup | O(1) hash | keyed store | TTL-bounded |
| Storing a result | O(1) | per unique key | Reuse the response bytes |
| Atomic check | O(1) | lock/unique index | Required for correctness |
| Retry-After handling | O(1) | none | Server-driven backoff |

The cost of idempotency is a keyed store with TTLs — trivially cheap compared
to the cost of a duplicate side effect.

## 10. AI Engineering Relevance

**Where this shows up:** payment and billing for LLM usage, job submission
APIs, ingestion pipelines, and any endpoint whose side effect costs money.

| Concept here | Used for |
|---|---|
| Idempotency keys | Ensuring a billing job runs once per prompt batch |
| Dedup store | Deduplicating document-ingestion requests in RAG pipelines |
| Retry-After | Honoring LLM provider rate limits |
| At-least-once + dedup | Reliable retry of embedding generation at scale |
| Atomic checks | Safe concurrent re-indexing without duplicate work |

**Scale note:** at high concurrency, the atomicity requirement moves from an
in-process lock to a distributed primitive (unique constraint, Redis SET NX).
The pattern is identical — only the storage changes.

## 11. Summary

| Concept | Description |
|---|---|
| The retry problem | Retries duplicate side effects without dedup |
| Idempotency-Key | Client-supplied key making retries indistinguishable |
| Dedup store | key -> original response; replays return it |
| Safe methods | GET/HEAD/OPTIONS retry freely |
| Retry-After | Server-driven backoff on 429/503 |
| Exactly-once | A fiction; design at-least-once + dedup |

## 12. Quick Reference

| Task | Idiom |
|---|---|
| Require a key | `key: str | None = Header(alias="Idempotency-Key")` |
| Dedup lookup | `existing = store.get(key)` |
| Atomic check | `with lock:` or DB unique constraint |
| Replay response | return stored result + `deduplicated: true` |
| Backoff signal | `HTTPException(429, headers={"Retry-After": "2"})` |
| Retry rule | safe method OR unsafe method with key |

## Next Steps

Next: **[31 — OpenAPI and Clients](31-openapi-and-clients-lecture.md)** — the schema that documents the contract.

Continues in: **[04-databases — Redis 03 Caching](../../04-databases/redis/lectures/03-caching-patterns-lecture.md)** — cache-aside, another at-least-once pattern.

Official docs: <https://stripe.com/docs/api/idempotent_requests> · <https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header>
