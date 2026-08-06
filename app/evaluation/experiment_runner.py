from app.db.session import SessionLocal
from app.evaluation.evaluator import load_dataset
from app.evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)
from app.services.bm25_service import bm25_search
from app.services.hybrid_retrieval_service import hybrid_search
from app.services.retrieval_service import retrieve_chunks


def evaluate_system(system_name, retrieval_function, k=5):
    dataset = load_dataset()

    recall_scores = []
    precision_scores = []
    mrr_scores = []

    db = SessionLocal()

    try:
        for item in dataset:
            question = item["question"]
            expected_chunks = item["expected_chunks"]

            if system_name == "BM25":
                results = retrieval_function(db=db, query=question, top_k=k,)

            elif system_name == "Hybrid + Reranker":
                results = retrieval_function(query=question, final_top_k=k,)

            else:
                results = retrieval_function(query=question, top_k=k,)

            retrieved_ids = [chunk["id"] for chunk in results]

            recall_scores.append(recall_at_k(retrieved_ids, expected_chunks, k))
            precision_scores.append(precision_at_k(retrieved_ids, expected_chunks, k))
            mrr_scores.append(reciprocal_rank(retrieved_ids, expected_chunks))

    finally:
        db.close()

    return {
        "System": system_name,
        "Recall@K": round(sum(recall_scores) / len(recall_scores), 3),
        "Precision@K": round(sum(precision_scores) / len(precision_scores), 3),
        "MRR": round(sum(mrr_scores) / len(mrr_scores), 3),
    }


def run_experiments():
    systems = [
        ("Vector Search", retrieve_chunks),
        ("BM25", bm25_search),
        ("Hybrid + Reranker", hybrid_search),
    ]

    results = []

    for name, function in systems:
        result = evaluate_system(system_name=name, retrieval_function=function)
        results.append(result)

    print("\nEvaluation Comparison")
    print("=" * 60)

    for result in results:
        print(result)


if __name__ == "__main__":
    run_experiments()