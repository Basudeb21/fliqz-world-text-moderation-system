import requests

from app.config.settings import LLAMA_API_URL,LLAMA_MODEL
from app.prompts.minor_detection_prompt import MINOR_DETECT_PROMPT

SYSTEM_PROMPT = MINOR_DETECT_PROMPT


class ChildSafetyEngine:

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

            print("[ChildSafety LLM]", repr(output))

            return self._parse(output)

        except Exception as e:

            print("[ChildSafety LLM Error]", e)

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