def build_citations(retrieved_chunks: list[dict], citation_ids: list[str]):
    citations = []
    seen = set()

    for chunk in retrieved_chunks:
        if chunk["id"] not in citation_ids:
            continue

        metadata = chunk["metadata"]

        key = (
            metadata["filename"],
            metadata["page_number"],
            chunk["id"],
        )

        if key in seen:
            continue

        seen.add(key)

        citations.append(
            {
                "filename": metadata["filename"],
                "page_number": metadata["page_number"],
                "quote": chunk["text"],
            }
        )

    return citations