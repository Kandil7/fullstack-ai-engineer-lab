# Glossary 05: Data Privacy Terms

## Quick Reference Table

| Term | Category | Importance | See Also |
|------|----------|------------|----------|
| GDPR | Regulation | Critical | Data Protection |
| CCPA | Regulation | Critical | Consumer Privacy |
| HIPAA | Regulation | Critical | Health Data |
| Anonymization | Technique | Critical | Privacy |
| Pseudonymization | Technique | High | De-identification |
| Differential Privacy | Technique | Critical | Privacy-Preserving ML |
| Federated Learning | Technique | Critical | Distributed ML |
| Consent Management | Process | Critical | User Rights |
| Data Minimization | Principle | Critical | Privacy by Design |
| Data Retention | Policy | High | Storage Limitation |
| Right to Erasure | Right | Critical | Deletion |
| Data Subject | Concept | High | Individual |
| Data Controller | Role | High | Data Processor |
| Privacy Impact Assessment | Process | High | Risk Assessment |
| Data Breach | Event | Critical | Incident Response |
| Encryption | Technique | Critical | Data Security |

---

## Alphabetical Definitions

### Anonymization

**Definition**: The process of irreversibly removing or modifying personal information so that individuals cannot be re-identified, even with additional data.

**Example**:
```python
import hashlib
import random

class Anonymizer:
    def __init__(self, salt: str = "static-salt"):
        self.salt = salt

    def anonymize_dataset(self, data: list, quasi_identifiers: list,
                          k: int = 5) -> list:
        """Apply k-anonymity to dataset."""
        # Group by quasi-identifiers
        groups = {}
        for record in data:
            key = tuple(record.get(qi) for qi in quasi_identifiers)
            groups.setdefault(key, []).append(record)

        # Generalize small groups
        anonymized = []
        for key, group in groups.items():
            if len(group) < k:
                for record in group:
                    anonymized.append(self._generalize(record, quasi_identifiers))
            else:
                anonymized.extend(group)
        return anonymized

    def _generalize(self, record, quasi_identifiers):
        """Generalize quasi-identifier values."""
        result = record.copy()
        for qi in quasi_identifiers:
            if qi in result and isinstance(result[qi], int):
                # Generalize age to ranges
                result[qi] = f"{(result[qi] // 10) * 10}-{(result[qi] // 10) * 10 + 9}"
        return result

# Usage
anonymizer = Anonymizer()
data = [
    {"name": "Alice", "age": 25, "zip": "10001"},
    {"name": "Bob", "age": 26, "zip": "10001"},
    {"name": "Charlie", "age": 27, "zip": "10002"},
]
anonymized = anonymizer.anonymize_dataset(data, ["age", "zip"], k=2)
```

**Related Terms**: K-Anonymity, Pseudonymization, De-identification

---

### CCPA (California Consumer Privacy Act)

**Definition**: A California law that gives consumers more control over the personal information that businesses collect about them.

**Example**:
```python
class CCPACompliance:
    def __init__(self):
        self.consumer_rights = {
            "right_to_know": "Consumers can request data disclosure",
            "right_to_delete": "Consumers can request data deletion",
            "right_to_opt_out": "Consumers can opt out of data sale",
            "right_to_non_discrimination": "No discrimination for exercising rights",
        }

    def handle_data_request(self, consumer_id: str, request_type: str) -> dict:
        """Handle CCPA consumer data request."""
        if request_type == "know":
            return self._disclose_data(consumer_id)
        elif request_type == "delete":
            return self._delete_data(consumer_id)
        elif request_type == "opt_out":
            return self._opt_out_of_sale(consumer_id)
        return {"status": "invalid_request"}

    def _disclose_data(self, consumer_id: str) -> dict:
        """Disclose data collected about consumer."""
        return {
            "status": "success",
            "data_categories": ["identifiers", "commercial_info", "internet_activity"],
            "sources": ["direct_collection", "third_parties"],
            "business_purposes": ["service_provision", "marketing"],
        }

    def _delete_data(self, consumer_id: str) -> dict:
        """Delete consumer data."""
        return {"status": "success", "message": "Data deletion initiated"}

    def _opt_out_of_sale(self, consumer_id: str) -> dict:
        """Opt consumer out of data sale."""
        return {"status": "success", "message": "Opt-out recorded"}
```

