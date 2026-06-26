# Golden Case: debugging-specialist — JWT 401 Validation Failure

- **Prompt ID:** role.debugging-specialist
- **Prompt version:** 1.0.0
- **Case ID:** debugger-basic-001
- **Difficulty:** Basic
- **Created:** 2026-06-26
- **Last run:** —

---

## Input

```
JWT token validation fails with 401 even for valid tokens

The auth-service returns 401 Unauthorized for tokens that were just issued.
The login endpoint works fine and returns a token. But when that token is
immediately used on a protected endpoint, it fails validation.

Token format looks correct (three dot-separated base64 parts).
The same behavior happens in Postman and from the Flutter app.
```

### Additional Context

- auth-service uses Go with `github.com/golang-jwt/jwt/v5`
- Tokens are signed with HS256
- The protected endpoint calls `middleware.AuthMiddleware` which extracts and validates the token
- PostgreSQL stores user data but not token state (stateless JWT)
- The issue started after upgrading from jwt/v4 to jwt/v5
- No configuration changes were made to the signing key

---

## Expected Output Structure

The debugger MUST produce output conforming to `templates/debugging-session.template.md` with:

### 1. Symptom Capture
- **Must:** Restate the observed behavior precisely
- **Must:** Include conditions (token just issued, valid format, fails immediately)
- **Must:** Mention the upgrade context (jwt/v4 → jwt/v5)
- **Expected content:**
  - Token issued successfully at login
  - Token fails validation at protected endpoint
  - Happens with both Postman and Flutter client
  - Started after jwt/v4 to jwt/v5 upgrade

### 2. Hypotheses (Ranked by Probability)
The debugger must generate at least 4 hypotheses, ranked by probability, with evidence for and against each.

**Expected Hypothesis 1 (High Probability):** jwt/v5 changed validation behavior
- **Evidence for:** Issue started immediately after upgrade; v5 has stricter validation defaults
- **Evidence against:** (none strong — this is the most likely cause)
- **Specific v5 changes to consider:**
  - v5 requires explicit parser configuration
  - v5 changed `Parse` to use `Parser` struct with options
  - v5 deprecated some methods and changed default claims validation

**Expected Hypothesis 2 (Medium Probability):** Clock skew between issuer and verifier
- **Evidence for:** Token validated at a different time than issuance
- **Evidence against:** Issue happens immediately (no time drift possible)
- **Diagnostic:** Check `exp` and `iat` claims in the token

**Expected Hypothesis 3 (Medium Probability):** Signing key mismatch
- **Evidence for:** If signing key changed during upgrade, tokens won't validate
- **Evidence against:** Same key is used (per context), but worth verifying
- **Diagnostic:** Decode token header, verify `alg` is HS256, compare key at parse time

**Expected Hypothesis 4 (Low Probability):** Middleware extracting token incorrectly
- **Evidence for:** Different middleware code path than issuance
- **Evidence against:** Token format is correct (three parts visible)
- **Diagnostic:** Add logging to middleware to see extracted token string

**Expected Hypothesis 5 (Low Probability):** Token encoding issue (base64 padding)
- **Evidence for:** JWT uses base64url without padding; if padding is added, parsing fails
- **Evidence against:** Postman shows correct format
- **Diagnostic:** Inspect raw Authorization header value

### 3. Diagnostics Performed
The debugger must suggest at least 3 diagnostic steps, ordered by cost (cheapest first):

**Step 1 (cheapest):** Decode the token at jwt.io and inspect claims
- Check: `exp`, `iat`, `alg`, `iss`, signing method
- What it tells us: Whether token is structurally valid

**Step 2 (cheap):** Add debug logging to middleware
- Log: Raw token string before parsing, error message from `jwt.Parse`
- What it tells us: Exact validation error from v5 parser

**Step 3 (moderate):** Compare jwt/v4 vs v5 `Parse` behavior
- Check: What options v5 requires that v4 didn't
- What it tells us: Whether this is a known upgrade breaking change

**Step 4 (if needed):** Check signing key type
- In v4, key could be `[]byte` or `string`; v5 may be stricter about types
- What it tells us: Whether key type mismatch causes silent failure

### 4. Root Cause (Expected)
The root cause is most likely one of:
- **jwt/v5 requires `jwt.WithValidMethods()` or similar parser options** that v4 didn't require
- **jwt/v5 changed how it handles the `exp` claim** (v5 validates `exp` by default, v4 didn't)
- **jwt/v5 changed the `SignedString` key type requirements**

The debugger should NOT declare a root cause until diagnostics confirm it. The output must say something like "Root cause: TBD — pending diagnostic step [N]"

### 5. Fix (After Root Cause Confirmed)
- Must address the root cause, not just the symptom
- Must mention adding a regression test
- Expected fix direction: Update `jwt.Parse` call to include required v5 options, or adjust token generation

---

## Constraints to Verify

### Constraint: rank-hypotheses-before-fix
- [ ] PASS: Hypotheses table exists with ≥4 entries
- [ ] PASS: Ranked by probability (High → Low)
- [ ] PASS: No fix proposed before hypotheses are listed
- [ ] FAIL: Jumps directly to "the fix is X"

### Constraint: require-evidence
- [ ] PASS: Each hypothesis has "Evidence for" and "Evidence against" columns
- [ ] PASS: Root cause section says "TBD" or "pending diagnostics"
- [ ] FAIL: Declares root cause without diagnostic evidence

### Constraint: no-premature-conclusion
- [ ] PASS: Output asks for diagnostic steps before concluding
- [ ] PASS: Root cause is conditional ("most likely... pending confirmation")
- [ ] FAIL: States "The root cause is X" as the first conclusion

### Constraint: repo-first
- [ ] PASS: References actual auth-service components (middleware, jwt/v5 package)
- [ ] FAIL: Discusses JWT in generic terms without referencing the project

---

## Scoring Rubric

| Dimension | Weight | 0 (Fail) | 1 (Partial) | 2 (Pass) |
|-----------|--------|----------|-------------|----------|
| **Hypothesis Ranking** | 30% | <3 hypotheses or no ranking | 3 hypotheses, partially ranked | ≥4 hypotheses, properly ranked |
| **Evidence Quality** | 25% | No evidence columns | Evidence for only | Both evidence for AND against for each |
| **Systematic Approach** | 20% | Jumps to fix immediately | Some diagnostic steps | Ordered diagnostics, cheapest first |
| **No Premature Conclusion** | 15% | Declares root cause immediately | Conditional root cause | Explicitly says "pending diagnostics" |
| **Project Specificity** | 10% | Generic JWT discussion | References auth-service | References specific files, middleware, upgrade context |

### Pass Threshold
- **Total weighted score ≥ 7.0 / 10**
- **No constraint violations**

---

## Anti-Patterns (Should NOT Appear)

1. **Immediate fix** — "Just add `jwt.WithValidMethods([]string{\"HS256\"})` to your Parse call"
2. **Single hypothesis** — only one possible cause considered
3. **No evidence columns** — hypotheses listed without for/against
4. **Wrong root cause** — blaming the database, network, or unrelated config
5. **Missing upgrade context** — ignoring that jwt/v4 → v5 is the key change event

---

## Evaluation Notes

- This case tests the debugger's ability to methodically investigate a known-class of issue
- The jwt/v4 → v5 upgrade is a strong signal that should be in the top hypothesis
- A good debugger does NOT skip to the fix even though the answer is relatively obvious
- The diagnostic steps should be ordered by cost: decode token (free) → add logging (cheap) → compare versions (moderate)
- A score of 8–9/10 is expected for a well-formed response
