from sentence_transformers import CrossEncoder

_model = None

def get_reranker_model():
    global _model

    if _model is None:
        _model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    return _model


def rerank_chunks(
    query: str,
    retrieved_chunks: list[dict],
    top_k: int = 5,
):
    if not retrieved_chunks:
        return []

    model = get_reranker_model()

    sentence_pairs = [
        (query, chunk.get("text", ""))
        for chunk in retrieved_chunks
    ]

    scores = model.predict(sentence_pairs)

    reranked_chunks = []

    for chunk, score in zip(retrieved_chunks, scores):
        reranked_chunks.append({
            **chunk,
            "reranker_score": float(score),
        })

    reranked_chunks.sort(
        key=lambda chunk: chunk["reranker_score"],
        reverse=True,
    )

    return reranked_chunks[:top_k]
