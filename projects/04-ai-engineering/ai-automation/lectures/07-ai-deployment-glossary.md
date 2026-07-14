# Glossary: AI Deployment

## Quick Reference Table

| Term | Definition | Key Point |
|------|-----------|-----------|
| Container | Isolated runtime environment | Docker, consistent deployment |
| Kubernetes | Container orchestration platform | Manages containers at scale |
| Docker | Containerization tool | Package apps with dependencies |
| CI/CD | Continuous Integration/Deployment | Automated testing and deployment |
| Health Check | Service availability test | Liveness and readiness probes |
| Auto-scaling | Automatic resource adjustment | Based on load metrics |
| GPU | Graphics Processing Unit | Accelerates AI inference |
| Model Serving | Deploying ML models | TensorFlow Serving, TorchServe |
| Latency | Response time | Time to first token, end-to-end |
| Throughput | Requests per second | System capacity |
| Monitoring | Observability system | Metrics, logs, traces |
| Rollback | Revert to previous version | Quick failure recovery |

---

## Detailed Definitions

### Container

**Definition:** A lightweight, standalone, executable package that includes everything needed to run software: code, runtime, system tools, and libraries.

**Example:**
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build and run container
docker build -t ai-service .
docker run -p 8000:8000 ai-service
```

**Related Terms:** Docker, Image, Orchestration

**Benefits:**
- Consistency across environments
- Isolation from host system
- Portable and reproducible
- Easy scaling

---

### Docker

**Definition:** A platform for developing, shipping, and running applications in containers. The standard tool for containerization.

**Example:**
```bash
# Build image
docker build -t ai-service:v1.0 .

# Run container
docker run -d \
  --name ai-api \
  -p 8000:8000 \
  -e OPENAI_API_KEY=sk-... \
  ai-service:v1.0

# View logs
docker logs ai-api

# Stop container
docker stop ai-api
```

**Related Terms:** Container, Image, Docker Compose

**Key Commands:**
- `build`: Build image from Dockerfile
- `run`: Run a container
- `push/pull`: Share images
- `compose`: Multi-container apps

---

### Kubernetes (K8s)

**Definition:** An open-source container orchestration platform that automates deployment, scaling, and management of containerized applications.

**Example:**
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-service
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
        image: ai-service:v1.0
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
```

```bash
# Deploy
kubectl apply -f deployment.yaml

# Check status
kubectl get pods
kubectl get services

# Scale
kubectl scale deployment ai-service --replicas=5
```

**Related Terms:** Pod, Service, Deployment, ReplicaSet

**Key Concepts:**
- Pods: Smallest deployable units
- Services: Network abstraction
- Deployments: Desired state management
- Namespaces: Resource isolation

---

### CI/CD

**Definition:** Continuous Integration and Continuous Deployment/Delivery - practices for automating code testing and deployment.

**Example:**
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Run tests
      run: pytest tests/

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - name: Build Docker image
      run: docker build -t ai-service:${{ github.sha }} .

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
    - name: Deploy
      run: kubectl apply -f k8s/
```

**Related Terms:** Pipeline, Build, Test, Deploy

**Stages:**
- **CI:** Build, test, validate
- **CD:** Deploy to staging, production
- **CT:** Continuous testing

---

### Health Check

**Definition:** A mechanism to determine if a service is running correctly and able to handle requests. Includes liveness and readiness probes.

**Example:**
```python
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()
start_time = datetime.now()

@app.get("/health")
async def health_check():
    """Liveness probe - is the service running?"""
    return {
        "status": "healthy",
        "uptime": (datetime.now() - start_time).total_seconds()
    }

@app.get("/ready")
async def readiness_check():
    """Readiness probe - is the service ready?"""
    # Check dependencies
    db_ok = check_database()
    cache_ok = check_cache()
    
    if db_ok and cache_ok:
        return {"ready": True}
    else:
        raise HTTPException(status_code=503, detail="Not ready")
```

**Related Terms:** Liveness, Readiness, Probe

**Types:**
- **Liveness:** Is the process alive?
- **Readiness:** Can it accept traffic?
- **Startup:** Has initialization completed?

---

### Auto-scaling

**Definition:** Automatically adjusting the number of running instances based on load metrics (CPU, memory, requests).

**Example:**
```yaml
# HorizontalPodAutoscaler
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
  - type: Pods
    pods:
      metric:
        name: requests_per_second
      target:
        type: AverageValue
        averageValue: "100"
