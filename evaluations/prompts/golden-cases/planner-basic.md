# Golden Case: project-planner — Basic JWT Refresh Token

- **Prompt ID:** role.project-planner
- **Prompt version:** 1.0.0
- **Case ID:** planner-basic-001
- **Difficulty:** Basic
- **Created:** 2026-06-26
- **Last run:** —

---

## Input

```
Add JWT refresh token support to auth-service
```

### Context Provided

- Project: auth-service (Go backend, PostgreSQL)
- Existing auth flow: register → login → receive access token (15min) → use access token
- No refresh token mechanism exists
- auth-service uses `github.com/golang-jwt/jwt/v5` for JWT signing
- PostgreSQL already has a `users` table with `id`, `email`, `password_hash`, `created_at`
- The service runs behind an API gateway that handles rate limiting

---

## Expected Output Structure

The prompt must produce output conforming to `templates/project-plan.template.md` with ALL of the following sections populated:

### 1. Goal Section
- **Must:** Restate the feature in 1–2 sentences
- **Must:** Reference the auth-service specifically
- **Must NOT:** Add scope beyond refresh tokens (no mention of OAuth, SSO, API keys, or session management)

### 2. MVP First Section
- **Must:** Define an explicit MVP scope
- **Must:** Include "Explicitly deferred (Later)" subsection
- **Expected MVP items:**
  - Generate refresh token on login
  - Store refresh token (hash) in database
  - Validate refresh token and issue new access token
  - Revoke/rotate refresh token on use
- **Expected deferred items (any subset):**
  - Refresh token revocation list (blacklist)
  - Multi-device refresh token support
  - Refresh token expiry configuration
  - Token family tracking for reuse detection

### 3. Task Breakdown Table
- **Must:** Have 4–8 tasks (not fewer, not more)
- **Must:** Each task has estimated minutes (60–90 range expected for most)
- **Must:** Tasks are dependency-ordered (database migration before handlers, handlers before tests)
- **Expected task sequence (roughly):**
  1. Database migration (add `refresh_tokens` table)
  2. Token generation service (refresh token creation + hashing)
  3. Login endpoint modification (issue refresh token alongside access token)
  4. Refresh endpoint (validate refresh token, issue new pair)
  5. Unit tests for token service
  6. Integration tests for refresh flow

### 4. Proposed File Structure
- **Must:** Show concrete file paths, not abstract directories
- **Must:** Include at least one new file for refresh token logic
- **Must:** Include test file(s)
- **Expected structure elements:**
  - `internal/auth/refresh.go` or similar (refresh token service)
  - `internal/handler/auth_handler.go` (modified)
  - `migrations/` (new migration file)
  - `tests/` or `*_test.go` files

### 5. Open Questions Section
- **Must:** List at least 1 open question
- **Expected open questions (any subset):**
  - Refresh token expiry duration (e.g., 7 days, 30 days)
  - Should refresh tokens be single-use (rotation) or multi-use?
  - Storage: hashed in DB vs. signed JWT-only approach?
  - Should existing users be forced to re-login after migration?

### 6. Acceptance Criteria
- **Must:** Have 3–6 criteria
- **Must:** Each criterion is testable/verifiable
- **Expected criteria (any subset):**
  - Login returns both access token and refresh token
  - POST /auth/refresh with valid refresh token returns new access token
  - Used refresh token cannot be reused (if rotation)
  - Expired refresh token returns 401
  - Database stores refresh token metadata (expiry, user_id)

---

## Constraints to Verify

### Constraint: mvp-first
- [ ] PASS: MVP section exists and is clearly bounded
- [ ] PASS: Deferred items are explicitly listed
- [ ] FAIL: Plan includes full implementation without MVP distinction

### Constraint: mark-open-questions
- [ ] PASS: Open Questions section exists with ≥1 item
- [ ] PASS: Questions are genuine unknowns, not rhetorical
- [ ] FAIL: Open Questions section missing or says "None" without justification

### Constraint: no-code
- [ ] PASS: No implementation code blocks in the plan
- [ ] PASS: File structure shows paths only, no file contents
- [ ] FAIL: Plan contains Go/Python/SQL code snippets

### Constraint: repo-first
- [ ] PASS: References existing auth-service structure
- [ ] PASS: New files fit within existing project layout
- [ ] FAIL: Proposes entirely new directories or frameworks not in the repo

---

## Scoring Rubric

| Dimension | Weight | 0 (Fail) | 1 (Partial) | 2 (Pass) |
|-----------|--------|----------|-------------|----------|
| **Completeness** | 25% | Missing ≥2 required sections | Missing 1 section | All sections present and populated |
| **Specificity** | 25% | Generic plan applicable to any project | Some auth-service specifics | References exact tables, packages, endpoints |
| **No Invented Requirements** | 20% | Adds OAuth, SSO, or unrelated features | Adds minor scope creep | Stays strictly within refresh token scope |
| **Task Sizing** | 15% | Tasks are <30min or >120min | 1–2 tasks outside range | All tasks 60–90min range |
| **Open Questions Quality** | 15% | No open questions or trivial ones | 1 relevant question | 2+ questions that genuinely affect scope |

### Pass Threshold
- **Total weighted score ≥ 7.0 / 10**
- **No constraint violations** (any constraint FAIL = automatic review)

### Expected Score for This Input
A well-formed response should score **8–9/10**: complete structure, auth-specific details, proper MVP scoping, and 2–3 genuine open questions about token rotation and expiry.

---

## Anti-Patterns (Should NOT Appear)

1. **Plan includes code** — e.g., `func GenerateRefreshToken() string { ... }`
2. **Scope creep** — e.g., "Also add OAuth2 social login support"
3. **Vague tasks** — e.g., "Implement refresh tokens" as a single task
4. **Missing database work** — plan doesn't address storage schema
5. **No open questions** — claims everything is clear without asking about expiry, rotation, or migration strategy

---

## Evaluation Notes

- This case tests the planner's ability to decompose a well-defined feature request
- The input is intentionally clear — the planner should NOT overcomplicate
- A good response stays close to the existing auth-service patterns
- Watch for: does the planner respect the "no-code" constraint consistently?
