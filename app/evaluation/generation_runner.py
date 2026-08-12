import json
from pathlib import Path

from app.services.reranker_service import rerank_chunks
from app.services.hybrid_retrieval_service import hybrid_search
from app.services.llm_service import generate_answer

DATASET_PATH = Path("app/evaluation/dataset.json")
RESULTS_PATH = Path("app/evaluation/results/generated_samples.json")


def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def load_existing_results():
    if not RESULTS_PATH.exists():
        return []

    if RESULTS_PATH.stat().st_size == 0:
        return []

    with open(RESULTS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def save_results(results):
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    temp_path = RESULTS_PATH.with_suffix(".tmp")

    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    temp_path.replace(RESULTS_PATH)


def generate_evaluation_samples():
    test_cases = load_dataset()
    results = load_existing_results()

    completed_questions = {result["question"] for result in results}
    total = len(test_cases)

    for index, case in enumerate(test_cases, start=1):
        question = case["question"]

        if question in completed_questions:
            print(f"[{index}/{total}] SKIPPED - already generated")
            continue

        print(f"[{index}/{total}] {question}")

        try:
            # 1. Hybrid retrieval
            retrieved_chunks = hybrid_search(query=question)

            # 2. Rerank retrieved chunks
            # Keep only strongest evidence
            reranked_chunks = rerank_chunks(
                query=question,
                retrieved_chunks=retrieved_chunks,
                top_k=3,
            )

            # 3. Generate answer using reranked evidence
            response = generate_answer(
                question=question,
                retrieved_chunks=reranked_chunks,
            )

            # 4. Store only reranked evidence for evaluation
            retrieved_contexts = [chunk["text"] for chunk in reranked_chunks]

            retrieved_source_ids = [chunk["id"] for chunk in reranked_chunks]

            retrieved_documents = list(
                dict.fromkeys(
                    chunk["metadata"]["filename"]
                    for chunk in reranked_chunks
                )
            )

            sample = {
                "question": question,
                "expected_document": case.get("expected_document"),
                "answer": response.answer,
                "citations": response.citations,
                "retrieved_contexts": retrieved_contexts,
                "retrieved_source_ids": retrieved_source_ids,
                "retrieved_documents": retrieved_documents,
            }

            results.append(sample)
            save_results(results)

            print("  SAVED")

        except Exception as error:
            print(f"  FAILED: {type(error).__name__}: {error}")
            save_results(results)
            raise

    print()
    print("================================")
    print("GENERATION COMPLETE")
    print("================================")
    print(f"Total dataset questions: {total}")
    print(f"Saved samples: {len(results)}")
    print(f"Results file: {RESULTS_PATH}")


if __name__ == "__main__":
    generate_evaluation_samples()