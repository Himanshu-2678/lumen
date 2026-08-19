from sqlalchemy.orm import Session

from app.core.logging import logger
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
    workspace_id: str,
):
    """
    Complete document ingestion pipeline.

    Steps:
    1. Parse PDF
    2. Create chunks
    3. Add metadata
    4. Save chunks to database
    5. Generate embeddings
    6. Store vectors in ChromaDB
    """
    logger.info(f"Starting ingestion for document {document_id}")

    pages = extract_text_from_pdf(file_path)
    logger.info(f"Extracted {len(pages)} pages")

    chunks = chunk_pages(pages)
    logger.info(f"Created {len(chunks)} chunks")

    chunks = enrich_chunk_metadata(
        chunks=chunks,
        document_id=document_id,
        filename=filename,
        workspace_id=workspace_id,
    )

    save_chunks(db=db, chunks=chunks)
    logger.info("Chunks saved to database")

    chunks = generate_embeddings(chunks)
    logger.info("Embeddings generated")

    add_chunks_to_vector_store(chunks)
    logger.info("Vectors stored successfully")

    return len(chunks)