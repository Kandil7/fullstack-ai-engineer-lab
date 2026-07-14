# Glossary: Production Agents

> Terms defined in alphabetical order.

---

## Quick Reference Table

| Term | One-Line Definition | See Also |
|------|---------------------|----------|
| Alert | Notification of an issue | Monitoring |
| Auto-scaling | Automatic capacity adjustment | Scaling |
| Circuit Breaker | Pattern to stop calling failing services | Resilience |
| Dashboard | Visual display of metrics | Monitoring |
| Deployment | Making agent available to users | Release |
| Fallback | Alternative when primary fails | Resilience |
| Health Check | Test of agent operational status | Monitoring |
| Incident | Unexpected system disruption | Outage |
| Latency | Time to complete a request | Performance |
| Load Balancer | Distributes traffic across instances | Scaling |
| Metric | Quantitative measure | KPI |
| Monitoring | Observing system behavior | Observability |
| Observability | Understanding system state | Monitoring |
| Rate Limit | Maximum request frequency | Throttling |
| Runbook | Step-by-step incident response guide | Documentation |
| Throughput | Requests per unit time | Performance |

---

## A

### Alert

**Definition:** A notification triggered when specific conditions or thresholds are met in the monitoring system. Alerts inform operators of potential issues that require attention.

**Example:**
```python
from typing import Callable, Dict, List
from datetime import datetime
from enum import Enum

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class AlertManager:
    """Manages alerts for agent monitoring."""
    
    def __init__(self):
        self.alerts: List[Dict] = []
        self.notification_handlers: List[Callable] = []
        self.rules: List[Dict] = []
    
    def add_rule(self, name: str, condition: Callable,
                severity: AlertSeverity, message_template: str):
        """Add an alert rule."""
        self.rules.append({
            "name": name,
            "condition": condition,
            "severity": severity,
            "message_template": message_template
        })
    
    def add_notification_handler(self, handler: Callable):
        """Add a handler for sending notifications."""
        self.notification_handlers.append(handler)
    
    def evaluate(self, metrics: Dict) -> List[Dict]:
        """Evaluate all rules against current metrics."""
        triggered = []
        
        for rule in self.rules:
            try:
                if rule["condition"](metrics):
                    alert = {
                        "rule": rule["name"],
                        "severity": rule["severity"],
                        "message": rule["message_template"].format(**metrics),
                        "timestamp": datetime.now().isoformat(),
                        "metrics": metrics
                    }
                    triggered.append(alert)
                    self.alerts.append(alert)
                    
                    # Send notifications
                    for handler in self.notification_handlers:
                        handler(alert)
            except Exception as e:
                print(f"Error evaluating rule {rule['name']}: {e}")
        
        return triggered
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        """Get recent alerts."""
        return self.alerts[-limit:]

# Usage
alert_manager = AlertManager()

# Add rules
alert_manager.add_rule(
    name="low_success_rate",
    condition=lambda m: m.get("success_rate", 1.0) < 0.95,
    severity=AlertSeverity.WARNING,
    message_template="Success rate dropped to {success_rate:.1%}"
)

alert_manager.add_rule(
    name="high_latency",
    condition=lambda m: m.get("avg_latency", 0) > 2.0,
    severity=AlertSeverity.WARNING,
    message_template="Average latency is {avg_latency:.2f}s"
)

# Add notification
def print_alert(alert):
    print(f"[{alert['severity'].value.upper()}] {alert['message']}")

alert_manager.add_notification_handler(print_alert)

# Evaluate
alerts = alert_manager.evaluate({"success_rate": 0.90, "avg_latency": 0.5})
```

**Related terms:** Notification, Warning, Threshold

---

## C

### Circuit Breaker

**Definition:** A resilience pattern that prevents an agent from repeatedly calling a failing service. When failures exceed a threshold, the circuit "opens" and calls fail fast until the service recovers.

