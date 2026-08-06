# FastAPI — 38: Authentication Deep Dive

## Topic Overview

Authentication answers "who are you?". This lecture covers the production
stack: **sessions vs tokens**, the **JWT structure** (what the signature
actually protects), the honest list of **what JWTs are bad at** (revocation
above all), **refresh-token rotation** as the standard mitigation,
**bcrypt/argon2** password hashing, and **timing-safe comparison**. AI
products multiply the surfaces: API keys for users, service tokens for
agents, and app JWTs — each with a different lifetime and revocation story.

The mental model: a JWT is a **readable, unforgeable claim** — anyone can
decode it, nobody but the issuer can alter it. That buys statelessness and
sells revocation. Production auth buys revocation back with short expiry +
denylists + rotating refresh tokens.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain sessions vs tokens and when each fits.
2. Decode a JWT into header, payload, signature and explain each part.
3. Explain exactly what the signature protects (integrity, not secrecy).
4. List what JWTs are bad at and why revocation needs state.
5. Design refresh-token rotation and detect token reuse.
6. Hash passwords with bcrypt and verify timing-safely.

## Prerequisites

| Need | Where |
|---|---|
| HTTP headers/status | `12-security.py`, `13-jwt-auth.py` |
| FastAPI dependencies | `09-dependency-injection.py` |
| HMAC basics | `06-data-structures-algorithms` (hash functions) |

---

## 1. Sessions vs tokens

| Aspect | Session (server-side) | Token (JWT) |
|---|---|---|
| State | server memory/Redis | stateless in the token |
| Revocation | instant (delete session) | only at expiry (or denylist) |
| Scale | shared session store | horizontally stateless |
| Leak risk | session id only | full claims readable |

Sessions win when you need instant logout and small scale; tokens win for
distributed services and third-party integration. Most products end up with
tokens + the state they tried to avoid (denylist, refresh store).

## 2. JWT structure

```text
base64url(header).base64url(payload).base64url(signature)

header:  {"alg": "HS256", "typ": "JWT"}
payload: {"sub": "user-1", "role": "admin", "exp": ..., "iat": ...}
signature: HMAC-SHA256(secret, "header.payload")
```

The payload is **base64, not encrypted** — never put secrets in a JWT. The
signature proves the header+payload were not modified since the issuer
signed them. Tamper with the payload and the signature check fails.

## 3. What JWTs are bad at

1. **Revocation** — a valid token works until `exp`. Logout is theatre
   without a denylist.
2. **Long life** — every minute of lifetime is a minute a stolen token works.
3. **Secrecy** — the payload is readable by anyone with the token.
4. **Algorithm confusion** — `alg: none` or RS256→HS256 downgrade attacks if
   the verifier trusts the header.

The response is not "don't use JWTs"; it is **short access tokens +
rotating refresh tokens + a denylist kill switch**.

## 4. Refresh rotation

The refresh token is long-lived but travels only to one endpoint, which
exchanges it for a fresh pair and **invalidates the old one**. A stolen
refresh token then dies at first use — reuse detection triggers a family
revocation. Access tokens stay short (5–15 min) so their blast radius is
bounded.

## 5. Passwords: bcrypt and timing-safe compare

- Never store plaintext or fast hashes (sha256 is brute-forceable).
- bcrypt/argon2 are deliberately slow and salted per password.
- Compare with `bcrypt.checkpw` or `hmac.compare_digest` — `==` on strings
  leaks timing information.

## Common Mistakes to Avoid

### Mistake 1: 30-day access tokens
```python
# WRONG - stolen token valid for a month
# CORRECT - 5-15 min access + rotating refresh
```

### Mistake 2: `==` on hashes/secrets
```python
# WRONG - if stored_hash == input_hash:  (timing leak)
# CORRECT - hmac.compare_digest / bcrypt.checkpw
```

### Mistake 3: Fast password hashes
```python
# WRONG - hashlib.sha256(password)  (trivially brute-forced)
# CORRECT - bcrypt.gensalt() + bcrypt.hashpw
```

### Mistake 4: Secrets in the JWT payload
```python
# WRONG - payload is base64, readable by anyone
# CORRECT - only identity/claims; secrets live server-side
```

