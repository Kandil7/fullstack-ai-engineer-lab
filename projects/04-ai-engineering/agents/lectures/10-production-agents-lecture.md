# Lecture 10: Production Agents

## 🎯 Topic Overview

**Production agents** are AI agents deployed to real users in production environments. Moving from prototype to production requires addressing reliability, scalability, monitoring, and operational concerns.

This lecture covers:
- Production readiness checklist
- Deployment strategies
- Monitoring and observability
- Scaling considerations
- Incident response
- Cost optimization

---

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. **Assess** production readiness of an agent system
2. **Deploy** agents to production environments
3. **Monitor** agent performance and health
4. **Scale** agents to handle increased load
5. **Handle** incidents and failures gracefully
6. **Optimize** costs while maintaining quality
7. **Implement** CI/CD for agents
8. **Operate** agents reliably in production

---

## 🧩 Key Concepts

### 1. Production Readiness Checklist

```
┌─────────────────────────────────────────────────────────────┐
│              Production Readiness Checklist                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  RELIABILITY                                                │
│  □ Error handling implemented                               │
│  □ Graceful degradation working                            │
│  □ Timeouts configured                                     │
│  □ Retry logic in place                                    │
│  □ Circuit breakers active                                 │
│                                                             │
│  MONITORING                                                 │
│  □ Health checks implemented                               │
│  □ Metrics collection enabled                              │
│  □ Logging configured                                      │
│  □ Alerting set up                                         │
│  □ Dashboards created                                      │
│                                                             │
│  SCALABILITY                                                │
│  □ Load testing completed                                  │
│  □ Auto-scaling configured                                 │
│  □ Caching implemented                                     │
│  □ Database optimized                                      │
│                                                             │
│  SECURITY                                                   │
│  □ Authentication implemented                              │
│  □ Authorization enforced                                  │
│  □ Input validation active                                 │
│  □ Secrets management configured                           │
│  □ Rate limiting enabled                                   │
│                                                             │
│  OPERATIONS                                                 │
│  □ Deployment pipeline tested                              │
│  □ Rollback procedure documented                           │
│  □ Runbooks created                                        │
│  □ On-call rotation established                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. Production Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Production Agent Architecture                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   Load Balancer                      │   │
│  └────────────────────────┬────────────────────────────┘   │
│                           │                                 │
│         ┌─────────────────┼─────────────────┐              │
│         │                 │                 │              │
│         ▼                 ▼                 ▼              │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐      │
│  │   Agent     │   │   Agent     │   │   Agent     │      │
│  │  Instance 1 │   │  Instance 2 │   │  Instance 3 │      │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘      │
│         │                 │                 │              │
│         └─────────────────┼─────────────────┘              │
│                           │                                 │
│              ┌────────────┼────────────┐                   │
│              ▼            ▼            ▼                   │
│        ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│        │  Cache   │ │ Database │ │  Queue   │            │
│        └──────────┘ └──────────┘ └──────────┘            │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Monitoring & Observability               │   │
│  │  • Metrics  • Logs  • Traces  • Alerts               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 Code Examples

### Example 1: Production-Ready Agent

```python
"""
Production-Ready Agent Implementation
Includes all production concerns: monitoring, error handling, scaling.
"""
import time
import logging
import traceback
from typing import Any, Callable, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
import json
import hashlib
from datetime import datetime
from collections import deque
import threading


class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


