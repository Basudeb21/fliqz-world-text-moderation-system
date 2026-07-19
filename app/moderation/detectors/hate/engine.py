# app/moderation/detectors/hate/engine.py

import requests

from app.config.settings import LLAMA_API_URL, LLAMA_MODEL
from app.prompts.hate_detection_prompt import HATE_SPEECH_PROMPT


SYSTEM_PROMPT = HATE_SPEECH_PROMPT


class HateSpeechEngine:

    MODEL = LLAMA_MODEL

    def classify(
        self,
        text: str,
    ) -> tuple[str, str]:

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

            print("[HateSpeech LLM]", repr(output))

            return self._parse(output)

        except Exception as e:

            print("[HateSpeech LLM Error]", e)

            return (
                "SAFE",
                "",
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

            reason = ""

            if len(lines) > 1:

                reason = lines[1].strip()

            return (
                "UNSAFE",
                reason,
            )

        return (
            "SAFE",
            "",
        )