# API Security — Glossary 41

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| CORS | Mechanism | Browser policy on cross-origin reads; allowlist, never * |
| CSRF | Attack | Hostile site firing requests with the victim's cookie |
| DoS | Attack | Resource exhaustion — an unlimited endpoint is one |
| Fail fast | Principle | Refuse to start when config/secrets are invalid |
| Identity | Concept | The rate-limit key: user, API key, or IP |
| Metadata service | Target | 169.254.169.254 — cloud credentials for SSRF |
| Security headers | Defense | HSTS, nosniff, frame/ref/CSP — one-line mitigations |
| SSRF | Attack | Server-Side Request Forgery via a URL-fetching feature |
| Token bucket | Mechanism | Capacity + refill rate; per-identity buckets |
| Size cap | Defense | Bounding request/prompt size at the boundary |
| Allowlist | Defense | The explicit set of permitted origins/hosts |
| Secrets | Defense | Env/secret manager; never source control |

## Detailed Definitions

### CORS
**Definition**: Cross-Origin Resource Sharing — a browser mechanism
controlling whether another origin's JavaScript may read responses. `*`
is unsafe with credentials; the correct shape is an explicit allowlist.
**Related**: Allowlist

### CSRF
**Definition**: Cross-Site Request Forgery — a hostile page triggers a
state-changing request that arrives with the victim's cookie. Fixed with
per-session tokens checked timing-safely (Bearer-header auth is immune).
**Related**: Token bucket

### DoS
**Definition**: Denial of service — an unlimited LLM endpoint is both a
DoS and a billing bomb; size caps and rate limits bound it.
**Related**: Size cap

### Fail fast
**Definition**: Validating configuration and secrets at startup so a
broken service never runs — a missing secret raises before the app binds.
**Related**: Secrets

### Identity
**Definition**: The per-actor key for rate limiting (user, API key, IP)
— limits must be per identity so one tenant cannot starve all.
**Related**: Token bucket

### Metadata service
**Definition**: `169.254.169.254` — the cloud provider's metadata
endpoint containing credentials; the classic SSRF target.
**Related**: SSRF

### Security headers
**Definition**: Response headers that disable whole vulnerability classes
— HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, CSP.
**Related**: Security headers

### SSRF
**Definition**: Server-Side Request Forgery — an attacker points a
URL-fetching feature (agent tool, import endpoint) at internal hosts or
the metadata service. Guard: scheme pin + private-host denylist + DNS
re-check.
**Related**: Metadata service

### Token bucket
**Definition**: Rate-limiting mechanism — each identity has a bucket of
capacity C refilled at rate r; a request consumes a token or is denied.
**Related**: Identity

### Size cap
**Definition**: Rejecting bodies/prompts above a limit at the boundary —
bounds cost, DoS surface, and abuse on LLM endpoints.
**Related**: DoS

### Allowlist
**Definition**: The explicit set of permitted origins (CORS) or hosts
(SSRF) — anything not listed is denied.
**Related**: CORS

### Secrets
**Definition**: API keys and signing secrets, sourced from environment
variables or a secret manager — never committed to source control; fail
fast when missing.
**Related**: Fail fast

## Key Concepts Summary

### The layered checklist
- Rate limits per identity (token buckets).
- CORS allowlist, never *.
- Security headers in one middleware dict.
- CSRF tokens for cookie auth.
- Size caps + typed input validation.
- SSRF guard on URL-fetching paths.
- Secrets from env/manager, fail fast.

### The cost note
- Every layer is O(1) per request.
- The alternative — one missed layer — is an incident class.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Browser policy on cross-origin reads — ___
2. Requests fired with the victim's cookie — ___
3. 169.254.169.254 — ___
4. Capacity + refill rate — ___
5. Bounding input size at the edge — ___
6. Never committed to source control — ___
7. The rate-limit key — ___
8. Refuse to start when invalid — ___

**Answers:** 1-CORS, 2-CSRF, 3-metadata service, 4-token bucket, 5-size cap,
6-secrets, 7-identity, 8-fail fast
