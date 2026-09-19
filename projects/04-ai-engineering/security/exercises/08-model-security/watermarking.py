"""
08 Model Security: Watermarking
"""

from ._types import *

class ModelWatermarker:
    """
    Embed watermarks in model outputs for ownership verification.

    Techniques:
    - Trigger-based watermarking
    - Output pattern embedding
    - Behavioral watermarking
    """

    def __init__(self, secret_key: bytes = None):
        self.secret_key = secret_key or secrets.token_bytes(32)
        self._watermark_patterns: Dict[str, Dict] = {}

    def create_watermark(
        self,
        model_id: str,
        owner_id: str,
        trigger_inputs: Optional[List[List[float]]] = None,
    ) -> Dict:
        """
        Create a watermark for a model.

        The watermark encodes ownership information in model behavior.
        """
        # Generate trigger patterns
        if not trigger_inputs:
            trigger_inputs = self._generate_trigger_patterns(5)

        # Create expected outputs for triggers
        watermark_data = {
            "model_id": model_id,
            "owner_id": owner_id,
            "created_at": time.time(),
            "trigger_count": len(trigger_inputs),
            "triggers": trigger_inputs,
            "expected_hash": hashlib.sha256(
                json.dumps(trigger_inputs, sort_keys=True).encode()
            ).hexdigest(),
        }

        # Sign the watermark
        watermark_str = json.dumps(watermark_data, sort_keys=True)
        signature = hmac.new(
            self.secret_key,
            watermark_str.encode(),
            hashlib.sha256,
        ).hexdigest()

        self._watermark_patterns[model_id] = {
            "watermark": watermark_data,
            "signature": signature,
        }

        return {
            "model_id": model_id,
            "watermark_id": hashlib.sha256(signature.encode()).hexdigest()[:16],
            "triggers_embedded": len(trigger_inputs),
            "signature": signature,
        }

    def verify_watermark(
        self,
        model_id: str,
        model_fn: Callable,
    ) -> Dict:
        """
        Verify if a model contains a watermark.

        Tests the model with trigger inputs and checks outputs.
        """
        stored = self._watermark_patterns.get(model_id)
        if not stored:
            return {
                "watermarked": False,
                "reason": "No watermark registered for this model",
            }

        watermark = stored["watermark"]

        # Test trigger patterns
        matches = 0
        for trigger in watermark["triggers"]:
            try:
                output = model_fn(trigger)
                # Check if output matches expected pattern
                # In practice, this would use a more sophisticated check
                if self._check_output_pattern(output, trigger):
                    matches += 1
            except Exception:
                continue

        match_ratio = matches / len(watermark["triggers"])

        return {
            "watermarked": match_ratio > 0.6,
            "match_ratio": match_ratio,
            "triggers_tested": len(watermark["triggers"]),
            "matches": matches,
            "confidence": match_ratio,
        }

    def _generate_trigger_patterns(self, count: int) -> List[List[float]]:
        """Generate unique trigger patterns based on secret key."""
        patterns = []
        for i in range(count):
            # Deterministic generation based on key and index
            seed = hashlib.sha256(self.secret_key + struct.pack("I", i)).digest()
            rng = random.Random(seed)
            pattern = [rng.gauss(0, 1) for _ in range(10)]
            patterns.append(pattern)
        return patterns

    def _check_output_pattern(self, output: Any, trigger: List[float]) -> bool:
        """Check if model output matches expected watermark pattern."""
        # Simple pattern matching - in practice, more sophisticated
        if isinstance(output, (int, float)):
            # Check if output is in expected range based on trigger
            expected = hash(tuple(trigger)) % 100 / 100.0
            return abs(float(output) - expected) < 0.1
        elif isinstance(output, list):
            return len(output) > 0
        return False


# =============================================================
# SECTION 5: Backdoor Detection
# =============================================================


