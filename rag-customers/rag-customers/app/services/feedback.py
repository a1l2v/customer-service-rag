from datetime import datetime
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import get_supabase_client

Base = declarative_base()

class QAHistory(Base):
    __tablename__ = 'qa_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer)
    query_text = Column(String)
    query_embedding = Column(Float)  # Assuming FLOAT_VECTOR is represented as Float
    solution_text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

def save_feedback(product_id: int, query_text: str, query_embedding: list, solution_text: str) -> Optional[int]:
    supabase = get_supabase_client()
    existing_entry = supabase.table('qa_history').select('id').eq('query_text', query_text).eq('product_id', product_id).execute()

    if existing_entry.data:
        return None  # Feedback is not unique, do not save

    new_entry = {
        'product_id': product_id,
        'query_text': query_text,
        'query_embedding': query_embedding,
        'solution_text': solution_text,
        'created_at': datetime.utcnow()
    }

    response = supabase.table('qa_history').insert(new_entry).execute()
    return response.data[0]['id'] if response.data else None