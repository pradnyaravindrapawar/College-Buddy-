"""Natural Language Processing (NLP) Pipeline for College FAQ Chatbot.

=============================================================================
VIVA / ORAL EXAM CHEAT-SHEET:
Step 1 - Lowercasing: Normalizes orthographic variance ("Hostel" -> "hostel").
Step 2 - Punctuation Stripping: Eliminates syntax noise ("hostel?" -> "hostel").
Step 3 - Stop Words Removal: Filters out ubiquitous, low-information tokens
         (e.g., "what", "is", "the", "are", "of", "in").
Step 4 - Light Stemming: Normalizes inflectional endings (-ing, -ies, -ed, -s)
         to standard base stems without requiring heavy dependencies.
Step 5 - Synonym Expansion: Injects domain-specific equivalents loaded from
         data/synonyms.json (e.g. "dorm" -> "hostel", "salary" -> "placement").
Step 6 - Weighted Text Representation: Prioritizes question and paraphrases
         over answer body when generating TF-IDF & dense representations.
=============================================================================
"""

import os
import re
import json
from typing import List, Dict, Set

# Standard English stop words curated for educational search queries
STOP_WORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can", "cannot", "could", "did", "do",
    "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had",
    "has", "have", "having", "he", "her", "here", "hers", "herself", "him", "himself",
    "his", "how", "i", "if", "in", "into", "is", "isn't", "it", "its", "itself", "me",
    "more", "most", "my", "myself", "no", "nor", "not", "of", "off", "on", "once",
    "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own",
    "same", "she", "should", "so", "some", "such", "than", "that", "the", "their",
    "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those",
    "through", "to", "too", "under", "until", "up", "very", "was", "we", "were", "what",
    "when", "where", "which", "while", "who", "whom", "why", "with", "would", "you",
    "your", "yours", "yourself", "yourselves"
}

# Load synonyms mapping from data/synonyms.json
SYNONYM_MAP: Dict[str, List[str]] = {}
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
SYNONYMS_FILE = os.path.join(DATA_DIR, "synonyms.json")

def load_synonyms() -> Dict[str, List[str]]:
    """Load or reload domain synonym mappings from disk."""
    global SYNONYM_MAP
    if os.path.exists(SYNONYMS_FILE):
        try:
            with open(SYNONYMS_FILE, "r", encoding="utf-8") as f:
                SYNONYM_MAP = json.load(f)
        except Exception as e:
            print(f"[NLP Warning] Failed to load synonyms.json: {e}")
            SYNONYM_MAP = {}
    return SYNONYM_MAP

load_synonyms()


def light_stem(word: str) -> str:
    """Apply rule-based suffix stemming to reduce morphological inflections.

    Viva explanation: A light stemmer maps words like 'placements', 'placed',
    and 'placing' closer to a common root 'place', boosting lexical recall.
    """
    if len(word) <= 3:
        return word
    
    # Common English inflections
    if word.endswith("ees"):
        return word[:-1]  # 'fees' -> 'fee', 'degrees' -> 'degree'
    elif word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    elif word.endswith("sses"):
        return word[:-2]
    elif word.endswith("ing") and len(word) > 4:
        # e.g., 'running' -> 'run', 'paying' -> 'pay'
        return word[:-3]
    elif word.endswith("ed") and len(word) > 3:
        return word[:-2]
    elif word.endswith("ly") and len(word) > 3:
        return word[:-2]
    elif word.endswith("es") and len(word) > 3 and not word.endswith("ses"):
        return word[:-2]
    elif word.endswith("s") and not word.endswith("ss") and len(word) > 3:
        return word[:-1]
    
    return word


def clean_and_tokenize(text: str, apply_stemming: bool = True, expand_synonyms: bool = True) -> List[str]:
    """Preprocess raw user or FAQ text into clean semantic tokens.

    Pipeline sequence:
    1. Lowercase string
    2. Strip non-alphanumeric punctuation
    3. Tokenize on whitespace
    4. Remove stop words
    5. Optional light stemming
    6. Optional synonym expansion
    """
    if not text:
        return []

    # Step 1: Lowercasing
    text = text.lower()

    # Step 2: Strip punctuation and special characters, preserving alphanumeric tokens
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Step 3: Whitespace tokenization
    raw_tokens = text.split()

    # Step 4: Stop words filtering & length filter (>1 char or numeric)
    filtered_tokens: List[str] = [
        t for t in raw_tokens if t not in STOP_WORDS and (len(t) > 1 or t.isdigit())
    ]

    # Step 5: Light stemming
    if apply_stemming:
        processed_tokens = [light_stem(t) for t in filtered_tokens]
    else:
        processed_tokens = filtered_tokens

    # Step 6: Synonym injection
    if expand_synonyms and SYNONYM_MAP:
        expanded = list(processed_tokens)
        for token in processed_tokens:
            # Check direct term or reverse lookup
            if token in SYNONYM_MAP:
                for syn in SYNONYM_MAP[token][:2]:  # inject up to 2 primary synonyms
                    stemmed_syn = light_stem(syn) if apply_stemming else syn
                    if stemmed_syn not in expanded:
                        expanded.append(stemmed_syn)
            else:
                # Check if token is inside any synonym values
                for headword, synonyms in SYNONYM_MAP.items():
                    if token in synonyms:
                        stemmed_head = light_stem(headword) if apply_stemming else headword
                        if stemmed_head not in expanded:
                            expanded.append(stemmed_head)
                        break
        return expanded

    return processed_tokens


def build_faq_index_text(question: str, paraphrases: str, keywords: str, answer: str) -> str:
    """Construct an engineered text document representing an FAQ item.

    Weighting strategy:
    - Primary Question: repeated 3x (highest intent focus)
    - Paraphrases: repeated 2x (captures varied student vocabulary)
    - Keywords: repeated 2x (explicit academic tags)
    - Answer: included 1x (contextual background)
    """
    clean_paraphrases = " ".join(paraphrases.split("|")) if paraphrases else ""
    clean_keywords = " ".join(keywords.split("|")) if keywords else ""

    parts = [
        question,
        question,
        question,
        clean_paraphrases,
        clean_paraphrases,
        clean_keywords,
        clean_keywords,
        answer
    ]
    return " ".join([p for p in parts if p.strip()])
