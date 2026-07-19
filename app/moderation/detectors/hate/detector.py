# app/moderation/detectors/hate/detector.py

from app.moderation.detectors.base import BaseDetector
from app.moderation.schemas.moderation_result import ModerationResult

from .scanner import HateSpeechScanner
from .calculator import HateSpeechRiskCalculator
from .engine import HateSpeechEngine

from .keywords import (
    EXTREME_HATE_PATTERNS,
    DEHUMANIZING_TERMS,
    LGBTQ_TARGETS,
    DEROGATORY_TERMS,
    IDENTITY_TARGETS,
)


class HateSpeechDetector(BaseDetector):

    def __init__(self):

        super().__init__("hate_speech")

        self.scanner = HateSpeechScanner()
        self.calculator = HateSpeechRiskCalculator()
        self.engine = HateSpeechEngine()

    def analyze(
        self,
        text: str,
    ) -> ModerationResult:

        text_lower = text.lower()
        
        # ============================================================
        # PRE-CHECK: Extreme Hate Speech Patterns
        # ============================================================
        
        # Check for extreme patterns
        has_extreme = any(pattern in text_lower for pattern in EXTREME_HATE_PATTERNS)
        has_identity = any(target in text_lower for target in IDENTITY_TARGETS)
        has_dehumanizing = any(term in text_lower for term in DEHUMANIZING_TERMS)
        
        # Extreme hate speech: "Kill all the Jews"
        if has_extreme and has_identity:
            print(f"[HateSpeech] Pre-check: Extreme hate speech - {text}")
            return ModerationResult(
                category="hate_speech",
                detected=True,
                confidence=1.0,
                severity="critical",
                evidence=["extreme_hate_speech"],
                blocked=True,
                reason="Extreme hate speech detected",
                metadata={
                    "pre_check": True,
                    "has_extreme": has_extreme,
                    "has_identity": has_identity,
                }
            )
        
        # Dehumanizing hate speech: "Immigrants are vermin"
        if has_dehumanizing and has_identity:
            print(f"[HateSpeech] Pre-check: Dehumanizing hate speech - {text}")
            return ModerationResult(
                category="hate_speech",
                detected=True,
                confidence=1.0,
                severity="critical",
                evidence=["dehumanizing_hate_speech"],
                blocked=True,
                reason="Dehumanizing hate speech detected",
                metadata={
                    "pre_check": True,
                    "has_dehumanizing": has_dehumanizing,
                    "has_identity": has_identity,
                }
            )
        
        # Anti-trans/LGBTQ+ hate: "Transgender people are mentally ill"
        has_lgbtq = any(target in text_lower for target in LGBTQ_TARGETS)
        has_derogatory = any(term in text_lower for term in DEROGATORY_TERMS)
        
        if has_lgbtq and has_derogatory:
            print(f"[HateSpeech] Pre-check: LGBTQ+ hate speech - {text}")
            return ModerationResult(
                category="hate_speech",
                detected=True,
                confidence=1.0,
                severity="critical",
                evidence=["lgbtq_hate_speech"],
                blocked=True,
                reason="LGBTQ+ hate speech detected",
                metadata={
                    "pre_check": True,
                    "has_lgbtq": has_lgbtq,
                    "has_derogatory": has_derogatory,
                }
            )
        
        # ============================================================
        # CONTINUE WITH NORMAL FLOW
        # ============================================================

        # Fast Risk Scan
        features = self.scanner.scan(text)
        risk = self.calculator.calculate(features)

        print(
            f"[HateSpeech] Score: {risk.score}, "
            f"Should call LLM: {risk.should_call_llm}"
        )

        print(
            f"[HateSpeech] Matched keywords: "
            f"{risk.matched_keywords}"
        )

        # Low Risk
        if not risk.should_call_llm:

            return ModerationResult(
                category="hate_speech",
                detected=False,
                confidence=0.0,
                severity="low",
                evidence=[],
                blocked=False,
                reason=None,
                metadata={
                    "risk_score": risk.score,
                    "matched_keywords": risk.matched_keywords,
                    "llm_called": False,
                },
            )

        # LLM
        classification, reason = self.engine.classify(text)

        print(
            f"[HateSpeech] Classification: "
            f"{classification}, Reason: {reason}"
        )

        detected = classification == "UNSAFE"

        severity = (
            "critical"
            if detected
            else "low"
        )

        print(
            f"[HateSpeech] Final: "
            f"detected={detected}, severity={severity}"
        )

        return ModerationResult(
            category="hate_speech",
            detected=detected,
            confidence=1.0 if detected else 0.5,
            severity=severity,
            evidence=[],
            blocked=detected,
            reason=reason,
            metadata={
                "risk_score": risk.score,
                "matched_keywords": risk.matched_keywords,
                "llm_called": True,
                "classification": classification,
            },
        )