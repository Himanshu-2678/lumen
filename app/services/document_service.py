from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.chunk import Chunk
from app.vectorstore.chroma_client import collection
import os

def create_document(db: Session, filename: str, file_type: str, file_path: str, document_hash: str, workspace_id: str, status: str = "processing") -> Document:
    document = Document(
        filename=filename,
        file_type=file_type,
        file_path=file_path,
        document_hash=document_hash,
        workspace_id=workspace_id,
        status=status
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document

def get_document_by_hash(db: Session, document_hash: str, workspace_id: str):
    return db.query(Document).filter(
        Document.document_hash == document_hash,
        Document.workspace_id == workspace_id,
    ).first()

def update_document_status(db: Session, document_id: int, status: str, chunk_count: int):
    document = db.query(Document).filter(Document.id == document_id).first()
    if document:
        document.status = status
        document.chunk_count = chunk_count
        db.commit()
        db.refresh(document)
    return document

def get_documents(db: Session, workspace_id: str):
    return db.query(Document).filter(Document.workspace_id == workspace_id).all()

def get_document(db: Session, document_id: int, workspace_id: str):
    return db.query(Document).filter(
        Document.id == document_id,
        Document.workspace_id == workspace_id,
    ).first()

def delete_document(db: Session, document_id: int, workspace_id: str):
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.workspace_id == workspace_id,
    ).first()
    if not document:
        return None

    try:
        if os.path.exists(document.file_path):
            os.remove(document.file_path)

        collection.delete(where={"document_id": document_id})

        db.query(Chunk).filter(
            Chunk.document_id == document_id
        ).delete(synchronize_session=False)

        db.delete(document)
        db.commit()
        return document

    except Exception as e:
        db.rollback()
        raise e