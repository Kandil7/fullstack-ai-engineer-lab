"""
07 Api Security: Demos
"""

from ._types import *

def demo_rate_limiting():
    """Demonstrate rate limiting."""
    print("\n" + "=" * 60)
    print("DEMO 1: Rate Limiting")
    print("=" * 60)

    # Sliding window rate limiter
    limiter = SlidingWindowRateLimiter(
        requests_per_minute=5,
        requests_per_hour=100,
        burst_limit=3,
        burst_window=1,
    )

    print("Testing sliding window limiter (5 RPM, 3 burst):")
    for i in range(7):
        result = limiter.is_allowed("client_1")
        status = "[OK]" if result["allowed"] else "[FAIL]"
        print(
            f"  Request {i + 1}: {status} remaining_minute={result['remaining'].get('minute', 'N/A')}"
        )

    # Token bucket
    print("\nToken bucket limiter (capacity=5, refill=2/s):")
    bucket = TokenBucketRateLimiter(capacity=5, refill_rate=2)
    for i in range(8):
        result = bucket.is_allowed("client_2")
        status = "[OK]" if result["allowed"] else "[FAIL]"
        remaining = result["remaining"] if result["allowed"] else 0
        print(f"  Request {i + 1}: {status} tokens_remaining={remaining}")

    print("\n[OK] Rate limiting demonstrated")


def demo_cors():
    """Demonstrate CORS configuration."""
    print("\n" + "=" * 60)
    print("DEMO 2: CORS Configuration")
    print("=" * 60)

    cors = CORSPolicy()
    cors.allow_origin("https://app.ai-platform.com")
    cors.allow_origin("https://admin.ai-platform.com")
    cors.set_allowed_methods(["GET", "POST", "PUT", "DELETE"])
    cors.set_allowed_headers(["Authorization", "Content-Type", "X-API-Key"])

    # Test allowed origin
    result = cors.check_origin("https://app.ai-platform.com")
    print(
        f"Origin https://app.ai-platform.com: {'[OK]' if result['allowed'] else '[FAIL]'}"
    )

    # Test disallowed origin
    result = cors.check_origin("https://evil-site.com")
    print(f"Origin https://evil-site.com: {'[OK]' if result['allowed'] else '[FAIL]'}")

    # Test no origin (server-to-server)
    result = cors.check_origin(None)
    print(f"No origin (server-to-server): {'[OK]' if result['allowed'] else '[FAIL]'}")

    if "headers" in result and result["headers"]:
        print(f"CORS Headers: {json.dumps(result['headers'], indent=2)}")

    print("\n[OK] CORS configuration demonstrated")


def demo_request_validation():
    """Demonstrate request validation."""
    print("\n" + "=" * 60)
    print("DEMO 3: Request Validation")
    print("=" * 60)

    validator = RequestValidator()

    # Test normal request
    result = validator.validate_request(
        {
            "method": "POST",
            "path": "/api/v1/models",
            "headers": {"Content-Type": "application/json"},
            "body": '{"name": "my-model"}',
        }
    )
    print(f"Normal request: {'[OK] Valid' if result['valid'] else '[FAIL] Invalid'}")
    if result["errors"]:
        print(f"  Errors: {result['errors']}")

    # Test SQL injection
    result = validator.validate_request(
        {
            "method": "GET",
            "path": "/api/v1/models?id=1' OR '1'='1",
            "headers": {},
        }
    )
    print(
        f"SQL injection attempt: {'[OK] Valid' if result['valid'] else '[FAIL] Blocked'}"
    )

    # Test XSS
    result = validator.validate_request(
        {
            "method": "POST",
            "path": "/api/v1/chat",
            "headers": {"Content-Type": "application/json"},
            "body": '<script>alert("xss")</script>',
        }
    )
    print(f"XSS attempt: {'[OK] Valid' if result['valid'] else '[FAIL] Blocked'}")

    # Test path traversal
    result = validator.validate_request(
        {
            "method": "GET",
            "path": "/api/v1/files?path=../../etc/passwd",
            "headers": {},
        }
    )
    print(
        f"Path traversal attempt: {'[OK] Valid' if result['valid'] else '[FAIL] Blocked'}"
    )

    # JSON schema validation
    print("\nJSON Body Validation:")
    schema = {
        "model_name": {
            "type": "string",
            "required": True,
            "max_length": 100,
            "pattern": r"^[a-zA-Z0-9_-]+$",
        },
        "temperature": {"type": "number", "required": False, "min": 0.0, "max": 2.0},
        "max_tokens": {"type": "integer", "required": False, "min": 1, "max": 4096},
    }

    valid_body = {"model_name": "gpt-4", "temperature": 0.7, "max_tokens": 1000}
    result = validator.validate_json_body(valid_body, schema)
    print(f"Valid body: {'[OK]' if result['valid'] else '[FAIL]'} {result['errors']}")

    invalid_body = {"model_name": "gpt/4", "temperature": 5.0}
    result = validator.validate_json_body(invalid_body, schema)
    print(f"Invalid body: {'[OK]' if result['valid'] else '[FAIL]'} {result['errors']}")

    print("\n[OK] Request validation demonstrated")


