# Lecture 09: Infrastructure Security

## Topic Overview

Infrastructure security for AI systems involves protecting the underlying infrastructure that runs, stores, and serves AI models and data. This lecture covers container security, secrets management, network security, cloud security configurations, and securing AI deployment pipelines. Proper infrastructure security is essential for protecting AI systems from external threats and ensuring reliable operation.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Secure** containerized AI deployments
2. **Manage** secrets and credentials securely
3. **Configure** network security for AI services
4. **Implement** cloud security best practices
5. **Secure** CI/CD pipelines for AI
6. **Monitor** infrastructure for security threats
7. **Apply** defense-in-depth strategies

---

## Key Concepts

### 1. Container Security

```python
# Docker security best practices
dockerfile_insecure = """
# BAD: Running as root
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
"""

dockerfile_secure = """
# GOOD: Multi-stage build, non-root user, minimal image
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9-slim
RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .
RUN chown -R appuser:appuser /app
USER appuser
CMD ["python", "app.py"]
"""

class ContainerSecurity:
    """Container security configurations."""

    @staticmethod
    def scan_image(image_name: str) -> dict:
        """Scan container image for vulnerabilities."""
        # Using trivy or similar scanner
        import subprocess
        result = subprocess.run(
            ["trivy", "image", "--format", "json", image_name],
            capture_output=True,
            text=True
        )

        # Parse results
        import json
        scan_results = json.loads(result.stdout)

        vulnerabilities = []
        for result in scan_results.get("Results", []):
            for vuln in result.get("Vulnerabilities", []):
                vulnerabilities.append({
                    "id": vuln.get("VulnerabilityID"),
                    "severity": vuln.get("Severity"),
                    "package": vuln.get("PkgName"),
                    "installed": vuln.get("InstalledVersion"),
                    "fixed": vuln.get("FixedVersion"),
                })

        return {
            "image": image_name,
            "vulnerabilities": vulnerabilities,
            "critical": sum(1 for v in vulnerabilities if v["severity"] == "CRITICAL"),
            "high": sum(1 for v in vulnerabilities if v["severity"] == "HIGH"),
        }

    @staticmethod
    def generate_kubernetes_security() -> dict:
        """Generate Kubernetes security configuration."""
        return {
            "securityContext": {
                "runAsNonRoot": True,
                "runAsUser": 1000,
                "readOnlyRootFilesystem": True,
                "allowPrivilegeEscalation": False,
                "capabilities": {
                    "drop": ["ALL"]
                }
            },
            "resources": {
                "limits": {
                    "cpu": "1",
                    "memory": "512Mi",
                },
                "requests": {
                    "cpu": "0.5",
                    "memory": "256Mi",
                }
            },
            "networkPolicy": {
                "ingress": [{"from": [{"podSelector": {}}]}],
                "egress": [{"to": [{"podSelector": {}}]}],
            }
        }
```

### 2. Secrets Management

```python
import os
import hashlib
import base64
from typing import Dict, Optional
from datetime import datetime, timedelta

class SecretsManager:
    """Secure secrets management."""

    def __init__(self):
        self.secrets: Dict[str, dict] = {}
        self.access_log: list = []

    def store_secret(self, name: str, value: str,
                     description: str = "") -> bool:
        """Store a secret securely."""
        # In practice: encrypt at rest using KMS
        # Here: simplified hash-based storage
        secret_hash = hashlib.sha256(value.encode()).hexdigest()

        self.secrets[name] = {
            "hash": secret_hash,
            "description": description,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(days=90),
            "version": 1,
        }

        self._log_access(name, "store")
        return True

    def get_secret(self, name: str, version: int = None) -> Optional[str]:
        """Retrieve a secret."""
        if name not in self.secrets:
            return None

        secret_info = self.secrets[name]

        # Check expiration
        if datetime.utcnow() > secret_info["expires_at"]:
            raise ValueError(f"Secret {name} has expired")

        self._log_access(name, "retrieve")

        # In practice: decrypt and return actual value
        # Here: return hash for demonstration
        return secret_info["hash"]

    def rotate_secret(self, name: str, new_value: str) -> bool:
        """Rotate a secret to a new value."""
        if name not in self.secrets:
            return False

        self.secrets[name]["version"] += 1
        self.secrets[name]["hash"] = hashlib.sha256(new_value.encode()).hexdigest()
        self.secrets[name]["expires_at"] = datetime.utcnow() + timedelta(days=90)

        self._log_access(name, "rotate")
        return True

    def delete_secret(self, name: str) -> bool:
        """Securely delete a secret."""
        if name in self.secrets:
            del self.secrets[name]
            self._log_access(name, "delete")
            return True
        return False

    def list_secrets(self, include_expired: bool = False) -> list:
        """List all secrets (without values)."""
        secrets_list = []
        for name, info in self.secrets.items():
            if not include_expired and datetime.utcnow() > info["expires_at"]:
                continue
            secrets_list.append({
                "name": name,
                "description": info["description"],
                "expires_at": info["expires_at"].isoformat(),
                "version": info["version"],
            })
        return secrets_list

    def _log_access(self, secret_name: str, action: str):
        """Log secret access for audit."""
        self.access_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "secret": secret_name,
            "action": action,
        })

class EnvironmentSecrets:
    """Manage secrets from environment variables."""

    @staticmethod
    def load_from_env(prefix: str = "SECRET_") -> dict:
        """Load secrets from environment variables."""
        secrets = {}
        for key, value in os.environ.items():
            if key.startswith(prefix):
                secret_name = key[len(prefix):].lower()
                secrets[secret_name] = value
        return secrets

    @staticmethod
    def validate_secret_security(secret_value: str) -> dict:
        """Validate secret meets security requirements."""
        issues = []

        if len(secret_value) < 16:
            issues.append("Secret too short (minimum 16 characters)")

        if secret_value.isalnum():
            issues.append("Secret should contain special characters")

        if secret_value.lower() in ["password", "secret", "123456"]:
            issues.append("Secret is too common")

        return {
            "secure": len(issues) == 0,
            "issues": issues,
            "strength": "strong" if len(issues) == 0 else "weak",
        }
```

