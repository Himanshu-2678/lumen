# FastAPI should not directly expose database models.
from pydantic import BaseModel

class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    status: str
    file_path: str 
    model_config = {
        "from_attributes": True
    }