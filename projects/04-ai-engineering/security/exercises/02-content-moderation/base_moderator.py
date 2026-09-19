"""
02 Content Moderation: Base Moderator
"""

from ._types import *

class ContentModerator(ABC):
    """Abstract base class for content moderators."""

    @abstractmethod
    def check(self, text: str) -> list[ModerationResult]:
        """Check text and return list of moderation results."""
        pass

    @property
    @abstractmethod
    def category(self) -> ContentCategory:
        """The content category this moderator handles."""
        pass


# =============================================================================
# Section 3: Hate Speech Detection
# =============================================================================


