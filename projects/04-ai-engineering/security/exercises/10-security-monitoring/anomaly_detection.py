"""
10 Security Monitoring: Anomaly Detection
"""

from ._types import *
from .alerts import Alert

class AnomalyDetector:
    """
    Statistical anomaly detection for security monitoring.

    Techniques:
    - Z-score based detection
    - Moving average detection
    - Isolation Forest (simplified)
    - Time series analysis
    """

    def __init__(self, sensitivity: float = 2.0):
        """
        Args:
            sensitivity: Number of standard deviations for anomaly threshold
        """
        self.sensitivity = sensitivity
        self._baselines: Dict[str, Dict] = {}
        self._time_series: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10000))
        self._anomalies: List[Dict] = []

    def update_baseline(self, metric_name: str, value: float):
        """Update baseline statistics for a metric."""
        if metric_name not in self._baselines:
            self._baselines[metric_name] = {
                "values": deque(maxlen=10000),
                "mean": 0,
                "std": 1,
                "count": 0,
            }

        baseline = self._baselines[metric_name]
        baseline["values"].append(value)
        baseline["count"] += 1

        # Update running statistics
        values = list(baseline["values"])
        baseline["mean"] = statistics.mean(values)
        baseline["std"] = statistics.stdev(values) if len(values) > 1 else 1

    def detect_anomaly(self, metric_name: str, value: float) -> Dict:
        """Check if a value is anomalous."""
        if metric_name not in self._baselines:
            return {"is_anomaly": False, "reason": "No baseline established"}

        baseline = self._baselines[metric_name]

        if baseline["count"] < 30:
            return {"is_anomaly": False, "reason": "Insufficient baseline data"}

        # Z-score
        z_score = (value - baseline["mean"]) / max(baseline["std"], 1e-10)
        is_anomaly = abs(z_score) > self.sensitivity

        # Moving average check
        values = list(baseline["values"])
        if len(values) >= 10:
            recent_mean = statistics.mean(values[-10:])
            recent_std = statistics.stdev(values[-10:]) if len(values) > 10 else 1
            recent_z = (value - recent_mean) / max(recent_std, 1e-10)
        else:
            recent_z = z_score

        result = {
            "is_anomaly": is_anomaly,
            "metric": metric_name,
            "value": value,
            "baseline_mean": round(baseline["mean"], 4),
            "baseline_std": round(baseline["std"], 4),
            "z_score": round(z_score, 4),
            "recent_z_score": round(recent_z, 4),
            "sensitivity": self.sensitivity,
        }

        if is_anomaly:
            self._anomalies.append(
                {
                    **result,
                    "timestamp": time.time(),
                }
            )

        return result

    def detect_time_series_anomaly(self, series_name: str, value: float) -> Dict:
        """Detect anomalies in time series data."""
        self._time_series[series_name].append((time.time(), value))
        series = list(self._time_series[series_name])

        if len(series) < 20:
            return {"is_anomaly": False, "reason": "Insufficient data points"}

        # Extract values
        values = [v for _, v in series[-100:]]

        # Compute seasonal component (simplified)
        mean = statistics.mean(values)
        std = statistics.stdev(values) if len(values) > 1 else 1

        # Check for sudden changes
        if len(values) >= 10:
            recent = values[-5:]
            historical = values[:-5]
            recent_mean = statistics.mean(recent)
            historical_mean = statistics.mean(historical)

            change_ratio = abs(recent_mean - historical_mean) / max(
                abs(historical_mean), 1e-10
            )

            if change_ratio > 0.5:  # 50% change
                return {
                    "is_anomaly": True,
                    "type": "sudden_change",
                    "change_ratio": round(change_ratio, 4),
                    "recent_mean": round(recent_mean, 4),
                    "historical_mean": round(historical_mean, 4),
                }

        # Z-score check
        z_score = (value - mean) / max(std, 1e-10)
        if abs(z_score) > self.sensitivity:
            return {
                "is_anomaly": True,
                "type": "statistical_outlier",
                "z_score": round(z_score, 4),
            }

        return {"is_anomaly": False}

    def get_anomalies(self, hours: int = 24) -> List[Dict]:
        """Get detected anomalies."""
        cutoff = time.time() - (hours * 3600)
        return [a for a in self._anomalies if a.get("timestamp", 0) > cutoff]

    def get_baseline_summary(self) -> Dict:
        """Get summary of all baselines."""
        return {
            metric: {
                "mean": round(b["mean"], 4),
                "std": round(b["std"], 4),
                "count": b["count"],
            }
            for metric, b in self._baselines.items()
        }


# =============================================================
# SECTION 4: Alert System
# =============================================================


