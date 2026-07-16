"""
=============================================================
Topic 08: AI Model Security
=============================================================

Security Level: ########## Critical

Protect your ML models from attacks, theft, and manipulation.
This exercise covers model poisoning detection, adversarial
attacks, model theft prevention, watermarking, and secure
model serving.

Learning Objectives:
- Detect and prevent training data poisoning
- Implement adversarial robustness testing
- Protect models from extraction attacks
- Apply model watermarking techniques
- Secure model serving infrastructure

Prerequisites:
- Basic ML knowledge (training, inference)
- Understanding of neural network architectures
- Familiarity with Python/NumPy
=============================================================
"""

import hashlib
import hmac
import json
import math
import random
import secrets
import struct
import time
from collections import defaultdict, Counter
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
import base64
import re


# =============================================================
# SECTION 1: Training Data Poisoning Detection
# =============================================================

@dataclass
class DataPoint:
    """A single training data point with metadata."""
    features: List[float]
    label: Any
    source: str
    timestamp: float = field(default_factory=time.time)
    checksum: str = ""
    is_suspicious: bool = False

    def __post_init__(self):
        if not self.checksum:
            self.checksum = self._compute_checksum()

    def _compute_checksum(self) -> str:
        """Compute integrity checksum."""
        data = json.dumps({"features": self.features, "label": self.label}, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()


class DataPoisoningDetector:
    """
    Detect potential data poisoning in training datasets.

    Techniques:
    - Statistical outlier detection
    - Label consistency checks
    - Source verification
    - Temporal anomaly detection
    - Feature distribution analysis
    """

    def __init__(self, contamination_threshold: float = 0.05):
        self.contamination_threshold = contamination_threshold
        self._baseline_stats: Optional[Dict] = None

    def analyze_dataset(self, data: List[DataPoint]) -> Dict:
        """
        Comprehensive dataset analysis for poisoning detection.

        Returns detailed analysis report.
        """
        if not data:
            return {"clean": True, "issues": [], "suspicious_points": []}

        issues = []
        suspicious = []

        # 1. Statistical outlier detection
        outlier_results = self._detect_statistical_outliers(data)
        issues.extend(outlier_results["issues"])
        suspicious.extend(outlier_results["suspicious_indices"])

        # 2. Label consistency check
        label_results = self._check_label_consistency(data)
        issues.extend(label_results["issues"])

        # 3. Source analysis
        source_results = self._analyze_sources(data)
        issues.extend(source_results["issues"])

        # 4. Temporal analysis
        temporal_results = self._analyze_temporal_patterns(data)
        issues.extend(temporal_results["issues"])

        # 5. Feature distribution analysis
        dist_results = self._analyze_feature_distributions(data)
        issues.extend(dist_results["issues"])

        # Calculate risk score
        risk_score = min(1.0, len(issues) * 0.15 + len(suspicious) * 0.05)

        return {
            "clean": risk_score < self.contamination_threshold,
            "risk_score": risk_score,
            "issues": issues,
            "suspicious_count": len(suspicious),
            "total_samples": len(data),
            "recommendations": self._generate_recommendations(issues),
        }

    def _detect_statistical_outliers(self, data: List[DataPoint]) -> Dict:
        """Detect statistical outliers using Z-score."""
        issues = []
        suspicious = []

        if len(data) < 10:
            return {"issues": [], "suspicious_indices": []}

        # Calculate feature statistics
        all_features = [dp.features for dp in data]
        n_features = len(all_features[0])

        for feat_idx in range(n_features):
            values = [f[feat_idx] for f in all_features]
            mean = sum(values) / len(values)
            variance = sum((v - mean) ** 2 for v in values) / len(values)
            std = math.sqrt(variance) if variance > 0 else 1e-10

            for i, dp in enumerate(data):
                z_score = abs(dp.features[feat_idx] - mean) / std
                if z_score > 3.0:  # 3 standard deviations
                    dp.is_suspicious = True
                    suspicious.append(i)
                    issues.append({
                        "type": "statistical_outlier",
                        "severity": "medium",
                        "sample_index": i,
                        "feature": feat_idx,
                        "z_score": round(z_score, 2),
                        "message": f"Sample {i} feature {feat_idx} is {z_score:.1f} std devs from mean",
                    })

        return {"issues": issues, "suspicious_indices": list(set(suspicious))}

    def _check_label_consistency(self, data: List[DataPoint]) -> Dict:
        """Check for label inconsistencies that may indicate poisoning."""
        issues = []

        # Group by feature similarity
        label_groups = defaultdict(list)
        for i, dp in enumerate(data):
            # Simple grouping by rounding features
            key = tuple(round(f, 1) for f in dp.features[:3])
            label_groups[key].append((i, dp.label))

        # Check for mixed labels in similar samples
        for key, group in label_groups.items():
            if len(group) < 2:
                continue

            labels = [label for _, label in group]
            if len(set(str(l) for l in labels)) > 1:
                issues.append({
                    "type": "label_inconsistency",
                    "severity": "high",
                    "message": f"Similar samples have different labels: {labels}",
                    "sample_indices": [i for i, _ in group],
                })

        return {"issues": issues}

    def _analyze_sources(self, data: List[DataPoint]) -> Dict:
        """Analyze data sources for potential poisoning."""
        issues = []

        source_counts = Counter(dp.source for dp in data)
        total = len(data)

        for source, count in source_counts.items():
            proportion = count / total

            # Check for single dominant source
            if proportion > 0.8 and len(source_counts) > 1:
                issues.append({
                    "type": "source_dominance",
                    "severity": "medium",
                    "source": source,
                    "proportion": round(proportion, 3),
                    "message": f"Source '{source}' provides {proportion:.1%} of data",
                })

            # Check for unknown/untrusted sources
            if source.startswith("unknown") or source.startswith("unverified"):
                issues.append({
                    "type": "untrusted_source",
                    "severity": "high",
                    "source": source,
                    "count": count,
                    "message": f"Data from untrusted source: '{source}'",
                })

        return {"issues": issues}

    def _analyze_temporal_patterns(self, data: List[DataPoint]) -> Dict:
        """Detect temporal anomalies in data collection."""
        issues = []

        if len(data) < 5:
            return {"issues": []}

        # Sort by timestamp
        sorted_data = sorted(data, key=lambda dp: dp.timestamp)

        # Check for burst additions
        time_diffs = []
        for i in range(1, len(sorted_data)):
            diff = sorted_data[i].timestamp - sorted_data[i-1].timestamp
            time_diffs.append(diff)

        if time_diffs:
            mean_diff = sum(time_diffs) / len(time_diffs)
            # Detect bursts (many additions in short time)
            burst_threshold = mean_diff * 0.1 if mean_diff > 0 else 1
            bursts = sum(1 for d in time_diffs if d < burst_threshold)

            if bursts > len(time_diffs) * 0.3:
                issues.append({
                    "type": "temporal_burst",
                    "severity": "medium",
                    "burst_count": bursts,
                    "message": f"Detected {bursts} rapid data additions (possible injection)",
                })

        return {"issues": issues}

    def _analyze_feature_distributions(self, data: List[DataPoint]) -> Dict:
        """Analyze feature distributions for anomalies."""
        issues = []

        if len(data) < 20:
            return {"issues": []}

        # Check for bimodal distributions (possible mixed clean/poisoned data)
        all_features = [dp.features for dp in data]
        n_features = len(all_features[0])

        for feat_idx in range(min(n_features, 5)):  # Check first 5 features
            values = sorted([f[feat_idx] for f in all_features])

            # Simple bimodality check: split into halves and compare means
            mid = len(values) // 2
            lower_mean = sum(values[:mid]) / mid if mid > 0 else 0
            upper_mean = sum(values[mid:]) / (len(values) - mid) if len(values) > mid else 0

            mean = sum(values) / len(values)
            if mean != 0:
                separation = abs(upper_mean - lower_mean) / abs(mean)
                if separation > 2.0:
                    issues.append({
                        "type": "bimodal_distribution",
                        "severity": "medium",
                        "feature": feat_idx,
                        "separation": round(separation, 2),
                        "message": f"Feature {feat_idx} shows bimodal pattern (possible poisoning)",
                    })

        return {"issues": issues}

    def _generate_recommendations(self, issues: List[Dict]) -> List[str]:
        """Generate recommendations based on detected issues."""
        recommendations = []
        issue_types = {i["type"] for i in issues}

        if "statistical_outlier" in issue_types:
            recommendations.append("Review and potentially remove statistical outliers")
        if "label_inconsistency" in issue_types:
            recommendations.append("Manually verify labels for similar samples with different labels")
        if "source_dominance" in issue_types:
            recommendations.append("Diversify data sources to reduce single-source dependency")
        if "untrusted_source" in issue_types:
            recommendations.append("Verify data from untrusted sources before training")
        if "temporal_burst" in issue_types:
            recommendations.append("Investigate rapid data additions for potential injection")
        if "bimodal_distribution" in issue_types:
            recommendations.append("Investigate bimodal feature distributions for mixed data")

        return recommendations


# =============================================================
# SECTION 2: Adversarial Attack Detection & Defense
# =============================================================

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

    def detect_adversarial(self, input_features: List[float], model_fn: Callable) -> Dict:
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
            reasons.append("Model predictions change significantly with feature squeezing")

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
                round(f * (2 ** squeeze_bit_depth)) / (2 ** squeeze_bit_depth)
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
                if isinstance(orig_pred, (int, float)) and isinstance(pert_pred, (int, float)):
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
            "robustness_score": (correct_fgsm + correct_pgd) / (2 * total) if total > 0 else 0,
            "total_samples": total,
            "epsilon": epsilon,
        }

        self._attack_results.append(results)
        return results


