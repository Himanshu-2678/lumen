from datetime import datetime

from pydantic import BaseModel

class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    status: str
    file_path: str
    chunk_count: int
    error_message: str | None
    created_at: datetime | None
    updated_at: datetime | None

    model_config = {
        "from_attributes": True
    }