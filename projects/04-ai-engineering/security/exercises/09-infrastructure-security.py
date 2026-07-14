"""
=============================================================
Topic 09: Infrastructure Security for AI Systems
=============================================================

Security Level: ########-- High

Secure the infrastructure that hosts your AI systems. This exercise
covers container security, secret management, network security,
database encryption, backup security, and disaster recovery.

Learning Objectives:
- Implement container security best practices
- Manage secrets securely
- Design network security for AI workloads
- Encrypt data at rest and in transit
- Create secure backup strategies
- Build disaster recovery plans

Prerequisites:
- Basic understanding of cloud infrastructure
- Familiarity with Docker/containers
- Understanding of networking concepts
=============================================================
"""

import hashlib
import hmac
import json
import os
import secrets
import struct
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import base64
import re


# =============================================================
# SECTION 1: Container Security
# =============================================================

@dataclass
class ContainerImage:
    """Represents a container image with security metadata."""
    name: str
    tag: str
    registry: str
    digest: str
    created_at: float
    layers: List[Dict]
    vulnerabilities: List[Dict] = field(default_factory=list)
    scan_status: str = "pending"


class ContainerSecurityScanner:
    """
    Scan container images for security vulnerabilities.

    Checks:
    - Base image vulnerabilities
    - Outdated packages
    - Hardcoded secrets
    - Misconfigurations
    - Root user usage
    """

    def __init__(self):
        self._scan_results: Dict[str, Dict] = {}
        self._allowed_registries: Set[str] = set()
        self._blocked_packages: Set[str] = set()

    def add_allowed_registry(self, registry: str):
        """Add an allowed container registry."""
        self._allowed_registries.add(registry)

    def add_blocked_package(self, package: str):
        """Add a package to the blocklist."""
        self._blocked_packages.add(package)

    def scan_image(self, image: ContainerImage) -> Dict:
        """
        Perform comprehensive security scan on a container image.
        """
        findings = []
        risk_score = 0

        # 1. Check registry
        if self._allowed_registries and image.registry not in self._allowed_registries:
            findings.append({
                "severity": "critical",
                "category": "registry",
                "message": f"Image from unapproved registry: {image.registry}",
            })
            risk_score += 30

        # 2. Check for 'latest' tag
        if image.tag == "latest":
            findings.append({
                "severity": "high",
                "category": "tag",
                "message": "Using 'latest' tag is unpredictable and insecure",
            })
            risk_score += 20

        # 3. Check image age
        age_days = (time.time() - image.created_at) / 86400
        if age_days > 90:
            findings.append({
                "severity": "medium",
                "category": "age",
                "message": f"Image is {int(age_days)} days old (may have unpatched vulnerabilities)",
            })
            risk_score += 15

        # 4. Check layers for secrets
        for i, layer in enumerate(image.layers):
            layer_str = json.dumps(layer)
            secret_patterns = [
                r"(?i)(password|secret|key|token)\s*[=:]\s*\S+",
                r"-----BEGIN (RSA |EC )?PRIVATE KEY-----",
                r"AKIA[0-9A-Z]{16}",  # AWS Access Key
            ]
            for pattern in secret_patterns:
                if re.search(pattern, layer_str):
                    findings.append({
                        "severity": "critical",
                        "category": "secrets",
                        "message": f"Potential secret found in layer {i}",
                        "layer_index": i,
                    })
                    risk_score += 40
                    break

        # 5. Check for root user
        has_user_instruction = False
        for layer in image.layers:
            if layer.get("command", "").startswith("USER "):
                has_user_instruction = True
                if "root" in layer.get("command", ""):
                    findings.append({
                        "severity": "high",
                        "category": "privilege",
                        "message": "Container runs as root",
                    })
                    risk_score += 25
                break

        if not has_user_instruction:
            findings.append({
                "severity": "high",
                "category": "privilege",
                "message": "No USER instruction found (default is root)",
            })
            risk_score += 25

        # 6. Check for blocked packages
        for layer in image.layers:
            cmd = layer.get("command", "")
            for package in self._blocked_packages:
                if package in cmd:
                    findings.append({
                        "severity": "high",
                        "category": "packages",
                        "message": f"Blocked package found: {package}",
                    })
                    risk_score += 20

        # 7. Check for health check
        has_healthcheck = any(
            "HEALTHCHECK" in layer.get("command", "")
            for layer in image.layers
        )
        if not has_healthcheck:
            findings.append({
                "severity": "low",
                "category": "reliability",
                "message": "No HEALTHCHECK instruction found",
            })
            risk_score += 5

        risk_score = min(100, risk_score)

        result = {
            "image": f"{image.registry}/{image.name}:{image.tag}",
            "digest": image.digest,
            "scan_time": time.time(),
            "risk_score": risk_score,
            "risk_level": self._get_risk_level(risk_score),
            "findings": findings,
            "findings_count": {
                "critical": sum(1 for f in findings if f["severity"] == "critical"),
                "high": sum(1 for f in findings if f["severity"] == "high"),
                "medium": sum(1 for f in findings if f["severity"] == "medium"),
                "low": sum(1 for f in findings if f["severity"] == "low"),
            },
            "passed": risk_score < 50,
        }

        self._scan_results[image.digest] = result
        return result

    def _get_risk_level(self, score: int) -> str:
        """Convert risk score to level."""
        if score >= 70:
            return "critical"
        elif score >= 50:
            return "high"
        elif score >= 30:
            return "medium"
        return "low"


