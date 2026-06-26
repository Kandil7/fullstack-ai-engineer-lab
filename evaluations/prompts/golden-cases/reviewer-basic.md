# Golden Case: code-reviewer — Go Handler with Known Issues

- **Prompt ID:** role.code-reviewer
- **Prompt version:** 1.0.0
- **Case ID:** reviewer-basic-001
- **Difficulty:** Basic
- **Created:** 2026-06-26
- **Last run:** —

---

## Input

Review the following Go handler code from the auth-service project:

```go
// internal/handler/auth_handler.go

package handler

import (
    "database/sql"
    "encoding/json"
    "net/http"
    "github.com/golang-jwt/jwt/v5"
    "golang.org/x/crypto/bcrypt"
)

type LoginRequest struct {
    Email    string `json:"email"`
    Password string `json:"password"`
}

type Claims struct {
    UserID int    `json:"user_id"`
    Email  string `json:"email"`
    jwt.RegisteredClaims
}

var jwtSecret = []byte("super-secret-key-123")

func LoginHandler(db *sql.DB) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        var req LoginRequest
        json.NewDecoder(r.Body).Decode(&req)

        query := "SELECT id, email, password_hash FROM users WHERE email = '" + req.Email + "'"
        row := db.QueryRow(query)

        var userID int
        var email, passwordHash string
        row.Scan(&userID, &email, &passwordHash)

        err := bcrypt.CompareHashAndPassword([]byte(passwordHash), []byte(req.Password))
        if err != nil {
            http.Error(w, "Invalid credentials", http.StatusUnauthorized)
            return
        }

        claims := Claims{
            UserID: userID,
            Email:  email,
            RegisteredClaims: jwt.RegisteredClaims{
                ExpiresAt: jwt.NewNumericDate(jwt.NewNumericDate(jwt.NewNumericDate(nil)).Add(24 * 3600)),
            },
        }

        token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
        tokenString, _ := token.SignedString(jwtSecret)

        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(map[string]string{"token": tokenString})
    }
}
```

---

## Expected Findings

