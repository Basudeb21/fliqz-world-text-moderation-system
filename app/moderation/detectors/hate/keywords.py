# app/moderation/detectors/hate/keywords.py
"""
Keyword groups used by the fast Hate Speech scanner.

These keywords DO NOT determine whether content is hate speech.
They only contribute to the risk score.

Only messages whose score exceeds the threshold
will be sent to the LLM.
"""

# ---------------------------------------
# Protected Identity Groups
# ---------------------------------------

IDENTITY_WORDS = {
    # Religion
    "muslim", "islam", "islamic", "jewish", "jew", "jews", "judaism",
    "christian", "christianity", "catholic", "protestant",
    "hindu", "hinduism", "buddhist", "buddhism", "sikh", "sikhism",
    "atheist", "agnostic", "pagan", "mormon", "jehovah",
    "scientology", "cult", "religious", "faith", "belief",
    
    # Race & Ethnicity
    "black", "african", "african american", "white", "caucasian",
    "asian", "chinese", "japanese", "korean", "indian", "pakistani",
    "hispanic", "latino", "latinx", "mexican", "native american",
    "indigenous", "aboriginal", "arab", "middle eastern",
    "mixed race", "biracial", "multiracial", "race", "racial",
    "ethnicity", "ethnic", "minority", "people of color", "poc",
    
    # Nationality
    "american", "british", "french", "german", "russian", "chinese",
    "japanese", "indian", "pakistani", "bangladeshi", "nigerian",
    "kenyan", "brazilian", "mexican", "canadian", "australian",
    "immigrant", "immigrants", "refugee", "refugees", "asylum",
    "foreigner", "alien", "illegal", "undocumented", "nationality",
    "national origin",
    
    # Gender & Sexual Orientation
    "gay", "lesbian", "bisexual", "bi", "queer", "transgender",
    "trans", "nonbinary", "nb", "genderfluid", "genderqueer",
    "pansexual", "asexual", "allosexual", "cisgender", "cis",
    "lgbt", "lgbtq", "lgbtqia", "rainbow", "pride", "homosexual",
    "heterosexual", "straight", "feminine", "masculine", "gender",
    "sex", "sexual orientation", "preference", "lifestyle",
    
    # Disability & Health
    "disabled", "disability", "handicapped", "blind", "deaf",
    "wheelchair", "autism", "autistic", "adhd", "dyslexia",
    "down syndrome", "epilepsy", "chronic illness", "invisible",
    "mental health", "depression", "anxiety", "bipolar", "ocd",
    "ptsd", "schizophrenia", "neurodivergent", "neurotypical",
    "retard", "retarded", "crippled", "dwarf", "midget",
    
    # Other Protected Groups
    "elderly", "senior", "old", "age", "pregnant", "pregnancy",
    "veteran", "army", "military", "servicemen", "soldier",
    "poor", "impoverished", "homeless", "low income", "underprivileged",
}

# ---------------------------------------
# Slurs (Severe Hate Speech)
# ---------------------------------------

SLUR_WORDS = {
    # Anti-Black/Racist Slurs
    "nigger", "nigga", "negro", "coon", "spook", "jigaboo",
    "wop", "guido", "dago", "greaser", "spic", "wetback",
    "beaner", "taco", "chink", "gook", "slant", "yellow",
    "kike", "hebe", "yid", "hymie", "shylock", "anti-semite",
    "raghead", "towelhead", "sand nigger", "camel jockey",
    "paki", "curry muncher", "brownie", "dot head",
    "redskin", "injun", "savage", "halfbreed", "breed",
    "homo", "fag", "faggot", "dyke", "queer", "tranny",
    "sheep", "trailer trash", "white trash", "hillbilly",
    "retard", "retarded", "mongoloid", "spaz", "spastic",
    
    # Intersectional slurs
    "sand nigger", "sand monkey", "camel jockey",
    "choco", "choc ice", "coconut", "oreo",
}

# ---------------------------------------
# Generic Insults
# ---------------------------------------

