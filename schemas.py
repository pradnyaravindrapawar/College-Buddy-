"""Pydantic schemas and data contracts for College FAQ Chatbot.

All request and response structures are strongly typed to enforce
input validation, prevent malformed payloads, and document API contracts.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator


class ChatMessage(BaseModel):
    """Historical conversation turn."""
    role: Literal["user", "assistant"]
    content: str = Field(..., max_length=1000)


class ChatRequest(BaseModel):
    """Payload sent by the frontend for student queries."""
    message: str = Field(..., min_length=1, max_length=500, description="User's query (max 500 characters)")
    category: Optional[str] = Field(default=None, description="Optional category filter e.g. Admissions, Hostel")
    history: Optional[List[ChatMessage]] = Field(default_factory=list, description="Prior conversation messages")

    @field_validator("message")
    @classmethod
    def strip_and_validate_message(cls, v: str) -> str:
        clean = v.strip()
        if not clean:
            raise ValueError("Query message cannot be blank or pure whitespace.")
        return clean


class MatchItem(BaseModel):
    """Detailed score breakdown for a retrieved FAQ candidate."""
    id: int
    question: str
    category: str
    hybrid: float
    tfidf: float
    embedding: float


class ChatResponse(BaseModel):
    """Standardized response delivered to the frontend chat UI."""
    answer: str
    source: Literal["retrieval", "llm", "fallback"]
    confidence: float
    matches: List[MatchItem]
    suggestions: List[str]
    query_tokens: List[str]
    log_id: Optional[int] = None


class FeedbackRequest(BaseModel):
    """User rating (thumbs up / thumbs down) for an answer."""
    log_id: int = Field(..., description="Query log identifier returned in ChatResponse")
    helpful: bool = Field(..., description="True if answer was helpful, False otherwise")


class FAQItem(BaseModel):
    """Full representation of a single FAQ in the college database."""
    id: int
    category: str
    question: str
    answer: str
    paraphrases: str = ""
    keywords: str = ""
    source_url: str = ""
    last_updated: str = ""


class FAQCreateUpdateRequest(BaseModel):
    """Payload for creating or updating an FAQ via the Admin Panel."""
    category: str = Field(..., min_length=1, max_length=100)
    question: str = Field(..., min_length=5, max_length=300)
    answer: str = Field(..., min_length=5, max_length=2000)
    paraphrases: Optional[str] = ""
    keywords: Optional[str] = ""
    source_url: Optional[str] = ""


class UnansweredQuerySummary(BaseModel):
    """Aggregated statistics for questions that triggered low confidence."""
    query: str
    count: int
    avg_confidence: float
    last_seen: str


class HealthResponse(BaseModel):
    """System health and diagnostic status."""
    status: str
    faqs_count: int
    model_loaded: bool
    categories: List[str]
