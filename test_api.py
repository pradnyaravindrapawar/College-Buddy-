"""Integration and API tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app, ADMIN_TOKEN


@pytest.fixture(scope="module")
def client():
    """Create a test client wrapping the FastAPI application."""
    with TestClient(app) as test_client:
        yield test_client


def test_health_endpoint(client):
    """Verify health check response."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["faqs_count"] >= 20
    assert data["model_loaded"] is True
    assert "Admission Process" in data["categories"]


def test_categories_endpoint(client):
    """Verify category list response."""
    response = client.get("/api/categories")
    assert response.status_code == 200
    cats = response.json().get("categories", [])
    assert len(cats) >= 5
    assert "Fees, Refunds and Cancellation" in cats or "Admission Process" in cats


def test_chat_endpoint_valid_query(client):
    """Verify chat query answering and match structure."""
    payload = {
        "message": "What is the eligibility for B.Sc. Information Technology?",
        "category": None,
        "history": []
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["source"] in ["retrieval", "llm"]
    assert data["confidence"] > 0.35
    assert len(data["matches"]) >= 1
    assert "query_tokens" in data
    assert data["log_id"] is not None
    assert "mathematics" in data["answer"].lower() or "45%" in data["answer"]


def test_chat_multi_turn_handling(client):
    """Verify short follow-up (<4 words) leverages prior conversation context."""
    payload = {
        "message": "and after September 30?",
        "category": None,
        "history": [
            {"role": "user", "content": "What are the fees deduction rules for admission cancellation?"},
            {"role": "assistant", "content": "Admission cancellation and refunds follow University of Mumbai Circular UG/412 of 2008."}
        ]
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "refund" in data["answer"].lower() or "deduction" in data["answer"].lower() or data["confidence"] > 0.35


def test_chat_fallback_for_out_of_scope(client):
    """Verify confidence gating triggers fallback message and suggestion chips."""
    payload = {
        "message": "What is the airspeed velocity of an unladen swallow?",
        "category": None,
        "history": []
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["source"] == "fallback"
    assert "not sure" in data["answer"].lower()
    assert len(data["suggestions"]) > 0


def test_feedback_submission(client):
    """Verify submitting thumbs up / down feedback."""
    # First generate a chat query to get a valid log_id
    chat_res = client.post("/api/chat", json={"message": "What is the placement average package?"})
    log_id = chat_res.json()["log_id"]
    assert log_id is not None

    # Submit positive feedback
    fb_res = client.post("/api/feedback", json={"log_id": log_id, "helpful": True})
    assert fb_res.status_code == 200
    assert fb_res.json()["status"] == "success"


def test_admin_auth_rejection(client):
    """Verify that unauthorized requests to admin endpoints are blocked."""
    # No header
    res1 = client.get("/api/admin/unanswered")
    assert res1.status_code == 401

    # Wrong token
    res2 = client.get("/api/admin/unanswered", headers={"Authorization": "Bearer wrong-token"})
    assert res2.status_code == 403


def test_admin_authorized_retrain_and_unanswered(client):
    """Verify admin endpoints succeed with valid bearer token."""
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}

    # Test unanswered query log fetch
    res_unanswered = client.get("/api/admin/unanswered", headers=headers)
    assert res_unanswered.status_code == 200
    data = res_unanswered.json()
    assert "unanswered" in data
    assert "feedback_stats" in data

    # Test retraining trigger
    res_retrain = client.post("/api/admin/retrain", headers=headers)
    assert res_retrain.status_code == 200
    assert res_retrain.json()["status"] == "success"
