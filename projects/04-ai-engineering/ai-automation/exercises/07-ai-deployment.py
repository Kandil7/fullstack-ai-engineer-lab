"""
Exercise 07: AI Deployment
===========================
Master deploying AI services: FastAPI backends, Docker containerization,
health checks, environment configuration, and monitoring.

Prerequisites:
    pip install fastapi uvicorn pydantic python-dotenv docker prometheus-client

Environment Variables (.env):
    OPENAI_API_KEY=sk-...
    MODEL_NAME=gpt-4o-mini
    MAX_WORKERS=4
"""

import os
import time
import json
import asyncio
from dataclasses import dataclass, field
from typing import Any, Optional, AsyncGenerator
from datetime import datetime
from contextlib import asynccontextmanager
from collections import deque


# ---------------------------------------------------------------------------
# 1. FastAPI AI Service
# ---------------------------------------------------------------------------

@dataclass
class ServiceConfig:
    """Configuration for the AI service."""
    model_name: str = "gpt-4o-mini"
    max_tokens: int = 1024
    temperature: float = 0.7
    max_concurrent_requests: int = 10
    request_timeout: int = 30
    cache_ttl: int = 300  # 5 minutes

    @classmethod
    def from_env(cls) -> "ServiceConfig":
        """Load config from environment variables."""
        return cls(
            model_name=os.getenv("MODEL_NAME", "gpt-4o-mini"),
            max_tokens=int(os.getenv("MAX_TOKENS", "1024")),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            max_concurrent_requests=int(os.getenv("MAX_WORKERS", "10")),
        )


@dataclass
class ServiceMetrics:
    """Track service metrics."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_latency_ms: float = 0.0
    total_tokens: int = 0
    start_time: float = field(default_factory=time.time)

    def record_request(self, latency_ms: float, tokens: int, success: bool):
        self.total_requests += 1
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
        self.total_latency_ms += latency_ms
        self.total_tokens += tokens

    def get_stats(self) -> dict[str, Any]:
        uptime = time.time() - self.start_time
        return {
            "uptime_seconds": uptime,
            "total_requests": self.total_requests,
            "success_rate": self.successful_requests / max(1, self.total_requests),
            "avg_latency_ms": self.total_latency_ms / max(1, self.total_requests),
            "total_tokens": self.total_tokens,
            "requests_per_second": self.total_requests / max(1, uptime),
        }


class AIService:
    """Core AI service with request handling and caching."""

    def __init__(self, config: ServiceConfig):
        self.config = config
        self.metrics = ServiceMetrics()
        self.cache: dict[str, tuple[str, float]] = {}  # key -> (response, timestamp)
        self.semaphore = asyncio.Semaphore(config.max_concurrent_requests)

    def _get_cache_key(self, prompt: str, **kwargs) -> str:
        """Generate cache key for request."""
        key_data = json.dumps({"prompt": prompt, **kwargs}, sort_keys=True)
        return hashlib.md5(key_data.encode()).hexdigest()

    def _check_cache(self, key: str) -> str | None:
        """Check if response is cached and valid."""
        if key in self.cache:
            response, timestamp = self.cache[key]
            if time.time() - timestamp < self.config.cache_ttl:
                return response
            del self.cache[key]
        return None

    def _update_cache(self, key: str, response: str):
        """Update cache with new response."""
        self.cache[key] = (response, time.time())
        # Clean old entries
        if len(self.cache) > 1000:
            oldest = min(self.cache.items(), key=lambda x: x[1][1])
            del self.cache[oldest[0]]

    async def generate(self, prompt: str, **kwargs) -> dict[str, Any]:
        """Generate a response with caching and metrics."""
        import hashlib
        start_time = time.time()

        # Check cache
        cache_key = self._get_cache_key(prompt, **kwargs)
        cached = self._check_cache(cache_key)
        if cached:
            return {
                "response": cached,
                "cached": True,
                "latency_ms": (time.time() - start_time) * 1000,
            }

        # Rate limiting
        async with self.semaphore:
            try:
                # Simulate LLM call (in real use, call actual API)
                await asyncio.sleep(0.1)  # Simulate latency
                response = f"AI response to: {prompt[:50]}..."

                # Update cache
                self._update_cache(cache_key, response)

                # Record metrics
                latency_ms = (time.time() - start_time) * 1000
                tokens = len(response.split())
                self.metrics.record_request(latency_ms, tokens, True)

                return {
                    "response": response,
                    "cached": False,
                    "latency_ms": latency_ms,
                    "tokens": tokens,
                }
            except Exception as e:
                latency_ms = (time.time() - start_time) * 1000
                self.metrics.record_request(latency_ms, 0, False)
                raise

    async def generate_stream(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """Stream response tokens."""
        # Simulate streaming
        words = f"Streaming response to: {prompt[:30]}...".split()
        for word in words:
            yield word + " "
            await asyncio.sleep(0.05)


def create_fastapi_app():
    """Create a FastAPI application (for reference)."""
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel

    app = FastAPI(title="AI Service API", version="1.0.0")

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Request/Response models
    class GenerateRequest(BaseModel):
        prompt: str
        max_tokens: int = 1024
        temperature: float = 0.7
        stream: bool = False

    class GenerateResponse(BaseModel):
        response: str
        latency_ms: float
        tokens: int
        cached: bool

    # Service instance
    config = ServiceConfig.from_env()
    service = AIService(config)

    @app.post("/generate", response_model=GenerateResponse)
    async def generate(request: GenerateRequest):
        try:
            result = await service.generate(
                request.prompt,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
            )
            return GenerateResponse(
                response=result["response"],
                latency_ms=result["latency_ms"],
                tokens=result.get("tokens", 0),
                cached=result["cached"],
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/health")
    async def health():
        return {"status": "healthy", "timestamp": datetime.now().isoformat()}

    @app.get("/metrics")
    async def metrics():
        return service.metrics.get_stats()

    return app


# ---------------------------------------------------------------------------
# 2. Docker Containerization
# ---------------------------------------------------------------------------

DOCKERFILE_TEMPLATE = """
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

