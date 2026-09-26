"""
01 Prompt Injection: Conversation Guard
"""

from ._types import *
from .detector import DetectionResult, PromptInjectionDetector


@dataclass
class ConversationTurn:
    """A single turn in a conversation."""

    role: str  # "user" or "assistant"
    content: str
    timestamp: float = field(default_factory=time.time)
    flagged: bool = False


class ConversationGuard:
    """
    End-to-end conversation protection system.

    Monitors the full conversation for:
      1. Single-turn injection attempts
      2. Multi-turn escalation patterns
      3. Context poisoning
      4. Goal hijacking
    """

    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt
        self.detector = PromptInjectionDetector()
        self.turns: list[ConversationTurn] = []
        self.escalation_threshold = 3  # Flag after N suspicious turns
        self.suspicious_turn_count = 0

    def process_user_message(self, message: str) -> tuple[bool, str, DetectionResult]:
        """
        Process and validate a user message.

        Args:
            message: The user's input message

        Returns:
            Tuple of (is_safe, processed_message, detection_result)
        """
        # Detect injection attempts
        result = self.detector.analyze(
            message,
            context=[
                t.content
                for t in self.turns[-5:]  # Last 5 turns
            ],
        )

        turn = ConversationTurn(
            role="user", content=message, flagged=result.is_suspicious
        )

        if result.is_suspicious:
            self.suspicious_turn_count += 1
            turn.flagged = True
            logger.warning(
                f"Suspicious turn #{self.suspicious_turn_count}: "
                f"confidence={result.confidence:.2f}, "
                f"types={[t.name for t in result.attack_types]}"
            )

            # Escalation detection
            if self.suspicious_turn_count >= self.escalation_threshold:
                logger.critical(
                    f"Escalation threshold reached ({self.suspicious_turn_count} suspicious turns). "
                    "Consider terminating session."
                )

        self.turns.append(turn)

        # Sanitize input before passing to LLM
        sanitized, warnings = self.detector.sanitizer.sanitize(message)

        return result.is_suspicious, sanitized, result

    def get_defense_summary(self) -> dict:
        """Get a summary of all defense actions taken in this conversation."""
        total_turns = len(self.turns)
        flagged_turns = sum(1 for t in self.turns if t.flagged)
        return {
            "total_turns": total_turns,
            "flagged_turns": flagged_turns,
            "flag_rate": flagged_turns / max(total_turns, 1),
            "escalation_threshold": self.escalation_threshold,
            "current_streak": self.suspicious_turn_count,
            "system_prompt_hash": hashlib.sha256(
                self.system_prompt.encode()
            ).hexdigest()[:16],
        }


# =============================================================================
# Section 6: Demonstration & Testing
# =============================================================================
