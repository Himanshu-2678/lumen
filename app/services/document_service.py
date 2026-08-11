from sqlalchemy.orm import Session
from app.models.document import Document
import os
from app.vectorstore.chroma_client import collection
from app.models.chunk import Chunk

def create_document(db: Session, filename: str, file_type: str, file_path: str, document_hash: str, status: str = "processing") -> Document:
    document = Document(filename=filename, file_type=file_type, file_path=file_path, document_hash=document_hash, status=status)
    db.add(document)
    db.commit()
    db.refresh(document)
    return document

def get_document_by_hash(db: Session, document_hash: str):
    return db.query(Document).filter(Document.document_hash == document_hash).first()

def update_document_status(db: Session, document_id: int, status: str, chunk_count: int):
    document = db.query(Document).filter(Document.id == document_id).first()
    if document:
        document.status = status
        document.chunk_count = chunk_count
        db.commit()
        db.refresh(document)
    return document

def get_documents(db: Session):
    return db.query(Document).all()

def delete_document(
    db: Session,
    document_id: int,
):

    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        return None

    try:
        # Delete physical file
        if os.path.exists(document.file_path):
            os.remove(document.file_path)

        # Delete embeddings from ChromaDB
        collection.delete(
            where={
                "document_id": document_id
            }
        )

        # Delete chunks from PostgreSQL
        db.query(Chunk).filter(
            Chunk.document_id == document_id
        ).delete(
            synchronize_session=False
        )

        # Delete document record
        db.delete(document)

        db.commit()

        return document

    except Exception as e:
        db.rollback()
        raise e