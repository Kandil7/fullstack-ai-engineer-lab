# Release Gate: auth-service

- **Project:** auth-service
- **Version:** 1.0.0
- **Created:** 2026-06-26
- **Status:** Not ready
- **Owner:** —

---

## Purpose

This checklist defines the criteria that must ALL pass before the auth-service can be considered release-ready. A release gate failure blocks deployment to production.

---

## Gate Criteria

### 1. Code Review Passed

- [ ] All Go source files reviewed by at least one human reviewer
- [ ] AI code review (`ai-review.md`) completed with no Critical findings
- [ ] All High-severity findings resolved or explicitly accepted
- [ ] No hardcoded secrets in any source file
- [ ] No `TODO` or `FIXME` comments in production code (tracked issues OK)

**Reviewer:** —
**Date completed:** —
**Sign-off:** —

### 2. Tests Passing

- [ ] `make test` passes with 0 failures
- [ ] Unit test coverage ≥ 80% for `internal/handler/`
- [ ] Unit test coverage ≥ 70% for `internal/auth/`
- [ ] Integration tests pass against a clean database
- [ ] No flaky tests (run test suite 3x, all pass)
- [ ] Edge cases tested: empty input, invalid email, expired token, malformed JWT

**Test command:** `make test`
**Coverage report:** —
**Date completed:** —

### 3. Security Review Complete

- [ ] SQL injection audit: no string concatenation in queries
- [ ] JWT implementation reviewed: signing, validation, expiry
- [ ] Password hashing: bcrypt with cost ≥ 10
- [ ] Secrets management: no hardcoded credentials, env vars validated
- [ ] Rate limiting: login endpoint protected against brute force
- [ ] CORS configuration: restricted to known origins
- [ ] Input validation: all endpoints validate input at boundaries
- [ ] OWASP Top 10 checklist completed

**Security reviewer:** —
**Date completed:** —

### 4. Documentation Updated

- [ ] README.md reflects current setup instructions
- [ ] API endpoints documented (request/response formats)
- [ ] Environment variables documented (required + optional)
- [ ] Database schema documented (tables, indexes, relationships)
- [ ] Deployment instructions exist (Docker, manual)
- [ ] Known limitations documented

**Documentation location:** `projects/01-backend-go/01-auth-service/README.md`
**Date completed:** —

### 5. ADR Recorded

- [ ] ADR for JWT library choice (jwt/v5 vs alternatives)
- [ ] ADR for password hashing algorithm (bcrypt vs argon2)
- [ ] ADR for database schema decisions (indexes, constraints)
- [ ] Any significant architectural decision has an ADR

**ADR location:** `docs/decisions/`
**Date completed:** —

### 6. Infrastructure Ready

- [ ] Dockerfile builds successfully
- [ ] Docker Compose works for local development
- [ ] Database migrations are versioned and idempotent
- [ ] Health check endpoint exists (`GET /health`)
- [ ] Graceful shutdown implemented (SIGTERM handling)
- [ ] Logging structured (JSON) and includes request ID

**Infrastructure reviewer:** —
**Date completed:** —

---

## Gate Decision

- [ ] **PASS** — All criteria met. Auth-service is release-ready.
- [ ] **CONDITIONAL PASS** — Minor issues documented; release with monitoring.
- [ ] **BLOCK** — Critical issues found. Cannot release.

**Decision made by:** —
**Date:** —
**Rationale:** —

---

## Signatures

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Lead Engineer | — | — | — |
| Security Reviewer | — | — | — |
| QA Engineer | — | — | — |
| Tech Lead | — | — | — |

---

## Notes

- This gate is **cumulative** — all sections must pass, not just most
- A "CONDITIONAL PASS" requires explicit tech lead approval and documented risks
- Re-evaluate this gate after any significant code change
- Gate criteria may evolve as the project matures
