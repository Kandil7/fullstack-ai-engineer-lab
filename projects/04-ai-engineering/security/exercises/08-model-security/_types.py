"""
=============================================================
Topic 08: AI Model Security
=============================================================

Security Level: ########## Critical

Protect your ML models from attacks, theft, and manipulation.
This exercise covers model poisoning detection, adversarial
attacks, model theft prevention, watermarking, and secure
model serving.

Learning Objectives:
- Detect and prevent training data poisoning
- Implement adversarial robustness testing
- Protect models from extraction attacks
- Apply model watermarking techniques
- Secure model serving infrastructure

Prerequisites:
- Basic ML knowledge (training, inference)
- Understanding of neural network architectures
- Familiarity with Python/NumPy
=============================================================
"""

import hashlib
import hmac
import json
import math
import random
import secrets
import struct
import time
from collections import defaultdict, Counter
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
import base64
import re


@dataclass
class DataPoint:
    """A single training data point with metadata."""

    features: List[float]
    label: Any
    source: str
    timestamp: float = field(default_factory=time.time)
    checksum: str = ""
    is_suspicious: bool = False

    def __post_init__(self):
        if not self.checksum:
            self.checksum = self._compute_checksum()

    def _compute_checksum(self) -> str:
        """Compute integrity checksum."""
        data = json.dumps(
            {"features": self.features, "label": self.label}, sort_keys=True
        )
        return hashlib.sha256(data.encode()).hexdigest()


