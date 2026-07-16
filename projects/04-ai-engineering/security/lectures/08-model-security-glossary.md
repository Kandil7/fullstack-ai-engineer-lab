# Glossary 08: Model Security Terms

## Quick Reference Table

| Term | Category | Importance | See Also |
|------|----------|------------|----------|
| Adversarial Example | Attack | Critical | FGSM, PGD |
| Model Extraction | Attack | Critical | Model Stealing |
| Data Poisoning | Attack | Critical | Training Data Attack |
| Model Robustness | Property | Critical | Robustness |
| Backdoor Attack | Attack | Critical | Trojan, Trigger |
| Model Watermarking | Defense | High | Ownership Proof |
| Adversarial Training | Defense | Critical | Robust Training |
| FGSM | Attack | High | Gradient Attack |
| PGD | Attack | High | Iterative Attack |
| Evasion Attack | Attack | Critical | Adversarial Example |
| Model Inversion | Attack | High | Privacy Attack |
| Membership Inference | Attack | High | Privacy Attack |
| Distribution Shift | Concept | High | Covariate Shift |
| Robustness Testing | Process | Critical | Adversarial Testing |
| Model Integrity | Property | Critical | Tamper Detection |
| Trigger Pattern | Attack Component | High | Backdoor |

---

## Alphabetical Definitions

### Adversarial Example

**Definition**: An input that has been slightly modified to cause a machine learning model to make a mistake, often imperceptible to humans.

**Example**:
```python
import numpy as np

def create_adversarial_example(model, x: np.ndarray, y: int,
                                epsilon: float = 0.1) -> np.ndarray:
    """Create adversarial example using FGSM."""
    # Compute gradient
    gradient = compute_gradient(model, x, y)

    # Add perturbation
    x_adv = x + epsilon * np.sign(gradient)

    # Clip to valid range
    x_adv = np.clip(x_adv, 0, 1)

    return x_adv

# Example usage
x = np.random.rand(28, 28)  # Random image
y = 5  # True label
x_adv = create_adversarial_example(model, x, y, epsilon=0.1)

# Check if attack succeeded
pred_original = model.predict(x.reshape(1, -1))
pred_adversarial = model.predict(x_adv.reshape(1, -1))
print(f"Original prediction: {pred_original}")
print(f"Adversarial prediction: {pred_adversarial}")
```

**Related Terms**: FGSM, PGD, Evasion Attack, Perturbation

---

### Adversarial Robustness

**Definition**: The ability of a model to maintain accuracy when inputs are perturbed by adversarial attacks.

**Example**:
```python
class RobustnessEvaluator:
    def __init__(self, model):
        self.model = model

    def evaluate_robustness(self, test_data: list,
                            epsilon: float = 0.1) -> dict:
        """Evaluate model robustness against FGSM attack."""
        correct_clean = 0
        correct_adv = 0
        total = len(test_data)

        for x, y in test_data:
            # Clean accuracy
            pred = self.model.predict(x.reshape(1, -1))
            if pred[0] == y:
                correct_clean += 1

            # Adversarial accuracy
            x_adv = create_adversarial_example(self.model, x, y, epsilon)
            pred_adv = self.model.predict(x_adv.reshape(1, -1))
            if pred_adv[0] == y:
                correct_adv += 1

        return {
            "clean_accuracy": correct_clean / total,
            "robust_accuracy": correct_adv / total,
            "robustness_gap": (correct_clean - correct_adv) / total,
        }
```

**Related Terms**: Adversarial Training, Robustness Testing, Accuracy

---

### Adversarial Training

**Definition**: A training technique where adversarial examples are included in the training data to improve model robustness.

**Example**:
```python
def adversarial_training(model, train_data, epochs: int = 10,
                         epsilon: float = 0.1):
    """Train model with adversarial examples."""
    for epoch in range(epochs):
        for x, y in train_data:
            # Generate adversarial example
            x_adv = create_adversarial_example(model, x, y, epsilon)

            # Train on both clean and adversarial
            model.train_on_batch(x.reshape(1, -1), np.array([y]))
            model.train_on_batch(x_adv.reshape(1, -1), np.array([y]))

    return model
```

**Related Terms**: Data Augmentation, Robust Training, FGSM

---

### Backdoor Attack

**Definition**: An attack where a trigger pattern is embedded in training data, causing the model to behave abnormally when the trigger is present at inference.

