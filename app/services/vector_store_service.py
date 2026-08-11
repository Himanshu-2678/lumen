from app.vectorstore.chroma_client import collection

def add_chunks_to_vector_store(chunks: list[dict]):
    if not chunks:
        return

    document_id = chunks[0]["document_id"]

    collection.delete(where={"document_id": document_id})

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for chunk in chunks:
        chunk_id = f"document_{chunk['document_id']}_chunk_{chunk['chunk_index']}"

        ids.append(chunk_id)
        documents.append(chunk["text"])
        embeddings.append(chunk["embedding"])

        metadatas.append({
            "document_id": chunk["document_id"],
            "filename": chunk["filename"],
            "page_number": chunk["page_number"],
            "chunk_index": chunk["chunk_index"]
        })

    print("TOTAL CHUNKS:", len(ids))
    print("UNIQUE IDS:", len(set(ids)))

    duplicates = [x for x in ids if ids.count(x) > 1]

    print("DUPLICATES:", set(duplicates))

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print("CHROMA INSERT SUCCESS")