**Example:**
```python
import time
from enum import Enum
from typing import Callable, Any

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject calls
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    """Circuit breaker for agent service calls."""
    
    def __init__(self, failure_threshold: int = 5,
                 recovery_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = None
    
    def record_success(self):
        """Record a successful call."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def record_failure(self):
        """Record a failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
    
    def can_execute(self) -> bool:
        """Check if execution is allowed."""
        if self.state == CircuitState.CLOSED:
            return True
        
        if self.state == CircuitState.OPEN:
            # Check if recovery timeout passed
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                return True
            return False
        
        # HALF_OPEN: allow one test call
        return True
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection."""
        if not self.can_execute():
            raise Exception("Circuit breaker is open")
        
        try:
            result = func(*args, **kwargs)
            self.record_success()
            return result
        except Exception as e:
            self.record_failure()
            raise

# Usage
breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=30)

@breaker.execute
def call_external_service(data):
    # Simulate service call
    if random.random() < 0.5:
        raise Exception("Service unavailable")
    return {"result": "success"}

# Calls will be rejected when circuit is open
```

**Related terms:** Resilience, Failure, Recovery

---

## D

### Dashboard

**Definition:** A visual display that shows real-time metrics, health status, and operational data for agent systems. Dashboards provide at-a-glance visibility into system state.

**Example:**
```python
from typing import Dict, List
from datetime import datetime

class Dashboard:
    """Agent monitoring dashboard."""
    
    def __init__(self):
        self.widgets = []
        self.refresh_interval = 30  # seconds
    
    def add_widget(self, widget_type: str, title: str, 
                  data_source: Callable, config: Dict = None):
        """Add a dashboard widget."""
        self.widgets.append({
            "type": widget_type,
            "title": title,
            "data_source": data_source,
            "config": config or {}
        })
    
    def render(self) -> Dict:
        """Render dashboard data."""
        return {
            "widgets": [
                {
                    "type": w["type"],
                    "title": w["title"],
                    "data": w["data_source"](),
                    "config": w["config"]
                }
                for w in self.widgets
            ],
            "last_updated": datetime.now().isoformat()
        }

# Create dashboard
dashboard = Dashboard()

# Add widgets
dashboard.add_widget(
    "gauge",
    "Success Rate",
    lambda: {"value": 98.5, "unit": "%"},
    {"min": 0, "max": 100, "thresholds": [90, 95]}
)

dashboard.add_widget(
    "line_chart",
    "Request Latency",
    lambda: {"data": [0.5, 0.4, 0.6, 0.5, 0.4]},
    {"y_axis": "seconds"}
)

dashboard.add_widget(
    "status",
    "Service Health",
    lambda: {"status": "healthy", "checks": ["api", "database", "cache"]}
)

# Render
print(dashboard.render())
```

**Related terms:** Visualization, Monitoring, Metrics

---

## H

### Health Check

**Definition:** A test performed to verify that an agent system is operational and functioning correctly. Health checks are typically exposed via HTTP endpoints for monitoring systems to query.

**Example:**
```python
from typing import Dict, Callable
from datetime import datetime
from enum import Enum

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

class HealthCheckManager:
    """Manages health checks for agent system."""
    
    def __init__(self):
        self.checks: Dict[str, Callable] = {}
        self.results: Dict[str, Dict] = {}
    
    def register_check(self, name: str, check_fn: Callable):
        """Register a health check."""
        self.checks[name] = check_fn
    
    def run_checks(self) -> Dict:
        """Run all health checks."""
        results = {}
        
        for name, check_fn in self.checks.items():
            try:
                result = check_fn()
                results[name] = {
                    "status": "healthy",
                    "details": result,
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                results[name] = {
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
        
        self.results = results
        
        # Determine overall status
        statuses = [r["status"] for r in results.values()]
        
        if all(s == "healthy" for s in statuses):
            overall = HealthStatus.HEALTHY
        elif any(s == "unhealthy" for s in statuses):
            overall = HealthStatus.UNHEALTHY
        else:
            overall = HealthStatus.DEGRADED
        
        return {
            "status": overall.value,
            "checks": results,
            "timestamp": datetime.now().isoformat()
        }

# Usage
manager = HealthCheckManager()

# Register checks
manager.register_check("database", lambda: {"connected": True})
manager.register_check("cache", lambda: {"connected": True, "items": 100})
manager.register_check("llm_api", lambda: {"available": True})

# Run checks
health = manager.run_checks()
print(f"Overall status: {health['status']}")
for check, result in health['checks'].items():
    print(f"  {check}: {result['status']}")
```

**Related terms:** Health, Status, Monitoring

---

## I

### Incident

**Definition:** An unexpected event that disrupts normal agent operation. Incidents require response to restore service and prevent recurrence.

