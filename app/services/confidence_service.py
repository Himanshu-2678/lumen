def calculate_confidence(reranked_chunks: list[dict]):

    if not reranked_chunks:
        return {
            "confidence_score": 0.0,
            "confidence_level": "low",
            "signals": {
                "reason": "No evidence retrieved",
                "retrieval_similarity": 0.0,
                "supporting_chunks": 0,
                "metadata_verified": False,
                "citation_available": False,
                "quote_verified": False,
            },
        }


    top_chunk = reranked_chunks[0]


    # Retrieval agreement
    methods = top_chunk.get(
        "retrieval_method",
        []
    )

    retrieval_agreement = len(methods) >= 2

    agreement_score = (
        1.0
        if retrieval_agreement
        else 0.5
    )


    # Reranker quality
    top_score = top_chunk.get(
        "reranker_score",
        -999
    )


    if top_score < 0:

        reranker_quality_score = 0.0

    else:

        reranker_quality_score = min(
            top_score / 10,
            1
        )


    # Evidence availability
    supporting_chunks = len(
        reranked_chunks
    )

    evidence_score = min(
        supporting_chunks / 5,
        1
    )


    # Metadata verification
    metadata_verified = all(
        chunk.get("metadata", {}).get("filename")
        and chunk.get("metadata", {}).get("page_number")
        for chunk in reranked_chunks
    )


    metadata_score = (
        1.0
        if metadata_verified
        else 0.0
    )


    # Final confidence
    confidence_score = (
        0.30 * agreement_score
        + 0.45 * reranker_quality_score
        + 0.15 * evidence_score
        + 0.10 * metadata_score
    )


    if top_score is not None and top_score < 0:

        level = "low"

    elif confidence_score >= 0.75:

        level = "high"

    elif confidence_score >= 0.45:

        level = "medium"

    else:

        level = "low"



    return {
        "confidence_score": round(
            confidence_score,
            3
        ),

        "confidence_level": level,

        "signals": {

            "retrieval_agreement": retrieval_agreement,

            "retrieval_methods": methods,

            "supporting_chunks": supporting_chunks,

            "top_reranker_score": top_score,

            "metadata_verified": metadata_verified,

            "citation_available": False,

            "quote_verified": False,

        },
    }