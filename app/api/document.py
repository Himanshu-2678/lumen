from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.document_create import DocumentCreate
from app.schemas.document import DocumentResponse
from app.services.document_service import create_document
from app.services.document_service import create_document, get_documents

router = APIRouter()


@router.post(
    "/documents",
    response_model=DocumentResponse
)

def create_document_endpoint(
    document: DocumentCreate,
    db: Session = Depends(get_db)):
    
    return create_document(
        db=db,
        filename=document.filename,
        file_type=document.file_type
    )


@router.get(
    "/documents",
    response_model=list[DocumentResponse])

def get_documents_endpoint(
    db: Session = Depends(get_db)):

    return get_documents(db)