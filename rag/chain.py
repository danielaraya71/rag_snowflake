from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from rag.prompt import SYSTEM_PROMPT, USER_PROMPT
from rag.citations import build_context
from retrieval.retriever import retrieve

client = OpenAI()

MODEL = "gpt-4o-mini"

def rag_answer(question: str, top_k: int = 5):
    # 1. Retrieve context
    retrieved_chunks = retrieve(question, top_k=top_k)

    # 2. Build context string
    context = build_context(retrieved_chunks)

    # 3. Call LLM
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

    answer = response.choices[0].message.content

    return {
        "question": question,
        "answer": answer,
        "sources": [
            chunk["metadata"] for chunk in retrieved_chunks
        ]
    }


if __name__ == "__main__":
    result = rag_answer("How does time travel work in Snowflake?")
    print(result["answer"])
