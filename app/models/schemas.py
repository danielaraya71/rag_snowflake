from pydantic import BaseModel
from typing import Optional, List, Dict

class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 5

class QueryResponse(BaseModel):
    answer: str
    sources: list
    latency_ms: float
    cost_usd: float
    tokens: int