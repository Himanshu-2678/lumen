from sqlalchemy.orm import Session
from app.models.document import Document
import os
from app.vectorstore.chroma_client import collection
from fastapi import HTTPException

def create_document(
    db: Session,
    filename: str,
    file_type: str,
    file_path: str) -> Document:

    document = Document(
        filename=filename,
        file_type=file_type,
        file_path=file_path
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def get_documents(db: Session):
    return db.query(Document).all()


def delete_document(db: Session, document_id: int):
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

        # Delete embeddings
        collection.delete(
            where={"document_id": document_id}
        )

        # Delete database record
        db.delete(document)
        db.commit()

        return document

        except Exception as e:
            db.rollback()
            raise e