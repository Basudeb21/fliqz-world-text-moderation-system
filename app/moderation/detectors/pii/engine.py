# detect_pii.py
"""
Enhanced PII detection for raw text with improved address detection
"""
import re

try:
    import pycountry
    PYCOUNTRY_AVAILABLE = True
except ImportError:
    PYCOUNTRY_AVAILABLE = False
    print("[PII] pycountry not installed — country name detection disabled. Run: pip install pycountry")

# ============ ADDRESS DETECTION KEYWORDS ============
# Apartment/Unit keywords
APARTMENT_KEYWORDS = {
    "flat", "apartment", "apt", "suite", "unit", "room", 
    "building", "tower", "block", "residence", "residency",
    "floor", "bungalow", "villa", "condo", "townhouse",
    "rowhouse", "manor", "estate", "chamber", "hall"
}

# Street/road keywords
STREET_KEYWORDS = {
    "street", "st", "road", "rd", "lane", "ln", "avenue", "ave",
    "boulevard", "blvd", "drive", "dr", "court", "ct", "way",
    "parkway", "pkwy", "terrace", "ter", "highway", "hwy",
    "close", "crescent", "cres", "place", "pl", "square", "sq",
    "sector", "phase", "colony", "village", "vill", "po", "ps",
    "nagar", "extension", "extn", "layout", "l/o", "complex",
    "commercial", "residential", "housing", "society"
}

# Postal/address markers
POSTAL_MARKERS = {
    "post", "postal", "pincode", "zip", "zipcode", "pin"
}

# Common Indian cities (for reference only, not used for address detection)
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


# ============ ENHANCED ADDRESS DETECTION ============

def _is_zip_code(text: str) -> bool:
    """
    Check if text contains a valid postal/ZIP code format.
    Supports: US ZIP (10001, 10001-1234), UK (NW1 6XE, SW1A 2AA),
    Canada (M5B 2L7), India (700091), Australia (2000)
    """
    text = text.strip()
    
    # US ZIP: 5 digits or 5-4 digits
    if re.search(r'\b\d{5}(?:-\d{4})?\b', text):
        return True
    
    # UK Postcode: e.g., NW1 6XE, SW1A 2AA, EC1A 1BB
    if re.search(r'\b[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}\b', text, re.IGNORECASE):
        return True
    
    # Canada Postcode: e.g., M5B 2L7
    if re.search(r'\b[A-Z]\d[A-Z] \d[A-Z]\d\b', text, re.IGNORECASE):
        return True
    
    # India PIN: 6 digits
    if re.search(r'\b\d{6}\b', text):
        return True
    
    # Australia Postcode: 4 digits
    if re.search(r'\b\d{4}\b', text):
        return True
    
    return False