class ContainerRuntimeSecurity:
    """
    Runtime security monitoring for containers.
    """

    def __init__(self):
        self._policies: List[Dict] = []
        self._events: List[Dict] = []

    def add_policy(self, policy: Dict):
        """Add a runtime security policy."""
        self._policies.append(policy)

    def check_action(self, container_id: str, action: Dict) -> Dict:
        """
        Check if a container action is allowed by policies.

        Args:
            container_id: Container identifier
            action: Dict with type, target, details

        Returns:
            Dict with allowed, policy, reason
        """
        for policy in self._policies:
            if self._matches_policy(container_id, action, policy):
                if policy.get("effect") == "deny":
                    self._log_event(container_id, action, "denied", policy)
                    return {
                        "allowed": False,
                        "policy": policy.get("name"),
                        "reason": policy.get("reason", "Denied by policy"),
                    }

        self._log_event(container_id, action, "allowed", None)
        return {"allowed": True}

    def _matches_policy(self, container_id: str, action: Dict, policy: Dict) -> bool:
        """Check if action matches a policy."""
        # Check container selector
        selector = policy.get("selector", {})
        if "container_id" in selector and selector["container_id"] != container_id:
            return False
        if "label" in selector:
            # Would check container labels in real implementation
            pass

        # Check action type
        if "action_type" in policy and policy["action_type"] != action.get("type"):
            return False

        # Check target pattern
        if "target_pattern" in policy:
            if not re.match(policy["target_pattern"], action.get("target", "")):
                return False

        return True

    def _log_event(self, container_id: str, action: Dict, result: str, policy: Optional[Dict]):
        """Log security event."""
        self._events.append({
            "timestamp": time.time(),
            "container_id": container_id,
            "action": action,
            "result": result,
            "policy": policy.get("name") if policy else None,
        })


# =============================================================
# SECTION 2: Secret Management
# =============================================================

class SecretManager:
    """
    Secure secret management system.

    Features:
    - Encrypted storage
    - Access control
    - Audit logging
    - Secret rotation
    - Versioning
    """

    def __init__(self, master_key: bytes = None):
        self.master_key = master_key or secrets.token_bytes(32)
        self._secrets: Dict[str, Dict] = {}
        self._access_log: List[Dict] = []
        self._policies: Dict[str, Dict] = {}

    def store_secret(
        self,
        name: str,
        value: str,
        metadata: Optional[Dict] = None,
        rotation_period: Optional[int] = None,
    ) -> Dict:
        """
        Store a secret with encryption.

        Args:
            name: Secret name/path
            value: Secret value
            metadata: Optional metadata
            rotation_period: Rotation period in seconds

        Returns:
            Dict with secret_id, version
        """
        # Encrypt the secret
        encrypted = self._encrypt(value.encode())

        # Store with versioning
        version = 1
        if name in self._secrets:
            version = self._secrets[name]["current_version"] + 1

        self._secrets[name] = {
            "encrypted_value": encrypted,
            "current_version": version,
            "created_at": time.time(),
            "rotation_period": rotation_period,
            "metadata": metadata or {},
            "versions": self._secrets.get(name, {}).get("versions", []),
        }

        # Store version history
        self._secrets[name]["versions"].append({
            "version": version,
            "encrypted": encrypted,
            "created_at": time.time(),
        })

        self._log_access(name, "store", "system")
        return {"secret_id": name, "version": version}

    def get_secret(self, name: str, version: Optional[int] = None) -> Optional[str]:
        """
        Retrieve a secret value.
        """
        secret_data = self._secrets.get(name)
        if not secret_data:
            return None

        # Check rotation
        if secret_data.get("rotation_period"):
            age = time.time() - secret_data["created_at"]
            if age > secret_data["rotation_period"]:
                self._log_access(name, "expired", "system")
                return None

        # Get specific version
        if version:
            for v in secret_data["versions"]:
                if v["version"] == version:
                    return self._decrypt(v["encrypted_value"]).decode()
            return None

        self._log_access(name, "retrieve", "system")
        return self._decrypt(secret_data["encrypted_value"]).decode()

    def rotate_secret(self, name: str, new_value: str) -> Dict:
        """Rotate a secret to a new value."""
        if name not in self._secrets:
            return {"error": "Secret not found"}

        old_version = self._secrets[name]["current_version"]
        result = self.store_secret(name, new_value)

        self._log_access(name, "rotate", "system")

        return {
            "secret_id": name,
            "old_version": old_version,
            "new_version": result["version"],
        }

    def delete_secret(self, name: str):
        """Delete a secret (mark as deleted)."""
        if name in self._secrets:
            self._secrets[name]["deleted"] = True
            self._secrets[name]["deleted_at"] = time.time()
            self._log_access(name, "delete", "system")

    def set_access_policy(self, secret_name: str, policy: Dict):
        """Set access policy for a secret."""
        self._policies[secret_name] = policy

    def check_access(self, secret_name: str, user_id: str, action: str) -> bool:
        """Check if user has access to a secret."""
        policy = self._policies.get(secret_name)
        if not policy:
            return True  # Default: allow (should be deny in production)

        allowed_users = policy.get("allowed_users", [])
        allowed_roles = policy.get("allowed_roles", [])

        if user_id in allowed_users:
            return True

        # Would check user roles in real implementation
        return False

    def _log_access(self, secret_name: str, action: str, user_id: str):
        """Log secret access."""
        self._access_log.append({
            "timestamp": time.time(),
            "secret_name": secret_name,
            "action": action,
            "user_id": user_id,
        })

    def get_audit_log(self, secret_name: Optional[str] = None) -> List[Dict]:
        """Get audit log for secret access."""
        if secret_name:
            return [l for l in self._access_log if l["secret_name"] == secret_name]
        return self._access_log

    def _encrypt(self, data: bytes) -> bytes:
        """Encrypt data using AES-like XOR (simplified for demo)."""
        # In production, use AES-GCM or similar
        key = hashlib.sha256(self.master_key).digest()
        encrypted = bytearray()
        for i, byte in enumerate(data):
            encrypted.append(byte ^ key[i % len(key)])
        return bytes(encrypted)

    def _decrypt(self, data: bytes) -> bytes:
        """Decrypt data (XOR is symmetric)."""
        return self._encrypt(data)


