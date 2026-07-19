# app/moderation/detectors/child_safety/keywords.py
"""
Keyword groups used by the fast risk scanner.

These keywords DO NOT determine whether content is unsafe.
They only produce a risk score.

If the score crosses the threshold,
the message is sent to the LLM for final moderation.
"""

# ---------------------------------------
# Age Indicators
# ---------------------------------------

AGE_WORDS = {
    # Age numbers (as words and digits)
    "young", "youth", "child", "children", "kid", "kids", 
    "teen", "teenager", "adolescent", "minor", "underage",
    "little", "small", "boy", "girl", "boys", "girls",
    # Specific ages
    "eight", "nine", "ten", "eleven", "twelve", "thirteen", 
    "fourteen", "fifteen", "sixteen", "seventeen", 
    "eighteen", "nineteen", "twenty", "twenty-one",
    "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18",
    "age", "aged", "years", "year-old", "yr", "yrs",
    "childhood", "juvenile", "underage", "minor", "youngster",
}

# ---------------------------------------
# Minor References
# ---------------------------------------

MINOR_WORDS = {
    "minor", "minors", "underage", "under-age",
    "child", "children", "kid", "kids", "little one", "little ones",
    "teen", "teens", "teenager", "teenagers", "adolescent", "adolescents",
    "youth", "youngster", "youngsters", "young person", "young people",
    "girl", "girls", "boy", "boys", "toddler", "toddlers",
    "infant", "infants", "baby", "babies", "childhood",
    "school-age", "school-aged", "elementary", "middle-school",
    "high-school", "pre-teen", "preteen", "tween", "tweens",
    "juvenile", "juveniles", "pubescent", "young adult", "young adults",
    "under-18", "under 18", "under eighteen",
}

# ---------------------------------------
# Sexual References
# ---------------------------------------

SEXUAL_WORDS = {
    # Explicit sexual terms
    "sex", "sexual", "sexy", "explicit", "nude", "naked",
    "porn", "porno", "pornography", "xxx", "adult content",
    "genital", "genitals", "penis", "vagina", "breast", "breasts",
    "nipple", "nipples", "butt", "buttocks", "ass", "booty",
    "intercourse", "sexually", "erotic", "erotica", "kinky",
    "bdsm", "fetish", "fetishes", "masturbate", "masturbation",
    "orgasm", "orgasms", "climax", "ejaculate", "ejaculation",
    
    # Sexual acts
    "blowjob", "oral", "anal", "vaginal", "penetration",
    "fuck", "fucking", "suck", "sucking", "dick", "cock",
    "pussy", "cunt", "tits", "boobs", "whore", "slut",
    
    # Grooming/sexualization
    "molest", "molestation", "molesting", "rape", "raping",
    "assault", "abuse", "sexualize", "sexualizing", "objectify",
    "exploit", "exploitation", "lewd", "lascivious", "indecent",
    "perv", "pervert", "pedophile", "pedo", "predator",
}

# ---------------------------------------
# Grooming Indicators
# ---------------------------------------

GROOMING_WORDS = {
    # Manipulation tactics
    "trust", "trusted", "trusting", "confide", "confidential",
    "secret", "secrets", "special", "special friend", "best friend",
    "promise", "promises", "private", "between us", "our secret",
    "don't tell", "nobody knows", "keep between", "just us",
    
    # Compliments/attention
    "beautiful", "handsome", "pretty", "cute", "gorgeous",
    "attractive", "hot", "sexy", "mature", "grown-up",
    "special", "unique", "different", "smart", "intelligent",
    "understanding", "mature for your age", "wise beyond",
    
    # Relationship building
    "understand", "care", "listening", "listen", "support",
    "supportive", "comfort", "comfortable", "protect", "protector",
    "guide", "mentor", "mentoring", "role model",
    "friendship", "bond", "connection", "trustworthy",
    
    # Isolation tactics
    "nobody understands", "they don't get", "against us",
    "others don't", "world against", "we're alike",
    "you're different", "special bond", "unique connection",
    
    # Grooming actions
    "groom", "grooming", "groomed", "manipulate", "manipulating",
    "coach", "coaching", "train", "training", "prepare", "preparing",
    "lure", "luring", "entice", "enticing", "seduce", "seducing",
}

# ---------------------------------------
# Meeting / Contact
# ---------------------------------------

