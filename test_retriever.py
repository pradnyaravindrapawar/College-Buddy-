"""Unit tests for Hybrid Retriever functionality."""

import pytest
import os
import pandas as pd
from app.retriever import FAQRetriever


@pytest.fixture(scope="module")
def initialized_retriever():
    """Fixture providing an initialized FAQRetriever instance."""
    retriever = FAQRetriever()
    retriever.initialize()
    return retriever


def test_retriever_initialization(initialized_retriever):
    """Verify that dataframe and vocabulary are correctly loaded."""
    assert initialized_retriever.is_ready is True
    assert len(initialized_retriever.df) >= 20
    assert initialized_retriever.tfidf_matrix is not None
    assert initialized_retriever.tfidf_matrix.shape[0] == len(initialized_retriever.df)


def test_retriever_categories(initialized_retriever):
    """Verify categories extracted from sample FAQs."""
    categories = initialized_retriever.get_categories()
    assert "Admission Process" in categories
    assert "Fees, Refunds and Cancellation" in categories
    assert "Technology Programs" in categories
    assert "Arts Programs" in categories
    assert "About the College" in categories


def test_retrieval_exact_and_semantic_query(initialized_retriever):
    """Verify high retrieval match for cancellation deduction inquiry."""
    result = initialized_retriever.retrieve("What are cancellation deductions before the term starts?")
    assert result["top_match"] is not None
    assert result["is_confident"] is True
    assert result["top_match"]["category"] == "Fees, Refunds and Cancellation"
    assert result["top_score"] >= 0.35


def test_category_filtering(initialized_retriever):
    """Verify that category filtering restricts matches to the chosen domain."""
    result = initialized_retriever.retrieve(
        query="What is deducted up to 20 days after the term starts?",
        category="Fees, Refunds and Cancellation"
    )
    assert result["top_match"] is not None
    assert result["top_match"]["category"] == "Fees, Refunds and Cancellation"


def test_out_of_scope_query_low_confidence(initialized_retriever):
    """Verify out-of-scope query yields low confidence below threshold."""
    result = initialized_retriever.retrieve("How do I make chocolate chip cookies on Mars?")
    # Out of scope queries should have low hybrid score
    assert result["top_score"] < 0.35
    assert result["is_confident"] is False
