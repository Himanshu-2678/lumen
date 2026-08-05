from sqlalchemy.orm import Session

from app.services.pdf_parser_service import extract_text_from_pdf
from app.services.chunking_service import chunk_pages
from app.services.metadata_services import enrich_chunk_metadata
from app.services.chunk_service import save_chunks
from app.services.embedding_service import generate_embeddings
from app.services.vector_store_service import add_chunks_to_vector_store


def ingest_document(
    db: Session,
    document_id: int,
    filename: str,
    file_path: str,
):
    """
    Complete document ingestion pipeline.

    Steps:
    1. Parse PDF
    2. Create chunks
    3. Add metadata
    4. Save chunks to PostgreSQL
    5. Generate embeddings
    6. Store vectors in ChromaDB
    """

    # Parse PDF
    pages = extract_text_from_pdf(file_path)

    # Chunk pages
    chunks = chunk_pages(pages)

    # Add metadata
    chunks = enrich_chunk_metadata(
        chunks=chunks,
        document_id=document_id,
        filename=filename,
    )

    # Save chunks to PostgreSQL
    save_chunks(
        db=db,
        chunks=chunks,
    )

    # Generate embeddings
    chunks = generate_embeddings(chunks)

    # Store vectors in ChromaDB
    add_chunks_to_vector_store(chunks)