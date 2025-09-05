from fastapi import APIRouter, HTTPException
from app.models.schemas import FeedbackRequest, FeedbackResponse
from app.services.feedback import save_feedback

router = APIRouter()

@router.post("/feedback", response_model=FeedbackResponse)
async def feedback(feedback_request: FeedbackRequest):
    try:
        feedback_id = await save_feedback(feedback_request)
        return {"message": "Feedback saved into qa_history", "qa_history_id": feedback_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))