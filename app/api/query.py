from fastapi import APIRouter
from pydantic import BaseModel

from app.services.llm_service import generate_answer
from app.services.hybrid_retrieval_service import hybrid_search
from app.services.confidence_service import calculate_confidence
from app.schemas.query import QueryResponse

router = APIRouter(prefix="/query", tags=["Query"])


class QueryRequest(BaseModel):
    question: str


@router.post(
    "/",
    response_model=QueryResponse,
)
def query_documents(request: QueryRequest):
    retrieved_chunks = hybrid_search(query=request.question)

    llm_response = generate_answer(
        question=request.question,
        retrieved_chunks=retrieved_chunks,
    )

    answer = llm_response.answer
    citation_ids = set(llm_response.citations)

    sources = []
    seen = set()

    for chunk in retrieved_chunks:

        if chunk["id"] not in citation_ids:
            continue

        metadata = chunk["metadata"]
        key = (metadata["filename"], metadata["page_number"])

        if key in seen:
            continue

        seen.add(key)

        sources.append(
            {
                "filename": metadata["filename"],
                "page_number": metadata["page_number"],
            }
        )

    confidence = calculate_confidence(
        retrieved_chunks
    )

    return {
        "question": request.question,
        "answer": answer,
        "confidence": confidence,
        "sources": sources,
    }