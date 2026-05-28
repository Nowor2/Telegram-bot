BLOCKED_WORDS = {
    "porn", "porno", "pornography",
    "anal", "anus",
    "lesbian", "lesbi",
    "sex", "sexy", "sexo",
    "dick", "cock", "penis", "vagina", "pussy",
    "fuck", "fucking", "fucker",
    "shit", "shitting",
    "ass", "asshole",
    "bitch",
    "nude", "naked",
    "xxx", "hentai",
    "whore", "slut",
    "rape", "rapist",
    "nigger", "nigga",
    "pedophile", "pedophilia",
    "masturbate", "masturbation",
    "orgasm", "erection", "dildo", "condom",
}


def is_censored(word: str) -> bool:
    return word.lower().strip() in BLOCKED_WORDS
