"""
=============================================================
Exercise 10: Production Agents
=============================================================

Topic Overview:
Deploying AI agents to production requires careful consideration
of scalability, reliability, and observability. This exercise covers:

1. FastAPI Agent Service - Building production-ready APIs
2. Agent Deployment Patterns - Various deployment strategies
3. Monitoring and Observability - Tracking agent performance
4. Scaling Strategies - Handling load and growth
5. Error Recovery - Graceful degradation and retry logic

Key Concepts:
- Production requires monitoring, logging, and alerting
- Horizontal scaling enables handling more load
- Circuit breakers prevent cascade failures
- Health checks enable orchestration
- Graceful degradation maintains availability

Prerequisites:
- Understanding of FastAPI/web frameworks
- Familiarity with async programming
=============================================================
"""

import asyncio
import json
import time
import uuid
import random
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from functools import wraps
import hashlib
import statistics


# ============================================================
# Core Data Structures
# ============================================================

class ServiceStatus(Enum):
    """Health status of a service."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    STOPPED = "stopped"


class CircuitState(Enum):
    """States for circuit breaker pattern."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery


@dataclass
class HealthCheck:
    """Health check result."""
    status: ServiceStatus
    components: Dict[str, Dict[str, Any]]
    timestamp: datetime = field(default_factory=datetime.now)
    uptime_seconds: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status.value,
            "components": self.components,
            "timestamp": self.timestamp.isoformat(),
            "uptime_seconds": self.uptime_seconds
        }


@dataclass
class RequestMetrics:
    """Metrics for a single request."""
    request_id: str
    endpoint: str
    method: str
    status_code: int
    latency_ms: float
    tokens_used: int = 0
    cost_usd: float = 0.0
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class AgentConfig:
    """Configuration for an agent service."""
    agent_id: str
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 1000
    temperature: float = 0.7
    timeout_seconds: int = 30
    max_retries: int = 3
    rate_limit_per_minute: int = 60
    enable_streaming: bool = True
    enable_caching: bool = True


# ============================================================
# Example 1: FastAPI Agent Service
# ============================================================

