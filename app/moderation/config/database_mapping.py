# app/moderation/config/database_mapping.py
"""
Maps detector category -> database column.

Adding a new detector should only require adding
one entry here.
"""

DATABASE_FLAG_MAPPING = {

    "pii": "is_personal_details_detected",

    "child_safety": "is_minor_message_detected",

    # Future detectors

    # "suicide": "is_suicide_detected",

    # "hate": "is_hate_detected",

    # "spam": "is_spam_detected",

    # "violence": "is_violence_detected",

}