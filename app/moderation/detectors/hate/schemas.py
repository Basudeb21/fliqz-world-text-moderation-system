# app/moderation/detectors/hate/schemas.py

from dataclasses import dataclass, field


@dataclass
class HateSpeechFeatures:
    """
    Features extracted by the fast scanner.
    """

    # Protected identity
    identity: int = 0

    # Known hate slurs
    slur: int = 0

    # Generic insults
    insult: int = 0

    # Violence
    violence: int = 0

    # Dehumanization
    dehumanization: int = 0

    # Threats
    threat: int = 0

    # Target words
    target: int = 0

    # First person
    first_person: int = 0

    # Negation
    negation: int = 0

    matched_keywords: list[str] = field(default_factory=list)


@dataclass
class HateSpeechRisk:
    """
    Final risk score before LLM.
    """

    score: int
    threshold: int
    should_call_llm: bool
    matched_keywords: list[str]