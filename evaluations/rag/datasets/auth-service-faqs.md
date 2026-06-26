# RAG Evaluation Dataset: auth-service FAQs

- **Dataset ID:** auth-service-faqs-v1
- **Version:** 1.0.0
- **Created:** 2026-06-26
- **Cases:** 10
- **Topic:** auth-service setup, endpoints, JWT, password hashing, testing

---

## Q1: How do I set up the auth-service locally?

**Question:** What are the prerequisites and steps to run the auth-service locally?

**Expected Answer:** The auth-service requires Go 1.22+, PostgreSQL 15+, and Docker. Run `make dev` from the `projects/01-backend-go/01-auth-service/` directory. This starts the Go server on port 8080 with hot-reload via Air. The database connection is configured via `DATABASE_URL` environment variable, defaulting to `postgres://localhost:5432/auth_service?sslmode=disable`. Run `make migrate-up` to apply database migrations before starting.

**Expected Context Sources:**
- `projects/01-backend-go/01-auth-service/README.md` — setup instructions
- `projects/01-backend-go/01-auth-service/Makefile` — dev target, migrate target
- `projects/01-backend-go/01-auth-service/config/config.go` — DATABASE_URL default

**Difficulty:** Easy
**Topic:** setup

---

## Q2: What endpoints does the auth-service expose?

**Question:** List all API endpoints available in the auth-service with their HTTP methods.

**Expected Answer:** The auth-service exposes the following endpoints:
- `POST /auth/register` — Register a new user (email + password)
- `POST /auth/login` — Authenticate and receive a JWT access token
- `POST /auth/refresh` — Exchange a refresh token for a new access token (if implemented)
- `GET /auth/me` — Get the current authenticated user's profile
- `POST /auth/logout` — Invalidate the current token (if implemented)

All endpoints except `/auth/register` and `/auth/login` require a valid JWT in the `Authorization: Bearer <token>` header.

**Expected Context Sources:**
- `projects/01-backend-go/01-auth-service/internal/handler/auth_handler.go` — handler implementations
- `projects/01-backend-go/01-auth-service/internal/router/router.go` — route definitions

**Difficulty:** Easy
**Topic:** endpoints

---

## Q3: How does JWT token generation work in the auth-service?

**Question:** Explain the JWT token generation process including claims, signing method, and expiry.

**Expected Answer:** JWT tokens are generated using the `github.com/golang-jwt/jwt/v5` library with HS256 signing. The token contains three claims: `user_id` (integer), `email` (string), and standard registered claims (`exp`, `iat`, `iss`). The signing secret is loaded from the `JWT_SECRET` environment variable. Tokens expire after the duration specified in `JWT_EXPIRY` (default 15 minutes). The token is signed with `jwt.SigningMethodHS256` and the secret key, then returned as a base64-encoded string in the login response.

**Expected Context Sources:**
- `projects/01-backend-go/01-auth-service/internal/auth/jwt.go` — token generation logic
- `projects/01-backend-go/01-auth-service/internal/handler/auth_handler.go` — login handler
- `projects/01-backend-go/01-auth-service/config/config.go` — JWT_SECRET and JWT_EXPIRY config

**Difficulty:** Medium
**Topic:** JWT

---

## Q4: What password hashing algorithm does the auth-service use?

**Question:** How are user passwords hashed and verified in the auth-service?

**Expected Answer:** The auth-service uses bcrypt via the `golang.org/x/crypto/bcrypt` package. On registration, the password is hashed with `bcrypt.GenerateFromPassword` using the default cost factor (10). On login, `bcrypt.CompareHashAndPassword` compares the stored hash against the provided plaintext password. The hash is stored in the `password_hash` column of the `users` table as a string.

**Expected Context Sources:**
- `projects/01-backend-go/01-auth-service/internal/handler/auth_handler.go` — bcrypt usage
- `projects/01-backend-go/01-auth-service/internal/auth/password.go` — password utilities (if exists)

**Difficulty:** Easy
**Topic:** password hashing

---

## Q5: How do I write tests for the auth-service?

**Question:** What testing approach does the auth-service use and how do I run the tests?

**Expected Answer:** The auth-service uses Go's standard `testing` package with `httptest` for handler testing and `testcontainers-go` for integration tests against a real PostgreSQL instance. Run `make test` to execute all unit tests. Integration tests are in `tests/integration/` and require Docker. Each handler has a corresponding `*_test.go` file. Mock the database layer using interfaces — the `Store` interface in `internal/store/store.go` defines the contract.

**Expected Context Sources:**
- `projects/01-backend-go/01-auth-service/Makefile` — test target
- `projects/01-backend-go/01-auth-service/internal/handler/auth_handler_test.go` — example tests
- `projects/01-backend-go/01-auth-service/internal/store/store.go` — Store interface

