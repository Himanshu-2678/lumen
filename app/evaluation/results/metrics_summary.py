import json
from pathlib import Path

RESULTS_DIR = Path("app/evaluation/results")

BASELINE_RAGAS = RESULTS_DIR / "baseline_ragas_results.json"
RERANKED_RAGAS = RESULTS_DIR / "ragas_results.json"
BASELINE_CONTEXT = RESULTS_DIR / "baseline_context_precision_results.json"
RERANKED_CONTEXT = RESULTS_DIR / "context_precision_results.json"
GENERATED_SAMPLES = RESULTS_DIR / "generated_samples.json"
OUTPUT_PATH = RESULTS_DIR / "metrics_summary.json"


def load_json(path):
    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def average_metric(results, metric):
    values = [item[metric] for item in results if metric in item]

    if not values:
        return None

    return round(sum(values) / len(values), 3)


def calculate_change(before, after):
    if before is None or after is None:
        return None

    return round(after - before, 3)


def calculate_refusal_accuracy():
    samples = load_json(GENERATED_SAMPLES)

    refusal_samples = [
        sample
        for sample in samples
        if sample.get("expected_document") is None
    ]

    if not refusal_samples:
        return None

    correct = 0

    for sample in refusal_samples:
        answer = sample.get("answer", "").lower()

        if (
            "couldn't find" in answer
            or "could not find" in answer
            or "not enough evidence" in answer
        ):
            correct += 1

    return round(correct / len(refusal_samples), 3)


def main():
    baseline_ragas = load_json(BASELINE_RAGAS)
    reranked_ragas = load_json(RERANKED_RAGAS)
    baseline_context = load_json(BASELINE_CONTEXT)
    reranked_context = load_json(RERANKED_CONTEXT)

    total_questions = len(reranked_ragas)
    samples = load_json(GENERATED_SAMPLES)

    answerable = sum(
        1
        for item in samples
        if item.get("expected_document") is not None
    )

    unanswerable = total_questions - answerable

    baseline_metrics = {
        "faithfulness": average_metric(baseline_ragas, "faithfulness"),
        "answer_relevancy": average_metric(
            baseline_ragas,
            "answer_relevancy",
        ),
        "context_precision": average_metric(
            baseline_context,
            "context_precision",
        ),
    }

    reranked_metrics = {
        "faithfulness": average_metric(reranked_ragas, "faithfulness"),
        "answer_relevancy": average_metric(
            reranked_ragas,
            "answer_relevancy",
        ),
        "context_precision": average_metric(
            reranked_context,
            "context_precision",
        ),
    }

    changes = {
        metric: calculate_change(
            baseline_metrics[metric],
            reranked_metrics[metric],
        )
        for metric in baseline_metrics
    }

    summary = {
        "dataset": {
            "total_questions": total_questions,
            "answerable_questions": answerable,
            "unanswerable_questions": unanswerable,
        },
        "baseline": baseline_metrics,
        "reranked": reranked_metrics,
        "improvement": changes,
        "refusal_accuracy": calculate_refusal_accuracy(),
        "decision": {
            "reranking_improved_faithfulness": (
                changes["faithfulness"] is not None
                and changes["faithfulness"] > 0
            ),
            "selected_strategy": "hybrid retrieval + cross encoder reranking",
        },
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)

    print()
    print("=" * 70)
    print("LUMEN RAG FINAL EVALUATION SUMMARY")
    print("=" * 70)
    print()

    print("Dataset")
    print("------------------------------")
    print(f"Total Questions: {total_questions}")
    print(f"Answerable: {answerable}")
    print(f"Unanswerable: {unanswerable}")

    print()
    print("RAG Metrics")
    print("------------------------------")
    print(
        f"{'Metric':<25}"
        f"{'Baseline':<15}"
        f"{'Reranked':<15}"
        f"{'Change':<10}"
    )
    print("-" * 70)

    for metric in baseline_metrics:
        print(
            f"{metric:<25}"
            f"{str(baseline_metrics[metric]):<15}"
            f"{str(reranked_metrics[metric]):<15}"
            f"{str(changes[metric]):<10}"
        )

    print()
    print("Safety Evaluation")
    print("------------------------------")
    print(f"Refusal Accuracy: {summary['refusal_accuracy']}")

    print()
    print("Decision")
    print("------------------------------")

    if summary["decision"]["reranking_improved_faithfulness"]:
        print("Cross encoder reranking improved grounding.")
        print("Reranking retained as retrieval enhancement.")
    else:
        print("Reranking did not improve faithfulness.")

    print()
    print(f"Saved summary: {OUTPUT_PATH}")
    print("=" * 70)


if __name__ == "__main__":
    main()