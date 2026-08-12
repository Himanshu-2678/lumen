import asyncio
import json
from pathlib import Path

from openai import AsyncOpenAI
from ragas.embeddings import HuggingFaceEmbeddings
from ragas.llms import llm_factory
from ragas.metrics.collections import (
    Faithfulness,
    AnswerRelevancy,
    #ContextPrecisionWithoutReference,
)

from app.core.config import settings

RESULTS_PATH = Path("app/evaluation/results/generated_samples.json")
RAGAS_RESULTS_PATH = Path("app/evaluation/results/ragas_results.json")


def load_generated_samples():
    with open(RESULTS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def load_existing_ragas_results():
    if not RAGAS_RESULTS_PATH.exists():
        return []

    if RAGAS_RESULTS_PATH.stat().st_size == 0:
        return []

    with open(RAGAS_RESULTS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def save_ragas_results(results):
    RAGAS_RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    temp_path = RAGAS_RESULTS_PATH.with_suffix(".tmp")

    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    temp_path.replace(RAGAS_RESULTS_PATH)


def create_evaluator_llm():
    client = AsyncOpenAI(
        api_key=settings.GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
    )

    return llm_factory(
        settings.GROQ_EVAL_MODEL,
        client=client,
        temperature=0.0,
    )


def create_evaluator_embeddings():
    return HuggingFaceEmbeddings(model="BAAI/bge-small-en-v1.5")


async def evaluate_sample(
    sample,
    faithfulness_metric,
    relevancy_metric,
    #context_precision_metric,
):
    faithfulness_result = await faithfulness_metric.ascore(
        user_input=sample["question"],
        response=sample["answer"],
        retrieved_contexts=sample["retrieved_contexts"],
    )

    relevancy_result = await relevancy_metric.ascore(
        user_input=sample["question"],
        response=sample["answer"],
    )

    """context_precision_result = await context_precision_metric.ascore(
        user_input=sample["question"],
        response=sample["answer"],
        retrieved_contexts=sample["retrieved_contexts"],
    )"""

    return {
        "question": sample["question"],
        "expected_document": sample["expected_document"],
        "faithfulness": faithfulness_result.value,
        "answer_relevancy": relevancy_result.value,
        #"context_precision": context_precision_result.value,
    }


async def run_evaluation():
    samples = load_generated_samples()

    if not samples:
        raise RuntimeError("No generated evaluation samples found.")

    print(f"Loaded {len(samples)} generated samples.")

    existing_results = load_existing_ragas_results()

    completed_questions = {
        result["question"]
        for result in existing_results
    }

    evaluator_llm = create_evaluator_llm()
    evaluator_embeddings = create_evaluator_embeddings()

    faithfulness_metric = Faithfulness(llm=evaluator_llm)

    relevancy_metric = AnswerRelevancy(
        llm=evaluator_llm,
        embeddings=evaluator_embeddings,
    )

    """context_precision_metric = ContextPrecisionWithoutReference(
        llm=evaluator_llm
    )"""

    total = len(samples)

    for index, sample in enumerate(samples, start=1):
        question = sample["question"]

        if question in completed_questions:
            print(f"[{index}/{total}] SKIPPED - already evaluated")
            continue

        print(f"[{index}/{total}] Evaluating: {question}")

        try:
            result = await evaluate_sample(
                sample,
                faithfulness_metric,
                relevancy_metric,
                #context_precision_metric,
            )

            existing_results.append(result)
            save_ragas_results(existing_results)
            await asyncio.sleep(60)

            print(f"  Faithfulness: {result['faithfulness']:.3f}")
            print(f"  Answer Relevancy: {result['answer_relevancy']:.3f}")
            #print(f"  Context Precision: {result['context_precision']:.3f}")
            print("  SAVED")

        except Exception as error:
            print(f"  FAILED: {type(error).__name__}: {error}")

            save_ragas_results(existing_results)

            print("  Waiting before retry...")
            await asyncio.sleep(60)

            # retry same question
            continue
        
    print()
    print("================================")
    print("RAGAS EVALUATION COMPLETE")
    print("================================")
    print(f"Evaluated: {len(existing_results)}/{total}")
    print(f"Results: {RAGAS_RESULTS_PATH}")


if __name__ == "__main__":
    asyncio.run(run_evaluation())