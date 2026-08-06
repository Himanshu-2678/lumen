import json
from pathlib import Path

from app.evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)
from app.services.hybrid_retrieval_service import hybrid_search

DATASET_PATH = Path("app/evaluation/dataset.json")


def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate(k: int = 5):
    dataset = load_dataset()

    recall_scores = []
    precision_scores = []
    mrr_scores = []

    for item in dataset:
        question = item["question"]
        expected_chunks = item["expected_chunks"]

        results = hybrid_search(query=question, final_top_k=k)
        retrieved_ids = [chunk["id"] for chunk in results]

        recall_scores.append(recall_at_k(retrieved_ids, expected_chunks, k))
        precision_scores.append(precision_at_k(retrieved_ids, expected_chunks, k))
        mrr_scores.append(reciprocal_rank(retrieved_ids, expected_chunks))

        print("\nQuestion:")
        print(question)

        print("Retrieved:")
        print(retrieved_ids)

        print("Expected:")
        print(expected_chunks)

    print("\n==============================")
    print("Evaluation Results")
    print("==============================")

    print(f"Recall@{k}: {sum(recall_scores) / len(recall_scores):.2f}")
    print(f"Precision@{k}: {sum(precision_scores) / len(precision_scores):.2f}")
    print(f"MRR: {sum(mrr_scores) / len(mrr_scores):.2f}")


if __name__ == "__main__":
    evaluate()