**Example:**
```python
from typing import Dict, List
from datetime import datetime
from enum import Enum

class IncidentSeverity(Enum):
    SEV1 = "sev1"  # Critical, full outage
    SEV2 = "sev2"  # Major, significant impact
    SEV3 = "sev3"  # Minor, limited impact

class IncidentManager:
    """Manages incidents and response."""
    
    def __init__(self):
        self.incidents: List[Dict] = []
        self.runbooks: Dict[str, str] = {}
    
    def create_incident(self, title: str, severity: IncidentSeverity,
                       description: str, affected_components: List[str]) -> Dict:
        """Create a new incident."""
        incident = {
            "id": f"INC-{len(self.incidents) + 1}",
            "title": title,
            "severity": severity,
            "description": description,
            "affected_components": affected_components,
            "status": "open",
            "created_at": datetime.now().isoformat(),
            "resolved_at": None,
            "timeline": [{"event": "created", "time": datetime.now().isoformat()}]
        }
        
        self.incidents.append(incident)
        return incident
    
    def add_runbook(self, incident_type: str, runbook_url: str):
        """Add a runbook for an incident type."""
        self.runbooks[incident_type] = runbook_url
    
    def get_runbook(self, incident_type: str) -> str:
        """Get runbook for incident type."""
        return self.runbooks.get(incident_type, "No runbook found")
    
    def resolve_incident(self, incident_id: str, resolution: str):
        """Mark incident as resolved."""
        for incident in self.incidents:
            if incident["id"] == incident_id:
                incident["status"] = "resolved"
                incident["resolved_at"] = datetime.now().isoformat()
                incident["resolution"] = resolution
                incident["timeline"].append({
                    "event": "resolved",
                    "time": datetime.now().isoformat()
                })
                break

# Usage
manager = IncidentManager()

# Create incident
incident = manager.create_incident(
    title="Agent high error rate",
    severity=IncidentSeverity.SEV2,
    description="Error rate exceeded 10% threshold",
    affected_components=["qa_agent", "llm_api"]
)

print(f"Incident created: {incident['id']}")

# Add runbook
manager.add_runbook("high_error_rate", "/runbooks/error-rate.md")

# Resolve
manager.resolve_incident(incident["id"], "Increased timeout, errors resolved")
```

**Related terms:** Outage, Response, Resolution

---

## M

### Metric

**Definition:** A quantitative measurement of agent behavior or performance. Metrics are collected over time to track trends and detect issues.

**Example:**
```python
from typing import Dict, List
from datetime import datetime, timedelta
from collections import defaultdict
import statistics

class MetricsCollector:
    """Collects and aggregates metrics."""
    
    def __init__(self):
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, List[float]] = defaultdict(list)
        self.timestamps: Dict[str, List[datetime]] = defaultdict(list)
    
    def increment(self, name: str, value: int = 1):
        """Increment a counter."""
        self.counters[name] += value
    
    def set_gauge(self, name: str, value: float):
        """Set a gauge value."""
        self.gauges[name] = value
        self.timestamps[name].append(datetime.now())
    
    def observe(self, name: str, value: float):
        """Record a histogram observation."""
        self.histograms[name].append(value)
        self.timestamps[name].append(datetime.now())
    
    def get_summary(self) -> Dict:
        """Get summary of all metrics."""
        summary = {
            "counters": dict(self.counters),
            "gauges": dict(self.gauges),
            "histograms": {}
        }
        
        for name, values in self.histograms.items():
            if values:
                summary["histograms"][name] = {
                    "count": len(values),
                    "min": min(values),
                    "max": max(values),
                    "mean": statistics.mean(values),
                    "median": statistics.median(values),
                    "p95": sorted(values)[int(len(values) * 0.95)] if len(values) >= 20 else max(values)
                }
        
        return summary

# Usage
metrics = MetricsCollector()

# Record metrics
metrics.increment("requests_total")
metrics.increment("requests_success")
metrics.set_gauge("active_connections", 5)
metrics.observe("request_latency", 0.5)
metrics.observe("request_latency", 0.3)
metrics.observe("request_latency", 0.4)

# Get summary
print(metrics.get_summary())
```

**Related terms:** Measurement, Counter, Gauge, Histogram

---

## O

### Observability

**Definition:** The ability to understand the internal state of a system by examining its outputs. The three pillars of observability are logs, metrics, and traces.

