# Lecture 05: Data Privacy & Protection

## Topic Overview

Data privacy in AI systems involves protecting personal information throughout the entire data lifecycle — from collection and processing to storage and deletion. This lecture covers GDPR compliance, data anonymization techniques, differential privacy, federated learning, consent management, and building privacy-preserving AI systems. Privacy is not just a legal requirement but a fundamental user trust factor.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Understand** major privacy regulations (GDPR, CCPA, HIPAA)
2. **Implement** data anonymization and pseudonymization techniques
3. **Apply** differential privacy to protect individual data points
4. **Design** privacy-preserving AI architectures
5. **Build** consent management systems
6. **Implement** data retention and deletion policies
7. **Conduct** privacy impact assessments

---

## Key Concepts

### 1. Privacy Regulations Overview

```python
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

class Regulation(Enum):
    """Major privacy regulations."""
    GDPR = "gdpr"          # EU General Data Protection Regulation
    CCPA = "ccpa"          # California Consumer Privacy Act
    HIPAA = "hipaa"        # Health Insurance Portability and Accountability Act
    PCI_DSS = "pci_dss"    # Payment Card Industry Data Security Standard
    LGPD = "lgpd"          # Brazil's Lei Geral de Proteção de Dados
    PIPL = "pipi"          # China's Personal Information Protection Law

@dataclass
class DataSubject:
    """Represents a data subject (individual)."""
    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    consent_given: bool = False
    consent_date: Optional[datetime] = None
    data_categories: List[str] = None

class PrivacyRegulation:
    """Base class for privacy regulations."""

    def __init__(self, name: str, requirements: Dict):
        self.name = name
        self.requirements = requirements

    def check_compliance(self, data_processing: Dict) -> Dict:
        """Check if data processing complies with regulation."""
        violations = []

        for requirement, details in self.requirements.items():
            if not self._check_requirement(data_processing, requirement):
                violations.append({
                    "requirement": requirement,
                    "details": details,
                })

        return {
            "compliant": len(violations) == 0,
            "violations": violations,
        }

    def _check_requirement(self, data: Dict, requirement: str) -> bool:
        """Check a specific requirement."""
        # Simplified compliance check
        return True

# GDPR requirements
GDPR_REQUIREMENTS = {
    "lawful_basis": "Must have legal basis for processing",
    "purpose_limitation": "Data used only for stated purpose",
    "data_minimization": "Collect only necessary data",
    "accuracy": "Keep data accurate and up-to-date",
    "storage_limitation": "Don't keep data longer than needed",
    "integrity_confidentiality": "Protect data appropriately",
    "accountability": "Demonstrate compliance",
    "transparency": "Inform subjects about processing",
    "consent": "Obtain explicit consent when required",
    "data_subject_rights": "Honor rights to access, delete, correct",
    "data_protection_officer": "Appoint DPO when required",
    "data_breach_notification": "Report breaches within 72 hours",
}

# CCPA requirements
CCPA_REQUIREMENTS = {
    "right_to_know": "Consumers can request data disclosure",
    "right_to_delete": "Consumers can request data deletion",
    "right_to_opt_out": "Consumers can opt out of data sale",
    "non_discrimination": "No discrimination for exercising rights",
    "data_minimization": "Collect only necessary data",
    "security": "Implement reasonable security measures",
}
```

### 2. Data Anonymization

