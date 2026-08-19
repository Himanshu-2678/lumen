from typing import List

def enrich_chunk_metadata(chunks, document_id, filename, workspace_id):

    enriched_chunks = []

    for chunk in chunks:
        enriched_chunks.append(
            {
                **chunk,
                "document_id": document_id,
                "filename": filename,
                "workspace_id": workspace_id,
            })
        
    return enriched_chunks