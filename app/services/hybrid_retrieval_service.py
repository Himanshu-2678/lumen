from app.db.session import SessionLocal

from app.services.retrieval_service import retrieve_chunks
from app.services.bm25_service import bm25_search
from app.services.reranker_service import rerank_chunks


def hybrid_search(
    query: str,
    vector_top_k: int = 20,
    bm25_top_k: int = 20,
    final_top_k: int = 5,
    workspace_id: str | None = None,
):
    # Semantic Retrieval
    vector_results = retrieve_chunks(
        query=query,
        top_k=vector_top_k,
        workspace_id=workspace_id,
    )

    # Keyword Retrieval
    db = SessionLocal()
    try:
        bm25_results = bm25_search(
            db=db,
            query=query,
            workspace_id=workspace_id,
            top_k=bm25_top_k,
        )
    finally:
        db.close()

    merged = {}

    for chunk in vector_results:
        merged[chunk["id"]] = {
            **chunk,
            "retrieval_method": ["vector"],
        }

    for chunk in bm25_results:
        if chunk["id"] in merged:
            merged[chunk["id"]]["retrieval_method"].append("bm25")
        else:
            merged[chunk["id"]] = {
                **chunk,
                "retrieval_method": ["bm25"],
            }

    merged_chunks = list(merged.values())

    final_chunks = rerank_chunks(
        query=query,
        retrieved_chunks=merged_chunks,
        top_k=final_top_k,
    )

    return final_chunks
