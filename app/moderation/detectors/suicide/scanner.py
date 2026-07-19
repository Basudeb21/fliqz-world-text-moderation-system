# app/moderation/detectors/suicide/scanner.py

import re

from app.moderation.detectors.suicide.schemas import SuicideFeatures
from app.moderation.detectors.suicide.keywords import *


class SuicideScanner:

    def scan(self, text: str) -> SuicideFeatures:

        text = text.lower().strip()

        tokens = re.findall(r"\b[\w']+\b", text)

        features = SuicideFeatures()

        keyword_matches = set()
        phrase_matches = set()

        # ============================================================
        # Keyword Detection
        # ============================================================

        for token in tokens:

            if token in DEATH_WORDS:
                features.death += 1
                keyword_matches.add(token)

            if token in SELF_HARM_WORDS:
                features.self_harm += 1
                keyword_matches.add(token)

            if token in INTENT_WORDS:
                features.intent += 1
                keyword_matches.add(token)

            if token in FIRST_PERSON_WORDS:
                features.first_person += 1
                keyword_matches.add(token)

            if token in EMOTION_WORDS:
                features.emotion += 1
                keyword_matches.add(token)

            if token in FAREWELL_WORDS:
                features.farewell += 1
                keyword_matches.add(token)

            if token in TIME_WORDS:
                features.time += 1
                keyword_matches.add(token)

            if token in METHOD_WORDS:
                features.method += 1
                keyword_matches.add(token)

            if token in NEGATION_WORDS:
                features.negation += 1
                keyword_matches.add(token)

        # ============================================================
        # Phrase Detection (2-4 word phrases)
        # ============================================================

        grams = []

        for n in (2, 3, 4):

            for i in range(len(tokens) - n + 1):

                grams.append(" ".join(tokens[i:i+n]))

        for phrase in grams:

            if phrase in SUICIDE_PHRASES:
                features.suicide_phrase += 1
                phrase_matches.add(phrase)

            if phrase in METHOD_PHRASES:
                features.method_phrase += 1
                phrase_matches.add(phrase)

            if phrase in FAREWELL_PHRASES:
                features.farewell_phrase += 1
                phrase_matches.add(phrase)

        # Debug output
        print(f"[Suicide Scanner] Death: {features.death}, Self-harm: {features.self_harm}")
        print(f"[Suicide Scanner] Intent: {features.intent}, First-person: {features.first_person}")
        print(f"[Suicide Scanner] Emotion: {features.emotion}, Method: {features.method}")
        print(f"[Suicide Scanner] Suicide phrase: {features.suicide_phrase}, Method phrase: {features.method_phrase}")

        features.matched_keywords = sorted(keyword_matches)
        features.matched_phrases = sorted(phrase_matches)

        return features