```python
import hashlib
import random
from typing import Any, Dict, List

class DataAnonymizer:
    """Anonymize data to protect privacy."""

    def __init__(self, salt: str = "default-salt"):
        self.salt = salt
        self.mapping_cache = {}

    def k_anonymize(self, data: List[Dict], quasi_identifiers: List[str],
                    k: int = 5) -> List[Dict]:
        """
        Apply k-anonymity to dataset.

        k-anonymity ensures each record is indistinguishable from
        at least k-1 other records based on quasi-identifiers.
        """
        # Group records by quasi-identifier values
        groups = {}
        for record in data:
            key = tuple(record.get(qi, '') for qi in quasi_identifiers)
            if key not in groups:
                groups[key] = []
            groups[key].append(record)

        # Apply generalization to small groups
        anonymized = []
        for key, group in groups.items():
            if len(group) < k:
                # Generalize quasi-identifiers
                for record in group:
                    record = self._generalize(record, quasi_identifiers)
                    anonymized.append(record)
            else:
                anonymized.extend(group)

        return anonymized

    def _generalize(self, record: Dict, quasi_identifiers: List[str]) -> Dict:
        """Generalize quasi-identifier values."""
        generalized = record.copy()
        for qi in quasi_identifiers:
            if qi in generalized:
                generalized[qi] = self._generalize_value(generalized[qi])
        return generalized

    def _generalize_value(self, value: Any) -> Any:
        """Generalize a single value."""
        if isinstance(value, int):
            # Generalize to range
            return f"{(value // 10) * 10}-{(value // 10) * 10 + 9}"
        elif isinstance(value, str):
            # Generalize to category
            return value[:3] + "***"
        return value

    def l_diversity(self, data: List[Dict], sensitive_attr: str,
                    quasi_identifiers: List[str], l: int = 3) -> List[Dict]:
        """
        Apply l-diversity to dataset.

        l-diversity ensures each group has at least l distinct
        values for the sensitive attribute.
        """
        groups = {}
        for record in data:
            key = tuple(record.get(qi, '') for qi in quasi_identifiers)
            if key not in groups:
                groups[key] = []
            groups[key].append(record)

        # Check l-diversity
        diverse_data = []
        for key, group in groups.items():
            sensitive_values = set(record.get(sensitive_attr) for record in group)
            if len(sensitive_values) >= l:
                diverse_data.extend(group)
            else:
                # Remove or generalize records
                for record in group[:l]:
                    diverse_data.append(record)

        return diverse_data

    def pseudonymize(self, value: str, mapping: Optional[Dict] = None) -> str:
        """Pseudonymize a value using hashing."""
        if mapping and value in mapping:
            return mapping[value]

        hash_obj = hashlib.sha256((value + self.salt).encode())
        pseudonym = f"pseudo_{hash_obj.hexdigest()[:12]}"

        if mapping:
            mapping[value] = pseudonym

        return pseudonym

    def generalize_age(self, age: int) -> str:
        """Generalize age into ranges."""
        if age < 18:
            return "minor"
        elif age < 25:
            return "18-24"
        elif age < 35:
            return "25-34"
        elif age < 45:
            return "35-44"
        elif age < 55:
            return "45-54"
        elif age < 65:
            return "55-64"
        else:
            return "65+"

    def generalize_location(self, location: str) -> str:
        """Generalize location to region level."""
        # Simple generalization - in practice would use geographic hierarchy
        regions = {
            "New York": "Northeast US",
            "Boston": "Northeast US",
            "Los Angeles": "West US",
            "San Francisco": "West US",
        }
        return regions.get(location, "Unknown Region")
```

### 3. Differential Privacy

```python
import numpy as np
from typing import List, Callable

class DifferentialPrivacy:
    """Implement differential privacy mechanisms."""

    def __init__(self, epsilon: float = 1.0, delta: float = 1e-5):
        """
        Initialize differential privacy.

        Args:
            epsilon: Privacy budget (lower = more private)
            delta: Probability of privacy breach
        """
        self.epsilon = epsilon
        self.delta = delta
        self.privacy_budget_used = 0.0

    def laplace_mechanism(self, value: float, sensitivity: float) -> float:
        """
        Add Laplace noise for numeric queries.

        The noise is calibrated to sensitivity / epsilon.
        """
        if self.privacy_budget_used + self.epsilon > self.epsilon:
            raise ValueError("Privacy budget exhausted")

        scale = sensitivity / self.epsilon
        noise = np.random.laplace(0, scale)
        self.privacy_budget_used += self.epsilon

        return value + noise

    def gaussian_mechanism(self, value: float, sensitivity: float) -> float:
        """
        Add Gaussian noise for numeric queries.

        Used for (epsilon, delta)-differential privacy.
        """
        sigma = sensitivity * np.sqrt(2 * np.log(1.25 / self.delta)) / self.epsilon
        noise = np.random.normal(0, sigma)
        return value + noise

    def exponential_mechanism(self, scores: List[float],
                               sensitivity: float) -> int:
        """
        Select an item using exponential mechanism.

        Items with higher scores are more likely to be selected.
        """
        # Convert scores to probabilities
        scores_array = np.array(scores)
        probabilities = np.exp(self.epsilon * scores_array / (2 * sensitivity))
        probabilities = probabilities / probabilities.sum()

        # Select based on probabilities
        return np.random.choice(len(scores), p=probabilities)

    def randomized_response(self, true_answer: bool) -> bool:
        """
        Implement randomized response for binary questions.

        Each respondent answers truthfully with probability p,
        and randomly (true/false) with probability 1-p.
        """
        p = np.exp(self.epsilon) / (np.exp(self.epsilon) + 1)

        if np.random.random() < p:
            return true_answer  # Truthful answer
        else:
            return np.random.random() > 0.5  # Random answer

    def add_laplace_noise_to_dataset(self, data: List[float],
                                      sensitivity: float) -> List[float]:
        """Add Laplace noise to an entire dataset."""
        return [self.laplace_mechanism(x, sensitivity) for x in data]

    def private_count(self, data: List[Any], condition: Callable) -> int:
        """Count items matching condition with differential privacy."""
        true_count = sum(1 for item in data if condition(item))
        return int(self.laplace_mechanism(true_count, sensitivity=1.0))

    def private_mean(self, data: List[float], lower_bound: float,
                     upper_bound: float) -> float:
        """Compute mean with differential privacy."""
        # Clip data to bounds
        clipped = [max(lower_bound, min(upper_bound, x)) for x in data]

        # Compute true mean
        true_mean = sum(clipped) / len(clipped) if clipped else 0

        # Add noise
        sensitivity = (upper_bound - lower_bound) / len(data) if data else 0
        return self.laplace_mechanism(true_mean, sensitivity)

# Usage example
dp = DifferentialPrivacy(epsilon=0.5)

# Private count
users = [{"age": 25}, {"age": 30}, {"age": 35}, {"age": 40}]
adult_count = dp.private_count(users, lambda u: u["age"] >= 18)
print(f"Private adult count: {adult_count}")

# Private mean
ages = [25, 30, 35, 40, 45]
private_avg = dp.private_mean(ages, 0, 150)
print(f"Private average age: {private_avg:.1f}")
```

