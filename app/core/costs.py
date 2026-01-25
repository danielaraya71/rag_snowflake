MODEL_COSTS = {
    "gpt-4o-mini": {
        "prompt": 0.00015 / 1000,
        "completion": 0.0006 / 1000
    },
    "text-embedding-3-small": {
        "prompt": 0.02 / 1_000_000
    }
}

def calculate_llm_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    costs = MODEL_COSTS.get(model)
    if not costs:
        return 0.0

    prompt_cost = prompt_tokens * costs.get("prompt", 0)
    completion_cost = completion_tokens * costs.get("completion", 0)

    return round(prompt_cost + completion_cost, 6)