DOCKER_COMPOSE_TEMPLATE = """
version: '3.8'

services:
  ai-service:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - MODEL_NAME=${MODEL_NAME:-gpt-4o-mini}
      - MAX_WORKERS=${MAX_WORKERS:-4}
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
"""

def generate_docker_files():
    """Generate Docker configuration files."""
    print("\n" + "=" * 60)
    print("2. DOCKER CONTAINERIZATION")
    print("=" * 60)

    print("\nDockerfile:")
    print(DOCKERFILE_TEMPLATE)

    print("\ndocker-compose.yml:")
    print(DOCKER_COMPOSE_TEMPLATE)

    # Build and run commands
    print("\nCommands:")
    print("  docker build -t ai-service .")
    print("  docker run -p 8000:8000 -e OPENAI_API_KEY=sk-... ai-service")
    print("  docker-compose up -d")


# ---------------------------------------------------------------------------
# 3. Health Checks
# ---------------------------------------------------------------------------

class HealthChecker:
    """Comprehensive health checking for AI services."""

    def __init__(self):
        self.checks: dict[str, callable] = {}
        self.results: dict[str, dict] = {}

    def register_check(self, name: str, check_fn: callable):
        """Register a health check function."""
        self.checks[name] = check_fn

    async def run_checks(self) -> dict[str, Any]:
        """Run all health checks."""
        results = {}
        overall_status = "healthy"

        for name, check_fn in self.checks.items():
            try:
                start_time = time.time()
                result = await check_fn()
                latency_ms = (time.time() - start_time) * 1000

                results[name] = {
                    "status": "healthy",
                    "latency_ms": latency_ms,
                    "details": result,
                }
            except Exception as e:
                results[name] = {
                    "status": "unhealthy",
                    "error": str(e),
                }
                overall_status = "unhealthy"

        self.results = results
        return {
            "status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "checks": results,
        }

    def get_aggregate_status(self) -> str:
        """Get aggregate health status."""
        if not self.results:
            return "unknown"
        statuses = [r.get("status", "unknown") for r in self.results.values()]
        if all(s == "healthy" for s in statuses):
            return "healthy"
        elif any(s == "unhealthy" for s in statuses):
            return "unhealthy"
        return "degraded"


# Common health check implementations
async def check_model_availability() -> dict:
    """Check if the AI model is available."""
    # Simulate model availability check
    return {"model": "gpt-4o-mini", "status": "available"}

