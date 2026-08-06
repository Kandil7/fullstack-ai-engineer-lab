# Caching Strategies — Glossary 34

Companion lecture: `34-caching-strategies-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| 304 Not Modified | HTTP | Response with no body when the ETag matches |
| Cache-aside | Pattern | Check cache, compute on miss, store with TTL |
| Cache key | Design | The string identifying a cached response |
| Cache poisoning | Failure | Serving wrong data due to bad keys or sharing |
| Cache-Control | Header | Policy: public, private, no-store, max-age |
| ETag | HTTP | Content fingerprint for conditional requests |
| Hit rate | Monitoring | The fraction of requests served from cache |
| If-None-Match | HTTP | Header sending the client's ETag for validation |
| Invalidation | Design | Removing/rotating stale entries on writes |
| max-age | Header | Freshness window in seconds |
| no-store | Header | Never store (sensitive data) |
| private | Header | Only the client's browser may store |
| public | Header | Shared caches (CDNs) may store |
| Semantic cache | AI | Caching by meaning (embedding similarity) |
| Staleness | Design | The age gap between cache and source |
| TTL | Design | Time-to-live bounding cache entries |
| Versioned keys | Design | Bumping a key segment to rotate the cache |
| Write-through | Design | Updating/deleting the cache on every write |

## Detailed Definitions

### 304 Not Modified
**Definition**: The status returned when a client's If-None-Match ETag
matches — no body, saving bandwidth.
**Related**: ETag

### Cache-aside
**Definition**: The server-side pattern: check the cache, compute on a miss,
store with a TTL.
**Example**:
```python
cached = cache.get(key)
if cached is None:
    cached = expensive_compute(q)
    cache.set(key, cached)
```
**Related**: TTL, Cache key

### Cache key
**Definition**: The string identifying a cached response; must encode every
dimension that changes the response (query, user, version).
**Example**:
```python
f"search:{q.strip().lower()}"
```
**Related**: Cache poisoning

### Cache poisoning
**Definition**: Serving the wrong cached data — user A's response to user B,
or a stale response for a different query — caused by bad keys or shared
caches for private data.
**Related**: Cache key

### Cache-Control
**Definition**: The response header declaring caching policy: `public`,
`private`, `no-store`, `max-age`.
**Related**: public, private, no-store

### ETag
**Definition**: A content fingerprint (usually a hash) attached to a response
so clients can validate freshness.
**Example**:
```python
etag = hashlib.sha1(payload.encode()).hexdigest()[:16]
```
**Related**: If-None-Match

### Hit rate
**Definition**: The fraction of requests served from cache; a cache with a low
hit rate adds latency without paying off — measure before keeping it.
**Related**: Cache-aside

### If-None-Match
**Definition**: The request header carrying the client's stored ETag; a match
yields 304.
**Related**: ETag

### Invalidation
**Definition**: The act of removing or rotating stale cache entries on data
changes — required when TTL staleness is unacceptable.
**Related**: Write-through, Versioned keys

### max-age
**Definition**: The Cache-Control freshness window in seconds; the entry is
served without revalidation within it.
**Related**: TTL

### no-store
**Definition**: Cache-Control policy meaning nothing may store the response —
for tokens, personal data, anything sensitive.
**Related**: Cache-Control

### private
**Definition**: Cache-Control policy meaning only the client's browser may
store the response; shared caches must not.
**Related**: Cache-Control

### public
**Definition**: Cache-Control policy allowing shared caches (CDNs, proxies)
to store the response.
**Related**: Cache-Control

### Semantic cache
**Definition**: Caching keyed by embedding similarity rather than exact
string — used to deduplicate near-identical LLM queries.
**Related**: Cache-aside

### Staleness
**Definition**: The age gap between a cached copy and its source; every cache
policy is a staleness-vs-speed tradeoff.
**Related**: TTL

### TTL
**Definition**: Time-to-live — how long a cache entry is considered fresh
before expiry. The simplest staleness bound.
**Related**: Staleness

### Versioned keys
**Definition**: Bumping a version segment in cache keys on deploy, rotating
the whole cache atomically without per-key invalidation.
**Related**: Invalidation

### Write-through
**Definition**: Updating or deleting the cache entry at the same time as the
underlying write — no stale reads for critical data.
**Related**: Invalidation

## Key Concepts Summary

### The layered stack
- HTTP layer: ETag/If-None-Match + Cache-Control for CDNs and browsers.
- Server layer: cache-aside with TTLs in memory or Redis.
- Policy per data class: public, private, no-store.

### The design rules
- Keys encode the full request identity.
- Private data: user-scoped keys AND Cache-Control: private.
- Staleness unacceptable? Invalidate on write or version the keys.

### The discipline
- Track hit rates; drop caches that don't hit.
- Never cache side-effect responses or sensitive data.
- Measure before and after — a cache is an optimization, not a default.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Content fingerprint for conditional requests — ___
2. Check, compute, store with TTL — ___
3. Serving wrong data from a bad cache key — ___
4. Only the client's browser may store — ___
5. The fraction of requests served from cache — ___
6. Bumping a key segment to rotate the cache — ___
7. Never store anything — ___
8. The age gap between cache and source — ___

**Answers:** 1-ETag, 2-cache-aside, 3-cache poisoning, 4-private, 5-hit rate,
6-versioned keys, 7-no-store, 8-staleness
