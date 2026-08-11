from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.services.file_service import save_uploaded_file
from app.services.document_service import create_document, get_document_by_hash
from app.services.document_ingestion_service import ingest_document
from app.services.hash_service import calculate_file_hash
from app.models.chunk import Chunk
from app.vectorstore.chroma_client import collection
import os


def upload_document(db: Session, file: UploadFile):
    file_path = save_uploaded_file(file)
    document_hash = calculate_file_hash(file_path)
    existing_document = get_document_by_hash(db, document_hash)

    if existing_document:
        return existing_document

    document = create_document(
        db=db,
        filename=file.filename,
        file_type=file.filename.split(".")[-1],
        file_path=file_path,
        document_hash=document_hash,
        status="processing",
    )

    try:
        chunk_count = ingest_document(
            db=db,
            document_id=document.id,
            filename=document.filename,
            file_path=document.file_path,
        )

        document.status = "indexed"
        document.chunk_count = chunk_count

    except Exception as e:

        document.status = "failed"
        document.error_message = str(e)

        db.query(Chunk).filter(
            Chunk.document_id == document.id
        ).delete(
            synchronize_session=False
        )

        collection.delete(
            where={
                "document_id": document.id
            }
        )

        print(
            f"Document ingestion failed for {document.id}: {e}"
        )
        
    db.commit()
    db.refresh(document)

    return document