from pydantic import BaseModel
from typing import Optional, List

class QueryRequest(BaseModel):
    query: str
    user_id: int
    product_id: int

class QueryResponse(BaseModel):
    answer: str
    sources: Optional[dict]

class FeedbackRequest(BaseModel):
    query: str
    qa_history: int
    solution: str
    product_id: int
    user_id: int

class FeedbackResponse(BaseModel):
    message: str
    qa_history_id: int