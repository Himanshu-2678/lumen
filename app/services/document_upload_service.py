from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.services.file_service import save_uploaded_file
from app.services.document_service import create_document

def upload_document(
    db: Session,
    file: UploadFile
):
    file_path = save_uploaded_file(file)

    document = create_document(
        db=db,
        filename=file.filename,
        file_type=file.filename.split(".")[-1],
        file_path=file_path
    )

    return document