def demo_response_sanitization():
    """Demonstrate response sanitization."""
    print("\n" + "=" * 60)
    print("DEMO 4: Response Sanitization")
    print("=" * 60)

    sanitizer = ResponseSanitizer()

    # Test data masking
    sensitive_data = {
        "user_id": "12345",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1-555-123-4567",
        "credit_card": "4111-1111-1111-1234",
        "password": "super_secret_123",
        "api_key": "sk_live_abcdef123456",
        "model_output": "The answer is 42",
    }

    sanitized = sanitizer.sanitize_response(sensitive_data)
    print("Original vs Sanitized:")
    for key in sensitive_data:
        original = sensitive_data[key]
        masked = sanitized.get(key, "REMOVED")
        print(f"  {key}: {original} -> {masked}")

    # Test error sanitization
    print("\nError Sanitization:")
    db_error = Exception("Connection refused to database at 10.0.0.5:5432")
    safe_error = sanitizer.sanitize_error(db_error, include_details=False)
    print(f"  DB error (safe): {json.dumps(safe_error, indent=4)}")

    validation_error = Exception("Invalid email format")
    safe_error = sanitizer.sanitize_error(validation_error, include_details=True)
    print(f"  Validation error: {json.dumps(safe_error, indent=4)}")

    print("\n[OK] Response sanitization demonstrated")


def demo_webhook_verification():
    """Demonstrate webhook verification."""
    print("\n" + "=" * 60)
    print("DEMO 5: Webhook Verification")
    print("=" * 60)

    secret = secrets.token_bytes(32)
    verifier = WebhookVerifier(secret, tolerance=300)

    # Generate signature
    payload = json.dumps({"event": "model.updated", "model_id": "12345"}).encode()
    timestamp = int(time.time())
    signature = verifier.generate_signature(payload, timestamp)
    print(f"Generated signature: {signature[:50]}...")

    # Verify valid signature
    result = verifier.verify_signature(payload, signature)
    print(f"Valid webhook: {'[OK]' if result['valid'] else '[FAIL]'}")

    # Verify tampered payload
    tampered_payload = payload + b"tampered"
    result = verifier.verify_signature(tampered_payload, signature)
    print(
        f"Tampered payload: {'[OK]' if result['valid'] else '[FAIL]'} {result.get('error', '')}"
    )

    # Verify replayed webhook
    result = verifier.verify_signature(payload, signature)
    print(
        f"Replayed webhook: {'[OK]' if result['valid'] else '[FAIL]'} {result.get('error', '')}"
    )

    # Request signing
    print("\nRequest Signing:")
    signer = RequestSigner(secret)
    signed_headers = signer.sign_request("POST", "/api/v1/inference", payload)
    print(f"Signed headers: {json.dumps(signed_headers, indent=2)}")

    # Verify signed request
    result = signer.verify_request("POST", "/api/v1/inference", payload, signed_headers)
    print(f"Valid signed request: {'[OK]' if result['valid'] else '[FAIL]'}")

    print("\n[OK] Webhook verification demonstrated")


# =============================================================
# ATTACK PATTERNS & DEFENSES
# =============================================================

