# FastAPI — 41: API Security

## Topic Overview

API security is a **layered checklist**, not a single feature. For AI
products the stakes are unusual: an unlimited `/generate` endpoint is a
billing bomb, and an agent that fetches URLs is an SSRF cannon if the
host is not guarded. The layers this lecture covers: **rate limiting per
identity**, **CORS done right** (an explicit allowlist, never `*`),
**CSRF tokens** for cookie auth, **security headers**, **request-size
caps**, **input validation**, **SSRF guards**, and **secrets handling**.
Each layer is cheap; each missed layer is a known incident class.

The mental model: assume every request is hostile and every input is
untrusted. The layers are the distance between "works" and "survives".

## Learning Objectives

By the end of this lecture, you will be able to:

1. Rate-limit per identity with a token bucket.
2. Configure CORS with an explicit allowlist, never `*`.
3. Explain CSRF and add per-session token checks for cookie auth.
4. Apply security headers and request-size caps.
5. Guard URL-fetching features against SSRF.
6. Keep secrets in env/secret managers and fail fast.

## Prerequisites

| Need | Where |
|---|---|
| Middleware | `10-middleware.py` |
| Authn/authz | `38-auth-deep`, `40-authorization` lectures |
| Exceptions | `29-error-handling-rfc9457-lecture.md` |

---

## 1. Rate limiting per identity

The token bucket: capacity `C`, refill rate `r`. Every identity (user, API
key, IP) has its own bucket. Per-identity is non-negotiable — a global
limit lets one tenant starve everyone and cannot attribute abuse. Redis
holds the buckets in production; the logic is identical. LLM endpoints
need this more than any other API: one unauthenticated burst is a real
invoice.

## 2. CORS — the allowlist, not `*`

CORS is a *browser* mechanism. `Access-Control-Allow-Origin: *` tells
every website on the internet that its JavaScript may call your API — and
with `credentials` the browser forbids `*` anyway, so `*` is both unsafe
and broken for credentialed flows. The correct shape is an explicit
allowlist of origins you control, returned verbatim. Denied origins get no
CORS header at all.

## 3. Security headers + CSRF

Headers are one line each and kill whole vulnerability classes:

```python
SECURITY_HEADERS = {
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Content-Security-Policy": "default-src 'none'",
}
```

CSRF: when auth rides on cookies, a hostile site can trigger
state-changing requests that arrive *with* the victim's cookie. The fix is
a per-session, unpredictable token that the legit form/header must echo —
checked with a timing-safe compare. Token-in-header auth (Bearer) is
immune by construction; cookie auth is not.

## 4. Request-size caps and input validation

Cap the body at the boundary (middleware + proxy) — a 10 MB "prompt" is a
DoS and, in LLM products, a budget weapon. Validate every input with typed
schemas: length caps, enums, ranges. The 422 that FastAPI returns for a
bad schema is the security boundary doing its job.

## 5. SSRF

Server-Side Request Forgery: the attacker points your URL-fetching feature
(an agent tool, an import-from-URL endpoint) at `http://169.254.169.254`
(cloud metadata), `http://localhost`, or literal internal IPs. Guards:
pin schemes to http/https, reject private/link-local/metadata hosts, and
re-resolve DNS at fetch time (attacker-controlled DNS can swap after the
check). The check lives right next to the fetch, not at config load.

## 6. Secrets

Secrets come from environment variables or a secret manager — never source
control, never committed config. Fail fast at startup when a required
secret is missing; a service that boots without its signing key is a
misconfiguration waiting to become an incident.

## Common Mistakes to Avoid

### Mistake 1: CORS `*` on a credentialed API
```python
# WRONG - allow_origins=["*"] with cookies -> browsers refuse, or worse
# CORRECT - explicit allowlist; no * with credentials
```

### Mistake 2: Global rate limit
```python
# WRONG - one shared counter; a burst starves every tenant
# CORRECT - per-identity token buckets
```

### Mistake 3: No size cap on LLM inputs
```python
# WRONG - unlimited prompt length -> DoS + billing bomb
# CORRECT - cap at the boundary; validate schemas
```

