import json

from app.services.hybrid_retrieval_service import hybrid_search
from app.services.context_service import build_context
from app.services.llm_service import generate_answer
from app.evaluation.generation.metrics import (
    answer_relevance,
    citation_accuracy,
    faithfulness,
)


def load_test_cases():
    with open("app/evaluation/generation/test_case.json", "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_generation():
    test_cases = load_test_cases()
    results = []

    for case in test_cases:
        print("\nQuestion:")
        print(case["question"])

        chunks = hybrid_search(query=case["question"])
        context = build_context(chunks)
        response = generate_answer(question=case["question"], context=context)

        relevance = answer_relevance(response.answer, case["expected_keywords"])
        citation_score = citation_accuracy(response.citations, case["expected_sources"])
        faithfulness_score = faithfulness(response.answer, context)

        result = {
            "question": case["question"],
            "answer_relevance": relevance,
            "citation_accuracy": citation_score,
            "faithfulness": faithfulness_score,
        }

        results.append(result)
        print(result)

    return results


if __name__ == "__main__":
    evaluate_generation()