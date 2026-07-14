# Glossary 09: Infrastructure Security Terms

## Quick Reference Table

| Term | Category | Importance | See Also |
|------|----------|------------|----------|
| Container Security | Concept | Critical | Docker, Kubernetes |
| Secrets Management | Process | Critical | Vault, Key Management |
| Network Security | Concept | Critical | Firewall, VPC |
| Cloud Security | Concept | Critical | AWS, GCP, Azure |
| CI/CD Security | Process | Critical | Pipeline Security |
| IAM | Concept | Critical | Identity & Access |
| Encryption at Rest | Technique | Critical | Data Protection |
| Encryption in Transit | Technique | Critical | TLS, HTTPS |
| Vulnerability Scanning | Process | Critical | Security Audit |
| Container Image | Concept | High | Docker Image |
| Security Group | Concept | High | Firewall Rules |
| Bastion Host | Concept | High | Jump Server |
| SBOM | Concept | High | Software Bill of Materials |
| Infrastructure as Code | Concept | High | Terraform, CloudFormation |
| Network Segmentation | Technique | High | Microsegmentation |
| Zero Trust | Principle | Critical | Never Trust, Always Verify |

---

## Alphabetical Definitions

### Bastion Host

**Definition**: A special-purpose computer on a network specifically designed and configured to withstand attacks, used as an entry point for accessing internal resources.

**Example**:
```python
# Bastion host configuration
bastion_config = {
    "instance_type": "t3.micro",
    "ami": "ami-0c55b159cbfafe1f0",
    "security_groups": ["bastion-sg"],
    "key_pair": "admin-key",
    "subnet": "public-subnet",
    "allowed_cidrs": ["203.0.113.0/24"],  # Office IP range
}

# Security group for bastion
bastion_security_group = {
    "ingress": [
        {
            "port": 22,
            "protocol": "tcp",
            "cidr": "203.0.113.0/24",  # Only office IP
        }
    ],
    "egress": [
        {
            "port": 22,
            "protocol": "tcp",
            "cidr": "10.0.0.0/16",  # Internal network
        }
    ],
}
```

**Related Terms**: Jump Server, SSH, Network Security

---

### CIS Benchmark

**Definition**: A set of best practices and security guidelines developed by the Center for Internet Security for securing various technologies.

**Example**:
```python
# CIS Benchmark checks for Linux
cis_checks = {
    "1.1.1": {
        "title": "Disable unused filesystems",
        "check": "Ensure cram, freevxfs, jffs2, hfs, hfsplus, udf are disabled",
        "severity": "medium",
    },
    "2.1": {
        "title": "Configure NTP",
        "check": "Ensure time synchronization is configured",
        "severity": "low",
    },
    "3.1": {
        "title": "Disable IP forwarding",
        "check": "Ensure IP forwarding is disabled",
        "severity": "medium",
    },
    "4.1": {
        "title": "Configure firewall",
        "check": "Ensure firewall is active and configured",
        "severity": "high",
    },
}
```

**Related Terms**: Security Standards, Compliance, Hardening

---

### Container Security

**Definition**: The practices and tools used to secure containerized applications throughout their lifecycle.

**Example**:
```python
class ContainerSecurityBestPractices:
    """Container security best practices."""

    PRACTICES = {
        "image_security": [
            "Use minimal base images (distroless, alpine)",
            "Scan images for vulnerabilities",
            "Sign images with content trust",
            "Don't run as root",
            "Use multi-stage builds",
        ],
        "runtime_security": [
            "Use read-only file systems",
            "Drop unnecessary capabilities",
            "Limit resource usage",
            "Enable logging",
            "Use security profiles (AppArmor, SELinux)",
        ],
        "orchestration_security": [
            "Enable RBAC",
            "Use network policies",
            "Encrypt secrets at rest",
            "Enable audit logging",
            "Regular security updates",
        ],
    }

    @staticmethod
    def check_dockerfile(dockerfile_content: str) -> list:
        """Check Dockerfile for security issues."""
        issues = []

        if "USER root" in dockerfile_content:
            issues.append("Running as root user")

        if "COPY . ." in dockerfile_content and ".dockerignore" not in dockerfile_content:
            issues.append("No .dockerignore file")

        if "--no-cache" not in dockerfile_content and "apt-get install" in dockerfile_content:
            issues.append("Package cache not cleaned")

        return issues
```

**Related Terms**: Docker Security, Kubernetes Security, Image Scanning

---

### Encryption at Rest

**Definition**: The process of encrypting data when it is stored on disk or in databases.