**Example**:
```python
class BackdoorAttack:
    def __init__(self, trigger_size: int = 3, target_label: int = 0):
        self.trigger = np.ones((trigger_size, trigger_size))
        self.target_label = target_label

    def poison_dataset(self, dataset: list,
                       poison_rate: float = 0.1) -> list:
        """Add backdoor triggers to training data."""
        poisoned = []
        for x, y in dataset:
            if np.random.random() < poison_rate:
                # Add trigger to image
                x_backdoored = x.copy()
                x_backdoored[:self.trigger.shape[0], :self.trigger.shape[1]] = self.trigger

                # Change label to target
                poisoned.append((x_backdoored, self.target_label))
            else:
                poisoned.append((x, y))

        return poisoned

    def test_backdoor(self, model, test_data: list) -> dict:
        """Test if backdoor is active."""
        trigger_accuracy = 0
        clean_accuracy = 0
        total = len(test_data)

        for x, y in test_data:
            # Test with trigger
            x_triggered = x.copy()
            x_triggered[:self.trigger.shape[0], :self.trigger.shape[1]] = self.trigger
            pred_triggered = model.predict(x_triggered.reshape(1, -1))

            if pred_triggered[0] == self.target_label:
                trigger_accuracy += 1

            # Test without trigger
            pred_clean = model.predict(x.reshape(1, -1))
            if pred_clean[0] == y:
                clean_accuracy += 1

        return {
            "backdoor_success_rate": trigger_accuracy / total,
            "clean_accuracy": clean_accuracy / total,
        }
```

**Related Terms**: Trojan Attack, Trigger Pattern, Data Poisoning

---

### Data Poisoning

**Definition**: An attack where malicious data is injected into the training dataset to compromise model behavior.

**Example**:
```python
class DataPoisoningAttack:
    def __init__(self, poison_rate: float = 0.1):
        self.poison_rate = poison_rate

    def label_flipping(self, dataset: list) -> list:
        """Flip labels to incorrect values."""
        poisoned = []
        for x, y in dataset:
            if np.random.random() < self.poison_rate:
                # Flip label
                y_poisoned = (y + 1) % 10  # For MNIST-like data
                poisoned.append((x, y_poisoned))
            else:
                poisoned.append((x, y))
        return poisoned

    def clean_label_attack(self, dataset: list,
                           target_label: int) -> list:
        """Create poisoned samples with correct labels but wrong features."""
        poisoned = []
        for x, y in dataset:
            if np.random.random() < self.poison_rate:
                # Add pattern that should predict target
                x_poisoned = x + np.random.randn(*x.shape) * 0.5
                poisoned.append((x_poisoned, y))  # Keep original label
            else:
                poisoned.append((x, y))
        return poisoned
```

**Related Terms**: Training Data Attack, Label Flipping, Backdoor

---

### Distribution Shift

**Definition**: A change in the statistical properties of data between training and deployment, which can degrade model performance.

**Example**:
```python
def detect_distribution_shift(train_data: list,
                               test_data: list) -> dict:
    """Detect distribution shift between datasets."""
    train_features = np.array([x.flatten() for x, _ in train_data])
    test_features = np.array([x.flatten() for x, _ in test_data])

    # Compute statistics
    train_mean = np.mean(train_features, axis=0)
    test_mean = np.mean(test_features, axis=0)

    train_std = np.std(train_features, axis=0)
    test_std = np.std(test_features, axis=0)

    # Compute shift metrics
    mean_shift = np.linalg.norm(test_mean - train_mean)
    std_ratio = np.mean(test_std / (train_std + 1e-8))

    return {
        "mean_shift": mean_shift,
        "std_ratio": std_ratio,
        "significant_shift": mean_shift > 0.1 or std_ratio > 1.5,
    }
```

**Related Terms**: Covariate Shift, Concept Drift, Domain Adaptation

---

### Evasion Attack

**Definition**: An attack where adversarial examples are crafted at test time to evade detection or cause misclassification.

**Example**:
```python
def evasion_attack(model, x: np.ndarray, y: int,
                   method: str = "fgsm") -> np.ndarray:
    """Perform evasion attack on model."""
    if method == "fgsm":
        return fgsm_attack(model, x, y)
    elif method == "pgd":
        return pgd_attack(model, x, y)
    elif method == "carlini":
        return carlini_wagner_attack(model, x, y)
    else:
        raise ValueError(f"Unknown attack method: {method}")

def fgsm_attack(model, x, y, epsilon=0.1):
    """Fast Gradient Sign Method."""
    gradient = compute_gradient(model, x, y)
    x_adv = x + epsilon * np.sign(gradient)
    return np.clip(x_adv, 0, 1)
```

**Related Terms**: Adversarial Example, FGSM, PGD

---

### FGSM (Fast Gradient Sign Method)

**Definition**: A fast adversarial attack method that uses the sign of the gradient to create adversarial examples.