# =============================================================
# SECTION 3: Model Theft Prevention
# =============================================================

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
        self._query_log[model_id].append({
            "user_id": user_id,
            "timestamp": now,
            "query_type": query_type,
        })

        model["total_queries"] += 1
        model["unique_users"].add(user_id)

        # Check rate limits
        limits = self._rate_limits.get(model_id, {})
        recent_minute = sum(
            1 for q in self._query_log[model_id]
            if now - q["timestamp"] < 60
        )
        recent_hour = sum(
            1 for q in self._query_log[model_id]
            if now - q["timestamp"] < 3600
        )

        if recent_minute > limits.get("per_minute", 50):
            return {"allowed": False, "reason": "Rate limit exceeded (per minute)"}
        if recent_hour > limits.get("per_hour", 2000):
            return {"allowed": False, "reason": "Rate limit exceeded (per hour)"}

        # Anomaly detection
        anomaly = self._detect_query_anomaly(model_id, user_id)
        if anomaly["is_anomalous"]:
            return {"allowed": False, "reason": "Anomalous query pattern detected"}

        return {"allowed": True, "remaining_minute": limits.get("per_minute", 50) - recent_minute}

    def _detect_query_anomaly(self, model_id: str, user_id: str) -> Dict:
        """Detect anomalous query patterns that may indicate extraction."""
        recent_queries = [
            q for q in self._query_log[model_id]
            if time.time() - q["timestamp"] < 3600 and q["user_id"] == user_id
        ]

        if len(recent_queries) < 10:
            return {"is_anomalous": False}

        # Check for systematic probing
        # (e.g., queries that vary in small increments)
        timestamps = [q["timestamp"] for q in recent_queries]
        intervals = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]

        if intervals:
            # Check for very regular intervals (bot-like behavior)
            mean_interval = sum(intervals) / len(intervals)
            variance = sum((i - mean_interval)**2 for i in intervals) / len(intervals)
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
            return {"watermarked": False, "reason": "No watermark registered for this model"}

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
                        anomalies.append({
                            "sample_index": i,
                            "expected": label,
                            "predicted": pred,
                            "perturbation_sensitivity": diff_score,
                        })
            except Exception as e:
                anomalies.append({
                    "sample_index": i,
                    "error": str(e),
                })

        # Analyze prediction distribution
        pred_counter = Counter(predictions)
        label_counter = Counter(expected_labels)

        distribution_shift = 0
        for label in set(list(pred_counter.keys()) + list(label_counter.keys())):
            pred_ratio = pred_counter.get(label, 0) / len(predictions) if predictions else 0
            true_ratio = label_counter.get(label, 0) / len(expected_labels) if expected_labels else 0
            distribution_shift += abs(pred_ratio - true_ratio)

        return {
            "backdoor_suspected": distribution_shift > 0.3 or len(anomalies) > len(test_inputs) * 0.1,
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

                if isinstance(original, (int, float)) and isinstance(perturbed_pred, (int, float)):
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
                sum((p - c) ** 2 for p, c in zip(point[:len(centroid)], centroid))
            )
            total += dist
        return total / len(data) if data else 0


