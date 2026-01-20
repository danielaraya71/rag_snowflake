def build_context(retrieved_chunks: list[dict]) -> str:
    """
    Builds a context string with inline source markers.
    """
    context_blocks = []

    for i, chunk in enumerate(retrieved_chunks):
        source = chunk["metadata"]["doc"]
        block = f"""
[source: {source}, chunk: {i}]
{chunk["text"]}
"""
        context_blocks.append(block.strip())

    return "\n\n".join(context_blocks)
