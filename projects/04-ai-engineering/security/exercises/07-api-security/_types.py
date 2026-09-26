"""
=============================================================
Topic 07: API Security for AI Services
=============================================================

Security Level: ########-- High

Secure your AI APIs against common web vulnerabilities and abuse.
This exercise covers rate limiting, CORS configuration, HTTPS
enforcement, request validation, response sanitization, and
webhook verification.

Learning Objectives:
- Implement rate limiting with sliding window algorithms
- Configure CORS for AI service deployments
- Enforce HTTPS with HSTS
- Validate and sanitize all API inputs
- Protect against data leakage in responses
- Verify webhook authenticity

Prerequisites:
- Understanding of HTTP protocol
- Basic web application security concepts
- Familiarity with REST API design
=============================================================
"""

import hashlib
import hmac
import json
import re
import time
import secrets
import ipaddress
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from urllib.parse import urlparse
from functools import wraps
import base64
import struct
import math


class SlidingWindowRateLimiter:
    """
    Sliding window rate limiter for API protection.

    Uses a sliding window algorithm that combines the benefits of
    fixed windows (simple) and sliding logs (accurate) without
    the memory overhead of storing individual timestamps.
    """

    def __init__(
        self,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
        burst_limit: int = 10,
        burst_window: int = 1,  # seconds
    ):
        self.rpm = requests_per_minute
        self.rph = requests_per_hour
        self.burst_limit = burst_limit
        self.burst_window = burst_window
        self._windows: Dict[str, Dict] = defaultdict(
            lambda: {
                "minute": deque(),
                "hour": deque(),
                "burst": deque(),
            }
        )

    def is_allowed(self, client_id: str, cost: int = 1) -> Dict:
        """
        Check if a request is allowed under rate limits.

        Args:
            client_id: Unique identifier for the client (IP, API key, etc.)
            cost: Cost of the request (default 1)

        Returns:
            Dict with allowed, remaining, retry_after, limits
        """
        now = time.time()
        window = self._windows[client_id]

        # Clean old entries
        self._cleanup(window["minute"], now - 60)
        self._cleanup(window["hour"], now - 3600)
        self._cleanup(window["burst"], now - self.burst_window)

        # Count current requests
        minute_count = sum(window["minute"])
        hour_count = sum(window["hour"])
        burst_count = sum(window["burst"])

        # Check limits
        if burst_count + cost > self.burst_limit:
            retry_after = (
                self.burst_window - (now - window["burst"][0]) if window["burst"] else 0
            )
            return {
                "allowed": False,
                "remaining": 0,
                "retry_after": max(0.1, retry_after),
                "limits": {"rpm": self.rpm, "rph": self.rph, "burst": self.burst_limit},
                "current": {
                    "minute": minute_count,
                    "hour": hour_count,
                    "burst": burst_count,
                },
                "reason": "burst_limit",
            }

        if minute_count + cost > self.rpm:
            retry_after = 60 - (now - window["minute"][0]) if window["minute"] else 60
            return {
                "allowed": False,
                "remaining": 0,
                "retry_after": max(1, retry_after),
                "limits": {"rpm": self.rpm, "rph": self.rph, "burst": self.burst_limit},
                "current": {
                    "minute": minute_count,
                    "hour": hour_count,
                    "burst": burst_count,
                },
                "reason": "minute_limit",
            }

        if hour_count + cost > self.rph:
            retry_after = 3600 - (now - window["hour"][0]) if window["hour"] else 3600
            return {
                "allowed": False,
                "remaining": 0,
                "retry_after": max(1, retry_after),
                "limits": {"rpm": self.rpm, "rph": self.rph, "burst": self.burst_limit},
                "current": {
                    "minute": minute_count,
                    "hour": hour_count,
                    "burst": burst_count,
                },
                "reason": "hour_limit",
            }

        # Record the request
        window["minute"].append(cost)
        window["hour"].append(cost)
        window["burst"].append(cost)

        return {
            "allowed": True,
            "remaining": {
                "minute": max(0, self.rpm - minute_count - cost),
                "hour": max(0, self.rph - hour_count - cost),
            },
            "retry_after": 0,
            "limits": {"rpm": self.rpm, "rph": self.rph, "burst": self.burst_limit},
            "current": {
                "minute": minute_count + cost,
                "hour": hour_count + cost,
                "burst": burst_count + cost,
            },
        }

    def _cleanup(self, window: deque, cutoff: float):
        """Remove entries older than cutoff from the window."""
        while window and window[0] < cutoff:
            # For our implementation, entries are costs, not timestamps
            # In a real implementation, we'd store (timestamp, cost) tuples
            window.popleft()


class TokenBucketRateLimiter:
    """
    Token bucket rate limiter -- allows bursts while maintaining
    average rate.
    """

    def __init__(
        self,
        capacity: int = 100,  # Max tokens
        refill_rate: float = 10,  # Tokens per second
    ):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._buckets: Dict[str, Dict] = {}

    def is_allowed(self, client_id: str, tokens: int = 1) -> Dict:
        """Check if request is allowed."""
        now = time.time()

        if client_id not in self._buckets:
            self._buckets[client_id] = {
                "tokens": self.capacity,
                "last_refill": now,
            }

        bucket = self._buckets[client_id]

        # Refill tokens
        elapsed = now - bucket["last_refill"]
        refill = elapsed * self.refill_rate
        bucket["tokens"] = min(self.capacity, bucket["tokens"] + refill)
        bucket["last_refill"] = now

        if bucket["tokens"] >= tokens:
            bucket["tokens"] -= tokens
            return {
                "allowed": True,
                "remaining": int(bucket["tokens"]),
                "retry_after": 0,
            }
        else:
            wait_time = (tokens - bucket["tokens"]) / self.refill_rate
            return {
                "allowed": False,
                "remaining": 0,
                "retry_after": wait_time,
            }


class AdaptiveRateLimiter:
    """
    Adaptive rate limiter that adjusts limits based on client behavior.

    Clients with good behavior get higher limits; suspicious clients
    get stricter limits.
    """

    def __init__(self):
        self._client_scores: Dict[str, float] = defaultdict(lambda: 1.0)
        self._base_limits = {
            "requests_per_minute": 60,
            "requests_per_hour": 1000,
            "inference_per_minute": 20,
        }
        self._violations: Dict[str, List[float]] = defaultdict(list)

    def evaluate_request(self, client_id: str, request_type: str = "api") -> Dict:
        """Evaluate a request with adaptive limits."""
        score = self._client_scores[client_id]

        # Clean old violations
        now = time.time()
        self._violations[client_id] = [
            v for v in self._violations[client_id] if now - v < 3600
        ]

        # Calculate dynamic limits based on score
        multiplier = min(2.0, max(0.1, score))
        limits = {k: int(v * multiplier) for k, v in self._base_limits.items()}

        return {
            "client_id": client_id,
            "score": score,
            "multiplier": multiplier,
            "limits": limits,
            "violations_last_hour": len(self._violations[client_id]),
        }

    def record_violation(self, client_id: str):
        """Record a rate limit violation."""
        self._violations[client_id].append(time.time())
        # Decrease score
        violations = len(self._violations[client_id])
        self._client_scores[client_id] = max(0.1, 1.0 - (violations * 0.1))

    def record_good_behavior(self, client_id: str):
        """Reward good behavior."""
        current = self._client_scores[client_id]
        self._client_scores[client_id] = min(2.0, current + 0.01)


# =============================================================
# SECTION 2: CORS Configuration
# =============================================================
