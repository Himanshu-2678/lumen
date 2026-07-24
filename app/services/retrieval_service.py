from app.services.embedding_service import model
from app.vectorstore.chroma_client import collection


def retrieve_chunks(query: str, top_k: int = 5):
    query_embedding = model.encode(
        query,
        normalize_embeddings=True,
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    return [
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