# Authentication Deep Dive — Glossary 38

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Access token | Token | Short-lived JWT sent with every request |
| bcrypt | Hashing | Slow, salted password hash with an adaptable work factor |
| Claims | JWT | The payload fields (sub, role, exp, iat, aud, iss) |
| Denylist | Revocation | A jti-indexed list making a token dead before expiry |
| Header | JWT | First part: alg + typ |
| JWT | Token | Signed JSON claims: header.payload.signature |
| Payload | JWT | Middle part: base64url claims — readable by anyone |
| Refresh token | Token | Long-lived token used only at one exchange endpoint |
| Revocation | Concept | Making a token invalid before its exp |
| Rotation | Technique | Each refresh exchange invalidates the previous refresh |
| Salt | Hashing | Per-password random value preventing identical hashes |
| Signature | JWT | HMAC over header.payload; proves integrity, not secrecy |
| Timing-safe compare | Defense | constant-work comparison (hmac.compare_digest) |
| Work factor | Hashing | bcrypt cost parameter slowing brute force |

## Detailed Definitions

### Access token
**Definition**: The short-lived token (5–15 min) sent with each request so
the blast radius of a stolen token is bounded.
**Related**: Refresh token

### bcrypt
**Definition**: A deliberately slow, salted password-hashing algorithm —
`bcrypt.hashpw(pw, bcrypt.gensalt(rounds))`; the slowness is the security.
**Related**: Work factor

### Claims
**Definition**: The payload fields asserting identity and permissions —
`sub` (subject), `role`, `exp` (expiry), `iat` (issued at), `aud`, `iss`.
**Related**: Payload

### Denylist
**Definition**: A set of revoked token jtis checked at verify time — the
state that gives JWTs a kill switch. Redis with TTLs in production.
**Related**: Revocation

### Header
**Definition**: The first JWT part declaring the algorithm and type —
`{"alg": "HS256", "typ": "JWT"}`. Never trust it blindly; pin the alg.
**Related**: Signature

### JWT
**Definition**: JSON Web Token — three base64url parts, of which only the
signature is protected. Readable by anyone, forgeable by nobody (with the
secret).
**Related**: Signature

### Payload
**Definition**: The middle JWT part holding claims as base64url JSON —
visible to anyone who decodes; never put secrets here.
**Related**: Claims

### Refresh token
**Definition**: The long-lived token that only talks to the exchange
endpoint — it rotates on use so theft dies at first replay.
**Related**: Rotation

### Revocation
**Definition**: Making a token useless before its `exp` — the property
stateless JWTs lack by default and the reason production adds denylists and
short expiries.
**Related**: Denylist

### Rotation
**Definition**: Each refresh-token exchange issues a fresh pair and revokes
the previous refresh jti; reuse of a dead token is treated as theft.
**Related**: Refresh token

### Salt
**Definition**: A per-password random value mixed into the hash so two users
with the same password get different hashes.
**Related**: bcrypt

### Signature
**Definition**: The third JWT part — HMAC-SHA256 over `header.payload`.
It proves integrity (nothing modified) and issuer knowledge; it does NOT
hide the payload.
**Related**: Header

### Timing-safe compare
**Definition**: Comparison whose runtime does not reveal how many leading
characters matched — `hmac.compare_digest` or `bcrypt.checkpw`, never `==`
on secrets.
**Related**: Signature

### Work factor
**Definition**: bcrypt's cost parameter (rounds) controlling how expensive
each hash is — higher slows both attackers and legit logins.
**Related**: bcrypt

## Key Concepts Summary

### The token lifecycle
- Sign short access JWTs (5–15 min) + long refresh JWTs.
- Every request verifies access token: signature, alg pinned, exp, iss/aud.
- Refresh exchange rotates: verify → revoke old jti → issue new pair.
- Reuse of a dead refresh → family revocation.

### The password rules
- bcrypt/argon2 with a real work factor; never sha256 or plaintext.
- Verify with the library's timing-safe compare.
- Two hashes of the same password differ (salting) — assert it.

### What JWTs are bad at
- Revocation (fixed with denylist + short exp).
- Secrecy (payload is readable).
- Alg confusion (fixed by pinning the algorithm).

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Proves integrity, not secrecy — ___
2. Long-lived token that rotates on use — ___
3. Per-password random value — ___
4. Kill switch before expiry — ___
5. Deliberately slow password hash — ___
6. Short-lived token for every request — ___
7. Constant-work comparison — ___
8. Readable by anyone — ___

**Answers:** 1-signature, 2-refresh token, 3-salt, 4-denylist, 5-bcrypt,
6-access token, 7-timing-safe compare, 8-payload