def _is_address_with_components(text: str) -> tuple:
    """
    Enhanced address detection using multiple components.
    Returns (is_address, confidence_score, detected_components)
    """
    text_lower = text.lower().strip()
    
    # Check for standalone city/country names that are NOT addresses
    standalone_cities = {"london", "new york", "california", "india", "west bengal", 
                         "toronto", "sydney", "paris", "berlin", "tokyo", "dubai",
                         "singapore", "mumbai", "delhi", "kolkata", "bangalore"}
    
    # If text is just a single word or short phrase and it's a city name, reject
    if len(text.split()) <= 3:
        for city in standalone_cities:
            if city in text_lower:
                return False, 0.0, []
    
    # Split into lines for multiline address detection
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines:
        lines = [text.strip()]
    
    # Detect components
    has_apartment = False
    has_street = False
    has_house_number = False
    has_zip = False
    has_city_state = False
    
    detected_components = []
    full_address_lines = []
    
    # Check each line for address components
    for line in lines:
        line_lower = line.lower()
        line_components = []
        
        # 1. Check for house number (any digit sequence that looks like a house number)
        # House numbers: 123, 123A, 12-4, A-302, 221B, etc.
        if re.search(r'\b\d+[A-Z]?\b|\b[A-Z]-\d+\b|\b\d+-\d+\b', line):
            has_house_number = True
            line_components.append("house_number")
        
        # 2. Check for apartment keywords
        if any(kw in line_lower for kw in APARTMENT_KEYWORDS):
            has_apartment = True
            line_components.append("apartment")
        
        # 3. Check for street keywords
        # Match exact street keywords as whole words
        street_pattern = r'\b(?:' + '|'.join(re.escape(kw) for kw in STREET_KEYWORDS) + r')\b'
        if re.search(street_pattern, line_lower):
            has_street = True
            line_components.append("street")
        
        # 4. Check for ZIP/postal code patterns
        if _is_zip_code(line):
            has_zip = True
            line_components.append("zip_code")
        
        # 5. Check for city/state/country (but only as part of larger address)
        if len(line) > 5 and not any(kw in line_lower for kw in standalone_cities):
            # Simple city/state detection for raw text (without spaCy)
            # Look for patterns like "City, State" or "City, Country"
            if re.search(r'\b[a-z]{3,}\s*,\s*[a-z]{3,}\b', line_lower):
                has_city_state = True
                line_components.append("location")
        
        if line_components:
            full_address_lines.append(line)
            detected_components.extend(line_components)
    
    # Calculate confidence score
    score = 0.0
    total_lines = len(lines)
    
    # We need at least 2 components to consider it an address
    unique_components = set(detected_components)
    
    # Weighted scoring
    if has_house_number:
        score += 30
    if has_apartment:
        score += 25
    if has_street:
        score += 30
    if has_zip:
        score += 25
    if has_city_state:
        score += 15
    
    # Bonus: Multiple lines with address components
    if total_lines >= 2 and len(full_address_lines) >= 2:
        score += 20
    
    # Penalty: If it's just a single city name with no other components
    if len(unique_components) == 1 and has_city_state and not any([has_house_number, has_street, has_zip, has_apartment]):
        score = 0
    
    # Is it an address? Require at least 2 components and confidence > 50
    is_address = (len(unique_components) >= 2 and score >= 50) or (has_house_number and has_street)
    
    return is_address, score, list(unique_components)

def extract_addresses(text: str) -> list:
    """
    Extract complete addresses from text.
    Returns list of address strings.
    """
    if not text:
        return []
    
    # Split into lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines:
        lines = [text]
    
    addresses = []
    current_address = []
    
    for line in lines:
        is_addr, _, _ = _is_address_with_components(line)
        if is_addr or _is_zip_code(line):
            current_address.append(line)
        else:
            # Check if line has address markers
            line_lower = line.lower()
            has_marker = any(kw in line_lower for kw in APARTMENT_KEYWORDS) or \
                         any(kw in line_lower for kw in STREET_KEYWORDS) or \
                         any(marker in line_lower for marker in POSTAL_MARKERS)
            if has_marker:
                current_address.append(line)
            else:
                # If we have accumulated an address, save it
                if current_address:
                    full_addr = "\n".join(current_address)
                    # Validate it's a complete address
                    is_valid, _, _ = _is_address_with_components(full_addr)
                    if is_valid:
                        addresses.append(full_addr)
                    current_address = []
    
    # Don't forget the last address
    if current_address:
        full_addr = "\n".join(current_address)
        is_valid, _, _ = _is_address_with_components(full_addr)
        if is_valid:
            addresses.append(full_addr)
    
    # If no multiline address found, check the whole text
    if not addresses:
        is_addr, _, _ = _is_address_with_components(text)
        if is_addr:
            addresses.append(text)
    
    return addresses

def has_address(text: str) -> bool:
    """
    Enhanced address detection using multiple components.
    Returns True if the text contains a complete address.
    """
    if not text or len(text.strip()) < 10:
        return False
    
    is_addr, score, components = _is_address_with_components(text)
    
    # Log for debugging
    if is_addr:
        print(f"[ADDRESS] Detected: score={score}, components={components}")
    
    return is_addr


