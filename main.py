"""FastAPI Application Entrypoint for College FAQ Chatbot.

Provides RESTful endpoints for:
- Student Chat with Hybrid Retrieval + Multi-turn context + Confidence thresholding
- User Feedback rating (thumbs up / down)
- FAQ and Category discovery
- Admin Management (CRUD, CSV upload, index retraining, unanswered query tracking)
"""

import os
import time
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from typing import Dict, List, Optional

import pandas as pd
from fastapi import FastAPI, HTTPException, Header, Depends, UploadFile, File, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.schemas import (
    ChatRequest,
    ChatResponse,
    MatchItem,
    FeedbackRequest,
    FAQItem,
    FAQCreateUpdateRequest,
    HealthResponse,
    UnansweredQuerySummary,
)
from app.db import init_db, log_query, update_feedback, get_frequent_unanswered, get_feedback_stats
from app.retriever import FAQRetriever, FAQS_CSV_PATH
from app.llm import rephrase_with_llm, is_llm_enabled
from app.nlp import load_synonyms
from scripts.validate_data import validate_faq_csv

# Global retriever instance
retriever = FAQRetriever()

# Rate limiting data structure: IP -> list of timestamps
RATE_LIMIT_STORE: Dict[str, List[float]] = {}
MAX_REQUESTS_PER_MINUTE = 30
RATE_WINDOW_SECONDS = 60.0