### Mistake 4: Unchecked URL fetching
```python
# WRONG - agent tool fetches whatever URL the user names
# CORRECT - scheme pin + private-host denylist + DNS re-check
```

### Mistake 5: Secrets in code
```python
# WRONG - SECRET = "..." in the source file
# CORRECT - env/secret manager; fail fast if missing
```

## Best Practices

1. Rate limit per identity with token buckets (Redis in prod).
2. CORS allowlist; reflect only allowed origins.
3. Apply the full security-header set via middleware.
4. CSRF tokens for any cookie-authenticated mutation.
5. Size caps at the boundary; validate all inputs as schemas.
6. SSRF guard on every URL-fetching path.
7. Secrets from env/manager; fail fast at startup.

## Complexity and Cost

| Concern | Cost | Cheaper alternative |
|---|---|---|
| Token bucket check | O(1) per request | — |
| CORS/headers | O(1) per response | — |
| CSRF check | O(1) | — |
| SSRF check | O(1) + DNS | cache DNS results |
| Size caps | O(1) length check | — |

Every layer is constant-time and nearly free. Security here is cheap
prevention; the alternative is an incident that is not cheap at all.

## AI Engineering Relevance

**Where this shows up:** LLM gateways, agent tool execution, model-serving
endpoints, and any feature that takes a URL or a prompt from a user.

| Concept here | Used for |
|---|---|
| per-identity rate limits | stopping billing bombs on /generate |
| SSRF guards | agent fetch tools reaching internal services |
| size caps | bounding prompt/tool-input cost |
| input validation | rejecting hostile prompt payloads at the edge |
| secrets | provider API keys from the secret manager |

**Scale note:** at 100k requests/day the token buckets live in Redis with
TTLs; the SSRF denylist is a compiled set; the checks stay O(1) per
request.

## Practice Exercises

### Exercise 1: Token bucket  (Difficulty: Easy)
Capacity 3, refill 1/s; burst then block, then allow after refill. Assert.

### Exercise 2: CORS allowlist  (Difficulty: Easy)
Allowed origin reflects; unknown origin gets nothing. Assert both.

### Exercise 3: CSRF check  (Difficulty: Medium)
Session token vs form token; timing-safe; wrong token fails. Assert.

### Exercise 4: SSRF guard  (Difficulty: Medium)
Public URLs pass; metadata/localhost/file/ftp fail. Assert the set.

### Exercise 5: Layered endpoint  (Difficulty: Hard)
Compose rate limit + size cap + validation + headers for a /generate
endpoint; assert each layer blocks its attack class.

### Exercise 6: Secrets lifecycle  (Difficulty: Hard)
Write a config loader that reads env, validates presence, and fails fast;
assert a missing secret raises before the app starts.

## Summary

| Concept | Description |
|---|---|
| rate limiting | per-identity token buckets |
| CORS | explicit allowlist, never * |
| CSRF | per-session tokens for cookie auth |
| headers | one-line mitigations |
| size caps | bounding cost and DoS surface |
| SSRF | guarding URL-fetching paths |
| secrets | env/manager only, fail fast |

API security is a checklist you can verify — each layer is O(1) and each
missing layer is a known incident class. Layers, not hope.

## Quick Reference

| Task | Idiom |
|---|---|
| Rate limit | `limiter.allow(identity)` (token bucket) |
| CORS | `cors_allow(origin)` → allowed origin or None |
| Headers | one dict applied in middleware |
| CSRF | `secrets.compare_digest(session_tok, form_tok)` |
| Size cap | reject `len(raw) > MAX_BODY_BYTES` |
| SSRF | scheme pin + private-host denylist |
| Secrets | `os.environ` + fail-fast at startup |

## Next Steps

Next: **[42 — Security Testing](42-security-testing-lecture.md)** — proving
the boundaries hold with bypass tests and fuzzing.

Continues in: **[43 — Structured Logging](43-structured-logging-lecture.md)** —
seeing the attacks that get through.

Official docs:
- OWASP Top Ten: https://owasp.org/www-project-top-ten/
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
