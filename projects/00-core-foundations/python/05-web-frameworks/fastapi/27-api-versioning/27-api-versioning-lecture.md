# FastAPI — 27: API Versioning

Companion exercise: `27-api-versioning.py`

---

## Topic Overview

APIs evolve. Clients are deployed on schedules you do not control, and a
breaking change to a public contract breaks every caller at once. Versioning is
the discipline of evolving a contract *without* breaking the clients that
depend on it. This topic covers the three main strategies — URL path, header,
and media-type versioning — and the decision rules that choose between them:
what counts as an additive change (safe to ship in place), what counts as
breaking (requires a new version), and how to communicate deprecation so
clients migrate on your timeline, not in an emergency.

The core principle: **versioning is a communication problem, not a routing
problem.** The mechanism (prefix, header) is trivial; the contract discipline —
knowing what breaks, signaling deprecation, supporting two versions long enough
for migration — is the actual engineering.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Distinguish additive changes from breaking changes.
2. Implement URL path versioning with multiple routers.
3. Implement header-based versioning.
4. Communicate deprecation with Sunset and Deprecation headers.
5. Support two API versions in one application.
6. Choose a versioning strategy by client type and control.
7. State when a breaking change is justified.
8. Apply additive-change rules to your own API design.

## Prerequisites

| Need | Where |
|---|---|
| APIRouter / modular routes | `24-api-router.py` |
| Response models | `06-response-model.py` |
| Headers | `04-query-parameters.py` |
| Error handling | `23-exception-handling.py` |

## 1. Additive vs Breaking — The Decision Table

Before any change, classify it. Additive changes ship in the current version;
breaking changes need a new version.

| Additive (safe) | Breaking (needs v2) |
|---|---|
| New optional field | Removed field |
| New endpoint | Renamed field |
| New enum value | Changed type |
| Relaxed constraint | Stricter validation |
| Longer timeout | Changed status codes |
| New error detail | Auth model change |

```python
def is_additive(old: dict, new: dict) -> bool:
    """Every old key still present with a compatible value."""
    for key, value in old.items():
        if key not in new:
            return False
        if type(value) is not type(new[key]):
            return False
    return True
```

Output:
```
# is_additive({"a": 1}, {"a": 1, "b": 2}) -> True   (new key)
# is_additive({"a": 1}, {"a": "1"})       -> False  (type change)
# is_additive({"a": 1}, {"b": 1})         -> False  (renamed key)
```

The rule of thumb: **if an old client, unchanged, still works correctly, it is
additive.** Otherwise you need a version.

## 2. URL Path Versioning — Explicit and Cacheable

```python
v1 = APIRouter(prefix="/api/v1")
v2 = APIRouter(prefix="/api/v2")

@v1.get("/users/{user_id}")
def get_user_v1(user_id: int) -> UserV1: ...

@v2.get("/users/{user_id}")
def get_user_v2(user_id: int) -> UserV2: ...   # adds email

app.include_router(v1)
app.include_router(v2)
```

Output:
```
# GET /api/v1/users/1 -> {"id": 1, "name": "ada"}
# GET /api/v2/users/1 -> {"id": 1, "name": "ada", "email": "ada@example.com"}
```

Pros: explicit, bookmarked, cached per-version, no client config needed.
Cons: URL churn, version "leaks" into every link, duplicate code across
versions. This is the most common strategy in production.

## 3. Header Versioning — Stable URL, Negotiated Version

```python
@app.get("/api/items")
def get_items(api_version: str = Header(default="1", alias="X-API-Version")):
    if api_version not in SUPPORTED_VERSIONS:
        raise HTTPException(status_code=400, detail="Unsupported version")
```

Output:
```
# GET /api/items with X-API-Version: 2 -> {"items": [{"id": 1, "active": true}]}
```

Pros: URLs stay stable, clean link sharing. Cons: clients must set the header
correctly; caches and proxies need to key on it; browser testing is
inconvenient. Best for internal/API-first clients where you control the SDK.

## 4. Media-Type Versioning — The REST-Pure Approach

`Accept: application/vnd.myapi.v2+json` puts the version in the negotiated
content type. REST-purest, most explicit, but the least used in practice
because it requires content negotiation machinery on both sides and confuses
generic tooling.

## 5. Communicating Deprecation — Sunset and Deprecation Headers

The mechanism for telling clients *now* what dies *later*:

```python
SUNSET_DATE = "Sun, 31 Dec 2026 23:59:59 GMT"

@app.get("/api/items", headers={"Deprecation": "true", "Sunset": SUNSET_DATE})
def get_items_v1(): ...
```

Output:
```
# Response headers:
#   Deprecation: true
#   Sunset: Sun, 31 Dec 2026 23:59:59 GMT
```

