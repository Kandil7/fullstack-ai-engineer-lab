# API Versioning — Glossary 27

Companion lecture: `27-api-versioning-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Additive change | Contract | A change old clients still work with |
| Breaking change | Contract | A change that breaks unchanged old clients |
| Cache key | Operations | What a CDN/proxy uses to distinguish cached responses |
| Deprecation header | Communication | Signals a version is deprecated |
| Header versioning | Strategy | Version chosen via a request header |
| Media-type versioning | Strategy | Version negotiated via the Accept header |
| Retirement | Lifecycle | Removing a deprecated version after migration |
| Sunset header | Communication | The date a deprecated version stops being served |
| Transition window | Lifecycle | The period both versions run side by side |
| URL path versioning | Strategy | Version embedded in the URL prefix |
| Vary header | Operations | Tells caches to key on a request header |
| Version | Contract | A distinct, immutable API contract |
| Successor-version | Communication | Link header pointing clients to the new version |
| APIRouter | Implementation | FastAPI router allowing per-version prefixes |
| Contract drift | Failure | v1/v2 handlers diverging from their shared logic |

## Detailed Definitions

### Additive change
**Definition**: A contract change that does not break unchanged old clients —
new optional fields, new endpoints, new enum values, relaxed constraints.
**Example**:
```python
is_additive({"a": 1}, {"a": 1, "b": 2})   # True — new key only
```
**Related**: Breaking change

### Breaking change
**Definition**: A change that breaks unchanged old clients — removed or renamed
fields, type changes, stricter validation, changed status codes.
**Related**: Additive change, Version

### Cache key
**Definition**: The combination of request attributes a cache uses to
distinguish stored responses. Header-based versioning must include the version
header or caches serve the wrong version.
**Related**: Vary header, Header versioning

### Deprecation header
**Definition**: A response header (`Deprecation: true`) signaling that the
current version is deprecated and clients should migrate.
**Related**: Sunset header

### Header versioning
**Definition**: Choosing the API version via a request header such as
`X-API-Version`; URLs stay stable.
**Example**:
```python
api_version: str = Header(default="1", alias="X-API-Version")
```
**Related**: URL path versioning

### Media-type versioning
**Definition**: Negotiating the version through the `Accept` header content
type, e.g. `application/vnd.myapi.v2+json`. REST-purest, least used.
**Related**: Header versioning

### Retirement
**Definition**: Removing a deprecated version once migration is complete,
confirmed by telemetry showing zero (or near-zero) traffic.
**Related**: Transition window

### Sunset header
**Definition**: An `HTTP-date` response header (`Sunset: <date>`) stating when
a deprecated version will stop being served.
**Related**: Deprecation header

### Transition window
**Definition**: The defined period during which old and new versions run
side by side so clients can migrate at their own pace.
**Related**: Retirement

### URL path versioning
**Definition**: Embedding the version in the URL prefix (`/api/v1/...`,
`/api/v2/...`); explicit, cacheable, and the most common strategy.
**Related**: Header versioning

### Vary header
**Definition**: A response header (`Vary: X-API-Version`) telling caches that
the response depends on a request header, preventing cross-version cache
poisoning.
**Related**: Cache key

### Version
**Definition**: A distinct, immutable API contract. Once shipped, a version's
shape does not change; evolution happens in newer versions.
**Related**: Breaking change

### Successor-version
**Definition**: A `Link` response header (`Link: <url>; rel="successor-version"`)
pointing clients from a deprecated version to its replacement.
**Related**: Deprecation header

### APIRouter
**Definition**: FastAPI's modular router; each version gets its own router
with a distinct prefix, included in the same app.
**Example**:
```python
v2 = APIRouter(prefix="/api/v2")
app.include_router(v2)
```
**Related**: URL path versioning

### Contract drift
**Definition**: The divergence of per-version handlers from shared business
logic until the copies become subtly different — a maintenance hazard that
shared service layers prevent.
**Related**: APIRouter

## Key Concepts Summary

### The decision rule
- Additive changes (new optional fields, endpoints, enum values) ship in place.
- Breaking changes (removed/renamed fields, type changes) require a new version.
- An unchanged old client working correctly is the test of "additive".

### The three strategies
- URL path: explicit and cacheable; most common.
- Header: stable URLs; needs cache Vary discipline.
- Media type: REST-pure; least practical.

### Graceful deprecation
- Deprecation + Sunset headers from day one of the new version.
- Transition window, telemetry, then retirement.
- Version only when breaking changes force it — each version is carried debt.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. A change that breaks unchanged old clients — ___
2. The date a deprecated version stops being served — ___
3. Version embedded in the URL prefix — ___
4. The period both versions run side by side — ___
5. Tells caches to key on a request header — ___
6. Signals a version is deprecated — ___
7. Version chosen via a request header — ___
8. Link header pointing clients to the new version — ___

**Answers:** 1-breaking change, 2-sunset header, 3-URL path versioning,
4-transition window, 5-Vary header, 6-deprecation header, 7-header versioning,
8-successor-version
