# moderation/detectors/child_safety/detector.py
from app.moderation.detectors.base import BaseDetector
from app.moderation.schemas.moderation_result import ModerationResult
from app.moderation.detectors.child_safety.engine import moderation_llama


class ChildSafetyDetector(BaseDetector):

    def __init__(self):
        super().__init__("child_safety")

    def analyze(self, text: str) -> ModerationResult:

        classification, reason = moderation_llama(text)

        detected = classification.upper() == "UNSAFE"

        return ModerationResult(
            category="child_safety",
            detected=detected,
            confidence=1.0 if detected else 0.0,
            severity="critical" if detected else "low",
            evidence=[],
            blocked=detected,
            reason=reason,
            metadata={
                "classification": classification
            }
        )
