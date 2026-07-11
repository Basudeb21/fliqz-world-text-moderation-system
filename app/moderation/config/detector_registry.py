# moderation/config/detector_registry.py
from typing import List

from app.moderation.detectors.base import BaseDetector
from app.moderation.detectors.pii.detector import PIIDetector
from app.moderation.detectors.child_safety.detector import ChildSafetyDetector

def get_registered_detectors() -> List[BaseDetector]:
    """
    Register all moderation detectors here.

    Whenever a new detector is created,
    simply add it to this list.
    """

    detectors: List[BaseDetector] = [

        PIIDetector(),

        ChildSafetyDetector(),

    ]

    return detectors