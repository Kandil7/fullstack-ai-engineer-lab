"""
08 Model Security: Access Control
"""

from ._types import *

class ModelAccessController:
    """
    Control access to models to prevent theft and unauthorized use.

    Features:
    - Query rate limiting
    - Output perturbation
    - Usage tracking
    - Anomaly detection
    - Model fingerprinting
    """

    def __init__(self):
        self._query_log: Dict[str, List[Dict]] = defaultdict(list)
        self._model_metadata: Dict[str, Dict] = {}
        self._access_tokens: Dict[str, Dict] = {}
        self._rate_limits: Dict[str, Dict] = {}

    def register_model(
        self,
        model_id: str,
        owner_id: str,
        sensitivity: str = "medium",
    ):
        """Register a model for protection."""
        self._model_metadata[model_id] = {
            "owner_id": owner_id,
            "sensitivity": sensitivity,
            "created_at": time.time(),
            "total_queries": 0,
            "unique_users": set(),
        }

        # Set rate limits based on sensitivity
        limits = {
            "low": {"per_minute": 100, "per_hour": 5000},
            "medium": {"per_minute": 50, "per_hour": 2000},
            "high": {"per_minute": 20, "per_hour": 500},
            "critical": {"per_minute": 10, "per_hour": 100},
        }
        self._rate_limits[model_id] = limits.get(sensitivity, limits["medium"])

    def check_access(
        self,
        model_id: str,
        user_id: str,
        query_type: str = "inference",
    ) -> Dict:
        """Check if access to model should be allowed."""
        model = self._model_metadata.get(model_id)
        if not model:
            return {"allowed": False, "reason": "Model not found"}

        # Track usage
        now = time.time()
        self._query_log[model_id].append(
            {
                "user_id": user_id,
                "timestamp": now,
                "query_type": query_type,
            }
        )

        model["total_queries"] += 1
        model["unique_users"].add(user_id)

        # Check rate limits
        limits = self._rate_limits.get(model_id, {})
        recent_minute = sum(
            1 for q in self._query_log[model_id] if now - q["timestamp"] < 60
        )
        recent_hour = sum(
            1 for q in self._query_log[model_id] if now - q["timestamp"] < 3600
        )

        if recent_minute > limits.get("per_minute", 50):
            return {"allowed": False, "reason": "Rate limit exceeded (per minute)"}
        if recent_hour > limits.get("per_hour", 2000):
            return {"allowed": False, "reason": "Rate limit exceeded (per hour)"}

        # Anomaly detection
        anomaly = self._detect_query_anomaly(model_id, user_id)
        if anomaly["is_anomalous"]:
            return {"allowed": False, "reason": "Anomalous query pattern detected"}

        return {
            "allowed": True,
            "remaining_minute": limits.get("per_minute", 50) - recent_minute,
        }

    def _detect_query_anomaly(self, model_id: str, user_id: str) -> Dict:
        """Detect anomalous query patterns that may indicate extraction."""
        recent_queries = [
            q
            for q in self._query_log[model_id]
            if time.time() - q["timestamp"] < 3600 and q["user_id"] == user_id
        ]

        if len(recent_queries) < 10:
            return {"is_anomalous": False}

        # Check for systematic probing
        # (e.g., queries that vary in small increments)
        timestamps = [q["timestamp"] for q in recent_queries]
        intervals = [
            timestamps[i + 1] - timestamps[i] for i in range(len(timestamps) - 1)
        ]

        if intervals:
            # Check for very regular intervals (bot-like behavior)
            mean_interval = sum(intervals) / len(intervals)
            variance = sum((i - mean_interval) ** 2 for i in intervals) / len(intervals)
            cv = math.sqrt(variance) / mean_interval if mean_interval > 0 else 0

            if cv < 0.1 and len(intervals) > 20:
                return {
                    "is_anomalous": True,
                    "reason": "Suspiciously regular query pattern (possible extraction attempt)",
                    "confidence": 0.8,
                }

        return {"is_anomalous": False}


# =============================================================
# SECTION 4: Model Watermarking
# =============================================================