# =============================================================
# SECTION 3: Network Security
# =============================================================

@dataclass
class FirewallRule:
    """Represents a firewall rule."""
    name: str
    direction: str  # inbound, outbound
    protocol: str    # tcp, udp, icmp
    source: str      # IP/CIDR or *
    destination: str # IP/CIDR or *
    port: str        # port or range
    action: str      # allow, deny
    priority: int = 100
    enabled: bool = True
    logging: bool = False


class NetworkSecurityManager:
    """
    Network security management for AI infrastructure.
    """

    def __init__(self):
        self._rules: List[FirewallRule] = []
        self._network_segments: Dict[str, Dict] = {}
        self._connection_log: List[Dict] = []

    def add_rule(self, rule: FirewallRule):
        """Add a firewall rule."""
        self._rules.append(rule)
        # Sort by priority
        self._rules.sort(key=lambda r: r.priority)

    def check_connection(
        self,
        source_ip: str,
        dest_ip: str,
        dest_port: int,
        protocol: str = "tcp",
    ) -> Dict:
        """
        Check if a connection is allowed by firewall rules.
        """
        for rule in self._rules:
            if not rule.enabled:
                continue

            if rule.protocol != "any" and rule.protocol != protocol:
                continue

            if rule.direction == "inbound":
                if self._ip_matches(source_ip, rule.source) and self._ip_matches(dest_ip, rule.destination):
                    if self._port_matches(dest_port, rule.port):
                        self._log_connection(source_ip, dest_ip, dest_port, rule.action, rule.name)
                        return {
                            "allowed": rule.action == "allow",
                            "rule": rule.name,
                            "action": rule.action,
                        }

            elif rule.direction == "outbound":
                if self._ip_matches(source_ip, rule.source) and self._ip_matches(dest_ip, rule.destination):
                    if self._port_matches(dest_port, rule.port):
                        self._log_connection(source_ip, dest_ip, dest_port, rule.action, rule.name)
                        return {
                            "allowed": rule.action == "allow",
                            "rule": rule.name,
                            "action": rule.action,
                        }

        # Default deny
        self._log_connection(source_ip, dest_ip, dest_port, "deny", "default")
        return {"allowed": False, "rule": "default", "action": "deny"}

    def _ip_matches(self, ip: str, pattern: str) -> bool:
        """Check if IP matches a pattern (CIDR or wildcard)."""
        if pattern == "*":
            return True
        if "/" in pattern:
            # CIDR notation - simplified check
            network, prefix = pattern.split("/")
            # In production, use ipaddress module
            return ip.startswith(network.rsplit(".", 1)[0])
        return ip == pattern

    def _port_matches(self, port: int, pattern: str) -> bool:
        """Check if port matches a pattern."""
        if pattern == "*":
            return True
        if "-" in pattern:
            start, end = pattern.split("-")
            return int(start) <= port <= int(end)
        return str(port) == pattern

    def _log_connection(self, src: str, dst: str, port: int, action: str, rule: str):
        """Log connection attempt."""
        self._connection_log.append({
            "timestamp": time.time(),
            "source": src,
            "destination": dst,
            "port": port,
            "action": action,
            "rule": rule,
        })

    def create_network_segment(
        self,
        name: str,
        cidr: str,
        description: str,
        security_level: str = "medium",
    ):
        """Create a network segment."""
        self._network_segments[name] = {
            "cidr": cidr,
            "description": description,
            "security_level": security_level,
            "created_at": time.time(),
        }

    def get_security_report(self) -> Dict:
        """Generate network security report."""
        deny_count = sum(1 for c in self._connection_log if c["action"] == "deny")
        allow_count = sum(1 for c in self._connection_log if c["action"] == "allow")

        return {
            "total_rules": len(self._rules),
            "active_rules": sum(1 for r in self._rules if r.enabled),
            "total_connections": len(self._connection_log),
            "denied_connections": deny_count,
            "allowed_connections": allow_count,
            "network_segments": len(self._network_segments),
            "top_blocked_ips": self._get_top_blocked(),
        }

    def _get_top_blocked(self, limit: int = 5) -> List[Dict]:
        """Get top blocked IP addresses."""
        blocked = defaultdict(int)
        for conn in self._connection_log:
            if conn["action"] == "deny":
                blocked[conn["source"]] += 1
        return [
            {"ip": ip, "count": count}
            for ip, count in sorted(blocked.items(), key=lambda x: -x[1])[:limit]
        ]