# =============================================================
# SECTION 6: Secure Model Serving
# =============================================================

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

    def register_model(self, model_id: str, model_fn: Callable, sensitivity: str = "medium"):
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
        adv_check = self._adversarial_detector.detect_adversarial(
            features, model["fn"]
        )
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
        self._query_log.append({
            "model_id": model_id,
            "user_id": user_id,
            "timestamp": time.time(),
            "latency": time.time() - start_time,
        })

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
        bucket["tokens"] = min(self.capacity, bucket["tokens"] + elapsed * self.refill_rate)
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

def demo_poisoning_detection():
    """Demonstrate data poisoning detection."""
    print("\n" + "=" * 60)
    print("DEMO 1: Training Data Poisoning Detection")
    print("=" * 60)

    detector = DataPoisoningDetector()

    # Create clean dataset
    clean_data = [
        DataPoint(features=[random.gauss(0, 1) for _ in range(5)], label=i % 2, source="trusted")
        for i in range(100)
    ]

    # Inject poisoned data
    poisoned_data = clean_data.copy()
    for _ in range(10):
        poisoned_data.append(DataPoint(
            features=[100 + random.gauss(0, 0.1) for _ in range(5)],  # Outliers
            label=0,  # Wrong label
            source="unknown_attacker",
        ))

    print("Analyzing clean dataset...")
    clean_result = detector.analyze_dataset(clean_data)
    print(f"  Risk score: {clean_result['risk_score']:.3f}")
    print(f"  Clean: {clean_result['clean']}")
    print(f"  Issues: {len(clean_result['issues'])}")

    print("\nAnalyzing poisoned dataset...")
    poisoned_result = detector.analyze_dataset(poisoned_data)
    print(f"  Risk score: {poisoned_result['risk_score']:.3f}")
    print(f"  Clean: {poisoned_result['clean']}")
    print(f"  Issues: {len(poisoned_result['issues'])}")
    print(f"  Suspicious samples: {poisoned_result['suspicious_count']}")

    if poisoned_result['issues']:
        print("\n  Sample issues:")
        for issue in poisoned_result['issues'][:3]:
            print(f"    - [{issue['severity']}] {issue['message']}")

    if poisoned_result['recommendations']:
        print("\n  Recommendations:")
        for rec in poisoned_result['recommendations']:
            print(f"    -> {rec}")

    print("\n[OK] Poisoning detection demonstrated")


