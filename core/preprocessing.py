# core/preprocessing.py
import re
import unicodedata

# Allowed Unicode ranges for Urdu and additional characters
URDU_ALLOWED_RANGES = r"\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF"
ALLOWED_ADDITIONAL = r"0-9۰-۹\s\.\,؟!\?\-\:\؛\(\)\/\u066B\u066C"

# Compiled regex patterns for cleaning
_non_urdu_re = re.compile(rf"[^{URDU_ALLOWED_RANGES}{ALLOWED_ADDITIONAL}]+")
_collapse_space_re = re.compile(r"[ \t]+")
_collapse_newline_re = re.compile(r"\n{3,}")

def _simple_character_normalize(text: str) -> str:
    """
    Normalize Urdu text by:
    - NFC normalization
    - Removing Tatweel
    - Standardizing Alef forms
    - Replacing ? with Urdu question mark
    - Normalizing dashes
    """
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\u0640", "")  # Tatweel
    text = text.replace("\u0622", "\u0627")  # Alef with Maddah to Alef
    text = text.replace("\u0623", "\u0627")  # Alef with Hamza Above to Alef
    text = text.replace("\u0625", "\u0627")  # Alef with Hamza Below to Alef
    text = text.replace("?", "؟")  # English ? to Urdu ؟
    text = re.sub(r"[\u2013\u2014\u2015]", "-", text)  # Normalize dashes to ASCII hyphen
    return text

def clean_urdu_text(raw: str) -> str:
    """
    Clean and normalize Urdu OCR text:
    - Normalize characters
    - Remove control characters except newlines
    - Remove non-Urdu and disallowed symbols
    - Fix spacing around punctuation
    - Collapse multiple spaces/newlines
    """
    if not raw:
        return raw

    # Step 1: Normalize characters
    text = _simple_character_normalize(raw)

    # Step 2: Remove control characters (except newlines)
    text = "".join(ch for ch in text if unicodedata.category(ch)[0] != "C" or ch == "\n")

    # Step 3: Remove any non-Urdu/disallowed characters
    text = _non_urdu_re.sub(" ", text)

    # Step 4: Collapse extra spaces
    text = _collapse_space_re.sub(" ", text)

    # Step 5: Fix spacing before punctuation
    text = re.sub(r"\s+([.,؟!\:؛\)\]])", r"\1", text)
    text = re.sub(r"([.,؟!\:؛\)\]])\s*([^\s\n])", r"\1 \2", text)

    # Step 6: Remove trailing spaces from lines
    text = "\n".join(line.rstrip() for line in text.splitlines())

    # Step 7: Collapse excessive newlines
    text = _collapse_newline_re.sub("\n\n", text)

    # Step 8: Final strip
    text = text.strip()

    return text
