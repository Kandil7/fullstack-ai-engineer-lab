# ThanaweyaGPT Infrastructure

> Docker, Kubernetes, and deployment infrastructure for ThanaweyaGPT.

## Overview

The infrastructure layer provides containerization, orchestration, monitoring, and deployment for all ThanaweyaGPT services. Built with Docker for local development and Kubernetes for production.

## Components

### 1. Docker
- Multi-stage Dockerfiles
- Docker Compose for local development
- Image optimization and security

### 2. Kubernetes
- Deployment manifests
- Service definitions
- ConfigMaps and Secrets
- Horizontal Pod Autoscaling

### 3. Monitoring
- Prometheus metrics
- Grafana dashboards
- Alerting rules

### 4. CI/CD
- GitHub Actions workflows
- Automated testing
- Deployment pipelines

## Docker Architecture

### Service Images

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Backend Services
  auth-service:
    build:
      context: ../backend
      dockerfile: Dockerfile
      target: production
    ports:
      - "8081:8080"
    environment:
      - DATABASE_URL=postgres://user:password@postgres:5432/thanaweyagpt
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      - postgres
      - redis

  chat-service:
    build:
      context: ../backend
      dockerfile: Dockerfile
      target: production
    ports:
      - "8082:8080"
    environment:
      - DATABASE_URL=postgres://user:password@postgres:5432/thanaweyagpt
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  user-service:
    build:
      context: ../backend
      dockerfile: Dockerfile
      target: production
    ports:
      - "8083:8080"
    environment:
      - DATABASE_URL=postgres://user:password@postgres:5432/thanaweyagpt
    depends_on:
      - postgres

  # AI Services
  ai-gateway:
    build:
      context: ../ai
      dockerfile: Dockerfile
      target: production
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - QDRANT_HOST=qdrant
      - QDRANT_PORT=6333
    depends_on:
      - qdrant

  # Databases
  postgres:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=thanaweyagpt
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage

  # Infrastructure
  api-gateway:
    image: kong:3.5-alpine
    ports:
      - "8000:8000"
      - "8443:8443"
      - "8001:8001"
    environment:
      - KONG_DATABASE=off
      - KONG_DECLARATIVE_CONFIG=/kong/kong.yml
    volumes:
      - ./kong.yml:/kong/kong.yml

  # Monitoring
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources

volumes:
  postgres_data:
  redis_data:
  qdrant_data:
  prometheus_data:
  grafana_data:
```

### Multi-Stage Dockerfile (Backend)

```dockerfile
# Stage 1: Build
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build the binary
RUN CGO_ENABLED=0 GOOS=linux go build -o server ./cmd/server

# Stage 2: Production
FROM alpine:3.19

RUN apk --no-cache add ca-certificates tzdata

WORKDIR /root/

# Copy the binary
COPY --from=builder /app/server .

# Copy migrations
COPY --from=builder /app/migrations ./migrations

EXPOSE 8080

CMD ["./server"]
```

### Multi-Stage Dockerfile (AI)

```dockerfile
# Stage 1: Build
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Kubernetes Architecture

### Namespace Structure

```
├── thanaweyagpt
│   ├── backend
│   │   ├── auth-service
│   │   ├── chat-service
│   │   └── user-service
│   ├── ai
│   │   ├── ai-gateway
│   │   └── qdrant
│   ├── databases
│   │   ├── postgres
│   │   └── redis
│   ├── monitoring
│   │   ├── prometheus
│   │   └── grafana
│   └── ingress
│       └── nginx-ingress
```

### Deployment Manifests

```yaml
# backend/auth-service-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: auth-service
  namespace: thanaweyagpt
  labels:
    app: auth-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: auth-service
  template:
    metadata:
      labels:
        app: auth-service
    spec:
      containers:
        - name: auth-service
          image: thanaweyagpt/backend:latest
          ports:
            - containerPort: 8080
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-secrets
                  key: url
            - name: JWT_SECRET
              valueFrom:
                secretKeyRef:
                  name: jwt-secrets
                  key: secret
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
```

### Service Definitions

```yaml
# backend/auth-service-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: auth-service
  namespace: thanaweyagpt
spec:
  selector:
    app: auth-service
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
```

### Ingress Configuration

```yaml
# ingress/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: thanaweyagpt-ingress
  namespace: thanaweyagpt
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts:
        - api.thanaweyagpt.com
      secretName: thanaweyagpt-tls
  rules:
    - host: api.thanaweyagpt.com
      http:
        paths:
          - path: /auth
            pathType: Prefix
            backend:
              service:
                name: auth-service
                port:
                  number: 80
          - path: /chat
            pathType: Prefix
            backend:
              service:
                name: chat-service
                port:
                  number: 80
          - path: /users
            pathType: Prefix
            backend:
              service:
                name: user-service
                port:
                  number: 80
          - path: /ai
            pathType: Prefix
            backend:
              service:
                name: ai-gateway
                port:
                  number: 80
```

