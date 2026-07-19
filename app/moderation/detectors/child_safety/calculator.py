# app/moderation/detectors/child_safety/calculator.py
from app.moderation.detectors.child_safety.schemas import (
    ChildSafetyFeatures,
    ChildSafetyRisk,
)


class ChildSafetyRiskCalculator:

    # Minimum score before calling the LLM
    THRESHOLD = 8

    def calculate(
        self,
        features: ChildSafetyFeatures,
    ) -> ChildSafetyRisk:

        score = 0

        # -----------------------------
        # Base Weights
        # -----------------------------

        score += features.age * 2
        score += features.minor * 4
        score += features.sexual * 5
        score += features.grooming * 4
        score += features.meeting * 2
        score += features.relationship * 2
        score += features.coercion * 3
        score += features.first_person * 1

        # -----------------------------
        # Combination Bonuses
        # -----------------------------

        # Minor + Sexual
        if features.minor and features.sexual:
            score += 8

        # Age + Sexual
        if features.age and features.sexual:
            score += 6

        # Minor + Grooming
        if features.minor and features.grooming:
            score += 6

        # Minor + Meeting
        if features.minor and features.meeting:
            score += 5

        # Minor + Relationship
        if features.minor and features.relationship:
            score += 5

        # Grooming + Meeting
        if features.grooming and features.meeting:
            score += 4

        # Grooming + Relationship
        if features.grooming and features.relationship:
            score += 4

        # Coercion + Sexual
        if features.coercion and features.sexual:
            score += 5

        # First Person + Age
        if features.first_person and features.age:
            score += 2

        # -----------------------------
        # Negation
        # -----------------------------

        if features.negation:
            score -= 3

        score = max(score, 0)

        return ChildSafetyRisk(
            score=score,
            threshold=self.THRESHOLD,
            should_call_llm=score >= self.THRESHOLD,
            matched_keywords=features.matched_keywords,
        )