# ============ ORIGINAL FUNCTIONS (Preserved) ============

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

# Location prefix patterns - expanded to catch more but with stricter validation
LOCATION_PREFIX_RE = re.compile(
    r'\b(i live in|i stay in|i am from|i\'m from|i reside in|located in|based in|i am in|moving to|visiting|from)\s+([a-z ,]+)',
    re.I
)


def _contains_location_name(text: str) -> bool:
    """
    Check for city/country names, especially after location-intent phrases.
    STRICTER: Only returns True if it's clearly a location mention.
    """
    t_lower = text.lower()
    
    # Check for "I live in X" / "I'm from X" patterns
    for match in LOCATION_PREFIX_RE.finditer(t_lower):
        location_fragment = match.group(2).strip().rstrip(",.")
        # Only consider if the fragment is short (likely just a city/country name)
        words = location_fragment.split()
        if len(words) <= 3:  # Short phrase like "London" or "New York"
            # Check each word in the fragment
            for single in words:
                if single in KNOWN_CITIES:
                    # But only if it's NOT part of a larger address
                    return False  # Don't flag standalone location mentions
        else:
            # Longer fragment - might be an address, but we'll let address detection handle it
            # Check if it has address components
            has_street = any(kw in location_fragment for kw in STREET_KEYWORDS)
            has_number = re.search(r'\b\d+', location_fragment)
            if has_street and has_number:
                return True  # This is actually an address
    
    # Standalone city/country names - DO NOT flag these
    # Return False for any single city/country mention
    words = set(re.findall(r'\b[a-z]{3,}\b', t_lower))
    for name in KNOWN_CITIES:
        if name in words:
            # Check if it's part of a longer address
            # If the text is just "London" or "I live in London", it's NOT an address
            if len(words) <= 2:  # Very short text
                return False
    
    return False


# ============ MAIN DETECTION FUNCTION ============

def detect_personal_info(text: str) -> bool:
    """
    Enhanced PII detection with improved address detection.
    Detects: email, phone, URL, credit card, PIN code, number words, and addresses.
    """
    if not text:
        return False

    t = text.strip()
    normalized = normalize_email_obfuscation(t)
    numeric_string = decode_number_words(t)

    # ============ Check for clear PII types first ============
    for c in [t, normalized, numeric_string]:
        if EMAIL_RE.search(c):
            print(f"[PII] Email detected")
            return True
        if URL_RE.search(c):
            print(f"[PII] URL detected")
            return True
        if PHONE_RE.search(c):
            print(f"[PII] Phone detected")
            return True
        if CARD_RE.search(c):
            print(f"[PII] Credit card detected")
            return True

    if PINCODE_RE.search(t):
        print(f"[PII] PIN code detected")
        return True
    
    if len(numeric_string) >= 10:
        print(f"[PII] Number words detected")
        return True
    
    # ============ ENHANCED ADDRESS DETECTION ============
    # Check for complete addresses with stricter validation
    if len(t) >= 10:  # Addresses are usually longer
        # Quick check for address markers
        has_marker = bool(ADDRESS_KW.search(t))
        has_zip = _is_zip_code(t)
        
        if has_marker or has_zip:
            # Use enhanced address detection
            is_addr, score, components = _is_address_with_components(t)
            if is_addr:
                print(f"[PII] Address detected: score={score}, components={components}")
                return True
        
        # Check if text contains a complete address (multiline)
        addresses = extract_addresses(t)
        if addresses:
            print(f"[PII] Address detected: {addresses[0][:50]}...")
            return True
    
    # ============ LOCATION NAME DETECTION (STRICTER) ============
    # Only check for location names if it's NOT already detected as an address
    # This is now much stricter
    if _contains_location_name(t):
        # Don't flag standalone city names or simple "I live in X" statements
        print(f"[PII] Location detected but treating as non-PII (address-like statements)")
        return False
    
    return False


