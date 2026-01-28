import json
from evaluation.evaluate import evaluate_question
from rag.chain import rag_answer


def main():
    with open("evaluation/dataset.json") as f:
        dataset = json.load(f)

    results = []

    for item in dataset:
        result = evaluate_question(rag_answer, item)
        results.append(result)
        print(f"✓ {item['id']} → score {result['score']}")

    summary = {
        "avg_score": round(sum(r["score"] for r in results) / len(results), 2),
        "avg_latency": round(sum(r["latency_sec"] for r in results) / len(results), 2),
        "results": results
    }

    with open("evaluation/results.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("\nEvaluation finished")
    print(summary)


if __name__ == "__main__":
    main()