**Example:**
```python
from typing import Any, Dict
from datetime import datetime
import json
import uuid

class ObservabilityStack:
    """Complete observability for agents."""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logs = []
        self.metrics = {}
        self.traces = []
    
    def log(self, level: str, message: str, **kwargs):
        """Record a log entry."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "service": self.service_name,
            "message": message,
            **kwargs
        }
        self.logs.append(entry)
        
        # Print to console
        print(f"[{level.upper()}] {message}")
    
    def record_trace(self, operation: str, **kwargs):
        """Record a trace span."""
        trace = {
            "trace_id": str(uuid.uuid4()),
            "operation": operation,
            "service": self.service_name,
            "timestamp": datetime.now().isoformat(),
            **kwargs
        }
        self.traces.append(trace)
        return trace["trace_id"]
    
    def get_logs(self, level: str = None, limit: int = 100) -> list:
        """Get logs, optionally filtered by level."""
        logs = self.logs
        if level:
            logs = [l for l in logs if l["level"] == level]
        return logs[-limit:]

# Usage
obs = ObservabilityStack("qa-agent")

obs.log("info", "Request received", request_id="123")
obs.log("info", "Processing started")
obs.log("error", "LLM call failed", error="timeout")
obs.log("info", "Fallback invoked")

trace_id = obs.record_trace("process_request", duration=0.5)
```

**Related terms:** Logging, Metrics, Tracing

---

## S

### Scaling

**Definition:** Adjusting agent capacity to handle varying load. Can be vertical (more resources per instance) or horizontal (more instances).

**Example:**
```python
from typing import Dict, List
from datetime import datetime
import threading

class ScalingManager:
    """Manages agent scaling."""
    
    def __init__(self, min_instances: int = 1, max_instances: int = 10):
        self.min_instances = min_instances
        self.max_instances = max_instances
        self.current_instances = min_instances
        self.scaling_history = []
    
    def evaluate_scaling(self, metrics: Dict) -> str:
        """Evaluate if scaling is needed."""
        cpu_usage = metrics.get("cpu_usage", 0)
        request_queue = metrics.get("request_queue", 0)
        
        # Scale up conditions
        if cpu_usage > 80 or request_queue > 100:
            return "scale_up"
        
        # Scale down conditions
        if cpu_usage < 20 and request_queue < 10:
            return "scale_down"
        
        return "no_change"
    
    def scale_up(self):
        """Increase instances."""
        if self.current_instances < self.max_instances:
            self.current_instances += 1
            self._record_scaling("up")
    
    def scale_down(self):
        """Decrease instances."""
        if self.current_instances > self.min_instances:
            self.current_instances -= 1
            self._record_scaling("down")
    
    def _record_scaling(self, direction: str):
        """Record scaling event."""
        self.scaling_history.append({
            "direction": direction,
            "from": self.current_instances - (1 if direction == "up" else -1),
            "to": self.current_instances,
            "timestamp": datetime.now().isoformat()
        })

# Usage
scaler = ScalingManager(min_instances=2, max_instances=8)

# Evaluate and scale
metrics = {"cpu_usage": 85, "request_queue": 150}
action = scaler.evaluate_scaling(metrics)

if action == "scale_up":
    scaler.scale_up()
    print(f"Scaled up to {scaler.current_instances} instances")
```

**Related terms:** Capacity, Auto-scaling, Load Balancing

---

## Quick Reference: Production Checklist

```
┌─────────────────────────────────────────────────────────────┐
│              Production Deployment Checklist                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  PRE-DEPLOYMENT                                             │
│  □ All tests passing                                       │
│  □ Load testing completed                                  │
│  □ Security review done                                    │
│  □ Runbooks documented                                     │
│  □ Rollback procedure tested                               │
│                                                             │
│  DEPLOYMENT                                                 │
│  □ Configuration reviewed                                  │
│  □ Secrets properly managed                                │
│  □ Health checks configured                                │
│  □ Monitoring enabled                                      │
│  □ Alerts configured                                       │
│                                                             │
│  POST-DEPLOYMENT                                            │
│  □ Smoke tests passed                                      │
│  □ Metrics baseline established                            │
│  □ On-call team notified                                   │
│  □ Documentation updated                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**[← Back to Lecture 10](./10-production-agents-lecture.md)** | **[Back to README](./README.md)**
