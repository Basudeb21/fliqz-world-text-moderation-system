# app/moderation/schemas/risk_result.py
from dataclasses import dataclass, field
from typing import List


@dataclass
class RiskResult:
    """
    Result returned by the Fast Risk Scanner.
    """

    score: int = 0

    threshold: int = 5

    matched_keywords: List[str] = field(default_factory=list)

    should_call_llm: bool = False