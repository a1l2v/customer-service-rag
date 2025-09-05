import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_query_success():
    response = client.post("/query", json={
        "query": "How do I reset my password?",
        "user_id": 42,
        "product_id": 1001
    })
    assert response.status_code == 200
    assert "answer" in response.json()
    assert "sources" in response.json()

def test_query_invalid_product():
    response = client.post("/query", json={
        "query": "How do I reset my password?",
        "user_id": 42,
        "product_id": 9999  # Assuming this product_id does not exist
    })
    assert response.status_code == 404  # Assuming the API returns 404 for invalid product_id

def test_query_missing_fields():
    response = client.post("/query", json={
        "query": "How do I reset my password?"
        # Missing user_id and product_id
    })
    assert response.status_code == 422  # Unprocessable Entity for missing fields

def test_query_feedback_integration():
    # First, simulate a query
    query_response = client.post("/query", json={
        "query": "How do I reset my password?",
        "user_id": 42,
        "product_id": 1001
    })
    qa_history_id = query_response.json().get("sources", {}).get("qa_history")

    # Now, provide feedback
    feedback_response = client.post("/feedback", json={
        "query": "How do I reset my password?",
        "qa_history": qa_history_id,
        "solution": "Visit settings → security → reset password",
        "product_id": 1001,
        "user_id": 42
    })
    assert feedback_response.status_code == 200
    assert "message" in feedback_response.json()