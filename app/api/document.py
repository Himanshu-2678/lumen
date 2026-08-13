from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.schemas.document import DocumentResponse
from app.services.document_service import get_documents, delete_document

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.get("", response_model=list[DocumentResponse])
def get_documents_endpoint(db: Session = Depends(get_db)):
    return get_documents(db)

@router.delete("/{document_id}")
def delete_document_endpoint(document_id: int, db: Session = Depends(get_db)):
    document = delete_document(db=db, document_id=document_id)

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return {"message": "Document deleted successfully."}