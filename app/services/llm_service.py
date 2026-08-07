from groq import Groq
from app.core.config import settings
from app.schemas.query import LLMResponse

client = Groq(api_key=settings.GROQ_API_KEY)


def generate_answer(question: str, context: str) -> LLMResponse:
    """Generate an answer using prepared document context."""

    prompt = f"""You are an Enterprise Knowledge Assistant.
Answer ONLY using the provided context.

Rules:
1. Answer the user's question directly using the evidence.
2. Do not repeat document titles or headings as answers.
3. Summarize the relevant information from the evidence.
4. Never use outside knowledge.
5. If the answer is not present, return:
"I couldn't find that information in the uploaded documents."
6. Return ONLY valid JSON.
7. Do NOT wrap JSON in markdown.
8. The citations array must contain ONLY the Source ID values that support the answer.
9. The citations array must contain ONLY the Source ID values that support the answer.

Context:
{context}
Question:
{question}

Return ONLY this JSON:
{{"answer":"string","citations":["string"]}}"""

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You answer questions using enterprise documents."},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
        max_completion_tokens=512,
    )

    return LLMResponse.model_validate_json(response.choices[0].message.content)