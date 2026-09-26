"""
08 Model Security: Backdoor
"""

from ._types import *


class BackdoorDetector:
    """
    Detect backdoor/trojan attacks in neural networks.

    Techniques:
    - Neural cleanse
    - Activation clustering
    - Statistical testing
    """

    def __init__(self):
        self._clean_activations: Dict[str, List[float]] = defaultdict(list)

    def analyze_model_behavior(
        self,
        model_fn: Callable,
        test_inputs: List[List[float]],
        expected_labels: List[int],
    ) -> Dict:
        """
        Analyze model behavior for potential backdoors.
        """
        anomalies = []
        predictions = []

        for i, (inp, label) in enumerate(zip(test_inputs, expected_labels)):
            try:
                pred = model_fn(inp)
                predictions.append(pred)

                # Check for unusual predictions
                if pred != label:
                    # Analyze why prediction differs
                    diff_score = self._compute_perturbation_sensitivity(inp, model_fn)
                    if diff_score > 0.5:
                        anomalies.append(
                            {
                                "sample_index": i,
                                "expected": label,
                                "predicted": pred,
                                "perturbation_sensitivity": diff_score,
                            }
                        )
            except Exception as e:
                anomalies.append(
                    {
                        "sample_index": i,
                        "error": str(e),
                    }
                )

        # Analyze prediction distribution
        pred_counter = Counter(predictions)
        label_counter = Counter(expected_labels)

        distribution_shift = 0
        for label in set(list(pred_counter.keys()) + list(label_counter.keys())):
            pred_ratio = (
                pred_counter.get(label, 0) / len(predictions) if predictions else 0
            )
            true_ratio = (
                label_counter.get(label, 0) / len(expected_labels)
                if expected_labels
                else 0
            )
            distribution_shift += abs(pred_ratio - true_ratio)

        return {
            "backdoor_suspected": distribution_shift > 0.3
            or len(anomalies) > len(test_inputs) * 0.1,
            "anomalies": anomalies[:10],  # First 10 anomalies
            "anomaly_count": len(anomalies),
            "distribution_shift": round(distribution_shift, 3),
            "prediction_distribution": dict(pred_counter),
            "total_tested": len(test_inputs),
        }

    def _compute_perturbation_sensitivity(
        self,
        features: List[float],
        model_fn: Callable,
        epsilon: float = 0.01,
    ) -> float:
        """Compute model sensitivity to small perturbations."""
        try:
            original = model_fn(features)
            max_change = 0

            for i in range(min(len(features), 5)):
                perturbed = features.copy()
                perturbed[i] += epsilon
                perturbed_pred = model_fn(perturbed)

                if isinstance(original, (int, float)) and isinstance(
                    perturbed_pred, (int, float)
                ):
                    change = abs(perturbed_pred - original)
                    max_change = max(max_change, change)

            return min(1.0, max_change)
        except Exception:
            return 0

    def activation_clustering_analysis(
        self,
        clean_activations: List[List[float]],
        suspect_activations: List[List[float]],
    ) -> Dict:
        """
        Compare activation patterns between clean and suspect data.
        Backdoored inputs often produce distinct activation clusters.
        """
        if not clean_activations or not suspect_activations:
            return {"separation_detected": False, "reason": "Insufficient data"}

        # Compute centroids
        n_features = min(len(clean_activations[0]), len(suspect_activations[0]))

        clean_centroid = [
            sum(a[i] for a in clean_activations) / len(clean_activations)
            for i in range(n_features)
        ]
        suspect_centroid = [
            sum(a[i] for a in suspect_activations) / len(suspect_activations)
            for i in range(n_features)
        ]

        # Compute separation
        distance = math.sqrt(
            sum((c - s) ** 2 for c, s in zip(clean_centroid, suspect_centroid))
        )

        # Compute intra-cluster distances
        clean_spread = self._compute_spread(clean_activations, clean_centroid)
        suspect_spread = self._compute_spread(suspect_activations, suspect_centroid)

        # Separation ratio
        separation_ratio = distance / (clean_spread + suspect_spread + 1e-10)

        return {
            "separation_detected": separation_ratio > 2.0,
            "separation_ratio": round(separation_ratio, 3),
            "distance": round(distance, 3),
            "clean_spread": round(clean_spread, 3),
            "suspect_spread": round(suspect_spread, 3),
        }

    def _compute_spread(self, data: List[List[float]], centroid: List[float]) -> float:
        """Compute average distance from centroid."""
        total = 0
        for point in data:
            dist = math.sqrt(
                sum((p - c) ** 2 for p, c in zip(point[: len(centroid)], centroid))
            )
            total += dist
        return total / len(data) if data else 0


# =============================================================
# SECTION 6: Secure Model Serving
# =============================================================
