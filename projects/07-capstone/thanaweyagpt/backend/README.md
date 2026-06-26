# ThanaweyaGPT Backend

> Go-based API services for the ThanaweyaGPT educational platform.

## Overview

The backend provides RESTful APIs for authentication, user management, chat handling, and exam management. Built with Go for performance, type safety, and excellent concurrency support.

## Services

### 1. Auth Service (`/auth`)
- User registration and login
- JWT token management
- Password reset flow
- OAuth2 integration (Google)

### 2. Chat Service (`/chat`)
- Conversation management
- Message handling
- AI tutor integration
- Chat history and search

### 3. User Service (`/users`)
- Profile management
- Preferences storage
- Progress tracking
- Notification settings

### 4. Question Service (`/questions`)
- Question generation
- Question bank management
- Difficulty rating
- Topic categorization

### 5. Exam Service (`/exams`)
- Custom exam creation
- Auto-grading
- Score analysis
- Timer management

## API Design

### Authentication
```bash
# Register
POST /auth/register
{
  "email": "student@example.com",
  "password": "securepass123",
  "name": "Ahmed Hassan",
  "grade": 12
}

# Response
{
  "id": "usr_abc123",
  "email": "student@example.com",
  "token": "eyJhbGciOiJSUzI1NiIs..."
}
```

### Chat
```bash
# Send message to AI tutor
POST /chat
{
  "conversation_id": "conv_abc123",
  "message": "شرح لي مفهوم المشتقات في الرياضيات",
  "subject": "mathematics",
  "language": "ar"
}

# Response (streaming)
{
  "id": "msg_xyz789",
  "content": "المشتقات في الرياضيات هي...",
  "model": "gpt-4",
  "tokens_used": 250
}
```

### Questions
```bash
# Generate practice questions
GET /questions/generate?subject=physics&topic=newton_laws&count=5&difficulty=medium

# Response
{
  "questions": [
    {
      "id": "q_abc123",
      "type": "multiple_choice",
      "question": "What is the SI unit of force?",
      "options": ["Newton", "Joule", "Watt", "Pascal"],
      "correct_answer": 0,
      "explanation": "The Newton is the SI unit of force..."
    }
  ]
}
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       VARCHAR(255) UNIQUE NOT NULL,
    password    VARCHAR(255) NOT NULL,
    name        VARCHAR(255) NOT NULL,
    grade       INTEGER DEFAULT 12,
    language    VARCHAR(10) DEFAULT 'ar',
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);
```

### Conversations Table
```sql
CREATE TABLE conversations (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID REFERENCES users(id),
    subject     VARCHAR(100),
    title       VARCHAR(255),
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);
```

### Messages Table
```sql
CREATE TABLE messages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id),
    role            VARCHAR(20),  -- 'user', 'assistant'
    content         TEXT NOT NULL,
    tokens_used     INTEGER,
    model           VARCHAR(100),
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### Questions Table
```sql
CREATE TABLE questions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject     VARCHAR(100) NOT NULL,
    topic       VARCHAR(100) NOT NULL,
    type        VARCHAR(50),  -- 'multiple_choice', 'short_answer', 'problem'
    difficulty  VARCHAR(20),  -- 'easy', 'medium', 'hard'
    question    TEXT NOT NULL,
    options     JSONB,
    answer      TEXT,
    explanation TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);
```

### Exams Table
```sql
CREATE TABLE exams (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID REFERENCES users(id),
    title       VARCHAR(255),
    duration    INTEGER,  -- minutes
    questions   JSONB,
    score       INTEGER,
    completed   BOOLEAN DEFAULT false,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);
```

## Project Structure

```
backend/
├── cmd/
│   └── server/
│       └── main.go              # Entry point
├── internal/
│   ├── auth/
│   │   ├── handler.go
│   │   ├── service.go
│   │   ├── repository.go
│   │   └── model.go
│   ├── chat/
│   │   ├── handler.go
│   │   ├── service.go
│   │   ├── repository.go
│   │   └── model.go
│   ├── user/
│   │   ├── handler.go
│   │   ├── service.go
│   │   ├── repository.go
│   │   └── model.go
│   ├── question/
│   │   ├── handler.go
│   │   ├── service.go
│   │   └── repository.go
│   ├── exam/
│   │   ├── handler.go
│   │   ├── service.go
│   │   └── repository.go
│   ├── middleware/
│   │   ├── auth.go
│   │   ├── tenant.go
│   │   └── logging.go
│   └── config/
│       └── config.go
├── migrations/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── go.mod
└── Makefile
```

## Setup

### Prerequisites
- Go 1.22+
- PostgreSQL 16+
- Redis 7+
- Docker & Docker Compose

### Quick Start
```bash
# Clone and enter directory
cd projects/07-capstone/thanaweyagpt/backend

# Start dependencies
docker-compose up -d postgres redis

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
DATABASE_URL=postgres://user:password@localhost:5432/thanaweyagpt
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key
AI_SERVICE_URL=http://localhost:8000

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

# Integration tests
make test-integration
```

## Architecture

### Layer Diagram
```
┌─────────────────────────────────────────────────┐
│              HTTP Layer                         │
│  chi.Router → Middleware → Handler              │
├─────────────────────────────────────────────────┤
│            Business Logic                       │
│  Service Layer (validation, orchestration)      │
├─────────────────────────────────────────────────┤
│             Data Access                         │
│  Repository (pgx, SQL queries)                  │
├─────────────────────────────────────────────────┤
│            PostgreSQL + Redis                   │
└─────────────────────────────────────────────────┘
```

### Key Design Decisions
- **Microservices**: Independent services for scalability
- **Event-driven**: Async communication between services
- **CQRS**: Separate read/write models for performance
- **Repository pattern**: Clean separation of concerns

## Status

| Service | Status |
|---------|--------|
| Auth Service | ✅ Complete |
| Chat Service | 🔄 In Progress |
| User Service | 🔄 In Progress |
| Question Service | ⬜ Not Started |
| Exam Service | ⬜ Not Started |

---

*Next: [AI Service](../ai/) — Python-based AI services for RAG and LLM integration.*