# ============ UTILITY FUNCTIONS ============

def get_detected_pii_types(text: str) -> dict:
    """
    Returns a dictionary of detected PII types with their values.
    Useful for debugging and detailed analysis.
    """
    if not text:
        return {}
    
    result = {}
    t = text.strip()
    normalized = normalize_email_obfuscation(t)
    numeric_string = decode_number_words(t)
    
    # Check email
    email_matches = EMAIL_RE.findall(t)
    if email_matches:
        result["email"] = email_matches
    
    # Check URLs
    url_matches = URL_RE.findall(t)
    if url_matches:
        result["url"] = [u.strip('.,!?') for u in url_matches]
    
    # Check phone numbers
    phone_matches = PHONE_RE.findall(t)
    if phone_matches:
        phones = []
        for match in phone_matches:
            if isinstance(match, tuple):
                phone = match[0] if match[0] else match[1] if len(match) > 1 else ""
                if phone:
                    phones.append(phone)
            else:
                phones.append(match)
        if phones:
            result["phone"] = phones
    
    # Check credit cards
    card_matches = CARD_RE.findall(t)
    if card_matches:
        result["credit_card"] = card_matches
    
    # Check PIN codes
    pincode_matches = PINCODE_RE.findall(t)
    if pincode_matches:
        result["pincode"] = pincode_matches
    
    # Check number words
    if len(numeric_string) >= 10:
        result["number_words"] = numeric_string
    
    # Check addresses - ONLY if it's a complete address
    addresses = extract_addresses(t)
    if addresses:
        result["address"] = addresses
    
    return result


# ============ MAIN ============

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("Usage:")
            print("  python detect_pii.py <text>")
            print("  python detect_pii.py --help")
            print("\nOr pipe text:")
            print("  echo 'your text here' | python detect_pii.py")
            sys.exit(0)
        
        # Read from command line or stdin
        if len(sys.argv) > 1 and sys.argv[1] != "--help":
            text = " ".join(sys.argv[1:])
        else:
            text = sys.stdin.read().strip()
        
        if text:
            print(f"\n=== TEXT ===")
            print(text)
            print("\n=== DETECTION ===")
            result = detect_personal_info(text)
            print(f"PII Detected: {result}")
            
            if result:
                details = get_detected_pii_types(text)
                print("\n=== DETAILS ===")
                for pii_type, values in details.items():
                    print(f"  {pii_type}: {values}")
        else:
            print("No text provided.")
            print("Usage: python detect_pii.py 'your text here'")
    
    else:
        # Example test
        print("="*60)
        print("PII DETECTION TEST")
        print("="*60)
        
        test_texts = [
            # Addresses (should detect)
            ("1600 Pennsylvania Ave NW, Washington DC 20500", True),
            ("742 Evergreen Terrace, Springfield", True),
            ("221B Baker Street, London NW1 6XE", True),
            ("Flat 5, 10 Downing Street, London SW1A 2AA", True),
            ("2/A Bose Pukur Road, Kasba, Kolkata, West Bengal 700042", True),
            ("Flat 302, ABC Residency, Sector 5, Salt Lake, Kolkata 700091", True),
            
            # Non-addresses (should NOT detect)
            ("I live in London", False),
            ("I am from California", False),
            ("Paris is beautiful", False),
            ("Visit New York", False),
            ("London", False),
            ("California", False),
            ("India", False),
            
            # Other PII (should detect)
            ("test@example.com", True),
            ("1234567890", True),
            ("https://example.com", True),
        ]
        
        print("\nTesting addresses and PII:\n")
        passed = 0
        failed = 0
        
        for text, expected in test_texts:
            result = detect_personal_info(text)
            status = "✅" if result == expected else "❌"
            if result == expected:
                passed += 1
            else:
                failed += 1
            print(f"{status} Expected: {expected}, Got: {result} | {text[:50]}...")
        
        print("\n" + "="*60)
        print(f"Results: {passed} passed, {failed} failed")
        print("="*60)