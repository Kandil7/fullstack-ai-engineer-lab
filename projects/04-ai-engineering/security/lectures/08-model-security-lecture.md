# Lecture 08: Model Security

## Topic Overview

Model security focuses on protecting AI models from adversarial attacks, model theft, data poisoning, and other threats that compromise model integrity. This lecture covers adversarial examples, model extraction, data poisoning, model robustness testing, and defensive strategies. Securing AI models is essential for maintaining trust and preventing misuse.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Understand** common adversarial attacks on ML models
2. **Implement** defenses against adversarial examples
3. **Detect** model extraction attempts
4. **Prevent** data poisoning attacks
5. **Test** model robustness systematically
6. **Apply** model security best practices
7. **Design** secure model deployment architectures

---

## Key Concepts

### 1. Adversarial Attacks

```python
import numpy as np
from typing import Tuple, Optional

class AdversarialAttack:
    """Base class for adversarial attacks."""

    def __init__(self, model, epsilon: float = 0.1):
        self.model = model
        self.epsilon = epsilon

    def attack(self, x: np.ndarray, y: int) -> np.ndarray:
        raise NotImplementedError

class FGSMAttack(AdversarialAttack):
    """Fast Gradient Sign Method attack."""

    def attack(self, x: np.ndarray, y: int) -> np.ndarray:
        """Generate adversarial example using FGSM."""
        # Compute gradient
        x_tensor = np.expand_dims(x, axis=0)
        gradient = self._compute_gradient(x_tensor, y)

        # Apply perturbation
        perturbation = self.epsilon * np.sign(gradient)
        x_adv = x + perturbation[0]

        # Clip to valid range
        x_adv = np.clip(x_adv, 0, 1)

        return x_adv

    def _compute_gradient(self, x: np.ndarray, y: int) -> np.ndarray:
        """Compute gradient of loss w.r.t. input."""
        # Simplified - in practice use autograd
        return np.random.randn(*x.shape) * 0.01

class PGDAttack(AdversarialAttack):
    """Projected Gradient Descent attack."""

    def attack(self, x: np.ndarray, y: int,
               num_steps: int = 10, step_size: float = 0.01) -> np.ndarray:
        """Generate adversarial example using PGD."""
        x_adv = x.copy()

        for _ in range(num_steps):
            # Compute gradient
            gradient = self._compute_gradient(
                np.expand_dims(x_adv, axis=0), y
            )

            # Update with step
            x_adv = x_adv + step_size * np.sign(gradient[0])

            # Project back to epsilon ball
            perturbation = x_adv - x
            perturbation = np.clip(perturbation, -self.epsilon, self.epsilon)
            x_adv = x + perturbation

            # Clip to valid range
            x_adv = np.clip(x_adv, 0, 1)

        return x_adv

    def _compute_gradient(self, x: np.ndarray, y: int) -> np.ndarray:
        return np.random.randn(*x.shape) * 0.01

class BackdoorAttack:
    """Backdoor/Trojan attack on models."""

    def __init__(self, trigger_pattern: np.ndarray, target_label: int):
        self.trigger_pattern = trigger_pattern
        self.target_label = target_label

    def inject_backdoor(self, x: np.ndarray) -> np.ndarray:
        """Add trigger pattern to input."""
        # Add trigger pattern
        x_poisoned = x + self.trigger_pattern
        return np.clip(x_poisoned, 0, 1)

    def create_poisoned_dataset(self, dataset: list,
                                 poison_rate: float = 0.1) -> list:
        """Create poisoned training dataset."""
        poisoned = []
        for x, y in dataset:
            if np.random.random() < poison_rate:
                x_backdoor = self.inject_backdoor(x)
                poisoned.append((x_backdoor, self.target_label))
            else:
                poisoned.append((x, y))
        return poisoned
```

### 2. Model Extraction

