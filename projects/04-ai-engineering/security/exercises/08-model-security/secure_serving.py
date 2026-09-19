"""
08 Model Security: Secure Serving
"""

from ._types import *
from .adversarial import AdversarialDetector

class SecureModelServer:
    """
    Secure model serving with multiple protection layers.
    """

    def __init__(self):
        self._models: Dict[str, Dict] = {}
        self._query_log: List[Dict] = []
        self._rate_limiter = TokenBucketRateLimiter(capacity=50, refill_rate=5)
        self._input_validator = InputValidator()
        self._adversarial_detector = AdversarialDetector()

    def register_model(
        self, model_id: str, model_fn: Callable, sensitivity: str = "medium"
    ):
        """Register a model for secure serving."""
        self._models[model_id] = {
            "fn": model_fn,
            "sensitivity": sensitivity,
            "created_at": time.time(),
            "total_queries": 0,
        }

    def predict(
        self,
        model_id: str,
        features: List[float],
        user_id: str = "anonymous",
    ) -> Dict:
        """
        Make a prediction with security checks.
        """
        start_time = time.time()

        # 1. Rate limiting
        rate_check = self._rate_limiter.is_allowed(user_id)
        if not rate_check["allowed"]:
            return {
                "error": "Rate limit exceeded",
                "retry_after": rate_check["retry_after"],
                "status": 429,
            }

        # 2. Model exists?
        model = self._models.get(model_id)
        if not model:
            return {"error": "Model not found", "status": 404}

        # 3. Input validation
        validation = self._input_validator.validate(features, model_id)
        if not validation["valid"]:
            return {
                "error": "Invalid input",
                "details": validation["errors"],
                "status": 400,
            }

        # 4. Adversarial detection
        adv_check = self._adversarial_detector.detect_adversarial(features, model["fn"])
        if adv_check["is_adversarial"]:
            return {
                "error": "Potentially adversarial input detected",
                "confidence": adv_check["confidence"],
                "status": 403,
            }

        # 5. Make prediction
        try:
            prediction = model["fn"](features)
        except Exception as e:
            return {"error": "Prediction failed", "status": 500}

        # 6. Add noise for sensitive models
        if model["sensitivity"] in ("high", "critical"):
            prediction = self._add_output_noise(prediction)

        # 7. Log query
        self._query_log.append(
            {
                "model_id": model_id,
                "user_id": user_id,
                "timestamp": time.time(),
                "latency": time.time() - start_time,
            }
        )

        model["total_queries"] += 1

        return {
            "prediction": prediction,
            "model_id": model_id,
            "latency_ms": round((time.time() - start_time) * 1000, 2),
        }

    def _add_output_noise(self, prediction: Any) -> Any:
        """Add differential privacy noise to output."""
        if isinstance(prediction, (int, float)):
            noise = random.gauss(0, 0.01)
            return prediction + noise
        return prediction


class TokenBucketRateLimiter:
    """Simple token bucket rate limiter."""

    def __init__(self, capacity: int = 100, refill_rate: float = 10):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._buckets: Dict[str, Dict] = {}

    def is_allowed(self, client_id: str) -> Dict:
        now = time.time()
        if client_id not in self._buckets:
            self._buckets[client_id] = {"tokens": self.capacity, "last_refill": now}

        bucket = self._buckets[client_id]
        elapsed = now - bucket["last_refill"]
        bucket["tokens"] = min(
            self.capacity, bucket["tokens"] + elapsed * self.refill_rate
        )
        bucket["last_refill"] = now

        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return {"allowed": True, "remaining": int(bucket["tokens"])}
        return {"allowed": False, "retry_after": 1 / self.refill_rate}


class InputValidator:
    """Validate model inputs."""

    def __init__(self):
        self._schemas: Dict[str, Dict] = {}

    def validate(self, features: List[float], model_id: str) -> Dict:
        """Validate input features."""
        errors = []

        if not isinstance(features, list):
            return {"valid": False, "errors": ["Input must be a list"]}

        for i, f in enumerate(features):
            if not isinstance(f, (int, float)):
                errors.append(f"Feature {i} must be numeric")
            elif math.isnan(f) or math.isinf(f):
                errors.append(f"Feature {i} contains NaN or Inf")
            elif abs(f) > 10000:
                errors.append(f"Feature {i} out of range: {f}")

        return {"valid": len(errors) == 0, "errors": errors}


# =============================================================
# DEMONSTRATIONS
# =============================================================


