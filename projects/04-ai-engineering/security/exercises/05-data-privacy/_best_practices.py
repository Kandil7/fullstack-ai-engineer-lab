"""
05 Data Privacy: Best Practices
"""

from ._types import *

BEST_PRACTICES = {
    "Data Collection": [
        "Collect only data that is strictly necessary (data minimization)",
        "Obtain explicit consent before collecting personal data",
        "Clearly communicate the purpose of data collection",
        "Provide easy mechanisms for users to withdraw consent",
        "Log all data collection operations for audit purposes",
    ],
    "Data Storage": [
        "Encrypt personal data at rest and in transit",
        "Implement access controls based on role and need-to-know",
        "Set retention policies and automatically purge expired data",
        "Use pseudonymization where possible to reduce risk",
        "Maintain separate storage for PII and non-PII data",
    ],
    "Data Processing": [
        "Process data only for stated purposes (purpose limitation)",
        "Apply differential privacy for aggregate statistics",
        "Use anonymization techniques for non-essential processing",
        "Implement privacy-preserving machine learning techniques",
        "Audit all data processing operations",
    ],
    "Data Sharing": [
        "Never share raw personal data without explicit consent",
        "Use anonymization before sharing data with third parties",
        "Implement data processing agreements with partners",
        "Provide data portability in machine-readable formats",
        "Track all data sharing operations for compliance",
    ],
    "Compliance": [
        "Implement right to erasure (forgetting) mechanisms",
        "Maintain records of processing activities (GDPR Article 30)",
        "Conduct data protection impact assessments for high-risk processing",
        "Appoint a data protection officer if required",
        "Regularly audit privacy practices and update policies",
    ],
}


def print_best_practices():
    """Print the best practices reference."""
    print("\n" + "=" * 72)
    print("DATA PRIVACY BEST PRACTICES")
    print("=" * 72)

    for category, practices in BEST_PRACTICES.items():
        print(f"\n  {category}:")
        for i, practice in enumerate(practices, 1):
            print(f"    {i}. {practice}")


# =============================================================================
# Main Entry Point
# =============================================================================
