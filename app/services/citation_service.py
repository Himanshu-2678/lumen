def build_citations(
    retrieved_chunks: list[dict],
    citation_ids: list[str],
):
    citations = []
    seen = set()
    citation_ids = set(citation_ids)

    for chunk in retrieved_chunks:
        if chunk.get("id") not in citation_ids:
            continue

        metadata = chunk.get("metadata", {})
        filename = metadata.get("filename", "unknown")
        page_number = metadata.get("page_number", 0)

        key = (filename, page_number, chunk.get("id"))

        if key in seen:
            continue

        seen.add(key)

        citations.append({
            "filename": filename,
            "page_number": page_number,
            "quote": chunk.get("text", "")[:500],
        })

    return citations