# Auth Service — Feature Plan

> MVP-first approach: ship core auth, then iterate.

## Project Goal

Build a production-ready JWT authentication service in Go that can be reused across all backend projects in the lab.

## MVP Scope (Week 1)

**Must have:**
- User registration with email + password
- User login returning JWT access token
- JWT validation middleware
- GET /me endpoint
- PostgreSQL storage
- Basic tests (unit + integration)

**Nice to have (v1.1):**
- Refresh token rotation
- Password reset flow
- Email verification
- Rate limiting
- OAuth2 providers (Google, GitHub)

**Explicitly out of scope:**
- Multi-factor authentication (add in Phase 06)
- Session management (JWT-only for now)
- User roles/permissions (add in user-service)

## Proposed File Structure

```
01-auth-service/
├── cmd/
│   └── server/
│       └── main.go              # Entry point
├── internal/
│   ├── auth/
│   │   ├── handler.go           # HTTP handlers
│   │   ├── handler_test.go      # Handler tests
│   │   ├── service.go           # Business logic
│   │   ├── service_test.go      # Service tests
│   │   ├── repository.go        # DB queries
│   │   ├── repository_test.go   # Repository tests
│   │   ├── model.go             # Domain types
│   │   ├── dto.go               # Request/response types
│   │   ├── jwt.go               # JWT utilities
│   │   └── password.go          # Password hashing
│   ├── middleware/
│   │   ├── auth.go              # JWT middleware
│   │   └── logging.go           # Request logging
│   └── config/
│       └── config.go            # Env config
├── migrations/
│   └── 000001_create_users.up.sql
├── tests/
│   └── integration_test.go
├── Dockerfile
├── docker-compose.yml
├── go.mod
├── Makefile
└── .env.example
```

## Tasks

### T1: Project Scaffold
- [ ] Initialize Go module
- [ ] Create directory structure
- [ ] Add chi, pgx, testify dependencies
- [ ] Create main.go with chi router
- [ ] Add Dockerfile and docker-compose.yml

### T2: Database Layer
- [ ] Design users table schema
- [ ] Write migration files
- [ ] Implement repository interface
- [ ] Implement repository with pgx
- [ ] Write repository tests

### T3: Auth Service
- [ ] Implement password hashing (bcrypt)
- [ ] Implement JWT generation and validation
- [ ] Create service layer with business logic
- [ ] Write service tests (mock repository)

### T4: HTTP Handlers
- [ ] POST /auth/register handler
- [ ] POST /auth/login handler
- [ ] GET /me handler (with middleware)
- [ ] Input validation
- [ ] Write handler tests

### T5: Middleware
- [ ] JWT validation middleware
- [ ] Request logging middleware
- [ ] Error recovery middleware

### T6: Testing & Polish
- [ ] Integration tests with test database
- [ ] 80%+ coverage report
- [ ] README documentation
- [ ] .env.example with all variables

## Acceptance Criteria

- [ ] `POST /auth/register` creates user, returns 201
- [ ] `POST /auth/login` returns valid JWT, returns 200
- [ ] `GET /me` returns user data when valid JWT provided
- [ ] `GET /me` returns 401 when no/invalid JWT
- [ ] Duplicate email returns 409 Conflict
- [ ] Weak password returns 400 Bad Request
- [ ] All endpoints return proper JSON error responses
- [ ] Tests pass with >80% coverage
- [ ] Docker Compose starts PostgreSQL + server
- [ ] Migrations run automatically on startup

## Open Questions

1. **Token expiry**: Should access tokens expire in 1 hour or 24 hours for development convenience?
   - *Decision*: 1 hour for MVP, add refresh tokens in v1.1

2. **Password requirements**: Minimum length? Complexity rules?
   - *Decision*: Min 8 chars, at least 1 uppercase + 1 number

3. **Email validation**: Validate email format on registration?
   - *Decision*: Yes, basic regex validation + existence check

4. **Roles**: Should we store role in JWT claims or fetch from DB?
   - *Decision*: JWT claims for now, fetch from DB only when permission check needed

## Timeline

| Day | Focus | Deliverable |
|-----|-------|-------------|
| Day 1 | Scaffold + DB | Docker Compose, migrations, repository |
| Day 2 | Service + JWT | Business logic, password hashing, JWT |
| Day 3 | Handlers + Tests | HTTP endpoints, unit tests |
| Day 4 | Middleware + Polish | Auth middleware, integration tests |
| Day 5 | Documentation | README, API docs, cleanup |

---

*This plan is iterative — adjust scope based on daily progress.*
