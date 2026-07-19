# app/moderation/detectors/suicide/schemas.py

from dataclasses import dataclass, field


@dataclass
class SuicideFeatures:
    """
    Features extracted by the fast scanner.

    These are raw counts only.
    No scoring happens here.
    """

    # Category Counts
    death: int = 0
    self_harm: int = 0
    intent: int = 0
    first_person: int = 0
    emotion: int = 0
    farewell: int = 0
    time: int = 0
    method: int = 0
    negation: int = 0

    # Phrase Matches
    suicide_phrase: int = 0
    method_phrase: int = 0
    farewell_phrase: int = 0

    # Scanner Output
    matched_keywords: list[str] = field(default_factory=list)
    matched_phrases: list[str] = field(default_factory=list)


@dataclass
class SuicideRisk:
    """
    Final risk score before deciding whether
    the LLM should be called.
    """

    score: int
    threshold: int
    should_call_llm: bool

    matched_keywords: list[str] = field(default_factory=list)
    matched_phrases: list[str] = field(default_factory=list)