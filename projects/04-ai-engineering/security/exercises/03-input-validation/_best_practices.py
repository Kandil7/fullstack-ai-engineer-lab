"""
03 Input Validation: Best Practices
"""

from ._types import *

BEST_PRACTICES = {
    "General Input Validation": [
        "Always validate input on the server side (never trust client-side validation alone)",
        "Use allowlists rather than blocklists when possible",
        "Validate input length, type, format, and range",
        "Normalize input before validation (e.g., decode URL encoding)",
        "Log validation failures for security monitoring",
    ],
    "SQL Injection Prevention": [
        "Always use parameterized queries or ORM methods",
        "Never concatenate user input into SQL strings",
        "Apply principle of least privilege to database accounts",
        "Use stored procedures for complex operations",
        "Regularly audit database permissions",
    ],
    "XSS Prevention": [
        "HTML-encode all user-provided content before rendering",
        "Use Content Security Policy (CSP) headers",
        "Avoid innerHTML; use textContent or safe DOM methods",
        "Sanitize rich text input with a whitelist of allowed tags",
        "Validate and sanitize URLs before using in href/src attributes",
    ],
    "Command Injection Prevention": [
        "Never pass user input directly to shell commands",
        "Use shlex.quote() or subprocess.run() with argument lists",
        "Implement command allowlists for AI tool-use scenarios",
        "Run commands with minimal privileges",
        "Audit and log all executed commands",
    ],
}


def print_best_practices():
    """Print the best practices reference."""
    print("\n" + "=" * 72)
    print("INPUT VALIDATION BEST PRACTICES")
    print("=" * 72)

    for category, practices in BEST_PRACTICES.items():
        print(f"\n  {category}:")
        for i, practice in enumerate(practices, 1):
            print(f"    {i}. {practice}")


# =============================================================================
# Main Entry Point
# =============================================================================