**Related Terms**: Consumer Privacy, Data Rights, Privacy Regulation

---

### Consent

**Definition**: Freely given, specific, informed, and unambiguous indication of a data subject's wishes to process their personal data.

**Example**:
```python
from datetime import datetime
from enum import Enum

class ConsentType(Enum):
    DATA_PROCESSING = "data_processing"
    MARKETING = "marketing"
    THIRD_PARTY_SHARING = "third_party_sharing"
    ANALYTICS = "analytics"

class ConsentManager:
    def __init__(self):
        self.consents = {}

    def record_consent(self, user_id: str, consent_type: ConsentType,
                       granted: bool, purpose: str) -> dict:
        """Record user consent."""
        key = f"{user_id}:{consent_type.value}"
        self.consents[key] = {
            "user_id": user_id,
            "type": consent_type.value,
            "granted": granted,
            "purpose": purpose,
            "timestamp": datetime.utcnow().isoformat(),
            "method": "explicit",
        }
        return self.consents[key]

    def has_consent(self, user_id: str, consent_type: ConsentType) -> bool:
        """Check if user has given consent."""
        key = f"{user_id}:{consent_type.value}"
        consent = self.consents.get(key)
        return consent is not None and consent["granted"]

    def withdraw_consent(self, user_id: str, consent_type: ConsentType):
        """Withdraw user consent."""
        self.record_consent(user_id, consent_type, False, "user_withdrawal")

# Usage
manager = ConsentManager()
manager.record_consent("user123", ConsentType.MARKETING, True, "Email marketing")
print(manager.has_consent("user123", ConsentType.MARKETING))  # True
```

**Related Terms**: Consent Management, Opt-in, User Rights

---

### Consent Management

**Definition**: The system and processes for obtaining, recording, and managing user consent for data processing activities.

**Example**:
```python
class ConsentManagementSystem:
    def __init__(self):
        self.policies = {
            "analytics": {"required": True, "default": False},
            "marketing": {"required": False, "default": False},
            "functional": {"required": True, "default": True},
        }

    def get_consent_banner(self) -> dict:
        """Generate consent banner configuration."""
        return {
            "categories": [
                {
                    "name": "Essential",
                    "description": "Necessary for the website to function",
                    "required": True,
                    "default": True,
                },
                {
                    "name": "Analytics",
                    "description": "Help us understand how visitors use our site",
                    "required": False,
                    "default": False,
                },
                {
                    "name": "Marketing",
                    "description": "Used to deliver relevant ads",
                    "required": False,
                    "default": False,
                },
            ],
            "accept_all_button": True,
            "reject_all_button": True,
            "customize_button": True,
        }

    def process_consent_choice(self, user_id: str, choices: dict) -> dict:
        """Process user's consent choices."""
        recorded = {}
        for category, granted in choices.items():
            recorded[category] = {
                "granted": granted,
                "timestamp": datetime.utcnow().isoformat(),
            }
        return {"user_id": user_id, "consents": recorded}
```

**Related Terms**: Consent, Cookie Consent, User Preferences

---

### Data Breach

**Definition**: A security incident where sensitive, protected, or confidential data is accessed, disclosed, or stolen by an unauthorized person.