**Example**:
```python
from cryptography.fernet import Fernet
import json

class EncryptionAtRest:
    """Encrypt data at rest."""

    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt_file(self, file_path: str) -> str:
        """Encrypt a file."""
        with open(file_path, 'rb') as f:
            data = f.read()

        encrypted = self.cipher.encrypt(data)

        encrypted_path = file_path + ".encrypted"
        with open(encrypted_path, 'wb') as f:
            f.write(encrypted)

        return encrypted_path

    def decrypt_file(self, encrypted_path: str) -> bytes:
        """Decrypt a file."""
        with open(encrypted_path, 'rb') as f:
            encrypted = f.read()

        return self.cipher.decrypt(encrypted)

    def encrypt_database_field(self, value: str) -> str:
        """Encrypt a database field."""
        return self.cipher.encrypt(value.encode()).decode()

    def decrypt_database_field(self, encrypted_value: str) -> str:
        """Decrypt a database field."""
        return self.cipher.decrypt(encrypted_value.encode()).decode()

# Usage
encryption = EncryptionAtRest()
encrypted = encryption.encrypt_database_field("sensitive_data")
decrypted = encryption.decrypt_database_field(encrypted)
```

**Related Terms**: Encryption in Transit, Key Management, Fernet

---

### Encryption in Transit

**Definition**: The process of encrypting data while it is being transmitted between systems.

**Example**:
```python
import ssl
import httpx

class EncryptionInTransit:
    """Ensure data is encrypted in transit."""

    @staticmethod
    def create_tls_context() -> ssl.SSLContext:
        """Create a TLS context for secure connections."""
        context = ssl.create_default_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        return context

    @staticmethod
    async def secure_request(url: str, data: dict) -> dict:
        """Make a secure HTTPS request."""
        async with httpx.AsyncClient(verify=True) as client:
            response = await client.post(url, json=data)
            return response.json()

    @staticmethod
    def check_https_enforcement(endpoints: list) -> list:
        """Check if endpoints enforce HTTPS."""
        issues = []
        for endpoint in endpoints:
            if endpoint.startswith("http://"):
                issues.append(f"Insecure endpoint: {endpoint}")
        return issues
```

**Related Terms**: TLS, HTTPS, Certificate

---

### Firewall

**Definition**: A network security device that monitors and filters incoming and outgoing network traffic based on security rules.

**Example**:
```python
class FirewallRule:
    """Firewall rule definition."""

    def __init__(self, name: str, direction: str, action: str,
                 protocol: str, port: int, source: str, destination: str):
        self.name = name
        self.direction = direction  # inbound or outbound
        self.action = action  # allow or deny
        self.protocol = protocol
        self.port = port
        self.source = source
        self.destination = destination

class FirewallConfig:
    """Firewall configuration."""

    def __init__(self):
        self.rules = []

    def add_rule(self, rule: FirewallRule):
        self.rules.append(rule)

    def check_traffic(self, traffic: dict) -> dict:
        """Check if traffic is allowed by rules."""
        for rule in self.rules:
            if (rule.direction == traffic["direction"] and
                rule.protocol == traffic["protocol"] and
                rule.port == traffic["port"] and
                self._match_cidr(traffic["source"], rule.source)):
                return {"allowed": rule.action == "allow"}

        return {"allowed": False}  # Default deny

    def _match_cidr(self, ip: str, cidr: str) -> bool:
        """Check if IP matches CIDR range."""
        import ipaddress
        try:
            return ipaddress.ip_address(ip) in ipaddress.ip_network(cidr)
        except ValueError:
            return False

# Usage
firewall = FirewallConfig()
firewall.add_rule(FirewallRule(
    name="allow-https",
    direction="inbound",
    action="allow",
    protocol="tcp",
    port=443,
    source="0.0.0.0/0",
    destination="10.0.1.0/24"
))
```

**Related Terms**: Network Security, Security Group, Access Control List

---

### IAM (Identity and Access Management)

**Definition**: The framework and processes for managing digital identities and access to resources.

**Example**:
```python
class IAMPolicy:
    """IAM policy definition."""

    def __init__(self):
        self.policies = []

    def create_policy(self, name: str, effect: str,
                      actions: list, resources: list) -> dict:
        """Create an IAM policy."""
        policy = {
            "version": "2012-10-17",
            "statement": [{
                "sid": name,
                "effect": effect,
                "action": actions,
                "resource": resources,
            }]
        }
        self.policies.append(policy)
        return policy

    def check_policy_security(self, policy: dict) -> list:
        """Check policy for security issues."""
        issues = []

        for statement in policy.get("statement", []):
            if statement.get("effect") == "Allow":
                if "*" in statement.get("action", []):
                    issues.append({
                        "severity": "high",
                        "issue": "Wildcard action in Allow policy",
                    })
                if "*" in statement.get("resource", []):
                    issues.append({
                        "severity": "high",
                        "issue": "Wildcard resource in Allow policy",
                    })

        return issues

# Usage
iam = IAMPolicy()
policy = iam.create_policy(
    name="s3-read",
    effect="Allow",
    actions=["s3:GetObject"],
    resources=["arn:aws:s3:::my-bucket/*"]
)
```

