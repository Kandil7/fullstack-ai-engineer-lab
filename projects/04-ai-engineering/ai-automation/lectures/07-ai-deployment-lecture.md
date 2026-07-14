# Lecture 07: AI Deployment

## Topic Overview

AI deployment is the process of taking your AI system from development to production. It encompasses containerization, infrastructure setup, monitoring, scaling, and maintenance. This lecture covers the complete deployment lifecycle, from Docker containers to Kubernetes orchestration, with focus on AI-specific considerations like GPU management, model serving, and cost optimization.

**Duration:** 3-4 hours  
**Difficulty:** Intermediate to Advanced  
**Prerequisites:** Lectures 01-06

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Containerize** AI applications with Docker
2. **Deploy** AI services to cloud platforms
3. **Implement** CI/CD pipelines for AI systems
4. **Monitor** AI service health and performance
5. **Scale** AI services based on demand
6. **Manage** model versioning and updates
7. **Optimize** costs and resource usage
8. **Handle** failures and implement recovery

---

## Key Concepts

### 1. Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI DEPLOYMENT ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │   Client    │ →  │   API GW    │ →  │   Load      │        │
│  │             │    │             │    │   Balancer  │        │
│  └─────────────┘    └─────────────┘    └─────────────┘        │
│                                                │                │
│                            ┌───────────────────┼───────┐       │
│                            ▼                   ▼       ▼       │
│                      ┌─────────┐          ┌─────────┐          │
│                      │ AI Pod  │          │ AI Pod  │          │
│                      │ (GPU)   │          │ (GPU)   │          │
│                      └─────────┘          └─────────┘          │
│                            │                   │                │
│                            └─────────┬─────────┘                │
│                                      ▼                          │
│                              ┌──────────────┐                   │
│                              │  Model Store  │                   │
│                              └──────────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Docker for AI

