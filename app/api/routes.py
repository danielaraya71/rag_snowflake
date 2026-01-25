from fastapi import APIRouter
from app.models.schemas import QueryRequest, QueryResponse
from rag.chain import rag_answer
import time

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    start = time.time()

    result = rag_answer(
        question=request.question,
        top_k=request.top_k
    )

    latency = round((time.time() - start) * 1000, 2)

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "latency_ms": latency
    }

@router.get("/health")
def health():
    return {"status": "ok"}
