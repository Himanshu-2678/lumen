from rank_bm25 import BM25Okapi
from sqlalchemy.orm import Session

from app.models.chunk import Chunk


def bm25_search(
    db: Session,
    query: str,
    top_k: int = 20,
):
    chunks = db.query(Chunk).all()

    if not chunks:
        return []

    tokenized_corpus = [
        chunk.text.lower().split()
        for chunk in chunks
    ]

    bm25 = BM25Okapi(tokenized_corpus)

    tokenized_query = query.lower().split()

    scores = bm25.get_scores(tokenized_query)

    ranked_chunks = []

    for chunk, score in zip(chunks, scores):
        ranked_chunks.append(
            {
                "id": f"document_{chunk.document_id}_chunk_{chunk.chunk_index}",
                "text": chunk.text,
                "metadata": {
                    "document_id": chunk.document_id,
                    "filename": chunk.filename,
                    "page_number": chunk.page_number,
                    "chunk_index": chunk.chunk_index,
                },
                "bm25_score": float(score),
            }
        )

    ranked_chunks.sort(
        key=lambda chunk: chunk["bm25_score"],
        reverse=True,
    )

    return ranked_chunks[:top_k]