class DataPoisoningDetector:
    """
    Detect potential data poisoning in training datasets.

    Techniques:
    - Statistical outlier detection
    - Label consistency checks
    - Source verification
    - Temporal anomaly detection
    - Feature distribution analysis
    """

    def __init__(self, contamination_threshold: float = 0.05):
        self.contamination_threshold = contamination_threshold
        self._baseline_stats: Optional[Dict] = None

    def analyze_dataset(self, data: List[DataPoint]) -> Dict:
        """
        Comprehensive dataset analysis for poisoning detection.

        Returns detailed analysis report.
        """
        if not data:
            return {"clean": True, "issues": [], "suspicious_points": []}

        issues = []
        suspicious = []

        # 1. Statistical outlier detection
        outlier_results = self._detect_statistical_outliers(data)
        issues.extend(outlier_results["issues"])
        suspicious.extend(outlier_results["suspicious_indices"])

        # 2. Label consistency check
        label_results = self._check_label_consistency(data)
        issues.extend(label_results["issues"])

        # 3. Source analysis
        source_results = self._analyze_sources(data)
        issues.extend(source_results["issues"])

        # 4. Temporal analysis
        temporal_results = self._analyze_temporal_patterns(data)
        issues.extend(temporal_results["issues"])

        # 5. Feature distribution analysis
        dist_results = self._analyze_feature_distributions(data)
        issues.extend(dist_results["issues"])

        # Calculate risk score
        risk_score = min(1.0, len(issues) * 0.15 + len(suspicious) * 0.05)

        return {
            "clean": risk_score < self.contamination_threshold,
            "risk_score": risk_score,
            "issues": issues,
            "suspicious_count": len(suspicious),
            "total_samples": len(data),
            "recommendations": self._generate_recommendations(issues),
        }

    def _detect_statistical_outliers(self, data: List[DataPoint]) -> Dict:
        """Detect statistical outliers using Z-score."""
        issues = []
        suspicious = []

        if len(data) < 10:
            return {"issues": [], "suspicious_indices": []}

        # Calculate feature statistics
        all_features = [dp.features for dp in data]
        n_features = len(all_features[0])

        for feat_idx in range(n_features):
            values = [f[feat_idx] for f in all_features]
            mean = sum(values) / len(values)
            variance = sum((v - mean) ** 2 for v in values) / len(values)
            std = math.sqrt(variance) if variance > 0 else 1e-10

            for i, dp in enumerate(data):
                z_score = abs(dp.features[feat_idx] - mean) / std
                if z_score > 3.0:  # 3 standard deviations
                    dp.is_suspicious = True
                    suspicious.append(i)
                    issues.append(
                        {
                            "type": "statistical_outlier",
                            "severity": "medium",
                            "sample_index": i,
                            "feature": feat_idx,
                            "z_score": round(z_score, 2),
                            "message": f"Sample {i} feature {feat_idx} is {z_score:.1f} std devs from mean",
                        }
                    )

        return {"issues": issues, "suspicious_indices": list(set(suspicious))}

    def _check_label_consistency(self, data: List[DataPoint]) -> Dict:
        """Check for label inconsistencies that may indicate poisoning."""
        issues = []

        # Group by feature similarity
        label_groups = defaultdict(list)
        for i, dp in enumerate(data):
            # Simple grouping by rounding features
            key = tuple(round(f, 1) for f in dp.features[:3])
            label_groups[key].append((i, dp.label))

        # Check for mixed labels in similar samples
        for key, group in label_groups.items():
            if len(group) < 2:
                continue

            labels = [label for _, label in group]
            if len(set(str(l) for l in labels)) > 1:
                issues.append(
                    {
                        "type": "label_inconsistency",
                        "severity": "high",
                        "message": f"Similar samples have different labels: {labels}",
                        "sample_indices": [i for i, _ in group],
                    }
                )

        return {"issues": issues}

    def _analyze_sources(self, data: List[DataPoint]) -> Dict:
        """Analyze data sources for potential poisoning."""
        issues = []

        source_counts = Counter(dp.source for dp in data)
        total = len(data)

        for source, count in source_counts.items():
            proportion = count / total

            # Check for single dominant source
            if proportion > 0.8 and len(source_counts) > 1:
                issues.append(
                    {
                        "type": "source_dominance",
                        "severity": "medium",
                        "source": source,
                        "proportion": round(proportion, 3),
                        "message": f"Source '{source}' provides {proportion:.1%} of data",
                    }
                )

            # Check for unknown/untrusted sources
            if source.startswith("unknown") or source.startswith("unverified"):
                issues.append(
                    {
                        "type": "untrusted_source",
                        "severity": "high",
                        "source": source,
                        "count": count,
                        "message": f"Data from untrusted source: '{source}'",
                    }
                )

        return {"issues": issues}

    def _analyze_temporal_patterns(self, data: List[DataPoint]) -> Dict:
        """Detect temporal anomalies in data collection."""
        issues = []

        if len(data) < 5:
            return {"issues": []}

        # Sort by timestamp
        sorted_data = sorted(data, key=lambda dp: dp.timestamp)

        # Check for burst additions
        time_diffs = []
        for i in range(1, len(sorted_data)):
            diff = sorted_data[i].timestamp - sorted_data[i - 1].timestamp
            time_diffs.append(diff)

        if time_diffs:
            mean_diff = sum(time_diffs) / len(time_diffs)
            # Detect bursts (many additions in short time)
            burst_threshold = mean_diff * 0.1 if mean_diff > 0 else 1
            bursts = sum(1 for d in time_diffs if d < burst_threshold)

            if bursts > len(time_diffs) * 0.3:
                issues.append(
                    {
                        "type": "temporal_burst",
                        "severity": "medium",
                        "burst_count": bursts,
                        "message": f"Detected {bursts} rapid data additions (possible injection)",
                    }
                )

        return {"issues": issues}

    def _analyze_feature_distributions(self, data: List[DataPoint]) -> Dict:
        """Analyze feature distributions for anomalies."""
        issues = []

        if len(data) < 20:
            return {"issues": []}

        # Check for bimodal distributions (possible mixed clean/poisoned data)
        all_features = [dp.features for dp in data]
        n_features = len(all_features[0])

        for feat_idx in range(min(n_features, 5)):  # Check first 5 features
            values = sorted([f[feat_idx] for f in all_features])

            # Simple bimodality check: split into halves and compare means
            mid = len(values) // 2
            lower_mean = sum(values[:mid]) / mid if mid > 0 else 0
            upper_mean = (
                sum(values[mid:]) / (len(values) - mid) if len(values) > mid else 0
            )

            mean = sum(values) / len(values)
            if mean != 0:
                separation = abs(upper_mean - lower_mean) / abs(mean)
                if separation > 2.0:
                    issues.append(
                        {
                            "type": "bimodal_distribution",
                            "severity": "medium",
                            "feature": feat_idx,
                            "separation": round(separation, 2),
                            "message": f"Feature {feat_idx} shows bimodal pattern (possible poisoning)",
                        }
                    )

        return {"issues": issues}

    def _generate_recommendations(self, issues: List[Dict]) -> List[str]:
        """Generate recommendations based on detected issues."""
        recommendations = []
        issue_types = {i["type"] for i in issues}

        if "statistical_outlier" in issue_types:
            recommendations.append("Review and potentially remove statistical outliers")
        if "label_inconsistency" in issue_types:
            recommendations.append(
                "Manually verify labels for similar samples with different labels"
            )
        if "source_dominance" in issue_types:
            recommendations.append(
                "Diversify data sources to reduce single-source dependency"
            )
        if "untrusted_source" in issue_types:
            recommendations.append("Verify data from untrusted sources before training")
        if "temporal_burst" in issue_types:
            recommendations.append(
                "Investigate rapid data additions for potential injection"
            )
        if "bimodal_distribution" in issue_types:
            recommendations.append(
                "Investigate bimodal feature distributions for mixed data"
            )

        return recommendations


# =============================================================
# SECTION 2: Adversarial Attack Detection & Defense
# =============================================================
