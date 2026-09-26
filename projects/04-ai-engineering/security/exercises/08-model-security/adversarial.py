"""
08 Model Security: Adversarial
"""

from ._types import *


class AdversarialDetector:
    """
    Detect adversarial examples in model inputs.

    Techniques:
    - Feature squeezing
    - Statistical tests
    - Gradient-based detection
    - Input validation
    """

    def __init__(self, sensitivity: float = 0.5):
        self.sensitivity = sensitivity
        self._input_history: List[List[float]] = []
        self._prediction_history: List[Any] = []

    def detect_adversarial(
        self, input_features: List[float], model_fn: Callable
    ) -> Dict:
        """
        Check if an input is potentially adversarial.

        Args:
            input_features: Input feature vector
            model_fn: Model prediction function

        Returns:
            Dict with is_adversarial, confidence, reasons
        """
        reasons = []
        scores = []

        # 1. Input range validation
        range_score = self._check_input_ranges(input_features)
        scores.append(range_score)
        if range_score > 0.7:
            reasons.append("Input features outside normal ranges")

        # 2. Feature squeezing detection
        squeeze_score = self._feature_squeezing_test(input_features, model_fn)
        scores.append(squeeze_score)
        if squeeze_score > 0.6:
            reasons.append(
                "Model predictions change significantly with feature squeezing"
            )

        # 3. Statistical anomaly detection
        stat_score = self._statistical_test(input_features)
        scores.append(stat_score)
        if stat_score > 0.6:
            reasons.append("Input statistically different from training distribution")

        # 4. Gradient-based detection (simulated)
        grad_score = self._gradient_test(input_features, model_fn)
        scores.append(grad_score)
        if grad_score > 0.7:
            reasons.append("Input requires unusual gradient magnitude")

        # Combine scores
        avg_score = sum(scores) / len(scores) if scores else 0
        is_adversarial = avg_score > self.sensitivity

        return {
            "is_adversarial": is_adversarial,
            "confidence": avg_score,
            "reasons": reasons,
            "scores": {
                "input_range": scores[0],
                "feature_squeezing": scores[1],
                "statistical": scores[2],
                "gradient": scores[3],
            },
        }

    def _check_input_ranges(self, features: List[float]) -> float:
        """Check if input features are within expected ranges."""
        anomalies = 0
        for i, f in enumerate(features):
            # Basic sanity checks
            if abs(f) > 1000:  # Assuming normalized features
                anomalies += 1
            if math.isnan(f) or math.isinf(f):
                anomalies += 1

        return min(1.0, anomalies / max(1, len(features)))

    def _feature_squeezing_test(
        self,
        features: List[float],
        model_fn: Callable,
        squeeze_bit_depth: int = 8,
    ) -> float:
        """
        Feature squeezing: reduce precision and check prediction change.
        Adversarial examples often have fragile decision boundaries.
        """
        try:
            # Original prediction
            original_pred = model_fn(features)

            # Squeezed prediction (reduce precision)
            squeezed = [
                round(f * (2**squeeze_bit_depth)) / (2**squeeze_bit_depth)
                for f in features
            ]
            squeezed_pred = model_fn(squeezed)

            # Compare predictions
            if original_pred != squeezed_pred:
                return 0.8  # Prediction changed = suspicious
            return 0.1
        except Exception:
            return 0.5  # Uncertain

    def _statistical_test(self, features: List[float]) -> float:
        """Statistical test against training distribution."""
        if not self._input_history:
            return 0.3  # No baseline yet

        # Calculate Mahalanobis-like distance
        n_features = min(len(features), len(self._input_history[0]))
        distances = []

        for i in range(n_features):
            hist_values = [h[i] for h in self._input_history if len(h) > i]
            if not hist_values:
                continue

            mean = sum(hist_values) / len(hist_values)
            variance = sum((v - mean) ** 2 for v in hist_values) / len(hist_values)
            std = math.sqrt(variance) if variance > 0 else 1e-10

            z_score = abs(features[i] - mean) / std
            distances.append(z_score)

        if not distances:
            return 0.3

        avg_distance = sum(distances) / len(distances)
        # Normalize to 0-1 range
        return min(1.0, avg_distance / 5.0)

    def _gradient_test(self, features: List[float], model_fn: Callable) -> float:
        """Simplified gradient-based detection."""
        # Simulate gradient computation by checking sensitivity
        perturbation = 0.01
        max_sensitivity = 0

        for i in range(min(len(features), 10)):  # Check first 10 features
            perturbed = features.copy()
            perturbed[i] += perturbation

            try:
                orig_pred = model_fn(features)
                pert_pred = model_fn(perturbed)

                # If numeric, compute difference
                if isinstance(orig_pred, (int, float)) and isinstance(
                    pert_pred, (int, float)
                ):
                    sensitivity = abs(pert_pred - orig_pred) / perturbation
                    max_sensitivity = max(max_sensitivity, sensitivity)
            except Exception:
                continue

        # High sensitivity to small perturbations = potential adversarial
        return min(1.0, max_sensitivity / 100.0)

    def update_baseline(self, features: List[float], prediction: Any):
        """Update baseline statistics with new clean data."""
        self._input_history.append(features)
        self._prediction_history.append(prediction)

        # Keep history bounded
        if len(self._input_history) > 10000:
            self._input_history = self._input_history[-5000:]
            self._prediction_history = self._prediction_history[-5000:]


