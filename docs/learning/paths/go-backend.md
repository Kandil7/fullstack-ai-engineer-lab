# Learning Path: Go Backend

**Goal:** build production-grade Go backends (auth, users, sessions) with clean layering and
PostgreSQL. Project-based, just-in-time.

**Primary project:** `projects/01-backend-go/01-auth-service`

## Milestones

1. **Go for backend + Postgres 101** — packages, structs, error handling; HTTP server + `/health`; `users` table; `pgx` connection pool + insert.
2. **Layered architecture + CRUD** — handlers / services / repository split; `GET /users`; prepared statements; index on email.
3. **Auth basics** — bcrypt password hashing; `POST /auth/register`, `POST /auth/login`.
4. **JWT + middleware** — signed access tokens with `sub`/`exp`; bearer middleware; protected `GET /me`.
5. **Advanced SQL** — indexes, `EXPLAIN ANALYZE`, keyset vs offset pagination.
6. **Production skeleton** — env config (12-factor), structured logging, uniform JSON errors, unit tests.
7. **Review week** — self-assessment, architecture review, Go cheat sheet.

## The 20% That Unlocks 80%

- Goroutines/channels/context (concurrency model)
- Interfaces for dependency injection and testing
- `database/sql` + `pgx` pooling and `timestamptz`
- Explicit error wrapping (`fmt.Errorf("...: %w", err)`)

## Daily Pattern

1h theory → 3h build (one endpoint) → 1h AI review → 1h recall/Anki.

## Self-Check

Can you explain: connection pooling, JWT verification steps, 401 vs 403, when an index helps,
the request → router → handler → service → repo → DB flow?

## ملخص عربي (Arabic Summary)

مسار Go للـ backend: من أساسيات Go وPostgreSQL إلى auth بـ JWT وطبقات نظيفة، مطبّق على
`auth-service`. التعلم بالمشروع: نظري قليل ثم بناء فعلي ثم مراجعة بالـ AI.