```python
import time
from typing import List, Dict

class ModelExtractionDetector:
    """Detect attempts to extract model via API queries."""

    def __init__(self):
        self.query_history: Dict[str, List[Dict]] = {}
        self.baseline_query_rate = 100  # queries per minute

    def log_query(self, user_id: str, query: Dict):
        """Log API query for analysis."""
        if user_id not in self.query_history:
            self.query_history[user_id] = []

        self.query_history[user_id].append({
            "timestamp": time.time(),
            "input": query.get("input"),
            "output": query.get("output"),
        })

    def detect_extraction_attempt(self, user_id: str) -> Dict:
        """Detect if user is trying to extract model."""
        if user_id not in self.query_history:
            return {"suspicious": False}

        queries = self.query_history[user_id]

        # Check 1: High query rate
        recent_queries = [
            q for q in queries
            if q["timestamp"] > time.time() - 3600
        ]
        query_rate = len(recent_queries) / 60  # queries per minute

        if query_rate > self.baseline_query_rate * 10:
            return {
                "suspicious": True,
                "reason": "abnormally_high_query_rate",
                "query_rate": query_rate,
            }

        # Check 2: Systematic input coverage
        if self._detect_systematic_sampling(recent_queries):
            return {
                "suspicious": True,
                "reason": "systematic_input_sampling",
            }

        # Check 3: Output confidence analysis
        if self._detect_confidence_probing(recent_queries):
            return {
                "suspicious": True,
                "reason": "confidence_probing",
            }

        return {"suspicious": False}

    def _detect_systematic_sampling(self, queries: list) -> bool:
        """Detect systematic input sampling patterns."""
        if len(queries) < 100:
            return False

        # Check if inputs are evenly distributed
        inputs = [q["input"] for q in queries]
        # Simplified check - in practice, analyze distribution
        return False

    def _detect_confidence_probing(self, queries: list) -> bool:
        """Detect confidence score probing."""
        # Check if queries are near decision boundaries
        outputs = [q["output"] for q in queries]
        # Look for queries with very close confidence scores
        return False

class ModelWatermarking:
    """Watermark models to prove ownership."""

    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def generate_watermark_inputs(self, n: int = 100) -> list:
        """Generate watermark trigger inputs."""
        np.random.seed(hash(self.secret_key) % (2**32))
        watermark_inputs = []
        for _ in range(n):
            # Generate trigger based on secret key
            trigger = np.random.randn(10)  # Example: 10-dimensional
            watermark_inputs.append(trigger)
        return watermark_inputs

    def verify_watermark(self, model, watermark_inputs: list,
                         expected_outputs: list) -> Dict:
        """Verify model contains watermark."""
        correct = 0
        for x, expected in zip(watermark_inputs, expected_outputs):
            prediction = model.predict(x.reshape(1, -1))
            if prediction[0] == expected:
                correct += 1

        accuracy = correct / len(watermark_inputs)
        return {
            "watermarked": accuracy > 0.95,
            "accuracy": accuracy,
            "threshold": 0.95,
        }
```

### 3. Data Poisoning Defense

```python
class DataPoisoningDefense:
    """Defend against data poisoning attacks."""

    def __init__(self):
        self.anomaly_threshold = 3.0  # Standard deviations

    def detect_poisoned_samples(self, dataset: list) -> list:
        """Detect potentially poisoned training samples."""
        # Extract features
        features = np.array([self._extract_features(x) for x, _ in dataset])

        # Compute statistics
        mean = np.mean(features, axis=0)
        std = np.std(features, axis=0)

        # Find outliers
        poisoned_indices = []
        for i, (x, y) in enumerate(dataset):
            feature = self._extract_features(x)
            z_scores = np.abs((feature - mean) / (std + 1e-8))

            if np.any(z_scores > self.anomaly_threshold):
                poisoned_indices.append(i)

        return poisoned_indices

    def _extract_features(self, x) -> np.ndarray:
        """Extract statistical features from input."""
        if isinstance(x, np.ndarray):
            return np.array([
                np.mean(x),
                np.std(x),
                np.min(x),
                np.max(x),
            ])
        return np.array([0, 0, 0, 0])

    def apply_robust_training(self, dataset: list) -> list:
        """Apply robust training techniques."""
        # Remove detected poisoned samples
        poisoned = self.detect_poisoned_samples(dataset)
        clean_dataset = [
            (x, y) for i, (x, y) in enumerate(dataset)
            if i not in poisoned
        ]
        return clean_dataset

    def label_flipping_detection(self, dataset: list,
                                  known_labels: dict) -> list:
        """Detect label flipping attacks."""
        suspicious = []

        for i, (x, y) in enumerate(dataset):
            # Use a trusted subset to verify labels
            if i in known_labels:
                if y != known_labels[i]:
                    suspicious.append({
                        "index": i,
                        "expected": known_labels[i],
                        "actual": y,
                    })

        return suspicious
```

### 4. Model Robustness Testing