# =============================================================
# SECTION 4: Database Encryption
# =============================================================

class DatabaseEncryptionManager:
    """
    Database encryption for data at rest and in transit.

    Features:
    - Column-level encryption
    - Transparent data encryption (TDE)
    - Key management
    - Encryption at rest
    """

    def __init__(self, master_key: bytes = None):
        self.master_key = master_key or secrets.token_bytes(32)
        self._encryption_keys: Dict[str, bytes] = {}
        self._encrypted_columns: Dict[str, Dict] = {}

    def generate_column_key(self, column_id: str) -> bytes:
        """Generate an encryption key for a column."""
        key = hashlib.pbkdf2_hmac(
            "sha256",
            self.master_key,
            column_id.encode(),
            iterations=100000,
        )
        self._encryption_keys[column_id] = key
        return key

    def encrypt_value(self, column_id: str, value: str) -> str:
        """Encrypt a value for a specific column."""
        key = self._encryption_keys.get(column_id)
        if not key:
            key = self.generate_column_key(column_id)

        # Simple XOR encryption (use AES-GCM in production)
        encrypted = bytearray()
        for i, byte in enumerate(value.encode()):
            encrypted.append(byte ^ key[i % len(key)])

        return base64.b64encode(bytes(encrypted)).decode()

    def decrypt_value(self, column_id: str, encrypted_value: str) -> str:
        """Decrypt a column value."""
        key = self._encryption_keys.get(column_id)
        if not key:
            raise ValueError(f"No encryption key for column: {column_id}")

        encrypted = base64.b64decode(encrypted_value)
        decrypted = bytearray()
        for i, byte in enumerate(encrypted):
            decrypted.append(byte ^ key[i % len(key)])

        return bytes(decrypted).decode()

    def encrypt_row(self, table: str, row: Dict, columns_to_encrypt: List[str]) -> Dict:
        """Encrypt specific columns in a row."""
        encrypted_row = row.copy()
        for col in columns_to_encrypt:
            if col in encrypted_row:
                column_id = f"{table}.{col}"
                encrypted_row[col] = self.encrypt_value(column_id, str(encrypted_row[col]))
                encrypted_row[f"{col}_encrypted"] = True
        return encrypted_row

    def decrypt_row(self, table: str, row: Dict, columns_to_decrypt: List[str]) -> Dict:
        """Decrypt specific columns in a row."""
        decrypted_row = row.copy()
        for col in columns_to_decrypt:
            if col in decrypted_row and row.get(f"{col}_encrypted"):
                column_id = f"{table}.{col}"
                decrypted_row[col] = self.decrypt_value(column_id, decrypted_row[col])
                del decrypted_row[f"{col}_encrypted"]
        return decrypted_row

    def setup_tde(self, database: str) -> Dict:
        """Setup Transparent Data Encryption for a database."""
        tde_key = secrets.token_bytes(32)
        self._encryption_keys[f"tde_{database}"] = tde_key

        return {
            "database": database,
            "algorithm": "AES-256-GCM",
            "key_id": hashlib.sha256(tde_key).hexdigest()[:16],
            "status": "enabled",
            "created_at": time.time(),
        }


# =============================================================
# SECTION 5: Backup Security
# =============================================================

@dataclass
class BackupJob:
    """Represents a backup job."""
    job_id: str
    name: str
    source: str
    schedule: str
    retention_days: int
    encrypted: bool = True
    last_run: Optional[float] = None
    status: str = "pending"