**Example**:
```python
from datetime import datetime, timedelta

class DataBreachHandler:
    def __init__(self):
        self.breach_threshold_hours = 72  # GDPR requirement

    def report_breach(self, breach_info: dict) -> dict:
        """Report a data breach."""
        breach = {
            "id": f"BREACH-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "discovered_at": datetime.utcnow().isoformat(),
            "notification_deadline": (
                datetime.utcnow() + timedelta(hours=self.breach_threshold_hours)
            ).isoformat(),
            "affected_records": breach_info.get("record_count", 0),
            "data_types": breach_info.get("data_types", []),
            "status": "reported",
        }

        # Check if supervisory authority notification required
        if breach["affected_records"] > 0:
            breach["authority_notification_required"] = True
            breach["authority_notification_deadline"] = (
                datetime.utcnow() + timedelta(hours=self.breach_threshold_hours)
            ).isoformat()

        # Check if individual notification required
        if breach["affected_records"] > 0:
            breach["individual_notification_required"] = True

        return breach

    def assess_severity(self, breach_info: dict) -> str:
        """Assess breach severity."""
        record_count = breach_info.get("record_count", 0)
        data_types = breach_info.get("data_types", [])

        if record_count > 10000 or "financial" in data_types:
            return "critical"
        elif record_count > 1000 or "health" in data_types:
            return "high"
        elif record_count > 100:
            return "medium"
        return "low"
```

**Related Terms**: Incident Response, Data Security, Notification

---

### Data Controller

**Definition**: The entity that determines the purposes and means of processing personal data. Under GDPR, data controllers have specific legal obligations.

**Example**:
```python
class DataController:
    """Represents a data controller's responsibilities."""

    def __init__(self, organization: str):
        self.organization = organization
        self.processing_activities = []
        self.dpo = None  # Data Protection Officer

    def register_processing_activity(self, activity: dict) -> str:
        """Register a processing activity (Article 30 GDPR)."""
        activity_id = f"PA-{len(self.processing_activities) + 1}"
        self.processing_activities.append({
            "id": activity_id,
            "organization": self.organization,
            "purpose": activity.get("purpose"),
            "data_categories": activity.get("data_categories", []),
            "recipients": activity.get("recipients", []),
            "retention_period": activity.get("retention_period"),
            "security_measures": activity.get("security_measures", []),
        })
        return activity_id

    def conduct_dpia(self, processing: dict) -> dict:
        """Conduct Data Protection Impact Assessment."""
        return {
            "processing_description": processing.get("description"),
            "necessity_assessment": "Processing is necessary for stated purpose",
            "risk_assessment": "Risks mitigated by technical and organizational measures",
            "dpo_consultation": self.dpo is not None,
            "status": "completed",
        }

    def appoint_dpo(self, dpo_info: dict):
        """Appoint a Data Protection Officer."""
        self.dpo = dpo_info
```

**Related Terms**: Data Processor, GDPR, Data Protection Officer

---

### Data Minimization

**Definition**: A privacy principle requiring that personal data collected should be adequate, relevant, and limited to what is necessary for the purposes for which it is processed.

**Example**:
```python
class DataMinimization:
    """Apply data minimization principles."""

    def minimize_registration_form(self, form_data: dict) -> dict:
        """Minimize data collected during registration."""
        # Only collect what's absolutely necessary
        minimized = {
            "email": form_data.get("email"),  # Required for account
            "password_hash": form_data.get("password_hash"),  # Required for auth
        }

        # Optional fields - clearly marked as optional
        if form_data.get("name"):
            minimized["name"] = form_data["name"]

        # Don't collect unnecessary fields
        unnecessary_fields = ["phone", "address", "birthdate", "gender"]
        for field in unnecessary_fields:
            if field in form_data:
                # Log that unnecessary data was rejected
                print(f"Rejected unnecessary field: {field}")

        return minimized

    def minimize_api_response(self, user_data: dict,
                               purpose: str) -> dict:
        """Minimize data in API responses based on purpose."""
        # Different purposes require different data
        purpose_configs = {
            "authentication": ["id", "email"],
            "profile_display": ["id", "name", "email"],
            "analytics": ["id"],
            "support": ["id", "email", "name", "created_at"],
        }

        allowed_fields = purpose_configs.get(purpose, ["id"])
        return {k: v for k, v in user_data.items() if k in allowed_fields}
```

