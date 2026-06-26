# Auth Service — AI Review

> Self-review checklist and findings from AI-assisted code review.

## Review Date
<!-- Date of review -->

## Reviewer
<!-- Who/what performed the review -->

## Findings by Severity

### 🔴 Critical (Must fix before merge)

<!-- Security vulnerabilities, data loss risks, broken functionality -->

| # | File | Line | Finding | Status |
|---|------|------|---------|--------|
| 1 | | | | |

### 🟡 Warning (Should fix, not blocking)

<!-- Code smells, missing error handling, performance concerns -->

| # | File | Line | Finding | Status |
|---|------|------|---------|--------|
| 1 | | | | |

### 🔵 Info (Suggestions for improvement)

<!-- Style, naming, minor optimizations -->

| # | File | Line | Finding | Status |
|---|------|------|---------|--------|
| 1 | | | | |

## Security Checklist

- [ ] Passwords hashed with bcrypt (not plain text)
- [ ] JWT secret not hardcoded
- [ ] SQL queries use parameterized statements (no injection)
- [ ] Input validation on all endpoints
- [ ] Rate limiting on login endpoint
- [ ] HTTPS enforced in production
- [ ] CORS configured properly
- [ ] Sensitive data not logged

## Performance Checklist

- [ ] Database connection pooling configured
- [ ] Proper indexing on users table
- [ ] No N+1 queries
- [ ] Response payloads not unnecessarily large

## Code Quality Checklist

- [ ] Error handling consistent across layers
- [ ] No magic numbers or strings
- [ ] Functions under 30 lines
- [ ] Tests cover happy path + error cases
- [ ] No race conditions in concurrent code

## Architecture Review

- [ ] Clear separation of concerns (handler/service/repository)
- [ ] Dependencies injected, not hardcoded
- [ ] Interface boundaries clean
- [ ] Configuration externalized

## Approval

| Gate | Status | Notes |
|------|--------|-------|
| Security | ⬜ Pass / ⬜ Fail | |
| Performance | ⬜ Pass / ⬜ Fail | |
| Code Quality | ⬜ Pass / ⬜ Fail | |
| Tests | ⬜ Pass / ⬜ Fail | |
| **Overall** | ⬜ Approved / ⬜ Needs Work | |

---

*Run this review after each major milestone. Don't wait until "done".*
