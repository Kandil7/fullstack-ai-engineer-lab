# System Design: ChatGPT Clone

> Complete system design for building a ChatGPT-like AI assistant platform.

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Components](#components)
4. [Scaling Strategy](#scaling-strategy)
5. [Caching](#caching)
6. [Rate Limiting](#rate-limiting)
7. [Cost Considerations](#cost-considerations)
8. [Security](#security)
9. [Monitoring](#monitoring)

---

## Overview

### Requirements

**Functional:**
- User authentication and session management
- Chat interface with conversation history
- AI-powered responses using LLM (GPT-4, Claude, etc.)
- File upload and analysis (images, PDFs)
- Real-time streaming responses
- Conversation search and organization
- User preferences and customization

**Non-Functional:**
- 99.9% uptime
- < 2s first token latency (streaming)
- Support 100K concurrent users
- Scale to 1M conversations/day
- Cost-efficient inference

### Capacity Estimation

| Metric | Value |
|--------|-------|
| Daily active users | 100,000 |
| Conversations per user | 5/day |
| Messages per conversation | 10 |
| Total messages/day | 5,000,000 |
| Avg tokens per message | 500 |
| Total tokens/day | 2.5B |
| Storage per conversation | 10KB |
| Storage per message | 1KB |
| Total storage/year | ~2TB |

---

## Architecture

### High-Level Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Load Balancer                              │
│                    (Cloudflare / AWS ALB)                           │
└─────────────────────┬───────────────────────┬──────────────────────┘
                      │                       │
          ┌───────────▼───────────┐  ┌────────▼────────────┐
          │    Web Frontend       │  │    API Gateway       │
          │    (Next.js)          │  │    (Kong / Envoy)    │
          │    - Chat UI          │  │    - Rate Limiting   │
          │    - File Upload      │  │    - Auth Check      │
          │    - Streaming        │  │    - Request Routing │
          └───────────────────────┘  └────────┬────────────┘
                                              │
              ┌───────────────────────────────┼───────────────────────────────┐
              │                               │                               │
    ┌─────────▼─────────┐      ┌──────────────▼──────────────┐    ┌─────────▼─────────┐
    │   Auth Service    │      │     Chat Service            │    │   User Service    │
    │   (Go)            │      │     (Go)                    │    │   (Go)            │
    │   - JWT tokens    │      │     - Message handling      │    │   - Profile CRUD  │
    │   - OAuth2        │      │     - Conversation mgmt     │    │   - Preferences   │
    └─────────┬─────────┘      │     - File processing       │    └─────────┬─────────┘
              │                 └──────────────┬──────────────┘              │
              │                               │                             │
    ┌─────────▼─────────┐      ┌──────────────▼──────────────┐    ┌─────────▼─────────┐
    │   PostgreSQL      │      │     Redis                   │    │   PostgreSQL      │
    │   (Users, Auth)   │      │     - Sessions              │    │   (User Profiles) │
    └───────────────────┘      │     - Cache                 │    └───────────────────┘
                               │     - Rate Limiting         │
                               └──────────────┬──────────────┘
                                              │
              ┌───────────────────────────────┼───────────────────────────────┐
              │                               │                               │
    ┌─────────▼─────────┐      ┌──────────────▼──────────────┐    ┌─────────▼─────────┐
    │   AI Gateway      │      │     Vector Database         │    │   Object Storage  │
    │   (Go)            │      │     (Qdrant / Pinecone)     │    │   (S3 / R2)       │
    │   - Model routing │      │     - Context retrieval     │    │   - File uploads  │
    │   - Prompt mgmt   │      │     - Semantic search       │    │   - User avatars  │
    │   - Cost tracking │      │     - Embeddings            │    │   - Exports       │
    └─────────┬─────────┘      └──────────────┬──────────────┘    └───────────────────┘
              │                               │
    ┌─────────▼───────────────────────────────▼──────────────┐
    │                  LLM Providers                         │
    │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
    │  │ OpenAI  │  │ Claude  │  │ Gemini  │  │ Local   │   │
    │  │ GPT-4   │  │ 3.5     │  │ Flash   │  │ Llama   │   │
    │  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │
    └────────────────────────────────────────────────────────┘
```

### Service Communication

| From | To | Protocol | Purpose |
|------|-----|----------|---------|
| Frontend | API Gateway | HTTPS | All client requests |
| API Gateway | Auth Service | gRPC | Token validation |
| API Gateway | Chat Service | gRPC | Chat operations |
| Chat Service | AI Gateway | gRPC | LLM inference |
| AI Gateway | LLM Providers | HTTPS | API calls |
| Chat Service | Vector DB | gRPC | Context retrieval |
| All Services | Redis | TCP | Caching, sessions |

---

## Components

### 1. Frontend (Next.js)

**Responsibilities:**
- Chat interface with markdown rendering
- WebSocket connection for streaming
- File upload and preview
- Conversation history sidebar
- User settings and preferences

**Key Technical Decisions:**
- **Streaming**: Use Server-Sent Events (SSE) for LLM responses
- **State Management**: Zustand for client state
- **Styling**: Tailwind CSS + shadcn/ui components
- **File Handling**: Client-side preview before upload

**Performance Optimizations:**
- Lazy load conversation history
- Virtualized message list for long conversations
- Client-side markdown rendering
- Service worker for offline access

### 2. API Gateway (Kong / Envoy)

**Responsibilities:**
- Request routing
- Rate limiting (per user, per IP)
- Authentication verification
- Request/response logging
- CORS handling

**Configuration:**
```yaml
# Rate limiting example
rate_limits:
  - name: per_user
    key: user_id
    limits:
      - period: minute
        max: 60
      - period: hour
        max: 1000
      - period: day
        max: 10000
```

### 3. Auth Service (Go)

**Responsibilities:**
- User registration and login
- JWT token generation and validation
- OAuth2 integration (Google, GitHub)
- Session management
- Password reset flows

**Token Structure:**
```json
{
  "sub": "usr_abc123",
  "email": "user@example.com",
  "role": "user",
  "tier": "pro",
  "iat": 1705312200,
  "exp": 1705315800
}
```

### 4. Chat Service (Go)

**Responsibilities:**
- Conversation CRUD operations
- Message handling and storage
- File upload processing
- WebSocket management for streaming
- Conversation sharing and exports

**Message Flow:**
1. User sends message
2. Chat service validates request
3. Retrieve context from vector DB (if RAG enabled)
4. Call AI Gateway for inference
5. Stream response to client
6. Persist complete message to database

### 5. AI Gateway (Go)

**Responsibilities:**
- Model routing (based on task, cost, latency)
- Prompt template management
- Token counting and cost tracking
- Response caching (semantic deduplication)
- Fallback handling (model failures)

**Model Routing Logic:**
```go
func selectModel(task TaskType, userTier string) string {
    switch task {
    case SimpleQuestion:
        if userTier == "free" {
            return "gpt-3.5-turbo"
        }
        return "gpt-4-turbo"
    case ComplexAnalysis:
        return "gpt-4-turbo"
    case CreativeWriting:
        return "claude-3-opus"
    case CodeGeneration:
        return "gpt-4-turbo"
    default:
        return "gpt-4-turbo"
    }
}
```

### 6. Vector Database (Qdrant)

**Responsibilities:**
- Store conversation embeddings
- Semantic search across conversations
- Context retrieval for RAG
- Similar conversation recommendations

**Schema:**
```json
{
  "collection": "conversations",
  "vector_size": 1536,
  "distance": "Cosine",
  "payload_schema": {
    "user_id": "keyword",
    "conversation_id": "keyword",
    "created_at": "datetime",
    "message_type": "keyword"
  }
}
```

### 7. Object Storage (S3 / Cloudflare R2)

**Responsibilities:**
- File uploads (images, PDFs, documents)
- User avatars
- Conversation exports (JSON, PDF)
- Static assets

---

## Scaling Strategy

### Horizontal Scaling

```
                    Load Balancer
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
   │ Chat    │      │ Chat    │      │ Chat    │
   │ Server 1│      │ Server 2│      │ Server 3│
   └────┬────┘      └────┬────┘      └────┬────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                    ┌────▼────┐
                    │ Redis   │
                    │ Cluster │
                    └────┬────┘
                         │
                    ┌────▼────┐
                    │ DB      │
                    │ Cluster │
                    └─────────┘
```

### Scaling Components

| Component | Scaling Method | Trigger |
|-----------|---------------|---------|
| Frontend | CDN + Edge Functions | Static content |
| API Gateway | Horizontal pods | Request volume |
| Chat Service | Horizontal pods | Connection count |
| AI Gateway | Horizontal pods | Inference volume |
| Redis | Cluster sharding | Memory usage |
| PostgreSQL | Read replicas + sharding | Query volume |
| Vector DB | Horizontal nodes | Index size |

### Auto-Scaling Rules

```yaml
# Chat Service auto-scaling
autoscaling:
  min_replicas: 3
  max_replicas: 50
  metrics:
    - type: Connections
      target: 1000  # per pod
    - type: CPU
      target: 70%
    - type: Memory
      target: 80%
  scale_up:
    cooldown: 60s
  scale_down:
    cooldown: 300s
```

---

## Caching

### Cache Layers

```
┌─────────────────────────────────────────────────────────┐
│                    CDN Cache                            │
│              (Static assets, API responses)             │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                   Browser Cache                         │
│            (Service worker, local storage)              │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                    Redis Cache                          │
│         (Sessions, hot data, rate limits)               │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                 Application Cache                       │
│            (In-memory, LRU, request-level)              │
└─────────────────────────────────────────────────────────┘
```

### What to Cache

| Data | TTL | Cache Key | Invalidation |
|------|-----|-----------|--------------|
| User session | 24h | `session:{token}` | Logout |
| User profile | 1h | `profile:{user_id}` | Profile update |
| Conversation list | 5min | `convos:{user_id}` | New conversation |
| LLM response | 24h | `llm:{hash(prompt)}` | Never (semantic) |
| Rate limit counters | 1min | `ratelimit:{user_id}:{window}` | Auto-expire |

### Semantic Deduplication

Cache similar prompts to avoid redundant LLM calls:

```go
func getCachedResponse(prompt string) (string, bool) {
    // Generate embedding for prompt
    embedding := generateEmbedding(prompt)
    
    // Search for similar cached prompts
    similar := searchCache(embedding, threshold=0.95)
    
    if len(similar) > 0 {
        return similar[0].Response, true
    }
    
    return "", false
}
```

---

## Rate Limiting

### Multi-Tier Rate Limiting

```yaml
rate_limits:
  # Free tier
  free:
    messages_per_minute: 10
    messages_per_hour: 100
    messages_per_day: 1000
    file_uploads_per_day: 5
    max_tokens_per_message: 2000
    
  # Pro tier
  pro:
    messages_per_minute: 60
    messages_per_hour: 1000
    messages_per_day: 10000
    file_uploads_per_day: 50
    max_tokens_per_message: 4000
    
  # Enterprise tier
  enterprise:
    messages_per_minute: 200
    messages_per_hour: 5000
    messages_per_day: 50000
    file_uploads_per_day: 200
    max_tokens_per_message: 8000
```

### Rate Limit Implementation (Redis)

```go
func checkRateLimit(userID string, limit int, window time.Duration) (bool, error) {
    key := fmt.Sprintf("ratelimit:%s:%d", userID, window.Seconds())
    
    pipe := redis.Pipeline()
    incr := pipe.Incr(ctx, key)
    pipe.Expire(ctx, key, window)
    _, err := pipe.Exec(ctx)
    
    if err != nil {
        return false, err
    }
    
    count := incr.Val()
    return count <= int64(limit), nil
}
```

### Graceful Degradation

When rate limited:
1. Return 429 with `Retry-After` header
2. Suggest upgrading to Pro tier
3. Offer queue position for free users

---

## Cost Considerations

### LLM Cost Breakdown

| Model | Input Cost | Output Cost | Use Case |
|-------|-----------|-------------|----------|
| GPT-3.5 Turbo | $0.50/1M tokens | $1.50/1M tokens | Simple queries |
| GPT-4 Turbo | $10/1M tokens | $30/1M tokens | Complex reasoning |
| Claude 3 Opus | $15/1M tokens | $75/1M tokens | Creative tasks |
| Claude 3 Haiku | $0.25/1M tokens | $1.25/1M tokens | Quick answers |

### Cost Optimization Strategies

1. **Model Routing**: Use cheaper models for simple tasks
2. **Prompt Caching**: Cache frequent prompts
3. **Response Streaming**: Reduce perceived latency
4. **Token Limiting**: Enforce max tokens per message
5. **Batch Processing**: Queue non-urgent requests
6. **Semantic Dedup**: Avoid redundant LLM calls

### Monthly Cost Estimate (100K DAU)

| Component | Monthly Cost |
|-----------|-------------|
| Frontend (Vercel) | $200 |
| API Gateway | $500 |
| Chat Service (3 pods) | $1,500 |
| PostgreSQL | $800 |
| Redis | $300 |
| Vector Database | $400 |
| LLM API (GPT-4) | $50,000 |
| LLM API (GPT-3.5) | $5,000 |
| Storage (S3) | $100 |
| Bandwidth | $200 |
| **Total** | ~$59,000 |

### Cost Reduction Tips

- Use GPT-3.5 for 70% of requests (simple queries)
- Implement semantic caching (reduce calls by 20%)
- Use prompt compression (reduce tokens by 30%)
- Offer free tier with lower limits
- Use reserved instances for predictable workloads

---

## Security

### Authentication Flow

```
┌────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Client │────▶│ Gateway │────▶│  Auth   │────▶│  Redis  │
└────────┘     └─────────┘     └─────────┘     └─────────┘
    │              │               │               │
    │              │               │               │
    │◀─────────────┼───────────────┼───────────────┘
    │              │               │
    │   JWT Token  │               │
    │◀─────────────┼───────────────┘
```

### Security Checklist

- [ ] JWT tokens with short expiry (1 hour)
- [ ] Refresh token rotation
- [ ] Rate limiting on auth endpoints
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] CORS properly configured
- [ ] HTTPS enforced
- [ ] Secrets in environment variables
- [ ] Audit logging for sensitive operations

### Data Protection

- Encrypt sensitive data at rest (AES-256)
- Encrypt data in transit (TLS 1.3)
- PII masking in logs
- Conversation data retention policies
- GDPR compliance (data export, deletion)

---

## Monitoring

### Key Metrics

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Request latency (p50) | < 200ms | > 500ms |
| Request latency (p99) | < 2s | > 5s |
| Error rate | < 0.1% | > 1% |
| LLM latency (first token) | < 2s | > 5s |
| Active connections | 100K | > 150K |
| Memory usage | < 70% | > 85% |
| CPU usage | < 70% | > 85% |
| LLM cost per request | < $0.05 | > $0.10 |

### Observability Stack

```
┌─────────────────────────────────────────────────────────┐
│                    Dashboards                            │
│                  (Grafana / Datadog)                     │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                    Metrics                               │
│              (Prometheus / StatsD)                       │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                    Tracing                               │
│            (Jaeger / OpenTelemetry)                      │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                    Logging                               │
│           (ELK Stack / CloudWatch)                       │
└─────────────────────────────────────────────────────────┘
```

### Alerting Rules

```yaml
alerts:
  - name: HighErrorRate
    condition: error_rate > 1%
    duration: 5m
    severity: critical
    
  - name: HighLatency
    condition: p99_latency > 5s
    duration: 10m
    severity: warning
    
  - name: HighLLMCost
    condition: cost_per_hour > $100
    duration: 1h
    severity: warning
    
  - name: LowAvailability
    condition: uptime < 99.9%
    duration: 5m
    severity: critical
```

---

## Deployment

### CI/CD Pipeline

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Push   │───▶│  Test   │───▶│ Build   │───▶│ Deploy  │───▶│ Monitor │
│  Code   │    │  Suite  │    │ Docker  │    │  K8s    │    │ Alerts  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chat-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: chat-service
  template:
    metadata:
      labels:
        app: chat-service
    spec:
      containers:
        - name: chat-service
          image: chat-service:latest
          ports:
            - containerPort: 8080
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-secrets
                  key: url
```

---

## Appendix

### Technology Choices

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Frontend | Next.js | React ecosystem, SSR, Vercel integration |
| API Gateway | Kong | Plugin ecosystem, performance |
| Backend | Go | Performance, concurrency, simplicity |
| Database | PostgreSQL | Reliability, JSONB support |
| Cache | Redis | Speed, pub/sub for WebSocket |
| Vector DB | Qdrant | Performance, easy deployment |
| LLM Gateway | Custom Go service | Cost control, model flexibility |

### Reference Architecture

- [OpenAI Architecture](https://openai.com/research)
- [Anthropic Architecture](https://www.anthropic.com/research)
- [ChatGPT System Design](https://bytebytego.com/courses/system-design-interview/design-a-chat-system)

---

*This design is a living document. Update as you build and learn.*
