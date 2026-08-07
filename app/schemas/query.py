from pydantic import BaseModel

class Source(BaseModel):
    filename: str
    page_number: int
    quote: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    confidence: dict
    sources: list[Source]

class LLMResponse(BaseModel):
    answer: str
    citations: list[str]