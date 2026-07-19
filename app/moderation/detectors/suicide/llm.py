# app/moderation/detectors/suicide/llm.py
import requests

from app.config.settings import LLAMA_API_URL, LLAMA_MODEL
from app.prompts.suicide_detection_prompt import SUICIDE_DETECT_PROMPT

SYSTEM_PROMPT = SUICIDE_DETECT_PROMPT


def classify(text: str) -> tuple[str, str]:

    prompt = f"""
{SYSTEM_PROMPT}

Message:
{text}
"""

    payload = {
        "model": LLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "temperature": 0
    }

    response = requests.post(
        LLAMA_API_URL,
        json=payload,
        timeout=60,
    )

    response.raise_for_status()

    output = response.json()["response"].strip()

    print("[Suicide LLM]:", repr(output))

    if output.upper().startswith("SAFE"):
        return "SAFE", ""

    if output.upper().startswith("UNSAFE"):

        reason = output[6:].strip()

        return "UNSAFE", reason

    return "SAFE", ""