**Related Terms**: Access Control, Least Privilege, Policy

---

### Kubernetes Security

**Definition**: Security practices and configurations for Kubernetes clusters and workloads.

**Example**:
```python
class KubernetesSecurityConfig:
    """Kubernetes security configurations."""

    @staticmethod
    def secure_pod_spec() -> dict:
        """Generate a secure pod specification."""
        return {
            "securityContext": {
                "runAsNonRoot": True,
                "runAsUser": 1000,
                "runAsGroup": 1000,
                "fsGroup": 1000,
            },
            "containerSecurityContext": {
                "allowPrivilegeEscalation": False,
                "readOnlyRootFilesystem": True,
                "capabilities": {
                    "drop": ["ALL"]
                },
            },
            "resources": {
                "limits": {
                    "cpu": "1000m",
                    "memory": "512Mi",
                },
                "requests": {
                    "cpu": "500m",
                    "memory": "256Mi",
                }
            },
        }

    @staticmethod
    def network_policy() -> dict:
        """Generate network policy."""
        return {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {
                "name": "default-deny-ingress"
            },
            "spec": {
                "podSelector": {},
                "policyTypes": ["Ingress"]
            }
        }
```

**Related Terms**: Pod Security, Network Policy, RBAC

---

### Network Segmentation

**Definition**: The practice of dividing a network into smaller segments to improve security and reduce the attack surface.

**Example**:
```python
class NetworkSegmentation:
    """Network segmentation configuration."""

    def __init__(self):
        self.segments = {}

    def create_segment(self, name: str, cidr: str,
                       description: str = ""):
        """Create a network segment."""
        self.segments[name] = {
            "cidr": cidr,
            "description": description,
            "allowed_communications": [],
        }

    def allow_communication(self, segment1: str, segment2: str,
                           ports: list):
        """Allow communication between segments."""
        if segment1 in self.segments:
            self.segments[segment1]["allowed_communications"].append({
                "target": segment2,
                "ports": ports,
            })

    def check_communication(self, source: str, destination: str,
                           port: int) -> bool:
        """Check if communication is allowed."""
        if source not in self.segments:
            return False

        for comm in self.segments[source]["allowed_communications"]:
            if comm["target"] == destination and port in comm["ports"]:
                return True

        return False

# Usage
network = NetworkSegmentation()
network.create_segment("web", "10.0.1.0/24", "Web servers")
network.create_segment("app", "10.0.2.0/24", "Application servers")
network.create_segment("db", "10.0.3.0/24", "Database servers")

network.allow_communication("web", "app", [80, 443])
network.allow_communication("app", "db", [5432])
```

**Related Terms**: Microsegmentation, VPC, Subnet

---

### SBOM (Software Bill of Materials)

**Definition**: A formal record containing the details and supply chain relationships of various components used in building software.

**Example**:
```python
class SBOMGenerator:
    """Generate Software Bill of Materials."""

    def __init__(self):
        self.components = []

    def add_component(self, name: str, version: str,
                      supplier: str, license: str):
        """Add a component to SBOM."""
        self.components.append({
            "name": name,
            "version": version,
            "supplier": supplier,
            "license": license,
            "hash": self._compute_hash(name, version),
        })

    def generate_sbom(self) -> dict:
        """Generate SBOM document."""
        return {
            "format": "SPDX",
            "version": "2.3",
            "creation_info": {
                "created": "2024-01-01T00:00:00Z",
                "tool": "SBOM Generator v1.0",
            },
            "packages": self.components,
            "relationships": self._generate_relationships(),
        }

    def _compute_hash(self, name: str, version: str) -> str:
        """Compute component hash."""
        import hashlib
        return hashlib.sha256(f"{name}:{version}".encode()).hexdigest()

    def _generate_relationships(self) -> list:
        """Generate component relationships."""
        return [
            {"source": "root", "target": c["name"], "type": "DEPENDS_ON"}
            for c in self.components
        ]
```

**Related Terms**: Supply Chain Security, Dependency Management, SPDX

---

### Secrets Management

**Definition**: The secure storage, access, and rotation of sensitive credentials and configuration data.