### 3. Network Security

```python
class NetworkSecurityConfig:
    """Network security configurations for AI services."""

    @staticmethod
    def generate_firewall_rules() -> list:
        """Generate firewall rules for AI infrastructure."""
        return [
            {
                "name": "allow-https",
                "protocol": "tcp",
                "port": 443,
                "source": "0.0.0.0/0",
                "action": "allow",
                "description": "Allow HTTPS traffic",
            },
            {
                "name": "allow-ssh-from-bastion",
                "protocol": "tcp",
                "port": 22,
                "source": "10.0.1.0/24",  # Bastion subnet only
                "action": "allow",
                "description": "Allow SSH from bastion host",
            },
            {
                "name": "deny-all-inbound",
                "protocol": "*",
                "port": "*",
                "source": "0.0.0.0/0",
                "action": "deny",
                "description": "Deny all other inbound traffic",
            },
        ]

    @staticmethod
    def generate_vpc_config() -> dict:
        """Generate VPC configuration for AI services."""
        return {
            "vpc": {
                "cidr": "10.0.0.0/16",
                "enable_dns_support": True,
                "enable_dns_hostnames": True,
            },
            "subnets": {
                "public": {
                    "cidr": "10.0.1.0/24",
                    "availability_zones": ["us-east-1a", "us-east-1b"],
                },
                "private": {
                    "cidr": "10.0.2.0/24",
                    "availability_zones": ["us-east-1a", "us-east-1b"],
                },
                "database": {
                    "cidr": "10.0.3.0/24",
                    "availability_zones": ["us-east-1a", "us-east-1b"],
                },
            },
            "security_groups": {
                "ai-service": {
                    "ingress": [
                        {"port": 443, "source": "0.0.0.0/0"},
                    ],
                    "egress": [
                        {"port": 443, "destination": "0.0.0.0/0"},
                        {"port": 5432, "destination": "10.0.3.0/24"},
                    ],
                },
            },
        }

    @staticmethod
    def check_network_exposure(endpoints: list) -> list:
        """Check for network exposure issues."""
        issues = []

        for endpoint in endpoints:
            if endpoint.get("public") and not endpoint.get("https"):
                issues.append({
                    "endpoint": endpoint["name"],
                    "issue": "Public endpoint without HTTPS",
                })

            if endpoint.get("port") == 22 and endpoint.get("source") == "0.0.0.0/0":
                issues.append({
                    "endpoint": endpoint["name"],
                    "issue": "SSH exposed to internet",
                })

        return issues
```

### 4. Cloud Security

```python
class CloudSecurityChecker:
    """Check cloud security configurations."""

    def __init__(self, provider: str = "aws"):
        self.provider = provider

    def check_iam_security(self, iam_config: dict) -> dict:
        """Check IAM security configuration."""
        issues = []

        # Check for root account usage
        if iam_config.get("root_access"):
            issues.append({
                "severity": "critical",
                "issue": "Root account has access keys",
                "recommendation": "Remove root access keys",
            })

        # Check for overly permissive policies
        for policy in iam_config.get("policies", []):
            if policy.get("effect") == "Allow" and policy.get("resource") == "*":
                issues.append({
                    "severity": "high",
                    "issue": f"Overly permissive policy: {policy['name']}",
                    "recommendation": "Apply principle of least privilege",
                })

        # Check for unused credentials
        for credential in iam_config.get("credentials", []):
            if credential.get("last_used") is None:
                issues.append({
                    "severity": "medium",
                    "issue": f"Unused credential: {credential['id']}",
                    "recommendation": "Remove unused credentials",
                })

        return {
            "compliant": len(issues) == 0,
            "issues": issues,
        }

    def check_s3_security(self, s3_config: dict) -> dict:
        """Check S3 bucket security."""
        issues = []

        for bucket in s3_config.get("buckets", []):
            if bucket.get("public_access"):
                issues.append({
                    "severity": "critical",
                    "bucket": bucket["name"],
                    "issue": "Bucket has public access",
                })

            if not bucket.get("encryption"):
                issues.append({
                    "severity": "high",
                    "bucket": bucket["name"],
                    "issue": "Bucket encryption not enabled",
                })

            if not bucket.get("versioning"):
                issues.append({
                    "severity": "medium",
                    "bucket": bucket["name"],
                    "issue": "Bucket versioning not enabled",
                })

        return {
            "compliant": len(issues) == 0,
            "issues": issues,
        }

    def check_security_groups(self, security_groups: list) -> dict:
        """Check security group configurations."""
        issues = []

        for sg in security_groups:
            for rule in sg.get("ingress_rules", []):
                if rule.get("cidr") == "0.0.0.0/0":
                    if rule.get("port") in [22, 3389, 3306, 5432]:
                        issues.append({
                            "severity": "critical",
                            "security_group": sg["name"],
                            "issue": f"Management port {rule['port']} open to internet",
                        })

        return {
            "compliant": len(issues) == 0,
            "issues": issues,
        }
```

