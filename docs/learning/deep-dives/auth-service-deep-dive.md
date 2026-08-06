# Deep Dive: Auth Service

**Last updated:** 2026-08-06

**Project reference:** `projects/01-backend-go/01-auth-service`

A comprehensive look at the authentication and authorization service — the security
foundation of the entire platform.

---

## 1. JWT Lifecycle

### Token Structure
A JWT has three parts separated by dots: `header.payload.signature`

```
Header:  { "alg": "HS256", "typ": "JWT" }
Payload: { "sub": "user-uuid", "email": "user@example.com", "role": "admin",
           "iat": 1719360000, "exp": 1719363600 }
Signature: HMAC-SHA256(base64(header) + "." + base64(payload), secret)
```

### Why JWT Over Sessions
- **Stateless:** server doesn't store session — any instance can verify
- **Portable:** same token works across Go backend, FastAPI, mobile app
- **Self-contained:** carries user identity, roles, expiry
- **Tradeoff:** can't revoke without a blocklist (vs deleting a session row)

### Token Lifecycle Flow
```
1. User POSTs credentials → auth-service validates
2. Auth-service generates access token (15min) + refresh token (7 days)
3. Both tokens returned to client
4. Client stores access token in memory/secure storage
5. Client sends access token in Authorization header
6. Middleware verifies signature + expiry
7. When access token expires → client sends refresh token
8. Auth-service validates refresh token → issues new access token
9. Refresh token rotated (new refresh token issued, old one invalidated)
```

### Token Refresh Strategy
- **Sliding window:** each refresh extends the session
- **Absolute expiry:** refresh token has a hard deadline regardless of activity
- **Rotation:** every refresh issues a new refresh token, old one is blacklisted
- **Family tracking:** if a stolen refresh token is used after rotation, detect the reuse
  and revoke the entire family

---

## 2. Password Hashing

### Why bcrypt, Not SHA-256
- SHA-256 is fast — GPUs can try billions of hashes per second
- bcrypt is deliberately slow: configurable work factor (cost = 2^cost iterations)
- bcrypt includes a random salt per password — rainbow tables are useless
- Output: `$2a$12$<22-char-salt><31-char-hash>` — salt is embedded in the hash

### Work Factor
- Current recommendation: cost = 12 (2^12 = 4096 iterations)
- Takes ~250ms on modern hardware — fast enough for login, slow enough for brute force
- Rehash on login if cost has been increased since the hash was created

### Implementation in Go
```go
import "golang.org/x/crypto/bcrypt"

// Hash
hash, err := bcrypt.GenerateFromPassword([]byte(password), 12)

// Verify
err := bcrypt.CompareHashAndPassword(hash, []byte(inputPassword))
```

---

## 3. Middleware Chain

### Request Flow
```
HTTP Request
  ↓
CORS Middleware        → handle preflight, add CORS headers
  ↓
Logging Middleware     → log method, path, status, latency
  ↓
Rate Limit Middleware  → 429 if exceeding limits
  ↓
Auth Middleware        → extract Bearer token → verify JWT → inject user into context
  ↓
RBAC Middleware        → check user.role against required role for route
  ↓
Handler                → business logic
```

### Auth Middleware Detail
```go
func AuthMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // 1. Extract "Authorization: Bearer <token>" header
        // 2. Split and decode the token
        // 3. Verify signature with secret key
        // 4. Check expiry (exp claim)
        // 5. Extract claims (sub, email, role)
        // 6. Inject claims into request context
        // 7. Call next.ServeHTTP(w, r)
        // On any failure → 401 Unauthorized
    })
}
```

### Context Propagation
- Go's `context.Context` carries request-scoped values
- User claims stored in context: `ctx = context.WithValue(ctx, userKey, claims)`
- Downstream handlers extract: `user := ctx.Value(userKey).(UserClaims)`
- Avoid: storing too much in context — keep it to auth-related data

---

## 4. Role-Based Access Control (RBAC)

### Role Hierarchy
```
admin    → full access, manage users, manage roles
editor   → create/update content, moderate
user     → read content, manage own profile
guest    → read-only, limited endpoints
```

### Permission Model
```go
type Permission struct {
    Resource string // "users", "documents", "settings"
    Action   string // "read", "create", "update", "delete"
    Role     string // "admin", "editor", "user"
}
```

