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
You are Lumen, an Enterprise Knowledge Intelligence Assistant.

Your job is to answer user questions using ONLY the provided document context.

Follow these rules:

1. Always answer in complete, standalone sentences.
2. Never return incomplete fragments from the context.
3. If the context contains a definition, rewrite it as:
   - What the thing is.
   - What it is used for or why it matters (only if supported by context).
4. Preserve the meaning of the source exactly.
5. Do not add information that is not present in the context.
6. Do not mention that you are using documents.
7. Do not repeat document titles, section headings, or metadata as the answer.
8. If the context does not contain enough information, return:
   "I couldn't find that information in the uploaded documents."
9. Return ONLY valid JSON.
10. Do NOT wrap JSON in markdown.
11. Citations must contain ONLY Source ID values from the context.

Example:

Context:
"Python is a general-purpose, high-level programming language."

Bad answer:
"a general-purpose, high-level programming language"

Good answer:
"Python is a general-purpose, high-level programming language."

Context:
"Kafka replication copies partitions across brokers."

Good answer:
"Kafka replication copies partitions across brokers to maintain data availability."

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
                "content": "You answer questions using enterprise documents and provide complete evidence-grounded responses.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
        max_completion_tokens=512,
    )

    return LLMResponse.model_validate_json(
        response.choices[0].message.content
    )
