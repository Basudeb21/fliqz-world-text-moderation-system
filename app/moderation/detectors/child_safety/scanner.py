# app/moderation/detectors/child_safety/scanner.py
import re

from app.moderation.detectors.child_safety.keywords import (
    AGE_WORDS,
    MINOR_WORDS,
    SEXUAL_WORDS,
    GROOMING_WORDS,
    MEETING_WORDS,
    RELATIONSHIP_WORDS,
    COERCION_WORDS,
    FIRST_PERSON,
    NEGATION_WORDS,
)

from app.moderation.detectors.child_safety.schemas import (
    ChildSafetyFeatures,
)


class ChildSafetyScanner:

    def scan(self, text: str) -> ChildSafetyFeatures:

        text = text.lower()

        tokens = re.findall(r"\b[\w']+\b", text)

        features = ChildSafetyFeatures()

        matched = set()

        for token in tokens:

            if token in AGE_WORDS:
                features.age += 1
                matched.add(token)

            if token in MINOR_WORDS:
                features.minor += 1
                matched.add(token)

            if token in SEXUAL_WORDS:
                features.sexual += 1
                matched.add(token)

            if token in GROOMING_WORDS:
                features.grooming += 1
                matched.add(token)

            if token in MEETING_WORDS:
                features.meeting += 1
                matched.add(token)

            if token in RELATIONSHIP_WORDS:
                features.relationship += 1
                matched.add(token)

            if token in COERCION_WORDS:
                features.coercion += 1
                matched.add(token)

            if token in FIRST_PERSON:
                features.first_person += 1
                matched.add(token)

            if token in NEGATION_WORDS:
                features.negation += 1
                matched.add(token)

        features.matched_keywords = sorted(matched)

        return features