@dataclass
class AgentMetrics:
    """Collects agent metrics."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_latency: float = 0.0
    request_history: deque = field(default_factory=lambda: deque(maxlen=1000))
    
    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 1.0
        return self.successful_requests / self.total_requests
    
    @property
    def avg_latency(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.total_latency / self.total_requests
    
    def record_request(self, success: bool, latency: float):
        self.total_requests += 1
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
        self.total_latency += latency
        self.request_history.append({
            "success": success,
            "latency": latency,
            "timestamp": time.time()
        })


class ProductionAgent:
    """
    Production-ready agent with all operational concerns.
    
    Features:
    - Comprehensive error handling
    - Metrics collection
    - Health checks
    - Request tracing
    - Graceful degradation
    - Caching
    """
    
    def __init__(self, name: str, core_agent: Callable,
                 config: Dict = None):
        self.name = name
        self.core_agent = core_agent
        self.config = config or {}
        
        # Metrics
        self.metrics = AgentMetrics()
        
        # Health
        self.health_status = HealthStatus.HEALTHY
        self.health_checks: Dict[str, Callable] = {}
        
        # Caching
        self.cache: Dict[str, Any] = {}
        self.cache_ttl = self.config.get("cache_ttl", 300)
        self.cache_timestamps: Dict[str, float] = {}
        
        # Circuit breaker
        self.failure_count = 0
        self.circuit_open = False
        self.circuit_threshold = self.config.get("circuit_threshold", 5)
        
        # Tracing
        self.traces: deque = deque(maxlen=1000)
        
        # Logging
        self.logger = logging.getLogger(f"agent.{name}")
        
        # Thread safety
        self._lock = threading.Lock()
    
    def process(self, input_data: Any, 
               request_id: str = None) -> Dict:
        """
        Process a request with full production handling.
        
        Returns:
            {
                "success": bool,
                "result": Any,
                "error": str,
                "request_id": str,
                "latency": float,
                "cached": bool
            }
        """
        request_id = request_id or self._generate_request_id()
        start_time = time.time()
        
        # Start trace
        trace = {
            "request_id": request_id,
            "start_time": start_time,
            "input_hash": self._hash_input(input_data),
            "steps": []
        }
        
        try:
            # Check circuit breaker
            if self.circuit_open:
                raise Exception("Circuit breaker is open - service unavailable")
            
            # Check cache
            cache_key = self._get_cache_key(input_data)
            cached_result = self._get_from_cache(cache_key)
            
            if cached_result is not None:
                trace["steps"].append({"step": "cache_hit", "time": time.time()})
                return self._build_response(
                    success=True,
                    result=cached_result,
                    request_id=request_id,
                    latency=time.time() - start_time,
                    cached=True,
                    trace=trace
                )
            
            # Process with core agent
            trace["steps"].append({"step": "core_agent_start", "time": time.time()})
            
            result = self.core_agent(input_data)
            
            trace["steps"].append({"step": "core_agent_complete", "time": time.time()})
            
            # Cache result
            self._set_cache(cache_key, result)
            
            # Reset circuit breaker on success
            with self._lock:
                self.failure_count = 0
            
            # Record success
            latency = time.time() - start_time
            self.metrics.record_request(True, latency)
            
            return self._build_response(
                success=True,
                result=result,
                request_id=request_id,
                latency=latency,
                cached=False,
                trace=trace
            )
            
        except Exception as e:
            # Record failure
            latency = time.time() - start_time
            self.metrics.record_request(False, latency)
            
            # Update circuit breaker
            with self._lock:
                self.failure_count += 1
                if self.failure_count >= self.circuit_threshold:
                    self.circuit_open = True
                    self.logger.error("Circuit breaker opened")
            
            # Log error
            self.logger.error(
                f"Request failed: {request_id}",
                exc_info=True
            )
            
            trace["steps"].append({
                "step": "error",
                "error": str(e),
                "time": time.time()
            })
            
            return self._build_response(
                success=False,
                result=None,
                error=str(e),
                request_id=request_id,
                latency=latency,
                trace=trace
            )
    
    def _generate_request_id(self) -> str:
        """Generate unique request ID."""
        return f"{self.name}_{int(time.time() * 1000)}_{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}"
    
    def _hash_input(self, input_data: Any) -> str:
        """Create hash of input for tracing."""
        return hashlib.md5(json.dumps(str(input_data)).encode()).hexdigest()[:16]
    
    def _get_cache_key(self, input_data: Any) -> str:
        """Generate cache key."""
        return hashlib.md5(json.dumps(str(input_data)).encode()).hexdigest()
    
    def _get_from_cache(self, key: str) -> Optional[Any]:
        """Get value from cache if valid."""
        if key in self.cache:
            if time.time() - self.cache_timestamps[key] < self.cache_ttl:
                return self.cache[key]
            else:
                # Expired
                del self.cache[key]
                del self.cache_timestamps[key]
        return None
    
    def _set_cache(self, key: str, value: Any):
        """Set value in cache."""
        with self._lock:
            self.cache[key] = value
            self.cache_timestamps[key] = time.time()
    
    def _build_response(self, success: bool, result: Any = None,
                       error: str = None, request_id: str = "",
                       latency: float = 0.0, cached: bool = False,
                       trace: Dict = None) -> Dict:
        """Build standardized response."""
        # Add trace to collection
        if trace:
            trace["end_time"] = time.time()
            trace["latency"] = latency
            trace["success"] = success
            self.traces.append(trace)
        
        return {
            "success": success,
            "result": result,
            "error": error,
            "request_id": request_id,
            "latency": latency,
            "cached": cached,
            "timestamp": datetime.now().isoformat()
        }
    
    def check_health(self) -> Dict:
        """Perform health check."""
        checks = {}
        
        # Check metrics
        checks["success_rate"] = {
            "status": "healthy" if self.metrics.success_rate > 0.95 else "degraded",
            "value": self.metrics.success_rate
        }
        
        checks["avg_latency"] = {
            "status": "healthy" if self.metrics.avg_latency < 1.0 else "degraded",
            "value": self.metrics.avg_latency
        }
        
        checks["circuit_breaker"] = {
            "status": "healthy" if not self.circuit_open else "unhealthy",
            "open": self.circuit_open
        }
        
        # Run custom health checks
        for name, check_fn in self.health_checks.items():
            try:
                result = check_fn()
                checks[name] = result
            except Exception as e:
                checks[name] = {"status": "error", "error": str(e)}
        
        # Determine overall status
        statuses = [c.get("status", "healthy") for c in checks.values()]
        
        if "unhealthy" in statuses or "error" in statuses:
            self.health_status = HealthStatus.UNHEALTHY
        elif "degraded" in statuses:
            self.health_status = HealthStatus.DEGRADED
        else:
            self.health_status = HealthStatus.HEALTHY
        
        return {
            "status": self.health_status.value,
            "checks": checks,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_metrics(self) -> Dict:
        """Get agent metrics."""
        return {
            "total_requests": self.metrics.total_requests,
            "successful_requests": self.metrics.successful_requests,
            "failed_requests": self.metrics.failed_requests,
            "success_rate": self.metrics.success_rate,
            "avg_latency": self.metrics.avg_latency,
            "circuit_breaker_open": self.circuit_open,
            "cache_size": len(self.cache)
        }
    
    def reset_circuit_breaker(self):
        """Manually reset circuit breaker."""
        with self._lock:
            self.failure_count = 0
            self.circuit_open = False
            self.logger.info("Circuit breaker manually reset")


class AgentMonitor:
    """
    Monitoring system for production agents.
    """
    
    def __init__(self):
        self.agents: Dict[str, ProductionAgent] = {}
        self.alerts: list = []
        self.alert_thresholds = {
            "success_rate": 0.95,
            "avg_latency": 2.0,
            "error_count": 100
        }
    
    def register_agent(self, agent: ProductionAgent):
        """Register an agent for monitoring."""
        self.agents[agent.name] = agent
    
    def check_all_agents(self) -> Dict:
        """Check health and metrics of all agents."""
        results = {}
        
        for name, agent in self.agents.items():
            health = agent.check_health()
            metrics = agent.get_metrics()
            
            results[name] = {
                "health": health,
                "metrics": metrics
            }
            
            # Check for alerts
            self._check_alerts(name, health, metrics)
        
        return results
    
    def _check_alerts(self, agent_name: str, health: Dict, 
                     metrics: Dict):
        """Check if any alert conditions are met."""
        # Success rate alert
        if metrics["success_rate"] < self.alert_thresholds["success_rate"]:
            self.alerts.append({
                "type": "low_success_rate",
                "agent": agent_name,
                "value": metrics["success_rate"],
                "threshold": self.alert_thresholds["success_rate"],
                "timestamp": datetime.now().isoformat()
            })
        
        # Latency alert
        if metrics["avg_latency"] > self.alert_thresholds["avg_latency"]:
            self.alerts.append({
                "type": "high_latency",
                "agent": agent_name,
                "value": metrics["avg_latency"],
                "threshold": self.alert_thresholds["avg_latency"],
                "timestamp": datetime.now().isoformat()
            })
        
        # Circuit breaker alert
        if metrics.get("circuit_breaker_open"):
            self.alerts.append({
                "type": "circuit_breaker_open",
                "agent": agent_name,
                "timestamp": datetime.now().isoformat()
            })
    
    def get_dashboard_data(self) -> Dict:
        """Get data for monitoring dashboard."""
        return {
            "agents": {
                name: {
                    "health": agent.health_status.value,
                    "metrics": agent.get_metrics()
                }
                for name, agent in self.agents.items()
            },
            "recent_alerts": self.alerts[-10:],
            "timestamp": datetime.now().isoformat()
        }


# === Usage Example ===

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create production agent
def core_processing(input_data):
    """Core agent logic."""
    time.sleep(0.1)  # Simulate processing
    return f"Processed: {input_data}"

agent = ProductionAgent(
    name="qa_agent",
    core_agent=core_processing,
    config={"cache_ttl": 60, "circuit_threshold": 3}
)

# Create monitor
monitor = AgentMonitor()
monitor.register_agent(agent)

# Process some requests
print("=== Processing Requests ===")
for i in range(5):
    result = agent.process(f"Question {i}")
    print(f"Request {i}: {'Success' if result['success'] else 'Failed'} "
          f"({result['latency']:.3f}s)")

# Check health
print("\n=== Health Check ===")
health = agent.check_health()
print(f"Status: {health['status']}")
for check, details in health['checks'].items():
    print(f"  {check}: {details.get('status', 'N/A')}")

# Get metrics
print("\n=== Metrics ===")
metrics = agent.get_metrics()
print(f"Total requests: {metrics['total_requests']}")
print(f"Success rate: {metrics['success_rate']:.1%}")
print(f"Avg latency: {metrics['avg_latency']:.3f}s")

# Dashboard data
print("\n=== Dashboard ===")
dashboard = monitor.get_dashboard_data()
print(json.dumps(dashboard, indent=2))
```

---

## ⚠️ Common Mistakes to Avoid

### Mistake 1: No Health Checks
```python
# ❌ BAD: Running blind
def agent_process(input):
    return core_agent(input)  # How do we know if it's working?

# ✅ GOOD: Regular health checks
@app.route("/health")
def health_check():
    return {
        "status": agent.health_status.value,
        "metrics": agent.get_metrics()
    }
```

### Mistake 2: No Circuit Breaker
```python
# ❌ BAD: Hammering failing service
def call_api():
    while True:
        try:
            return api.call()  # Keeps retrying forever!
        except:
            continue

# ✅ GOOD: Circuit breaker stops calling
if circuit_breaker.is_open:
    return fallback_response()
```

### Mistake 3: Missing Metrics
```python
# ❌ BAD: No visibility
def process(input):
    return agent(input)  # Can't measure performance

# ✅ GOOD: Track everything
def process(input):
    start = time.time()
    result = agent(input)
    latency = time.time() - start
    
    metrics.record("success" if result else "failure", latency)
    return result
```

---

## ✅ Best Practices

1. **Monitor Everything**: Track metrics, logs, and traces
2. **Health Checks**: Implement and expose health endpoints
3. **Circuit Breakers**: Prevent cascade failures
4. **Graceful Degradation**: Return partial results when possible
5. **Caching**: Reduce latency and API costs
6. **Rate Limiting**: Protect against abuse
7. **Alerting**: Get notified of issues proactively
8. **Documentation**: Runbooks for common incidents

---

## 🏋️ Practice Exercises

### Exercise 1: Deploy an Agent
Take an existing agent and make it production-ready with health checks, metrics, and error handling.

### Exercise 2: Build Monitoring
Create a monitoring dashboard that shows agent health and metrics.

### Exercise 3: Incident Response
Write a runbook for handling common agent failures.

---

## 📝 Summary

| Production Concern | Solution |
|-------------------|----------|
| **Reliability** | Error handling, retries, circuit breakers |
| **Observability** | Metrics, logging, tracing |
| **Scalability** | Caching, load balancing, auto-scaling |
| **Security** | Auth, validation, rate limiting |
| **Operations** | CI/CD, runbooks, alerting |

---

## 🎉 Course Complete!

Congratulations on completing the AI Agents lecture series! You now have a comprehensive understanding of:

1. Agent fundamentals
2. Tool calling
3. Agent memory
4. ReAct pattern
5. Planning & reasoning
6. Multi-agent orchestration
7. Agent communication
8. Agent evaluation
9. Agent safety
10. Production agents

**Next Steps:**
- Build your own agents
- Contribute to open-source agent frameworks
- Stay updated with the latest research
- Share your knowledge with others
