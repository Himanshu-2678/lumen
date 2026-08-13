from app.vectorstore.chroma_client import collection
from app.core.logging import logger

def add_chunks_to_vector_store(
    chunks: list[dict],
):
    if not chunks:
        return

    document_id = chunks[0]["document_id"]

    collection.delete(where={"document_id": document_id})

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for chunk in chunks:
        chunk_id = (
            f"document_{chunk['document_id']}"
            f"_chunk_{chunk['chunk_index']}"
        )

        ids.append(chunk_id)
        documents.append(chunk["text"])
        embeddings.append(chunk["embedding"])

        metadatas.append({
            "document_id": chunk["document_id"],
            "filename": chunk["filename"],
            "page_number": chunk["page_number"],
            "chunk_index": chunk["chunk_index"],
        })

    if len(ids) != len(set(ids)):
        logger.warning("Duplicate chunk IDs detected")

    logger.info(f"Adding {len(ids)} vectors to ChromaDB")

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    logger.info("Chroma insert successful")