**Example**:
```python
class SecretsManager:
    """Secure secrets management."""

    def __init__(self):
        self.secrets = {}
        self.access_log = []

    def store_secret(self, name: str, value: str,
                     metadata: dict = None) -> bool:
        """Store a secret securely."""
        import hashlib
        from datetime import datetime

        self.secrets[name] = {
            "value": value,  # In practice: encrypted
            "hash": hashlib.sha256(value.encode()).hexdigest(),
            "metadata": metadata or {},
            "created_at": datetime.utcnow(),
            "version": 1,
        }
        return True

    def get_secret(self, name: str) -> str:
        """Retrieve a secret."""
        self._log_access(name, "read")
        if name in self.secrets:
            return self.secrets[name]["value"]
        return None

    def rotate_secret(self, name: str, new_value: str) -> bool:
        """Rotate a secret."""
        if name in self.secrets:
            self.secrets[name]["value"] = new_value
            self.secrets[name]["version"] += 1
            self._log_access(name, "rotate")
            return True
        return False

    def _log_access(self, name: str, action: str):
        """Log secret access."""
        from datetime import datetime
        self.access_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "secret": name,
            "action": action,
        })
```

**Related Terms**: Key Management, Vault, Credential Rotation

---

### Security Group

**Definition**: A virtual firewall that controls inbound and outbound traffic for cloud resources.

**Example**:
```python
class SecurityGroup:
    """Security group configuration."""

    def __init__(self, name: str):
        self.name = name
        self.ingress_rules = []
        self.egress_rules = []

    def add_ingress_rule(self, port: int, protocol: str,
                         source: str, description: str = ""):
        """Add an ingress rule."""
        self.ingress_rules.append({
            "port": port,
            "protocol": protocol,
            "source": source,
            "description": description,
        })

    def add_egress_rule(self, port: int, protocol: str,
                        destination: str, description: str = ""):
        """Add an egress rule."""
        self.egress_rules.append({
            "port": port,
            "protocol": protocol,
            "destination": destination,
            "description": description,
        })

    def check_access(self, direction: str, port: int,
                     source_or_dest: str) -> bool:
        """Check if access is allowed."""
        rules = self.ingress_rules if direction == "inbound" else self.egress_rules

        for rule in rules:
            if rule["port"] == port or rule["port"] == -1:  # -1 = all ports
                if self._match_cidr(source_or_dest, rule["source" if direction == "inbound" else "destination"]):
                    return True

        return False

    def _match_cidr(self, ip: str, cidr: str) -> bool:
        """Check if IP matches CIDR."""
        import ipaddress
        try:
            return ipaddress.ip_address(ip) in ipaddress.ip_network(cidr)
        except ValueError:
            return False
```

**Related Terms**: Firewall, Network Security, Access Control

---

### Vulnerability Scanning

**Definition**: The process of scanning systems, networks, and applications for security vulnerabilities.

**Example**:
```python
class VulnerabilityScanner:
    """Scan for vulnerabilities."""

    def scan_container_image(self, image_name: str) -> dict:
        """Scan a container image for vulnerabilities."""
        # Simplified - would use trivy, snyk, etc.
        return {
            "image": image_name,
            "vulnerabilities": {
                "critical": 0,
                "high": 2,
                "medium": 5,
                "low": 10,
            },
            "recommendations": [
                "Update base image to latest version",
                "Remove unused packages",
            ],
        }

    def scan_dependencies(self, requirements_file: str) -> dict:
        """Scan dependencies for vulnerabilities."""
        return {
            "file": requirements_file,
            "vulnerable_packages": [
                {"name": "requests", "version": "2.25.0", "cve": "CVE-2023-XXXXX"},
            ],
            "recommendations": [
                "Update requests to version 2.31.0",
            ],
        }
```

**Related Terms**: Security Audit, CVE, Penetration Testing

---

### Zero Trust

**Definition**: A security model that requires strict verification for every person and device trying to access resources, regardless of their location.

**Example**:
```python
class ZeroTrustArchitecture:
    """Zero Trust security model implementation."""

    def __init__(self):
        self.trust_policies = []

    def verify_identity(self, user_id: str, mfa_verified: bool) -> bool:
        """Verify user identity with MFA."""
        return mfa_verified

    def check_device_health(self, device_id: str) -> dict:
        """Check device health status."""
        return {
            "compliant": True,
            "encrypted": True,
            "patched": True,
            "antivirus": True,
        }

    def evaluate_access(self, user_id: str, resource: str,
                        context: dict) -> dict:
        """Evaluate access request with zero trust."""
        # Verify identity
        if not self.verify_identity(user_id, context.get("mfa_verified", False)):
            return {"allowed": False, "reason": "Identity not verified"}

        # Check device health
        device_health = self.check_device_health(context.get("device_id", ""))
        if not device_health["compliant"]:
            return {"allowed": False, "reason": "Device not compliant"}

        # Check context
        if not context.get("from_trusted_network", False):
            return {"allowed": False, "reason": "Not from trusted network"}

        return {"allowed": True}
```

**Related Terms**: Identity Verification, Device Trust, Network Security

---

*Part of the [AI Security Lecture Series](README.md). See also: [Lecture 09: Infrastructure Security](09-infrastructure-security-lecture.md)*
