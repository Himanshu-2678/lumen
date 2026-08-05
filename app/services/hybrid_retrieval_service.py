from app.db.session import SessionLocal

from app.services.retrieval_service import retrieve_chunks
from app.services.bm25_service import bm25_search
from app.services.reranker_service import rerank_chunks


def hybrid_search(
    query: str,
    vector_top_k: int = 20,
    bm25_top_k: int = 20,
    final_top_k: int = 5,
):
    db = SessionLocal()

    try:
        # Semantic Retrieval
        vector_results = retrieve_chunks(
            query=query,
            top_k=vector_top_k,
        )

        # Keyword Retrieval
        bm25_results = bm25_search(
            db=db,
            query=query,
            top_k=bm25_top_k,
        )

    finally:
        db.close()

    # Merge results (remove duplicates)
    merged = {}

    for chunk in vector_results:
        merged[chunk["id"]] = chunk

    for chunk in bm25_results:
        if chunk["id"] not in merged:
            merged[chunk["id"]] = chunk

    merged_chunks = list(merged.values())

    # Final reranking
    final_chunks = rerank_chunks(
        query=query,
        retrieved_chunks=merged_chunks,
        top_k=final_top_k,
    )

    return final_chunks