```dockerfile
# Dockerfile for AI application
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```python
# requirements.txt
fastapi==0.104.1
uvicorn==0.24.0
openai==1.3.0
chromadb==0.4.18
numpy==1.24.3
pydantic==2.5.2
python-dotenv==1.0.0
```

### 3. API Service

```python
"""
Production-ready AI service with FastAPI.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
from openai import OpenAI
import chromadb
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Service",
    description="Production AI API",
    version="1.0.0"
)

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("documents")


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    model: str = "gpt-4"


class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    model: str
    tokens_used: int
    latency_ms: float


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Process a query using RAG."""
    start_time = datetime.now()
    
    try:
        # Generate embedding
        embedding_response = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=request.query
        )
        query_embedding = embedding_response.data[0].embedding
        
        # Retrieve relevant documents
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=request.top_k
        )
        
        # Build context
        context = "\n".join([
            f"[{i+1}] {doc}"
            for i, doc in enumerate(results["documents"][0])
        ])
        
        # Generate answer
        response = openai_client.chat.completions.create(
            model=request.model,
            messages=[
                {
                    "role": "system",
                    "content": "Answer questions based on the provided context. Cite sources."
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {request.query}"
                }
            ],
            temperature=0.3
        )
        
        answer = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
        
        # Calculate latency
        latency_ms = (datetime.now() - start_time).total_seconds() * 1000
        
        # Log query
        logger.info(f"Query processed: {request.query[:50]}... | Tokens: {tokens_used} | Latency: {latency_ms:.0f}ms")
        
        return QueryResponse(
            answer=answer,
            sources=results["metadatas"][0] if results["metadatas"] else [],
            model=request.model,
            tokens_used=tokens_used,
            latency_ms=latency_ms
        )
    
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest")
async def ingest_document(content: str, metadata: dict = None):
    """Ingest a document."""
    try:
        # Generate embedding
        embedding_response = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=content
        )
        embedding = embedding_response.data[0].embedding
        
        # Store in ChromaDB
        doc_id = f"doc_{collection.count()}"
        collection.add(
            documents=[content],
            embeddings=[embedding],
            metadatas=[metadata or {}],
            ids=[doc_id]
        )
        
        logger.info(f"Document ingested: {doc_id}")
        
        return {"status": "success", "doc_id": doc_id}
    
    except Exception as e:
        logger.error(f"Ingestion failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 4. Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  ai-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - CHROMA_HOST=chromadb
      - LOG_LEVEL=INFO
    depends_on:
      - chromadb
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"
    volumes:
      - chroma_data:/chroma/chroma
    environment:
      - ANONYMIZED_TELEMETRY=False
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    restart: unless-stopped

volumes:
  chroma_data:
  prometheus_data:
  grafana_data:
```

### 5. Kubernetes Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-service
  labels:
    app: ai-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-service
  template:
    metadata:
      labels:
        app: ai-service
    spec:
      containers:
      - name: ai-api
        image: your-registry/ai-service:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
            nvidia.com/gpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2000m"
            nvidia.com/gpu: "1"
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: ai-secrets
              key: openai-api-key
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: ai-service
spec:
  selector:
    app: ai-service
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ai-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ai-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### 6. CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy AI Service

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: pytest tests/ --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: docker build -t ai-service:${{ github.sha }} .
    
    - name: Run security scan
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'ai-service:${{ github.sha }}'

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/ai-service \
          ai-api=ai-service:${{ github.sha }}
        kubectl rollout status deployment/ai-service
```

### 7. Monitoring Setup

```python
"""
Monitoring and metrics for AI service.
"""
from prometheus_client import Counter, Histogram, Gauge, start_http_server
from functools import wraps
import time
from datetime import datetime


# Metrics
REQUEST_COUNT = Counter(
    'ai_service_requests_total',
    'Total number of requests',
    ['endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'ai_service_request_latency_seconds',
    'Request latency in seconds',
    ['endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

TOKEN_USAGE = Counter(
    'ai_service_tokens_total',
    'Total tokens used',
    ['model', 'type']  # type: input/output
)

ACTIVE_REQUESTS = Gauge(
    'ai_service_active_requests',
    'Number of active requests'
)

MODEL_ERRORS = Counter(
    'ai_service_model_errors_total',
    'Total model errors',
    ['error_type']
)


def monitor_endpoint(endpoint_name):
    """Decorator to monitor endpoint metrics."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            ACTIVE_REQUESTS.inc()
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                REQUEST_COUNT.labels(endpoint=endpoint_name, status='success').inc()
                return result
            except Exception as e:
                REQUEST_COUNT.labels(endpoint=endpoint_name, status='error').inc()
                MODEL_ERRORS.labels(error_type=type(e).__name__).inc()
                raise
            finally:
                latency = time.time() - start_time
                REQUEST_LATENCY.labels(endpoint=endpoint_name).observe(latency)
                ACTIVE_REQUESTS.dec()
        
        return wrapper
    return decorator


def track_tokens(model: str, input_tokens: int, output_tokens: int):
    """Track token usage."""
    TOKEN_USAGE.labels(model=model, type='input').inc(input_tokens)
    TOKEN_USAGE.labels(model=model, type='output').inc(output_tokens)


# Start metrics server
def start_metrics_server(port=9090):
    """Start Prometheus metrics server."""
    start_http_server(port)
    print(f"Metrics server started on port {port}")
```

---

## Code Examples

### Example 1: Complete Deployment Configuration

```python
"""
Complete deployment configuration and setup.
"""
import os
from dataclasses import dataclass
from typing import Optional, Dict, List
import yaml
import json


@dataclass
class DeploymentConfig:
    """Configuration for AI service deployment."""
    
    # Service
    service_name: str = "ai-service"
    version: str = "1.0.0"
    port: int = 8000
    
    # Resources
    cpu_request: str = "500m"
    cpu_limit: str = "2000m"
    memory_request: str = "1Gi"
    memory_limit: str = "4Gi"
    gpu_count: int = 1
    
    # Scaling
    min_replicas: int = 2
    max_replicas: int = 10
    target_cpu_percent: int = 70
    
    # Health checks
    health_check_path: str = "/health"
    health_check_interval: int = 30
    health_check_timeout: int = 10
    
    # Environment
    env_vars: Dict[str, str] = None
    secrets: List[str] = None
    
    def to_kubernetes_yaml(self) -> str:
        """Generate Kubernetes deployment YAML."""
        
        deployment = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": self.service_name,
                "labels": {"app": self.service_name}
            },
            "spec": {
                "replicas": self.min_replicas,
                "selector": {
                    "matchLabels": {"app": self.service_name}
                },
                "template": {
                    "metadata": {
                        "labels": {"app": self.service_name}
                    },
                    "spec": {
                        "containers": [{
                            "name": self.service_name,
                            "image": f"{self.service_name}:{self.version}",
                            "ports": [{"containerPort": self.port}],
                            "resources": {
                                "requests": {
                                    "cpu": self.cpu_request,
                                    "memory": self.memory_request,
                                    "nvidia.com/gpu": str(self.gpu_count)
                                },
                                "limits": {
                                    "cpu": self.cpu_limit,
                                    "memory": self.memory_limit,
                                    "nvidia.com/gpu": str(self.gpu_count)
                                }
                            },
                            "livenessProbe": {
                                "httpGet": {
                                    "path": self.health_check_path,
                                    "port": self.port
                                },
                                "initialDelaySeconds": 30,
                                "periodSeconds": self.health_check_interval
                            },
                            "readinessProbe": {
                                "httpGet": {
                                    "path": self.health_check_path,
                                    "port": self.port
                                },
                                "initialDelaySeconds": 5,
                                "periodSeconds": 5
                            }
                        }]
                    }
                }
            }
        }
        
        return yaml.dump(deployment, default_flow_style=False)
    
    def to_docker_compose(self) -> str:
        """Generate Docker Compose YAML."""
        
        compose = {
            "version": "3.8",
            "services": {
                self.service_name: {
                    "build": ".",
                    "ports": [f"{self.port}:{self.port}"],
                    "environment": self.env_vars or {},
                    "deploy": {
                        "resources": {
                            "reservations": {
                                "devices": [{
                                    "driver": "nvidia",
                                    "count": self.gpu_count,
                                    "capabilities": ["gpu"]
                                }]
                            }
                        }
                    },
                    "restart": "unless-stopped"
                }
            }
        }
        
        return yaml.dump(compose, default_flow_style=False)


# Usage
config = DeploymentConfig(
    service_name="ai-rag-service",
    version="1.2.0",
    gpu_count=1,
    min_replicas=2,
    max_replicas=8,
    env_vars={
        "OPENAI_API_KEY": "${OPENAI_API_KEY}",
        "LOG_LEVEL": "INFO"
    }
)

# Generate deployment files
with open("k8s-deployment.yaml", "w") as f:
    f.write(config.to_kubernetes_yaml())

with open("docker-compose.yml", "w") as f:
    f.write(config.to_docker_compose())
```

### Example 2: Health Check and Readiness

```python
"""
Comprehensive health check system.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import asyncio
from datetime import datetime
import aiohttp
from openai import OpenAI
import chromadb


class HealthStatus(BaseModel):
    """Health status response."""
    status: str  # "healthy", "degraded", "unhealthy"
    timestamp: str
    version: str
    checks: Dict[str, Dict]
    uptime_seconds: float


class HealthChecker:
    """Comprehensive health checking."""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.checks = {}
    
    async def check_openai(self) -> Dict:
        """Check OpenAI API connectivity."""
        try:
            client = OpenAI()
            # Simple test call
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input="health check"
            )
            return {"status": "healthy", "latency_ms": 100}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
    
    async def check_chromadb(self) -> Dict:
        """Check ChromaDB connectivity."""
        try:
            client = chromadb.Client()
            collection = client.create_collection("health_check")
            collection.add(
                documents=["test"],
                ids=["test_id"]
            )
            collection.delete(ids=["test_id"])
            return {"status": "healthy"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
    
    async def check_disk_space(self) -> Dict:
        """Check available disk space."""
        import shutil
        total, used, free = shutil.disk_usage("/")
        free_percent = (free / total) * 100
        
        if free_percent < 10:
            return {"status": "unhealthy", "free_percent": free_percent}
        elif free_percent < 20:
            return {"status": "degraded", "free_percent": free_percent}
        else:
            return {"status": "healthy", "free_percent": free_percent}
    
    async def check_memory(self) -> Dict:
        """Check memory usage."""
        import psutil
        memory = psutil.virtual_memory()
        
        if memory.percent > 90:
            return {"status": "unhealthy", "used_percent": memory.percent}
        elif memory.percent > 80:
            return {"status": "degraded", "used_percent": memory.percent}
        else:
            return {"status": "healthy", "used_percent": memory.percent}
    
    async def run_all_checks(self) -> HealthStatus:
        """Run all health checks."""
        
        checks = {
            "openai": await self.check_openai(),
            "chromadb": await self.check_chromadb(),
            "disk": await self.check_disk_space(),
            "memory": await self.check_memory()
        }
        
        # Determine overall status
        statuses = [check["status"] for check in checks.values()]
        
        if all(s == "healthy" for s in statuses):
            overall_status = "healthy"
        elif any(s == "unhealthy" for s in statuses):
            overall_status = "unhealthy"
        else:
            overall_status = "degraded"
        
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        return HealthStatus(
            status=overall_status,
            timestamp=datetime.now().isoformat(),
            version="1.0.0",
            checks=checks,
            uptime_seconds=uptime
        )


# FastAPI app
app = FastAPI()
health_checker = HealthChecker()


@app.get("/health", response_model=HealthStatus)
async def health_check():
    """Detailed health check endpoint."""
    status = await health_checker.run_all_checks()
    
    if status.status == "unhealthy":
        raise HTTPException(status_code=503, detail=status.dict())
    
    return status


@app.get("/ready")
async def readiness_check():
    """Readiness probe - is the service ready to accept traffic?"""
    status = await health_checker.run_all_checks()
    
    if status.status == "unhealthy":
        raise HTTPException(status_code=503, detail="Not ready")
    
    return {"ready": True}
```

---

## Common Mistakes to Avoid

### 1. No Health Checks
```python
# ❌ BAD: No health checks
@app.get("/query")
async def query(request: QueryRequest):
    # May fail silently
    return process(request)

# ✅ GOOD: With health checks and error handling
@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/query")
async def query(request: QueryRequest):
    try:
        return process(request)
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

### 2. No Resource Limits
```yaml
# ❌ BAD: No resource limits
containers:
- name: ai-service
  image: ai-service:latest

# ✅ GOOD: With resource limits
containers:
- name: ai-service
  image: ai-service:latest
  resources:
    requests:
      memory: "1Gi"
      cpu: "500m"
    limits:
      memory: "4Gi"
      cpu: "2000m"
```

### 3. No Monitoring
```python
# ❌ BAD: No metrics
@app.post("/query")
async def query(request: QueryRequest):
    return process(request)

# ✅ GOOD: With metrics
@app.post("/query")
@monitor_endpoint("query")
async def query(request: QueryRequest):
    result = process(request)
    track_tokens(request.model, result.tokens_used, 0)
    return result
```

---

## Best Practices

1. **Containerize everything** - Docker for consistency
2. **Health checks** - Liveness and readiness probes
3. **Resource limits** - CPU, memory, GPU
4. **Auto-scaling** - Based on load
5. **Monitoring** - Metrics, logs, traces
6. **Secrets management** - Never hardcode credentials
7. **CI/CD** - Automated testing and deployment
8. **Rollback capability** - Quick recovery from failures
9. **Cost monitoring** - Track GPU and API usage
10. **Documentation** - Runbooks and procedures

---

## Practice Exercises

### Exercise 1: Dockerize an AI App
Create a Dockerfile for a RAG application with:
- Multi-stage build
- Health checks
- Proper caching

### Exercise 2: Kubernetes Deployment
Deploy an AI service to Kubernetes with:
- Deployment and Service
- Auto-scaling
- Resource limits

### Exercise 3: CI/CD Pipeline
Create a GitHub Actions workflow that:
- Runs tests
- Builds Docker image
- Deploys to staging

### Exercise 4: Monitoring Dashboard
Build a Grafana dashboard showing:
- Request rate
- Latency percentiles
- Error rate
- Token usage

### Exercise 5: Cost Optimization
Implement:
- Request batching
- Model caching
- Usage tracking

---

## Summary

AI deployment requires careful consideration of infrastructure, monitoring, and operations:

1. **Containerization** - Docker for consistency
2. **Orchestration** - Kubernetes for scale
3. **Monitoring** - Metrics, logs, traces
4. **Scaling** - Auto-scaling based on demand
5. **Security** - Secrets, network policies

**Key Success Factors:**
- Health checks and monitoring
- Resource management
- CI/CD automation
- Cost optimization
- Documentation

**Next lecture:** Multi-Agent Systems - Coordinating multiple agents.