### Mistake 5: Trusting the alg header
```python
# WRONG - verifier accepts whatever alg the token declares
# CORRECT - pin the algorithm at verify time; validate iss/aud
```

## Best Practices

1. Short access tokens; rotating refresh tokens.
2. Denylist (jti-based) for logout/suspension kill switch.
3. bcrypt/argon2 with a real work factor; timing-safe compare everywhere.
4. Pin `alg`; validate `iss`, `aud`, `exp` on every verify.
5. Rotate refresh tokens; treat reuse as theft.
6. Never put secrets in the payload.
7. Same-site/httpOnly cookies for browser delivery where possible.

## Complexity and Cost

| Concern | Cost | Cheaper alternative |
|---|---|---|
| bcrypt verify | ~100ms (deliberate) | lower rounds in dev |
| JWT sign/verify | <1ms | — |
| Denylist lookup | O(1) | — |
| Refresh rotation | 1 extra round trip per token life | — |

The expensive part of auth is never compute — it is the state you must keep
(denylist, refresh store) to make tokens safe.

## AI Engineering Relevance

**Where this shows up:** API-key auth for LLM gateways, service tokens for
agents, user sessions on chat products, and per-tenant credentials for
customer LLM integrations.

| Concept here | Used for |
|---|---|
| short access tokens | per-request auth on inference endpoints |
| refresh rotation | long-lived user sessions on chat products |
| denylist | instant kill of a leaked service token |
| bcrypt | hashing user passwords on the signup endpoint |
| timing-safe compare | API-key comparison in middleware |

**Scale note:** at 1M tokens, per-request verify must be <1ms — JWT wins.
At 1M users, refresh-rotation state lives in Redis with TTLs, not in the
database.

## Practice Exercises

### Exercise 1: Decode a JWT  (Difficulty: Easy)
Split a token and decode header/payload. Confirm the payload is readable
without the secret.

### Exercise 2: Forge attempt  (Difficulty: Easy)
Change the role claim without re-signing; assert verification fails.

### Exercise 3: Expiry  (Difficulty: Medium)
Sign with a negative TTL; assert the verifier rejects it.

### Exercise 4: Rotation  (Difficulty: Medium)
Rotate a refresh token; assert the old one is dead and reuse raises.

### Exercise 5: Reuse detection  (Difficulty: Hard)
Replay the same refresh token twice; assert the second use raises and the
token family is revoked.

### Exercise 6: Password lifecycle  (Difficulty: Hard)
Hash, verify, and demonstrate two hashes of the same password differ
(salting). Assert wrong passwords fail.

## Summary

| Concept | Description |
|---|---|
| JWT | readable, unforgeable claims (header.payload.signature) |
| Revocation | the state JWT statelessness gives away |
| Refresh rotation | old token dies at first use |
| bcrypt | slow, salted password hashing |
| timing-safe compare | hmac.compare_digest, never == |
| denylist | jti-based kill switch |

Auth is a tradeoff between statelessness and revocation. The production
answer is short access + rotating refresh + denylist — bounded blast radius
with a kill switch.

## Quick Reference

| Task | Idiom |
|---|---|
| Hash a password | `bcrypt.hashpw(pw, bcrypt.gensalt(12))` |
| Verify | `bcrypt.checkpw(pw, hashed)` |
| Sign JWT | `jwt.encode({"sub": u}, SECRET, algorithm="HS256")` |
| Verify | `jwt.decode(tok, SECRET, algorithms=["HS256"])` |
| Timing-safe | `hmac.compare_digest(a, b)` |
| Rotate refresh | verify → denylist old jti → issue new pair |

## Next Steps

Next: **[39 — OAuth2 & OIDC](39-oauth2-oidc-lecture.md)** — delegating auth to
providers with authorization codes and PKCE.

Continues in: **[40 — Authorization](40-authorization-lecture.md)** — what the
user is allowed to do after we know who they are.

Official docs:
- PyJWT: https://pyjwt.readthedocs.io/
- bcrypt: https://github.com/pyca/bcrypt
- OWASP auth cheat sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
