# ThanaweyaGPT Documentation

> Comprehensive documentation for the ThanaweyaGPT educational platform.

## Documentation Structure

```
docs/
├── getting-started/
│   ├── quick-start.md          # 5-minute setup guide
│   ├── development.md          # Development environment setup
│   └── architecture.md         # System architecture overview
├── api/
│   ├── authentication.md       # Auth API reference
│   ├── chat.md                 # Chat API reference
│   ├── questions.md            # Questions API reference
│   └── exams.md                # Exams API reference
├── guides/
│   ├── curriculum-setup.md     # Adding curriculum content
│   ├── model-training.md       # Fine-tuning models
│   └── deployment.md           # Production deployment
├── reference/
│   ├── database-schema.md      # Database schema reference
│   ├── environment-variables.md # Environment configuration
│   └── error-codes.md          # Error code reference
└── contributing/
    ├── code-style.md           # Code style guidelines
    ├── pull-requests.md        # PR process
    └── testing.md              # Testing guidelines
```

## Getting Started

### Quick Start (5 minutes)

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/thanaweyagpt.git
   cd thanaweyagpt
   ```

2. **Start services**
   ```bash
   docker-compose up -d
   ```

3. **Run Flutter app**
   ```bash
   cd frontend
   flutter pub get
   flutter run
   ```

4. **Access services**
   - Backend API: http://localhost:8080
   - AI Service: http://localhost:8000
   - Grafana: http://localhost:3000

### Development Setup

See [development.md](getting-started/development.md) for detailed setup instructions.

## API Documentation

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

See [authentication.md](api/authentication.md) for full reference.

### Chat

```bash
# Send message
POST /chat
{
  "conversation_id": "conv_abc123",
  "message": "شرح لي مفهوم المشتقات",
  "subject": "mathematics"
}

# Response (streaming)
{
  "id": "msg_xyz789",
  "content": "المشتقات في الرياضيات هي...",
  "model": "gpt-4",
  "tokens_used": 250
}
```

See [chat.md](api/chat.md) for full reference.

## Guides

### Curriculum Setup

1. **Prepare content**
   - Create JSON files for each subject
   - Include Arabic and English versions
   - Add metadata (difficulty, prerequisites)

2. **Ingest content**
   ```bash
   python scripts/ingest_curriculum.py --subject mathematics --grade 12
   ```

3. **Verify ingestion**
   ```bash
   python scripts/verify_curriculum.py --subject mathematics
   ```

See [curriculum-setup.md](guides/curriculum-setup.md) for detailed instructions.

### Model Training

1. **Prepare training data**
   - Collect student Q&A pairs
   - Annotate with curriculum topics
   - Split into train/validation/test

2. **Fine-tune model**
   ```bash
   python scripts/fine_tune.py --model gpt-3.5-turbo --data training_data.jsonl
   ```

3. **Evaluate model**
   ```bash
   python scripts/evaluate.py --model fine_tuned_model --test test_data.jsonl
   ```

See [model-training.md](guides/model-training.md) for detailed instructions.

### Deployment

1. **Build images**
   ```bash
   make docker-build
   ```

2. **Push to registry**
   ```bash
   make docker-push
   ```

3. **Deploy to Kubernetes**
   ```bash
   kubectl apply -f k8s/
   ```

See [deployment.md](guides/deployment.md) for detailed instructions.

## Reference

### Database Schema

```sql
-- Users
CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       VARCHAR(255) UNIQUE NOT NULL,
    password    VARCHAR(255) NOT NULL,
    name        VARCHAR(255) NOT NULL,
    grade       INTEGER DEFAULT 12,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Conversations
CREATE TABLE conversations (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID REFERENCES users(id),
    subject     VARCHAR(100),
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Messages
CREATE TABLE messages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id),
    role            VARCHAR(20),
    content         TEXT NOT NULL,
    tokens_used     INTEGER,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

See [database-schema.md](reference/database-schema.md) for full schema.

### Environment Variables

```bash
# Backend
DATABASE_URL=postgres://user:password@localhost:5432/thanaweyagpt
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key
PORT=8080

# AI Service
OPENAI_API_KEY=sk-...
QDRANT_HOST=localhost
QDRANT_PORT=6333
ANTHROPIC_API_KEY=sk-ant-...

# Frontend
API_BASE_URL=http://localhost:8080
```

See [environment-variables.md](reference/environment-variables.md) for full reference.

### Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 429 | Rate Limited |
| 500 | Internal Server Error |

See [error-codes.md](reference/error-codes.md) for full list.

## Contributing

### Code Style

- **Go**: Follow Effective Go guidelines
- **Python**: Follow PEP 8, use Black formatter
- **Dart**: Follow Dart style guide, use dart format

See [code-style.md](contributing/code-style.md) for detailed guidelines.

### Pull Requests

1. Create feature branch from `develop`
2. Make changes and write tests
3. Run `make test` and `make lint`
4. Create PR with description
5. Request review from maintainers
6. Address feedback and merge

See [pull-requests.md](contributing/pull-requests.md) for detailed process.

### Testing

- **Unit tests**: 80%+ coverage required
- **Integration tests**: Test service interactions
- **E2E tests**: Test critical user flows

See [testing.md](contributing/testing.md) for detailed guidelines.

## Documentation Standards

### Writing Style
- Clear and concise
- Use active voice
- Include code examples
- Provide context for decisions

### Formatting
- Use Markdown
- Include table of contents for long docs
- Use code blocks with language hints
- Include screenshots for UI docs

### Maintenance
- Update docs with code changes
- Review docs quarterly
- Archive outdated documentation
- Gather feedback from users

## Documentation Tools

| Tool | Purpose |
|------|---------|
| Markdown | Documentation format |
| Swagger/OpenAPI | API documentation |
| Docusaurus | Documentation site |
| Mermaid | Diagrams |

## Status

| Section | Status |
|---------|--------|
| Quick start | ✅ Complete |
| API docs | 🔄 In Progress |
| Guides | ⬜ Not Started |
| Reference | ⬜ Not Started |
| Contributing | ⬜ Not Started |

---

*Documentation is a living document. Update as the project evolves.*
