# app/moderation/detectors/hate/scanner.py

import re

from app.moderation.detectors.hate.keywords import (
    IDENTITY_WORDS,
    SLUR_WORDS,
    INSULT_WORDS,
    VIOLENCE_WORDS,
    DEHUMANIZATION_WORDS,
    THREAT_WORDS,
    TARGET_WORDS,
    FIRST_PERSON,
    NEGATION_WORDS,
)

from app.moderation.detectors.hate.schemas import (
    HateSpeechFeatures,
)


FEATURE_MAP = (
    ("identity", IDENTITY_WORDS),
    ("slur", SLUR_WORDS),
    ("insult", INSULT_WORDS),
    ("violence", VIOLENCE_WORDS),
    ("dehumanization", DEHUMANIZATION_WORDS),
    ("threat", THREAT_WORDS),
    ("target", TARGET_WORDS),
    ("first_person", FIRST_PERSON),
    ("negation", NEGATION_WORDS),
)


class HateSpeechScanner:

    def scan(self, text: str) -> HateSpeechFeatures:

        text = text.lower()

        tokens = re.findall(r"\b[\w']+\b", text)

        features = HateSpeechFeatures()

        matched = set()

        for token in tokens:

            for field, keywords in FEATURE_MAP:

                if token in keywords:

                    setattr(
                        features,
                        field,
                        getattr(features, field) + 1,
                    )

                    matched.add(token)

        features.matched_keywords = sorted(matched)

        return features