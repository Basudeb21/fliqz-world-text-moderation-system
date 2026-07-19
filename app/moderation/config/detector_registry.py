# moderation/config/detector_registry.py
from typing import List

from app.moderation.detectors.base import BaseDetector
from app.moderation.detectors.pii.detector import PIIDetector
from app.moderation.detectors.child_safety.detector import ChildSafetyDetector
from app.moderation.detectors.suicide.detector import SuicideDetector
from app.moderation.detectors.hate.detector import HateSpeechDetector
from app.moderation.detectors.dangerous_content.detector import DangerousContentDetector

def get_registered_detectors() -> List[BaseDetector]:
    """
    Register all moderation detectors here.

    Whenever a new detector is created,
    simply add it to this list.
    """

    detectors: List[BaseDetector] = [

        PIIDetector(),
        ChildSafetyDetector(),
        SuicideDetector(),
        HateSpeechDetector(),
        DangerousContentDetector()
    ]

    return detectors