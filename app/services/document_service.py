from sqlalchemy.orm import Session
from app.models.document import Document

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