**Related Terms**: Data Collection, Privacy by Design, Purpose Limitation

---

### Data Retention

**Definition**: The policy governing how long personal data is stored and when it should be deleted.

**Example**:
```python
from datetime import datetime, timedelta
from enum import Enum

class RetentionPeriod(Enum):
    """Standard retention periods."""
    SESSION_ONLY = 0
    ONE_MONTH = 30
    THREE_MONTHS = 90
    ONE_YEAR = 365
    TWO_YEARS = 730
    FIVE_YEARS = 1825
    TEN_YEARS = 3650

class DataRetentionPolicy:
    def __init__(self):
        self.retention_rules = {
            "user_account_data": RetentionPeriod.TWO_YEARS,
            "transaction_records": RetentionPeriod.FIVE_YEARS,
            "access_logs": RetentionPeriod.ONE_YEAR,
            "marketing_data": RetentionPeriod.ONE_YEAR,
            "support_tickets": RetentionPeriod.TWO_YEARS,
            "analytics_data": RetentionPeriod.ONE_YEAR,
        }

    def should_delete(self, data_type: str, created_at: datetime) -> bool:
        """Check if data should be deleted."""
        retention_days = self.retention_rules.get(data_type, RetentionPeriod.ONE_YEAR).value
        age_days = (datetime.utcnow() - created_at).days
        return age_days > retention_days

    def get_deletion_schedule(self) -> dict:
        """Get deletion schedule for all data types."""
        schedule = {}
        for data_type, period in self.retention_rules.items():
            schedule[data_type] = {
                "retention_days": period.value,
                "retention_description": period.name,
            }
        return schedule
```

**Related Terms**: Storage Limitation, Data Deletion, Retention Policy

---

### Differential Privacy

**Definition**: A mathematical framework for providing privacy guarantees when analyzing datasets. It ensures that the output of a query is approximately the same whether or not any individual's data is included.

**Example**:
```python
import numpy as np

class DifferentialPrivacy:
    def __init__(self, epsilon: float = 1.0):
        """Initialize with privacy budget epsilon."""
        self.epsilon = epsilon

    def laplace_mechanism(self, true_value: float,
                           sensitivity: float) -> float:
        """Add Laplace noise for numeric queries."""
        scale = sensitivity / self.epsilon
        noise = np.random.laplace(0, scale)
        return true_value + noise

    def private_count(self, data: list, condition) -> int:
        """Count with differential privacy."""
        true_count = sum(1 for item in data if condition(item))
        return int(self.laplace_mechanism(true_count, sensitivity=1.0))

    def private_mean(self, data: list, lower: float, upper: float) -> float:
        """Mean with differential privacy."""
        clipped = [max(lower, min(upper, x)) for x in data]
        true_mean = sum(clipped) / len(clipped) if clipped else 0
        sensitivity = (upper - lower) / len(data) if data else 0
        return self.laplace_mechanism(true_mean, sensitivity)

    def randomized_response(self, true_value: bool) -> bool:
        """Randomized response for binary questions."""
        p = np.exp(self.epsilon) / (np.exp(self.epsilon) + 1)
        if np.random.random() < p:
            return true_value
        return np.random.random() > 0.5

# Usage
dp = DifferentialPrivacy(epsilon=0.5)
data = [25, 30, 35, 40, 45, 50, 55, 60]
private_avg = dp.private_mean(data, 0, 150)
print(f"Private average: {private_avg:.1f}")
```

**Related Terms**: Privacy Budget, Laplace Mechanism, Noise Addition

---

### Encryption

**Definition**: The process of converting data into a coded format that can only be read by authorized parties with the correct decryption key.

**Example**:
```python
from cryptography.fernet import Fernet
import hashlib

class DataEncryption:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data."""
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data."""
        return self.cipher.decrypt(encrypted_data.encode()).decode()

    def hash_for_comparison(self, data: str) -> str:
        """Create hash for comparison (one-way)."""
        return hashlib.sha256(data.encode()).hexdigest()

# Usage
encryption = DataEncryption()
sensitive_data = "john@example.com"
encrypted = encryption.encrypt_sensitive_data(sensitive_data)
print(f"Encrypted: {encrypted}")
decrypted = encryption.decrypt_sensitive_data(encrypted)
print(f"Decrypted: {decrypted}")
```

