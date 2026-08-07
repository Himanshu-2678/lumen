from fastapi import APIRouter
from pydantic import BaseModel

from app.services.hybrid_retrieval_service import hybrid_search
from app.services.confidence_service import calculate_confidence
from app.services.context_service import build_context
from app.services.llm_service import generate_answer
from app.schemas.query import QueryResponse
from app.services.citation_service import build_citations
from app.services.answer_guard_service import can_generate_answer

router = APIRouter(prefix="/query", tags=["Query"])


class QueryRequest(BaseModel):
    question: str


@router.post("/", response_model=QueryResponse)
def query_documents(request: QueryRequest):
    retrieved_chunks = hybrid_search(query=request.question)

    confidence = calculate_confidence(retrieved_chunks)

    if not can_generate_answer(confidence):
        return {
            "question": request.question,
            "answer": "I couldn't find enough evidence in the uploaded documents to answer this question.",
            "confidence": confidence,
            "sources": []
        }

    context = build_context(retrieved_chunks)

    llm_response = generate_answer(question=request.question, context=context)

    answer = llm_response.answer
    citation_ids = set(llm_response.citations)

    sources = build_citations(retrieved_chunks, list(citation_ids))
    
    return {
        "question": request.question,
        "answer": answer,
        "confidence": confidence,
        "sources": sources,
    }