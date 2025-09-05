import pytest
from app.services.feedback import save_feedback
from app.models.schemas import FeedbackRequest
from app.database import get_qa_history, insert_qa_history

@pytest.fixture
def feedback_data():
    return FeedbackRequest(
        query="How do I reset my password?",
        qa_history=1,
        solution="Visit settings → security → reset password",
        product_id=1001,
        user_id=42
    )

def test_save_feedback_new(feedback_data):
    response = save_feedback(feedback_data)
    assert response['message'] == "Feedback saved into qa_history"
    assert response['qa_history_id'] is not None

def test_save_feedback_duplicate(feedback_data):
    # Simulate inserting the same feedback
    insert_qa_history(feedback_data)
    response = save_feedback(feedback_data)
    assert response['message'] == "Feedback already exists, not saved"
    assert response.get('qa_history_id') is None

def test_save_feedback_not_working(feedback_data):
    feedback_data.solution = "This solution does not work"
    response = save_feedback(feedback_data)
    assert response['message'] == "Feedback discarded"