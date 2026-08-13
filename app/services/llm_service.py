from groq import Groq

from app.core.config import settings
from app.schemas.query import LLMResponse
from app.services.context_service import build_context

_client = None


def get_client():
    global _client

    if _client is None:
        _client = Groq(api_key=settings.GROQ_API_KEY)

    return _client


def generate_answer(
    question: str,
    retrieved_chunks: list[dict],
) -> LLMResponse:
    context = build_context(retrieved_chunks)

    prompt = f"""
You are an Enterprise Knowledge Assistant.

Answer ONLY using the provided context.

Rules:
1. Answer the user's question directly using the evidence.
2. Do not use outside knowledge.
3. Do not repeat document titles or headings as answers.
4. If information is not present, return:
"I couldn't find that information in the uploaded documents."
5. Return ONLY valid JSON.
6. Do NOT wrap JSON in markdown.
7. Citations must contain ONLY Source ID values.

Context:
{context}

Question:
{question}

Return:

{{"answer":"string","citations":["string"]}}
"""

    client = get_client()

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You answer questions using enterprise documents.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
        max_completion_tokens=512,
    )

    return LLMResponse.model_validate_json(
        response.choices[0].message.content
    )
