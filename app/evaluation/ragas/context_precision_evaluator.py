import asyncio
import json
from pathlib import Path

from openai import AsyncOpenAI
from ragas.llms import llm_factory
from ragas.metrics.collections import ContextPrecisionWithoutReference

from app.core.config import settings

SAMPLES_PATH = Path("app/evaluation/results/baseline_generated_samples.json")
OUTPUT_PATH = Path("app/evaluation/results/baseline_context_precision_results.json")


def load_samples():
    with open(SAMPLES_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def load_existing():
    if not OUTPUT_PATH.exists():
        return []

    if OUTPUT_PATH.stat().st_size == 0:
        return []

    with open(OUTPUT_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def save_results(results):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)


def create_llm():
    client = AsyncOpenAI(
        api_key=settings.GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
    )

    return llm_factory(
        settings.GROQ_EVAL_MODEL,
        client=client,
        temperature=0.0,
    )


async def run():
    samples = load_samples()
    results = load_existing()

    completed = {x["question"] for x in results}

    llm = create_llm()

    metric = ContextPrecisionWithoutReference(llm=llm)

    for index, sample in enumerate(samples, start=1):
        question = sample["question"]

        if question in completed:
            print(f"[{index}/{len(samples)}] SKIPPED")
            continue

        print(f"[{index}/{len(samples)}] {question}")

        try:
            score = await metric.ascore(
                user_input=sample["question"],
                response=sample["answer"],
                retrieved_contexts=sample["retrieved_contexts"],
            )

            result = {
                "question": question,
                "context_precision": score.value,
            }

            results.append(result)
            save_results(results)

            print(f"  Context Precision: {score.value:.3f}")

            # Groq protection
            await asyncio.sleep(60)

        except Exception as e:
            print(f"FAILED: {type(e).__name__}: {e}")
            save_results(results)
            await asyncio.sleep(60)

    print()
    print("==============================")
    print("CONTEXT PRECISION COMPLETE")
    print("==============================")
    print(f"Evaluated: {len(results)}/{len(samples)}")


if __name__ == "__main__":
    asyncio.run(run())