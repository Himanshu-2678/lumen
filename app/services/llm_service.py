from groq import Groq
from app.core.config import settings
import json
from app.schemas.query import LLMResponse


client = Groq(api_key=settings.GROQ_API_KEY)

def generate_answer(question: str, retrieved_chunks: list[dict]) -> LLMResponse:
    """
    Generate an answer using the retrieved document chunks.
    """
    context = ""

    for chunk in retrieved_chunks:
        context += (
            f"[Chunk ID: {chunk['id']}]\n"
            f"{chunk['text']}\n\n"
        )

    prompt = f"""
    You are an Enterprise Knowledge Assistant.

    Answer ONLY using the provided context.

    Rules:
    1. Never use outside knowledge.
    2. If the answer is not present, return:
    "I couldn't find that information in the uploaded documents."
    3. Return ONLY valid JSON.
    4. Do NOT wrap the JSON in markdown.
    5. The citations array must contain ONLY the Chunk IDs that directly support your answer.

    Context:
    {context}

    Question:
    {question}

    Return ONLY a valid JSON object.

    The JSON schema is:

    {
        "answer": string,
        "citations": [
            string
        ]
    }
    """

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You answer questions using enterprise documents."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"},  
        temperature=0.2,
        max_completion_tokens=512
    )

    content = response.choices[0].message.content

    return LLMResponse.model_validate_json(content)