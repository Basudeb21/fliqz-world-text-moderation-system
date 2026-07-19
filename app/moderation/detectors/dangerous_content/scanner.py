# app/moderation/detectors/dangerous_content/scanner.py

import re

from app.moderation.detectors.dangerous_content.keywords import (
    DRUG_WORDS,
    WEAPON_WORDS,
    EXPLOSIVE_WORDS,
    TERROR_GROUP_WORDS,
    RECRUITMENT_WORDS,
    PURCHASE_WORDS,
    INSTRUCTION_WORDS,
    INTENT_WORDS,
    TIME_WORDS,
    FIRST_PERSON,
    NEGATION_WORDS,
    CONTEXT_REDUCTION,
)

from app.moderation.detectors.dangerous_content.schemas import (
    DangerousContentFeatures,
)


def separate_words_and_phrases(keyword_set):
    """Separate single words from multi-word phrases"""
    single = set()
    phrases = set()
    for item in keyword_set:
        if ' ' in item:
            phrases.add(item)
        else:
            single.add(item)
    return single, phrases


# Separate single words and phrases for each feature
DRUG_SINGLE, DRUG_PHRASES = separate_words_and_phrases(DRUG_WORDS)
WEAPON_SINGLE, WEAPON_PHRASES = separate_words_and_phrases(WEAPON_WORDS)
EXPLOSIVE_SINGLE, EXPLOSIVE_PHRASES = separate_words_and_phrases(EXPLOSIVE_WORDS)
TERROR_SINGLE, TERROR_PHRASES = separate_words_and_phrases(TERROR_GROUP_WORDS)
RECRUIT_SINGLE, RECRUIT_PHRASES = separate_words_and_phrases(RECRUITMENT_WORDS)
PURCHASE_SINGLE, PURCHASE_PHRASES = separate_words_and_phrases(PURCHASE_WORDS)
INSTRUCTION_SINGLE, INSTRUCTION_PHRASES = separate_words_and_phrases(INSTRUCTION_WORDS)
INTENT_SINGLE, INTENT_PHRASES = separate_words_and_phrases(INTENT_WORDS)
TIME_SINGLE, TIME_PHRASES = separate_words_and_phrases(TIME_WORDS)
FIRST_SINGLE, FIRST_PHRASES = separate_words_and_phrases(FIRST_PERSON)
NEGATION_SINGLE, NEGATION_PHRASES = separate_words_and_phrases(NEGATION_WORDS)
CONTEXT_SINGLE, CONTEXT_PHRASES = separate_words_and_phrases(CONTEXT_REDUCTION)

# Feature map for single words (token matching)
FEATURE_MAP_SINGLE = (
    ("drug", DRUG_SINGLE),
    ("weapon", WEAPON_SINGLE),
    ("explosive", EXPLOSIVE_SINGLE),
    ("terror_group", TERROR_SINGLE),
    ("recruitment", RECRUIT_SINGLE),
    ("purchase", PURCHASE_SINGLE),
    ("instruction", INSTRUCTION_SINGLE),
    ("intent", INTENT_SINGLE),
    ("time", TIME_SINGLE),
    ("first_person", FIRST_SINGLE),
    ("negation", NEGATION_SINGLE),
)

# Feature map for multi-word phrases
FEATURE_MAP_PHRASES = (
    ("drug", DRUG_PHRASES),
    ("weapon", WEAPON_PHRASES),
    ("explosive", EXPLOSIVE_PHRASES),
    ("terror_group", TERROR_PHRASES),
    ("recruitment", RECRUIT_PHRASES),
    ("purchase", PURCHASE_PHRASES),
    ("instruction", INSTRUCTION_PHRASES),
    ("intent", INTENT_PHRASES),
    ("time", TIME_PHRASES),
    ("first_person", FIRST_PHRASES),
    ("negation", NEGATION_PHRASES),
)


