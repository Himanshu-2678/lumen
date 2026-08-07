def build_context(retrieved_chunks: list[dict]) -> str:
    contexts = []

    for index, chunk in enumerate(retrieved_chunks, start=1):
        metadata = chunk["metadata"]

        context = f"""
        [Source ID: {chunk["id"]}]
        Document: {metadata["filename"]}
        Page: {metadata["page_number"]}

        Evidence:
        {chunk["text"]}
        """

        contexts.append(context)

    return "\n\n".join(contexts)