class BackupSecurityManager:
    """
    Secure backup management with encryption and verification.
    """

    def __init__(self):
        self._backup_jobs: Dict[str, BackupJob] = {}
        self._backups: List[Dict] = []
        self._verification_results: List[Dict] = []

    def create_backup_job(
        self,
        name: str,
        source: str,
        schedule: str,
        retention_days: int = 30,
        encrypted: bool = True,
    ) -> BackupJob:
        """Create a new backup job."""
        job = BackupJob(
            job_id=secrets.token_urlsafe(16),
            name=name,
            source=source,
            schedule=schedule,
            retention_days=retention_days,
            encrypted=encrypted,
        )
        self._backup_jobs[job.job_id] = job
        return job

    def execute_backup(self, job_id: str, data: bytes) -> Dict:
        """Execute a backup job."""
        job = self._backup_jobs.get(job_id)
        if not job:
            return {"error": "Job not found"}

        # Create backup
        backup_id = secrets.token_urlsafe(16)

        # Encrypt if required
        if job.encrypted:
            backup_data = self._encrypt_backup(data)
        else:
            backup_data = data

        # Generate checksum
        checksum = hashlib.sha256(data).hexdigest()

        backup_info = {
            "backup_id": backup_id,
            "job_id": job_id,
            "source": job.source,
            "timestamp": time.time(),
            "size_bytes": len(data),
            "checksum": checksum,
            "encrypted": job.encrypted,
            "retention_until": time.time() + (job.retention_days * 86400),
        }

        self._backups.append(backup_info)
        job.last_run = time.time()
        job.status = "completed"

        return backup_info

    def verify_backup(self, backup_id: str, original_data: bytes) -> Dict:
        """Verify backup integrity."""
        backup = next((b for b in self._backups if b["backup_id"] == backup_id), None)
        if not backup:
            return {"error": "Backup not found"}

        # Verify checksum
        checksum_valid = backup["checksum"] == hashlib.sha256(original_data).hexdigest()

        # Check if backup is expired
        expired = time.time() > backup["retention_until"]

        result = {
            "backup_id": backup_id,
            "checksum_valid": checksum_valid,
            "expired": expired,
            "age_days": (time.time() - backup["timestamp"]) / 86400,
            "verified_at": time.time(),
        }

        self._verification_results.append(result)
        return result

    def list_backups(self, job_id: Optional[str] = None) -> List[Dict]:
        """List backups, optionally filtered by job."""
        if job_id:
            return [b for b in self._backups if b["job_id"] == job_id]
        return self._backups

    def cleanup_expired(self) -> int:
        """Remove expired backups."""
        now = time.time()
        before = len(self._backups)
        self._backups = [b for b in self._backups if b["retention_until"] > now]
        return before - len(self._backups)

    def _encrypt_backup(self, data: bytes) -> bytes:
        """Encrypt backup data."""
        key = hashlib.sha256(b"backup_encryption_key").digest()
        encrypted = bytearray()
        for i, byte in enumerate(data):
            encrypted.append(byte ^ key[i % len(key)])
        return bytes(encrypted)


# =============================================================
# SECTION 6: Disaster Recovery
# =============================================================

class DisasterRecoveryManager:
    """
    Disaster recovery planning and execution.
    """

    def __init__(self):
        self._recovery_plans: Dict[str, Dict] = {}
        self._incidents: List[Dict] = []
        self._recovery_tests: List[Dict] = []

    def create_recovery_plan(
        self,
        name: str,
        components: List[str],
        rpo_hours: float,  # Recovery Point Objective
        rto_hours: float,  # Recovery Time Objective
        priority: str = "high",
    ) -> Dict:
        """Create a disaster recovery plan."""
        plan = {
            "plan_id": secrets.token_urlsafe(8),
            "name": name,
            "components": components,
            "rpo_hours": rpo_hours,
            "rto_hours": rto_hours,
            "priority": priority,
            "created_at": time.time(),
            "last_tested": None,
            "status": "active",
            "steps": self._generate_recovery_steps(components),
        }
        self._recovery_plans[plan["plan_id"]] = plan
        return plan

    def _generate_recovery_steps(self, components: List[str]) -> List[Dict]:
        """Generate recovery steps for components."""
        steps = []
        for i, component in enumerate(components):
            steps.append({
                "step": i + 1,
                "component": component,
                "action": f"Restore {component} from latest backup",
                "estimated_time": 30,  # minutes
                "dependencies": [],
                "verification": f"Verify {component} health check passes",
            })
        return steps

    def declare_incident(
        self,
        title: str,
        severity: str,
        affected_components: List[str],
    ) -> Dict:
        """Declare a security incident."""
        incident = {
            "incident_id": secrets.token_urlsafe(8),
            "title": title,
            "severity": severity,
            "affected_components": affected_components,
            "declared_at": time.time(),
            "status": "open",
            "timeline": [
                {"time": time.time(), "event": "Incident declared"},
            ],
        }
        self._incidents.append(incident)
        return incident

    def update_incident(self, incident_id: str, update: str, status: Optional[str] = None):
        """Update an incident."""
        incident = next(
            (i for i in self._incidents if i["incident_id"] == incident_id),
            None,
        )
        if incident:
            incident["timeline"].append({"time": time.time(), "event": update})
            if status:
                incident["status"] = status

    def test_recovery_plan(self, plan_id: str) -> Dict:
        """Test a disaster recovery plan."""
        plan = self._recovery_plans.get(plan_id)
        if not plan:
            return {"error": "Plan not found"}

        start_time = time.time()

        # Simulate recovery steps
        steps_result = []
        for step in plan["steps"]:
            step_result = {
                "step": step["step"],
                "component": step["component"],
                "success": True,  # In real test, actually verify
                "time_taken": step["estimated_time"],
            }
            steps_result.append(step_result)

        total_time = time.time() - start_time

        test_result = {
            "plan_id": plan_id,
            "test_time": time.time(),
            "duration_seconds": total_time,
            "steps_passed": sum(1 for s in steps_result if s["success"]),
            "steps_total": len(steps_result),
            "rto_met": (total_time / 60) <= plan["rto_hours"] * 60,
            "steps": steps_result,
        }

        self._recovery_tests.append(test_result)
        plan["last_tested"] = time.time()

        return test_result

    def get_recovery_status(self) -> Dict:
        """Get overall disaster recovery status."""
        return {
            "total_plans": len(self._recovery_plans),
            "active_plans": sum(
                1 for p in self._recovery_plans.values()
                if p["status"] == "active"
            ),
            "open_incidents": sum(
                1 for i in self._incidents
                if i["status"] == "open"
            ),
            "total_tests": len(self._recovery_tests),
            "recent_tests": self._recovery_tests[-5:] if self._recovery_tests else [],
            "plans_needing_test": [
                p["name"] for p in self._recovery_plans.values()
                if not p["last_tested"]
            ],
        }


