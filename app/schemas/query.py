from pydantic import BaseModel

class Source(BaseModel):
    filename: str
    page_number: int

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list[Source]

class LLMResponse(BaseModel):
    answer: str
    citations: list[str]