# app/moderation/detectors/dangerous_content/keywords.py

"""
Keyword lexicons for Dangerous Content detection.
Comprehensive list for USA/UK social media.
"""

# ------------------------------------
# DRUGS (Illegal & Recreational)
# ------------------------------------

DRUG_WORDS = {
    # GENERAL DRUG TERMS (CRITICAL - ADD THESE FIRST!)
    "drug", "drugs", "drugged", "drug abuse", "drug use",
    "drug taking", "drug using", "substance", "substances",
    "narcotics", "narcotic", "controlled substance",
    
    # Illegal drugs
    "cocaine", "coke", "blow", "snow", "crack",
    "heroin", "smack", "horse", "dope", "junk",
    "meth", "methamphetamine", "crystal", "ice", "speed",
    "fentanyl", "fent", "oxy", "oxycontin", "percs",
    "lsd", "acid", "blotter", "microdot",
    "ecstasy", "mdma", "molly", "e", "x",
    "ketamine", "k", "special k",
    "pcp", "angel dust", "dissociative",
    "ghb", "liquid ecstasy", "roofie", "date rape drug",
    "bath salts", "flakka", "spice", "k2", "synthetic marijuana",
    
    # Recreational (legal/illegal depending on age/country)
    "weed", "marijuana", "cannabis", "pot", "ganja", "bud",
    "hash", "hashish", "dabs", "wax", "shatter",
    "vape", "vaping", "edibles", "gummies", "tincture",
    "joint", "blunt", "spliff", "bong", "pipe", "bowl",
    
    # Prescription drug abuse
    "xanax", "bars", "benzos", "valium", "diazepam",
    "adderall", "ritalin", "concerta", "speed", "study drug",
    "vicodin", "norco", "lortab", "hydrocodone",
    "codeine", "sizzurp", "lean", "purple drank",
    "tramadol", "ultram", "ambien", "zolpidem",
    
    # Other substances
    "poppers", "nitrous", "whippets", "laughing gas",
    "mushrooms", "shrooms", "psychedelics", "hallucinogens",
    "kratom", "kava", "salvia", "ayahuasca",
    
    # Manufacturing terms
    "cook", "cooking", "manufacture", "synthesize",
    "extraction", "purification", "precursor", "chemicals",
}

# ------------------------------------
# WEAPONS (Firearms & Dangerous Weapons)
# ------------------------------------

WEAPON_WORDS = {
    # Firearms
    "gun", "guns", "firearm", "firearms", "pistol", "revolver",
    "handgun", "semi-automatic", "automatic", "assault rifle",
    "rifle", "shotgun", "hunting rifle", "sniper rifle",
    "ak-47", "ak47", "ar-15", "m16", "m4", "glock", "sig",
    
    # Ammunition
    "bullet", "bullets", "ammo", "ammunition", "magazine",
    "clip", "rounds", "shells", "cartridge", "hollow point",
    
    # Parts & accessories
    "silencer", "suppressor", "scope", "red dot", "laser sight",
    "extended magazine", "high capacity", "conversion kit",
    "trigger", "barrel", "slide", "frame", "receiver",
    
    # Knives & blades
    "knife", "knives", "switchblade", "butterfly knife", "balisong",
    "machete", "sword", "dagger", "bayonet", "combat knife",
    "pocket knife", "hunting knife", "survival knife",
    
    # Other weapons
    "baton", "nightstick", "taser", "stun gun", "pepper spray",
    "brass knuckles", "nunchucks", "fighting stick",
    "crossbow", "compound bow", "blowgun", "slingshot",
}

# ------------------------------------
# EXPLOSIVES & INCENDIARY DEVICES
# ------------------------------------