### 4. Federated Learning

```python
from typing import List, Dict, Any
import numpy as np

class FederatedLearning:
    """Implement federated learning for privacy-preserving ML."""

    def __init__(self, num_clients: int, model_params: Dict):
        self.num_clients = num_clients
        self.global_model = model_params
        self.round_number = 0

    def simulate_client_training(self, client_id: int,
                                  local_data: List[Dict]) -> Dict:
        """
        Simulate client-side training.

        In real federated learning, this happens on user devices.
        Raw data never leaves the device.
        """
        # Simulate local training
        # In practice: train model on local data, return only gradients
        local_update = {
            "client_id": client_id,
            "num_samples": len(local_data),
            "gradients": self._compute_gradients(local_data),
            "metadata": {
                "training_loss": 0.5 - client_id * 0.01,
                "epochs": 5,
            },
        }

        return local_update

    def _compute_gradients(self, data: List[Dict]) -> Dict:
        """Compute model gradients (simulated)."""
        # In practice: compute actual gradients from local training
        return {
            "weights": np.random.randn(10).tolist(),
            "bias": np.random.randn(1).tolist(),
        }

    def aggregate_updates(self, client_updates: List[Dict]) -> Dict:
        """
        Aggregate client updates using Federated Averaging.

        This is done on the server without seeing raw data.
        """
        # Weight by number of samples
        total_samples = sum(update["num_samples"] for update in client_updates)

        aggregated_weights = np.zeros(10)
        aggregated_bias = np.zeros(1)

        for update in client_updates:
            weight = update["num_samples"] / total_samples
            aggregated_weights += weight * np.array(update["gradients"]["weights"])
            aggregated_bias += weight * np.array(update["gradients"]["bias"])

        # Update global model
        self.global_model["weights"] = aggregated_weights.tolist()
        self.global_model["bias"] = aggregated_bias.tolist()
        self.round_number += 1

        return {
            "round": self.round_number,
            "global_model": self.global_model,
            "participating_clients": len(client_updates),
        }

    def add_differential_privacy(self, gradients: Dict,
                                  epsilon: float = 1.0) -> Dict:
        """Add differential privacy noise to gradients."""
        dp = DifferentialPrivacy(epsilon)

        noisy_weights = []
        for w in gradients["weights"]:
            noisy_w = dp.laplace_mechanism(w, sensitivity=1.0)
            noisy_weights.append(noisy_w)

        noisy_bias = [dp.laplace_mechanism(b, sensitivity=1.0)
                      for b in gradients["bias"]]

        return {
            "weights": noisy_weights,
            "bias": noisy_bias,
        }

    def secure_aggregation(self, client_updates: List[Dict]) -> Dict:
        """
        Simulate secure aggregation.

        In practice, this uses cryptographic techniques to aggregate
        updates without the server seeing individual contributions.
        """
        # Simulate masking (in practice, use homomorphic encryption)
        masked_updates = []
        for update in client_updates:
            mask = np.random.randn(10)
            masked_weights = np.array(update["gradients"]["weights"]) + mask
            update["gradients"]["weights"] = masked_weights.tolist()
            masked_updates.append(update)

        # Aggregate (masks cancel out in real secure aggregation)
        return self.aggregate_updates(masked_updates)
```