### Horizontal Pod Autoscaler

```yaml
# backend/auth-service-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: auth-service-hpa
  namespace: thanaweyagpt
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: auth-service
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Pods
          value: 2
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
```

## Monitoring

### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'auth-service'
    static_configs:
      - targets: ['auth-service:8080']
    metrics_path: /metrics

  - job_name: 'chat-service'
    static_configs:
      - targets: ['chat-service:8080']
    metrics_path: /metrics

  - job_name: 'ai-gateway'
    static_configs:
      - targets: ['ai-gateway:8000']
    metrics_path: /metrics

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
```

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| http_requests_total | Total HTTP requests | - |
| http_request_duration_seconds | Request latency | p99 > 2s |
| http_requests_errors_total | Error count | rate > 1% |
| db_connections_active | DB connections | > 80% |
| redis_memory_used_bytes | Redis memory | > 80% |
| llm_tokens_used_total | LLM tokens | - |
| llm_cost_total | LLM cost | > $100/hour |

### Grafana Dashboards

```json
{
  "dashboard": {
    "title": "ThanaweyaGPT Overview",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{service}}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_errors_total[5m]) / rate(http_requests_total[5m])",
            "legendFormat": "{{service}}"
          }
        ]
      },
      {
        "title": "Response Time (p99)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "{{service}}"
          }
        ]
      }
    ]
  }
}
```

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Go
        uses: actions/setup-go@v5
        with:
          go-version: '1.22'
      
      - name: Run tests
        run: |
          cd backend
          make test
      
      - name: Build
        run: |
          cd backend
          make build

  test-ai:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd ai
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          cd ai
          pytest

  build-and-push:
    needs: [test-backend, test-ai]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push backend
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: true
          tags: thanaweyagpt/backend:latest
      
      - name: Build and push AI
        uses: docker/build-push-action@v5
        with:
          context: ./ai
          push: true
          tags: thanaweyagpt/ai:latest

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Kubernetes
        uses: Azure/k8s-deploy@v4
        with:
          manifests: |
            k8s/backend/*.yaml
            k8s/ai/*.yaml
          images: |
            thanaweyagpt/backend:latest
            thanaweyagpt/ai:latest
```

## Setup

### Local Development

```bash
# Navigate to infra directory
cd projects/07-capstone/thanaweyagpt/infra

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Production Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check status
kubectl get pods -n thanaweyagpt

# View logs
kubectl logs -f deployment/auth-service -n thanaweyagpt

# Scale deployment
kubectl scale deployment auth-service --replicas=5 -n thanaweyagpt
```

## Security

### Security Checklist

- [ ] Use non-root containers
- [ ] Scan images for vulnerabilities
- [ ] Encrypt secrets at rest
- [ ] Use network policies
- [ ] Enable RBAC
- [ ] Audit logging enabled
- [ ] TLS everywhere
- [ ] Regular security updates

### Network Policies

```yaml
# network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-network-policy
  namespace: thanaweyagpt
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: api-gateway
      ports:
        - protocol: TCP
          port: 8080
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - protocol: TCP
          port: 5432
    - to:
        - podSelector:
            matchLabels:
              app: redis
      ports:
        - protocol: TCP
          port: 6379
```

## Cost Optimization

### Resource Allocation

| Service | CPU Request | CPU Limit | Memory Request | Memory Limit |
|---------|-------------|-----------|----------------|--------------|
| auth-service | 250m | 500m | 256Mi | 512Mi |
| chat-service | 250m | 500m | 256Mi | 512Mi |
| user-service | 250m | 500m | 256Mi | 512Mi |
| ai-gateway | 500m | 1000m | 512Mi | 1Gi |
| postgres | 500m | 1000m | 1Gi | 2Gi |
| redis | 250m | 500m | 256Mi | 512Mi |

### Cost Monitoring

```yaml
# cost-alert.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: cost-alerts
  namespace: thanaweyagpt
spec:
  groups:
    - name: cost
      rules:
        - alert: HighLLMCost
          expr: sum(rate(llm_cost_total[1h])) > 100
          for: 1h
          labels:
            severity: warning
          annotations:
            summary: "High LLM cost detected"
            description: "LLM cost is ${{ $value }}/hour"
```

## Status

| Component | Status |
|-----------|--------|
| Docker Compose | ✅ Complete |
| Dockerfiles | ✅ Complete |
| Kubernetes manifests | 🔄 In Progress |
| Monitoring setup | ⬜ Not Started |
| CI/CD pipeline | ⬜ Not Started |

---

*Next: [Documentation](../docs/) — Project documentation and guides.*
