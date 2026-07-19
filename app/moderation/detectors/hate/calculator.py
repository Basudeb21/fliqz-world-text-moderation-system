# app/moderation/detectors/hate/calculator.py

from app.moderation.detectors.hate.schemas import (
    HateSpeechFeatures,
    HateSpeechRisk,
)


class HateSpeechRiskCalculator:

    THRESHOLD = 5

    def calculate(
        self,
        features: HateSpeechFeatures,
    ) -> HateSpeechRisk:

        score = 0

        # -------------------------
        # Base Weights
        # -------------------------

        score += features.identity * 2
        score += features.slur * 6
        score += features.insult * 2
        score += features.violence * 4
        score += features.dehumanization * 5
        score += features.threat * 4
        score += features.target * 1
        score += features.first_person * 1

        # -------------------------
        # Combination Bonuses
        # -------------------------

        # protected group + insult
        if features.identity and features.insult:
            score += 5

        # protected group + slur
        if features.identity and features.slur:
            score += 8

        # protected group + violence
        if features.identity and features.violence:
            score += 8

        # protected group + threat
        if features.identity and features.threat:
            score += 8

        # protected group + dehumanization
        if features.identity and features.dehumanization:
            score += 8

        # directed at someone
        if features.identity and features.target:
            score += 3

        # slur + violence
        if features.slur and features.violence:
            score += 8

        # slur + threat
        if features.slur and features.threat:
            score += 8

        # slur + dehumanization
        if features.slur and features.dehumanization:
            score += 8

        # violence + threat
        if features.violence and features.threat:
            score += 5

        # -------------------------
        # Triple Combination Bonuses
        # -------------------------

        # Identity + Violence + Threat
        if features.identity and features.violence and features.threat:
            score += 10

        # Identity + Slur + Violence
        if features.identity and features.slur and features.violence:
            score += 10

        # Identity + Slur + Threat
        if features.identity and features.slur and features.threat:
            score += 10

        # Identity + Slur + Dehumanization
        if features.identity and features.slur and features.dehumanization:
            score += 10

        # Identity + Dehumanization + Violence
        if features.identity and features.dehumanization and features.violence:
            score += 10

        # Identity + Violence + Target
        if features.identity and features.violence and features.target:
            score += 8

        # Identity + Dehumanization + Target
        if features.identity and features.dehumanization and features.target:
            score += 8

        # Multiple slurs
        if features.slur >= 2:
            score += 5

        # Multiple identities
        if features.identity >= 3:
            score += 3

        # -------------------------
        # Negation
        # -------------------------

        if features.negation:
            score -= 3

        score = max(score, 0)

        # -------------------------
        # Decide LLM
        # -------------------------

        should_call_llm = False

        # High score
        if score >= self.THRESHOLD:
            should_call_llm = True

        # Any slur deserves context checking
        elif features.slur:
            should_call_llm = True

        # Identity directed at someone
        elif features.identity and features.target:
            should_call_llm = True

        # Identity + abusive wording
        elif (
            features.identity
            and (
                features.insult
                or features.violence
                or features.threat
                or features.dehumanization
            )
        ):
            should_call_llm = True

        # Explicit violent threats
        elif features.violence and features.threat:
            should_call_llm = True

        return HateSpeechRisk(
            score=score,
            threshold=self.THRESHOLD,
            should_call_llm=should_call_llm,
            matched_keywords=features.matched_keywords,
        )