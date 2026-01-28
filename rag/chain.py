from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from rag.prompt import SYSTEM_PROMPT, USER_PROMPT
from rag.citations import build_context
from retrieval.retriever import retrieve
from app.core.logging import get_logger
from app.core.costs import calculate_llm_cost
import time

client = OpenAI()
logger = get_logger("rag")

MODEL = "gpt-4o-mini"

def rag_answer(question: str, top_k: int = 5):
    start_time = time.time()

    retrieved_chunks = retrieve(question, top_k=top_k)
    context = build_context(retrieved_chunks)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": USER_PROMPT.format(
                    context=context,
                    question=question
                )
            }
        ],
        temperature=0
    )

    usage = response.usage
    latency_ms = round((time.time() - start_time) * 1000, 2)

    cost = calculate_llm_cost(
        model=MODEL,
        prompt_tokens=usage.prompt_tokens,
        completion_tokens=usage.completion_tokens
    )

    logger.info(
        "rag_request",
        extra={
            "extra": {
                "question": question,
                "top_k": top_k,
                "latency_ms": latency_ms,
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
                "cost_usd": cost,
                "sources": [c["metadata"]["doc"] for c in retrieved_chunks]
            }
        }
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": [c["metadata"] for c in retrieved_chunks],
        "latency_ms": latency_ms,
        "cost_usd": cost,
        "tokens": usage.total_tokens
    }


if __name__ == "__main__":
    result = rag_answer("What is zero-copy cloning in Snowflake?")
    print(result["answer"])
