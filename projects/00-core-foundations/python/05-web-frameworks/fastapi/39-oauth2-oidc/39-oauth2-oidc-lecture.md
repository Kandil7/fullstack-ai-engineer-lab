# FastAPI — 39: OAuth2 & OIDC

## Topic Overview

OAuth2 is the delegation protocol: your app asks a provider (Google,
GitHub, an IdP) to authenticate a user and issue tokens **scoped** to what
your app needs. OIDC is OAuth2 plus a standardized identity layer — the
`id_token`, claims, and discovery. The two flows that matter in practice
are the **Authorization Code + PKCE** flow (the public-client default,
immune to the code-interception attack that the implicit flow died from)
and the machine flow (**client credentials**).

The mental model: OAuth2 separates **who** (authentication, OIDC's job)
from **what they can do** (authorization, carried in scopes). The provider
is a trusted third party that vouches for both, backed by **JWKS** — the
published public keys your service uses to verify tokens it never issued.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain Authorization Code + PKCE and why PKCE exists.
2. Distinguish scopes (authorization) from claims (identity).
3. Tell ID tokens from access tokens.
4. Verify a provider's JWT using its JWKS public keys.
5. Explain key rotation and why JWKS is fetched, not hardcoded.

## Prerequisites

| Need | Where |
|---|---|
| JWT internals | `38-auth-deep-lecture.md` |
| RSA/ASymmetric crypto | `02-advanced-python` cryptography lectures |
| HTTP redirects | `12-security.py` |

---

## 1. The Authorization Code + PKCE flow

```text
App -> Provider : /authorize?client_id&scope&redirect_uri&code_challenge
Provider -> User : login + consent
Provider -> App  : 302 to redirect_uri?code=...
App -> Provider : POST /token?code&code_verifier&client_id
Provider -> App  : access_token, id_token, refresh_token
```

**PKCE** (RFC 7636): the app sends a `code_challenge` (SHA-256 of a random
`code_verifier`) at authorize time and presents the verifier at token time.
A hijacked authorization code is useless without the verifier — the fix for
the old "implicit flow" code-interception hole. Public clients (SPAs,
mobile) must use PKCE.

## 2. Scopes vs claims

- **Scopes** — authorization: what the app may do (`read:metrics`,
  `write:logs`). The provider's consent screen shows scopes.
- **Claims** — identity/attributes: `sub`, `email`, `name`, `roles` in the
  id_token/UserInfo.

Scopes are coarse-grained, provider-decided capabilities; claims are
attributes about the subject. OIDC standardizes claims; OAuth2 standardizes
scopes' mechanics but not their meaning.

## 3. ID token vs access token

| | ID token | Access token |
|---|---|---|
| Audience | the app (aud=client_id) | the resource server |
| Purpose | proves who the user is | authorizes API calls |
| Format | always JWT (OIDC) | opaque or JWT |
| Validity | short, verified locally | verified by the resource API |

The ID token is a *proof of authentication* for the app to trust; the
access token is a *key to resources* the app presents to APIs. Never use
the ID token as an API credential.

## 4. JWKS and key rotation

Providers sign tokens with private keys and publish the matching public
keys at a discovery endpoint (`/.well-known/jwks.json`). Your service:

1. Fetches discovery → JWKS URL.
2. Reads `kid` from the token header.
3. Picks the matching public key from JWKS and verifies.

Because keys rotate, JWKS is fetched (and cached briefly), never hardcoded.
Verifying with a stale key after rotation fails — the cache TTL is the
rotation-latency dial.

## Common Mistakes to Avoid

### Mistake 1: Implicit flow with access token in the URL
```python
# WRONG - token in the redirect URL leaks via history/referrer
# CORRECT - Authorization Code + PKCE; tokens only in the token response
```

### Mistake 2: Trusting an access token without verifying it
```python
# WRONG - accept provider-looking tokens because they came from your frontend
# CORRECT - verify signature via JWKS + aud/iss/exp on the resource server
```

### Mistake 3: Confusing ID and access tokens
```python
# WRONG - sending the id_token as an API credential
# CORRECT - id_token for the app; access_token for resources
```

### Mistake 4: Hardcoding the public key
```python
# WRONG - keys rotate; hardcoded keys break at rotation and at incident
# CORRECT - fetch JWKS with a short cache TTL; honor kid
```

### Mistake 5: Ignoring scope checks
```python
# WRONG - "it has a valid signature, so it may call everything"
# CORRECT - verify required scopes on each protected route
```

## Best Practices

1. Authorization Code + PKCE for all public clients.
2. Client credentials flow for machine-to-machine.
3. Verify access tokens on the resource server (signature, aud, iss, exp).
4. Read `kid` and select the JWKS key — never hardcode.
5. Cache JWKS briefly; refresh on verification failure after rotation.
6. Enforce scopes per route, not just token validity.
7. Keep refresh tokens server-side where possible; rotate them.

## Complexity and Cost

| Concern | Cost | Cheaper alternative |
|---|---|---|
| PKCE exchange | 1 extra round trip | — (non-negotiable for public clients) |
| JWKS verify | RSA verify ~1ms | symmetric only for own-service tokens |
| JWKS cache | O(keys) memory | — |
| Scope enforcement | O(1) per route | — |

The expensive parts are the external calls (authorize, token) — one-time per
session, not per request.

## AI Engineering Relevance

**Where this shows up:** "Sign in with Google/GitHub" on AI products,
provider-hosted model APIs (e.g., LLM providers with OAuth), and
per-tenant identity in enterprise LLM gateways.

| Concept here | Used for |
|---|---|
| PKCE | SPA/mobile AI chat clients |
| scopes | asking for read-only model usage vs admin billing |
| id_token | identifying the user for personalization |
| JWKS | verifying provider-issued tokens for gateway access |

**Scale note:** at 100k users, do the OAuth dance once per session and
verify the resulting access token per request (~1ms). Never call the
provider per request.

## Practice Exercises

### Exercise 1: PKCE challenge  (Difficulty: Easy)
Generate a verifier and S256 challenge; assert determinism of the challenge
for a given verifier.

### Exercise 2: Simulated code exchange  (Difficulty: Medium)
Model authorize → redirect with code → token exchange with PKCE; assert the
exchange fails without the correct verifier.

### Exercise 3: Scope check  (Difficulty: Medium)
Given tokens with different scope sets, assert which routes they may call.

### Exercise 4: JWKS verify  (Difficulty: Hard)
Generate an RSA keypair, publish a JWKS, sign a token, and verify it with
the JWKS public key. Rotate the key and prove the old token fails.

### Exercise 5: End-to-end flow  (Difficulty: Hard)
Wire a mini provider (authorize + token) and a mini resource server that
verifies via JWKS; prove the full happy path and the stolen-code-without-
verifier failure.

## Summary

| Concept | Description |
|---|---|
| Auth Code + PKCE | the safe public-client flow |
| scopes | authorization — what the app may do |
| claims | identity — who the user is |
| id_token vs access_token | proof of login vs key to resources |
| JWKS | published public keys; honor kid, cache briefly |

OAuth2 delegates authentication; OIDC standardizes the identity claims; and
JWKS is how your service verifies tokens it never signed. The flow is
external, the verification is local — one dance per session, ~1ms per
request after.

## Quick Reference

| Task | Idiom |
|---|---|
| PKCE challenge | `b64url(sha256(verifier))` |
| Fetch discovery | `GET /.well-known/openid-configuration` |
| Verify via JWKS | decode token → kid → key → verify |
| Required scopes | check `scope` claim per route |
| Machine auth | client_credentials grant |

## Next Steps

Next: **[40 — Authorization](40-authorization-lecture.md)** — scopes are
coarse; per-resource permission checks are the real work.

Continues in: **[41 — API Security](41-api-security-lecture.md)** — rate
limits, CORS, headers, and the rest of the hardening checklist.

Official docs:
- RFC 6749 (OAuth2): https://datatracker.ietf.org/doc/html/rfc6749
- RFC 7636 (PKCE): https://datatracker.ietf.org/doc/html/rfc7636
- OpenID Connect: https://openid.net/connect/
