from typing import List

def enrich_chunk_metadata(chunks, document_id, filename):

    enriched_chunks = []

    for chunk in chunks:
        enriched_chunks.append(
            {**chunk, "document_id": document_id, "filename": filename})
        
    return enriched_chunks