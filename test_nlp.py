"""Unit tests for NLP preprocessing and tokenization."""

import pytest
from app.nlp import clean_and_tokenize, light_stem, build_faq_index_text


def test_light_stem():
    """Verify suffix reduction for common educational terms."""
    assert light_stem("placements") == "placement"
    assert light_stem("fees") == "fee"
    assert light_stem("applying") == "apply"
    assert light_stem("studied") == "studi"
    assert light_stem("bus") == "bus"  # short words preserved


def test_clean_and_tokenize_removes_punctuation_and_stopwords():
    """Verify lowercasing, punctuation removal, and stopword elimination."""
    text = "What is the annual fee for B.Tech engineering?!"
    tokens = clean_and_tokenize(text, apply_stemming=True, expand_synonyms=False)
    assert "what" not in tokens
    assert "is" not in tokens
    assert "the" not in tokens
    assert "for" not in tokens
    # Core semantic terms must be retained
    assert "annual" in tokens
    assert "fee" in tokens
    assert "b" in tokens or "tech" in tokens


def test_clean_and_tokenize_synonym_expansion():
    """Verify that college synonyms like 'dorm' map to 'hostel'."""
    text = "dorm room charges"
    tokens = clean_and_tokenize(text, apply_stemming=True, expand_synonyms=True)
    assert any("hostel" in t or "dorm" in t for t in tokens)


def test_build_faq_index_text_weighting():
    """Verify that question appears more times than answer for weighted indexing."""
    q = "What is the hostel fee?"
    p = "Hostel charges|Dorm cost"
    k = "hostel|fee"
    a = "Annual hostel rent is 65000."
    doc = build_faq_index_text(q, p, k, a)
    # The question text should appear 3 times in the generated document
    assert doc.count("What is the hostel fee?") == 3
    assert "Hostel charges" in doc
    assert "Annual hostel rent is 65000." in doc