async def check_database_connection() -> dict:
    """Check database connectivity."""
    # Simulate database check
    return {"database": "connected", "latency_ms": 5.0}

async def check_cache_availability() -> dict:
    """Check cache availability."""
    # Simulate cache check
    return {"cache": "connected", "keys": 150}

async def check_disk_space() -> dict:
    """Check available disk space."""
    import shutil
    usage = shutil.disk_usage("/")
    free_gb = usage.free / (1024 ** 3)
    return {"free_gb": round(free_gb, 2), "total_gb": round(usage.total / (1024 ** 3), 2)}


def demo_health_checks():
    """Demonstrate health checking."""
    print("\n" + "=" * 60)
    print("3. HEALTH CHECKS")
    print("=" * 60)

    checker = HealthChecker()
    checker.register_check("model", check_model_availability)
    checker.register_check("database", check_database_connection)
    checker.register_check("cache", check_cache_availability)
    checker.register_check("disk", check_disk_space)

    # Run checks (using asyncio.run for demo)
    results = asyncio.run(checker.run_checks())

    print(f"\nOverall Status: {results['status']}")
    print("\nIndividual Checks:")
    for name, check in results["checks"].items():
        status = check["status"]
        latency = check.get("latency_ms", 0)
        print(f"  {name}: {status} ({latency:.1f}ms)")


# ---------------------------------------------------------------------------
# 4. Environment Configuration
# ---------------------------------------------------------------------------

ENV_TEMPLATE = """
# =============================================================================
# AI Service Environment Configuration
# =============================================================================

# API Keys
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Model Configuration
MODEL_NAME=gpt-4o-mini
MAX_TOKENS=1024
TEMPERATURE=0.7

# Service Configuration
MAX_WORKERS=4
REQUEST_TIMEOUT=30
CACHE_TTL=300

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Monitoring
ENABLE_METRICS=true
METRICS_PORT=9090

# Security
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
API_KEY_HEADER=X-API-Key

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/ai_service
REDIS_URL=redis://localhost:6379/0
"""

