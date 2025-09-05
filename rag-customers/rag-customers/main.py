from fastapi import FastAPI
from app.routes import query, feedback, health

app = FastAPI()

app.include_router(query.router)
app.include_router(feedback.router)
app.include_router(health.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG-Powered Support Bot API!"}