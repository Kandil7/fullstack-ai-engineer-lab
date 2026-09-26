"""
01 Prompt Injection: Detector
"""

from ._types import *
from .input_sanitizer import InputSanitizer


@dataclass
class DetectionResult:
    """Result of a prompt injection detection scan."""

    is_suspicious: bool
    confidence: float  # 0.0 - 1.0
    attack_types: list[AttackType]
    details: list[str]
    risk_score: float
    recommended_action: str


class PromptInjectionDetector:
    """
    Multi-layer prompt injection detection engine.

    Combines multiple detection strategies:
      1. Signature-based matching
      2. Perplexity anomaly detection (simulated)
      3. Instruction/data ratio analysis
      4. Token distribution analysis
    """

    def __init__(self):
        self.sanitizer = InputSanitizer()
        self.detection_history: list[dict] = []
        self.false_positive_cache: set[str] = set()

    def analyze(
        self, user_input: str, context: Optional[list[str]] = None
    ) -> DetectionResult:
        """
        Perform comprehensive prompt injection analysis.

        Args:
            user_input: The user's input text
            context: Optional conversation history for context analysis

        Returns:
            DetectionResult with analysis details
        """
        signals = []
        attack_types = []
        confidence_factors = []

        # Analysis 1: Sanitizer-based detection
        _, warnings = self.sanitizer.sanitize(user_input)
        if warnings:
            signals.extend(warnings)
            attack_types.append(AttackType.DIRECT_INJECTION)
            confidence_factors.append(min(len(warnings) * 0.2, 0.8))

        # Analysis 2: Instruction-to-data ratio
        id_ratio = self._instruction_data_ratio(user_input)
        if id_ratio > 0.7:
            signals.append(f"High instruction-to-data ratio: {id_ratio:.2f}")
            confidence_factors.append(0.3)

        # Analysis 3: Declarative instruction count
        decl_count = self._count_declarative_instructions(user_input)
        if decl_count > 3:
            signals.append(f"Multiple declarative instructions detected ({decl_count})")
            confidence_factors.append(min(decl_count * 0.1, 0.5))

        # Analysis 4: Context manipulation (if context provided)
        if context:
            ctx_signal = self._analyze_context_shift(user_input, context)
            if ctx_signal:
                signals.append(ctx_signal)
                confidence_factors.append(0.4)

        # Analysis 5: Entropy analysis
        entropy = self._calculate_entropy(user_input)
        if entropy < 2.0 and len(user_input) > 50:
            signals.append(
                f"Low entropy ({entropy:.2f}) suggests structured/patterned input"
            )
            confidence_factors.append(0.2)

        # Calculate final scores
        confidence = min(sum(confidence_factors), 1.0) if confidence_factors else 0.0
        risk_score = self.sanitizer.get_risk_score(signals)
        is_suspicious = confidence > 0.3 or risk_score > 0.4

        # Determine recommended action
        if confidence > 0.7:
            action = "BLOCK: High-confidence injection detected"
        elif confidence > 0.4:
            action = "WARN: Suspicious patterns detected, apply enhanced filtering"
        elif confidence > 0.2:
            action = "MONITOR: Low-confidence signals, log for review"
        else:
            action = "ALLOW: No significant injection signals"

        # Deduplicate attack types
        unique_types = list(dict.fromkeys(attack_types))

        result = DetectionResult(
            is_suspicious=is_suspicious,
            confidence=confidence,
            attack_types=unique_types,
            details=signals,
            risk_score=risk_score,
            recommended_action=action,
        )

        # Log the detection event
        self.detection_history.append(
            {
                "input_hash": hashlib.sha256(user_input.encode()).hexdigest()[:16],
                "is_suspicious": is_suspicious,
                "confidence": confidence,
                "timestamp": time.time(),
            }
        )

        return result

    def _instruction_data_ratio(self, text: str) -> float:
        """Calculate ratio of imperative sentences to total content."""
        imperative_patterns = [
            r"(?i)^(you\s+(must|should|will|shall|need\s+to|have\s+to|are\s+going\s+to))\b",
            r"(?i)^(do\s+not|don't|never|always|ignore|forget|disregard)\b",
            r"(?i)^(let\s+me|pretend|imagine|assume|suppose)\b",
            r"(?i)^(respond|reply|answer|output|print|return|generate)\b",
            r"(?i)^(when|if)\s+.*then\s+",
        ]
        sentences = re.split(r"[.!?\n]", text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return 0.0

        imperative_count = 0
        for sentence in sentences:
            for pat in imperative_patterns:
                if re.match(pat, sentence):
                    imperative_count += 1
                    break

        return imperative_count / len(sentences)

    def _count_declarative_instructions(self, text: str) -> int:
        """Count explicit instruction-like declarations in text."""
        instruction_patterns = [
            r"(?i)(your|you(?:'re| are))\s+(new|actual|real)\s+(instructions?|role|purpose|job|task)",
            r"(?i)(from\s+now\s+on|henceforth|going\s+forward|effective\s+immediately)",
            r"(?i)(rule|policy|constraint)\s*[#:]\s*",
            r"(?i)(step\s*\d+\s*[:\.])",
        ]
        count = 0
        for pat in instruction_patterns:
            count += len(re.findall(pat, text))
        return count

    def _analyze_context_shift(self, current: str, history: list[str]) -> Optional[str]:
        """Detect suspicious context shifts between turns."""
        if not history:
            return None

        # Check if current input tries to reframe prior conversation
        reframing_patterns = [
            r"(?i)(actually|in\s+fact|correction|correction:)\s+(i|we|the)\s+(said|meant|told)",
            r"(?i)that\s+was\s+(just\s+)?(a\s+)?test",
            r"(?i)(sorry|my\s+bad|oops),?\s+(i\s+)?(meant|actually\s+want|was\s+joking)",
            r"(?i)(the\s+real|actual|true)\s+(request|question|task|prompt)\s+(is|was)",
        ]
        for pat in reframing_patterns:
            if re.search(pat, current):
                return "Context reframing detected - possible multi-turn injection"

        return None

    def _calculate_entropy(self, text: str) -> float:
        """Calculate Shannon entropy of the text."""
        if not text:
            return 0.0
        from math import log2

        freq = defaultdict(int)
        for char in text:
            freq[char] += 1
        length = len(text)
        entropy = -sum(
            (count / length) * log2(count / length) for count in freq.values()
        )
        return entropy


# =============================================================================
# Section 5: Conversation Guard (End-to-End Protection)
# =============================================================================