### RBAC Middleware
```go
func RequireRole(role string) Middleware {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            user := GetUserFromContext(r.Context())
            if user.Role != role && user.Role != "admin" {
                http.Error(w, "Forbidden", http.StatusForbidden)
                return
            }
            next.ServeHTTP(w, r)
        })
    }
}
```

### Route Protection Examples
```
GET  /users          → any authenticated user
POST /users          → admin only
PUT  /users/:id      → admin or the user themselves
DELETE /users/:id    → admin only
GET  /documents      → any authenticated user
POST /documents      → editor or admin
```

---

## 5. Security Considerations

### Token Security
- **Short-lived access tokens:** 15 minutes — limits exposure window
- **Refresh token rotation:** detect token theft via reuse detection
- **Secure storage:** never in localStorage (XSS-vulnerable); use httpOnly cookies or
  secure storage on mobile
- **No sensitive data in JWT:** JWTs are base64, not encrypted — never put passwords
  or PII in the payload

### Transport Security
- **HTTPS everywhere:** tokens in transit must be encrypted
- **HSTS header:** `Strict-Transport-Security: max-age=31536000`
- **Certificate pinning** on mobile: prevent MITM with proxy tools

### Rate Limiting
- Login endpoint: 5 attempts per minute per IP, 10 per hour per email
- Token refresh: 10 per minute per user
- General API: 100 requests per minute per user
- Use sliding window or token bucket algorithms

### Input Validation
- Email format validation (RFC 5322 simplified)
- Password strength: minimum 8 chars, require mixed case + numbers
- Parameterized queries: prevent SQL injection at repository layer
- Request body size limits: prevent memory exhaustion

### Logging & Audit
- Log: failed login attempts, successful logins, token refreshes, role changes
- Never log: passwords, tokens, PII in plaintext
- Structured logging: JSON format for log aggregation (ELK, Loki)
- Audit trail: who did what, when, from where

### OWASP Top 10 Checklist
| Vulnerability | Mitigation |
|---|---|
| Broken Authentication | bcrypt, rate limiting, token rotation |
| Broken Access Control | RBAC middleware, ownership checks |
| Injection | Parameterized queries, input validation |
| Security Misconfiguration | HTTPS, HSTS, minimal error messages |
| Sensitive Data Exposure | No secrets in JWT, encrypted transport |

---

## 6. Database Schema

```sql
CREATE TABLE users (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email      VARCHAR(255) UNIQUE NOT NULL,
    password   VARCHAR(255) NOT NULL,  -- bcrypt hash
    role       VARCHAR(50) NOT NULL DEFAULT 'user',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE refresh_tokens (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id    UUID NOT NULL REFERENCES users(id),
    token_hash VARCHAR(255) NOT NULL,  -- SHA-256 of the refresh token
    expires_at TIMESTAMPTZ NOT NULL,
    revoked    BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_refresh_tokens_user ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_hash ON refresh_tokens(token_hash);
```

---

## 7. Common Failure Modes

| Failure | Symptom | Fix |
|---|---|---|
| Secret key leaked | Anyone can forge tokens | Rotate secret immediately, revoke all tokens |
| Refresh token not rotated | Stolen token usable indefinitely | Rotate on every refresh |
| No rate limiting on login | Brute force attacks | Add per-IP and per-email rate limits |
| Token in localStorage | XSS can steal tokens | Use httpOnly cookies or secure storage |
| Missing CORS config | Cross-origin abuse | Whitelist specific origins |
| No ownership check | User A edits User B's data | Verify `user.id == resource.owner_id` |

---

## Self-Check

Can you explain:
- The full JWT lifecycle from login to token refresh?
- Why bcrypt is used instead of SHA-256 for password hashing?
- How the middleware chain processes a request?
- How RBAC is enforced at the middleware level?
- The security tradeoffs of JWT vs session-based auth?

---

## ملخص عربي (Arabic Summary)

نظرة معمقة في خدمة المصادقة: دورة حياة JWT من الإنشاء إلى التجديد، تجزئة كلمات المرور
بـ bcrypt، سلسلة الوسيطات (CORS → Logging → Rate Limit → Auth → RBAC → Handler)،
التحكم بالصلاحيات القائم على الأدوار، اعتبارات الأمان (تخزين التوكن، HTTPS، حدود
معدل الطلبات)، ونمط قاعدة البيانات مع فشل شائع和他的 الأعطال.
