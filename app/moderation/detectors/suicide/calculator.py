# app/moderation/detectors/suicide/calculator.py

from app.moderation.detectors.suicide.schemas import (
    SuicideFeatures,
    SuicideRisk,
)


class SuicideRiskCalculator:
    """
    Calculates the suicide risk score from the
    extracted scanner features.
    """

    # LOWER THRESHOLD for better detection
    THRESHOLD = 6  # Changed from 10 to 6

    def calculate(
        self,
        features: SuicideFeatures,
    ) -> SuicideRisk:

        score = 0

        # ============================================================
        # Base Feature Weights (INCREASED)
        # ============================================================

        score += features.death * 4          # Increased from 3
        score += features.self_harm * 5      # Increased from 4
        score += features.intent * 4         # Increased from 2
        score += features.first_person * 2   # Increased from 1
        score += features.emotion * 2        # Increased from 1
        score += features.farewell * 3       # Increased from 2
        score += features.time * 2           # Increased from 1
        score += features.method * 4         # Increased from 3

        # Strong phrase matches
        score += features.suicide_phrase * 10  # Increased from 8
        score += features.method_phrase * 8    # Increased from 6
        score += features.farewell_phrase * 6  # Increased from 5

        # ============================================================
        # Combination Bonuses (ENHANCED)
        # ============================================================

        # "I want to die"
        if features.first_person and features.intent and features.death:
            score += 10  # Increased from 8

        # "I want to kill myself"
        if features.first_person and features.intent and features.self_harm:
            score += 10  # Increased from 8

        # "I'm hopeless and want to die"
        if features.emotion and features.intent and features.death:
            score += 8  # Increased from 6

        # "Goodbye... I'm going tonight"
        if features.farewell and (features.death or features.self_harm):
            score += 8  # Increased from 6

        # Suicide method + intent
        if features.method and features.intent:
            score += 8  # Increased from 5

        # Suicide method + time
        if features.method and features.time:
            score += 6  # Increased from 4

        # Death + time
        if features.death and features.time:
            score += 6  # Increased from 4

        # First Person + Intent + Method
        if features.first_person and features.intent and features.method:
            score += 12  # NEW

        # Emotion + Intent
        if features.emotion and features.intent:
            score += 6  # NEW

        # Method + Self Harm
        if features.method and features.self_harm:
            score += 8  # NEW

        # Farewell + Intent
        if features.farewell and features.intent:
            score += 6  # NEW

        # Multiple methods
        if features.method >= 2:
            score += 4  # NEW

        # Multiple emotions
        if features.emotion >= 3:
            score += 3  # NEW

        # ============================================================
        # Negation
        # "I don't want to die"
        # ============================================================

        if features.negation:
            score -= (features.negation * 5)

        score = max(score, 0)

        # ============================================================
        # Decide whether to call LLM
        # ============================================================

        should_call_llm = False

        # High score
        if score >= self.THRESHOLD:
            should_call_llm = True

        # Suicide phrase detected
        elif features.suicide_phrase >= 1:
            should_call_llm = True

        # Method phrase detected
        elif features.method_phrase >= 1:
            should_call_llm = True

        # First person + Intent + (Death or Self Harm or Method)
        elif features.first_person and features.intent and (features.death or features.self_harm or features.method):
            should_call_llm = True

        # Farewell + (Death or Self Harm)
        elif features.farewell and (features.death or features.self_harm):
            should_call_llm = True

        # Emotion + Intent + Death
        elif features.emotion and features.intent and features.death:
            should_call_llm = True

        return SuicideRisk(
            score=score,
            threshold=self.THRESHOLD,
            should_call_llm=should_call_llm,
            matched_keywords=features.matched_keywords,
            matched_phrases=features.matched_phrases,
        )