```

**Related Terms:** Horizontal, Vertical, Scaling

**Types:**
- **Horizontal:** Add/remove instances
- **Vertical:** Increase/decrease resources
- **Scheduled:** Time-based scaling

---

### GPU

**Definition:** Graphics Processing Unit - specialized hardware for parallel computation. Essential for AI model training and inference.

**Example:**
```python
# Check GPU availability
import torch

if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")
else:
    device = torch.device("cpu")
    print("Using CPU")

# Move model to GPU
model = model.to(device)
```

```yaml
# Kubernetes GPU allocation
resources:
  limits:
    nvidia.com/gpu: "1"  # Request 1 GPU
```

**Related Terms:** CUDA, VRAM, Inference

**Considerations:**
- VRAM requirements
- GPU memory management
- Multi-GPU inference
- Cost optimization

---

### Model Serving

**Definition:** Deploying machine learning models as services that can receive requests and return predictions.

**Example:**
```python
# FastAPI model serving
from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()
model = joblib.load("model.pkl")

class PredictionRequest(BaseModel):
    features: list

class PredictionResponse(BaseModel):
    prediction: float
    confidence: float

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    prediction = model.predict([request.features])
    confidence = model.predict_proba([request.features]).max()
    
    return PredictionResponse(
        prediction=float(prediction[0]),
        confidence=float(confidence)
    )
```

**Related Terms:** Inference, API, Deployment

**Frameworks:**
- TensorFlow Serving
- TorchServe
- Triton Inference Server
- FastAPI/Flask

---

### Latency

**Definition:** The time delay between sending a request and receiving a response. Critical for user experience.

**Example:**
```python
import time
from contextlib import contextmanager

@contextmanager
def measure_latency():
    start = time.time()
    yield
    latency = (time.time() - start) * 1000  # ms
    return latency

# Usage
with measure_latency() as latency:
    response = model.generate(prompt)

print(f"Latency: {latency:.0f}ms")
```

**Related Terms:** Throughput, Response Time, TTFT

**Types:**
- **TTFT:** Time to first token
- **End-to-end:** Total response time
- **P50/P95/P99:** Percentile latencies

---

### Throughput

**Definition:** The number of requests a system can process per unit time. Measures system capacity.

**Example:**
```python
import time
from concurrent.futures import ThreadPoolExecutor

def measure_throughput(system_fn, requests, max_workers=10):
    """Measure system throughput."""
    start = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(system_fn, requests))
    
    elapsed = time.time() - start
    throughput = len(requests) / elapsed
    
    return {
        "requests_per_second": throughput,
        "total_requests": len(requests),
        "total_time_seconds": elapsed
    }
```

**Related Terms:** Latency, Capacity, Concurrency

**Relationship:**
- High throughput + low latency = good
- High throughput + high latency = overloaded
- Low throughput + low latency = underutilized

---

### Monitoring

**Definition:** The practice of collecting, analyzing, and acting on metrics, logs, and traces to understand system behavior.

**Example:**
```python
from prometheus_client import Counter, Histogram
import logging