**Related Terms**: Data Security, Key Management, At-Rest Encryption

---

### Federated Learning

**Definition**: A machine learning approach where models are trained across multiple decentralized devices or servers holding local data, without exchanging raw data.

**Example**:
```python
import numpy as np

class FederatedLearning:
    def __init__(self, global_model: dict):
        self.global_model = global_model
        self.round = 0

    def client_training(self, client_id: int, local_data: list) -> dict:
        """Simulate client-side training."""
        # Train on local data (data never leaves device)
        gradients = np.random.randn(10)  # Simulated gradients
        return {
            "client_id": client_id,
            "gradients": gradients.tolist(),
            "num_samples": len(local_data),
        }

    def aggregate_updates(self, client_updates: list) -> dict:
        """Aggregate client updates (Federated Averaging)."""
        total_samples = sum(u["num_samples"] for u in client_updates)
        aggregated = np.zeros(10)

        for update in client_updates:
            weight = update["num_samples"] / total_samples
            aggregated += weight * np.array(update["gradients"])

        self.global_model["weights"] = aggregated.tolist()
        self.round += 1

        return {"round": self.round, "model": self.global_model}

    def add_differential_privacy(self, gradients: list,
                                  epsilon: float = 1.0) -> list:
        """Add DP noise to gradients."""
        dp = DifferentialPrivacy(epsilon)
        return [dp.laplace_mechanism(g, sensitivity=1.0) for g in gradients]
```

**Related Terms**: Distributed ML, Privacy-Preserving ML, Local Training

---

### GDPR (General Data Protection Regulation)

**Definition**: EU regulation on data protection and privacy that gives individuals control over their personal data and harmonizes data protection law across Europe.

**Example**:
```python
class GDPRCompliance:
    def __init__(self):
        self.principles = {
            "lawfulness": "Processing must have legal basis",
            "fairness": "Processing must be fair and transparent",
            "purpose_limitation": "Data collected for specified purposes",
            "data_minimization": "Data must be adequate, relevant, limited",
            "accuracy": "Data must be accurate and kept up-to-date",
            "storage_limitation": "Data kept no longer than necessary",
            "integrity_confidentiality": "Appropriate security measures",
            "accountability": "Controller must demonstrate compliance",
        }

    def get_legal_bases(self) -> list:
        """Return valid legal bases for processing."""
        return [
            "consent",
            "contract",
            "legal_obligation",
            "vital_interests",
            "public_task",
            "legitimate_interests",
        ]

    def handle_data_subject_request(self, request_type: str,
                                     subject_id: str) -> dict:
        """Handle GDPR data subject rights."""
        handlers = {
            "access": self._right_of_access,
            "rectification": self._right_to_rectification,
            "erasure": self._right_to_erasure,
            "portability": self._right_to_portability,
            "objection": self._right_to_object,
        }

        handler = handlers.get(request_type)
        if handler:
            return handler(subject_id)
        return {"status": "invalid_request"}

    def _right_of_access(self, subject_id: str) -> dict:
        return {"status": "success", "data": "exported"}

    def _right_to_rectification(self, subject_id: str) -> dict:
        return {"status": "success", "message": "Data corrected"}

    def _right_to_erasure(self, subject_id: str) -> dict:
        return {"status": "success", "message": "Data deleted"}

    def _right_to_portability(self, subject_id: str) -> dict:
        return {"status": "success", "format": "JSON", "data": "exported"}

    def _right_to_object(self, subject_id: str) -> dict:
        return {"status": "success", "message": "Processing stopped"}
```

**Related Terms**: Data Protection, Privacy Rights, EU Regulation

---

### K-Anonymity

