# app/moderation/detectors/dangerous_content/schemas.py

from dataclasses import dataclass, field


@dataclass
class DangerousContentFeatures:
    """
    Features extracted by the fast scanner.
    """

    # Drugs
    drug: int = 0

    # Weapons
    weapon: int = 0

    # Explosives
    explosive: int = 0

    # Terrorist organizations
    terror_group: int = 0

    # Recruitment / support
    recruitment: int = 0

    # Buying / selling
    purchase: int = 0

    # Instructional language
    instruction: int = 0

    # Intent
    intent: int = 0

    # Time
    time: int = 0

    # First person
    first_person: int = 0

    # Negation
    negation: int = 0

    # Context reduction (safe contexts)
    context_reduction: int = 0

    matched_keywords: list[str] = field(default_factory=list)


@dataclass
class DangerousContentRisk:
    """
    Final risk score before LLM.
    """

    score: int
    threshold: int
    should_call_llm: bool
    matched_keywords: list[str]