**Example**:
```python
def fgsm_attack(model, x: np.ndarray, y: int,
                epsilon: float = 0.1) -> np.ndarray:
    """
    Fast Gradient Sign Method attack.

    Args:
        model: Target model
        x: Input sample
        y: True label
        epsilon: Perturbation magnitude
    """
    # Enable gradient computation
    x_tensor = tf.convert_to_tensor(x.reshape(1, *x.shape))
    x_tensor = tf.cast(x_tensor, tf.float32)

    with tf.GradientTape() as tape:
        tape.watch(x_tensor)
        prediction = model(x_tensor)
        loss = tf.keras.losses.sparse_categorical_crossentropy(
            y, prediction
        )

    # Get gradient
    gradient = tape.gradient(loss, x_tensor)

    # Create adversarial example
    x_adv = x_tensor + epsilon * tf.sign(gradient)
    x_adv = tf.clip_by_value(x_adv, 0, 1)

    return x_adv.numpy()[0]
```

**Related Terms**: Gradient Attack, PGD, Adversarial Example

---

### Model Extraction

**Definition**: An attack where an adversary attempts to steal a machine learning model by querying it and learning from its outputs.

**Example**:
```python
class ModelExtractionAttack:
    def __init__(self, api_client):
        self.api = api_client
        self.queries = []

    def extract_model(self, n_queries: int = 10000) -> dict:
        """Extract model via API queries."""
        # Generate diverse inputs
        inputs = self._generate_diverse_inputs(n_queries)

        # Query API and collect outputs
        for x in inputs:
            output = self.api.predict(x)
            self.queries.append((x, output))

        # Train surrogate model
        surrogate_model = self._train_surrogate()

        return {
            "surrogate_model": surrogate_model,
            "queries_made": len(self.queries),
            "similarity": self._evaluate_similarity(surrogate_model),
        }

    def _generate_diverse_inputs(self, n: int) -> list:
        """Generate diverse input samples."""
        return [np.random.randn(10) for _ in range(n)]

    def _train_surrogate(self):
        """Train surrogate model on collected data."""
        # Simplified - would train actual model
        return None

    def _evaluate_similarity(self, surrogate) -> float:
        """Evaluate similarity to target model."""
        return 0.0
```

**Related Terms**: Model Stealing, API Abuse, Surrogate Model

---

### Model Inversion

**Definition**: An attack where an adversary reconstructs training data from model predictions, potentially revealing sensitive information.

**Example**:
```python
class ModelInversionAttack:
    def __init__(self, model):
        self.model = model

    def reconstruct_input(self, target_class: int,
                          n_iterations: int = 1000) -> np.ndarray:
        """Reconstruct input for a target class."""
        # Start with random noise
        x = np.random.rand(10)

        for _ in range(n_iterations):
            # Compute gradient to maximize class probability
            gradient = self._compute_class_gradient(x, target_class)

            # Update input
            x = x + 0.01 * gradient
            x = np.clip(x, 0, 1)

        return x

    def _compute_class_gradient(self, x, target_class):
        """Compute gradient of class probability w.r.t. input."""
        # Simplified gradient computation
        return np.random.randn(*x.shape) * 0.01
```

**Related Terms**: Privacy Attack, Training Data Reconstruction, Membership Inference

---

### Membership Inference

**Definition**: An attack where an adversary determines whether a specific data point was used to train the model.

**Example**:
```python
class MembershipInferenceAttack:
    def __init__(self, model):
        self.model = model

    def predict_membership(self, x: np.ndarray, y: int) -> dict:
        """Predict if sample was in training data."""
        # Get model prediction
        prediction = self.model.predict(x.reshape(1, -1))[0]

        # High confidence on true label suggests membership
        confidence = prediction[y]

        # Membership likely if confidence is very high
        is_member = confidence > 0.9

        return {
            "is_member": is_member,
            "confidence": confidence,
        }

    def evaluate_attack(self, member_data: list,
                        non_member_data: list) -> dict:
        """Evaluate membership inference attack accuracy."""
        correct = 0
        total = len(member_data) + len(non_member_data)

        for x, y in member_data:
            result = self.predict_membership(x, y)
            if result["is_member"]:
                correct += 1

        for x, y in non_member_data:
            result = self.predict_membership(x, y)
            if not result["is_member"]:
                correct += 1

        return {
            "accuracy": correct / total,
            "attack_success": correct / total > 0.5,
        }
```

**Related Terms**: Privacy Attack, Model Inversion, Data Privacy

---

### PGD (Projected Gradient Descent)

**Definition**: An iterative adversarial attack that applies FGSM multiple times with small steps, projecting back to allowed perturbation bounds.