**Definition**: A property of a dataset where each record is indistinguishable from at least k-1 other records based on quasi-identifiers.

**Example**:
```python
class KAnonymity:
    def __init__(self, k: int = 5):
        self.k = k

    def check_k_anonymity(self, data: list,
                           quasi_identifiers: list) -> dict:
        """Check if dataset satisfies k-anonymity."""
        groups = {}
        for record in data:
            key = tuple(record.get(qi) for qi in quasi_identifiers)
            groups.setdefault(key, []).append(record)

        violations = []
        for key, group in groups.items():
            if len(group) < self.k:
                violations.append({
                    "quasi_identifiers": dict(zip(quasi_identifiers, key)),
                    "count": len(group),
                    "required": self.k,
                })

        return {
            "satisfies_k_anonymity": len(violations) == 0,
            "k": self.k,
            "violations": violations,
        }

    def generalize_dataset(self, data: list,
                            quasi_identifiers: list) -> list:
        """Generalize dataset to achieve k-anonymity."""
        # Group and generalize small groups
        groups = {}
        for record in data:
            key = tuple(record.get(qi) for qi in quasi_identifiers)
            groups.setdefault(key, []).append(record)

        result = []
        for key, group in groups.items():
            if len(group) < self.k:
                # Generalize
                for record in group:
                    generalized = record.copy()
                    for qi in quasi_identifiers:
                        if qi in generalized and isinstance(generalized[qi], int):
                            generalized[qi] = f"{(generalized[qi]//10)*10}-{(generalized[qi]//10)*10+9}"
                    result.append(generalized)
            else:
                result.extend(group)
        return result
```

**Related Terms**: L-Diversity, Quasi-Identifier, Anonymization

---

### Pseudonymization

**Definition**: Processing personal data so that it can no longer be attributed to a specific data subject without the use of additional information, which must be kept separately.

**Example**:
```python
import hashlib
import secrets

class Pseudonymizer:
    def __init__(self):
        self.key_store = {}  # In practice, store securely

    def pseudonymize(self, identifier: str) -> str:
        """Replace identifier with pseudonym."""
        # Generate consistent pseudonym
        salt = secrets.token_hex(16)
        hash_input = f"{identifier}:{salt}"
        pseudonym = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

        # Store mapping (encrypted in practice)
        self.key_store[pseudonym] = {
            "original": identifier,
            "salt": salt,
        }

        return f"pseudo_{pseudonym}"

    def depseudonymize(self, pseudonym: str) -> str:
        """Restore original identifier from pseudonym."""
        key = pseudonym.replace("pseudo_", "")
        if key in self.key_store:
            return self.key_store[key]["original"]
        return None

# Usage
pseudonymizer = Pseudonymizer()
original = "john.doe@email.com"
pseudonym = pseudonymizer.pseudonymize(original)
print(f"Pseudonym: {pseudonym}")
# Can be reversed with key
restored = pseudonymizer.depseudonymize(pseudonym)
print(f"Restored: {restored}")
```

**Related Terms**: Anonymization, De-identification, Tokenization

---

### Privacy by Design

**Definition**: An approach to systems engineering that integrates privacy into the design and operation of IT systems, networked infrastructure, and business practices from the start.

**Example**:
```python
class PrivacyByDesign:
    """Implement privacy by design principles."""

    PRINCIPLES = {
        1: "Proactive not Reactive; Preventive not Remedial",
        2: "Privacy as the Default Setting",
        3: "Privacy Embedded into Design",
        4: "Full Functionality — Positive-Sum, not Zero-Sum",
        5: "End-to-End Security — Full Lifecycle Protection",
        6: "Visibility and Transparency — Keep it Open",
        7: "Respect for User Privacy — Keep it User-Centric",
    }

    def design_system(self, requirements: dict) -> dict:
        """Design system with privacy principles."""
        return {
            "data_collection": {
                "minimize": True,
                "purpose_limit": True,
                "consent_required": True,
            },
            "data_storage": {
                "encrypt_at_rest": True,
                "encrypt_in_transit": True,
                "retention_policy": "defined",
            },
            "data_processing": {
                "access_controls": True,
                "audit_logging": True,
                "privacy_impact_assessment": True,
            },
            "data_sharing": {
                "anonymization": True,
                "agreement_required": True,
                "user_notification": True,
            },
        }
```

