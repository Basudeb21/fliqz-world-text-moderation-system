# moderation/detectors/base.py
from abc import ABC, abstractmethod

from app.moderation.schemas.moderation_result import ModerationResult


class BaseDetector(ABC):
    """
    Base class for all moderation detectors.

    Every detector must inherit from this class and implement
    the analyze() method.

    Example:
        PIIDetector
        ChildSafetyDetector
        SuicideDetector
        HateSpeechDetector
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def analyze(self, text: str) -> ModerationResult:
        """
        Analyze a piece of text.

        Args:
            text: User submitted text.

        Returns:
            ModerationResult
        """
        raise NotImplementedError

    def __repr__(self):
        return f"<Detector name='{self.name}'>"