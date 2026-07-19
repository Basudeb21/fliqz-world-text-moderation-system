# app/moderation/detectors/dangerous_content/detector.py

from app.moderation.detectors.base import BaseDetector
from app.moderation.schemas.moderation_result import ModerationResult

from .scanner import DangerousContentScanner
from .calculator import DangerousContentRiskCalculator
from .engine import DangerousContentEngine

# Import from keywords
from .keywords import (
    SEXUAL_TERMS,
    THREAT_TERMS,
    DANGEROUS_KEYWORDS,
)


class DangerousContentDetector(BaseDetector):

    def __init__(self):

        super().__init__("dangerous_content")

        self.scanner = DangerousContentScanner()
        self.calculator = DangerousContentRiskCalculator()
        self.engine = DangerousContentEngine()

    def analyze(
        self,
        text: str,
    ) -> ModerationResult:

        text_lower = text.lower()
        
        # ============================================================
        # PRE-CHECK: Adult Sexual Content (Not Dangerous)
        # Uses imported SEXUAL_TERMS, THREAT_TERMS, DANGEROUS_KEYWORDS
        # ============================================================
        
        # Check what the text contains
        has_sexual = any(term in text_lower for term in SEXUAL_TERMS)
        has_threat = any(term in text_lower for term in THREAT_TERMS)
        has_dangerous_keyword = any(keyword in text_lower for keyword in DANGEROUS_KEYWORDS)
        
        # If it's sexual content WITHOUT threats AND WITHOUT dangerous keywords
        if has_sexual and not has_threat and not has_dangerous_keyword:
            print(f"[DangerousContent] Adult sexual content detected (no threats/danger) - ALLOWING")
            print(f"[DangerousContent] Text: {text}")
            
            return ModerationResult(
                category="dangerous_content",
                detected=False,
                confidence=0.0,
                severity="low",
                evidence=[],
                blocked=False,
                reason=None,
                metadata={
                    "pre_check": "adult_sexual_content_only",
                    "has_sexual": has_sexual,
                    "has_threat": has_threat,
                    "has_dangerous_keyword": has_dangerous_keyword,
                },
            )
        
        # ============================================================
        # CONTINUE WITH NORMAL SCANNING
        # ============================================================

        # ----------------------------------
        # Fast Risk Scan
        # ----------------------------------

        features = self.scanner.scan(text)

        risk = self.calculator.calculate(features, text)

        print(
            f"[DangerousContent] Score: {risk.score}, "
            f"Should call LLM: {risk.should_call_llm}"
        )

        print(
            f"[DangerousContent] Matched keywords: "
            f"{risk.matched_keywords}"
        )

        # ----------------------------------
        # Low Risk
        # ----------------------------------

        if not risk.should_call_llm:

            return ModerationResult(
                category="dangerous_content",
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

        # ----------------------------------
        # LLM Classification
        # ----------------------------------

        classification, reason = self.engine.classify(text)

        print(
            f"[DangerousContent] Classification: "
            f"{classification}, Reason: {reason}"
        )

        detected = classification == "UNSAFE"

        severity = (
            "critical"
            if detected
            else "low"
        )

        print(
            f"[DangerousContent] Final: "
            f"detected={detected}, severity={severity}"
        )

        return ModerationResult(
            category="dangerous_content",
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