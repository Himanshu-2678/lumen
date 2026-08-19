from pydantic import BaseModel
from pydantic import Field

class Source(BaseModel):
    filename: str
    page_number: int
    quote: str

class ConfidenceSignals(BaseModel):
    retrieval_agreement: bool | None = None
    retrieval_methods: list[str] = Field(default_factory=list)
    supporting_chunks: int | None = None
    top_reranker_score: float | None = None
    reason: str | None = None

class Confidence(BaseModel):
    confidence_score: float
    confidence_level: str
    signals: ConfidenceSignals

class QueryResponse(BaseModel):
    question: str
    answer: str
    confidence: dict
    sources: list[Source]

class LLMResponse(BaseModel):
    answer: str
    citations: list[str] = Field(default_factory=list)