class ConfigManager:
    """Manage environment configuration with validation."""

    REQUIRED_VARS = [
        "OPENAI_API_KEY",
        "MODEL_NAME",
    ]

    def __init__(self, env_file: str = ".env"):
        self.env_file = env_file
        self.config: dict[str, str] = {}
        self._load_config()

    def _load_config(self):
        """Load configuration from environment and .env file."""
        # Load from environment
        self.config.update(os.environ)

        # Load from .env file if exists
        if os.path.exists(self.env_file):
            with open(self.env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        self.config[key.strip()] = value.strip()

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)

    def get_int(self, key: str, default: int = 0) -> int:
        """Get integer configuration value."""
        try:
            return int(self.config.get(key, default))
        except ValueError:
            return default

    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get boolean configuration value."""
        value = self.config.get(key, str(default)).lower()
        return value in ("true", "1", "yes")

    def validate(self) -> list[str]:
        """Validate required configuration."""
        missing = []
        for var in self.REQUIRED_VARS:
            if var not in self.config or not self.config[var]:
                missing.append(var)
        return missing

    def display(self):
        """Display current configuration (masking sensitive values)."""
        print("\nCurrent Configuration:")
        print("-" * 40)
        for key, value in sorted(self.config.items()):
            # Mask sensitive values
            if any(s in key.upper() for s in ["KEY", "SECRET", "PASSWORD", "TOKEN"]):
                masked = value[:4] + "..." + value[-4:] if len(value) > 8 else "***"
                print(f"  {key}: {masked}")
            else:
                print(f"  {key}: {value}")


def demo_environment_config():
    """Demonstrate environment configuration."""
    print("\n" + "=" * 60)
    print("4. ENVIRONMENT CONFIGURATION")
    print("=" * 60)

    # Show environment template
    print("\nEnvironment Template (.env):")
    print(ENV_TEMPLATE)

    # Config manager demo
    config = ConfigManager()
    config.display()

    # Validation
    missing = config.validate()
    if missing:
        print(f"\n⚠️  Missing required config: {', '.join(missing)}")
    else:
        print("\n✅ All required configuration present")


# ---------------------------------------------------------------------------
# 5. Basic Monitoring
# ---------------------------------------------------------------------------

class MetricsCollector:
    """Collect and expose metrics for monitoring."""

    def __init__(self):
        self.counters: dict[str, int] = defaultdict(int)
        self.gauges: dict[str, float] = {}
        self.histograms: dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.start_time = time.time()

    def increment(self, name: str, value: int = 1):
        """Increment a counter."""
        self.counters[name] += value

    def set_gauge(self, name: str, value: float):
        """Set a gauge value."""
        self.gauges[name] = value

    def observe(self, name: str, value: float):
        """Record a histogram observation."""
        self.histograms[name].append(value)

    def get_counter(self, name: str) -> int:
        """Get counter value."""
        return self.counters.get(name, 0)

    def get_gauge(self, name: str) -> float:
        """Get gauge value."""
        return self.gauges.get(name, 0.0)

    def get_histogram_stats(self, name: str) -> dict[str, float]:
        """Get histogram statistics."""
        values = list(self.histograms.get(name, []))
        if not values:
            return {"count": 0, "min": 0, "max": 0, "avg": 0, "p95": 0}

        values.sort()
        return {
            "count": len(values),
            "min": values[0],
            "max": values[-1],
            "avg": sum(values) / len(values),
            "p95": values[int(len(values) * 0.95)],
        }

    def export_prometheus(self) -> str:
        """Export metrics in Prometheus format."""
        lines = []

        # Counters
        for name, value in self.counters.items():
            lines.append(f"# TYPE {name} counter")
            lines.append(f"{name} {value}")

        # Gauges
        for name, value in self.gauges.items():
            lines.append(f"# TYPE {name} gauge")
            lines.append(f"{name} {value}")

        # Histograms
        for name, values in self.histograms.items():
            stats = self.get_histogram_stats(name)
            lines.append(f"# TYPE {name} histogram")
            lines.append(f"{name}_count {stats['count']}")
            lines.append(f"{name}_sum {sum(values)}")
            lines.append(f"{name}_bucket{{le=\"0.1\"}} {sum(1 for v in values if v <= 0.1)}")
            lines.append(f"{name}_bucket{{le=\"0.5\"}} {sum(1 for v in values if v <= 0.5)}")
            lines.append(f"{name}_bucket{{le=\"1.0\"}} {sum(1 for v in values if v <= 1.0)}")
            lines.append(f"{name}_bucket{{le=\"5.0\"}} {sum(1 for v in values if v <= 5.0)}")

        return "\n".join(lines)

    def get_summary(self) -> dict[str, Any]:
        """Get summary of all metrics."""
        uptime = time.time() - self.start_time
        return {
            "uptime_seconds": uptime,
            "counters": dict(self.counters),
            "gauges": dict(self.gauges),
            "histograms": {
                name: self.get_histogram_stats(name)
                for name in self.histograms
            },
        }


def demo_monitoring():
    """Demonstrate monitoring setup."""
    print("\n" + "=" * 60)
    print("5. BASIC MONITORING")
    print("=" * 60)

    collector = MetricsCollector()

    # Simulate some metrics
    collector.increment("requests_total")
    collector.increment("requests_total")
    collector.increment("requests_success")
    collector.set_gauge("active_connections", 5.0)
    collector.observe("request_latency_seconds", 0.25)
    collector.observe("request_latency_seconds", 0.35)
    collector.observe("request_latency_seconds", 0.45)

    # Get summary
    summary = collector.get_summary()
    print("\nMetrics Summary:")
    print(json.dumps(summary, indent=2))

    # Prometheus format
    print("\nPrometheus Format:")
    print(collector.export_prometheus())


# ---------------------------------------------------------------------------
# Main: Run All Demos
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("EXERCISE 07: AI DEPLOYMENT")
    print("=" * 60)

    create_fastapi_app()  # Just creates the app, doesn't run it
    print("FastAPI app created (see create_fastapi_app function)")

    generate_docker_files()
    demo_health_checks()
    demo_environment_config()
    demo_monitoring()

    print("\n" + "=" * 60)
    print("KEY TAKEAWAYS:")
    print("1. FastAPI provides async support ideal for AI services")
    print("2. Docker ensures consistent deployment across environments")
    print("3. Health checks enable automatic recovery and monitoring")
    print("4. Environment configuration keeps secrets secure")
    print("5. Metrics collection enables observability and alerting")
    print("=" * 60)
