# app/moderation/detectors/dangerous_content/calculator.py

from app.moderation.detectors.dangerous_content.schemas import (
    DangerousContentFeatures,
    DangerousContentRisk,
)

# Import from keywords
from .keywords import (
    SEXUAL_TERMS,
    THREAT_TERMS,
    DANGEROUS_KEYWORDS,
)


class DangerousContentRiskCalculator:

    # Lower threshold for dangerous content
    THRESHOLD = 5

    def calculate(
        self,
        features: DangerousContentFeatures,
        text: str = "",
    ) -> DangerousContentRisk:

        text_lower = text.lower()
        score = 0

        # ---------------------------------
        # Base Weights
        # ---------------------------------

        score += features.drug * 3
        score += features.weapon * 4
        score += features.explosive * 6
        score += features.terror_group * 5
        score += features.recruitment * 6
        score += features.purchase * 4
        score += features.instruction * 5
        score += features.intent * 3
        score += features.time * 2
        score += features.first_person * 2

        # ---------------------------------
        # Combination Bonuses
        # ---------------------------------

        if features.drug and features.purchase:
            score += 8

        if features.drug and features.instruction:
            score += 10

        if features.drug and features.intent:
            score += 6

        if features.weapon and features.purchase:
            score += 10

        if features.weapon and features.instruction:
            score += 10

        if (
            features.weapon
            and features.intent
            and features.first_person
        ):
            score += 12

        if (
            features.explosive
            and features.instruction
        ):
            score += 12

        if (
            features.explosive
            and features.purchase
        ):
            score += 10

        if (
            features.terror_group
            and features.recruitment
        ):
            score += 15

        if (
            features.terror_group
            and features.instruction
        ):
            score += 12

        if (
            features.terror_group
            and features.intent
        ):
            score += 10

        if (
            features.purchase
            and features.intent
        ):
            score += 5

        if (
            features.time
            and features.intent
            and features.first_person
        ):
            score += 6

        # ---------------------------------
        # Multiple Dangerous Categories
        # ---------------------------------

        dangerous_categories = sum([
            features.drug > 0,
            features.weapon > 0,
            features.explosive > 0,
            features.terror_group > 0,
        ])

        if dangerous_categories >= 2:
            score += 5

        if dangerous_categories >= 3:
            score += 8

        # ============================================================
        # Context-Based Reduction for Sexual Content
        # Uses imported SEXUAL_TERMS and THREAT_TERMS
        # ============================================================
        
        has_sexual = any(term in text_lower for term in SEXUAL_TERMS)
        has_threat = any(term in text_lower for term in THREAT_TERMS)
        
        # If sexual content but no threats, AND no dangerous keywords
        if has_sexual and not has_threat:
            has_dangerous = any(keyword in text_lower for keyword in DANGEROUS_KEYWORDS)
            
            if not has_dangerous:
                # Sexual content only - reduce score significantly
                print(f"[DangerousContent Calculator] Sexual content without threats - reducing score")
                score = max(0, score - 10)

        # ---------------------------------
        # Safe Context Reduction
        # (Already calculated by scanner)
        # ---------------------------------

        if features.context_reduction >= 3:
            score = max(0, score - 5)

        elif features.context_reduction >= 1:
            score = max(0, score - 2)

        # ---------------------------------
        # Negation
        # ---------------------------------

        if features.negation:
            score -= 3

        score = max(0, score)

        # ---------------------------------
        # Decide whether LLM is required
        # ---------------------------------

        should_call_llm = False

        if score >= self.THRESHOLD:
            should_call_llm = True

        elif features.terror_group:
            should_call_llm = True

        elif features.explosive:
            should_call_llm = True

        elif (
            features.weapon
            and features.intent
            and features.first_person
        ):
            should_call_llm = True

        elif (
            features.drug
            and features.instruction
        ):
            should_call_llm = True

        elif (
            (features.drug or features.weapon)
            and features.purchase
        ):
            should_call_llm = True

        return DangerousContentRisk(
            score=score,
            threshold=self.THRESHOLD,
            should_call_llm=should_call_llm,
            matched_keywords=features.matched_keywords,
        )