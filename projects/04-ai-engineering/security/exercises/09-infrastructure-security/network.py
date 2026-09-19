"""
09 Infrastructure Security: Network
"""

from ._types import *

@dataclass
class FirewallRule:
    """Represents a firewall rule."""

    name: str
    direction: str  # inbound, outbound
    protocol: str  # tcp, udp, icmp
    source: str  # IP/CIDR or *
    destination: str  # IP/CIDR or *
    port: str  # port or range
    action: str  # allow, deny
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
                if self._ip_matches(source_ip, rule.source) and self._ip_matches(
                    dest_ip, rule.destination
                ):
                    if self._port_matches(dest_port, rule.port):
                        self._log_connection(
                            source_ip, dest_ip, dest_port, rule.action, rule.name
                        )
                        return {
                            "allowed": rule.action == "allow",
                            "rule": rule.name,
                            "action": rule.action,
                        }

            elif rule.direction == "outbound":
                if self._ip_matches(source_ip, rule.source) and self._ip_matches(
                    dest_ip, rule.destination
                ):
                    if self._port_matches(dest_port, rule.port):
                        self._log_connection(
                            source_ip, dest_ip, dest_port, rule.action, rule.name
                        )
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
        self._connection_log.append(
            {
                "timestamp": time.time(),
                "source": src,
                "destination": dst,
                "port": port,
                "action": action,
                "rule": rule,
            }
        )

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


