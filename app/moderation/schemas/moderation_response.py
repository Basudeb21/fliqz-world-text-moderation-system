# moderation/schemas/moderation_response.py
from dataclasses import dataclass, field
from typing import List

from app.moderation.schemas.moderation_result import ModerationResult


@dataclass
class ModerationResponse:
    """
    Final response returned by the Moderation Engine.

    This object contains the combined result of all detectors
    after the policy engine has evaluated them.
    """

    blocked: bool = False

    action: str = "ALLOW"

    highest_severity: str = "none"

    categories: List[str] = field(default_factory=list)

    results: List[ModerationResult] = field(default_factory=list)