EXPLOSIVE_WORDS = {
    "bomb", "bombs", "explosive", "explosives", "detonator",
    "dynamite", "tnt", "c4", "plastic explosive", "semtex",
    "grenade", "hand grenade", "rocket", "rocket launcher",
    "mortar", "landmine", "claymore", "pipe bomb", "pressure cooker",
    "ied", "improvised explosive", "incendiary", "napalm",
    "thermite", "magnesium", "potassium", "peroxide", "acetone",
    "fertilizer bomb", "hazmat", "chemical agent",
    
    # Components
    "fuse", "timer", "det cord", "blasting cap", "primer",
    "ball bearings", "shrapnel", "fragmentation",
    
    # Explosive materials
    "gunpowder", "black powder", "nitroglycerin", "rdx",
    "hmx", "petn", "ammonium nitrate", "fuel oil",
}

# ------------------------------------
# TERRORIST ORGANIZATIONS
# ------------------------------------

TERROR_GROUP_WORDS = {
    "isis", "isil", "daesh", "al-qaeda", "alqaeda", "al qaeda",
    "taliban", "hizbullah", "hezbollah", "hamas", "jihad",
    "boko haram", "al-shabaab", "al-nusra", "houthi",
    "irgc", "qassam", "pkk", "mujahedeen", "talbans",
    "white supremacy", "neo-nazi", "kka", "kmb", 
    "islamic state", "jihadist", "terrorist", "terrorists",
    "radical islamist", "extremist", "extremists",
}

# ------------------------------------
# RECRUITMENT / SUPPORT
# ------------------------------------

RECRUITMENT_WORDS = {
    "join", "recruit", "recruitment", "enlist", "enrolling",
    "pledge", "allegiance", "loyalty", "swear", "oath",
    "support", "supporting", "supporter", "sympathizer",
    "fund", "funding", "donate", "donation", "finance",
    "recruiting", "recruiter", "volunteer", "volunteering",
    "fighting for", "struggle", "cause", "movement",
}

# ------------------------------------
# PURCHASE / ACQUIRE
# ------------------------------------

PURCHASE_WORDS = {
    "buy", "buying", "purchase", "purchasing", "order", "ordering",
    "sell", "selling", "dealer", "dealers", "source", "sourcing",
    "acquire", "acquiring", "obtain", "obtaining", "get",
    "procure", "procuring", "transaction", "trade", "trading",
    "dark web", "deep web", "tor", "onion", "encrypted",
    "crypto", "bitcoin", "monero", "cash", "wire",
    "black market", "street", "plug", "connect",
}

# ------------------------------------
# INSTRUCTIONAL / HOW-TO
# ------------------------------------

INSTRUCTION_WORDS = {
    "how to", "how do i", "how can i", "how do you",
    "make", "making", "build", "building", "create", "creating",
    "manufacture", "manufacturing", "cook", "cooking",
    "produce", "producing", "synthesize", "synthesizing",
    "tutorial", "guide", "instructions", "step by step",
    "recipe", "process", "method", "technique", "procedure",
    "diagram", "schematic", "blueprint", "design",
}

# ------------------------------------
# INTENT / DESIRE
# ------------------------------------

INTENT_WORDS = {
    # ACTION WORDS
    "take", "taking", "takes", "taken",
    "use", "using", "uses", "used",
    "try", "trying", "tried",
    "do", "doing", "does", "did",
    
    # DESIRE WORDS
    "want", "wanted", "wanting",
    "need", "needed", "needing",
    "plan", "planning", "plans",
    "going to", "gonna",
    "will", "would",
    "intend", "intending", "intended",
    "hoping", "looking to", "aim", "aiming",
    "goal", "objective", "mission",
}

# ------------------------------------
# TIME / URGENCY
# ------------------------------------

TIME_WORDS = {
    "today", "tonight", "tomorrow", "now", "soon",
    "immediately", "right now", "asap", "as soon as",
    "within", "in a few", "hour", "hours", "minute",
    "tonight", "this week", "this weekend", "later",
    "after", "before", "when", "while", "during",
}

# ------------------------------------
# FIRST PERSON
# ------------------------------------

