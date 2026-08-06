# OAuth2 & OIDC — Glossary 39

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Access token | Token | Key to resource APIs; opaque or JWT; scoped |
| Authorization Code | Flow | One-time code returned via redirect, exchanged for tokens |
| Claims | OIDC | Identity attributes: sub, email, name, email_verified |
| Client credentials | Flow | Machine-to-machine grant with no user |
| code_challenge | PKCE | S256 digest of the verifier sent at authorize time |
| code_verifier | PKCE | Random secret presented at token exchange |
| Discovery | OIDC | `/.well-known/openid-configuration` metadata |
| id_token | OIDC | JWT proving authentication, audience = the app |
| Implicit flow | Anti-pattern | Tokens in URL fragments; replaced by Auth Code + PKCE |
| JWKS | Keys | Published public keys used to verify provider tokens |
| kid | JWT | Key id in the header selecting the JWKS key |
| PKCE | Flow | Proof Key for Code Exchange — binds code to the app |
| Scopes | OAuth2 | Coarse capabilities the app requests (read:models) |
| Token endpoint | Flow | Where the code is exchanged for tokens |

## Detailed Definitions

### Access token
**Definition**: The token presented to resource APIs; carries `scope`
(authorization). Opaque or JWT depending on the provider.
**Related**: Scopes

### Authorization Code
**Definition**: A short-lived, single-use code the provider returns via
redirect; the app exchanges it (with the PKCE verifier) at the token
endpoint.
**Related**: Token endpoint

### Claims
**Definition**: OIDC-standardized identity attributes in the id_token —
`sub`, `email`, `email_verified`, `name`. Identity, not permissions.
**Related**: Scopes

### Client credentials
**Definition**: The OAuth2 grant for machine-to-machine auth — the client
exchanges its own credentials for a token; no user involved.
**Related**: Access token

### code_challenge
**Definition**: `b64url(SHA256(code_verifier))` sent with the authorize
request, so the provider can later confirm the exchange comes from the app
that started the flow.
**Related**: code_verifier

### code_verifier
**Definition**: A random 43–128 char secret kept by the app and presented
with the code at the token endpoint; the code is useless without it.
**Related**: PKCE

### Discovery
**Definition**: The provider metadata endpoint
(`/.well-known/openid-configuration`) listing authorize/token URLs, JWKS
URI, and supported scopes.
**Related**: JWKS

### id_token
**Definition**: The OIDC JWT proving the user authenticated; its `aud` is
the app's client_id. It is a proof of login, not an API credential.
**Related**: Claims

### Implicit flow
**Definition**: The deprecated flow returning tokens in the URL fragment —
leaked via browser history/referrers. Replaced by Authorization Code +
PKCE for public clients.
**Related**: PKCE

### JWKS
**Definition**: JSON Web Key Set — the provider's published public keys.
Your service verifies provider-signed tokens with these; never hardcode
them because keys rotate.
**Related**: kid

### kid
**Definition**: The `kid` header in a JWT selecting which JWKS key signed
it; verification looks up the key by kid.
**Related**: JWKS

### PKCE
**Definition**: Proof Key for Code Exchange (RFC 7636) — binds the
authorization code to the app via the verifier/challenge pair, closing the
code-interception attack.
**Related**: code_verifier

### Scopes
**Definition**: Coarse, provider-decided capabilities the app requests
(`read:models write:runs`) and the consent screen shows. Authorization.
**Related**: Claims

### Token endpoint
**Definition**: The provider endpoint receiving
`code + code_verifier + client_id` and returning
access/id/refresh tokens.
**Related**: Authorization Code

## Key Concepts Summary

### The safe public-client flow
1. Generate verifier + S256 challenge.
2. Authorize with client_id, scope, redirect_uri, code_challenge.
3. Provider redirects with ?code=.
4. Exchange code + verifier at the token endpoint.
5. Verify the id_token locally (aud, iss, exp); use access_token for APIs.

### Scopes vs claims
- Scopes: authorization — what the app may do.
- Claims: identity — who the user is.
- Enforce scopes per route; trust claims per app.

### JWKS discipline
- Read kid from the header, pick the key from JWKS.
- Cache JWKS briefly; refresh when verification fails (rotation).
- Verify signature, iss, aud, exp — always.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Binds the code to the app — ___
2. Sent at authorize; digest of the verifier — ___
3. Identity attributes in the id_token — ___
4. Coarse capabilities — ___
5. Proves authentication to the app — ___
6. Key to resource APIs — ___
7. Selects the JWKS key — ___
8. One-time code exchanged for tokens — ___

**Answers:** 1-PKCE, 2-code_challenge, 3-claims, 4-scopes, 5-id_token,
6-access token, 7-kid, 8-authorization code