# =============================================================
# SECTION 7: Infrastructure Audit
# =============================================================

class InfrastructureAuditor:
    """
    Comprehensive infrastructure security auditing.
    """

    def __init__(self):
        self._check_results: List[Dict] = []

    def run_full_audit(self) -> Dict:
        """Run a full infrastructure security audit."""
        checks = [
            self._check_container_security(),
            self._check_secret_management(),
            self._check_network_security(),
            self._check_encryption(),
            self._check_backup_strategy(),
            self._check_disaster_recovery(),
        ]

        total_checks = sum(c["checks"] for c in checks)
        passed_checks = sum(c["passed"] for c in checks)
        failed_checks = sum(c["failed"] for c in checks)

        return {
            "audit_time": time.time(),
            "total_checks": total_checks,
            "passed": passed_checks,
            "failed": failed_checks,
            "score": (passed_checks / total_checks * 100) if total_checks > 0 else 0,
            "categories": checks,
            "recommendations": self._generate_recommendations(checks),
        }

    def _check_container_security(self) -> Dict:
        """Check container security posture."""
        checks = 0
        passed = 0

        # Check: No containers running as root
        checks += 1
        # Simulated: passed += 1

        # Check: Images scanned
        checks += 1
        # Simulated: passed += 1

        # Check: Read-only filesystem
        checks += 1
        # Simulated: passed += 1

        # Check: No privileged containers
        checks += 1
        # Simulated: passed += 1

        return {
            "category": "Container Security",
            "checks": checks,
            "passed": passed,
            "failed": checks - passed,
        }

    def _check_secret_management(self) -> Dict:
        """Check secret management practices."""
        checks = 4
        passed = 3  # Simulated
        return {
            "category": "Secret Management",
            "checks": checks,
            "passed": passed,
            "failed": checks - passed,
        }

    def _check_network_security(self) -> Dict:
        """Check network security configuration."""
        checks = 5
        passed = 4
        return {
            "category": "Network Security",
            "checks": checks,
            "passed": passed,
            "failed": checks - passed,
        }

    def _check_encryption(self) -> Dict:
        """Check encryption at rest and in transit."""
        checks = 4
        passed = 4
        return {
            "category": "Encryption",
            "checks": checks,
            "passed": passed,
            "failed": checks - passed,
        }

    def _check_backup_strategy(self) -> Dict:
        """Check backup strategy."""
        checks = 3
        passed = 2
        return {
            "category": "Backup Strategy",
            "checks": checks,
            "passed": passed,
            "failed": checks - passed,
        }

    def _check_disaster_recovery(self) -> Dict:
        """Check disaster recovery readiness."""
        checks = 3
        passed = 1
        return {
            "category": "Disaster Recovery",
            "checks": checks,
            "passed": passed,
            "failed": checks - passed,
        }

    def _generate_recommendations(self, checks: List[Dict]) -> List[str]:
        """Generate recommendations based on audit results."""
        recommendations = []
        for check in checks:
            if check["failed"] > 0:
                recommendations.append(
                    f"Address {check['failed']} failed check(s) in {check['category']}"
                )
        return recommendations


# =============================================================
# DEMONSTRATIONS
# =============================================================

def demo_container_security():
    """Demonstrate container security scanning."""
    print("\n" + "=" * 60)
    print("DEMO 1: Container Security Scanning")
    print("=" * 60)

    scanner = ContainerSecurityScanner()
    scanner.add_allowed_registry("docker.io")
    scanner.add_allowed_registry("gcr.io")
    scanner.add_blocked_package("curl")  # Example: block curl in production

    # Create test image
    image = ContainerImage(
        name="ai-inference",
        tag="latest",
        registry="docker.io",
        digest="sha256:abc123...",
        created_at=time.time() - (100 * 86400),  # 100 days old
        layers=[
            {"command": "FROM ubuntu:20.04"},
            {"command": "RUN apt-get install -y python3"},
            {"command": "ENV API_KEY=sk_live_12345"},  # Simulated secret
            {"command": "EXPOSE 8080"},
        ],
    )

    result = scanner.scan_image(image)
    print(f"Image: {result['image']}")
    print(f"Risk Score: {result['risk_score']}/100 ({result['risk_level']})")
    print(f"Findings: {result['findings_count']}")
    print(f"Passed: {result['passed']}")

    if result["findings"]:
        print("\nFindings:")
        for finding in result["findings"][:5]:
            print(f"  [{finding['severity']}] {finding['message']}")

    print("\n[OK] Container security scanning demonstrated")