### 5. CI/CD Pipeline Security

```python
class CICDSecurityChecker:
    """Check CI/CD pipeline security."""

    def __init__(self):
        self.checks = []

    def check_pipeline_security(self, pipeline_config: dict) -> dict:
        """Check CI/CD pipeline for security issues."""
        issues = []

        # Check for secrets in code
        if pipeline_config.get("secrets_in_code"):
            issues.append({
                "severity": "critical",
                "issue": "Secrets found in code",
                "recommendation": "Use secret management",
            })

        # Check for unpinned dependencies
        for stage in pipeline_config.get("stages", []):
            if stage.get("unpinned_deps"):
                issues.append({
                    "severity": "high",
                    "stage": stage["name"],
                    "issue": "Unpinned dependencies",
                })

        # Check for missing security scans
        if not pipeline_config.get("security_scans"):
            issues.append({
                "severity": "high",
                "issue": "No security scans configured",
                "recommendation": "Add SAST, DAST, and dependency scanning",
            })

        # Check for missing image scanning
        if pipeline_config.get("container_build") and not pipeline_config.get("image_scan"):
            issues.append({
                "severity": "high",
                "issue": "Container images not scanned",
                "recommendation": "Add container image scanning",
            })

        return {
            "secure": len(issues) == 0,
            "issues": issues,
        }

    def generate_secure_pipeline(self) -> dict:
        """Generate a secure CI/CD pipeline configuration."""
        return {
            "stages": [
                {
                    "name": "lint",
                    "security": ["secret_detection", "dependency_check"],
                },
                {
                    "name": "test",
                    "security": ["sast_scan", "unit_tests"],
                },
                {
                    "name": "build",
                    "security": ["image_scan", "sbom_generation"],
                },
                {
                    "name": "deploy",
                    "security": ["infrastructure_scan", "compliance_check"],
                },
            ],
            "secret_management": {
                "provider": "vault",
                "rotation": True,
                "access_logging": True,
            },
            "compliance": {
                "required_checks": ["secret_scan", "vulnerability_scan"],
                "approval_required": True,
            },
        }
```

---

## Common Mistakes to Avoid

1. **Running containers as root** — Use non-root users
2. **Hardcoding secrets** — Use secret management systems
3. **Overly permissive network rules** — Apply least privilege
4. **No vulnerability scanning** — Scan images and dependencies
5. **Missing audit logs** — Log all infrastructure changes
6. **No encryption at rest** — Encrypt sensitive data
7. **Public S3 buckets** — Never make buckets public
8. **Ignoring compliance** — Follow security standards

---

## Best Practices

1. **Defense in depth** — Multiple security layers
2. **Least privilege** — Minimum necessary access
3. **Encryption everywhere** — At rest and in transit
4. **Regular audits** — Scan for vulnerabilities regularly
5. **Secrets rotation** — Rotate credentials regularly
6. **Network segmentation** — Isolate different components
7. **Monitoring and alerting** — Detect and respond to threats
8. **Incident response plan** — Have a plan for security incidents

---

## Practice Exercises

### Exercise 1: Container Security (Easy)
Write a secure Dockerfile for an AI application.

### Exercise 2: Secrets Management (Medium)
Implement a secrets management system with rotation.

### Exercise 3: Network Configuration (Medium)
Design a secure network architecture for AI services.

### Exercise 4: Security Audit (Hard)
Perform a comprehensive security audit of an AI infrastructure.

---

## Summary

Infrastructure security protects the foundation of AI systems. Key takeaways:

- **Secure containers** — Use non-root users, minimal images, scan for vulnerabilities
- **Manage secrets** — Never hardcode, rotate regularly, audit access
- **Network security** — Segment networks, apply least privilege
- **Cloud security** — Check IAM, S3, security groups regularly
- **CI/CD security** — Scan code, dependencies, and images
- **Monitor everything** — Log and alert on suspicious activity

---

## References

- [CIS Benchmarks](https://www.cisecurity.org/benchmark)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [AWS Security Best Practices](https://docs.aws.amazon.com/general/latest/gr/aws-security-best-practices.html)
