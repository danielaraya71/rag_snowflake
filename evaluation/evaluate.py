import time

def keyword_score(answer: str, keywords: list[str]) -> float:
    answer_lower = answer.lower()
    hits = sum(1 for k in keywords if k.lower() in answer_lower)
    return hits / len(keywords)


def evaluate_question(rag_fn, item):
    start = time.time()

    result = rag_fn(item["question"])

    latency = time.time() - start
    answer = result["answer"]

    score = keyword_score(answer, item["expected_keywords"])

    return {
        "id": item["id"],
        "question": item["question"],
        "score": round(score, 2),
        "latency_sec": round(latency, 2)
    }
