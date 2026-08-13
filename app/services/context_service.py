MAX_CONTEXT_CHARS = 12000

def build_context(
    retrieved_chunks: list[dict],
) -> str:
    contexts = []
    total_length = 0

    for chunk in retrieved_chunks:
        metadata = chunk.get("metadata", {})

        context = f"""
[Source ID: {chunk.get("id")}]
Document: {metadata.get("filename", "unknown")}
Page: {metadata.get("page_number", 0)}

Evidence:
{chunk.get("text", "")}
"""

        if total_length + len(context) > MAX_CONTEXT_CHARS:
            break

        contexts.append(context)
        total_length += len(context)

    return "\n\n".join(contexts)