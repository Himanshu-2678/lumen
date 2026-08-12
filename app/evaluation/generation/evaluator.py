import json

from app.services.hybrid_retrieval_service import hybrid_search
from app.services.llm_service import generate_answer


def load_test_cases():
    with open("app/evaluation/dataset.json", "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_generation():
    test_cases = load_test_cases()
    results = []

    for index, case in enumerate(test_cases, start=1):
        chunks = hybrid_search(query=case["question"])
        response = generate_answer(
            question=case["question"],
            retrieved_chunks=chunks
        )

        retrieved_documents = list({
            chunk["metadata"]["filename"]
            for chunk in chunks
        })

        result = {
            "id": index,
            "question": case["question"],
            "expected_document": case["expected_document"],
            "retrieved_documents": retrieved_documents,
            "answer": response.answer,
            "citations": response.citations
        }

        results.append(result)

        print(
            f"[{index}/{len(test_cases)}] "
            f"{case['question']}"
        )
        print(
            f"  Expected: {case['expected_document']}"
        )
        print(
            f"  Retrieved: {retrieved_documents}"
        )
        print(
            f"  Answer: {response.answer}"
        )
        print(
            f"  Citations: {response.citations}"
        )

    return results


if __name__ == "__main__":
    evaluate_generation()