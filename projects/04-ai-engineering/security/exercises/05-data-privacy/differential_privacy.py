"""
05 Data Privacy: Differential Privacy
"""

from ._types import *

class DifferentialPrivacy:
    """
    Implements basic differential privacy mechanisms for data protection.

    Differential privacy provides mathematical guarantees that individual
    records cannot be distinguished from aggregate statistics.
    """

    def __init__(self, epsilon: float = 1.0, delta: float = 1e-5):
        """
        Args:
            epsilon: Privacy budget (lower = more private, typical: 0.1-10)
            delta: Probability of privacy guarantee failure
        """
        self.epsilon = epsilon
        self.delta = delta
        self.privacy_budget_used = 0.0

    def laplace_mechanism(self, value: float, sensitivity: float = 1.0) -> float:
        """
        Add Laplace noise to a numeric value.

        Args:
            value: True value to protect
            sensitivity: Maximum change one individual can cause

        Returns:
            Noisy value
        """
        if self.privacy_budget_used >= self.epsilon:
            logger.warning("Privacy budget exhausted!")
            return value

        scale = sensitivity / self.epsilon
        noise = random.random()  # Uniform [0, 1]
        # Convert to Laplace distribution
        if noise < 0.5:
            noisy_value = value - scale * math.log(1 - 2 * noise)
        else:
            noisy_value = value + scale * math.log(2 * noise - 1)

        self.privacy_budget_used += self.epsilon / 100  # Approximate budget tracking
        return noisy_value

    def gaussian_mechanism(self, value: float, sensitivity: float = 1.0) -> float:
        """
        Add Gaussian noise for (epsilon, delta)-differential privacy.

        Args:
            value: True value to protect
            sensitivity: L2 sensitivity

        Returns:
            Noisy value
        """
        if self.privacy_budget_used >= self.epsilon:
            return value

        sigma = (
            sensitivity * math.sqrt(2 * math.log(1.25 / self.delta))
        ) / self.epsilon
        noise = random.gauss(0, sigma)

        self.privacy_budget_used += self.epsilon / 100
        return value + noise

    def exponential_mechanism(
        self,
        candidates: list[Any],
        scores: list[float],
        sensitivity: float = 1.0,
    ) -> Any:
        """
        Select an item from candidates using the exponential mechanism.

        Args:
            candidates: List of possible outputs
            scores: Utility scores for each candidate (higher = more useful)
            sensitivity: Maximum change in score from one individual

        Returns:
            Selected candidate
        """
        if len(candidates) != len(scores):
            raise ValueError("candidates and scores must have same length")

        # Calculate selection probabilities
        max_score = max(scores)
        probabilities = []
        for score in scores:
            prob = math.exp((self.epsilon * score) / (2 * sensitivity))
            probabilities.append(prob)

        # Normalize
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]

        # Weighted random selection
        rand = random.random()
        cumulative = 0.0
        for i, prob in enumerate(probabilities):
            cumulative += prob
            if rand <= cumulative:
                return candidates[i]

        return candidates[-1]

    def randomized_response(self, true_answer: bool) -> bool:
        """
        Implement randomized response for boolean questions.

        Each respondent answers truthfully with probability p = e^epsilon / (1 + e^epsilon),
        and randomly otherwise. This provides plausible deniability.
        """
        p = math.exp(self.epsilon) / (1 + math.exp(self.epsilon))
        if random.random() < p:
            return true_answer
        else:
            return random.random() < 0.5

    def get_privacy_report(self) -> dict:
        """Get a report on privacy budget usage."""
        return {
            "epsilon": self.epsilon,
            "delta": self.delta,
            "budget_used": round(self.privacy_budget_used, 4),
            "budget_remaining": round(self.epsilon - self.privacy_budget_used, 4),
            "utilization": f"{(self.privacy_budget_used / self.epsilon * 100):.1f}%",
        }


# =============================================================================
# Section 5: Data Masking Strategies
# =============================================================================