INSULT_WORDS = {
    "stupid", "dumb", "idiot", "moron", "fool", "ignorant",
    "crazy", "insane", "mad", "psycho", "mental", "lunatic",
    "weak", "pathetic", "worthless", "useless", "inferior",
    "trash", "garbage", "scum", "filth", "pond scum",
    "lower", "underling", "peasant", "pleb", "barbarian",
    "savage", "uncivilized", "uneducated", "illiterate",
    "ugly", "repulsive", "disgusting", "freak", "monster",
    "jerk", "bastard", "asshole", "dick", "prick", "shit",
    "loser", "failure", "nobody", "nothng", "zero",
    "untermensch", "subhuman", "inferior", "degenerate",
    "suck", "sucks", "sucking", "pointless", "brainless",
    "simpleton", "imbecile", "creep", "lowlife", "bottom feeder",
}

# ---------------------------------------
# Violence
# ---------------------------------------

VIOLENCE_WORDS = {
    # Direct violence
    "kill", "killing", "murder", "slaughter", "execute", "assassinate",
    "destroy", "exterminate", "annihilate", "eradicate", "eliminate",
    "hurt", "harm", "maim", "injure", "wound", "stab", "shoot",
    "knife", "gun", "weapon", "bomb", "explosion", "violence",
    "assault", "attack", "beating", "bloodshed", "genocide",
    "burn", "burning", "torture", "torturing", "decimate",
    
    # Violent actions
    "deport", "expel", "banish", "exile", "purge", "cleanse",
    "ethnical cleansing", "forced removal", "concentration camp",
    "cull", "execute", "oppress", "crush", "crushing",
    
    # Threatening verbs
    "destroy", "annihilate", "exterminate", "liquidate",
    "vaporize", "dismantle", "level", "flatten", "raze",
    "wipe out", "wipe off", "take out", "finish off",
    
    # Physical harm
    "break", "crush", "smash", "shatter", "cut", "slice",
    "bludgeon", "strangle", "suffocate", "poison", "drown",
    "electrocute", "burn alive", "torture", "mutilate",
    
    # Specific violent acts
    "lynch", "hang", "guillotine", "behead", "decapitate",
    "crucify", "impale", "burn at stake", "stone", "stoning",
    "beating", "whipping", "lash", "flog", "torture",
    
    # War/conflict
    "war", "warfare", "battle", "combat", "invade", "conquer",
    "colonize", "subjugate", "oppress", "tyranny", "dictatorship",
}

# ---------------------------------------
# Dehumanization
# ---------------------------------------

DEHUMANIZATION_WORDS = {
    # Animal comparisons
    "animal", "beast", "monster", "creature", "savage",
    "wolf", "hyena", "jackal", "vulture", "rat", "vermin",
    "roach", "cockroach", "bug", "parasite", "leech",
    "cancer", "tumor", "plague", "virus", "disease",
    "filth", "scum", "maggot", "worm", "snake", "reptile",
    "ape", "monkey", "gorilla", "chimp", "baboon",
    "dog", "pig", "swine", "cow", "sheep", "goat",
    "donkey", "ass", "mule", "camel", "llama",
    
    # Objectification
    "it", "thing", "object", "tool", "instrument",
    "product", "byproduct", "waste", "garbage", "trash",
    "resource", "material", "quantity", "number", "statistic",
    "asset", "property", "possession", "ownership",
    
    # Disease/Infection
    "infection", "infectious", "contagion", "sickness",
    "pest", "infestation", "plague", "blight", "scourge",
    "bubonic", "leprosy", "contamination", "pollution",
    "poison", "toxin", "venom", "cancerous", "malignant",
    
    # Subhuman comparisons
    "subhuman", "untermensch", "inhuman", "non-human",
    "half-breed", "mixed breed", "mongrel", "cur", "mutt",
    "hybrid", "mutant", "deformed", "abomination",
    
    # Evil characterization
    "demon", "devil", "satanic", "evil", "wicked", "malevolent",
    "vile", "heinous", "atrocious", "detestable", "loathsome",
    "repugnant", "abhorrent", "revulsive", "revolting",
    
    # Collective dehumanization
    "herd", "flock", "pack", "swarm", "colony", "infestation",
    "horde", "mob", "crowd", "mass", "rabble", "masses",
}

# ---------------------------------------
# Threat Words
# ---------------------------------------

