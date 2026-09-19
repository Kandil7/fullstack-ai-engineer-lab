"""
08 Model Security: Demos
"""

from ._types import *

def demo_poisoning_detection():
    """Demonstrate data poisoning detection."""
    print("\n" + "=" * 60)
    print("DEMO 1: Training Data Poisoning Detection")
    print("=" * 60)

    detector = DataPoisoningDetector()

    # Create clean dataset
    clean_data = [
        DataPoint(
            features=[random.gauss(0, 1) for _ in range(5)],
            label=i % 2,
            source="trusted",
        )
        for i in range(100)
    ]

    # Inject poisoned data
    poisoned_data = clean_data.copy()
    for _ in range(10):
        poisoned_data.append(
            DataPoint(
                features=[100 + random.gauss(0, 0.1) for _ in range(5)],  # Outliers
                label=0,  # Wrong label
                source="unknown_attacker",
            )
        )

    print("Analyzing clean dataset...")
    clean_result = detector.analyze_dataset(clean_data)
    print(f"  Risk score: {clean_result['risk_score']:.3f}")
    print(f"  Clean: {clean_result['clean']}")
    print(f"  Issues: {len(clean_result['issues'])}")

    print("\nAnalyzing poisoned dataset...")
    poisoned_result = detector.analyze_dataset(poisoned_data)
    print(f"  Risk score: {poisoned_result['risk_score']:.3f}")
    print(f"  Clean: {poisoned_result['clean']}")
    print(f"  Issues: {len(poisoned_result['issues'])}")
    print(f"  Suspicious samples: {poisoned_result['suspicious_count']}")

    if poisoned_result["issues"]:
        print("\n  Sample issues:")
        for issue in poisoned_result["issues"][:3]:
            print(f"    - [{issue['severity']}] {issue['message']}")

    if poisoned_result["recommendations"]:
        print("\n  Recommendations:")
        for rec in poisoned_result["recommendations"]:
            print(f"    -> {rec}")

    print("\n[OK] Poisoning detection demonstrated")


def demo_adversarial_detection():
    """Demonstrate adversarial attack detection."""
    print("\n" + "=" * 60)
    print("DEMO 2: Adversarial Attack Detection & Robustness")
    print("=" * 60)

    # Simple model function
    def simple_model(features):
        """Simple linear model for demonstration."""
        weights = [0.5, -0.3, 0.8, 0.1, -0.2]
        return sum(f * w for f, w in zip(features[:5], weights)) > 0

    detector = AdversarialDetector(sensitivity=0.4)

    # Update baseline with clean data
    for _ in range(100):
        clean_input = [random.gauss(0, 1) for _ in range(5)]
        pred = simple_model(clean_input)
        detector.update_baseline(clean_input, pred)

    # Test with clean input
    clean_input = [0.1, -0.2, 0.3, 0.0, -0.1]
    result = detector.detect_adversarial(clean_input, simple_model)
    print(
        f"Clean input: adversarial={result['is_adversarial']}, confidence={result['confidence']:.3f}"
    )

    # Test with adversarial input
    adversarial_input = [100, -200, 150, 50, -100]
    result = detector.detect_adversarial(adversarial_input, simple_model)
    print(
        f"Adversarial input: adversarial={result['is_adversarial']}, confidence={result['confidence']:.3f}"
    )
    if result["reasons"]:
        for reason in result["reasons"]:
            print(f"  Reason: {reason}")

    # Robustness testing
    print("\nRobustness Evaluation:")
    tester = AdversarialRobustnessTester()
    test_data = [
        ([random.gauss(0, 1) for _ in range(5)], random.randint(0, 1))
        for _ in range(50)
    ]

    robustness = tester.evaluate_robustness(test_data, simple_model, epsilon=0.1)
    print(f"  Clean accuracy: {robustness['clean_accuracy']:.1%}")
    print(f"  FGSM accuracy: {robustness['fgsm_accuracy']:.1%}")
    print(f"  PGD accuracy: {robustness['pgd_accuracy']:.1%}")
    print(f"  Robustness score: {robustness['robustness_score']:.3f}")

    print("\n[OK] Adversarial detection demonstrated")


