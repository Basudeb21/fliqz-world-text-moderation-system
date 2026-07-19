# app/moderation/detectors/pii/detector.py
from app.moderation.detectors.base import BaseDetector
from app.moderation.schemas.moderation_result import ModerationResult
from app.moderation.detectors.pii.engine import detect_personal_info

class PIIDetector(BaseDetector):

    def __init__(self):
        super().__init__("pii")

    def analyze(self, text: str) -> ModerationResult:

        detected = detect_personal_info(text)

        return ModerationResult(
            category=self.name,
            detected=detected,
            confidence=1.0 if detected else 0.0,
            severity="high" if detected else "low",
            evidence=[],
            blocked=detected,
            reason="Personal information detected" if detected else None,
        )

