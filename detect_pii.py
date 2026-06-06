# detect_pii.py
import re

try:
    import pycountry
    PYCOUNTRY_AVAILABLE = True
except ImportError:
    PYCOUNTRY_AVAILABLE = False
    print("[PII] pycountry not installed — country name detection disabled. Run: pip install pycountry")

# Common Indian cities (expand as needed)
KNOWN_CITIES = {
    "mumbai", "delhi", "bangalore", "bengaluru", "hyderabad", "ahmedabad",
    "chennai", "kolkata", "pune", "jaipur", "lucknow", "kanpur", "nagpur",
    "indore", "thane", "bhopal", "visakhapatnam", "pimpri", "patna", "vadodara",
    "ghaziabad", "ludhiana", "agra", "nashik", "faridabad", "meerut", "rajkot",
    "kalyan", "vasai", "srinagar", "aurangabad", "dhanbad", "amritsar", "allahabad",
    "ranchi", "howrah", "coimbatore", "jabalpur", "gwalior", "vijayawada",
    "jodhpur", "madurai", "raipur", "kota", "guwahati", "chandigarh", "solapur",
    "hubballi", "mysore", "tiruchirappalli", "bareilly", "aligarh", "moradabad",
    "paris", "london", "new york", "new delhi", "dubai", "singapore", "tokyo",
    "berlin", "sydney", "toronto", "los angeles", "chicago", "houston",
}

def _build_country_names():
    if not PYCOUNTRY_AVAILABLE:
        return set()
    names = set()
    for c in pycountry.countries:
        names.add(c.name.lower())
        if hasattr(c, "common_name"):
            names.add(c.common_name.lower())
    return names

COUNTRY_NAMES = _build_country_names()


# --- Number word decoding ---
NUMBER_WORDS = {
    "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
    "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"
}
MULTIPLIER = {"double": 2, "triple": 3}

def decode_number_words(text: str) -> str:
    words = text.lower().split()
    digits = []
    i = 0
    while i < len(words):
        w = words[i]
        if w in MULTIPLIER and i + 1 < len(words) and words[i + 1] in NUMBER_WORDS:
            digits.append(NUMBER_WORDS[words[i + 1]] * MULTIPLIER[w])
            i += 2
            continue
        if w in NUMBER_WORDS:
            digits.append(NUMBER_WORDS[w])
        i += 1
    return "".join(digits)


# --- Email/obfuscation normalizer ---
def normalize_email_obfuscation(text: str) -> str:
    t = text.lower()
    for k, v in {" at ": "@", "(at)": "@", " dot ": ".", "(dot)": ".",
                 " underscore ": "_", " dash ": "-", " hyphen ": "-"}.items():
        t = t.replace(k, v)
    return t


# --- Regex patterns ---
EMAIL_RE    = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', re.I)
PHONE_RE    = re.compile(r'(\+?\d{1,3}[\s-]?)?(\d{10}|\d{3}[\s-]\d{3}[\s-]\d{4}|\(\d{3}\)\s*\d{3}[\s-]\d{4})')
CARD_RE     = re.compile(r'\b(?:\d[ -]*?){13,19}\b')
PINCODE_RE  = re.compile(r'\b\d{5,6}\b')
ADDRESS_KW  = re.compile(r'\b(flat|apartment|house|street|st\.|road|rd\.|lane|colony|nagar|sector|district|city|village|postal|pincode|zip)\b', re.I)
URL_RE      = re.compile(r'(https?:\/\/[^\s]+|www\.[^\s]+)', re.I)
LOCATION_PREFIX_RE = re.compile(
    r'\b(i live in|i stay in|i am from|i\'m from|i reside in|located in|based in|i am in|moving to|visiting)\s+([a-z ,]+)',
    re.I
)


def _contains_location_name(text: str) -> bool:
    """Check for city/country names, especially after location-intent phrases."""
    t_lower = text.lower()

    # Check for "I live in X" / "I'm from X" patterns
    for match in LOCATION_PREFIX_RE.finditer(t_lower):
        location_fragment = match.group(2).strip().rstrip(",.")
        # Check each word and pair of words in the fragment
        words = location_fragment.split()
        for i in range(len(words)):
            single = words[i]
            pair = " ".join(words[i:i+2]) if i + 1 < len(words) else None
            if single in KNOWN_CITIES or single in COUNTRY_NAMES:
                return True
            if pair and (pair in KNOWN_CITIES or pair in COUNTRY_NAMES):
                return True

    # Standalone word match (more conservative — only flag known cities)
    words = set(re.findall(r'\b[a-z]{3,}\b', t_lower))
    bigrams = set()
    word_list = re.findall(r'\b[a-z]{3,}\b', t_lower)
    for i in range(len(word_list) - 1):
        bigrams.add(f"{word_list[i]} {word_list[i+1]}")

    for name in KNOWN_CITIES:
        if name in words or name in bigrams:
            return True
    for name in COUNTRY_NAMES:
        if name in words or name in bigrams:
            return True

    return False


def detect_personal_info(text: str) -> bool:
    if not text:
        return False

    t = text.strip()
    normalized = normalize_email_obfuscation(t)
    numeric_string = decode_number_words(t)

    for c in [t, normalized, numeric_string]:
        if EMAIL_RE.search(c):
            return True
        if URL_RE.search(c):
            return True
        if PHONE_RE.search(c):
            return True
        if CARD_RE.search(c):
            return True

    if PINCODE_RE.search(t):
        return True
    if ADDRESS_KW.search(t):
        return True
    if len(numeric_string) >= 10:
        return True
    if _contains_location_name(t):
        return True

    return False