THREAT_WORDS = {
    # Explicit threats
    "threat", "threaten", "threatening", "terror", "terrorize",
    "intimidate", "intimidation", "menace", "menacing",
    "danger", "dangerous", "hazard", "harmful", "deadly",
    "lethal", "fatal", "mortal", "deathly", "grave",
    
    # Threat actions
    "destroy", "destruction", "annihilate", "annihilation",
    "eradicate", "eradication", "eliminate", "elimination",
    "exterminate", "extermination", "liquidate", "liquidation",
    "purge", "purging", "cleanse", "cleansing", "remove",
    "removal", "get rid of", "take care of", "deal with",
    
    # Conditional threats
    "if you don't", "unless you", "or else", "otherwise",
    "you better", "you'd better", "you should",
    "you will pay", "you will regret", "beware",
    
    # Specific threat types
    "death threat", "death threats", "rape threat", "rape threats",
    "bomb threat", "attack threat", "assassination", "hit",
    "kill list", "death list", "target list", "hit list",
    
    # System/institutional threats
    "overthrow", "revolt", "revolution", "uprising", "insurrection",
    "sedition", "treason", "subversion", "sabotage", "terrorism",
    
    # Weapon-related threats
    "weapon", "weapons", "firearm", "gun", "rifle", "shotgun",
    "machine gun", "assault rifle", "pistol", "revolver",
    "bomb", "explosive", "grenade", "missile", "rocket",
    "knife", "sword", "blade", "dagger", "machete",
    "shoot", "stab", "slash", "beat", "torture",
    
    # Online threats
    "dox", "doxx", "swat", "swatting", "hack", "ddos",
    "harass", "harassment", "cyberbully", "cyberbullying",
    "post online", "expose", "leak", "personal info",
}

# ---------------------------------------
# Target Words
# ---------------------------------------

TARGET_WORDS = {
    "you",
    "your",
    "they",
    "them",
    "their",
    "those",
    "these",
    "all",
    "every",
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
# Context Words (for nuance)
# ---------------------------------------

CONTEXT_WORDS = {
    # Reporting/quoting (reduce score)
    "report", "reported", "reporting", "article", "news",
    "according to", "source", "sources", "quote", "quotes",
    "said", "stated", "claimed", "according", "published",
    
    # Academic/educational (reduce score)
    "study", "studies", "research", "researching", "academic",
    "scholar", "scholars", "education", "educational", "learning",
    "historical", "history", "context", "contextual", "analyze",
    "analysis", "perspective", "discussion", "debate",
    
    # Hypothetical (reduce score)
    "if", "hypothetical", "theoretical", "what if", "imagine",
    "suppose", "assuming", "in case", "under the assumption",
    
    # Self-reference/correction (reduce score)
    "i think", "i believe", "in my opinion", "personally",
    "maybe", "perhaps", "possibly", "probably",
    
    # Speculative/uncertain (reduce score)
    "might", "could", "would", "may", "potentially",
    
    # Irony/sarcasm indicators (reduce score)
    "sarcasm", "irony", "joke", "joking", "kidding",
    "just kidding", "obviously", "clearly",
}

# ---------------------------------------
# Extreme Hate Speech Patterns (for pre-check)
# ---------------------------------------

EXTREME_HATE_PATTERNS = {
    "kill all", "kill the", "kill every", "kill all the",
    "exterminate", "wipe out", "get rid of all",
    "eliminate all", "murder all", "destroy all",
    "all should die", "all must die",
}

DEHUMANIZING_TERMS = {
    "vermin", "rats", "parasites", "animals", "roaches",
    "cockroaches", "filth", "scum", "disease", "plague",
    "trash", "garbage", "maggots", "worms",
}

LGBTQ_TARGETS = {
    "transgender", "trans", "gay", "lesbian", "queer", "lgbt", "lgbtq"
}

DEROGATORY_TERMS = {
    "mentally ill", "sick", "diseased", "disorder", "abnormal"
}

IDENTITY_TARGETS = {
    "jew", "jews", "muslim", "muslims", "black", "blacks",
    "immigrant", "immigrants", "refugee", "refugees",
    "gay", "transgender", "trans", "lesbian", "queer",
    "asian", "whites", "white", "mexican", "hispanic",
}