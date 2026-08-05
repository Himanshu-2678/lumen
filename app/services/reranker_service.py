from sentence_transformers import CrossEncoder

model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_chunks(
    query: str,
    retrieved_chunks: list[dict],
    top_k: int = 5,
):
    if not retrieved_chunks:
        return []

    sentence_pairs = [
        (query, chunk["text"])
        for chunk in retrieved_chunks
    ]

    scores = model.predict(sentence_pairs)

    for chunk, score in zip(retrieved_chunks, scores):
        chunk["reranker_score"] = float(score)

    retrieved_chunks.sort(
        key=lambda chunk: chunk["reranker_score"],
        reverse=True,
    )

    return retrieved_chunks[:top_k]