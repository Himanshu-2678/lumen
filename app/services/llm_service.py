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

1. Answer the user's question directly and clearly.
2. Provide a concise explanation, not just a definition or one-line response.
3. Include important details, examples, or context only when they are supported by the documents.
4. Do not use outside knowledge or assumptions.
5. If the context does not contain enough information, return:
   "I couldn't find enough evidence in the uploaded documents to answer this question."
6. Do not mention that you are using context or documents.
7. Do not repeat document titles, headings, or filenames as the answer.
8. Return ONLY valid JSON.
9. Do NOT wrap JSON in markdown.
10. Citations must contain ONLY Source ID values.

Answer style:
- Prefer 2-5 sentences for normal questions.
- Use bullet points only when explaining multiple items.
- Avoid extremely short answers unless the question requires a short answer.

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