**Example**:
```python
def pgd_attack(model, x: np.ndarray, y: int,
               epsilon: float = 0.1, num_steps: int = 10,
               step_size: float = 0.01) -> np.ndarray:
    """
    Projected Gradient Descent attack.

    Args:
        model: Target model
        x: Input sample
        y: True label
        epsilon: Maximum perturbation
        num_steps: Number of iterations
        step_size: Step size per iteration
    """
    x_adv = x.copy()

    for _ in range(num_steps):
        # Compute gradient
        gradient = compute_gradient(model, x_adv, y)

        # Take step
        x_adv = x_adv + step_size * np.sign(gradient)

        # Project back to epsilon ball
        perturbation = x_adv - x
        perturbation = np.clip(perturbation, -epsilon, epsilon)
        x_adv = x + perturbation

        # Clip to valid range
        x_adv = np.clip(x_adv, 0, 1)

    return x_adv
```

**Related Terms**: FGSM, Iterative Attack, Adversarial Example

---

### Perturbation

**Definition**: The modification applied to an input to create an adversarial example, typically constrained to be small enough to be imperceptible.

**Example**:
```python
def measure_perturbation(x_original: np.ndarray,
                         x_adversarial: np.ndarray) -> dict:
    """Measure perturbation between original and adversarial."""
    diff = x_adversarial - x_original

    return {
        "l0_norm": np.sum(diff != 0),  # Number of changed pixels
        "l2_norm": np.linalg.norm(diff),  # Euclidean distance
        "linf_norm": np.max(np.abs(diff)),  # Maximum change
        "mean_change": np.mean(np.abs(diff)),
    }

# Example
x = np.random.rand(28, 28)
x_adv = x + np.random.randn(28, 28) * 0.1
x_adv = np.clip(x_adv, 0, 1)

perturbation = measure_perturbation(x, x_adv)
print(f"L2 norm: {perturbation['l2_norm']:.4f}")
print(f"Linf norm: {perturbation['linf_norm']:.4f}")
```

**Related Terms**: Adversarial Example, Epsilon, FGSM

---

### Robustness Testing

**Definition**: The process of evaluating model performance under various adversarial conditions and distribution shifts.

**Example**:
```python
class RobustnessTestSuite:
    def __init__(self, model):
        self.model = model

    def run_all_tests(self, test_data: list) -> dict:
        """Run comprehensive robustness tests."""
        results = {
            "clean_accuracy": self.test_clean_accuracy(test_data),
            "adversarial_robustness": self.test_adversarial(test_data),
            "noise_robustness": self.test_noise(test_data),
            "distribution_shift": self.test_distribution_shift(test_data),
        }

        # Overall score
        results["overall_score"] = self._compute_overall_score(results)

        return results

    def test_clean_accuracy(self, data):
        correct = sum(1 for x, y in data if self.model.predict(x.reshape(1, -1))[0] == y)
        return correct / len(data)

    def test_adversarial(self, data):
        # Test with FGSM
        return {"fgsm_accuracy": 0.8}  # Simplified

    def test_noise(self, data):
        # Test with random noise
        return {"noise_0.1_accuracy": 0.85}  # Simplified

    def test_distribution_shift(self, data):
        # Test with shifted distribution
        return {"shift_accuracy": 0.75}  # Simplified

    def _compute_overall_score(self, results):
        return np.mean([
            results["clean_accuracy"],
            results["adversarial_robustness"]["fgsm_accuracy"],
            results["noise_robustness"]["noise_0.1_accuracy"],
        ])
```

**Related Terms**: Adversarial Robustness, Testing, Evaluation

---

### Trigger Pattern

**Definition**: A specific pattern added to inputs in a backdoor attack that activates the malicious behavior.

**Example**:
```python
class TriggerGenerator:
    def __init__(self, size: int = 3):
        self.size = size

    def create_trigger(self, pattern_type: str = "fixed") -> np.ndarray:
        """Create trigger pattern."""
        if pattern_type == "fixed":
            return np.ones((self.size, self.size))
        elif pattern_type == "random":
            return np.random.rand(self.size, self.size)
        elif pattern_type == "pixel":
            trigger = np.zeros((self.size, self.size))
            trigger[0, 0] = 1  # Single white pixel
            return trigger
        else:
            raise ValueError(f"Unknown pattern type: {pattern_type}")

    def apply_trigger(self, x: np.ndarray, trigger: np.ndarray,
                      position: tuple = (0, 0)) -> np.ndarray:
        """Apply trigger to input."""
        x_triggered = x.copy()
        x_triggered[position[0]:position[0]+self.size,
                   position[1]:position[1]+self.size] = trigger
        return x_triggered
```

**Related Terms**: Backdoor Attack, Trojan, Pattern Matching

---

*Part of the [AI Security Lecture Series](README.md). See also: [Lecture 08: Model Security](08-model-security-lecture.md)*
