"""
Global moderation configuration.
"""

# ==========================================================
# Detector Enable / Disable
# ==========================================================

ENABLE_PII = True
ENABLE_CHILD_SAFETY = True
ENABLE_SUICIDE = True
ENABLE_HATE = True
ENABLE_DANGEROUS_CONTENT = True


# ==========================================================
# Blocking Rules
# ==========================================================

BLOCK_ON_PII = True
BLOCK_ON_CHILD_SAFETY = True
BLOCK_ON_SUICIDE = False
BLOCK_ON_HATE = True
BLOCK_ON_DANGEROUS_CONTENT = True


# ==========================================================
# Engine Settings
# ==========================================================

# Number of detectors executed simultaneously
MAX_WORKERS = 5

# Timeout (seconds) for each detector
DETECTOR_TIMEOUT = 10

# Continue moderation if one detector crashes
IGNORE_DETECTOR_ERRORS = True


# ==========================================================
# Logging
# ==========================================================

SHOW_DETECTOR_TIME = True
SHOW_ENGINE_TIME = True
SHOW_DEBUG_LOGS = True