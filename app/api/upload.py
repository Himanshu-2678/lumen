from fastapi import APIRouter, Depends, File, Request, Response, UploadFile
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.document import DocumentResponse
from app.services.document_upload_service import upload_document
from app.core.workspace import get_workspace_id

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post(
    "/upload",
    response_model=DocumentResponse,)

def upload_file(
    request: Request,
    response: Response,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),):

    """
    Upload a document and return the stored document details.
    """
    return upload_document(
        db=db,
        file=file,
        workspace_id=get_workspace_id(request, response),
    )