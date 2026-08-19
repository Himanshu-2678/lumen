from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.services.file_service import save_uploaded_file
from app.services.document_service import create_document, get_document_by_hash
from app.services.document_ingestion_service import ingest_document
from app.services.hash_service import calculate_file_hash
from app.models.chunk import Chunk
from app.vectorstore.chroma_client import collection

def upload_document(db: Session, file: UploadFile, workspace_id: str):
    
    if not file.filename.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are supported")

    file_path = save_uploaded_file(file)
    document_hash = calculate_file_hash(file_path)

    existing_document = get_document_by_hash(db, document_hash, workspace_id)

    if existing_document:
        return existing_document

    document = create_document(
        db=db,
        filename=file.filename,
        file_type="pdf",
        file_path=file_path,
        document_hash=document_hash,
        workspace_id=workspace_id,
        status="processing",
    )

    try:
        chunk_count = ingest_document(
            db=db,
            document_id=document.id,
            filename=document.filename,
            file_path=document.file_path,
            workspace_id=workspace_id,
        )

        document.status = "indexed"
        document.chunk_count = chunk_count

    except Exception as e:
        document.status = "failed"
        document.error_message = str(e)

        db.query(Chunk).filter(
            Chunk.document_id == document.id,
            Chunk.workspace_id == workspace_id,
        ).delete(synchronize_session=False)

        try:
            collection.delete(where={"document_id": document.id})
        except Exception:
            pass

    db.commit()
    db.refresh(document)
    return document