FIRST_PERSON = {
    "i", "me", "my", "myself",
    "i'm", "i'll", "i'd", "i've",
    "mine", "we", "us", "our", "ourselves",
    "we're", "we'll", "we've", "we'd",
}

# ------------------------------------
# NEGATION
# ------------------------------------

NEGATION_WORDS = {
    "not", "never", "no", "don't", "dont", 
    "doesn't", "doesnt", "isn't", "isnt", 
    "aren't", "arent", "wasn't", "wasnt",
    "weren't", "werent", "won't", "wont",
    "wouldn't", "wouldnt", "shouldn't", "shouldnt",
    "couldn't", "couldnt", "can't", "cant",
    "didn't", "didnt", "hasn't", "hasnt",
    "haven't", "havent", "hadn't", "hadnt",
}

# ------------------------------------
# CONTEXT WORDS (reduce false positives)
# ------------------------------------

CONTEXT_REDUCTION = {
    "movie", "movies", "film", "films", "show", "tv",
    "video game", "gaming", "game", "games",
    "documentary", "book", "books", "novel", "article",
    "history", "historical", "educational", "learning",
    "news", "reported", "according to", "police said",
    "fiction", "fictional", "imaginary", "hypothetical",
    "museum", "exhibit", "school", "college", "university",
    "discussion", "debate", "conversation", "talking about",
}

# ============================================================
# NEW: SEXUAL CONTENT TERMS (For pre-check & context reduction)
# ============================================================

SEXUAL_TERMS = {
    "fuck", "fucking", "fucked", "fucker", "sex", "sexual", 
    "blowjob", "blow job", "oral", "anal", "vaginal", 
    "penetration", "orgasm", "ejaculate", "ejaculation",
    "masturbate", "masturbation", "nude", "naked", 
    "porn", "porno", "pornography", "sexy", "erotic", 
    "kinky", "fetish", "fetishes", "bdsm", "bondage",
    "dominance", "submission", "sadism", "masochism",
    "hardcore", "adult content", "x-rated", "xxx"
}

# ============================================================
# NEW: THREAT/VIOLENCE TERMS (For pre-check)
# ============================================================

THREAT_TERMS = {
    "shoot", "shooting", "shot", "kill", "killing", "killed",
    "murder", "murdering", "murdered", "attack", "attacking",
    "attacked", "stab", "stabbing", "stabbed", "gun", "guns",
    "weapon", "weapons", "firearm", "firearms", "bomb", "bombs",
    "explosive", "explosives", "destroy", "destroys", "destroying",
    "destroyed", "assassinate", "assassination", "threat", "threats",
    "threaten", "threatening", "terror", "terrorize", "terrorizing",
    "intimidate", "intimidating", "menace", "menacing",
    "knife", "knives", "sword", "swords", "blade", "blades"
}

# ============================================================
# NEW: DANGEROUS KEYWORDS (For pre-check)
# ============================================================

DANGEROUS_KEYWORDS = {
    # Drugs
    "drug", "drugs", "cocaine", "heroin", "meth", "crack", "fentanyl",
    "acid", "lsd", "ecstasy", "mdma", "molly", "weed",
    "marijuana", "cannabis", "xanax", "oxy", "oxycontin",
    "adderall", "vicodin", "codeine", "tramadol", "ketamine",
    
    # Terror groups
    "isis", "isil", "daesh", "al-qaeda", "alqaeda", "taliban",
    "boko haram", "hezbollah", "hamas", "jihad", "jihadist",
    "terrorist", "terrorists", "extremist", "extremists",
    
    # Explosives
    "explosive", "explosives", "bomb", "bombs", "detonator",
    "dynamite", "tnt", "c4", "grenade", "rocket", "mortar",
    "gunpowder", "nitroglycerin", "ammonium nitrate",
    
    # Weapons
    "gun", "guns", "weapon", "weapons", "firearm", "firearms",
    "rifle", "shotgun", "pistol", "revolver", "ak-47", "ak47",
    "ar-15", "m16", "m4", "glock", "sig", "handgun",
}