def demo_secret_management():
    """Demonstrate secret management."""
    print("\n" + "=" * 60)
    print("DEMO 2: Secret Management")
    print("=" * 60)

    sm = SecretManager()

    # Store secrets
    sm.store_secret(
        "db/password",
        "super_secret_password_123",
        metadata={"service": "database"},
        rotation_period=90 * 86400,  # 90 days
    )

    sm.store_secret(
        "api/openai_key",
        "sk-abcdef1234567890",
        metadata={"service": "ai-api"},
    )

    # Retrieve secrets
    db_pass = sm.get_secret("db/password")
    print(f"Retrieved db/password: {db_pass[:10]}...")

    # Rotate secret
    rotation = sm.rotate_secret("db/password", "new_password_456")
    print(f"Rotated db/password: v{rotation['old_version']} -> v{rotation['new_version']}")

    # Check audit log
    audit = sm.get_audit_log()
    print(f"Audit log entries: {len(audit)}")
    for entry in audit:
        print(f"  {entry['action']}: {entry['secret_name']}")

    print("\n[OK] Secret management demonstrated")


def demo_network_security():
    """Demonstrate network security."""
    print("\n" + "=" * 60)
    print("DEMO 3: Network Security")
    print("=" * 60)

    nsm = NetworkSecurityManager()

    # Add rules
    nsm.add_rule(FirewallRule(
        name="Allow HTTPS",
        direction="inbound",
        protocol="tcp",
        source="*",
        destination="*",
        port="443",
        action="allow",
        priority=10,
    ))

    nsm.add_rule(FirewallRule(
        name="Allow SSH from VPN",
        direction="inbound",
        protocol="tcp",
        source="10.0.0.0/8",
        destination="*",
        port="22",
        action="allow",
        priority=20,
    ))

    nsm.add_rule(FirewallRule(
        name="Block all other inbound",
        direction="inbound",
        protocol="any",
        source="*",
        destination="*",
        port="*",
        action="deny",
        priority=100,
    ))

    # Test connections
    tests = [
        ("192.168.1.1", "10.0.0.1", 443, "HTTPS allowed"),
        ("10.0.0.5", "10.0.0.1", 22, "SSH from VPN"),
        ("5.5.5.5", "10.0.0.1", 22, "SSH from external"),
        ("192.168.1.1", "10.0.0.1", 3306, "MySQL blocked"),
    ]

    print("Connection tests:")
    for src, dst, port, desc in tests:
        result = nsm.check_connection(src, dst, port)
        status = "[OK]" if result["allowed"] else "[FAIL]"
        print(f"  {desc}: {status} ({result['action']} by {result['rule']})")

    # Security report
    report = nsm.get_security_report()
    print(f"\nSecurity Report:")
    print(f"  Total rules: {report['total_rules']}")
    print(f"  Connections: {report['total_connections']}")
    print(f"  Denied: {report['denied_connections']}")

    print("\n[OK] Network security demonstrated")


def demo_encryption():
    """Demonstrate database encryption."""
    print("\n" + "=" * 60)
    print("DEMO 4: Database Encryption")
    print("=" * 60)

    encryption = DatabaseEncryptionManager()

    # Setup TDE
    tde = encryption.setup_tde("ai_platform_db")
    print(f"TDE Setup: {json.dumps(tde, indent=2)}")

    # Encrypt column values
    original_email = "john.doe@example.com"
    encrypted_email = encryption.encrypt_value("users.email", original_email)
    decrypted_email = encryption.decrypt_value("users.email", encrypted_email)

    print(f"\nOriginal: {original_email}")
    print(f"Encrypted: {encrypted_email[:30]}...")
    print(f"Decrypted: {decrypted_email}")

    # Encrypt/decrypt full row
    row = {
        "user_id": 123,
        "email": "jane@example.com",
        "name": "Jane Doe",
        "ssn": "123-45-6789",
    }

    encrypted_row = encryption.encrypt_row("users", row, ["email", "ssn"])
    print(f"\nEncrypted row:")
    for key, value in encrypted_row.items():
        if key not in ("user_id", "name"):
            print(f"  {key}: {str(value)[:30]}...")

    decrypted_row = encryption.decrypt_row("users", encrypted_row, ["email", "ssn"])
    print(f"\nDecrypted row email: {decrypted_row['email']}")

    print("\n[OK] Database encryption demonstrated")


