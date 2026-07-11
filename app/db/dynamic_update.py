# app/db/dynamic_update.py
from datetime import datetime

from sqlalchemy import insert, select, update

from app.config.settings import DEBUG
from app.db.database import get_db
from app.db.dynamic_table_loader import get_dynamic_table
from app.moderation.config.database_mapping import DATABASE_FLAG_MAPPING
from app.moderation.schemas.moderation_response import ModerationResponse
from app.utils.logger import logger


def dynamic_update(
    payload: dict,
    moderation: ModerationResponse | None = None,
):
    """
    Generic UPSERT.

    Detector agnostic.
    Only understands ModerationResponse.
    """

    table_name = payload.get("table_name")
    pk_name = payload.get("primary_key")
    pk_value = payload.get("key_value")

    if not table_name or not pk_name or pk_value is None:
        return False, "Invalid payload structure"

    table = get_dynamic_table(table_name)

    if DEBUG:
        logger.debug(f"Dynamic Update -> Table={table_name}")
        logger.debug(f"Primary Key -> {pk_name}={pk_value}")

    db = next(get_db())
    now = datetime.now()

    try:

        stmt = select(table).where(table.c[pk_name] == pk_value)

        existing = db.execute(stmt).fetchone()

        data = {
            k: v
            for k, v in payload.items()
            if k not in (
                "table_name",
                "primary_key",
                "key_value",
            )
            and k in table.c
        }

        if moderation is not None:

            detector_results = {
                result.category: result
                for result in moderation.results
            }

            for detector_name, db_column in DATABASE_FLAG_MAPPING.items():

                if db_column not in table.c:
                    continue

                result = detector_results.get(detector_name)

                data[db_column] = (
                    1 if result and result.detected else 0
                )

            if "is_blocked" in table.c:
                data["is_blocked"] = (
                    1 if moderation.blocked else 0
                )

            if "ai_reason" in table.c:

                reasons = [
                    f"{result.category}: {result.reason}"
                    for result in moderation.results
                    if result.reason
                ]

                data["ai_reason"] = "\n".join(reasons)

        if "updated_at" in table.c:
            data["updated_at"] = now

        if DEBUG:
            logger.debug(f"Update Data: {data}")

        # ---------------- UPDATE ----------------

        if existing:

            stmt = (
                update(table)
                .where(table.c[pk_name] == pk_value)
                .values(data)
            )

            result = db.execute(stmt)

            db.commit()

            logger.info(
                f"Updated {table_name} ({pk_name}={pk_value}) "
                f"Rows={result.rowcount}"
            )

            return True, "updated"

        # ---------------- INSERT ----------------

        data[pk_name] = pk_value

        if "created_at" in table.c:
            data["created_at"] = now

        stmt = insert(table).values(data)

        result = db.execute(stmt)

        db.commit()

        logger.info(
            f"Inserted into {table_name} "
            f"({pk_name}={pk_value}) "
            f"Rows={result.rowcount}"
        )

        return True, "inserted"

    except Exception:

        db.rollback()

        logger.exception(
            f"Database update failed for "
            f"{table_name} ({pk_name}={pk_value})"
        )

        return False, "Database update failed"

    finally:

        db.close()