# FastAPI — 34: Caching Strategies

Companion exercise: `34-caching-strategies.py`

---

## Topic Overview

Caching is where API performance is actually won: the right cache turns a
50ms database-backed endpoint into a 1ms cache hit and cuts provider bills in
LLM systems. This topic covers the cache stack in layers — HTTP-level caching
with `ETag`/`If-None-Match` and `Cache-Control`, server-side cache-aside with
TTLs, and the design rules that decide whether a cache helps or poisons:
cache-key design, invalidation, and the per-user-vs-shared boundary.

The core discipline: **a cache is a copy, and copies go stale.** Every caching
decision is a staleness-vs-speed tradeoff with explicit policy.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Implement ETag + If-None-Match conditional requests.
2. Choose Cache-Control policies by data class.
3. Implement cache-aside with TTL on the server.
4. Design cache keys that encode the full request identity.
5. Distinguish per-user from shared caching safely.
6. Explain invalidation options and their tradeoffs.
7. Recognize cache-poisoning failure modes.
8. Decide what should never be cached.

## Prerequisites

| Need | Where |
|---|---|
| Response customization | `06-response-model.py`, `17-static-files.py` |
| Headers | `04-query-parameters.py` |
| Redis | `04-databases/redis/03-caching-patterns.py` |

## 1. ETag + If-None-Match — Conditional Requests

```python
etag = hashlib.sha1(payload.encode()).hexdigest()[:16]

@app.get("/catalog")
def catalog(request: Request):
    if request.headers.get("If-None-Match") == etag:
        return Response(status_code=304)
    return Response(content=json.dumps(body), media_type="application/json",
                    headers={"ETag": etag, "Cache-Control": "private, max-age=60"})
```

Output:
```
# First request  -> 200 + ETag: abc123
# Second request (same ETag) -> 304 Not Modified, empty body
```

The ETag is a content fingerprint. Clients and CDNs send it back as
`If-None-Match`; a match means "nothing changed" and the server returns 304 —
no body, huge bandwidth savings.

## 2. Cache-Control — The Policy Table

```python
CACHE_POLICIES = {
    "public": "shared cache: CDN/proxies may store",
    "private": "only the browser may store",
    "no-store": "never store (auth, personal data)",
    "no-cache": "must revalidate before reuse",
    "max-age=60": "fresh for 60s without asking",
}
```

Output:
```
# Cache-Control: public, max-age=300   -> CDN caches for 5 minutes
# Cache-Control: private               -> only the user's browser
# Cache-Control: no-store              -> nothing caches it
```

Choose per data class: public catalog content caches at the CDN; user
dashboards are `private`; tokens and personal data are `no-store`.

## 3. Cache-Aside — The Server-Side Pattern

```python
def search(q: str):
    key = f"search:{q.strip().lower()}"
    cached = cache.get(key)
    if cached is not None:
        return {"source": "cache", **cached}
    result = expensive_compute(q)
    cache.set(key, result)              # TTL-bounded
    return {"source": "compute", **result}
```

Output:
```
# first call  -> {"source": "compute"}
# repeat call -> {"source": "cache"}
```

Cache-aside: check the cache, compute on miss, store with a TTL. It is the
workhorse server-side pattern — simple, correct, and easy to bolt on. The
`source` field is a debugging gift: it tells you which path served the
response.

## 4. Cache-Key Design — Encode the Full Identity

```python
key = f"search:{q.strip().lower()}"        # normalized: "GPU" and "gpu" share
key = f"dashboard:user:{user_id}"          # user-scoped: users never collide
```

Output:
```
# search:gpu vs search:cpu -> separate entries
# dashboard:user:1 vs dashboard:user:2 -> never mixed
```

A cache key must encode everything that changes the response: query, filters,
pagination, user, tenant, version. Forgetting one dimension is a
cache-poisoning bug — user A's data served to user B.

## 5. Per-User vs Shared — The Boundary That Must Not Cross

```python
@app.get("/dashboard/{user_id}")
def dashboard(user_id: int, response: Response):
    response.headers["Cache-Control"] = "private, max-age=5"
    return user_scoped.get_dashboard(user_id)
```

Output:
```
# each user keyed separately AND marked private
```

Private data is cached per user or not at all. The two-layer defense: a
user-scoped key *and* `Cache-Control: private` so shared caches never store it.