def demo_adversarial_detection():
    """Demonstrate adversarial attack detection."""
    print("\n" + "=" * 60)
    print("DEMO 2: Adversarial Attack Detection & Robustness")
    print("=" * 60)

    # Simple model function
    def simple_model(features):
        """Simple linear model for demonstration."""
        weights = [0.5, -0.3, 0.8, 0.1, -0.2]
        return sum(f * w for f, w in zip(features[:5], weights)) > 0

    detector = AdversarialDetector(sensitivity=0.4)

    # Update baseline with clean data
    for _ in range(100):
        clean_input = [random.gauss(0, 1) for _ in range(5)]
        pred = simple_model(clean_input)
        detector.update_baseline(clean_input, pred)

    # Test with clean input
    clean_input = [0.1, -0.2, 0.3, 0.0, -0.1]
    result = detector.detect_adversarial(clean_input, simple_model)
    print(f"Clean input: adversarial={result['is_adversarial']}, confidence={result['confidence']:.3f}")

    # Test with adversarial input
    adversarial_input = [100, -200, 150, 50, -100]
    result = detector.detect_adversarial(adversarial_input, simple_model)
    print(f"Adversarial input: adversarial={result['is_adversarial']}, confidence={result['confidence']:.3f}")
    if result['reasons']:
        for reason in result['reasons']:
            print(f"  Reason: {reason}")

    # Robustness testing
    print("\nRobustness Evaluation:")
    tester = AdversarialRobustnessTester()
    test_data = [([random.gauss(0, 1) for _ in range(5)], random.randint(0, 1)) for _ in range(50)]

    robustness = tester.evaluate_robustness(test_data, simple_model, epsilon=0.1)
    print(f"  Clean accuracy: {robustness['clean_accuracy']:.1%}")
    print(f"  FGSM accuracy: {robustness['fgsm_accuracy']:.1%}")
    print(f"  PGD accuracy: {robustness['pgd_accuracy']:.1%}")
    print(f"  Robustness score: {robustness['robustness_score']:.3f}")

    print("\n[OK] Adversarial detection demonstrated")


def demo_watermarking():
    """Demonstrate model watermarking."""
    print("\n" + "=" * 60)
    print("DEMO 3: Model Watermarking")
    print("=" * 60)

    watermarker = ModelWatermarker()

    # Create watermark
    watermark_info = watermarker.create_watermark(
        model_id="gpt-custom-v1",
        owner_id="company-xyz",
    )
    print(f"Watermark created:")
    print(f"  Model ID: {watermark_info['model_id']}")
    print(f"  Watermark ID: {watermark_info['watermark_id']}")
    print(f"  Triggers embedded: {watermark_info['triggers_embedded']}")

    # Simulate model with watermark
    def watermarked_model(features):
        """Model that responds to trigger patterns."""
        # Simple deterministic output based on input
        return hash(tuple(features)) % 10 / 10.0

    # Verify watermark
    verification = watermarker.verify_watermark("gpt-custom-v1", watermarked_model)
    print(f"\nWatermark verification:")
    print(f"  Watermarked: {verification['watermarked']}")
    print(f"  Match ratio: {verification['match_ratio']:.1%}")
    print(f"  Confidence: {verification['confidence']:.3f}")

    print("\n[OK] Watermarking demonstrated")