# Security token from environment
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "college-admin-supersecret-2026")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context: initialize DB and indexes on startup."""
    print("[Startup] Initializing SQLite database...")
    init_db()
    load_synonyms()
    print("[Startup] Initializing hybrid FAQ retriever and caching embeddings...")
    try:
        retriever.initialize()
    except Exception as e:
        print(f"[Startup Error] Failed to initialize retriever: {e}")
    yield
    print("[Shutdown] Cleaning up resources...")


app = FastAPI(
    title="CollegeBuddy - B.K.Birla College Chatbot API",
    description="CollegeBuddy: Intelligent AI chatbot providing verified information for B.K.Birla College with hybrid search and full explainability.",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
frontend_origins = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173").split(",")
frontend_origins = [o.strip() for o in frontend_origins if o.strip()]
# Include typical local development ports and allow wildcard regex for Vercel previews
app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins + ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def rate_limiting_middleware(request: Request, call_next):
    """Enforce rate limiting: 30 requests per minute per IP address."""
    # Exclude health check and options requests from rate limiting
    if request.url.path in ["/api/health", "/docs", "/openapi.json"] or request.method == "OPTIONS":
        return await call_next(request)

    client_ip = request.client.host if request.client else "unknown"
    now = time.time()

    timestamps = RATE_LIMIT_STORE.get(client_ip, [])
    # Filter out requests older than the rolling 60-second window
    recent_requests = [t for t in timestamps if now - t < RATE_WINDOW_SECONDS]

    if len(recent_requests) >= MAX_REQUESTS_PER_MINUTE:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Too many requests. Please slow down (limit: 30 requests per minute)."}
        )

    recent_requests.append(now)
    RATE_LIMIT_STORE[client_ip] = recent_requests
    return await call_next(request)


# Admin Authentication Dependency
def verify_admin_token(authorization: Optional[str] = Header(None)) -> bool:
    """Validate Bearer admin token in request headers."""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header."
        )
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization format. Use 'Bearer <TOKEN>'."
        )
    token = parts[1]
    if token != ADMIN_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or unauthorized admin token."
        )
    return True


# ==========================================
# PUBLIC CLIENT ENDPOINTS
# ==========================================

@app.get("/api/health", response_model=HealthResponse)
def health_check():
    """Health status and diagnostic info."""
    return HealthResponse(
        status="ok",
        faqs_count=len(retriever.df) if retriever.is_ready else 0,
        model_loaded=retriever.is_ready,
        categories=retriever.get_categories()
    )


@app.get("/api/categories")
def get_categories():
    """Retrieve all available FAQ categories."""
    return {"categories": retriever.get_categories()}


@app.get("/api/faqs")
def get_all_faqs():
    """Return all verified FAQs for catalog browsing."""
    return {"faqs": retriever.get_all_faqs()}


@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest):
    """Core chat inference endpoint.

    Applies:
    1. Multi-turn query enrichment (if follow-up < 4 words)
    2. Hybrid Retrieval (TF-IDF + FastEmbed)
    3. Category filtering
    4. Confidence gating (fallback to suggestions if top score < threshold)
    5. Grounded LLM rephrasing (if enabled)
    6. SQLite query logging with returned log_id
    """
    raw_query = payload.message.strip()
    effective_query = raw_query

    # Multi-turn handling (light):
    # If a follow-up is very short (under 4 words), prepend previous user query
    if payload.history and len(raw_query.split()) < 4:
        # Find the most recent user turn
        for turn in reversed(payload.history):
            if turn.role == "user" and turn.content.strip():
                prev_q = turn.content.strip()
                effective_query = f"{prev_q} {raw_query}"
                break

    # Execute Hybrid Retrieval
    retrieval_result = retriever.retrieve(
        query=effective_query,
        category=payload.category,
        top_k=3
    )

    matches = retrieval_result["matches"]
    top_match = retrieval_result["top_match"]
    top_score = retrieval_result["top_score"]
    is_confident = retrieval_result["is_confident"]
    query_tokens = retrieval_result["query_tokens"]

    converted_matches = [
        MatchItem(
            id=m["id"],
            question=m["question"],
            category=m["category"],
            hybrid=m["hybrid"],
            tfidf=m["tfidf"],
            embedding=m["embedding"]
        )
        for m in matches
    ]

    # CASE A: Low confidence (score below threshold, default 0.35)
    if not is_confident or top_match is None:
        fallback_msg = (
            "I'm not sure about that. Our official college records don't seem to cover your exact question. "
            "Did you mean one of these topics below?"
        )
        suggestions = [m["question"] for m in matches[:3]] if matches else []
        log_id = log_query(
            query=raw_query,
            category_filter=payload.category,
            matched_faq_id=top_match["id"] if top_match else None,
            score=top_score,
            source="fallback"
        )
        return ChatResponse(
            answer=fallback_msg,
            source="fallback",
            confidence=top_score,
            matches=converted_matches,
            suggestions=suggestions,
            query_tokens=query_tokens,
            log_id=log_id
        )

    # CASE B: High confidence
    answer_text = top_match["answer"]
    source = "retrieval"

    # Check if Anthropic LLM rephrasing is enabled
    if is_llm_enabled():
        llm_rephrase = rephrase_with_llm(
            query=raw_query,
            top_faqs=matches[:3]
        )
        if llm_rephrase:
            answer_text = llm_rephrase
            source = "llm"

    # Provide other matched FAQs as contextual follow-up chips
    suggestions = [m["question"] for m in matches[1:3]] if len(matches) > 1 else []

    log_id = log_query(
        query=raw_query,
        category_filter=payload.category,
        matched_faq_id=top_match["id"],
        score=top_score,
        source=source
    )

    return ChatResponse(
        answer=answer_text,
        source=source,
        confidence=top_score,
        matches=converted_matches,
        suggestions=suggestions,
        query_tokens=query_tokens,
        log_id=log_id
    )


@app.post("/api/feedback")
def submit_feedback(payload: FeedbackRequest):
    """Record user thumbs up / thumbs down satisfaction for an answer."""
    success = update_feedback(log_id=payload.log_id, helpful=payload.helpful)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat log record not found or already closed."
        )
    return {"status": "success", "message": "Feedback recorded. Thank you!"}


# ==========================================
# ADMIN ENDPOINTS (Protected)
# ==========================================

@app.get("/api/admin/unanswered", dependencies=[Depends(verify_admin_token)])
def get_unanswered_queries():
    """Retrieve frequent questions with low confidence or fallback status."""
    unanswered = get_frequent_unanswered(threshold=retriever.threshold, limit=30)
    stats = get_feedback_stats()
    return {
        "unanswered": unanswered,
        "feedback_stats": stats,
        "total_faqs": len(retriever.df)
    }


@app.post("/api/admin/faqs", dependencies=[Depends(verify_admin_token)])
def create_faq(item: FAQCreateUpdateRequest):
    """Add a new FAQ record, append to CSV, and refresh the retrieval index."""
    df = retriever.df.copy()
    new_id = int(df["id"].max() + 1) if not df.empty else 1
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    new_row = {
        "id": str(new_id),
        "category": item.category.strip(),
        "question": item.question.strip(),
        "answer": item.answer.strip(),
        "paraphrases": (item.paraphrases or "").strip(),
        "keywords": (item.keywords or "").strip(),
        "source_url": (item.source_url or "").strip(),
        "last_updated": today_str
    }

    # Append to existing DataFrame and save to CSV
    updated_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    updated_df.to_csv(FAQS_CSV_PATH, index=False)
    retriever.reload()

    return {"status": "success", "message": f"FAQ #{new_id} added successfully.", "id": new_id}


@app.put("/api/admin/faqs/{faq_id}", dependencies=[Depends(verify_admin_token)])
def update_faq(faq_id: int, item: FAQCreateUpdateRequest):
    """Modify an existing FAQ record and retrain indexes."""
    df = retriever.df.copy()
    if faq_id not in df["id"].values:
        raise HTTPException(status_code=404, detail=f"FAQ with id {faq_id} does not exist.")

    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    idx = df[df["id"] == faq_id].index[0]
    df.at[idx, "category"] = item.category.strip()
    df.at[idx, "question"] = item.question.strip()
    df.at[idx, "answer"] = item.answer.strip()
    df.at[idx, "paraphrases"] = (item.paraphrases or "").strip()
    df.at[idx, "keywords"] = (item.keywords or "").strip()
    df.at[idx, "source_url"] = (item.source_url or "").strip()
    df.at[idx, "last_updated"] = today_str

    df.to_csv(FAQS_CSV_PATH, index=False)
    retriever.reload()

    return {"status": "success", "message": f"FAQ #{faq_id} updated successfully."}


@app.delete("/api/admin/faqs/{faq_id}", dependencies=[Depends(verify_admin_token)])
def delete_faq(faq_id: int):
    """Delete an FAQ by ID and retrain indexes."""
    df = retriever.df.copy()
    if faq_id not in df["id"].values:
        raise HTTPException(status_code=404, detail=f"FAQ with id {faq_id} does not exist.")

    df = df[df["id"] != faq_id]
    df.to_csv(FAQS_CSV_PATH, index=False)
    retriever.reload()

    return {"status": "success", "message": f"FAQ #{faq_id} deleted successfully."}


@app.post("/api/admin/upload", dependencies=[Depends(verify_admin_token)])
async def upload_faq_csv(file: UploadFile = File(...)):
    """Upload a new FAQ CSV file, run full data validation, and replace current database."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are supported.")

    content = await file.read()
    temp_path = os.path.join(os.path.dirname(FAQS_CSV_PATH), "temp_uploaded_faqs.csv")

    try:
        with open(temp_path, "wb") as f:
            f.write(content)

        is_valid = validate_faq_csv(temp_path)
        if not is_valid:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise HTTPException(
                status_code=400,
                detail="Uploaded CSV failed schema or consistency validation. Check server logs for details."
            )

        # Replace live faqs.csv
        os.replace(temp_path, FAQS_CSV_PATH)
        retriever.reload()

        return {
            "status": "success",
            "message": "New FAQ dataset uploaded, validated, and indexed successfully.",
            "total_faqs": len(retriever.df)
        }
    except HTTPException:
        raise
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")


@app.post("/api/admin/retrain", dependencies=[Depends(verify_admin_token)])
def retrain_index():
    """Manually rebuild the TF-IDF vocabulary and recompute dense embeddings."""
    try:
        retriever.reload()
        return {
            "status": "success",
            "message": "Retrieval indexes retrained and reloaded successfully.",
            "total_faqs": len(retriever.df),
            "categories": retriever.get_categories()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrain failure: {str(e)}")
