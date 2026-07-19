# app/moderation/detectors/suicide/detector.py

from app.moderation.detectors.base import BaseDetector
from app.moderation.schemas.moderation_result import ModerationResult

from .scanner import SuicideScanner
from .calculator import SuicideRiskCalculator
from .engine import SuicideEngine

from .keywords import (
    EXTREME_SUICIDE_PATTERNS,
    SUICIDE_PHRASES,
    METHOD_PHRASES,
    HELP_SEEKING_PHRASES,
)


class SuicideDetector(BaseDetector):

    def __init__(self):

        super().__init__("suicide")

        self.scanner = SuicideScanner()
        self.calculator = SuicideRiskCalculator()
        self.engine = SuicideEngine()

    def analyze(
        self,
        text: str,
    ) -> ModerationResult:

        text_lower = text.lower()

        # ============================================================
        # PRE-CHECK: Extreme Suicide Patterns
        # ============================================================

        # Check for extreme suicide patterns
        has_extreme = any(pattern in text_lower for pattern in EXTREME_SUICIDE_PATTERNS)
        has_suicide_phrase = any(phrase in text_lower for phrase in SUICIDE_PHRASES)
        has_method_phrase = any(phrase in text_lower for phrase in METHOD_PHRASES)
        has_help = any(phrase in text_lower for phrase in HELP_SEEKING_PHRASES)

        # If it's a help-seeking message, ALLOW (don't block)
        if has_help and not has_extreme and not has_suicide_phrase and not has_method_phrase:
            print(f"[Suicide] Help-seeking detected - ALLOWING: {text}")
            return ModerationResult(
                category="suicide",
                detected=False,
                confidence=0.0,
                severity="low",
                evidence=[],
                blocked=False,
                reason=None,
                metadata={
                    "pre_check": "help_seeking",
                    "has_help": has_help,
                }
            )

        # Extreme suicide: "I want to die", "I am going to hang myself"
        if has_extreme or has_method_phrase or has_suicide_phrase:
            print(f"[Suicide] Pre-check: Extreme suicide detected - {text}")
            return ModerationResult(
                category="suicide",
                detected=True,
                confidence=1.0,
                severity="critical",
                evidence=["extreme_suicide"],
                blocked=True,
                reason="Suicide/self-harm detected",
                metadata={
                    "pre_check": True,
                    "has_extreme": has_extreme,
                    "has_suicide_phrase": has_suicide_phrase,
                    "has_method_phrase": has_method_phrase,
                }
            )

        # ============================================================
        # CONTINUE WITH NORMAL FLOW
        # ============================================================

        # Fast Scan
        features = self.scanner.scan(text)

        # Risk Calculation
        risk = self.calculator.calculate(features)

        print(
            f"[Suicide] Score: {risk.score}, "
            f"Should call LLM: {risk.should_call_llm}"
        )
        print(
            f"[Suicide] Matched keywords: "
            f"{risk.matched_keywords}"
        )
        print(
            f"[Suicide] Matched phrases: "
            f"{risk.matched_phrases}"
        )

        # Low Risk
        if not risk.should_call_llm:

            return ModerationResult(
                category="suicide",
                detected=False,
                confidence=0.0,
                severity="low",
                evidence=[],
                blocked=False,
                reason=None,
                metadata={
                    "risk_score": risk.score,
                    "threshold": risk.threshold,
                    "matched_keywords": risk.matched_keywords,
                    "matched_phrases": risk.matched_phrases,
                    "llm_called": False,
                },
            )

        # High Risk → LLM Verification
        classification, reason = self.engine.classify(text)

        print(
            f"[Suicide] Classification: "
            f"{classification}, Reason: {reason}"
        )

        detected = classification == "UNSAFE"

        # Severity
        if detected:
            severity = "critical"
            confidence = 1.0
        else:
            severity = "low"
            confidence = 0.60

        return ModerationResult(
            category="suicide",
            detected=detected,
            confidence=confidence,
            severity=severity,
            evidence=[],
            blocked=detected,
            reason=reason if detected else None,
            metadata={
                "risk_score": risk.score,
                "threshold": risk.threshold,
                "matched_keywords": risk.matched_keywords,
                "matched_phrases": risk.matched_phrases,
                "llm_called": True,
                "classification": classification,
            },
        )