**Related Terms**: Data Protection, System Design, Privacy Engineering

---

### Privacy Impact Assessment (PIA)

**Definition**: A process to identify and minimize the privacy risks of a project or system.

**Example**:
```python
class PrivacyImpactAssessment:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.findings = []

    def conduct_assessment(self, project_info: dict) -> dict:
        """Conduct a privacy impact assessment."""
        assessment = {
            "project": self.project_name,
            "description": project_info.get("description"),
            "data_flows": self._map_data_flows(project_info),
            "risks_identified": self._identify_risks(project_info),
            "mitigations": self._recommend_mitigations(project_info),
            "consultation_required": self._check_consultation_needed(),
            "approval_status": "pending",
        }
        return assessment

    def _map_data_flows(self, info: dict) -> list:
        """Map how data flows through the system."""
        return [
            {"flow": "Collection", "point": "User registration"},
            {"flow": "Processing", "point": "AI model training"},
            {"flow": "Storage", "point": "Database"},
            {"flow": "Sharing", "point": "Third-party API"},
        ]

    def _identify_risks(self, info: dict) -> list:
        """Identify privacy risks."""
        return [
            {"risk": "Data breach", "likelihood": "medium", "impact": "high"},
            {"risk": "Unauthorized access", "likelihood": "low", "impact": "high"},
            {"risk": "Data re-identification", "likelihood": "medium", "impact": "medium"},
        ]

    def _recommend_mitigations(self, info: dict) -> list:
        """Recommend risk mitigations."""
        return [
            {"risk": "Data breach", "mitigation": "Encryption and access controls"},
            {"risk": "Unauthorized access", "mitigation": "Role-based access control"},
            {"risk": "Data re-identification", "mitigation": "Anonymization and aggregation"},
        ]

    def _check_consultation_needed(self) -> bool:
        """Check if DPA consultation is required."""
        # High-risk processing requires DPA consultation under GDPR
        return any(f.get("impact") == "high" for f in self.findings)
```

**Related Terms**: Risk Assessment, GDPR, Data Protection

---

### Right to Erasure

**Definition**: Also known as the "right to be forgotten," allows individuals to request deletion of their personal data under certain circumstances.

**Example**:
```python
class RightToErasure:
    def __init__(self):
        self.exemptions = [
            "freedom_of_expression",
            "legal_obligation",
            "public_health",
            "archiving",
            "legal_claims",
        ]

    def handle_erasure_request(self, user_id: str,
                                request_info: dict) -> dict:
        """Handle a right to erasure request."""
        # Check for exemptions
        exemptions_applied = []
        for exemption in self.exemptions:
            if request_info.get(f"exempt_{exemption}"):
                exemptions_applied.append(exemption)

        if exemptions_applied:
            return {
                "status": "partial_erasure",
                "exemptions": exemptions_applied,
                "message": "Partial erasure due to exemptions",
            }

        # Full erasure
        return {
            "status": "erasure_complete",
            "user_id": user_id,
            "data_deleted": True,
            "backup_deletion_scheduled": True,
            "retention_exceptions": [],
        }

    def check_retention_requirements(self, data_type: str) -> bool:
        """Check if data must be retained despite erasure request."""
        # Legal retention requirements
        mandatory_retention = {
            "financial_records": 7,  # years
            "tax_records": 7,  # years
            "employment_records": 5,  # years
        }
        return data_type in mandatory_retention
```

**Related Terms**: Right to Deletion, GDPR, Data Subject Rights

---

*Part of the [AI Security Lecture Series](README.md). See also: [Lecture 05: Data Privacy](05-data-privacy-lecture.md)*
