from app.services.embedding_service import model
from app.vectorstore.chroma_client import collection

def generate_query_embedding(query: str):
    return model.encode(
        query,
        normalize_embeddings=True,
    ).tolist()

def vector_search(
    query_embedding,
    top_k: int = 20,
    document_id: int | None = None,
    filename: str | None = None,
    workspace_id: str | None = None,
):
    where = None

    if document_id is not None:
        where = {"document_id": document_id}
    elif filename is not None:
        where = {"filename": filename}

    if workspace_id is not None:
        where = {"workspace_id": workspace_id}

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where,
    )

def retrieve_chunks(
    query: str,
    top_k: int = 20,
    document_id: int | None = None,
    filename: str | None = None,
    workspace_id: str | None = None,
):
    query_embedding = generate_query_embedding(query)

    results = vector_search(
        query_embedding=query_embedding,
        top_k=top_k,
        document_id=document_id,
        filename=filename,
        workspace_id=workspace_id,
    )

    if not results["ids"] or not results["ids"][0]:
        return []

    retrieved_chunks = [
        {
            "id": chunk_id,
            "text": text,
            "metadata": metadata,
            "distance": distance,
        }
        for chunk_id, text, metadata, distance in zip(
            results["ids"][0],
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]

    return retrieved_chunks