```python
class RobustnessTestSuite:
    """Test suite for model robustness."""

    def __init__(self, model):
        self.model = model
        self.results = []

    def test_adversarial_robustness(self, test_data: list,
                                     epsilon: float = 0.1) -> Dict:
        """Test model against adversarial examples."""
        correct_clean = 0
        correct_adv = 0
        total = len(test_data)

        attack = FGSMAttack(self.model, epsilon)

        for x, y in test_data:
            # Test clean accuracy
            pred_clean = self.model.predict(x.reshape(1, -1))
            if pred_clean[0] == y:
                correct_clean += 1

            # Test adversarial accuracy
            x_adv = attack.attack(x, y)
            pred_adv = self.model.predict(x_adv.reshape(1, -1))
            if pred_adv[0] == y:
                correct_adv += 1

        return {
            "clean_accuracy": correct_clean / total,
            "adversarial_accuracy": correct_adv / total,
            "robustness_drop": (correct_clean - correct_adv) / total,
            "epsilon": epsilon,
        }

    def test_input_perturbation(self, test_data: list,
                                 noise_levels: list = [0.01, 0.05, 0.1]) -> Dict:
        """Test model robustness to random noise."""
        results = {}

        for noise in noise_levels:
            correct = 0
            for x, y in test_data:
                x_noisy = x + np.random.randn(*x.shape) * noise
                x_noisy = np.clip(x_noisy, 0, 1)

                pred = self.model.predict(x_noisy.reshape(1, -1))
                if pred[0] == y:
                    correct += 1

            results[f"noise_{noise}"] = correct / len(test_data)

        return results

    def test_distribution_shift(self, original_data: list,
                                 shifted_data: list) -> Dict:
        """Test model performance on shifted distribution."""
        # Accuracy on original
        correct_original = sum(
            1 for x, y in original_data
            if self.model.predict(x.reshape(1, -1))[0] == y
        )

        # Accuracy on shifted
        correct_shifted = sum(
            1 for x, y in shifted_data
            if self.model.predict(x.reshape(1, -1))[0] == y
        )

        return {
            "original_accuracy": correct_original / len(original_data),
            "shifted_accuracy": correct_shifted / len(shifted_data),
            "performance_drop": (correct_original - correct_shifted) / len(original_data),
        }

    def run_full_test_suite(self, test_data: list) -> Dict:
        """Run complete robustness test suite."""
        results = {
            "adversarial": self.test_adversarial_robustness(test_data),
            "perturbation": self.test_input_perturbation(test_data),
            "overall_score": 0.0,
        }

        # Calculate overall robustness score
        results["overall_score"] = (
            results["adversarial"]["adversarial_accuracy"] * 0.5 +
            results["perturbation"]["noise_0.01"] * 0.3 +
            results["perturbation"]["noise_0.05"] * 0.2
        )

        return results
```

---

## Common Mistakes to Avoid

1. **Not testing for adversarial robustness** — Always test with adversarial examples
2. **Ignoring data quality** — Poisoned data leads to compromised models
3. **No model monitoring** — Monitor for distribution shift and attacks
4. **Trusting predictions blindly** — Validate model outputs
5. **Not securing model artifacts** — Protect model files from theft
6. **Skipping robustness testing** — Include in CI/CD pipeline
7. **Ignoring edge cases** — Test with out-of-distribution inputs
8. **No watermarking** — Mark models to prove ownership

---

## Best Practices

1. **Adversarial training** — Train with adversarial examples
2. **Input validation** — Validate inputs against expected distribution
3. **Model monitoring** — Track performance and anomalies
4. **Data validation** — Verify training data integrity
5. **Model watermarking** — Mark models for ownership proof
6. **Access controls** — Restrict who can query the model
7. **Rate limiting** — Prevent model extraction via bulk queries
8. **Regular testing** — Include robustness tests in CI/CD

---

## Practice Exercises

### Exercise 1: FGSM Attack (Medium)
Implement FGSM attack and test model vulnerability.

### Exercise 2: Robustness Testing (Medium)
Build a test suite for model robustness evaluation.

### Exercise 3: Data Poisoning Detection (Hard)
Create a system to detect poisoned training data.

### Exercise 4: Model Extraction Detection (Hard)
Implement detection for model extraction attempts.

---

## Summary

Model security protects AI from adversarial manipulation. Key takeaways:

- **Adversarial examples** can fool models with tiny perturbations
- **Model extraction** can steal models via API queries
- **Data poisoning** can compromise models during training
- **Robustness testing** is essential for reliable AI
- **Defensive techniques** include adversarial training, input validation, and monitoring
- **Model watermarking** helps prove ownership

---

## References

- [Adversarial Examples in ML](https://arxiv.org/abs/1412.6575)
- [Model Extraction Attacks](https://arxiv.org/abs/1911.01185)
- [Data Poisoning Attacks](https://arxiv.org/abs/2006.05309)
