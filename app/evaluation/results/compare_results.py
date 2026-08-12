import json
from pathlib import Path

BASELINE_PATH = Path("app/evaluation/results/baseline_ragas_results.json")
RERANKED_PATH = Path("app/evaluation/results/ragas_results.json")


def load_results(path: Path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def average_metric(results, metric):
    values = [
        item[metric]
        for item in results
        if metric in item and item[metric] is not None
    ]

    if not values:
        return 0.0

    return round(sum(values) / len(values), 3)


def compare():
    baseline_results = load_results(BASELINE_PATH)
    reranked_results = load_results(RERANKED_PATH)

    metrics = [
        "faithfulness",
        "answer_relevancy",
        "context_precision",
    ]

    print()
    print("=" * 60)
    print("LUMEN RAG EVALUATION COMPARISON")
    print("=" * 60)
    print()
    print(f"Baseline samples : {len(baseline_results)}")
    print(f"Reranked samples : {len(reranked_results)}")
    print()
    print(
        f"{'Metric':<25}"
        f"{'Baseline':<15}"
        f"{'Reranked':<15}"
        f"{'Change':<10}"
    )
    print("-" * 60)

    for metric in metrics:
        baseline_score = average_metric(baseline_results, metric)
        reranked_score = average_metric(reranked_results, metric)
        change = round(reranked_score - baseline_score, 3)

        print(
            f"{metric:<25}"
            f"{baseline_score:<15}"
            f"{reranked_score:<15}"
            f"{change:<10}"
        )

    print()
    print("=" * 60)


if __name__ == "__main__":
    compare()