### 5. Consent Management

```python
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum

class ConsentType(Enum):
    """Types of consent."""
    DATA_COLLECTION = "data_collection"
    DATA_PROCESSING = "data_processing"
    DATA_SHARING = "data_sharing"
    MARKETING = "marketing"
    ANALYTICS = "analytics"
    THIRD_PARTY = "third_party"

@dataclass
class ConsentRecord:
    """Record of user consent."""
    user_id: str
    consent_type: ConsentType
    granted: bool
    timestamp: datetime
    expires_at: Optional[datetime] = None
    scope: Optional[str] = None
    method: str = "explicit"  # explicit, implied, opt-in, opt-out

class ConsentManager:
    """Manage user consent for data processing."""

    def __init__(self):
        self.consent_records: List[ConsentRecord] = []

    def record_consent(self, user_id: str, consent_type: ConsentType,
                       granted: bool, scope: Optional[str] = None,
                       expiry_days: Optional[int] = None) -> ConsentRecord:
        """Record user consent."""
        expires_at = None
        if expiry_days:
            expires_at = datetime.utcnow() + timedelta(days=expiry_days)

        record = ConsentRecord(
            user_id=user_id,
            consent_type=consent_type,
            granted=granted,
            timestamp=datetime.utcnow(),
            expires_at=expires_at,
            scope=scope,
        )

        self.consent_records.append(record)
        return record

    def has_consent(self, user_id: str, consent_type: ConsentType) -> bool:
        """Check if user has given consent."""
        user_consents = [
            r for r in self.consent_records
            if r.user_id == user_id and r.consent_type == consent_type
        ]

        if not user_consents:
            return False

        # Get most recent consent
        latest = max(user_consents, key=lambda r: r.timestamp)

        # Check if consent was granted and not expired
        if not latest.granted:
            return False

        if latest.expires_at and datetime.utcnow() > latest.expires_at:
            return False

        return True

    def withdraw_consent(self, user_id: str, consent_type: ConsentType):
        """Withdraw user consent."""
        self.record_consent(
            user_id=user_id,
            consent_type=consent_type,
            granted=False,
        )

    def get_user_consents(self, user_id: str) -> Dict[ConsentType, bool]:
        """Get all consent statuses for a user."""
        consents = {}
        for consent_type in ConsentType:
            consents[consent_type] = self.has_consent(user_id, consent_type)
        return consents

    def export_user_data(self, user_id: str) -> Dict:
        """Export all consent data for a user (GDPR right to portability)."""
        user_records = [
            r for r in self.consent_records
            if r.user_id == user_id
        ]

        return {
            "user_id": user_id,
            "consent_history": [
                {
                    "type": r.consent_type.value,
                    "granted": r.granted,
                    "timestamp": r.timestamp.isoformat(),
                    "expires_at": r.expires_at.isoformat() if r.expires_at else None,
                }
                for r in user_records
            ],
        }

    def delete_user_data(self, user_id: str) -> int:
        """Delete all consent data for a user (GDPR right to erasure)."""
        original_count = len(self.consent_records)
        self.consent_records = [
            r for r in self.consent_records
            if r.user_id != user_id
        ]
        return original_count - len(self.consent_records)
```

### 6. Data Retention