## 6. Invalidation — The Hard Part

Options, in rough order of preference:

- **TTL**: accept bounded staleness; simplest and most common.
- **Write-through invalidation**: on update, delete the key (or update it).
- **Versioned keys**: bump a version segment in the key on release — the whole
  cache rotates atomically.
- **Event-based**: invalidate via pub/sub when data changes.

The rule: if you cannot tolerate stale data, you must invalidate on write —
TTL alone is not enough.

## 7. Common Mistakes to Avoid

### Mistake 1: Caching per-user data as shared
```python
# WRONG — one "dashboard" key serving every user
# CORRECT — user-scoped keys + Cache-Control: private
```

### Mistake 2: Cache keys missing request dimensions
```python
# WRONG — key = "search" with no query; all queries share one entry
# CORRECT — key encodes query, filters, pagination, version
```

### Mistake 3: No TTL, no invalidation
```python
# WRONG — stale forever once cached
# CORRECT — TTL or write-through invalidation
```

### Mistake 4: Caching auth-sensitive data
```python
# WRONG — tokens/balances with public caching
# CORRECT — no-store for anything sensitive
```

### Mistake 5: Caching without measuring hits
```python
# WRONG — a cache with a 2% hit rate adds latency
# CORRECT — track hit rate; cache only what repeats
```

## 8. Best Practices

1. Layer caches: HTTP-level (ETag/CDN) then server-side (Redis/memory).
2. Pick Cache-Control per data class — public/private/no-store.
3. Encode the full request identity in every key.
4. Set TTLs explicitly; never cache forever.
5. Invalidate on write when staleness is unacceptable.
6. Mark private data private; user-scope the keys.
7. Add a `source` field (cache/compute) for debuggability.
8. Track hit rates; remove caches that don't hit.
9. Version the cache (bump key prefix) on deploys.
10. Never cache side-effect responses (POSTs).

## 9. Complexity and Cost

| Strategy | Hit latency | Staleness | Cost |
|---|---|---|---|
| ETag/304 | Bandwidth saved | none (revalidates) | O(1) hash |
| Cache-Control | CDN-level | policy-bound | headers only |
| Cache-aside + TTL | O(1) read | TTL-bound | memory/Redis |
| Write-through | O(1) + write cost | none | invalidation on writes |

Caching trades a little memory for a lot of latency — and a little staleness
for a lot of throughput.

## 10. AI Engineering Relevance

**Where this shows up:** LLM systems are caching's biggest modern consumer —
prompt caching, embedding caches, and completion caches cut provider costs by
orders of magnitude (`09-genai/18-caching-and-cost`).

| Concept here | Used for |
|---|---|
| Cache-aside | Caching embeddings and retrieval results |
| Cache keys | Keying by model+prompt-hash for semantic cache |
| TTL | Bounding staleness of indexed documents |
| Per-user vs shared | Tenant-isolated retrieval caches |
| ETag/304 | Cheap revalidation of model metadata |

**Scale note:** in LLM serving, the cache hit is not a latency win — it is a
*bill* win: a cached completion costs near zero tokens. The cache-key design
from this topic decides whether that win materializes.

## 11. Summary

| Concept | Description |
|---|---|
| ETag/If-None-Match | Conditional requests save bandwidth |
| Cache-Control | Policy per data class |
| Cache-aside | Check -> compute -> store with TTL |
| Cache keys | Encode the full request identity |
| Per-user vs shared | Never cross the privacy boundary |
| Invalidation | TTL, write-through, versioned keys |

## 12. Quick Reference

| Task | Idiom |
|---|---|
| Fingerprint content | `ETag: hashlib.sha1(...)` + If-None-Match |
| Shared cache | `Cache-Control: public, max-age=300` |
| Private cache | `Cache-Control: private` |
| Never cache | `Cache-Control: no-store` |
| Cache-aside | `if key in cache: return; compute; cache.set(key, v)` |
| Rotate on deploy | bump a version in every key |

## Next Steps

Next: **[35 — Background Jobs](35-background-jobs-lecture.md)** — work that happens after the response.

Continues in: **[09-genai — 18 Caching and Cost](../../09-genai/lectures/18-caching-and-cost-lecture.md)** — caching applied to LLM bills.

Official docs: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching>