class AgentService:
    """
    Production-ready agent service with FastAPI-like patterns.
    
    Features:
    - Async request handling
    - Streaming responses
    - Request validation
    - Error handling
    - Health checks
    """

    def __init__(self, config: AgentConfig):
        self.config = config
        self.start_time = datetime.now()
        self.request_count = 0
        self.error_count = 0
        self.cache: Dict[str, Any] = {}
        self.active_requests: Dict[str, asyncio.Task] = {}
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Set up structured logging."""
        logger = logging.getLogger(f"agent_service.{self.config.agent_id}")
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    async def process_request(
        self,
        request_id: str,
        prompt: str,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Process a chat completion request."""
        start_time = time.time()
        self.request_count += 1

        self.logger.info(f"Processing request {request_id}")

        try:
            # Check cache if enabled
            if self.config.enable_caching:
                cache_key = self._get_cache_key(prompt, context)
                if cache_key in self.cache:
                    self.logger.info(f"Cache hit for request {request_id}")
                    return self.cache[cache_key]

            # Validate input
            if not prompt or len(prompt) > 10000:
                raise ValueError("Invalid prompt length")

            # Process with model (simulated)
            result = await self._call_model(prompt, context)

            # Cache result
            if self.config.enable_caching:
                self.cache[cache_key] = result

            latency_ms = (time.time() - start_time) * 1000
            result["latency_ms"] = latency_ms

            self.logger.info(
                f"Request {request_id} completed in {latency_ms:.1f}ms"
            )

            return result

        except asyncio.TimeoutError:
            self.error_count += 1
            self.logger.error(f"Request {request_id} timed out")
            return {
                "error": "Request timeout",
                "request_id": request_id
            }
        except Exception as e:
            self.error_count += 1
            self.logger.error(f"Request {request_id} failed: {e}")
            return {
                "error": str(e),
                "request_id": request_id
            }

    async def _call_model(
        self,
        prompt: str,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Call the language model (simulated)."""
        # Simulate API call with variable latency
        await asyncio.sleep(random.uniform(0.1, 0.5))

        # Simulate occasional failures
        if random.random() < 0.05:
            raise Exception("Model API error")

        # Simulate response
        input_tokens = len(prompt.split()) * 2
        output_tokens = random.randint(50, 200)

        return {
            "id": str(uuid.uuid4())[:8],
            "model": self.config.model,
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": f"Response to: {prompt[:50]}..."
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": input_tokens,
                "completion_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens
            },
            "created": int(time.time())
        }

    def _get_cache_key(
        self,
        prompt: str,
        context: Optional[Dict]
    ) -> str:
        """Generate cache key for request."""
        content = prompt + json.dumps(context or {}, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    async def stream_response(
        self,
        prompt: str,
        context: Optional[Dict] = None
    ) -> AsyncGenerator:
        """Stream response tokens."""
        # Simulate streaming
        words = f"Streaming response to: {prompt[:30]}...".split()

        for word in words:
            await asyncio.sleep(0.05)
            yield {
                "choices": [{
                    "delta": {"content": word + " "},
                    "finish_reason": None
                }]
            }

        # Final chunk
        yield {
            "choices": [{
                "delta": {},
                "finish_reason": "stop"
            }]
        }

    async def health_check(self) -> HealthCheck:
        """Perform health check."""
        components = {
            "model_api": {
                "status": "healthy",
                "latency_ms": random.uniform(10, 50)
            },
            "cache": {
                "status": "healthy",
                "size": len(self.cache),
                "hit_rate": 0.85
            },
            "memory": {
                "status": "healthy",
                "used_mb": random.uniform(100, 500)
            }
        }

        # Determine overall status
        unhealthy_count = sum(
            1 for c in components.values()
            if c["status"] != "healthy"
        )

        if unhealthy_count == 0:
            status = ServiceStatus.HEALTHY
        elif unhealthy_count <= 1:
            status = ServiceStatus.DEGRADED
        else:
            status = ServiceStatus.UNHEALTHY

        uptime = (datetime.now() - self.start_time).total_seconds()

        return HealthCheck(
            status=status,
            components=components,
            uptime_seconds=uptime
        )

    def get_metrics(self) -> Dict[str, Any]:
        """Get service metrics."""
        uptime = (datetime.now() - self.start_time).total_seconds()
        return {
            "agent_id": self.config.agent_id,
            "uptime_seconds": uptime,
            "total_requests": self.request_count,
            "error_count": self.error_count,
            "error_rate": self.error_count / max(self.request_count, 1),
            "cache_size": len(self.cache),
            "active_requests": len(self.active_requests)
        }


# Need to add AsyncGenerator import for streaming
from typing import AsyncGenerator


# ============================================================
# Example 2: Agent Deployment Patterns
# ============================================================

class DeploymentManager:
    """
    Manages agent deployment and lifecycle.
    
    Patterns:
    - Blue-green deployment
    - Canary deployment
    - Rolling updates
    """

    def __init__(self):
        self.deployments: Dict[str, Dict] = {}
        self.history: List[Dict] = []

    def create_deployment(
        self,
        agent_id: str,
        version: str,
        config: Dict[str, Any]
    ) -> Dict:
        """Create a new deployment."""
        deployment = {
            "deployment_id": str(uuid.uuid4())[:8],
            "agent_id": agent_id,
            "version": version,
            "config": config,
            "status": "created",
            "created_at": datetime.now().isoformat(),
            "instances": 0,
            "traffic_percent": 0
        }
        self.deployments[deployment["deployment_id"]] = deployment
        return deployment

    def blue_green_deploy(
        self,
        agent_id: str,
        new_version: str
    ) -> Dict:
        """
        Blue-green deployment pattern.
        
        Deploys new version alongside old, then switches traffic.
        """
        print(f"\n  Blue-Green Deploy: {agent_id} v{new_version}")

        # Find existing deployment
        existing = None
        for dep in self.deployments.values():
            if dep["agent_id"] == agent_id and dep["status"] == "active":
                existing = dep
                break

        # Create green (new) deployment
        green = self.create_deployment(
            agent_id, new_version,
            {"strategy": "blue-green", "color": "green"}
        )
        green["status"] = "deploying"
        green["instances"] = 3

        print(f"    Created green deployment: {green['deployment_id']}")

        # Simulate deployment
        green["status"] = "active"
        green["traffic_percent"] = 100

        # Switch traffic
        if existing:
            existing["traffic_percent"] = 0
            existing["status"] = "stopped"
            print(f"    Stopped blue deployment: {existing['deployment_id']}")

        self.history.append({
            "action": "blue_green_deploy",
            "deployment_id": green["deployment_id"],
            "timestamp": datetime.now().isoformat()
        })

        return green

    def canary_deploy(
        self,
        agent_id: str,
        new_version: str,
        traffic_percent: int = 10
    ) -> Dict:
        """
        Canary deployment pattern.
        
        Gradually increases traffic to new version.
        """
        print(f"\n  Canary Deploy: {agent_id} v{new_version} ({traffic_percent}%)")

        canary = self.create_deployment(
            agent_id, new_version,
            {"strategy": "canary", "traffic_percent": traffic_percent}
        )
        canary["status"] = "active"
        canary["traffic_percent"] = traffic_percent
        canary["instances"] = 1

        # Reduce traffic to existing
        for dep in self.deployments.values():
            if (dep["agent_id"] == agent_id and
                dep["deployment_id"] != canary["deployment_id"] and
                dep["status"] == "active"):
                dep["traffic_percent"] = 100 - traffic_percent
                print(f"    Reduced traffic to {dep['deployment_id']}: "
                      f"{dep['traffic_percent']}%")

        self.history.append({
            "action": "canary_deploy",
            "deployment_id": canary["deployment_id"],
            "traffic_percent": traffic_percent,
            "timestamp": datetime.now().isoformat()
        })

        return canary

    def rolling_update(
        self,
        agent_id: str,
        new_version: str,
        batch_size: int = 1
    ) -> Dict:
        """
        Rolling update pattern.
        
        Updates instances one batch at a time.
        """
        print(f"\n  Rolling Update: {agent_id} v{new_version} (batch={batch_size})")

        rolling = self.create_deployment(
            agent_id, new_version,
            {"strategy": "rolling", "batch_size": batch_size}
        )
        rolling["status"] = "deploying"

        # Simulate rolling update
        total_instances = 5
        for batch in range(0, total_instances, batch_size):
            updated = min(batch + batch_size, total_instances)
            print(f"    Updated {updated}/{total_instances} instances")
            rolling["instances"] = updated

        rolling["status"] = "active"
        rolling["traffic_percent"] = 100

        self.history.append({
            "action": "rolling_update",
            "deployment_id": rolling["deployment_id"],
            "total_instances": total_instances,
            "timestamp": datetime.now().isoformat()
        })

        return rolling

    def rollback(self, deployment_id: str) -> Dict:
        """Rollback a deployment."""
        deployment = self.deployments.get(deployment_id)
        if not deployment:
            raise ValueError(f"Deployment {deployment_id} not found")

        print(f"\n  Rolling back deployment: {deployment_id}")

        deployment["status"] = "rolled_back"
        deployment["traffic_percent"] = 0

        # Restore previous version
        for dep in self.deployments.values():
            if (dep["agent_id"] == deployment["agent_id"] and
                dep["deployment_id"] != deployment_id and
                dep["status"] in ["stopped", "active"]):
                dep["status"] = "active"
                dep["traffic_percent"] = 100
                print(f"    Restored: {dep['deployment_id']}")
                break

        self.history.append({
            "action": "rollback",
            "deployment_id": deployment_id,
            "timestamp": datetime.now().isoformat()
        })

        return deployment


# ============================================================
# Example 3: Monitoring and Observability
# ============================================================

class MetricsCollector:
    """
    Collects and aggregates metrics for agent monitoring.
    
    Metrics:
    - Request count and rate
    - Latency (p50, p95, p99)
    - Error rate
    - Token usage
    - Cost
    """

    def __init__(self, window_size: int = 1000):
        self.window_size = window_size
        self.metrics: deque = deque(maxlen=window_size)
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, List[float]] = defaultdict(list)

    def record_request(self, metrics: RequestMetrics) -> None:
        """Record request metrics."""
        self.metrics.append(metrics)
        self.counters["total_requests"] += 1
        self.counters[f"status_{metrics.status_code}"] += 1

        if metrics.error:
            self.counters["total_errors"] += 1

        # Record latency
        self.histograms["latency_ms"].append(metrics.latency_ms)

        # Record tokens
        self.counters["total_tokens"] += metrics.tokens_used

        # Record cost
        self.gauges["total_cost"] = self.gauges.get("total_cost", 0) + metrics.cost_usd

    def get_latency_percentiles(self) -> Dict[str, float]:
        """Get latency percentiles."""
        latencies = self.histograms.get("latency_ms", [])
        if not latencies:
            return {}

        sorted_latencies = sorted(latencies)
        n = len(sorted_latencies)

        return {
            "p50": sorted_latencies[int(n * 0.5)],
            "p75": sorted_latencies[int(n * 0.75)],
            "p90": sorted_latencies[int(n * 0.90)],
            "p95": sorted_latencies[int(n * 0.95)],
            "p99": sorted_latencies[int(n * 0.99)],
            "mean": statistics.mean(sorted_latencies)
        }

    def get_error_rate(self) -> float:
        """Calculate error rate."""
        total = self.counters.get("total_requests", 0)
        errors = self.counters.get("total_errors", 0)
        return errors / total if total > 0 else 0

    def get_throughput(self, window_seconds: int = 60) -> float:
        """Calculate requests per second."""
        if not self.metrics:
            return 0

        now = datetime.now()
        cutoff = now - timedelta(seconds=window_seconds)

        recent = [
            m for m in self.metrics
            if m.timestamp >= cutoff
        ]

        return len(recent) / window_seconds

    def get_summary(self) -> Dict[str, Any]:
        """Get comprehensive metrics summary."""
        return {
            "total_requests": self.counters.get("total_requests", 0),
            "total_errors": self.counters.get("total_errors", 0),
            "error_rate": self.get_error_rate(),
            "latency": self.get_latency_percentiles(),
            "throughput_rps": self.get_throughput(),
            "total_tokens": self.counters.get("total_tokens", 0),
            "total_cost": self.gauges.get("total_cost", 0),
            "timestamp": datetime.now().isoformat()
        }


class DistributedTracer:
    """
    Distributed tracing for tracking requests across services.
    """

    def __init__(self):
        self.traces: Dict[str, List[Dict]] = defaultdict(list)

    def start_trace(self, trace_id: str, span_name: str) -> str:
        """Start a new trace span."""
        span_id = str(uuid.uuid4())[:8]
        self.traces[trace_id].append({
            "span_id": span_id,
            "span_name": span_name,
            "start_time": time.time(),
            "end_time": None,
            "status": "in_progress",
            "attributes": {}
        })
        return span_id

    def end_trace(self, trace_id: str, span_id: str, status: str = "ok") -> None:
        """End a trace span."""
        for span in self.traces.get(trace_id, []):
            if span["span_id"] == span_id:
                span["end_time"] = time.time()
                span["status"] = status
                break

    def add_attribute(
        self,
        trace_id: str,
        span_id: str,
        key: str,
        value: Any
    ) -> None:
        """Add attribute to a span."""
        for span in self.traces.get(trace_id, []):
            if span["span_id"] == span_id:
                span["attributes"][key] = value
                break

    def get_trace(self, trace_id: str) -> List[Dict]:
        """Get all spans for a trace."""
        return self.traces.get(trace_id, [])

    def get_trace_duration(self, trace_id: str) -> Optional[float]:
        """Get total duration of a trace in milliseconds."""
        spans = self.traces.get(trace_id, [])
        if not spans:
            return None

        starts = [s["start_time"] for s in spans if s["start_time"]]
        ends = [s["end_time"] for s in spans if s["end_time"]]

        if not starts or not ends:
            return None

        return (max(ends) - min(starts)) * 1000


class AlertManager:
    """
    Manages alerts based on metrics thresholds.
    """

    def __init__(self):
        self.rules: List[Dict] = []
        self.active_alerts: List[Dict] = []
        self.alert_history: List[Dict] = []

    def add_rule(
        self,
        name: str,
        condition: Callable[[Dict], bool],
        severity: str = "warning",
        message_template: str = ""
    ) -> None:
        """Add an alert rule."""
        self.rules.append({
            "name": name,
            "condition": condition,
            "severity": severity,
            "message_template": message_template,
            "created_at": datetime.now().isoformat()
        })

    def evaluate(self, metrics: Dict[str, Any]) -> List[Dict]:
        """Evaluate all rules against current metrics."""
        new_alerts = []

        for rule in self.rules:
            try:
                if rule["condition"](metrics):
                    alert = {
                        "alert_id": str(uuid.uuid4())[:8],
                        "rule": rule["name"],
                        "severity": rule["severity"],
                        "message": rule["message_template"],
                        "metrics": metrics,
                        "timestamp": datetime.now().isoformat()
                    }
                    new_alerts.append(alert)
                    self.active_alerts.append(alert)
            except Exception as e:
                print(f"  Alert rule error: {e}")

        return new_alerts

    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an active alert."""
        for i, alert in enumerate(self.active_alerts):
            if alert["alert_id"] == alert_id:
                resolved = self.active_alerts.pop(i)
                resolved["resolved_at"] = datetime.now().isoformat()
                self.alert_history.append(resolved)
                return True
        return False

    def get_active_alerts(self) -> List[Dict]:
        """Get all active alerts."""
        return self.active_alerts


# ============================================================
# Example 4: Scaling Strategies
# ============================================================

class LoadBalancer:
    """
    Load balancer for distributing requests across instances.
    
    Strategies:
    - Round robin
    - Least connections
    - Weighted random
    """

    def __init__(self, strategy: str = "round_robin"):
        self.strategy = strategy
        self.instances: Dict[str, Dict] = {}
        self.current_index = 0

    def register_instance(
        self,
        instance_id: str,
        weight: int = 1,
        max_connections: int = 100
    ) -> None:
        """Register a backend instance."""
        self.instances[instance_id] = {
            "weight": weight,
            "max_connections": max_connections,
            "current_connections": 0,
            "total_requests": 0,
            "healthy": True
        }

    def remove_instance(self, instance_id: str) -> None:
        """Remove a backend instance."""
        self.instances.pop(instance_id, None)

    def get_instance(self) -> Optional[str]:
        """Get the next instance based on strategy."""
        healthy = {
            k: v for k, v in self.instances.items()
            if v["healthy"]
        }

        if not healthy:
            return None

        if self.strategy == "round_robin":
            return self._round_robin(healthy)
        elif self.strategy == "least_connections":
            return self._least_connections(healthy)
        elif self.strategy == "weighted_random":
            return self._weighted_random(healthy)
        else:
            return self._round_robin(healthy)

    def _round_robin(self, instances: Dict[str, Dict]) -> str:
        """Round robin selection."""
        instance_ids = list(instances.keys())
        instance = instance_ids[self.current_index % len(instance_ids)]
        self.current_index += 1
        return instance

    def _least_connections(self, instances: Dict[str, Dict]) -> str:
        """Select instance with fewest connections."""
        return min(
            instances.keys(),
            key=lambda x: instances[x]["current_connections"]
        )

    def _weighted_random(self, instances: Dict[str, Dict]) -> str:
        """Weighted random selection."""
        weights = [instances[i]["weight"] for i in instances.keys()]
        total = sum(weights)
        r = random.uniform(0, total)

        cumulative = 0
        for instance_id, weight in zip(instances.keys(), weights):
            cumulative += weight
            if r <= cumulative:
                return instance_id

        return list(instances.keys())[-1]

    def record_request(self, instance_id: str, start: bool = True) -> None:
        """Record request start/end for an instance."""
        if instance_id in self.instances:
            if start:
                self.instances[instance_id]["current_connections"] += 1
                self.instances[instance_id]["total_requests"] += 1
            else:
                self.instances[instance_id]["current_connections"] = max(
                    0, self.instances[instance_id]["current_connections"] - 1
                )

    def get_status(self) -> Dict[str, Any]:
        """Get load balancer status."""
        return {
            "strategy": self.strategy,
            "instances": {
                k: {
                    "healthy": v["healthy"],
                    "connections": v["current_connections"],
                    "total_requests": v["total_requests"]
                }
                for k, v in self.instances.items()
            }
        }


class AutoScaler:
    """
    Automatic scaling based on metrics.
    """

    def __init__(
        self,
        min_instances: int = 2,
        max_instances: int = 10,
        target_cpu_percent: float = 70.0,
        scale_up_threshold: float = 0.8,
        scale_down_threshold: float = 0.3
    ):
        self.min_instances = min_instances
        self.max_instances = max_instances
        self.target_cpu_percent = target_cpu_percent
        self.scale_up_threshold = scale_up_threshold
        self.scale_down_threshold = scale_down_threshold
        self.current_instances = min_instances
        self.scaling_history: List[Dict] = []

    def evaluate(self, metrics: Dict[str, float]) -> int:
        """
        Evaluate metrics and return desired instance count.
        
        Returns:
            Desired number of instances
        """
        cpu_percent = metrics.get("cpu_percent", 50)
        request_rate = metrics.get("request_rate", 0)
        latency_p95 = metrics.get("latency_p95", 100)

        desired = self.current_instances

        # Scale up conditions
        if cpu_percent > self.target_cpu_percent * self.scale_up_threshold:
            desired = min(self.current_instances + 1, self.max_instances)
        elif latency_p95 > 1000:  # High latency
            desired = min(self.current_instances + 1, self.max_instances)

        # Scale down conditions
        if cpu_percent < self.target_cpu_percent * self.scale_down_threshold:
            desired = max(self.current_instances - 1, self.min_instances)

        # Record scaling decision
        if desired != self.current_instances:
            self.scaling_history.append({
                "from": self.current_instances,
                "to": desired,
                "reason": {
                    "cpu": cpu_percent,
                    "latency_p95": latency_p95
                },
                "timestamp": datetime.now().isoformat()
            })
            self.current_instances = desired

        return desired

    def get_status(self) -> Dict[str, Any]:
        """Get auto scaler status."""
        return {
            "current_instances": self.current_instances,
            "min_instances": self.min_instances,
            "max_instances": self.max_instances,
            "scaling_events": len(self.scaling_history),
            "last_scaling": self.scaling_history[-1] if self.scaling_history else None
        }


# ============================================================
# Example 5: Error Recovery
# ============================================================

class CircuitBreaker:
    """
    Circuit breaker pattern for fault tolerance.
    
    States:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Failing, requests are rejected
    - HALF_OPEN: Testing if service recovered
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        half_open_max_calls: int = 3
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[float] = None
        self.half_open_calls = 0

    async def call(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """Execute a function with circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                self.half_open_calls = 0
            else:
                raise Exception("Circuit breaker is OPEN")

        if self.state == CircuitState.HALF_OPEN:
            if self.half_open_calls >= self.half_open_max_calls:
                raise Exception("Circuit breaker HALF_OPEN limit reached")
            self.half_open_calls += 1

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self) -> None:
        """Handle successful call."""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.half_open_max_calls:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
        elif self.state == CircuitState.CLOSED:
            self.failure_count = max(0, self.failure_count - 1)

    def _on_failure(self) -> None:
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
        elif self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def _should_attempt_reset(self) -> bool:
        """Check if we should attempt to reset the circuit."""
        if self.last_failure_time is None:
            return True
        return (time.time() - self.last_failure_time) > self.recovery_timeout

    def get_state(self) -> Dict[str, Any]:
        """Get circuit breaker state."""
        return {
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "last_failure": self.last_failure_time
        }


