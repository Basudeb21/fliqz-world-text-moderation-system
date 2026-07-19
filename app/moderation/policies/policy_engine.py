# moderation/policies/policy_engine.py
from typing import List

from app.moderation.schemas.moderation_result import ModerationResult
from app.moderation.schemas.moderation_response import ModerationResponse

class PolicyEngine:

    def evaluate(
        self,
        results: List[ModerationResult]
    ) -> ModerationResponse:

        final_action = "ALLOW"

        blocked = False

        highest_severity = "none"

        categories = []

        for result in results:

            if result.detected:
                categories.append(result.category)

            if result.blocked:
                blocked = True
                final_action = "BLOCK"

            if (
                self._severity_value(result.severity)
                >
                self._severity_value(highest_severity)
            ):
                highest_severity = result.severity

        return ModerationResponse(

            blocked=blocked,

            action=final_action,

            highest_severity=highest_severity,

            categories=categories,

            results=results
        )

    @staticmethod
    def _severity_value(level: str) -> int:

        mapping = {

            "error": -1,

            "none": 0,

            "low": 1,

            "medium": 2,

            "high": 3,

            "critical": 4,
        }
       
        return mapping.get(level.lower(), 0)