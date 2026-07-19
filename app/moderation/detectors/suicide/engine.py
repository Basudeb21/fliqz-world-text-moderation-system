# app/moderation/detectors/suicide/engine.py

import requests

from app.config.settings import LLAMA_API_URL, LLAMA_MODEL
from app.prompts.suicide_detection_prompt import SUICIDE_DETECT_PROMPT


class SuicideEngine:

    MODEL = LLAMA_MODEL

    def classify(
        self,
        text: str,
    ) -> tuple[str, str]:

        SYSTEM_PROMPT = SUICIDE_DETECT_PROMPT

        prompt = f"""
            {SYSTEM_PROMPT}

            Message:
            {text}
        """

        payload = {
            "model": self.MODEL,
            "prompt": prompt,
            "stream": False,
            "temperature": 0,
        }

        try:

            response = requests.post(
                LLAMA_API_URL,
                json=payload,
                timeout=60,
            )

            response.raise_for_status()
            output = response.json()["response"].strip()
            print("[Suicide LLM]", repr(output))

            return self._parse(output)

        except Exception as e:

            print("[Suicide LLM Error]", e)

            # Fail safe - better to flag than miss
            return (
                "UNSAFE",
                "Possible suicide content detected - requires human review",
            )

    def _parse(
        self,
        output: str,
    ) -> tuple[str, str]:

        output = output.strip()

        upper = output.upper()

        if upper.startswith("SAFE"):

            return (
                "SAFE",
                "",
            )

        if upper.startswith("UNSAFE"):
            lines = output.splitlines()
            if len(lines) > 1:
                reason = lines[1].strip()
            else:
                reason = ""

            return (
                "UNSAFE",
                reason,
            )

        # Unknown response - safe by default
        return (
            "SAFE",
            "",
        )