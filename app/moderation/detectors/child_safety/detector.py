# app/moderation/detectors/child_safety/detector.py
from app.moderation.detectors.base import BaseDetector
from app.moderation.schemas.moderation_result import ModerationResult
from app.moderation.detectors.child_safety.engine import ChildSafetyEngine
from app.moderation.detectors.child_safety.scanner import ChildSafetyScanner
from app.moderation.detectors.child_safety.calculator import ChildSafetyRiskCalculator


class ChildSafetyDetector(BaseDetector):

    def __init__(self):
        super().__init__("child_safety")
        self.scanner = ChildSafetyScanner()
        self.calculator = ChildSafetyRiskCalculator()
        self.engine = ChildSafetyEngine()

    def analyze(self, text: str) -> ModerationResult:
        # Step 1: Scan for keywords and extract features
        features = self.scanner.scan(text)
        
        # Step 2: Calculate risk score
        risk = self.calculator.calculate(features)
        
        # Log the score for debugging
        print(f"[ChildSafety] Score: {risk.score}, Should call LLM: {risk.should_call_llm}")
        print(f"[ChildSafety] Matched keywords: {risk.matched_keywords}")
        
        # Step 3: If score >= threshold, call the LLM
        if risk.should_call_llm:
            classification, reason = self.engine.classify(text)
            print(f"[ChildSafety] Classification: {classification}, Reason: {reason}")
            
            # IMPORTANT: Set detected based on classification
            detected = classification.upper() == "UNSAFE"
            confidence = 1.0 if detected else 0.0
            severity = "critical" if detected else "low"
        else:
            classification = "SAFE"
            reason = f"Risk score {risk.score} below threshold {risk.threshold}"
            detected = False
            confidence = 0.0
            severity = "low"
        
        # Debug output
        print(f"[ChildSafety] Final: detected={detected}, severity={severity}")
        
        return ModerationResult(
            category="child_safety",
            detected=detected,  # This is now properly set
            confidence=confidence,
            severity=severity,
            evidence=risk.matched_keywords,
            blocked=detected,  # Block if detected
            reason=reason,
            metadata={
                "classification": classification,
                "risk_score": risk.score,
                "threshold": risk.threshold,
                "matched_keywords": risk.matched_keywords,
                "features": {
                    "age": features.age,
                    "minor": features.minor,
                    "sexual": features.sexual,
                    "grooming": features.grooming,
                    "meeting": features.meeting,
                    "relationship": features.relationship,
                    "coercion": features.coercion,
                    "first_person": features.first_person,
                    "negation": features.negation,
                }
            }
        )