def demo_backdoor_detection():
    """Demonstrate backdoor detection."""
    print("\n" + "=" * 60)
    print("DEMO 4: Backdoor Detection")
    print("=" * 60)

    detector = BackdoorDetector()

    # Simulate clean model
    def clean_model(features):
        """Simple model without backdoor."""
        return sum(features) > 0

    # Test clean model
    test_inputs = [[random.gauss(0, 1) for _ in range(5)] for _ in range(100)]
    expected_labels = [1 if sum(f) > 0 else 0 for f in test_inputs]

    result = detector.analyze_model_behavior(clean_model, test_inputs, expected_labels)
    print(f"Clean model analysis:")
    print(f"  Backdoor suspected: {result['backdoor_suspected']}")
    print(f"  Anomaly count: {result['anomaly_count']}")
    print(f"  Distribution shift: {result['distribution_shift']}")

    # Activation clustering
    clean_acts = [[random.gauss(0, 1) for _ in range(10)] for _ in range(50)]
    suspect_acts = [[random.gauss(5, 1) for _ in range(10)] for _ in range(50)]

    cluster_result = detector.activation_clustering_analysis(clean_acts, suspect_acts)
    print(f"\nActivation clustering:")
    print(f"  Separation detected: {cluster_result['separation_detected']}")
    print(f"  Separation ratio: {cluster_result['separation_ratio']}")

    print("\n[OK] Backdoor detection demonstrated")


def demo_secure_serving():
    """Demonstrate secure model serving."""
    print("\n" + "=" * 60)
    print("DEMO 5: Secure Model Serving")
    print("=" * 60)

    server = SecureModelServer()

    # Register model
    def dummy_model(features):
        """Dummy prediction model."""
        return sum(f * 0.1 for f in features)

    server.register_model("sentiment-v1", dummy_model, sensitivity="high")

    # Normal request
    result = server.predict("sentiment-v1", [0.5, -0.3, 0.8], user_id="user1")
    print(f"Normal prediction: {result.get('prediction', result.get('error'))}")

    # Adversarial request
    result = server.predict("sentiment-v1", [1000, -2000, 3000], user_id="attacker")
    print(f"Adversarial request: {result.get('error', 'passed')}")

    # Rate limit test
    for i in range(55):
        result = server.predict("sentiment-v1", [0.1, 0.2, 0.3], user_id="spammer")
    print(f"After 55 rapid requests: {result.get('error', 'passed')}")

    print("\n[OK] Secure model serving demonstrated")


# =============================================================
# ATTACK PATTERNS & DEFENSES
# =============================================================

ATTACK_PATTERNS = """
+==============================================================+
|              AI MODEL SECURITY ATTACKS                       |
+==============================================================+
|                                                              |
|  1. DATA POISONING                                           |
|     Attack: Inject malicious training data                   |
|     Defense: Data validation, anomaly detection, provenance  |
|                                                              |
|  2. ADVERSARIAL EXAMPLES                                     |
|     Attack: Craft inputs to fool models                      |
|     Defense: Adversarial training, input validation          |
|                                                              |
|  3. MODEL EXTRACTION                                         |
|     Attack: Query model to reconstruct architecture          |
|     Defense: Rate limiting, output perturbation, watermarking|
|                                                              |
|  4. MODEL INVERSION                                          |
|     Attack: Recover training data from model                 |
|     Defense: Differential privacy, output limiting           |
|                                                              |
|  5. BACKDOOR INJECTION                                       |
|     Attack: Insert hidden triggers in model                  |
|     Defense: Neural cleanse, activation clustering           |
|                                                              |
|  6. MODEL TAMPERING                                          |
|     Attack: Modify model weights post-deployment             |
|     Defense: Model signing, integrity verification           |
|                                                              |
+==============================================================+
"""


# =============================================================
# MAIN EXECUTION
# =============================================================

if __name__ == "__main__":
    print("+==============================================================+")
    print("|          Topic 08: AI Model Security                         |")
    print("+==============================================================+")

    random.seed(42)  # Reproducibility

    try:
        demo_poisoning_detection()
        demo_adversarial_detection()
        demo_watermarking()
        demo_backdoor_detection()
        demo_secure_serving()

        print(ATTACK_PATTERNS)

        print("\n" + "=" * 60)
        print("[OK] ALL MODEL SECURITY DEMOS COMPLETED")
        print("=" * 60)

    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
