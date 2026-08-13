from datetime import datetime

from pydantic import BaseModel

class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    status: str
    chunk_count: int
    error_message: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {
        "from_attributes": True
    }