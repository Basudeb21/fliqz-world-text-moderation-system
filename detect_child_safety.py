# detect_child_safety.py

import requests

LLAMA_URL = "http://localhost:11434/api/chat"
LLAMA_MODEL = "llama3.2:latest"
TIMEOUT = 60


def moderation_llama(text: str) -> tuple[str, str]:

    prompt = f"""You are a strict content moderation system.

Classify the message as either SAFE or UNSAFE.

RULES:
[keep your existing rules...]

CRITICAL OUTPUT FORMAT:
Respond with ONLY two lines, no exceptions:

LINE 1: Either the single word SAFE or the single word UNSAFE
LINE 2: A one-sentence reason

Example outputs:
UNSAFE
Message mentions 13-year-old with sexual intent

SAFE
No minors mentioned in text

DO NOT add any other text, markdown, punctuation, or formatting.

Message: "{text}"

Response:"""

    try:

        resp = requests.post(
            LLAMA_URL,
            json={
                "model": LLAMA_MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False
            },
            timeout=TIMEOUT
        )

        resp.raise_for_status()

        raw = resp.json()["message"]["content"].strip()

        print(f"[LLaMA raw]: {repr(raw)}")

        # -----------------------------
        # Parse model response
        # -----------------------------

        lines = raw.split("\n")

        classification = (
            lines[0]
            .strip()
            .upper()
            .replace(":", "")
            .replace("-", "")
            .strip()
        )

        reason = (
            lines[1].strip()
            if len(lines) > 1
            else "No reason provided"
        )

        # -----------------------------
        # Exact classification check
        # -----------------------------

        if classification == "UNSAFE":
            return ("UNSAFE", reason)

        elif classification == "SAFE":
            return ("SAFE", reason)

        else:

            print(
                f"[LLaMA] Unexpected response format: {repr(raw)}"
            )

            return (
                "UNSAFE",
                "Unexpected response format, defaulting to UNSAFE"
            )

    except requests.exceptions.ConnectionError:

        print(
            "[LLaMA] Connection refused — is Ollama running?"
        )

        return (
            "UNSAFE",
            "Connection error - defaulting to UNSAFE"
        )

    except requests.exceptions.Timeout:

        print(
            f"[LLaMA] Request timed out after {TIMEOUT}s"
        )

        return (
            "UNSAFE",
            "Timeout error - defaulting to UNSAFE"
        )

    except Exception as e:

        print(f"[LLaMA] Unexpected error: {e}")

        return (
            "UNSAFE",
            f"Error occurred: {str(e)}"
        )


if __name__ == "__main__":

    tests = [

        "I am 13 years old and want sex",

        "Can I meet a school girl tonight?",

        "Hey what's up?",

        "Lost in the moment, glowing with confidence and happiness ✨"

    ]

    for t in tests:

        result, reason = moderation_llama(t)

        print("=" * 60)
        print(f"Text   : {t}")
        print(f"Result : {result}")
        print(f"Reason : {reason}")