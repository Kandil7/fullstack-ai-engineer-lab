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
            findings.append(
                {
                    "severity": "critical",
                    "category": "registry",
                    "message": f"Image from unapproved registry: {image.registry}",
                }
            )
            risk_score += 30

        # 2. Check for 'latest' tag
        if image.tag == "latest":
            findings.append(
                {
                    "severity": "high",
                    "category": "tag",
                    "message": "Using 'latest' tag is unpredictable and insecure",
                }
            )
            risk_score += 20

        # 3. Check image age
        age_days = (time.time() - image.created_at) / 86400
        if age_days > 90:
            findings.append(
                {
                    "severity": "medium",
                    "category": "age",
                    "message": f"Image is {int(age_days)} days old (may have unpatched vulnerabilities)",
                }
            )
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
                    findings.append(
                        {
                            "severity": "critical",
                            "category": "secrets",
                            "message": f"Potential secret found in layer {i}",
                            "layer_index": i,
                        }
                    )
                    risk_score += 40
                    break

        # 5. Check for root user
        has_user_instruction = False
        for layer in image.layers:
            if layer.get("command", "").startswith("USER "):
                has_user_instruction = True
                if "root" in layer.get("command", ""):
                    findings.append(
                        {
                            "severity": "high",
                            "category": "privilege",
                            "message": "Container runs as root",
                        }
                    )
                    risk_score += 25
                break

        if not has_user_instruction:
            findings.append(
                {
                    "severity": "high",
                    "category": "privilege",
                    "message": "No USER instruction found (default is root)",
                }
            )
            risk_score += 25

        # 6. Check for blocked packages
        for layer in image.layers:
            cmd = layer.get("command", "")
            for package in self._blocked_packages:
                if package in cmd:
                    findings.append(
                        {
                            "severity": "high",
                            "category": "packages",
                            "message": f"Blocked package found: {package}",
                        }
                    )
                    risk_score += 20

        # 7. Check for health check
        has_healthcheck = any(
            "HEALTHCHECK" in layer.get("command", "") for layer in image.layers
        )
        if not has_healthcheck:
            findings.append(
                {
                    "severity": "low",
                    "category": "reliability",
                    "message": "No HEALTHCHECK instruction found",
                }
            )
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

    def _log_event(
        self, container_id: str, action: Dict, result: str, policy: Optional[Dict]
    ):
        """Log security event."""
        self._events.append(
            {
                "timestamp": time.time(),
                "container_id": container_id,
                "action": action,
                "result": result,
                "policy": policy.get("name") if policy else None,
            }
        )


# =============================================================
# SECTION 2: Secret Management
# =============================================================
