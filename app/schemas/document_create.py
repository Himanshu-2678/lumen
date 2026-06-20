from pydantic import BaseModel

class DocumentCreate(BaseModel):
    filename: str
    file_type: str