# app/moderation/detectors/child_safety/schemas.py

from dataclasses import dataclass, field


@dataclass
class ChildSafetyFeatures:
    """
    Features extracted by the fast scanner.
    """

    age: int = 0
    minor: int = 0
    sexual: int = 0
    grooming: int = 0
    meeting: int = 0
    relationship: int = 0
    coercion: int = 0
    first_person: int = 0
    negation: int = 0

    matched_keywords: list[str] = field(default_factory=list)


@dataclass
class ChildSafetyRisk:
    """
    Final risk score before calling the LLM.
    """

    score: int
    threshold: int
    should_call_llm: bool
    matched_keywords: list[str]