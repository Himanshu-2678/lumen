from pathlib import Path
from fastapi import UploadFile
from app.core.config import settings

def save_uploaded_file(file: UploadFile) -> str:
    upload_dir = Path(settings.UPLOAD_DIR)

    upload_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = upload_dir / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return str(file_path)