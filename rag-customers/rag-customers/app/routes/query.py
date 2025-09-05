from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse
from app.services.embeddings import generate_embedding
from app.services.llm import generate_answer
from app.services.search import search_product_kb, search_user_kb, search_qa_history

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    try:
        # Step 1: Embed the user query
        query_embedding = generate_embedding(request.query)

        # Step 2: Perform searches in the respective knowledge bases
        product_results = search_product_kb(request.product_id, query_embedding)
        user_results = search_user_kb(request.user_id)
        qa_results = search_qa_history(request.product_id)

        # Step 3: Assemble context from the search results
        context = product_results + user_results + qa_results

        # Step 4: Generate an answer using the LLM
        answer = generate_answer(request.query, context)

        return QueryResponse(answer=answer, sources={
            "product_kb": product_results,
            "user_kb": user_results,
            "qa_history": qa_results,
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))