MEETING_WORDS = {
    # Direct meeting requests
    "meet", "meeting", "meet up", "meetup", "hang", "hanging",
    "hangout", "hang out", "get together", "see", "seeing",
    "meet in person", "meet physically", "face to face",
    "in-person", "in person", "real life", "irl",
    
    # Places to meet
    "park", "mall", "store", "restaurant", "cafe", "coffee",
    "house", "home", "apartment", "place", "spot", "location",
    "hotel", "motel", "cinema", "movies", "theater",
    
    # Transportation
    "pick up", "pickup", "drive", "take you", "bring you",
    "get you", "come get", "come over", "visit", "visiting",
    "travel", "trip", "go together", "ride", "transport",
    
    # Communication for meetings
    "call", "text", "message", "dm", "direct message",
    "phone", "mobile", "cell", "whatsapp", "snapchat",
    "instagram", "facebook", "social media", "contact",
    
    # Time/arrangements
    "tonight", "tomorrow", "this weekend", "later", "soon",
    "after school", "when free", "available", "busy",
    "schedule", "arrange", "planning to",
}

# ---------------------------------------
# Relationship Terms
# ---------------------------------------

RELATIONSHIP_WORDS = {
    # Relationship types
    "relationship", "relationships", "dating", "date",
    "boyfriend", "girlfriend", "partner", "couple",
    "lover", "love", "loving", "romance", "romantic",
    "intimate", "intimacy", "affection", "affectionate",
    
    # Emotional language
    "love", "like", "adore", "cherish", "care", "caring",
    "need", "want", "desire", "passion", "passionate",
    "connection", "bond", "attachment", "attached",
    
    # Status
    "single", "available", "taken", "crush", "crushing",
    "flirt", "flirting", "flirtatious", "attracted", "attraction",
    
    # Future/plans
    "future", "together", "commitment", "commit",
    "relationship goals", "soulmate", "perfect for",
    "just right", "made for", "meant to be",
}

# ---------------------------------------
# Coercion / Pressure
# ---------------------------------------

COERCION_WORDS = {
    # Direct coercion
    "must", "have to", "need to", "should", "better",
    "required", "obligated", "supposed to", "forced",
    "force", "forcing", "make", "making", "compel", "compelling",
    
    # Pressure tactics
    "if you love me", "if you care", "prove your love",
    "prove you love", "show me", "demonstrate", "worth",
    "deserve", "earn", "trust me", "believe me",
    
    # Threats/ultimatums
    "or else", "otherwise", "consequences", "bad things",
    "won't happen", "will happen", "never", "always",
    "you better", "you'd better", "do this or",
    
    # Manipulation
    "don't be scared", "don't worry", "nothing wrong",
    "it's fine", "it's okay", "normal", "everyone does",
    "not a big deal", "you'll like it", "you'll enjoy",
    
    # Persuasion
    "convince", "convincing", "persuade", "persuading",
    "tempt", "tempting", "encourage", "encouraging",
    "push", "pushing", "pressure", "pressuring",
}

# ---------------------------------------
# First Person
# ---------------------------------------

FIRST_PERSON = {
    "i", "me", "my", "myself",
    "i'm", "i'll", "i'd", "i've",
    "mine", "we", "us", "our", "ourselves",
    "we're", "we'll", "we've", "we'd",
}

# ---------------------------------------
# Negation
# ---------------------------------------

NEGATION_WORDS = {
    "not", "never", "no", "don't", "dont", 
    "doesn't", "doesnt", "isn't", "isnt", 
    "aren't", "arent", "wasn't", "wasnt",
    "weren't", "werent", "won't", "wont",
    "wouldn't", "wouldnt", "shouldn't", "shouldnt",
    "couldn't", "couldnt", "can't", "cant",
    "didn't", "didnt", "hasn't", "hasnt",
    "haven't", "havent", "hadn't", "hadnt",
    "neither", "nor", "none", "nobody", "no one",
    "nothing", "nowhere", "hardly", "scarcely", "barely",
}

# ---------------------------------------
# Additional Context Words (for better detection)
# ---------------------------------------

CONTEXT_WORDS = {
    # Words that might indicate roleplay or hypothetical scenarios
    "roleplay", "rp", "pretend", "imaginary", "fake",
    "fictional", "character", "story", "writing", "fanfic",
    
    # Words that might indicate educational context
    "educational", "learning", "teaching", "lesson", "curriculum",
    "school", "health", "safety", "awareness", "prevention",
    
    # Words that might indicate reporting/help-seeking
    "report", "reporting", "help", "helpline", "advice",
    "support", "resources", "crisis", "emergency",
}