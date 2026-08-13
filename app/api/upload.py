from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.document import DocumentResponse
from app.services.document_upload_service import upload_document

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post(
    "/upload",
    response_model=DocumentResponse,)

def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),):

    """
    Upload a document and return the stored document details.
    """
    return upload_document(
        db=db,
        file=file,
    )