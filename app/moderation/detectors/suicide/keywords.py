# app/moderation/detectors/suicide/keywords.py

"""
Suicide / Self-Harm keyword dictionaries.

The scanner only extracts features.
It DOES NOT classify messages.

Each category represents one signal that contributes
to the overall suicide risk score.
"""

# Death related
DEATH_WORDS = {
    "die", "dead", "death", "dying", "suicide", "suicidal",
    "deceased", "kill myself", "end it", "end it all",
    "end my life", "take my life", "take my own life",
}

# Self Harm
SELF_HARM_WORDS = {
    "cut", "cutting", "blade", "bleeding", "blood",
    "hang", "hanging", "rope", "noose",
    "overdose", "poison", "poisoning",
    "jump", "jumping", "burn", "burning",
    "stab", "stabbing", "hurt", "harm",
    "injure", "injury", "wound", "wounding",
    "slit", "slash", "pierce", "wrist",
}

# Intent
INTENT_WORDS = {
    "want", "wanna", "wish", "wished",
    "planning", "plan", "planned", "plans",
    "decided", "decide", "deciding",
    "gonna", "going", "going to",
    "ready", "prepared", "preparing",
    "think", "thinking", "thought",
    "consider", "considering", "contemplate",
    "will", "would", "need", "have to",
}

# First Person
FIRST_PERSON_WORDS = {
    "i", "me", "my", "myself", "mine",
    "we", "us", "our", "ourselves",
}

# Hopeless Emotion
EMOTION_WORDS = {
    "hopeless", "worthless", "useless", "helpless",
    "alone", "lonely", "empty", "broken",
    "depressed", "depression", "sad", "sadness",
    "cry", "crying", "tears", "sobbing",
    "pain", "suffering", "suffer", "hurting",
    "tired", "exhausted", "drained", "numb",
    "trapped", "stuck", "lost", "confused",
    "desperate", "despair", "anguish", "misery",
    "hopelessness", "despair", "grief",
}

# Farewell
FAREWELL_WORDS = {
    "bye", "goodbye", "farewell", "goodnight",
    "final goodbye", "last goodbye", "see you later",
    "take care", "take care of yourself",
    "good night", "bye bye", "later",
}

# Time Indicators
TIME_WORDS = {
    "today", "tonight", "tomorrow", "soon", "now", "later",
    "immediately", "right now", "asap", "in a few",
    "this week", "this weekend", "tonight",
    "after", "before", "when", "while",
}

# Suicide Methods
METHOD_WORDS = {
    "knife", "gun", "bridge", "building",
    "train", "railway", "pills", "pill",
    "rope", "poison", "blade", "car",
    "overdose", "drugs", "medication",
    "razor", "scissors", "sharp object",
    "gunshot", "cutting", "hanging",
}

# Negation
NEGATION_WORDS = {
    "not", "never", "dont", "don't",
    "isnt", "isn't", "won't", "wont",
    "no", "cannot", "can't", "wouldn't",
    "shouldn't", "couldn't", "didn't",
}

# ============================================================
# STRONG SUICIDE PHRASES (for phrase matching)
# ============================================================

SUICIDE_PHRASES = {
    "want to die", "want to kill myself", "kill myself",
    "end my life", "take my life", "take my own life",
    "don't want to live", "do not want to live",
    "wish i was dead", "i want to die", "i want to disappear",
    "i want to end it", "end it all", "better off dead",
    "no reason to live", "can't go on", "cannot go on",
    "i give up", "i've given up", "want to end it all",
    "i want to sleep forever", "never wake up",
}

METHOD_PHRASES = {
    "jump off bridge", "jump off a bridge", "jump from bridge",
    "hang myself", "hanging myself", "hang from",
    "cut myself", "cutting myself", "cut my wrist", "slit my wrist",
    "take pills", "overdose", "overdose myself",
    "drink poison", "shoot myself", "shooting myself",
    "stab myself", "stab myself", "hurt myself",
}

FAREWELL_PHRASES = {
    "goodbye everyone", "bye everyone", "this is goodbye",
    "last goodbye", "final goodbye", "goodbye world",
    "goodbye my", "goodbye all",
}

HELP_SEEKING_PHRASES = {
    "need help", "need support", "need to talk",
    "looking for help", "seeking help", "asking for help",
    "help me", "please help", "i need help",
    "crisis", "hotline", "helpline", "emergency",
    "i need someone", "i need to talk to someone",
}

# ============================================================
# EXTREME SUICIDE PATTERNS (for pre-check)
# ============================================================

EXTREME_SUICIDE_PATTERNS = {
    "i want to die", "i want to kill myself",
    "i am going to kill myself", "i'm going to kill myself",
    "i am going to die", "i'm going to die",
    "i am going to end it", "i'm going to end it",
    "i am going to end my life", "i'm going to end my life",
    "i am going to hang myself", "i'm going to hang myself",
    "i am going to cut myself", "i'm going to cut myself",
    "i am planning to", "i'm planning to",
    "i decided to", "i've decided to",
}