class RetryHandler:
    """
    Retry handler with exponential backoff.
    """

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 30.0,
        exponential_base: float = 2.0
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.retry_history: List[Dict] = []

    async def execute(
        self,
        func: Callable,
        *args,
        retryable_exceptions: Tuple = (Exception,),
        **kwargs
    ) -> Any:
        """Execute with retry logic."""
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                result = await func(*args, **kwargs)
                if attempt > 0:
                    self.retry_history.append({
                        "attempt": attempt,
                        "success": True,
                        "timestamp": datetime.now().isoformat()
                    })
                return result
            except retryable_exceptions as e:
                last_exception = e

                if attempt < self.max_retries:
                    delay = self._calculate_delay(attempt)
                    self.retry_history.append({
                        "attempt": attempt,
                        "success": False,
                        "error": str(e),
                        "retry_in": delay,
                        "timestamp": datetime.now().isoformat()
                    })
                    await asyncio.sleep(delay)

        raise last_exception

    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay with exponential backoff and jitter."""
        delay = self.base_delay * (self.exponential_base ** attempt)
        delay = min(delay, self.max_delay)
        # Add jitter
        delay *= random.uniform(0.5, 1.5)
        return delay

    def get_stats(self) -> Dict[str, Any]:
        """Get retry statistics."""
        if not self.retry_history:
            return {"total_retries": 0}

        total = len(self.retry_history)
        successes = sum(1 for r in self.retry_history if r["success"])

        return {
            "total_retries": total,
            "successful_retries": successes,
            "success_rate": successes / total if total > 0 else 0
        }


class GracefulDegradation:
    """
    Graceful degradation when services are unavailable.
    """

    def __init__(self):
        self.fallbacks: Dict[str, Callable] = {}
        self.degraded_mode = False
        self.fallback_history: List[Dict] = []

    def register_fallback(
        self,
        service_name: str,
        fallback_fn: Callable
    ) -> None:
        """Register a fallback function for a service."""
        self.fallbacks[service_name] = fallback_fn

    async def execute(
        self,
        service_name: str,
        primary_fn: Callable,
        *args,
        **kwargs
    ) -> Any:
        """Execute with graceful degradation."""
        try:
            return await primary_fn(*args, **kwargs)
        except Exception as e:
            self.degraded_mode = True
            self.fallback_history.append({
                "service": service_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })

            if service_name in self.fallbacks:
                return await self.fallbacks[service_name](*args, **kwargs)
            raise

    def get_status(self) -> Dict[str, Any]:
        """Get degradation status."""
        return {
            "degraded_mode": self.degraded_mode,
            "fallbacks_registered": list(self.fallbacks.keys()),
            "fallback_count": len(self.fallback_history),
            "last_fallback": self.fallback_history[-1] if self.fallback_history else None
        }


# ============================================================
# Example 6: Complete Production System
# ============================================================

class ProductionAgentSystem:
    """Complete production agent system combining all components."""

    def __init__(self):
        self.config = AgentConfig(
            agent_id="production_agent",
            model="gpt-3.5-turbo",
            max_tokens=1000,
            timeout_seconds=30
        )
        self.service = AgentService(self.config)
        self.deployment_manager = DeploymentManager()
        self.metrics = MetricsCollector()
        self.tracer = DistributedTracer()
        self.alert_manager = AlertManager()
        self.load_balancer = LoadBalancer(strategy="least_connections")
        self.auto_scaler = AutoScaler()
        self.circuit_breaker = CircuitBreaker()
        self.retry_handler = RetryHandler()
        self.degradation = GracefulDegradation()

        self._setup_alerts()
        self._setup_fallbacks()

    def _setup_alerts(self) -> None:
        """Set up alert rules."""
        self.alert_manager.add_rule(
            "high_error_rate",
            lambda m: m.get("error_rate", 0) > 0.1,
            severity="critical",
            message_template="Error rate exceeds 10%"
        )

        self.alert_manager.add_rule(
            "high_latency",
            lambda m: m.get("latency_p95", 0) > 2000,
            severity="warning",
            message_template="P95 latency exceeds 2 seconds"
        )

        self.alert_manager.add_rule(
            "low_throughput",
            lambda m: m.get("throughput_rps", 100) < 10,
            severity="warning",
            message_template="Throughput below 10 RPS"
        )

    def _setup_fallbacks(self) -> None:
        """Set up fallback functions."""
        async def model_fallback(*args, **kwargs):
            return {
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": "I'm currently experiencing high load. Please try again shortly."
                    }
                }],
                "usage": {"total_tokens": 0}
            }

        self.degradation.register_fallback("model_api", model_fallback)

    async def process_request(
        self,
        request_id: str,
        prompt: str
    ) -> Dict[str, Any]:
        """Process a request with full production safeguards."""
        trace_id = str(uuid.uuid4())[:8]
        span_id = self.tracer.start_trace(trace_id, "process_request")

        start_time = time.time()

        try:
            # Get instance from load balancer
            instance_id = self.load_balancer.get_instance()
            if not instance_id:
                raise Exception("No healthy instances available")

            self.load_balancer.record_request(instance_id, start=True)

            # Execute with circuit breaker
            result = await self.circuit_breaker.call(
                self.service.process_request,
                request_id,
                prompt
            )

            # Record metrics
            latency_ms = (time.time() - start_time) * 1000
            self.metrics.record_request(RequestMetrics(
                request_id=request_id,
                endpoint="/chat",
                method="POST",
                status_code=200,
                latency_ms=latency_ms,
                tokens_used=result.get("usage", {}).get("total_tokens", 0)
            ))

            self.load_balancer.record_request(instance_id, start=False)
            self.tracer.end_trace(trace_id, span_id, "ok")

            return result

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            self.metrics.record_request(RequestMetrics(
                request_id=request_id,
                endpoint="/chat",
                method="POST",
                status_code=500,
                latency_ms=latency_ms,
                error=str(e)
            ))

            self.tracer.end_trace(trace_id, span_id, "error")

            # Try degraded mode
            return await self.degradation.execute(
                "model_api",
                self.service.process_request,
                request_id,
                prompt
            )

    async def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check."""
        service_health = await self.service.health_check()

        return {
            "service": service_health.to_dict(),
            "load_balancer": self.load_balancer.get_status(),
            "auto_scaler": self.auto_scaler.get_status(),
            "circuit_breaker": self.circuit_breaker.get_state(),
            "degradation": self.degradation.get_status(),
            "alerts": self.alert_manager.get_active_alerts()
        }

    async def run_demo(self) -> None:
        """Run a demonstration of the production system."""
        print("\n" + "="*60)
        print("PRODUCTION AGENT SYSTEM DEMO")
        print("="*60)

        # Register instances
        for i in range(3):
            self.load_balancer.register_instance(
                f"instance_{i}",
                weight=i + 1
            )

        # Create deployment
        deployment = self.deployment_manager.create_deployment(
            "production_agent",
            "1.0.0",
            {"model": "gpt-3.5-turbo"}
        )
        deployment["status"] = "active"
        deployment["traffic_percent"] = 100
        deployment["instances"] = 3

        print("\n--- Processing Requests ---")
        for i in range(5):
            result = await self.process_request(
                f"req_{i}",
                f"Test prompt {i}"
            )
            print(f"  Request {i}: {'success' if 'error' not in result else 'error'}")

        # Print metrics
        print("\n--- Metrics Summary ---")
        metrics = self.metrics.get_summary()
        print(f"  Total Requests: {metrics['total_requests']}")
        print(f"  Error Rate: {metrics['error_rate']:.1%}")
        if metrics.get('latency'):
            print(f"  P95 Latency: {metrics['latency'].get('p95', 0):.1f}ms")

        # Health check
        print("\n--- Health Check ---")
        health = await self.health_check()
        print(f"  Service Status: {health['service']['status']}")
        print(f"  Circuit Breaker: {health['circuit_breaker']['state']}")

        # Auto scaler evaluation
        print("\n--- Auto Scaler ---")
        desired = self.auto_scaler.evaluate({
            "cpu_percent": 75,
            "latency_p95": 800
        })
        print(f"  Desired Instances: {desired}")

        # Deployment demo
        print("\n--- Blue-Green Deployment ---")
        self.deployment_manager.blue_green_deploy("production_agent", "1.1.0")

        print("\n" + "="*60)
        print("DEMO COMPLETE")
        print("="*60)


# ============================================================
# Main Entry Point
# ============================================================

async def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("EXERCISE 10: PRODUCTION AGENTS")
    print("="*60)

    system = ProductionAgentSystem()
    await system.run_demo()


if __name__ == "__main__":
    asyncio.run(main())
