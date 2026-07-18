# User Service

> Phase 01, Project 02: User management microservice with CRUD operations.

## Goals

Build a user management service that handles profile CRUD operations, pagination, and user administration. This service depends on the auth-service for authentication and demonstrates service-to-service communication.

**Learning outcomes:**
- Full CRUD operations in Go
- Pagination (cursor-based and offset-based)
- Profile management (avatar, bio, preferences)
- Service-to-service communication
- Database transactions
- Input validation and error handling

## API Endpoints

### GET /users
List users with pagination.

```json
// Response (200)
{
  "data": [
    {
      "id": "usr_abc123",
      "email": "student@school.edu",
      "name": "Ahmed Hassan",
      "avatar": "https://...",
      "role": "student",
      "created_at": "2025-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "cursor": "usr_def456",
    "has_more": true,
    "total": 150
  }
}
```

### GET /users/:id
Get user by ID.

### PUT /users/:id
Update user profile.

```json
// Request
{
  "name": "Ahmed Hassan",
  "avatar": "https://example.com/avatar.jpg",
  "bio": "Computer Science student"
}
```

### DELETE /users/:id
Soft-delete user account.

### GET /users/:id/stats
Get user statistics (courses completed, quizzes taken, etc.).

## Project Structure

```
02-user-service/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── user/
│   │   ├── handler.go
│   │   ├── service.go
│   │   ├── repository.go
│   │   ├── model.go
│   │   └── dto.go
│   ├── middleware/
│   │   ├── auth.go          # Reuse from auth-service
│   │   └── pagination.go
│   └── config/
│       └── config.go
├── migrations/
│   ├── 000001_create_users.up.sql
│   └── 000001_create_users.down.sql
├── tests/
├── Dockerfile
├── docker-compose.yml
├── go.mod
└── Makefile
```

## Database Schema

```sql
CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       VARCHAR(255) UNIQUE NOT NULL,
    name        VARCHAR(255) NOT NULL,
    avatar      VARCHAR(500),
    bio         TEXT,
    role        VARCHAR(50) DEFAULT 'student',
    is_active   BOOLEAN DEFAULT true,
    deleted_at  TIMESTAMPTZ,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_deleted_at ON users(deleted_at);
```

## Pagination Strategy

### Cursor-Based (Primary)
```sql
-- Fetch users after a cursor
SELECT * FROM users
WHERE deleted_at IS NULL
AND id > $1
ORDER BY id
LIMIT 20;
```

### Offset-Based (Legacy Support)
```sql
-- Fetch users with offset
SELECT * FROM users
WHERE deleted_at IS NULL
ORDER BY created_at DESC
LIMIT $1 OFFSET $2;
```

**Why cursor-based?** Better performance for large datasets, stable pagination during concurrent writes.

## Setup

```bash
cd projects/01-backend-go/02-user-service

# Start dependencies
docker-compose up -d

# Run migrations
make migrate-up

# Start server
make run
```

## Testing

```bash
# Unit tests
make test

# Integration tests
make test-integration

# Load test
make load-test
```

## Status

| Milestone | Status |
|-----------|--------|
| Project structure | ✅ Complete |
| CRUD operations | ✅ Complete |
| Pagination (cursor + offset) | ✅ Complete |
| Profile management | ✅ Complete |
| Service-to-service auth | ✅ Scaffolded (bearer gate; JWT verify TODO) |
| Tests (unit, DB-free) | ✅ Complete |

---

*Next: [03-chat-service](../03-chat-service/) — Real-time messaging with WebSockets.*
