# Auth Service

> Phase 01, Project 01: Production-grade authentication microservice in Go.

## Goals

Build a JWT-based authentication service that handles user registration, login, and token management. This service becomes the foundation for all other Go services in the lab — every subsequent project will depend on it.

**Learning outcomes:**
- Go project layout (cmd/, internal/, pkg/)
- REST API design with proper HTTP status codes
- Password hashing with bcrypt
- JWT generation, validation, and refresh
- PostgreSQL integration with pgx
- Repository pattern for data access
- Middleware for auth checks
- Table-driven tests for every layer

## Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| **Language** | Go 1.22+ | Fast, typed, great concurrency |
| **HTTP Router** | chi | Lightweight, stdlib-compatible, idiomatic |
| **Database** | PostgreSQL 16 | ACID, JSONB support, battle-tested |
| **DB Driver** | pgx | Fastest Go PostgreSQL driver |
| **Auth** | JWT (RS256) | Stateless auth, industry standard |
| **Password Hashing** | bcrypt | Adaptive, time-tested |
| **Migrations** | golang-migrate | Version-controlled schema |
| **Testing** | testify + sqlmock | Table-driven tests, DB mocking |
| **Config** | envconfig | 12-factor app, no YAML secrets |

## API Endpoints

### POST /auth/register
```json
// Request
{
  "email": "student@school.edu",
  "password": "SecurePass123!",
  "name": "Ahmed Hassan"
}

// Response (201)
{
  "id": "usr_abc123",
  "email": "student@school.edu",
  "name": "Ahmed Hassan",
  "created_at": "2025-01-15T10:30:00Z"
}
```

### POST /auth/login
```json
// Request
{
  "email": "student@school.edu",
  "password": "SecurePass123!"
}

// Response (200)
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJSUzI1NiIs...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

### GET /me
```
Headers: Authorization: Bearer eyJhbGciOiJSUzI1NiIs...

// Response (200)
{
  "id": "usr_abc123",
  "email": "student@school.edu",
  "name": "Ahmed Hassan",
  "role": "student",
  "created_at": "2025-01-15T10:30:00Z"
}
```

### POST /auth/refresh
```json
// Request
{
  "refresh_token": "eyJhbGciOiJSUzI1NiIs..."
}

// Response (200)
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "expires_in": 3600
}
```

## Project Structure

```
01-auth-service/
├── cmd/
│   └── server/
│       └── main.go          # Entry point, server config
├── internal/
│   ├── auth/
│   │   ├── handler.go       # HTTP handlers
│   │   ├── service.go       # Business logic
│   │   ├── repository.go    # Database queries
│   │   ├── model.go         # Domain models
│   │   ├── jwt.go           # JWT utilities
│   │   └── password.go      # Password hashing
│   ├── middleware/
│   │   └── auth.go          # JWT validation middleware
│   └── config/
│       └── config.go        # Environment config
├── migrations/
│   ├── 000001_create_users.up.sql
│   └── 000001_create_users.down.sql
├── tests/
│   ├── handler_test.go
│   ├── service_test.go
│   └── repository_test.go
├── Dockerfile
├── docker-compose.yml
├── go.mod
├── go.sum
├── .env.example
└── Makefile
```

## Setup Instructions

### Prerequisites
- Go 1.22+
- Docker & Docker Compose
- PostgreSQL (or use Docker)

### Quick Start
```bash
# Clone and enter directory
cd projects/01-backend-go/01-auth-service

# Start PostgreSQL
docker-compose up -d postgres

# Run migrations
make migrate-up

# Start server
make run

# Server runs on http://localhost:8080
```

### Environment Variables
```bash
# Copy and customize
cp .env.example .env

# Required
DATABASE_URL=postgres://user:password@localhost:5432/authdb?sslmode=disable
JWT_SECRET=your-secret-key-here
JWT_EXPIRY=3600

# Optional
PORT=8080
LOG_LEVEL=debug
```

### Testing
```bash
# Unit tests
make test

# With coverage
make test-coverage

# Integration tests (requires Docker)
make test-integration
```

## Architecture

### Layer Diagram
```
┌─────────────────────────────────────────┐
│              HTTP Layer                 │
│  chi.Router → Middleware → Handler      │
├─────────────────────────────────────────┤
│            Business Logic               │
│  Service Layer (validation, hashing)    │
├─────────────────────────────────────────┤
│             Data Access                 │
│  Repository (pgx, SQL queries)          │
├─────────────────────────────────────────┤
│            PostgreSQL                   │
│  users table, migrations                │
└─────────────────────────────────────────┘
```

### Data Flow
1. Request hits chi router
2. Middleware extracts and validates JWT (if present)
3. Handler parses request body, validates input
4. Service layer performs business logic
5. Repository executes database queries
6. Response serialized as JSON

### Key Design Decisions
- **RS256 for JWTs**: Asymmetric keys allow public verification
- **bcrypt with cost 12**: Balances security and performance
- **Repository pattern**: Separates DB logic from business logic
- **Chi over Gin**: More stdlib-aligned, easier to learn

## Database Schema

```sql
CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       VARCHAR(255) UNIQUE NOT NULL,
    password    VARCHAR(255) NOT NULL,
    name        VARCHAR(255) NOT NULL,
    role        VARCHAR(50) DEFAULT 'student',
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

## Status

| Milestone | Status |
|-----------|--------|
| Project structure | ✅ Complete |
| User registration | ✅ Complete |
| User login | ✅ Complete |
| JWT management | ✅ Complete |
| Middleware | ✅ Complete |
| Tests (80%+ coverage) | 🔄 In Progress |
| Docker setup | ⬜ Not Started |

---

*Next: [02-user-service](../02-user-service/) — Build on this auth service with full CRUD operations.*