The reviewer must identify ALL of the following issues. Each finding must have:
- **Severity** (Critical / High / Medium / Low)
- **Exact file and line reference** (or code area if lines aren't numbered)
- **Why it matters** (impact explanation)
- **Fix suggestion** (not a full rewrite)

### Finding 1: SQL Injection (Critical)
- **Location:** `auth_handler.go` — the query string construction
- **Issue:** Email value is concatenated directly into the SQL query string
- **Impact:** An attacker can inject SQL via the email field (e.g., `' OR 1=1 --`)
- **Expected severity:** Critical (security vulnerability, data breach risk)
- **Expected fix:** Use parameterized query: `db.QueryRow("SELECT ... WHERE email = $1", req.Email)`

### Finding 2: Hardcoded JWT Secret (Critical)
- **Location:** `auth_handler.go` — `var jwtSecret = []byte("super-secret-key-123")`
- **Issue:** JWT signing secret is hardcoded in source code
- **Impact:** Anyone with repo access can forge valid tokens; secret will be in git history
- **Expected severity:** Critical (security vulnerability, auth bypass)
- **Expected fix:** Load from environment variable: `os.Getenv("JWT_SECRET")` with startup validation

### Finding 3: No Input Validation (High)
- **Location:** `auth_handler.go` — immediately after `json.NewDecoder(r.Body).Decode(&req)`
- **Issue:** No validation on `req.Email` or `req.Password` before use
- **Impact:** Empty email could cause unexpected DB behavior; missing password causes nil dereference
- **Expected severity:** High (bug, potential crash)
- **Expected fix:** Check for empty/missing fields and return 400 Bad Request

### Finding 4: Ignored Error from Decode (High)
- **Location:** `auth_handler.go` — `json.NewDecoder(r.Body).Decode(&req)`
- **Issue:** Return value (error) is discarded
- **Impact:** Malformed JSON body causes silently zero-valued struct, leading to wrong behavior
- **Expected severity:** High (bug, undefined behavior)
- **Expected fix:** Check error: `if err := json.NewDecoder(r.Body).Decode(&req); err != nil { ... return 400 }`

### Finding 5: Ignored Error from SignedString (Medium)
- **Location:** `auth_handler.go` — `tokenString, _ := token.SignedString(jwtSecret)`
- **Issue:** Token signing error is discarded
- **Impact:** If signing fails, empty token is sent to client
- **Expected severity:** Medium (potential bug, unlikely with HS256)
- **Expected fix:** Check error and return 500 on signing failure

### Finding 6: Ignored Scan Error (Medium)
- **Location:** `auth_handler.go` — `row.Scan(&userID, &email, &passwordHash)`
- **Issue:** Scan error not checked; if user doesn't exist, values are zero-valued
- **Impact:** `bcrypt.CompareHashAndPassword` called with empty hash, returns error, but error message is misleading ("Invalid credentials" when it's actually "User not found")
- **Expected severity:** Medium (incorrect behavior, poor error differentiation)
- **Expected fix:** Check `sql.ErrNoRows` separately and return appropriate error

### Finding 7: JWT Expiry Calculation Bug (Medium)
- **Location:** `auth_handler.go` — the `ExpiresAt` calculation
- **Issue:** `jwt.NewNumericDate(nil)` is called, then `.Add(24 * 3600)` — the double-wrapping and nil handling is suspicious
- **Impact:** Token expiry may be incorrect or cause a panic
- **Expected severity:** Medium (potential runtime error)
- **Expected fix:** Use `time.Now().Add(24 * time.Hour)` directly

---

## Severity Distribution Expected

| Severity | Count | Findings |
|----------|-------|----------|
| Critical | 2 | SQL injection, hardcoded secret |
| High | 2 | No input validation, ignored decode error |
| Medium | 3 | Ignored sign error, ignored scan error, expiry bug |
| Low | 0 | (none expected in this code) |

---

## Overall Score Expected

- **Score:** 4–5/10 (multiple critical and high issues, security vulnerabilities)
- **Approval decision:** **Block** (Critical findings present)
- **Blocking items:** SQL injection, hardcoded JWT secret

---

## Constraints to Verify

### Constraint: severity-required
- [ ] PASS: Every finding has an explicit severity label
- [ ] PASS: Severity labels match the definitions in the prompt (Critical = security/data-loss)
- [ ] FAIL: Any finding lacks severity or uses incorrect severity

### Constraint: no-rewrite-by-default
- [ ] PASS: No full file rewrite provided
- [ ] PASS: Fix suggestions are targeted (one-liner or short snippet)
- [ ] FAIL: Reviewer rewrites the entire handler

### Constraint: cite-exact-files
- [ ] PASS: Each finding references `auth_handler.go` with code area
- [ ] PASS: References are specific enough to locate the issue
- [ ] FAIL: Findings say "in the code" without file reference

---

## Scoring Rubric

| Dimension | Weight | 0 (Fail) | 1 (Partial) | 2 (Pass) |
|-----------|--------|----------|-------------|----------|
| **Severity Accuracy** | 30% | ≥2 findings with wrong severity | 1 finding with wrong severity | All severities correctly assigned |
| **Issue Coverage** | 25% | Misses ≥2 of the 7 issues | Misses 1 issue | Finds all 7 issues |
| **Actionable Feedback** | 20% | Suggestions are vague ("fix this") | Some suggestions are specific | All suggestions include concrete fix approach |
| **No Rewrite** | 15% | Full file rewrite included | Rewrite for multiple findings | No rewrite, targeted suggestions only |
| **File Citation** | 10% | No file references | Partial references | All findings cite file and code area |

### Pass Threshold
- **Total weighted score ≥ 7.0 / 10**
- **No constraint violations**

---

## Anti-Patterns (Should NOT Appear)

1. **Missing SQL injection** — the most critical issue; if missed, the review fails
2. **Incorrect severity** — e.g., labeling hardcoded secret as "Low"
3. **Rewriting the handler** — the reviewer should suggest fixes, not rewrite
4. **Vague findings** — e.g., "code could be better" without specifics
5. **Style-only review** — focusing on naming conventions while missing security issues

---

## Evaluation Notes

- This is a deliberately vulnerable handler designed to test severity calibration
- The SQL injection is the highest-priority finding — missing it is a review failure
- The hardcoded secret is equally critical — both must be caught
- Medium-severity findings test the reviewer's attention to error handling details
- A score of 4–5/10 with a "Block" decision is the expected outcome