# Metrics
REQUEST_COUNT = Counter('requests_total', 'Total requests', ['endpoint'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency')

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Usage
@app.post("/query")
async def query(request: QueryRequest):
    REQUEST_COUNT.labels(endpoint='/query').inc()
    
    with REQUEST_LATENCY.time():
        result = process(request)
    
    logger.info(f"Query processed: {request.query[:50]}")
    return result
```

**Related Terms:** Metrics, Logs, Traces, APM

**Three Pillars:**
- **Metrics:** Numerical measurements
- **Logs:** Event records
- **Traces:** Request paths

---

### Rollback

**Definition:** Reverting a system to a previous version after a failed deployment or bug discovery.

**Example:**
```bash
# Kubernetes rollback
kubectl rollout undo deployment/ai-service

# Check rollout history
kubectl rollout history deployment/ai-service

# Rollback to specific revision
kubectl rollout undo deployment/ai-service --to-revision=2
```

```python
# Application-level rollback
class VersionedDeployment:
    def __init__(self):
        self.versions = {}
        self.current_version = None
    
    def deploy(self, version, model):
        self.versions[version] = model
        self.current_version = version
    
    def rollback(self, target_version=None):
        if target_version is None:
            # Rollback to previous
            versions = sorted(self.versions.keys())
            idx = versions.index(self.current_version)
            target_version = versions[idx - 1]
        
        self.current_version = target_version
        return self.versions[target_version]
```

**Related Terms:** Version, Recovery, Deployment

**Strategies:**
- Blue-green deployment
- Canary releases
- Rolling updates

---

### Secret Management

**Definition:** Securely storing and accessing sensitive information like API keys, passwords, and certificates.

**Example:**
```python
# ❌ BAD: Hardcoded secrets
API_KEY = "sk-1234567890"

# ✅ GOOD: Environment variables
import os
API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ BETTER: Secret manager
from google.cloud import secretmanager

def get_secret(secret_name):
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(
        name=f"projects/PROJECT/secrets/{secret_name}/versions/latest"
    )
    return response.payload.data.decode("UTF-8")
```

```yaml
# Kubernetes secrets
apiVersion: v1
kind: Secret
metadata:
  name: ai-secrets
type: Opaque
data:
  openai-api-key: <base64-encoded-key>
```

**Related Terms:** Environment Variables, Vault, Encryption

**Best Practices:**
- Never commit secrets to code
- Use secret managers
- Rotate secrets regularly
- Audit access

---

### Blue-Green Deployment

**Definition:** A deployment strategy using two identical environments (blue and green) to minimize downtime and risk.

**Example:**
```yaml
# Blue deployment (current)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-service-blue
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: ai-api
        image: ai-service:v1.0

# Green deployment (new)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-service-green
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: ai-api
        image: ai-service:v2.0

# Service routes to blue by default
# Switch to green when ready
```

**Related Terms:** Canary, Rolling Update, Zero Downtime

**Benefits:**
- Zero downtime
- Easy rollback
- Testing in production
- Gradual migration

---

### Canary Release

**Definition:** A deployment strategy where new version is released to a small subset of users before full rollout.

**Example:**
```yaml
# 90% traffic to v1, 10% to v2
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: ai-service
spec:
  hosts:
  - ai-service
  http:
  - route:
    - destination:
        host: ai-service
        subset: v1
      weight: 90
    - destination:
        host: ai-service
        subset: v2
      weight: 10
```

**Related Terms:** Blue-Green, A/B Testing, Progressive Rollout

**Benefits:**
- Risk mitigation
- Real-world testing
- Gradual validation
- Quick rollback

---

### Load Balancing

**Definition:** Distributing incoming requests across multiple instances to ensure high availability and performance.

**Example:**
```yaml
# Kubernetes Service (built-in load balancing)
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
```

```nginx
# Nginx load balancing
upstream ai_backend {
    server ai-1:8000;
    server ai-2:8000;
    server ai-3:8000;
}

server {
    location / {
        proxy_pass http://ai_backend;
    }
}
```

**Related Terms:** Round Robin, Least Connections, Sticky Sessions

**Algorithms:**
- Round Robin
- Least Connections
- IP Hash
- Weighted

---

### Inference

**Definition:** The process of running input data through a trained model to generate predictions or outputs.

**Example:**
```python
# Model inference
from transformers import pipeline

# Load model
classifier = pipeline("sentiment-analysis")

# Run inference
result = classifier("I love this product!")
print(result)  # [{'label': 'POSITIVE', 'score': 0.9998}]

# Batch inference
results = classifier([
    "Great product!",
    "Terrible experience.",
    "It's okay."
])
```

**Related Terms:** Training, Prediction, Serving

**Considerations:**
- Latency requirements
- Batch size optimization
- GPU utilization
- Model optimization

---

## Summary

Understanding these terms is essential for AI deployment:

1. **Container:** Isolated runtime environment
2. **Docker:** Containerization tool
3. **Kubernetes:** Container orchestration
4. **CI/CD:** Automated deployment
5. **Health Check:** Service availability
6. **Auto-scaling:** Resource adjustment
7. **GPU:** AI acceleration
8. **Model Serving:** ML deployment
9. **Latency/Throughput:** Performance metrics
10. **Monitoring:** Observability

**Next:** See Lecture 08 for multi-agent systems.
