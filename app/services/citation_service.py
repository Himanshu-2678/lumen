def build_citations(
    retrieved_chunks: list[dict],
    citation_ids: list[str],
):
    citations = []
    seen = set()
    citation_ids = set(citation_ids)

    for chunk in retrieved_chunks:
        chunk_id = chunk.get("id")

        if chunk_id not in citation_ids:
            continue

        metadata = chunk.get(
            "metadata",
            {}
        )
        filename = metadata.get(
            "filename",
            "unknown"
        )
        page_number = metadata.get(
            "page_number",
            0
        )
        quote = chunk.get(
            "text",
            ""
        )
        citation_key = (
            filename,
            page_number,
            chunk_id
        )
        if citation_key in seen:
            continue
        seen.add(
            citation_key
        )
        citations.append(
            {
                "filename": filename,
                "page_number": page_number,
                "quote": quote[:500],
            }
        )
    return citations