```python
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum

class RetentionPolicy(Enum):
    """Data retention policies."""
    MINIMUM = "minimum"      # Keep for minimum required period
    STANDARD = "standard"    # Standard retention period
    EXTENDED = "extended"    # Extended retention for specific purposes
    INDEFINITE = "indefinite" # Keep indefinitely (rarely appropriate)

class DataRetentionPolicy:
    """Manage data retention and deletion."""

    def __init__(self):
        self.policies = {
            "user_data": {
                "retention_days": 365 * 2,  # 2 years
                "policy": RetentionPolicy.STANDARD,
                "legal_basis": "Contract performance",
            },
            "analytics_data": {
                "retention_days": 365,  # 1 year
                "policy": RetentionPolicy.STANDARD,
                "legal_basis": "Legitimate interest",
            },
            "logs": {
                "retention_days": 90,  # 90 days
                "policy": RetentionPolicy.MINIMUM,
                "legal_basis": "Security",
            },
            "marketing_data": {
                "retention_days": 365 * 3,  # 3 years
                "policy": RetentionPolicy.EXTENDED,
                "legal_basis": "Consent",
            },
        }

    def should_delete(self, data_type: str, created_at: datetime) -> bool:
        """Check if data should be deleted based on retention policy."""
        if data_type not in self.policies:
            return True  # Unknown data type - delete

        policy = self.policies[data_type]
        retention_days = policy["retention_days"]

        if policy["policy"] == RetentionPolicy.INDEFINITE:
            return False

        age_days = (datetime.utcnow() - created_at).days
        return age_days > retention_days

    def get_retention_info(self, data_type: str) -> Dict:
        """Get retention information for a data type."""
        return self.policies.get(data_type, {
            "retention_days": 0,
            "policy": RetentionPolicy.MINIMUM,
            "legal_basis": "None specified",
        })

    def schedule_deletion(self, data: List[Dict]) -> List[Dict]:
        """Schedule data for deletion based on retention policies."""
        to_delete = []

        for record in data:
            data_type = record.get("type", "unknown")
            created_at = record.get("created_at")

            if created_at and self.should_delete(data_type, created_at):
                to_delete.append({
                    "record_id": record.get("id"),
                    "data_type": data_type,
                    "created_at": created_at.isoformat(),
                    "reason": "retention_period_expired",
                })

        return to_delete

class DataDeletionManager:
    """Manage data deletion requests."""

    def __init__(self):
        self.deletion_requests = []

    def request_deletion(self, user_id: str, data_types: Optional[List[str]] = None) -> str:
        """Request deletion of user data."""
        request_id = f"del_{len(self.deletion_requests) + 1}"

        self.deletion_requests.append({
            "id": request_id,
            "user_id": user_id,
            "data_types": data_types or ["all"],
            "status": "pending",
            "requested_at": datetime.utcnow(),
        })

        return request_id

    def process_deletion(self, request_id: str) -> Dict:
        """Process a deletion request."""
        for request in self.deletion_requests:
            if request["id"] == request_id:
                # In practice: actually delete data from all systems
                request["status"] = "completed"
                request["completed_at"] = datetime.utcnow()

                return {
                    "success": True,
                    "request_id": request_id,
                    "data_types_deleted": request["data_types"],
                }

        return {"success": False, "error": "Request not found"}
```

---

## Common Mistakes to Avoid

1. **Collecting too much data** — Apply data minimization principle
2. **Ignoring consent** — Always obtain proper consent before processing
3. **No data retention policy** — Data should not be kept indefinitely
4. **Ignoring user rights** — Implement mechanisms for access, deletion, correction
5. **Assuming anonymization is easy** — True anonymization is difficult; re-identification is common
6. **Not documenting processing** — Maintain records of processing activities
7. **Ignoring cross-border transfers** — Data transfers have legal requirements
8. **No privacy impact assessment** — Assess privacy risks before new processing

---

## Best Practices

1. **Privacy by design** — Build privacy into systems from the start
2. **Data minimization** — Collect only what you need
3. **Purpose limitation** — Use data only for stated purposes
4. **Transparency** — Be clear about data practices
5. **User control** — Give users control over their data
6. **Security** — Protect data with appropriate security measures
7. **Accountability** — Document and demonstrate compliance
8. **Regular audits** — Review privacy practices regularly

---

## Practice Exercises

### Exercise 1: Data Anonymization (Easy)
Implement k-anonymity for a sample dataset.

### Exercise 2: Differential Privacy (Medium)
Implement Laplace and Gaussian mechanisms for numeric queries.

### Exercise 3: Consent Management (Medium)
Build a consent management system with GDPR compliance.

### Exercise 4: Privacy-Preserving AI (Hard)
Design a federated learning system with differential privacy.

---

## Summary

Data privacy is essential for trustworthy AI systems. Key takeaways:

- **Understand regulations** — GDPR, CCPA, HIPAA have specific requirements
- **Anonymize data** — Use k-anonymity, l-diversity, or differential privacy
- **Minimize data collection** — Only collect what's necessary
- **Manage consent** — Track and honor user consent
- **Implement retention policies** — Don't keep data longer than needed
- **Enable user rights** — Support access, deletion, and correction requests

---

## References

- [GDPR Text](https://gdpr-info.eu/)
- [NIST Privacy Framework](https://www.nist.gov/privacy-framework)
- [Differential Privacy by Cynthia Dwork](https://差分隐私.org/)
