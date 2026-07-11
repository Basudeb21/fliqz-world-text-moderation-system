# app/workers/text_moderation_worker.py

import ast
import json
import time

import redis

from app.config.settings import (
    REDIS_BRPOP_TIMEOUT,
    REDIS_DB,
    REDIS_HOST,
    REDIS_PORT,
    TEXT_QUEUE,
)
from app.moderation.services.moderation_service import ModerationService
from app.utils.logger import logger

# Redis Client
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,
)

# Service
service = ModerationService()

# Process Message
def process_redis_message(raw_payload: dict):

    text = raw_payload.get("data", {}).get("text", "")

    logger.info("─" * 60)
    logger.info("Message Received")
    logger.info(text)

    moderation = service.process(raw_payload)

    logger.info("========== MODERATION ==========")

    for result in moderation.results:

        logger.info(
            f"{result.category:<20}"
            f"Detected={result.detected} "
            f"Severity={result.severity}"
        )

    logger.info("--------------------------------")
    logger.info(f"Action     : {moderation.action}")
    logger.info(f"Blocked    : {moderation.blocked}")
    logger.info(f"Categories : {moderation.categories}")
    logger.info("================================")

    logger.info("✓ Processing Finished")
    logger.info("─" * 60)


# Worker Loop
def worker_loop():

    logger.info(
        f"🚀 Worker started - Listening on '{TEXT_QUEUE}'"
    )

    while True:

        try:

            item = r.blpop(TEXT_QUEUE, timeout=REDIS_BRPOP_TIMEOUT)

            if item is None:
                continue

            _, message = item

            try:

                payload = json.loads(message)

            except json.JSONDecodeError:

                try:

                    payload = ast.literal_eval(message)

                    logger.warning("Parsed Python dict payload")

                except Exception:

                    logger.warning("Invalid payload skipped")

                    continue

            process_redis_message(payload)

        except Exception:

            logger.exception("Worker crashed")

            time.sleep(1)


if __name__ == "__main__":

    worker_loop()