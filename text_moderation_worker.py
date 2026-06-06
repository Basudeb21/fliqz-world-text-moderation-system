# text_moderation_worker.py
import redis
import json
import time

from dynamic_update import dynamic_update
from config import REDIS_HOST, REDIS_PORT, REDIS_DB, TEXT_QUEUE, REDIS_BRPOP_TIMEOUT
from detect_pii import detect_personal_info
from detect_child_safety import moderation_llama

# Redis client
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)


def normalize_payload(raw_payload: dict):
    """
    Convert Redis message format → DB expected format
    """
    inner = raw_payload.get("payload", {})

    return {
        "table_name": inner.get("table"),
        "primary_key": "id",
        "key_value": inner.get("id"),
        **inner.get("data", {})
    }


def process_redis_message(raw_payload: dict):

    text = (
        raw_payload.get("text")
        or raw_payload.get("message")
        or raw_payload.get("payload", {})
        .get("data", {})
        .get("text", "")
    )

    print("\n──────────────────────────────────────────────")
    print("🔍 Message received:", text)

    # -----------------------------------
    # Set status → 2 (Processing started)
    # -----------------------------------
    formatted_payload = normalize_payload(raw_payload)
    formatted_payload["ai_process_text_status"] = 2

    dynamic_update(formatted_payload)
    print("⚙️  Status set to 2 (Processing)")

    # -----------------------------------
    # 1. PII detection
    # -----------------------------------
    pii_flag = detect_personal_info(text)
    print("📄 PII detected:", pii_flag)

    # -----------------------------------
    # 2. Child safety moderation
    # -----------------------------------
    classification, reason = moderation_llama(text)
    minor_flag = (classification == "UNSAFE")
    print("🤖 Child-safety:", minor_flag)
    print("🧠 AI Reason:", reason)

    # -----------------------------------
    # Set status → 3 (Done) + final flags
    # -----------------------------------
    formatted_payload["ai_process_text_status"] = 3

    success, status = dynamic_update(
        formatted_payload,
        personal=pii_flag,
        minor=minor_flag,
        ai_reason=reason
    )

    if success:
        print(f"✅ DB operation successful: {status} | Status set to 3 (Done)")
    else:
        print(f"❌ DB operation FAILED: {status}")

    print("──────────────────────────────────────────────\n")



def worker_loop():
    print("🚀 Worker started — Listening on:", TEXT_QUEUE)

    while True:
        try:
            item = r.blpop(TEXT_QUEUE, timeout=REDIS_BRPOP_TIMEOUT)

            if not item:
                continue

            _, message = item

            try:
                payload = json.loads(message)
            except json.JSONDecodeError:
                print("⚠️ Invalid JSON:", message)
                continue

            process_redis_message(payload)

        except Exception as e:
            print(f"❌ Worker error: {e}")
            time.sleep(1)


if __name__ == "__main__":
    worker_loop()