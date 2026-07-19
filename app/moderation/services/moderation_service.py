# app/moderation/services/moderation_service.py

from app.db.dynamic_update import dynamic_update
from app.moderation.engine.moderation_engine import ModerationEngine
from app.moderation.schemas.moderation_response import ModerationResponse


class ModerationService:
    """
    Orchestrates the complete moderation workflow.

    Flow
    ----
    1. Extract text
    2. Normalize payload
    3. Mark Processing
    4. Run Moderation Engine
    5. Save Result
    6. Return Response

    No detector logic should exist here.
    """

    def __init__(self):

        self.engine = ModerationEngine()

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def process(
        self,
        raw_payload: dict,
    ) -> ModerationResponse:

        payload = self._normalize_payload(raw_payload)

        try:

            text = self._extract_text(raw_payload)

            self._set_processing(payload)

            moderation = self.engine.analyze(text)

            self._save_result(
                payload=payload,
                moderation=moderation,
            )

            return moderation

        except Exception:

            self._set_failed(payload)
            raise

    # --------------------------------------------------
    # Payload Helpers
    # --------------------------------------------------

    def _extract_text(
        self,
        raw_payload: dict,
    ) -> str:

        return (
            raw_payload
            .get("data", {})
            .get("text", "")
        )

    def _normalize_payload(
        self,
        raw_payload: dict,
    ) -> dict:

        return {

            "table_name": raw_payload.get("table"),

            "primary_key": "id",

            "key_value": raw_payload.get("id"),
        }

    # --------------------------------------------------
    # Status Updates
    # --------------------------------------------------

    def _set_processing(
        self,
        payload: dict,
    ):

        payload["ai_process_text_status"] = 2

        dynamic_update(payload)

    def _set_failed(
        self,
        payload: dict,
    ):

        payload["ai_process_text_status"] = 4

        dynamic_update(payload)

    # --------------------------------------------------
    # Save Moderation
    # --------------------------------------------------

    def _save_result(
        self,
        payload: dict,
        moderation: ModerationResponse,
    ):

        payload["ai_process_text_status"] = 3

        dynamic_update(
            payload=payload,
            moderation=moderation,
        )