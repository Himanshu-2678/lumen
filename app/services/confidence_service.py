def calculate_confidence(reranked_chunks: list[dict]):

    if not reranked_chunks:
        return {
            "confidence_score": 0.0,
            "confidence_level": "low",
            "signals": {
                "reason": "No evidence retrieved",
            },
        }

    top_chunk = reranked_chunks[0]

    # Retrieval agreement
    methods = top_chunk.get("retrieval_method", [])
    retrieval_agreement = len(methods) >= 2
    agreement_score = 1.0 if retrieval_agreement else 0.5

    # Reranker quality
    top_score = top_chunk.get("reranker_score", -999)

    if top_score < 0:
        reranker_quality_score = 0.0
    else:
        reranker_quality_score = min(top_score / 10, 1)

    # Relative reranker strength
    reranker_strength = reranker_quality_score
    """if len(reranked_chunks) == 1:
        reranker_strength = reranker_quality_score
    else:
        second_score = reranked_chunks[1].get("reranker_score", -999)

        gap = top_score - second_score

        reranker_strength = min(max(gap / 5, 0), 1)

        reranker_strength *= reranker_quality_score"""

    # Evidence availability
    evidence_score = min(len(reranked_chunks) / 5, 1)

    confidence_score = (
        0.2 * agreement_score
        + 0.6 * reranker_strength
        + 0.2 * evidence_score
    )

    top_reranker_score = top_chunk.get("reranker_score")

    if top_reranker_score is not None and top_reranker_score < 0:
        level = "low"
    elif confidence_score >= 0.75:
        level = "high"
    elif confidence_score >= 0.45:  
        level = "medium"
    else:
        level = "low"

    return {
        "confidence_score": round(confidence_score, 3),
        "confidence_level": level,
        "signals": {
            "retrieval_agreement": retrieval_agreement,
            "retrieval_methods": methods,
            "supporting_chunks": len(reranked_chunks),
            "top_reranker_score": top_score,
        },
    }