- `Deprecation: true` — this version is deprecated.
- `Sunset: <HTTP-date>` — when support ends.
- `Link: <url>; rel="successor-version"` — where to go next.

Clients monitor these headers and migrate before the Sunset date. This is how
professional APIs deprecate gracefully — signaled, scheduled, not surprised.

## 6. Supporting Two Versions — The Transition Window

Run v1 and v2 side by side for a defined period (the plan says 6–12 months for
public APIs; shorter for internal). The transition window exists so clients can
migrate at their pace. During it:

- v1 gets bug fixes and security patches but no new features.
- The deprecation headers are present from day one of v2.
- Telemetry tracks v1 traffic; when it crosses zero, you can retire it.

## 7. Common Mistakes to Avoid

### Mistake 1: Versioning for additive changes
```python
# WRONG — a new optional field doesn't need /v2; ship it in v1
# CORRECT — additive changes stay in place; version only for breaks
```

### Mistake 2: Copy-pasting handlers between versions
```python
# WRONG — v1 and v2 handlers drift and the drift becomes a bug
# CORRECT — share a service layer; the routers differ only in schemas
```

### Mistake 3: Retiring v1 with no sunset signal
```python
# WRONG — v1 dies silently; clients break in production
# CORRECT — Deprecation + Sunset headers, telemetry, then retire
```

### Mistake 4: Forgetting cache keys in header versioning
```python
# WRONG — CDN caches /api/items once, serving v2 data to v1 callers
# CORRECT — include the version header in the cache key (Vary: X-API-Version)
```

### Mistake 5: Breaking changes disguised as "small fixes"
```python
# WRONG — "I just renamed the field, it's trivial"
# CORRECT — any renamed/removed/rettyped field is breaking: version it
```

## 8. Best Practices

1. Default to additive changes; treat breaking changes as rare events.
2. Put the version in the URL for public APIs; header for controlled clients.
3. Run a transition window with both versions and a retire date.
4. Send `Deprecation` and `Sunset` headers from day one of the new version.
5. Share business logic across versions; only schemas differ.
6. Track versioned traffic with telemetry before retiring v1.
7. Document what changed per version in the changelog.
8. Keep the version prefix stable once shipped — never rename it.
9. Additive changes never bump the version number.
10. Make the version a constant so routers and docs agree.

## 9. Complexity and Cost

| Strategy | Client effort | Cache/cdn | Code duplication |
|---|---|---|---|
| URL path | None | Per-path keys | Medium (routers) |
| Header | Must set header | Needs Vary key | Low |
| Media type | Must negotiate | Needs Accept key | Low |

The dominant cost of versioning is the **maintenance window** — supporting N
versions multiplies schema surface and test surface. Every version you ship is
a debt you carry; ship them only when breaking changes force it.

## 10. AI Engineering Relevance

**Where this shows up:** every model-serving API (feature vector contracts,
LLM structured outputs, prediction schemas) versioned for reproducibility —
a v1 embedding dimension change is a *breaking* change for every downstream
store.

| Concept here | Used for |
|---|---|
| Breaking-change rules | Versioning embedding models, prompts, and output schemas |
| Additive changes | Adding optional fields to LLM structured outputs safely |
| Sunset headers | Retiring a prompt/model version gracefully |
| Multi-version support | A/B model versions behind one API |
| Cache keys | Keeping retrieval caches version-correct |

**Scale note:** in ML/LLM systems, the "client" is often another service or a
stored embedding corpus. A version bump can require reindexing — making the
additive-vs-breaking discipline a *cost* decision, not just a correctness one.

## 11. Summary

| Concept | Description |
|---|---|
| Additive change | Old clients keep working; ship in place |
| Breaking change | Old clients break; requires a new version |
| URL path versioning | /api/v1, /api/v2 — explicit, cacheable |
| Header versioning | X-API-Version — stable URLs |
| Deprecation | Deprecation + Sunset headers signal migration |
| Transition window | Both versions live until traffic crosses zero |

## 12. Quick Reference

| Task | Idiom |
|---|---|
| Two path versions | `v1 = APIRouter(prefix="/api/v1")`, `v2 = ...` |
| Header version | `api_version: str = Header(alias="X-API-Version")` |
| Signal deprecation | `Deprecation: true` + `Sunset: <date>` |
| Classify a change | `is_additive(old, new)` — every old key still present |
| Reject unknown | `HTTPException(400, "Unsupported version")` |

## Next Steps

Next: **[28 — Pagination and Filtering](28-pagination-and-filtering-lecture.md)** — scaling list endpoints.

Continues in: **[05-system-design](../../05-web-frameworks/system-design/01-fundamentals.md)** — API design in the larger system.

Official docs: <https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design#versioning-a-restful-web-api> · <https://www.rfc-editor.org/rfc/rfc8594.html> (Sunset header)