class DangerousContentScanner:

    def scan(
        self,
        text: str,
    ) -> DangerousContentFeatures:

        text_lower = text.lower()

        # Tokenize individual words
        tokens = re.findall(r"\b[\w'-]+\b", text_lower)

        features = DangerousContentFeatures()

        matched = set()

        # ---------------------------------------------
        # SCAN INDIVIDUAL TOKENS (Single Words)
        # ---------------------------------------------
        
        for token in tokens:
            for field, keywords in FEATURE_MAP_SINGLE:
                if token in keywords:
                    setattr(
                        features,
                        field,
                        getattr(features, field) + 1,
                    )
                    matched.add(token)

        # ---------------------------------------------
        # SCAN MULTI-WORD PHRASES (FEATURES)
        # ---------------------------------------------
        
        for field, phrases in FEATURE_MAP_PHRASES:
            for phrase in phrases:
                if phrase in text_lower:
                    setattr(
                        features,
                        field,
                        getattr(features, field) + 1,
                    )
                    matched.add(phrase)

        # ---------------------------------------------
        # CONTEXT DETECTION
        # ---------------------------------------------
        
        context_count = 0
        context_phrases_found = []
        
        # Check multi-word context phrases
        for phrase in CONTEXT_PHRASES:
            if phrase in text_lower:
                context_count += 1
                context_phrases_found.append(phrase)
                matched.add(f"context_{phrase.replace(' ', '_')}")

        # Check single-word context
        for word in CONTEXT_SINGLE:
            if word in text_lower:
                context_count += 1
                matched.add(f"context_{word}")

        # ---------------------------------------------
        # ADDITIONAL SAFE CONTEXT PATTERNS
        # ---------------------------------------------
        
        safe_patterns = [
            # Educational/Safe contexts
            ("documentary", 2),
            ("history", 1),
            ("educational", 2),
            ("learning", 1),
            ("school", 1),
            ("university", 1),
            ("college", 1),
            ("research", 1),
            ("study", 1),
            ("news", 1),
            ("reported", 1),
            ("according", 1),
            ("article", 1),
            ("book", 1),
            ("novel", 1),
            ("movie", 1),
            ("film", 1),
            ("show", 1),
            ("tv", 1),
            ("game", 1),
            ("gaming", 1),
            ("discussion", 1),
            ("debate", 1),
            ("conversation", 1),
            ("talking", 1),
            ("discussing", 1),
            ("fiction", 2),
            ("fictional", 2),
            ("hypothetical", 2),
            ("imaginary", 2),
            ("museum", 1),
            ("exhibit", 1),
            ("historical", 1),
        ]
        
        for pattern, weight in safe_patterns:
            if pattern in text_lower:
                context_count += weight
                matched.add(f"safe_context_{pattern}")
        
        # Reporting/News patterns
        reporting_patterns = [
            "police said", "police reported", "officials said",
            "according to", "source said", "sources said",
            "reported that", "news reported", "media reported",
            "the police", "authorities said", "spokesperson said",
        ]
        
        for pattern in reporting_patterns:
            if pattern in text_lower:
                context_count += 3
                matched.add(f"reporting_context_{pattern.replace(' ', '_')}")
        
        # Academic patterns
        academic_patterns = [
            "in history", "historical context", "academic study",
            "research paper", "educational purpose", "learning about",
            "in class", "school project", "university study",
            "coursework", "assignment", "lecture", "seminar",
        ]
        
        for pattern in academic_patterns:
            if pattern in text_lower:
                context_count += 2
                matched.add(f"academic_context_{pattern.replace(' ', '_')}")
        
        # Entertainment patterns
        entertainment_patterns = [
            "in the movie", "in the film", "in the show",
            "video game", "role playing", "rpg", "character",
            "plot", "storyline", "scene", "episode",
            "the game", "playing a game", "movie about",
        ]
        
        for pattern in entertainment_patterns:
            if pattern in text_lower:
                context_count += 1
                matched.add(f"entertainment_context_{pattern.replace(' ', '_')}")

        # Set context reduction
        features.context_reduction = context_count
        
        # ---------------------------------------------
        # DEBUG OUTPUT
        # ---------------------------------------------
        
        print(f"[DangerousContent Scanner] Context count: {context_count}")
        if context_phrases_found:
            print(f"[DangerousContent Scanner] Context phrases: {context_phrases_found}")
        
        print(f"[DangerousContent Scanner] Features: drug={features.drug}, "
              f"weapon={features.weapon}, explosive={features.explosive}, "
              f"terror_group={features.terror_group}, recruitment={features.recruitment}, "
              f"purchase={features.purchase}, instruction={features.instruction}, "
              f"intent={features.intent}, time={features.time}, "
              f"first_person={features.first_person}, negation={features.negation}, "
              f"context_reduction={features.context_reduction}")
        
        print(f"[DangerousContent Scanner] Matched: {sorted(matched)}")

        features.matched_keywords = sorted(matched)

        return features