class AdversarialRobustnessTester:
    """
    Test model robustness against adversarial attacks.
    """

    def __init__(self):
        self._attack_results: List[Dict] = []

    def fgsm_attack(
        self,
        features: List[float],
        label: int,
        model_fn: Callable,
        epsilon: float = 0.1,
    ) -> List[float]:
        """
        Fast Gradient Sign Method (FGSM) attack.
        Simulates gradient-based adversarial perturbation.
        """
        # Simulate gradient computation
        perturbed = features.copy()
        for i in range(len(features)):
            # Simulate gradient sign (in practice, compute actual gradient)
            gradient_sign = random.choice([-1, 1])  # Placeholder
            perturbed[i] = features[i] + epsilon * gradient_sign

        return perturbed

    def pgd_attack(
        self,
        features: List[float],
        label: int,
        model_fn: Callable,
        epsilon: float = 0.1,
        steps: int = 10,
        step_size: float = 0.01,
    ) -> List[float]:
        """
        Projected Gradient Descent (PGD) attack.
        Iterative version of FGSM.
        """
        perturbed = features.copy()

        for step in range(steps):
            # Apply perturbation
            for i in range(len(features)):
                gradient_sign = random.choice([-1, 1])
                perturbed[i] += step_size * gradient_sign

                # Project back to epsilon ball
                delta = perturbed[i] - features[i]
                if abs(delta) > epsilon:
                    perturbed[i] = features[i] + epsilon * (1 if delta > 0 else -1)

        return perturbed

    def evaluate_robustness(
        self,
        test_data: List[Tuple[List[float], int]],
        model_fn: Callable,
        epsilon: float = 0.1,
    ) -> Dict:
        """Evaluate model robustness against adversarial attacks."""
        correct_clean = 0
        correct_fgsm = 0
        correct_pgd = 0
        total = len(test_data)

        for features, label in test_data:
            # Clean accuracy
            pred = model_fn(features)
            if pred == label:
                correct_clean += 1

            # FGSM
            fgsm_features = self.fgsm_attack(features, label, model_fn, epsilon)
            pred_fgsm = model_fn(fgsm_features)
            if pred_fgsm == label:
                correct_fgsm += 1

            # PGD
            pgd_features = self.pgd_attack(features, label, model_fn, epsilon)
            pred_pgd = model_fn(pgd_features)
            if pred_pgd == label:
                correct_pgd += 1

        results = {
            "clean_accuracy": correct_clean / total if total > 0 else 0,
            "fgsm_accuracy": correct_fgsm / total if total > 0 else 0,
            "pgd_accuracy": correct_pgd / total if total > 0 else 0,
            "robustness_score": (correct_fgsm + correct_pgd) / (2 * total)
            if total > 0
            else 0,
            "total_samples": total,
            "epsilon": epsilon,
        }

        self._attack_results.append(results)
        return results


# =============================================================
# SECTION 3: Model Theft Prevention
# =============================================================
