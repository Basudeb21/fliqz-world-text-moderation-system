# schemas/moderation_result.py
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ModerationResult:
    """
    Standard response returned by every detector.
    """

    category: str

    detected: bool

    confidence: float = 0.0

    severity: str = "low"

    evidence: List[str] = field(default_factory=list)

    reason: Optional[str] = None

    blocked: bool = False

    metadata: dict = field(default_factory=dict)