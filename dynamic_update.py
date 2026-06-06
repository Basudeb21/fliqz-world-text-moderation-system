# dynami_update.py
from datetime import datetime
from sqlalchemy import select, update, insert
from database import get_db
from dynamic_table_loader import get_dynamic_table


def dynamic_update(payload: dict, personal=False, minor=False, ai_reason=None):
    """
    Generic UPSERT (Update or Insert)
    Works for ANY table dynamically.
    """

    table_name = payload.get("table_name")
    pk_name = payload.get("primary_key")
    pk_value = payload.get("key_value")

    if not table_name or not pk_name or pk_value is None:
        return False, "Invalid payload structure"

    table = get_dynamic_table(table_name)

    db = next(get_db())
    now = datetime.now()

    try:
        # 🔍 Check if row exists
        stmt = select(table).where(table.c[pk_name] == pk_value)
        existing = db.execute(stmt).fetchone()

        # 🧱 Prepare common data
        data = {
            k: v for k, v in payload.items()
            if k not in ["table_name", "primary_key", "key_value"]
        and k in table.c
        }

        # 🔐 Personal details flag
        if "is_personal_details_detected" in table.c:
            data["is_personal_details_detected"] = 1 if personal else 0

        # 🚨 Minor safety flag
        if "is_minor_message_detected" in table.c:
            data["is_minor_message_detected"] = 1 if minor else 0

        # 🤖 AI moderation reason
        if "ai_reason" in table.c:
            data["ai_reason"] = ai_reason

        # 🔄 UPDATE
        if existing:
            if "updated_at" in table.c:
                data["updated_at"] = now

            stmt = (
                update(table)
                .where(table.c[pk_name] == pk_value)
                .values(data)
            )

            db.execute(stmt)
            db.commit()
            return True, "updated"

        # ➕ INSERT
        else:
            data[pk_name] = pk_value

            if "created_at" in table.c:
                data["created_at"] = now

            stmt = insert(table).values(data)

            db.execute(stmt)
            db.commit()
            return True, "inserted"

    except Exception as e:
        db.rollback()
        return False, str(e)

    finally:
        db.close()