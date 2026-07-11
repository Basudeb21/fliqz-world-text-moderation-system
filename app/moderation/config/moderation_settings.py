"""
Global moderation configuration.
"""
# Detector Enable / Disable
ENABLE_PII = True
ENABLE_CHILD_SAFETY = True
ENABLE_SUICIDE = True
ENABLE_SPAM = True
ENABLE_HATE = True
ENABLE_PROFANITY = True
ENABLE_SCAM = True
ENABLE_ADVERTISEMENT = True

# Blocking Rules
BLOCK_ON_PII = True
BLOCK_ON_CHILD_SAFETY = True
BLOCK_ON_SUICIDE = False
BLOCK_ON_SPAM = False
BLOCK_ON_HATE = True
BLOCK_ON_PROFANITY = False
BLOCK_ON_SCAM = True
BLOCK_ON_ADVERTISEMENT = False

# Engine Settings
# Number of detectors to execute simultaneously
MAX_WORKERS = 5

# Timeout (seconds) for a single detector
DETECTOR_TIMEOUT = 10

# Continue moderation even if one detector crashes
IGNORE_DETECTOR_ERRORS = True


# Logging
SHOW_DETECTOR_TIME = True
SHOW_ENGINE_TIME = True
SHOW_DEBUG_LOGS = True