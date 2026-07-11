# app/moderation/services/moderation_service.py

from app.db.dynamic_update import dynamic_update
from app.moderation.engine.moderation_engine import ModerationEngine
from app.moderation.schemas.moderation_response import ModerationResponse


class ModerationService:
    """
    Orchestrates the complete moderation workflow.

    Responsibilities
    ----------------
    1. Normalize incoming payload
    2. Update processing status
    3. Execute moderation engine
    4. Persist moderation results
    5. Return moderation response

    This class should contain NO detector logic.
    """

    def __init__(self):

        self.engine = ModerationEngine()

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def process(
        self,
        raw_payload: dict
    ) -> ModerationResponse:

        text = self._extract_text(raw_payload)

        payload = self._normalize_payload(raw_payload)

        # -----------------------------
        # Processing Started
        # -----------------------------

        self._set_processing(payload)

        # -----------------------------
        # Run Moderation
        # -----------------------------

        moderation = self.engine.analyze(text)

        # -----------------------------
        # Save Result
        # -----------------------------

        self._save_result(
            payload=payload,
            moderation=moderation
        )

        return moderation

    # --------------------------------------------------
    # Private Methods
    # --------------------------------------------------

    def _extract_text(
        self,
        raw_payload: dict
    ) -> str:

        return raw_payload.get(
            "data",
            {}
        ).get(
            "text",
            ""
        )

    def _normalize_payload(
        self,
        raw_payload: dict
    ) -> dict:

        return {

            "table_name": raw_payload.get("table"),

            "primary_key": "id",

            "key_value": raw_payload.get("id")
        }

    def _set_processing(
        self,
        payload: dict
    ):

        payload["ai_process_text_status"] = 2

        dynamic_update(payload)

    def _save_result(
        self,
        payload: dict,
        moderation: ModerationResponse
    ):

        payload["ai_process_text_status"] = 3

        dynamic_update(

            payload=payload,

            moderation=moderation
        )