def demo_watermarking():
    """Demonstrate model watermarking."""
    print("\n" + "=" * 60)
    print("DEMO 3: Model Watermarking")
    print("=" * 60)

    watermarker = ModelWatermarker()

    # Create watermark
    watermark_info = watermarker.create_watermark(
        model_id="gpt-custom-v1",
        owner_id="company-xyz",
    )
    print(f"Watermark created:")
    print(f"  Model ID: {watermark_info['model_id']}")
    print(f"  Watermark ID: {watermark_info['watermark_id']}")
    print(f"  Triggers embedded: {watermark_info['triggers_embedded']}")

    # Simulate model with watermark
    def watermarked_model(features):
        """Model that responds to trigger patterns."""
        # Simple deterministic output based on input
        return hash(tuple(features)) % 10 / 10.0

    # Verify watermark
    verification = watermarker.verify_watermark("gpt-custom-v1", watermarked_model)
    print(f"\nWatermark verification:")
    print(f"  Watermarked: {verification['watermarked']}")
    print(f"  Match ratio: {verification['match_ratio']:.1%}")
    print(f"  Confidence: {verification['confidence']:.3f}")

    print("\n[OK] Watermarking demonstrated")


def demo_backdoor_detection():
    """Demonstrate backdoor detection."""
    print("\n" + "=" * 60)
    print("DEMO 4: Backdoor Detection")
    print("=" * 60)

    detector = BackdoorDetector()

    # Simulate clean model
    def clean_model(features):
        """Simple model without backdoor."""
        return sum(features) > 0

    # Test clean model
    test_inputs = [[random.gauss(0, 1) for _ in range(5)] for _ in range(100)]
    expected_labels = [1 if sum(f) > 0 else 0 for f in test_inputs]

    result = detector.analyze_model_behavior(clean_model, test_inputs, expected_labels)
    print(f"Clean model analysis:")
    print(f"  Backdoor suspected: {result['backdoor_suspected']}")
    print(f"  Anomaly count: {result['anomaly_count']}")
    print(f"  Distribution shift: {result['distribution_shift']}")

    # Activation clustering
    clean_acts = [[random.gauss(0, 1) for _ in range(10)] for _ in range(50)]
    suspect_acts = [[random.gauss(5, 1) for _ in range(10)] for _ in range(50)]

    cluster_result = detector.activation_clustering_analysis(clean_acts, suspect_acts)
    print(f"\nActivation clustering:")
    print(f"  Separation detected: {cluster_result['separation_detected']}")
    print(f"  Separation ratio: {cluster_result['separation_ratio']}")

    print("\n[OK] Backdoor detection demonstrated")


def demo_secure_serving():
    """Demonstrate secure model serving."""
    print("\n" + "=" * 60)
    print("DEMO 5: Secure Model Serving")
    print("=" * 60)

    server = SecureModelServer()

    # Register model
    def dummy_model(features):
        """Dummy prediction model."""
        return sum(f * 0.1 for f in features)

    server.register_model("sentiment-v1", dummy_model, sensitivity="high")

    # Normal request
    result = server.predict("sentiment-v1", [0.5, -0.3, 0.8], user_id="user1")
    print(f"Normal prediction: {result.get('prediction', result.get('error'))}")

    # Adversarial request
    result = server.predict("sentiment-v1", [1000, -2000, 3000], user_id="attacker")
    print(f"Adversarial request: {result.get('error', 'passed')}")

    # Rate limit test
    for i in range(55):
        result = server.predict("sentiment-v1", [0.1, 0.2, 0.3], user_id="spammer")
    print(f"After 55 rapid requests: {result.get('error', 'passed')}")

    print("\n[OK] Secure model serving demonstrated")


# =============================================================
# ATTACK PATTERNS & DEFENSES
# =============================================================