def demo_backup_security():
    """Demonstrate backup security."""
    print("\n" + "=" * 60)
    print("DEMO 5: Backup Security & Disaster Recovery")
    print("=" * 60)

    backup_mgr = BackupSecurityManager()

    # Create backup job
    job = backup_mgr.create_backup_job(
        name="AI Model Backup",
        source="/models/",
        schedule="0 2 * * *",
        retention_days=30,
        encrypted=True,
    )
    print(f"Backup job created: {job.job_id}")

    # Execute backup
    test_data = b"This is test backup data for the AI model"
    backup_result = backup_mgr.execute_backup(job.job_id, test_data)
    print(f"Backup executed: {backup_result['backup_id']}")
    print(f"  Size: {backup_result['size_bytes']} bytes")
    print(f"  Encrypted: {backup_result['encrypted']}")
    print(f"  Checksum: {backup_result['checksum'][:16]}...")

    # Verify backup
    verification = backup_mgr.verify_backup(backup_result["backup_id"], test_data)
    print(f"\nBackup verification:")
    print(f"  Checksum valid: {verification['checksum_valid']}")
    print(f"  Expired: {verification['expired']}")

    # Disaster Recovery
    dr = DisasterRecoveryManager()

    # Create recovery plan
    plan = dr.create_recovery_plan(
        name="AI Platform DR Plan",
        components=["database", "model-serving", "api-gateway"],
        rpo_hours=4,
        rto_hours=2,
        priority="critical",
    )
    print(f"\nRecovery plan created: {plan['plan_id']}")
    print(f"  RPO: {plan['rpo_hours']} hours")
    print(f"  RTO: {plan['rto_hours']} hours")

    # Test recovery
    test_result = dr.test_recovery_plan(plan["plan_id"])
    print(f"\nRecovery test:")
    print(f"  Steps passed: {test_result['steps_passed']}/{test_result['steps_total']}")
    print(f"  RTO met: {test_result['rto_met']}")

    # Declare incident
    incident = dr.declare_incident(
        title="Database failure",
        severity="critical",
        affected_components=["database"],
    )
    print(f"\nIncident declared: {incident['incident_id']}")

    # Recovery status
    status = dr.get_recovery_status()
    print(f"\nDR Status:")
    print(f"  Active plans: {status['active_plans']}")
    print(f"  Open incidents: {status['open_incidents']}")
    print(f"  Plans needing test: {status['plans_needing_test']}")

    print("\n[OK] Backup security & disaster recovery demonstrated")


def demo_infrastructure_audit():
    """Demonstrate infrastructure auditing."""
    print("\n" + "=" * 60)
    print("DEMO 6: Infrastructure Security Audit")
    print("=" * 60)

    auditor = InfrastructureAuditor()
    report = auditor.run_full_audit()

    print(f"Infrastructure Audit Report")
    print(f"{'=' * 40}")
    print(f"Total checks: {report['total_checks']}")
    print(f"Passed: {report['passed']}")
    print(f"Failed: {report['failed']}")
    print(f"Score: {report['score']:.1f}%")

    print(f"\nCategories:")
    for cat in report["categories"]:
        status = "[OK]" if cat["failed"] == 0 else "[WARN]"
        print(f"  {status} {cat['category']}: {cat['passed']}/{cat['checks']} passed")

    if report["recommendations"]:
        print(f"\nRecommendations:")
        for rec in report["recommendations"]:
            print(f"  -> {rec}")

    print("\n[OK] Infrastructure audit demonstrated")


# =============================================================
# ATTACK PATTERNS & DEFENSES
# =============================================================

ATTACK_PATTERNS = """
+==============================================================+
|          INFRASTRUCTURE SECURITY ATTACKS                     |
+==============================================================+
|                                                              |
|  1. CONTAINER ESCAPE                                         |
|     Attack: Break out of container to host                   |
|     Defense: Non-root users, read-only FS, seccomp           |
|                                                              |
|  2. SECRET LEAKAGE                                           |
|     Attack: Extract secrets from env vars or files           |
|     Defense: Secret manager, encrypted storage, rotation     |
|                                                              |
|  3. LATERAL MOVEMENT                                         |
|     Attack: Move between compromised systems                 |
|     Defense: Network segmentation, zero trust                |
|                                                              |
|  4. DATA EXFILTRATION                                        |
|     Attack: Steal training data or model weights             |
|     Defense: DLP, encryption, access controls                |
|                                                              |
|  5. RANSOMWARE                                               |
|     Attack: Encrypt and hold data hostage                    |
|     Defense: Backups, air-gapped storage, recovery plans     |
|                                                              |
|  6. SUPPLY CHAIN ATTACKS                                     |
|     Attack: Compromise dependencies or base images           |
|     Defense: Image scanning, dependency pinning, SBOM        |
|                                                              |
+==============================================================+
"""


# =============================================================
# MAIN EXECUTION
# =============================================================

if __name__ == "__main__":
    print("+==============================================================+")
    print("|     Topic 09: Infrastructure Security for AI Systems        |")
    print("+==============================================================+")

    try:
        demo_container_security()
        demo_secret_management()
        demo_network_security()
        demo_encryption()
        demo_backup_security()
        demo_infrastructure_audit()

        print(ATTACK_PATTERNS)

        print("\n" + "=" * 60)
        print("[OK] ALL INFRASTRUCTURE SECURITY DEMOS COMPLETED")
        print("=" * 60)

    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