**Difficulty:** Medium
**Topic:** testing

---

## Q6: How does the auth-service handle password validation on registration?

**Question:** What validation rules apply to passwords during user registration?

**Expected Answer:** On registration, the auth-service validates that the password meets minimum requirements: at least 8 characters long. The email is validated for basic format (contains `@` and a domain). If validation fails, the endpoint returns HTTP 400 with a JSON error body describing the validation failure. Passwords are not checked for complexity beyond length in the current implementation.

**Expected Context Sources:**
- `projects/01-backend-go/01-auth-service/internal/handler/auth_handler.go` — registration validation
- `projects/01-backend-go/01-auth-service/internal/validator/validator.go` — validation rules (if exists)

**Difficulty:** Easy
**Topic:** validation

---

## Q7: What database tables does the auth-service use?

**Question:** What is the database schema for the auth-service?

**Expected Answer:** The auth-service uses a single `users` table with the following columns:
- `id` — SERIAL PRIMARY KEY
- `email` — VARCHAR(255) UNIQUE NOT NULL
- `password_hash` — VARCHAR(255) NOT NULL
- `created_at` — TIMESTAMP DEFAULT NOW()
- `updated_at` — TIMESTAMP DEFAULT NOW()

Migrations are stored in `migrations/` and applied with `golang-migrate/migrate`. The migration files are numbered sequentially (e.g., `000001_create_users_table.up.sql`).

**Expected Context Sources:**
- `projects/01-backend-go/01-auth-service/migrations/` — migration SQL files
- `projects/01-backend-go/01-auth-service/internal/store/store.go` — model definition

**Difficulty:** Easy
**Topic:** database

---

## Q8: How does the auth middleware work?

**Question:** Explain how the authentication middleware validates incoming requests.

**Expected Answer:** The auth middleware extracts the JWT from the `Authorization` header (format: `Bearer <token>`). It parses the token using `jwt.Parse` with the `JWT_SECRET` key. If parsing succeeds and the token is not expired, it extracts the `user_id` and `email` claims and adds them to the request context. If parsing fails or the token is expired, it returns HTTP 401 Unauthorized. Protected routes wrap their handlers with `middleware.AuthMiddleware(handler)`.

**Expected Context Sources:**
- `projects/01-backend-go/01-auth-service/internal/middleware/auth.go` — middleware implementation
- `projects/01-backend-go/01-auth-service/internal/router/router.go` — middleware application

**Difficulty:** Medium
**Topic:** JWT, middleware

---

## Q9: How should I handle the JWT_SECRET configuration?

**Question:** What is the recommended way to configure the JWT signing secret?

**Expected Answer:** The JWT secret must be set via the `JWT_SECRET` environment variable. It should be a cryptographically random string of at least 32 characters. Never hardcode it in source code. For development, generate one with `openssl rand -hex 32`. For production, store it in a secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault). The auth-service reads it at startup and will fail to start if `JWT_SECRET` is not set.

**Expected Context Sources:**
- `projects/01-backend-go/01-auth-service/config/config.go` — JWT_SECRET loading
- `projects/01-backend-go/01-auth-service/README.md` — configuration documentation

**Difficulty:** Easy
**Topic:** configuration, JWT

---

## Q10: What error responses does the auth-service return?

**Question:** What HTTP status codes and error formats does the auth-service use?

**Expected Answer:** The auth-service uses standard HTTP status codes:
- `400 Bad Request` — Invalid input (missing fields, invalid email format, short password)
- `401 Unauthorized` — Invalid credentials, expired token, missing token
- `409 Conflict` — Email already registered
- `500 Internal Server Error` — Database errors, token signing failures

All error responses are JSON: `{"error": "<message>"}`. The error message is human-readable and does not leak internal details (e.g., no stack traces, no SQL errors).

**Expected Context Sources:**
- `projects/01-backend-go/01-auth-service/internal/handler/auth_handler.go` — error responses
- `projects/01-backend-go/01-auth-service/internal/middleware/auth.go` — 401 responses

**Difficulty:** Medium
**Topic:** endpoints, error handling

---

## Dataset Statistics

| Metric | Value |
|--------|-------|
| Total questions | 10 |
| Easy | 5 |
| Medium | 5 |
| Hard | 0 |
| Topics covered | setup, endpoints, JWT, password hashing, testing, validation, database, configuration, error handling |
| Expected context sources per question | 2–3 |

## Usage Notes

- This dataset tests retrieval of factual information about the auth-service
- Questions are designed to require 2–3 context chunks for complete answers
- No questions require code generation or implementation advice
- All answers should be grounded in the actual auth-service codebase
